---
name: huifu-pay-integration
description: "汇付支付交易集成：用于聚合支付、托管支付、checkout-js、下单、查单、关单、退款、对账、支付通知、签名验签、请求头、幂等、交易终态、本地沙箱和支付上线；不用于企业/个人商户进件、图片上传、商户业务开通、商户详情或申请状态查询，这些任务使用 huifu-merchant-onboarding。"
---

# 汇付支付集成

## 版权声明

本 Skill 中的汇付支付资料整理自上海汇付支付有限公司官方开放平台与官方产品文档；原始文档及其更新维护权归汇付支付官方所有。仅作技术学习交流与接口集成辅助使用，详见 `references/shared-copyright-notice.md`。

## 执行流程

1. 识别产品线、Endpoint、接入阶段、技术栈、端形态、当前目标和是否存量系统。完成标准：这些维度均已唯一确定，极速版产品场景与 V4 API 枚举已分开。
2. 检查下方硬检查点；命中时停止生成可运行实现，只问一个最高优先级问题。完成标准：已记录命中或未命中的具体理由，SDK 传输安全和调试日志均已检查。
3. 从精确路由中选择 3–5 份 reference。只有用户同时提出两个独立目标时才合并；完整 DTO、响应或嵌套字段任务必须包含完整字段目录。完成标准：每个目标均有一跳可达的原子接口页、合同定位路径、实际 JSON/解码路径（分别记录 wire 字段路径与 String(JSON) 解码后路径）和明确语言 adapter，不使用“对应文档”占位，也不把官网展示分组当成 wire key；只有官网明确标注“方便文档展示”时才从 wire 路径移除该分组。
4. 首次接入输出产品线判断和方案卡；存量接入输出新增、保留、人工确认和回归检查。完成标准：请求、前端交接、通知、终态和补偿查询责任均已落到具体组件。
5. 最后应用签名、验签、幂等、终态确认、请求字段保留和凭据安全规则。完成标准：每项均已检查，未知合同明确标记并停止生成相应实现。

字段说明中的链接按其用途处理：完整字段目录已将官网 `#锚点` / 相对链接解析到各自接口原始页，并保留相对地址原文；绝对地址保持官网值。已确认的坏锚点使用显式映射：`#业务返回码` 补公共返回码全集，聚合下单 `notify_url` 的“异步返回参数”同时映射正扫、反扫通知参数和通用异步消息规范。只有命中本次字段的规范文档、编码表或渠道指引才作为外部资料提示。`notify_url`、`jump_url`、下载地址、二维码等裸 URL 示例是运行时值或格式示例，不是默认值、推荐地址或外部资料。

本 Skill 只处理支付交易。企业、个人商户进件、图片资料、业务开通、商户详情和申请状态使用 `$huifu-merchant-onboarding`；不要从本 Skill 读取进件实现文档。

## 精确路由

