---
name: huifu-pay-integration
description: "汇付支付/斗拱支付（Huifu Payment）交易接入与排障。用于聚合支付、托管支付、余额支付、checkout-js及各端收银台，覆盖微信、支付宝、银联、抖音等渠道的预下单/下单、查单、关单、退款、合单、拆单/分账查询、对账，以及余额手续费试算、付款关系提交和短信验证码。支持Java/PHP/Python官方SDK、完整字段/DTO、签名验签、异步通知/Webhook、幂等、支付终态、查单补偿、本地沙箱与上线排查。进件、开户及业务开通使用huifu-merchant-onboarding；任务同时涉及开户开通与支付时联用两个skill。"
---

# 汇付支付集成

汇付官方资料的版权与使用边界见 `references/shared-copyright-notice.md`。

## 执行流程

1. 根据用户目标和现有项目确定产品线、目标接口及技术栈。首次接入先做产品选择；存量项目只改相关链路；字段或报错问题直接进入目标接口，不强制重做接入向导。
2. 按下表读取目标页。单字段查目标章节即可；完整 DTO、完整响应、嵌套字段或同名字段核对必须联读完整字段目录的对应接口与方向。代码任务再补语言 adapter 和公共 SDK 矩阵，不规定资料数量、不默认加载整份目录。
3. 字段输出区分合同定位路径、实际 JSON/解码路径、类型、长度、Y/N/C、枚举与条件。不把官网展示分组当成 wire key；只有官方明确“方便文档展示”或目录已记录接入方裁决时才移除。String(JSON) 按父路径逐层编码/解码，示例不作默认值。
4. 仅追问会影响当前接口选择或实际调用的缺口；继续不依赖回答的工作。字段、SDK差异或未知通知协议标记 `[需要官方确认]`，附官方来源，争议部分留 TODO/配置；不编造协议，也不要求先取得官方答复才能开发。

商户进件、图片、业务开通、商户详情及申请状态交接给 `$huifu-merchant-onboarding`。余额支付的交易、付款关系、试算和短信属于本 Skill。

交易报错先按支付接口排障；任务包含商户进件、业务开通、配置变更，或明确要求联合排查时，再联用进件 Skill。

进件审核通过不代表业务或支付渠道已开通。任务要求核对业务开通、商户或渠道状态再接支付时，联用进件 Skill 确认前置并交接支付；前置已确认且只实现支付时，只加载支付 Skill。

## 精确路由

| 场景 | 按需读取的 reference |
| --- | --- |
| 首次接入、产品线不明 | `references/shared-overview.md`；需要接入判断时补 `references/copilot-onboarding.md` |
| 存量系统接入 | `references/copilot-existing-system.md`、`references/copilot-solution-selection.md` |
| 聚合支付快速接入 | `references/aggregation-quickstart.md`、`references/aggregation-customer-preparation.md` |
| 聚合下单参数或代码 | `references/aggregation-order.md`，按语言选择 `references/aggregation-java-adapter.md`、`references/aggregation-php-adapter.md` 或 `references/aggregation-python-adapter.md`，再按 `trade_type` 补微信/支付宝/银联分册 |
| 聚合交易查询 | `references/aggregation-query-payment-query.md` |
| 返回码、公共编码或术语 | `references/aggregation-error-codes.md`、`references/aggregation-common-params.md`；具体字段仍补对应原子接口页 |
| 聚合关单 | `references/aggregation-query-trade-close.md` |
| 聚合对账 | `references/aggregation-query-reconciliation.md` |
| 聚合退款或退款查询 | `references/aggregation-refund.md`，查询时补 `references/aggregation-refund-query.md` |
| 余额支付整体接入 | `references/balancepay-overview.md`、`references/balancepay-field-contracts.md`，代码任务补余额支付语言 adapter |
| 余额支付下单 | `references/balancepay-pay.md`、`references/balancepay-field-contracts.md`，按语言补余额支付 adapter |
| 余额支付查询 | `references/balancepay-query.md`，代码任务补余额支付语言 adapter |
| 余额支付退款 | `references/balancepay-refund.md`、`references/balancepay-field-contracts.md`，代码任务补余额支付语言 adapter |
| 余额支付退款查询 | `references/balancepay-refund-query.md`，代码任务补余额支付语言 adapter |
| 手续费试算 | `references/balancepay-fee-calc.md`，代码任务补余额支付语言 adapter |
| 付款关系提交 | `references/balancepay-pay-relation.md`、`references/balancepay-field-contracts.md` |
| 余额支付短信验证码 | `references/balancepay-sms.md`、`references/balancepay-sdk-matrix.md`，代码任务补余额支付语言 adapter |
| 余额支付 SDK 或代码 | `references/balancepay-sdk-matrix.md`，按语言选择 `references/balancepay-java-adapter.md`、`references/balancepay-php-adapter.md` 或 `references/balancepay-python-adapter.md`，再补目标原子页与完整字段目录 |
| 托管支付快速接入 | `references/hostingpay-quickstart.md`、`references/hostingpay-customer-preparation.md` |
| 托管预下单 | `references/hostingpay-preorder.md`，再按端形态补一个原子文档 |
| 抖音直连、`pre_order_type=4` | `references/hostingpay-preorder.md`、`references/hostingpay-preorder-douyin-direct.md` |
| 拆单支付查询、`splitpay/query` | `references/hostingpay-query.md`、`references/hostingpay-query-splitpay.md`；完整字段按完整目录路由 |
| 交易分账明细、`trade/trans/split/query` | `references/trade-split-detail-query.md`；代码任务再补对应 Java/PHP/Python adapter |
| 托管退款 | `references/hostingpay-refund.md`；完整字段按完整目录路由，Java setter 问题补 `references/hostingpay-faq.md` |
| 托管普通交易查询 | `references/hostingpay-query.md`、`references/hostingpay-query-payment-status-query.md` |
| 托管交易关单 | `references/hostingpay-query.md`、`references/hostingpay-query-trade-close.md` |
| 托管退款查询 | `references/hostingpay-refund.md`、`references/hostingpay-refund-query.md`；完整字段按完整目录路由 |
| 托管对账 | `references/hostingpay-query.md`、`references/hostingpay-query-reconciliation.md` |
| checkout-js 已完成服务端前置 | `references/checkout-js.md`、`references/checkout-js-callback-and-confirmation.md`、`references/hostingpay-async-webhook.md` |
| checkout-js 前置未确认 | `references/checkout-js-create-preorder-contract.md`；缺口留待配置，先实现明确部分 |
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


