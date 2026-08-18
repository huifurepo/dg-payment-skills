# 个人用户开户

## 适用范围

服务商或商户为旗下自然人建立分账/结算用户。官方来源：[个人用户基本信息开户](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxzc.md)。它不是无执照个人商户进件；实体不明时先触发硬停。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/basicdata/indv`。
- 快照更新时间：官网 `2026.01.26`，本地冻结 `2026-08-10`。
- 共34个字段路径：请求27、同步响应7、异步0。完整字段读取 `user-onboarding-complete-field-catalog.md`。
- 请求业务 `data` 没有 `huifu_id`、`upper_huifu_id` 或异步地址。

## 请求合同

- 必填主字段为流水、日期、姓名、证件类型/号码、证件有效期类型/开始日和手机号。
- `cert_end_date:String(8)` 的必填列为 `N`，说明明确“长期可不填，非长期必填”；保留该官网冲突并执行条件校验。
- 外国人居留证触发 `cert_nationality`；不得把示例国籍当默认值。
- `sms_send_flag` 只使用 `Y/N`，默认不发送；示例中的 `"1"` 不属于正式值域。
- `address` 在开通中信E管家或电子回单时必填。`mcc/prov_id/area_id/district_id` 的必填列为 `N`，但当用户业务入驻修改且电子回单配置开通时说明要求填写；省市区需要级联修改。
- `file_list` 按类型、说明和接入方确认发送 String(JSON Array)；请求示例中的普通数组登记为示例错误，不得发送，也不得二次序列化。官网另在表外注明：证件类型为身份证时，会对姓名和身份证号做实名认证。
- 示例含参数表未定义的 `operator_id`；禁止加入 DTO 或最终 `data`。

## 同步响应

响应结构与企业用户开户相同：外层 `response.data:Json` 的官网必填列为 `N`，接入方确认成功响应一定包含该对象；成功缺失按协议异常，异常响应 DTO 仍允许缺失。对象中包含业务码、描述，并可能返回 `huifu_id`、`login_name` 和初始 `login_password`。将 `huifu_id` 建模为 `userHuifuId`；初始密码按一次性高敏凭据处理。

公共响应表将 `sign:String(512)` 标为 `Y`，成功示例却省略 `sign`；保留 `[官网示例冲突]`，不得据此取消同步响应验签。

官网未声明异步通知。不得生成回调、轮询推断或复用企业/商户开户通知。

## SDK 边界

三语言锁定版本均有 `V2UserBasicdataIndvRequest`。生成类对 `cert_nationality/address` 等字段的 required/空串建模不覆盖官方 Y/N/C；三语言联调和生产实现均使用对应官方 SDK，PHP 另受 DEBUG 硬停约束。