| 场景 | 最小 reference 集 |
| --- | --- |
| 首次接入、产品线不明 | `references/shared-overview.md`、`references/copilot-onboarding.md`、`references/copilot-solution-selection.md` |
| 存量系统接入 | `references/copilot-existing-system.md`、`references/copilot-solution-selection.md` |
| 聚合支付快速接入 | `references/aggregation-quickstart.md`、`references/aggregation-customer-preparation.md` |
| 聚合下单参数或代码 | `references/aggregation-order.md`、`references/payment-complete-field-catalog.md`，按语言选择 `references/aggregation-java-adapter.md`、`references/aggregation-php-adapter.md` 或 `references/aggregation-python-adapter.md`，再按 `trade_type` 补微信/支付宝/银联分册 |
| 聚合交易查询 | `references/aggregation-query-payment-query.md` |
| 返回码、公共编码或术语 | `aggregation-error-codes.md`、`aggregation-common-params.md`；具体字段仍补对应原子接口页 |
| 聚合关单 | `references/aggregation-query-trade-close.md` |
| 聚合对账 | `references/aggregation-query-reconciliation.md` |
| 聚合退款或退款查询 | `references/aggregation-refund.md`、`references/payment-complete-field-catalog.md`，查询时补 `references/aggregation-refund-query.md` |
| 托管支付快速接入 | `references/hostingpay-quickstart.md`、`references/hostingpay-customer-preparation.md` |
| 托管预下单 | `references/hostingpay-preorder.md`、`references/payment-complete-field-catalog.md`，再按端形态补一个原子文档 |
| 抖音直连、`pre_order_type=4` | `references/hostingpay-preorder.md`、`references/hostingpay-preorder-douyin-direct.md` |
| 拆单支付查询、`splitpay/query` | `references/hostingpay-query.md`、`references/hostingpay-query-splitpay.md`；完整 DTO 同时执行下方完整字段目录路由 |
| 托管退款 | `references/hostingpay-refund.md`；完整 DTO 同时执行下方完整字段目录路由，Java setter 问题补 `references/hostingpay-faq.md` |
| 托管普通交易查询 | `references/hostingpay-query.md`、`references/hostingpay-query-payment-status-query.md` |
| 托管交易关单 | `references/hostingpay-query.md`、`references/hostingpay-query-trade-close.md` |
| 托管退款查询 | `references/hostingpay-refund.md`、`references/hostingpay-refund-query.md`；完整 DTO 同时执行下方完整字段目录路由 |
| 托管对账 | `references/hostingpay-query.md`、`references/hostingpay-query-reconciliation.md` |
| checkout-js 已完成服务端前置 | `references/checkout-js.md`、`references/checkout-js-callback-and-confirmation.md`、`references/hostingpay-async-webhook.md` |
| checkout-js 前置未确认 | `references/checkout-js-create-preorder-contract.md`，触发硬检查点 |
| 支付通知、重复通知、幂等 | `references/shared-async-notify.md`、`references/copilot-troubleshooting-playbooks.md` |
| 控台 Webhook 验签 | `references/shared-webhook-signing.md` |
| Java / PHP / Python SDK | 先读 `references/shared-server-sdk-matrix.md`；再按语言与产品线精确选择 `references/aggregation-java-adapter.md`、`references/hostingpay-java-adapter.md`、`references/aggregation-php-adapter.md`、`references/hostingpay-php-adapter.md`、`references/aggregation-python-adapter.md` 或 `references/hostingpay-python-adapter.md` |
| 请求头和 `skill_source` | `references/shared-request-header-policy.md` |
| DTO/Controller 字段保留 | `references/shared-request-field-preservation.md` |
| 完整 DTO、完整响应、嵌套字段或同名字段核对 | 对应原子接口页、`references/payment-complete-field-catalog.md`；代码任务再补语言 adapter |
| appid/openid、支付路由、对账或资金运营 FAQ | `references/payment-operations-faq.md`、`references/copilot-troubleshooting-playbooks.md` |
| 本地沙箱 | `references/shared-local-sandbox.md`，再补通知、查询或上线检查 |
| 上线前检查 | `references/copilot-go-live-checklist.md`、`references/copilot-existing-system.md` |
| 版本与升级 | `references/skill-version-policy.md` |

按语言选择 reference：

- Java：公共矩阵 + 产品线 Java adapter；先核对项目中的实际 SDK 版本和 Request 类。
- PHP：公共矩阵 + 产品线 PHP adapter；保留安全初始化顺序，但不得使用会启用 `DEBUG=true` 的官方 Demo/Composer loader。
- Python：公共矩阵 + 产品线 Python adapter；不要把 SDK 网络重试解释成业务重试。
- 前端：checkout-js 只负责展示与前端事件，支付终态仍由服务端确认。

## 🔴 CHECKPOINT · HARD STOP

命中以下任一情况时，首行输出 `🔴 CHECKPOINT · HARD STOP：硬检查点。`，列出当前判断和本轮 references，只问一个最高优先级问题：

1. 无法区分聚合支付、托管支付和 checkout-js。
2. 无法区分服务端接入、前端页面接入和最终状态确认。
3. 用户要求现成可运行代码，但当前接口、端形态或回退路径不唯一。
4. checkout-js 的托管预下单、支付通知验签/幂等和查单补偿未确认。
5. 用户要求联调或生产代码，但缺少环境、系统号、产品号、商户号、RSA 密钥安全来源、通知地址或必要渠道标识。未显式配置 `skill_source` 时使用下述确定性默认值，不因此硬停。
6. 本地 SDK 源码与文档在请求头、签名、版本或能力覆盖上冲突。
7. 用户要求 PHP 联调或生产可运行代码，但不能证明在加载 SDK、Demo/Composer 配置和调用 `BsPay::init` 之前已将全局 `DEBUG` 固定为 `false`，或仍使用会定义 `DEBUG=true` 的官方 Demo/Composer 入口。

