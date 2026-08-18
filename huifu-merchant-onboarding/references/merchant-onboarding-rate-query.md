# 商户费率信息查询

## 适用范围

用于查询指定商户的微信、支付宝、银行卡或银联二维码费率配置。官方来源：[商户费率信息查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md)，锁定来源 SHA-256 为 `c9bfb5ed774cf8bce622bb536d16b1ed60ffedd5bd5540bf83177cdf592008b9`。

这是进件配置查询，不是支付订单、对账或实际手续费结算结果查询。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/fee-rate/query`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共 35 个节点：请求 8、同步响应 27、无异步通知。完整路径、类型、长度、Y/N/C 和官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户费率信息查询”。
- 请求 `data` 为 `req_seq_id:String(32) Y`、`req_date:String(8) Y`、`huifu_id:String(32) Y`、`fee_rate_type:String N`。
- `fee_rate_type` 支持 `ALI_FEE_RATE`、`WX_FEE_RATE`、`BANK_CARD_FEE_RATE`、`UNION_FEE_RATE`；不传返回全部费率。

## 官方文档冲突

`fee_rate_type` 在字段表中定义为 `String`，说明写“支持多选”，示例又呈现数组样式字符串。该序列化形式标记为 `[官方文档口径冲突]`：调用方未提供已验证样本或官方确认前，不得自行选择 JSON 数组、逗号字符串或数组文本。

请求 `request.data.huifu_id` 定义为 `String(32) Y`，响应 `response.data.huifu_id` 定义为 `String(18) Y`，但响应说明又写“同入参”。这是第二处 `[官方文档口径冲突]`：请求和响应 DTO 必须分开保留 32/18 两套长度，在官方澄清前不得互相复制长度注解或用响应约束拒绝请求值。

响应的 `wx_fee_rate_list`、`ali_fee_rate_list`、`bank_card_fee_rate_list`、`union_fee_rate_list` 均按官方 jsonArray 说明解析。费率值保持字符串，不能自动换算、四舍五入或当成实际订单计费结果。

## 公共请求头

- `jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.0.1`，双 Skill 默认 `hfps/1.3.4;hfms/1.0.1`。

## SDK 证据边界

在用户提供且已锁定源码树摘要的 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24` 中未找到 `/v2/merchant/fee-rate/query` 的专属 Request 类或路由常量。因此：

- 不得声称三语言 SDK 已支持本接口；
- 不得用名称相近的费率或支付查询类替代；
- 只有获得新版官方 SDK 或经官方确认的通用签名/HTTP 调用证据后，才生成可运行代码。

字段解释和 DTO 审查仍可基于锁定官方文档完成。
