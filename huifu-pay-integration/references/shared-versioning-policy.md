# 版本治理规则

这份规则描述当前 Skill 包的版本理解方式和升级边界。

## 当前主线

- `v1.0.x`：初始内容补齐和格式修正
- `v1.1.x`：结构升级和多语言底座
- `v1.2.x`：语言覆盖增强、模板增强、单 Skill 收敛
- `v1.3.x`：接入副驾驶、存量系统增量接入、联调问题排查、本地沙箱入口和上线检查
- `v2.x`：如果再次出现目录结构或产品形态的重大调整，再考虑升主版本

## 当前版本事实

`1.3.1` 这一版已经包含：

- 单 Skill 结构
- 平铺 `references/`
- 官方 PHP SDK 落地口径
- 官方 Python SDK 落地口径
- PHP SDK 包基线为 `huifurepo/dg-php-sdk 2.0.27`
- Python SDK 包基线为 `dg-sdk 2.0.22`；安装或版本核对失败时不得无版本安装或降级
- 聚合支付 PHP / Python 的下单、查询、关单、退款、对账边界
- 托管支付 PHP / Python 的预下单、查询、关单、退款、对账边界
- 接入向导、方案选择、18 张方案卡、问题解决中心、参数检查和上线检查
- 本地沙箱入口 `shared-local-sandbox.md`，用于 local-sandbox 本地协议模拟、报告校验、故障注入和上线前边界说明
- 用户侧版本与升级提示策略
- `HUIFU_SKILL_SOURCE` 最终上送值保持 `<skill_source>` 原样透传；本地沙箱模式当前使用 `hfps/1.3.1;sandbox/1.0.0`，官方联调和生产使用 `hfps/1.3.1`
- `2026-06-10` API refresh：版本号仍保持 `1.3.0`，补充抖音直连下单、拆单支付订单查询和聚合字段差异
- `hf-payment-local-sandbox 1.0.0` 当前协议快照仍为 `huifu-pay-integration-1.3.0-r4`；Skill `1.3.1` 只新增使用入口和边界说明，不代表支付协议 contract bundle 被重命名

## 何时需要升级版本

- 共享协议口径变化
- SDK 版本基线变化
- 产品线能力边界变化
- 本地沙箱能力边界、报告证据或公开分发口径变化
- 上传结构变化
- 重要场景新增或删除
- 如果维护窗口明确要求版本号不变，必须在版本事实中增加 `API refresh` 日期和刷新范围，避免同名版本内容漂移

## 每次发版建议同步更新

- `SKILL.md` 正文中的“当前版本事实”
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
