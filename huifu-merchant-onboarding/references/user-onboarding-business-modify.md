# 用户业务入驻修改

## 适用范围

服务商或商户为已开户的企业/个人用户修改结算费率、结算卡、取现、延迟入账、斗拱 e 账户和电子回单配置。官方来源：[用户业务入驻修改](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrzxg.md)。首次开通使用 `/v2/user/busi/open`，本接口不能代替商户 `/v2/merchant/busi/modify`。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/busi/modify`。
- 官网更新时间：`2026-09-22`；本地活动快照：`2026-10-08`；原文 SHA-256：`ca3c5d4430cba1827c806c87d7dee3417b3f78bd4883ce1e88ea90149e5d9c78`。
- 共138个字段路径：请求98、同步响应11、异步29；6个根表、16个扩展表、19个父节点、119个叶节点。完整字段读取 `user-onboarding-complete-field-catalog.md`。
- `request.data.huifu_id:String(18) Y` 明确使用开户返回的用户号；不得填上级商户号。流水在同一商户号当天唯一，日期为 `yyyyMMdd`。

## 请求 wire

- `settle_config_list`、`cash_config`、`file_list`：`String(JSON Array)`。
- `card_info`、`elec_acct_config`：`String(JSON Object)`；其中 `elec_acct_config.elec_card_list` 当前为 String/jsonArray字符串，逐层各编码一次。
- `sign_user_info:String C`：电子回单开通时按 String(JSON Object) 发送。
- `elec_receipt_config` 当前正式类型为 `String` 且说明为“jsonObject字符串”，按 String(JSON Object) 编码；不得沿用旧快照的原生 Object 假设。
- `settle_config_list` 不支持同时开通 D1 与 T1；结算配置前必须已有或同时提交结算卡。配置取现或结算时 `card_info` 必填。
- 个人用户不支持对公卡和对私非法人卡；不得从企业用户规则外推。`card_type=4` 的企业非同名卡按正式文件枚举补材料。
- `cash_config[].fix_amt/fee_rate` 至少一项；`cash_config[].weekday_fix_amt` 与 `cash_config[].weekday_fee_rate` 当前说明均为 D1 工作日使用，未配置则按节假日手续费计算。旧“不生效/生效”冲突已关闭，不再据此硬停；仍分别保留两个路径并按正式金额、费率及 C 标记校验，不把未配置的回退规则擅自改成无条件必填。
- `delay_flag` 只允许 `Y/N`；当前示例已修正为 `N`。
- `async_return_url` 为空时不推送；当前示例已修正为合法 `http://` 地址，但示例仍不是默认值。

## 等级与新能力

request.data.account_level为LV1/LV2/LV3，默认LV1；仅企业可升LV3。balance_pay_config/account_recharge_config/delay_pay_config请求均为String(JSON Object)，只在LV3开通；不能把delay_flag Y/N与delay_pay_config.switch_state 1/0混同。完整材料、签约条件及新费用必填冲突联读 `user-onboarding-field-contracts.md` 的“用户等级与新资金配置”；争议规则用 TODO/配置隔离，提示核对本页官方文档或咨询官方/交流群，同时继续已明确字段和 SDK 实现。异步新增原生Object account_info及4个子路径，打款与活体状态不等于审核或支付终态。

## 官方示例边界

官网请求示例是合法 JSON，且只声明一次 `file_list`。它仍是非规范性示例，不是 fixture 或默认报文；字段名、类型、长度、必填性和嵌套以正式参数表及完整目录为准。

公共返回表把 `response.data` 定义为 `String N`，成功示例却返回原生 JSON Object；本接口尚无独立 wire 裁决，响应 DTO 用 TODO/可配置解析策略隔离两种形态，提示核对本页官方文档或咨询官方/交流群，继续已明确部分，不把示例提升为正式合同，也不要求先取得答复。同步 `resp_business:Object N` 的说明为 jsonArray格式，按原生 JSON Array 解析；申请审核中时可能返回 `apply_no`，不等于审核通过。

## SDK 边界

已核验源码基线 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 都使用 `V2UserBusiModifyRequest`，精确路由 `/v2/user/busi/modify`。三语言生成类恰好只声明 `req_seq_id/req_date/huifu_id/sign_user_info`。

官网当前把 `sign_user_info` 定义为 String/jsonObject字符串。三语言均按 String(JSON Object) 传输并用脱敏运行探针验证只序列化一次。Java `putAll`、PHP `array_merge`、Python `dict.update` 会让 exact-key 扩展覆盖声明字段，因此一律拒绝扩展覆盖 `req_seq_id/req_date/huifu_id/sign_user_info`，其他正式可选字段按白名单传入。

## 异步与安全

本接口声明与首次业务入驻相同节点数的29个异步节点；本页当前把外层 `async.data` 定义为 `Json N`，`async.data.audit_info.resp_business:String N` 的说明为 jsonArray格式，解码 `audit_info` 后再解码一层。配置类通知按公共协议处理：POST/UTF-8，保留原始请求体并使用精确收到的 `data` 表示执行 RSA 验签，成功返回 HTTP 200 与 `RECV_ORD_ID_` + `req_seq_id`，默认5秒超时，超时及500–599默认重试3次并做状态感知幂等。不得与控台 Webhook 混用。

异步 `huifu_id` 的中文名和说明现已统一为“汇付客户号”，按用户号解析。`token_no`、卡号、证件号、手机号、文件 ID 和签约信息不得写日志、前端或回答示例。