SDK 安装、初始化和安全 loader 骨架不因产品线不明而硬停，但不得猜具体业务 Request 或字段；PHP 骨架必须在加载任何 SDK 文件前拒绝 `DEBUG=true`。

## 支付终态与通知

- 同步受理成功、`jump_url`、浏览器回跳和前端 callback 都不是支付终态。
- 对支付通知先验签，再校验金额、商户号、订单号和状态，最后做幂等更新。
- 通知缺失时使用官方查单补偿；不要伪造通知、跳过验签或直接改成功。
- 控台 Webhook 和接口 `notify_url` 是不同协议，不能混用签名位置或 ACK。
- 聚合下单的同一个 `notify_url` 同时承接正扫和反扫两套通知参数；按 `trade_type` 分场景解析，不得只实现一套。

## 请求和凭据

- 保留 Controller/DTO 已接收的 `req_date`、`req_seq_id`、金额、商户号和原交易定位键；缺失或非法时报错，不自行重写。
- 私钥、系统号和生产商户号只能从服务端安全配置读取，不能写入前端、日志、仓库或回答示例。
- PHP `2.0.30` 默认 `DEBUG=false`，但官方 `BsPayDemo/loader.php` 与 `Composer/BsPayConfig.php` 会在初始化前启用调试；调试日志会包含带 RSA 私钥的 `MerConfig`、完整请求和响应。联调/生产必须拒绝这些入口，并在加载任何 SDK 文件前固定 `DEBUG=false`。
- 未显式配置 `skill_source` 时，按当前请求实际加载并参与生成的 Skill 集合取值：仅本 Skill 使用 `hfps/1.3.4`；支付与进件两个 Skill 都参与当前请求时使用 `hfps/1.3.4;hfms/1.0.1`。仅安装在仓库但未参与当前请求不计入；顺序固定为支付、进件，使用一个英文分号且不加空格。
- 调用方显式提供经确认的 `skill_source` 合同值时原样透传；不得再追加 `sys_id`。
- 不因方便绕过 SDK 的签名、验签、证书或请求头路径。

## 官方 SDK-only 传输规则

- 接入方已确认官方 Lightning Java `1.0.5`、通用 Java `3.0.40`、PHP `2.0.30` 和 Python `2.0.24` SDK 不存在本 Skill 曾从历史源码快照推断的 TLS 问题；不得再据此触发 Java/PHP TLS 硬停。
- Java、PHP、Python 的真实请求都必须使用对应官方 SDK 的 Request/facade/client；不得为了“规避 TLS”或补齐语言示例而改写 `HttpClient`、OkHttp、Guzzle、curl 或自实现 HTTP+签名/验签客户端。
- SDK 缺少专属 Request 时先核对官方通用调用入口；仍无官方能力证据则明确报告能力缺口，不得用手写 HTTP 静默补位。
- TLS 证书链和主机名校验属于部署环境的常规上线检查。不得关闭校验或安装信任所有证书的自定义实现，但该检查不构成针对当前官方 Java/PHP SDK 的预设硬停。

## 本地沙箱边界

本地沙箱仅验证本地协议闭环、状态机、幂等、故障注入和报告，不验证真实商户权限、通道、费率、风控、资金结果或生产准入。冻结的 `r1–r4` 合同和样例包属于历史支付证据，不得因本次 Skill 拆分改名或重算。

## 输出要求

回答至少包含：

1. 当前产品线、阶段、技术栈和存量判断。
2. 本轮实际使用的 3–5 份 references。
3. 请求、通知、终态和安全边界。
4. 缺失信息、人工确认项和下一步。

不要输出费率、合规、通道准入或生产失败责任结论；只整理脱敏升级材料并转人工确认。

## 当前版本

| 项目 | 口径 |
| --- | --- |
| Skill 版本 | `1.3.4` |
| 能力范围 | 聚合支付、托管支付、checkout-js、支付通知、SDK、本地沙箱和支付上线 |
| 进件能力 | 已迁移至独立 `$huifu-merchant-onboarding` |
| 聚合支付 Java SDK | `dg-lightning-sdk 1.0.5` |
| 托管支付 Java SDK | `dg-java-sdk 3.0.40` |
| PHP SDK | `huifurepo/dg-php-sdk 2.0.30` |
| Python SDK | `dg-sdk 2.0.24`，import 为 `dg_sdk` |
