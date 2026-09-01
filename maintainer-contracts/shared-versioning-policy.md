# 版本治理规则

这份规则描述多 Skill 家族的版本理解方式和升级边界。每个 Skill 独立版本、独立发布，不使用仓库级单一版本替代包版本。

## 当前发布线

| Skill | 当前版本 | 边界 |
| --- | --- | --- |
| `huifu-pay-integration` | `1.3.5` | 支付交易、checkout-js、通知、对账、SDK 与支付沙箱 |
| `huifu-merchant-onboarding` | `1.0.2` | 企业/个人商户进件、商户多费率配置及查询，以及企业/个人用户开户、企业/个人用户基本信息修改、用户业务入驻及修改、申请状态、用户信息和用户列表查询 |

- 十三个商户进件与管理接口当前锁定 `2026-08-31` 官方快照，共 2,183 个字段路径；九个用户接口同日复审，共554个字段路径。历史来源锁全部保持不可变。
- 当前进件 SDK 证据基线为 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24`；这不回写历史 `1.3.2` 版本事实。
- 两个 Skill 可单独升级和回滚；商户进件与用户开户能力随同一个进件包发布。
- 后续新增模块先按产品发布边界判断；属于进件管理的能力继续归入 `huifu-merchant-onboarding`。
- `skill_source` 优先使用外部显式合同值；缺失时支付使用 `hfps/1.3.5`，商户或用户接口都使用 `hfms/1.0.2`，两个 Skill 同时参与时使用 `hfps/1.3.5;hfms/1.0.2`。

## 当前主线

- `v1.0.x`：初始内容补齐和格式修正
- `v1.1.x`：结构升级和多语言底座
- `v1.2.x`：语言覆盖增强、模板增强、单 Skill 收敛
- `v1.3.x`：接入副驾驶、存量系统增量接入、联调问题排查、本地沙箱入口和上线检查
- `v1.3.5`：按本次维护窗口明确版本要求，增加交易分账明细查询、来源锁增量证明和三语言 SDK 能力边界
- `v1.3.5` 的 `2026-08-31` 同版本刷新：复审当前在线支付接口，关闭分账列表编码与聚合查询示例旧冲突
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
- 企业/个人进件、图片上传、业务开通、详情和申请状态的精确 API 路由；五个 JSON 接口已有三语言 SDK 证据，图片上传的官方专用实现当前只开放 Java，PHP/Python 允许图片专用受控通用 POST/自写 HTTPS 降级，进件回调协议不生成实现
- 六个商户进件接口的 1393 条完整字段路径、官网来源 SHA-256 和字段级外部资料索引
- Java 图片 `file_url` / 本地文件的 `BasePayClient.request/upload` 与 `isPage=true` 边界、PHP/Python 图片专用实现缺陷及受控降级合同，以及非图片接口的 Python 兼容性提示
- 用户侧版本与升级提示策略
- `HUIFU_SKILL_SOURCE` 显式配置时保持 `<skill_source>` 原样透传；未配置时官方联调和生产按当前请求实际参与生成的 Skill 组合使用 `hfps/1.3.5`、`hfms/1.0.2` 或 `hfps/1.3.5;hfms/1.0.2`，仅安装未参与的不计入。local-sandbox `1.0.1` 的冻结 r4 快照继续使用 `hfps/1.3.1;sandbox/1.0.1`
- `2026-06-10` API refresh：版本号仍保持 `1.3.0`，补充抖音直连下单、拆单支付订单查询和聚合字段差异
- `hf-payment-local-sandbox 1.0.1` 协议快照仍为 `huifu-pay-integration-1.3.0-r4`，report schema 为 `1.8`；当前支付 Skill `1.3.5` 也不修改该冻结契约或增加进件模拟端点

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
- `api-refresh-merchant-onboarding-1.0.1-2026-08-10-r2`：将五个 `/v2/user/*` 接口共354个字段路径纳入现有 `huifu-merchant-onboarding`，版本升为 `1.0.1`，默认来源标识为 `hfms/1.0.1`。
- `api-refresh-merchant-onboarding-2026-08-10-r1`：复审全部十一份商户接口实时来源；三页补全 `activated_products` 的 `01=一体化收款产品` 说明，字段路径和嵌套不变，Skill 版本保持 `1.0.1`。
- `api-refresh-merchant-onboarding-1.0.1-2026-08-10-r3`：将上述商户复审与五个用户接口来源锁合并到同一 `1.0.1` 发布合同。
- `sdk-only-correction-merchant-onboarding-1.0.1-2026-08-11-r2`：在 `1.0.1` 发布前撤销由历史源码快照误推的 Java/PHP TLS 硬停，恢复三语言官方 SDK 真实调用，并禁止手写 HTTP+签名替代；接口、字段、SDK 基线和来源标识不变。
- `api-refresh-merchant-multifee-config-2026-08-24-r1`：新增商户多费率配置27个完整路径与三语言 SDK 证据，进件 Skill 升级为 `1.0.2`，默认来源标识为 `hfms/1.0.2`。
- `api-refresh-merchant-multifee-query-2026-08-24-r2`：同版本新增商户多费率配置查询17个完整路径与三语言 SDK 证据，绑定独立 r2 来源锁并保留 r1 历史产物。
- `api-refresh-user-enterprise-modify-2026-08-24-r3`、`api-refresh-user-individual-modify-2026-08-24-r4`、`api-refresh-user-business-modify-2026-08-24-r5`、`api-refresh-user-list-query-2026-08-24-r6`：按用户指定版本 `1.0.2` 依次新增37、26、120、17个用户接口完整路径，逐轮只追加一份官方原文并保留全部历史锁。
- `api-refresh-trade-split-detail-query-2026-08-24`：新增交易分账明细查询29个完整路径与三语言 SDK 证据，支付 Skill 升级为 `1.3.5`；保留参数表 Array 与成功示例 String(JSON Array) 冲突，历史36页来源锁不变。
- 本轮维护窗口明确指定支付 `1.3.5`、进件 `1.0.2`，因此两项重要场景扩展采用指定补丁版本；来源锁与 refresh contract 必须记录完整新增范围，不能以补丁号掩盖能力变化。
- `api-refresh-payment-online-review-2026-08-31`：复审支付37页，修正聚合查询示例裁决和分账列表 String(JSON Array) 合同，支付 Skill 版本保持 `1.3.5`。
- `api-refresh-onboarding-online-review-2026-08-31`：复审商户十三页与用户九页，商户目录更新为2,183、用户目录保持554，进件 Skill 版本保持 `1.0.2`。
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
