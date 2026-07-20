# 商户业务开通

## 适用范围

用于已完成基础进件后的支付业务申请或补开。官方来源：[商户业务开通](https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md)。费率、MCC、渠道权限、实名审核和准入结论均转运营或官方确认。

## 已确认的请求合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/open`；顶层使用 `sys_id`、`product_id`、`sign`、`data`。
- 请求 51 组扩展表及同步、审核、逐业务、电子协议结果的完整父子路径、类型、长度、Y/N/C 与官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户业务开通”；本页不能替代完整字段目录。
- `data` 至少需新的当日唯一 `req_seq_id`、`req_date`、真实 `huifu_id`、`upper_huifu_id`。
- 微信、支付宝、银联、银行卡、线上业务、协议、分账等配置按业务分组条件填写；不能用一个通用模板猜填渠道字段或费率。
- `async_return_url` 是申请审核结果入口；`busi_async_return_url` 是逐支付业务结果入口；电子协议地址的路径为 `data.agreement_info.agreement_async_return_url`（`agreement_info` 是 String(JSON) 条件对象）。字段合同见 `merchant-onboarding-field-contracts.md`。

## 请求值生成约束

生成请求前必须先从 `merchant-onboarding-complete-field-catalog.md` 沿目标能力父路径读到所有相关叶子，再读取 `merchant-onboarding-field-contracts.md` 的“字段生成硬约束”和“商户业务开通顶层标量约束”。逐字段使用“完整路径 + 请求方向”匹配，示例值不是默认值；调用方未提供真实业务选择的字段只列缺口，不生成。

| 请求路径 | 允许值 / 条件 |
| --- | --- |
| `data.online_flag/quick_flag/withhold_flag` | 仅字符串 `Y/N`，禁止写 `1/0`。 |
| `data.out_fee_flag` | 仅字符串 `1/2`：`1=外扣`、`2=内扣`，默认 `2`；不要因官网示例为 `1` 就填 `1`。 |
| `data.out_fee_huifuid` | 仅 `out_fee_flag=1` 时必填，必须由调用方提供真实承担方。 |
| `data.out_fee_acct_type` | 仅 `01/02/05/09`，默认 `01`。 |
| `data.alipay_pre_auth_flag/wechatpay_pre_auth_flag` | 仅字符串 `Y/N`；目前仅支持企业商户，且汇付 MCC 必须为 `7011/7296/7512`。不满足时禁止填 `Y`。 |
| `data.delay_flag/forced_delay_flag` | 仅字符串 `Y/N`，默认 `N`。 |
| `data.use_chains_flag` | 仅 `1/2/3/4`：微信+支付宝、不使用、微信、支付宝。 |
| `data.online_refund/platform_refund/support_revoke/fund_collection_flag/half_pay_host_flag/online_recharge_flag/refund_mend_open_flag/bill_payment_flag` | 各自仅字符串 `Y/N`；不得统一填 `1`。 |
| `data.enter_fee_flag` | 仅 `1=一次性开户费`、`2=平台套餐费`。 |
| `data.withhold_pay_scene` | `withhold_flag=Y` 时必填，仅 `1..6`，具体语义见字段合同。 |

方向隔离是硬规则：商户详情查询响应的 `online_flag/quick_flag/withhold_flag/pre_authorization_flag` 使用 `1/0/空`，只表示查询到的当前配置；不得把这些响应值复制到本接口请求。本接口的预授权请求字段名也是 `alipay_pre_auth_flag` / `wechatpay_pre_auth_flag`，不是响应字段 `pre_authorization_flag`。

线上能力还必须按申请内容检查材料：`scene_type=ONLINE/ALL` 时提供 `online_busi_type` 和运营媒介；快捷、网银、余额支付 Pro、银行大额转账、分账比例大于 30%、代扣按官方“线上业务类型编码及补充材料说明”提供材料；纸质协议、余额支付、分账、代扣分别使用对应材料规则。材料缺失时列为阻断缺口，禁止用通用 `file_id`、示例材料编号或同一图片占位。