## 需要暂停的操作

接口或实体不明确时只暂停依赖该选择的业务实现，问一个最关键问题；SDK安装、安全初始化及接口骨架可继续。缺真实环境、密钥或商户配置时使用服务端配置占位，不称为已可联调；真实调用前必须取得对应配置与授权。

遇到明确非法输入、验签失败、凭据泄露或未经授权的真实操作，停止受影响操作并说明原因；需要提示时用 `🔴 CHECKPOINT · HARD STOP`。不要为了生成代码要求用户证明既有环境已安全；代码本身应包含必要的启动校验。

## 支付终态与通知

- 同步受理、跳转地址、浏览器回跳及前端 callback 均不代表支付终态；校验业务状态后才更新订单。
- 通知先验签，校验金额、商户号、订单号与状态，再幂等更新；通知缺失时查单补偿，不伪造成功。
- 接口 `notify_url` 与控台 Webhook 的签名位置和 ACK 不混用；聚合下单同一通知地址承接正扫/反扫两套参数。验签后按通知 `resp_data.trans_type` 与已匹配原订单的 `trade_type` 核对并选择合同，不从通知读取未声明的 `trade_type`；缺失或冲突时通过原交易/查询核对。
- 抖音直连只明确了 `resp_data` 外层，编码、签名位置和 ACK 尚未确认；不套用通用托管 Controller。

## 请求、凭据与来源头

- 保留调用方的日期、流水、金额、角色ID和原交易定位键；缺失或非法报错，不重写，扩展不能覆盖已声明字段。细节见 `references/shared-request-field-preservation.md`。
- 私钥与敏感资料使用服务端安全配置和脱敏示例；不得进入前端、日志或仓库。
- 按当前请求实际加载并参与生成的 Skill 集合取值：仅本 Skill 使用 `hfps/1.4.0`；两个 Skill 都参与当前请求时使用 `hfps/1.4.0;hfms/1.0.5`。顺序固定为支付、进件，用一个英文分号且不加空格；仅安装未参与的不计入。显式合同值原样透传，不追加 `sys_id`。
- Java调试在初始化及任何请求前全局关闭，不能并发临时切换。PHP官方 `BsPayDemo/loader.php` 与 `Composer/BsPayConfig.php` 会启用敏感调试日志：在加载任何 SDK 文件前固定 `DEBUG=false`，启动拒绝已启用DEBUG的进程；生成安全loader骨架不需先索取配置证明。

## 官方 SDK-only 传输规则

当前证据：Lightning Java `1.0.6`、通用 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28`（2026-10-08核验）。Java/PHP/Python真实请求都必须使用对应官方 SDK；不得为了“规避 TLS”或缺示例改写HTTP/签验客户端。缺专属Request先核对官方通用入口，仍无证据则报告能力缺口。构造器、具体路由和初始化读取公共矩阵及语言adapter。

通用Java/Python保持默认TLS；Lightning1.0.6存在信任所有证书/主机名的实现，PHP2.0.31关闭peer校验，作为非阻断开发提醒保留。继续官方SDK，不声称风险已修复，不自动修改SDK，也不新增关闭校验设置。

## 交付口径

直接回答当前问题，列出实际读取的 references；代码交付说明适用接口、配置缺口、字段/通知处理和验证结果，未实现部分明确留 TODO。费率试算按接口合同实现，商务费率、准入及生产定责转人工。

本地沙箱只证明协议、状态机和幂等闭环，不能证明真实权限、费率、资金或生产准入。冻结r1–r4证据不重算，差异与使用入口见 `references/shared-local-sandbox.md`。

## 当前版本

| 项目 | 口径 |
| --- | --- |
| Skill 版本 | `1.4.0` |
| 支付来源 | 2026-10-10，24 API / 2,930字段路径 |
| 版本与升级 | `references/skill-version-policy.md` |
