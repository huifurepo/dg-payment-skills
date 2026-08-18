# 用户开户 FAQ

## 已有 `huifu_id`，该用本 Skill 还是商户进件？

字段名不足以判断。多方分账/结算用户使用 `userHuifuId` 和 `/v2/user/*`；支付收单商户使用 `merchantHuifuId` 和 `/v2/merchant/*`。上下文不清楚时硬停确认实体。

## 企业/个人开户为什么不能传 `huifu_id`？

这两个接口用于创建新用户，正式请求参数没有 `data.huifu_id`。不能为 SDK 来源头兼容添加空值、调用主体号或其他用户号。

## 用户材料如何上传？

用户开户子域只消费图片接口返回的 `file_id`。图片上传 `data.huifu_id` 只支持直属商户号，不支持用户号；不要把开户返回的 `userHuifuId` 传入上传接口。需要上传时切换到本 Skill 的商户图片路由并遵守其图片边界。

## 用户申请状态查询能查开户或全部业务入驻吗？

不能。`/v2/user/apply/query` 官方范围仅是非同名对公结算卡审核，需要业务入驻返回的 `apply_no`。其他申请状态与补偿方式标记 `[需要官方确认]`。

## `file_list` 应发送数组还是 JSON 字符串？

类型列/说明是 String(jsonArray)，个人开户示例却是普通数组。接入方已确认按说明发送 String(JSON Array)；示例登记为错误，SDK 探针只验证没有再次序列化。

## 同步成功是否表示业务入驻全部完成？

不表示。同步业务码、配置 `S/F`、审核 `Y/P/N` 和银行 `S/F` 是不同层。只有所需层次均达到对应成功条件，才能进入后续业务判断。

## 可以直接实现异步回调吗？

可以按伙伴平台公共异步规范实现：配置类接口使用 `data`，对原始字符串免排序执行 RSA 验签，处理成功返回 HTTP 200 与 `RECV_ORD_ID_` + `req_seq_id`，默认5秒超时，超时及500-599默认重试3次，并做状态感知幂等。必须联读 `user-onboarding-platform-contracts.md`，不能混用控台 Webhook；异步 `huifu_id` 的用户号/商户号角色仍不得猜测。

## Java/PHP 会因为 TLS 被硬停吗？

不会。接入方已确认当前官方 Java/PHP SDK 不存在本 Skill 曾推断的 TLS 问题，真实请求应继续使用官方 SDK，不得降级成手写 HTTP。PHP Demo/Composer loader 启用 `DEBUG=true` 会记录私钥和完整报文，这是独立硬检查点；在加载 SDK 前固定 `DEBUG=false` 后才可生成联调/生产调用。