上述业务类型、补充材料、渠道编码、图片上传和协议说明都必须同时读取 `merchant-onboarding-external-resources.md`。只要命中其中一个字段，回答就必须单列 `外部资料提示`，逐条重复完整字段路径、触发条件和未经改写的原始地址，禁止用“同字段/同上”省略路径；未实际读取 XLSX/外站正文时必须要求人工核验。`data.agreement_info.agreement_type=3` 时，完整路径 `data.agreement_info.agreement_url` 必须使用索引中的固定 `PaymentServiceAgreement.htm` 原始地址。回调、二维码、商户网站和 APP 下载等示例或运行时 URL 不是官方资料，也不是默认值。

业务开通参数生成或评审的输出前必须逐项自检并明确写出：

- `online_flag/quick_flag/withhold_flag=Y/N`，不是 `1/0`；
- `out_fee_flag=1/2` 且默认 `2`，`out_fee_acct_type=01/02/05/09` 且默认 `01`；
- 预授权为 `Y/N`，且仅企业商户与 MCC `7011/7296/7512` 可申请；
- 详情查询响应的同名开关是 `1/0/空`，不能回填业务开通请求；
- `mer_bus_type` 只能从 `01..23` 选择，并核对线上运营媒介与补充材料；
- 官网示例值不是默认值，所有业务选择、费率、MCC、承担方和材料都不得猜填。

## 公共请求头

- Java 与 PHP 使用 Skill 调用时都要求 `jpt-x-skill-source: <skill_source>`；当前 Java `3.0.39` 与 PHP `2.0.29` 的官方 SDK 主链路会在配置来源值后自动补该头。Python `2.0.23` 同样从 `MerConfig.jpt_x_skill_source` 自动补头。
- 本接口 `data.huifu_id` 必填，因此三种 SDK 还必须从本次请求自动补 `jpt-x-skill-huifu_id: <data.huifu_id>`；禁止配置固定商户号或复用其他商户的头。

## 分层状态模型

- 申请审核、逐渠道/业务开通、渠道实名和电子协议是独立状态。
- `reg_result_list[].business_stat=S` 只表示该业务结果成功；存在电子协议时还需按实际 `agreement_info_list[].con_stat=5` 判断签约完成。缺少非必填渠道结果列表不表示未申请、成功或失败。
- 按字段路径保存状态；`data.audit_status`、`reg_result_list[].business_stat`、`zl_async_info.apply_state` 和 `agreement_info_list[].con_stat` 的枚举见 `merchant-onboarding-field-contracts.md`，不得混为一类。
- 用户问“已有 `huifu_id`、业务已提交，能否设为可交易”时，必须同时读取主体进件页和 `merchant-onboarding-application-status-query.md`，通过申请状态补偿查询确认所需能力；不得只凭业务回调字段或同步受理判断。

## SDK 证据边界

Java `3.0.39`、PHP `2.0.29`、Python `2.0.23` 都有 `V2MerchantBusiOpenRequest` 作为可选封装，并覆盖 `sign_user_info`、`agreement_info` 等 String(JSON) 边界。它不替代支付业务、费率、协议、实名和渠道权限的人工确认；每次调用显式传入新的当天唯一 `req_seq_id` / `req_date`。

## 已确认与未确认回调规则

- 仅 `busi_async_return_url` 的逐业务通知在存在 `ord_id`（`String(44)`）时，官网规定回包为 `RECV_ORD_ID_` + 该 `ord_id`；不得改用 `req_seq_id`，也不得外推到审核或电子协议通知。
- 逐业务通知的外层包装仍待官方样本确认；审核和电子协议通知的 ACK 仍为 `[需要官方确认]`。审核、逐业务与电子协议通知的验签原文、HTTP 语义、编码、超时和重试也均为 `[需要官方确认]`。未获得相应协议与脱敏样本前，不得生成回调实现或套用支付 `notify_url` 规则。
