# 版本治理规则

这份规则描述多 Skill 家族的版本理解方式和升级边界。每个 Skill 独立版本、独立发布，不使用仓库级单一版本替代包版本。

## 当前发布线

| Skill | 当前版本 | 边界 |
| --- | --- | --- |
| `huifu-pay-integration` | `1.3.3` | 支付交易、checkout-js、通知、对账、SDK 与支付沙箱 |
| `huifu-merchant-onboarding` | `1.0.0` | 企业/个人进件、图片、业务开通与修改、基础资料修改、费率、状态和短信 |

- 十一个进件接口当前锁定 `2026-07-29` 官方快照，共 2,111 个字段路径；企业进件新增请求 `material_card_info` 七个路径，其余十页与 `2026-07-28` 快照逐字节一致。此前的 `upper_huifu_id:String(18) C`、门店图片条件和详情 `material_card_info` 刷新继续保留。
- 当前进件 SDK 证据基线为 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24`；这不回写历史 `1.3.2` 版本事实。
- 两个 Skill 可单独升级和回滚；跨域任务才同时加载。
- 后续新增模块必须注册为新的 manifest Skill，不重新塞回支付或进件包。
- `skill_source` 优先使用外部显式合同值；缺失时按当前请求实际加载并参与生成的 Skill 集合取默认值：仅支付 `hfps/1.3.3`、仅进件 `hfms/1.0.0`、两者都参与 `hfps/1.3.3;hfms/1.0.0`。

## 当前主线

- `v1.0.x`：初始内容补齐和格式修正
- `v1.1.x`：结构升级和多语言底座
- `v1.2.x`：语言覆盖增强、模板增强、单 Skill 收敛
- `v1.3.x`：接入副驾驶、存量系统增量接入、联调问题排查、本地沙箱入口和上线检查
- `v2.x`：支付能力与进件能力拆分为独立 Skill 家族

## 历史 `1.3.2` 版本事实

`1.3.2` 这一版已经包含：

- 单 Skill 结构
- 平铺 `references/`
- 官方 PHP SDK 落地口径
- 官方 Python SDK 落地口径
- PHP SDK 包基线为 `huifurepo/dg-php-sdk 2.0.29`
- Python SDK 包基线为 `dg-sdk 2.0.23`；安装或版本核对失败时不得无版本安装或降级
- 聚合支付 PHP / Python 的下单、查询、关单、退款、对账边界
- 托管支付 PHP / Python 的预下单、查询、关单、退款、对账边界
- 接入向导、方案选择、18 张方案卡、问题解决中心、参数检查和上线检查
- 本地沙箱入口 `shared-local-sandbox.md`，用于 local-sandbox 本地协议模拟、报告校验、故障注入和上线前边界说明
- 企业/个人进件、图片上传、业务开通、详情和申请状态的精确 API 路由；五个 JSON 接口已有三语言 SDK 证据，图片只开放按语言区分的 `file_url` 受控片段，本地文件流与进件回调协议不生成实现
- 六个商户进件接口的 1393 条完整字段路径、官网来源 SHA-256 和字段级外部资料索引
- Java 图片 `file_url` 的 `isPage=true` 签名/验签边界、PHP `CURLFile` 阻断和 Python 空商户来源头兼容性提示
- 用户侧版本与升级提示策略
- `HUIFU_SKILL_SOURCE` 显式配置时保持 `<skill_source>` 原样透传；未配置时官方联调和生产按当前请求实际参与生成的 Skill 组合使用 `hfps/1.3.3`、`hfms/1.0.0` 或 `hfps/1.3.3;hfms/1.0.0`，仅安装未参与的不计入。local-sandbox `1.0.1` 的冻结 r4 快照继续使用 `hfps/1.3.1;sandbox/1.0.1`
- `2026-06-10` API refresh：版本号仍保持 `1.3.0`，补充抖音直连下单、拆单支付订单查询和聚合字段差异
- `hf-payment-local-sandbox 1.0.1` 协议快照仍为 `huifu-pay-integration-1.3.0-r4`，report schema 为 `1.8`；当前支付 Skill `1.3.3` 也不修改该冻结契约或增加进件模拟端点

## 何时需要升级版本

- 共享协议口径变化
- SDK 版本基线变化
- 产品线能力边界变化
- 本地沙箱能力边界、报告证据或公开分发口径变化
- 上传结构变化
- 重要场景新增或删除
- 如果维护窗口明确要求版本号不变，必须在版本事实中增加 `API refresh` 日期和刷新范围，避免同名版本内容漂移

## 同版本 API refresh

- `api-refresh-2026-07-28-r2`：刷新用户指定接口文档，修正高风险字段、类型、条件、路由和安全门禁；后续包版本同步见下一条。
- `api-refresh-2026-07-29-r3`：第五轮刷新企业进件 `material_card_info`，修复字段说明相对链接、坏锚点、规范截图和运行时 URL 分类；Skill 包版本保持不变。
- `skill-version-sync-2026-07-29-r1`：后续按维护要求将支付 Skill 包同步为 `1.3.3`、进件 Skill 包同步为 `1.0.0`，并与默认 `skill_source` 标识保持一致。
- 同版本刷新产物必须绑定 refresh ID、来源锁 SHA 和源提交，不得覆盖历史同版本产物。

## 每次发版建议同步更新

- 对应 Skill 的 `SKILL.md` 正文和 `agents/openai.yaml`
- `skills-manifest.json` 与对应 reference manifest
- `README.md`
- `CHANGELOG.md`
- `references/skill-version-policy.md`
- 新增或删除 reference 时同步仓库级 reference manifest
- 共享矩阵中的 SDK 版本口径
- Python references、共享矩阵和请求头策略中的 `dg-sdk` 版本口径
- 请求头策略中的版本号和 `skill-source` 规则
- 业务文档中的数量、日期和覆盖范围描述

## 不建议的做法

- 只改正文，不改版本说明
- 改了请求头或 SDK 版本，却不改共享矩阵
- 改了能力边界，却不改对应场景文档
