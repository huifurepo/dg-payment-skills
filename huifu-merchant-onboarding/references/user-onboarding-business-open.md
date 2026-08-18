# 用户业务入驻

## 适用范围

为已经完成企业/个人用户开户的 `userHuifuId` 配置结算费率、结算卡、取现、斗拱e账户和电子回单。官方来源：[用户业务入驻](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrz.md)。本接口不是商户业务开通，不能复用 `/v2/merchant/busi/open` DTO。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/busi/open`。
- 快照更新时间：官网 `2026.06.26`，本地冻结 `2026-08-10`。
- 共118个字段路径：请求83、同步响应11、异步24；是五接口中唯一声明异步通知的接口。
- 全部请求、同步响应和异步通知的完整父子路径、类型、长度、Y/N/C 与官方说明读取 `user-onboarding-complete-field-catalog.md`；String(JSON)、条件字段和官网冲突同时读取 `user-onboarding-field-contracts.md`。
- `data.huifu_id:String(18) Y` 是开户返回的用户号；`data.upper_huifu_id:String(18) Y` 是真实渠道商/商户号。两个角色不得交换。

## 请求对象

| 路径 | wire 与关键约束 |
| --- | --- |
| `data.settle_config_list` | String(JSON Array)；不支持同时开通 T1+D1，周期 `T1/D1/TS` |
| `data.card_info` | String(JSON Object)；配置结算或取现时必填 |
| `data.cash_config` | String(JSON Array)；固定金额和费率至少一项 |
| `data.file_list` | String(JSON Array)；使用图片上传返回的 `file_id`，但上传不得传用户号 |
| `data.elec_acct_config` | String(JSON Object)；内部 `elec_card_list` 再序列化为 String(JSON Array) |
| `data.elec_receipt_config` | 原生 JSON Object；开通电子回单时联动签约人信息 |
| `data.sign_user_info` | 原生 JSON Object 且条件必填 |
| `data.async_return_url` | String(128) N；为空时不推送异步消息 |

结算卡类型：`0=对公`、`1=对私法人`、`2=对私非法人`、`4=对公非同名`。接入方确认个人用户只允许 `1`，禁止 `0/2/4`；企业用户按业务条件使用 `0/1/2/4`。`card_type=4` 额外上传 `F07/F08/F516` 和证件材料。正式卡信息表没有 `bank_code`、`branch_name`，即使示例含有也不得提升。

`elec_card_list` 类型列为 Object、说明为 jsonArray 字符串；接入决策按说明使用 String(JSON Array)。其示例 `card_type=310100` 不符合正式 `0/1` 值域，禁止复制。

`card_info.card_name:String(128) C` 按接入方确认执行条件必填：企业用户接受的 `0/1/2/4` 以及个人用户唯一接受的 `1` 都必须填写对应账户名；先校验主体与 `card_type`，再校验卡户名，不能把企业账户名和个人姓名混用。

正式表要求 `settle_cycle=D1` 时 `fixed_ratio`、`constant_amt` 必填，且费率和金额保留两位小数；官方请求示例却漏传 `constant_amt`，并传 `fixed_ratio:"2"`。同一示例的 `cash_config.fee_rate:"2"` 也不满足两位小数说明。生成请求只按正式字段说明输出，不复制这些示例值。

官网未给 `elec_acct_config`、`elec_receipt_config` 和 `sign_user_info.mobile_no` 写说明，也未给 `async.sign`、`elec_receipt_config.switch_state`、`sign_user_info.type`、`sign_user_info.mobile_no`、`sign_user_info.cert_no`、`sign_user_info.name` 写长度；完整目录以 `—` 保留，相关约束标记 `[需要官方确认]`。

## 同步响应

同步业务 `data` 包含业务码、描述；用户号、`token_no`、`resp_business:String(JSON Array)` 和 `apply_no` 的官网必填列为 `N`。接入方确认业务入驻成功响应返回 `apply_no`；配置结果类型为 `1=绑卡`、`2=取现`、`3=结算`、`5=灵工`，状态为 `S/F`，不能把拿到申请单号解释为审核最终通过。

公共返回表把外层 `response.data:String` 的必填列标为 `N`；开发规范、成功示例和接入方确认共同裁决成功 wire 为原生 JSON Object。成功响应缺少 `data` 按协议异常处理，网关/异常响应 DTO 仍允许缺失；内部 String(JSON) 继续逐字段解码。`token_no` 是高敏定位字段，不得回显或写日志。

## 异步通知

外层：`resp_code:String(6)`、`resp_desc:String(512)`、`sign`、`data:String(JSON)`。内部按 `notify_type` 分流：

内部 `huifu_id:String(18) Y` 的中文名为“汇付客户号”，官网说明却写“汇付分配的商户号”，与请求侧用户号语义冲突。保留为 `[需要官方确认]`；在取得官方或脱敏 wire 证据前，不得直接映射为 `userHuifuId` 或 `merchantHuifuId`。

- `A`：解析 `audit_info:String(JSON Object)`；审核 `Y/P/N`，配置结果 `S/F`。
- `Z`：解析 `elec_acct_result:String(JSON Object)`；银行开通 `S/F`。

审核中的 `resp_business` 类型列为 Object、说明为 jsonArray；按说明和接入决策，在解码 `audit_info` 后读取原生 JSON Array。审核、配置与银行状态必须独立持久化。

公共异步规范已补齐：配置类通知以 POST/UTF-8 推送 `data`，默认5秒超时；超时及500-599默认重试3次。先对原始 `data` 免排序执行 SHA256WithRSA 验签，成功处理后返回 HTTP 200 与 `RECV_ORD_ID_` + `req_seq_id`，重复通知做状态感知幂等。不得改用支付通知的 `resp_data` 或控台 Webhook 协议；完整规则读取 `user-onboarding-platform-contracts.md`。

## SDK 边界

三语言锁定版本均有 `V2UserBusiOpenRequest`。对 `sign_user_info` 等原生 Object 和多层 String(JSON) 字段，按 `user-onboarding-platform-contracts.md` 的 wire 矩阵使用 exact-key 扩展能力，并用运行探针验证 SDK 没有再次序列化。三语言真实请求均使用对应官方 SDK，PHP 另受 DEBUG 硬停约束。
