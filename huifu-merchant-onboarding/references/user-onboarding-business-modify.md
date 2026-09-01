# 用户业务入驻修改

## 适用范围

服务商或商户为已开户的企业/个人用户修改结算费率、结算卡、取现、延迟入账、斗拱 e 账户和电子回单配置。官方来源：[用户业务入驻修改](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrzxg.md)。首次开通使用 `/v2/user/busi/open`，本接口不能代替商户 `/v2/merchant/busi/modify`。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/busi/modify`。
- 官网更新时间：`2026-08-25`；本地活动快照：`2026-08-31`；原文 SHA-256：`e8abc91b15587be26552d8989c408769246e4686fcdde02b74efec581344faf9`。
- 共120个字段路径：请求85、同步响应11、异步24；6个根表、12个扩展表、15个父节点、105个叶节点。完整字段读取 `user-onboarding-complete-field-catalog.md`。
- `request.data.huifu_id:String(18) Y` 明确使用开户返回的用户号；不得填上级商户号。流水在同一商户号当天唯一，日期为 `yyyyMMdd`。

## 请求 wire

- `settle_config_list`、`cash_config`、`file_list`：`String(JSON Array)`。
- `card_info`、`elec_acct_config`：`String(JSON Object)`；其中 `elec_acct_config.elec_card_list` 的类型列为 Object、说明为 jsonArray，尚未裁决真实 wire，不能仅按说明或子路径擅自编码。
- `sign_user_info:Object C`：电子回单开通时按原生 JSON Object 发送。
- `elec_receipt_config` 的类型列为 `Object`，说明却写“jsonObject字符串”，属于 `[官方文档口径冲突]`。正式编码确认前不得猜成原生 Object 或 String(JSON Object)；生产请求在此字段启用时硬停确认实际 wire。
- `settle_config_list` 不支持同时开通 D1 与 T1；结算配置前必须已有或同时提交结算卡。配置取现或结算时 `card_info` 必填。
- 个人用户不支持对公卡和对私非法人卡；不得从企业用户规则外推。`card_type=4` 的企业非同名卡按正式文件枚举补材料。
- `cash_config[].fix_amt/fee_rate` 至少一项；`cash_config[].weekday_fix_amt` 与 `cash_config[].weekday_fee_rate` 的说明都同时写 D1“不生效”和“遇工作日按此结算”，两个路径均标记 `[需要官方确认]`，不得只保留费率而遗漏固定金额。
- `delay_flag` 只允许 `Y/N`；当前示例已修正为 `N`。
- `async_return_url` 为空时不推送；当前示例已修正为合法 `http://` 地址，但示例仍不是默认值。

## 官方示例边界

官网请求示例是合法 JSON，且只声明一次 `file_list`。它仍是非规范性示例，不是 fixture 或默认报文；字段名、类型、长度、必填性和嵌套以正式参数表及完整目录为准。

公共返回表把 `response.data` 定义为 `String N`，成功示例却返回原生 JSON Object；本接口尚无独立 wire 裁决，响应 DTO 必须隔离两种形态并在生产联调前确认，不能把示例提升为正式合同。同步 `resp_business:Object N` 的说明为 jsonArray格式，按原生 JSON Array 解析；申请审核中时可能返回 `apply_no`，不等于审核通过。

## SDK 边界

Java `3.0.40`、PHP `2.0.30`、Python `2.0.24` 都使用 `V2UserBusiModifyRequest`，精确路由 `/v2/user/busi/modify`。三语言生成类恰好只声明 `req_seq_id/req_date/huifu_id/sign_user_info`。

官网把 `sign_user_info` 定义为 Object。Java setter 静态接收 String，因此 Java 必须通过 exact-key 扩展在最终合并阶段写入原生 Object，不得把 JSON 文本交给 String setter。PHP setter 没有类型约束，可直接传数组；Python 属性是动态类型，可直接赋 dict；两者也可按仓库统一构建策略使用受控 exact-key。三语言都要用脱敏运行探针验证最终 JSON 类型。Java `putAll`、PHP `array_merge`、Python `dict.update` 会让扩展覆盖声明字段，因此一律拒绝扩展覆盖 `req_seq_id/req_date/huifu_id`，其他正式可选字段按白名单传入。

## 异步与安全

本接口声明与首次业务入驻相同节点数的24个异步节点；本页当前把外层 `async.data` 定义为 `Json N`，`async.data.audit_info.resp_business:Object N` 的说明为 jsonArray格式，按原生 JSON Array 解析。配置类通知按公共协议处理：POST/UTF-8，保留原始请求体并使用精确收到的 `data` 表示执行 RSA 验签，成功返回 HTTP 200 与 `RECV_ORD_ID_` + `req_seq_id`，默认5秒超时，超时及500–599默认重试3次并做状态感知幂等。不得与控台 Webhook 混用。

异步 `huifu_id` 的中文名和说明现已统一为“汇付客户号”，按用户号解析。`token_no`、卡号、证件号、手机号、文件 ID 和签约信息不得写日志、前端或回答示例。
