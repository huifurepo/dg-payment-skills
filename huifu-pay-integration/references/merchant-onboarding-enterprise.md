# 企业商户进件

## 适用范围

适用于有营业执照或企业/个体主体的基础信息开户。官方来源：[企业商户进件](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md)。主体类型不明时必须触发硬检查点，只问“本次进件主体是企业/个体还是无执照个人？”。

## 已确认的请求合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/basicdata/ent`；顶层包含 `sys_id`、`product_id`、`sign`、`data`。
- 请求、同步响应和审核异步的完整父子路径、类型、长度、Y/N/C 与官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“企业商户进件”；本页只保留生成策略和高风险约束，不能替代完整字段目录。
- `data` 的请求定位键为 `req_seq_id`（当日唯一）和 `req_date`（`yyyyMMdd`），并需真实 `upper_huifu_id`。
- 最小资料按主体、营业执照、注册地址/经营地址、法人、联系人、结算卡和门店资料分组校验。图片字段只接收图片上传接口返回的标识。
- `scene_type=OFFLINE` 或 `ALL` 时，经营详细地址是条件必填；证照非长期时必须提供结束日期。
- `card_info` 是 SDK 边界的 JSON 字符串：业务层先校验对公/对私卡条件，再统一序列化；不得手拼或使用示例卡号。
- 生成字段时必须同时读取 `merchant-onboarding-field-contracts.md` 的企业值域表：`ent_type`、`busi_type`、`scene_type`、证照/证件有效期、`sms_send_flag`、总部/下级商户标识、结算/取现枚举均按各自字符串值域处理。官网示例值不是默认值，禁止把所有开关写成 `1`。
- String(JSON) 对象只能在 `merchant-onboarding-complete-field-catalog.md` 中沿父路径加载到全部相关叶子且调用方提供真实选择后生成；受益人、电子账户、股东和扩展材料对象不得只写父字段，也不得猜值。
- 涉及 MCC、地区、证件类型、图片上传、银行编码、结算批次或补充材料等带外部资料的字段时，必须同时读取 `merchant-onboarding-external-resources.md`，并按完整字段路径单列 `外部资料提示`，给出未经改写的原始地址；示例 URL 不是资料或默认值。

## 异步通知字段

- 企业进件审核异步通知地址是 `data.async_return_url:String(120) N`。
- `notify_url` 是支付交易接口字段，不是企业进件字段；企业进件的业务 DTO、`extendInfoMap` 和最终 `data` 中都禁止使用 `notify_url`。
- Java `V2MerchantBasicdataEntRequest` 没有该扩展字段的专属 setter 时，必须通过 `extendInfoMap` 原名透传，禁止改名：

```java
Map<String, Object> extendInfoMap = new HashMap<>();
if (request.asyncReturnUrl() != null && !request.asyncReturnUrl().isBlank()) {
    extendInfoMap.put("async_return_url", request.asyncReturnUrl());
}
sdkRequest.setExtendInfo(extendInfoMap);
```

## 公共请求头

- Java 与 PHP 使用 Skill 调用时都要求 `jpt-x-skill-source: <skill_source>`；当前 Java `3.0.39` 与 PHP `2.0.29` 的官方 SDK 主链路会在配置来源值后自动补该头。Python `2.0.23` 同样从 `MerConfig.jpt_x_skill_source` 自动补头。
- 只有当前请求 `data.huifu_id` 存在且非空时，Java、PHP、Python 才应自动补 `jpt-x-skill-huifu_id: <data.huifu_id>`；禁止配置固定商户号。企业基础进件请求本身没有 `data.huifu_id`。
- **按语言区分处理**：PHP `2.0.29` 在 `MerConfig.skill_source` 非空时直接读取请求参数中的 `huifu_id`，企业进件又没有该字段；运行环境把 warning 提升为异常时，必须使用已修复 SDK，不能添加虚构/空业务字段、关闭 warning 或吞异常。Python `2.0.23` 会发送空的 `jpt-x-skill-huifu_id`，但这只是 SDK 兼容性告警，不单独阻断企业进件代码。保持业务报文不含 `data.huifu_id`，单列 `SDK 兼容性提示`，在联调/上线前验证网关结果；若因空头被拒绝，再升级或修复 SDK。不得询问客户“是否允许空请求头”。

## 同步受理与状态

- 同步返回可能含 `huifu_id`、`apply_no`、`token_no`；它们只用于后续状态定位，不等于审核通过、渠道实名完成或支付业务可用。
- 将 `req_seq_id`、`req_date`、`apply_no`、主体资料版本和状态历史落库；`token_no` 必须字段级加密、访问审计，禁止前端、日志和示例输出。
- 审核补偿优先使用申请单状态查询；网络不确定时先查状态，不换流水盲目重复提交。

## SDK 证据边界

Java `3.0.39`、PHP `2.0.29`、Python `2.0.23` 都有 `V2MerchantBasicdataEntRequest` 作为可选封装。它只证明 URI、字段序列化和 SDK 默认的请求/同步响应处理路径；不替代本页资料、权限和条件必填校验，也不证明实际审核结果或回调协议。每次调用显式传入新的当天唯一 `req_seq_id` / `req_date`，Python 不会自动生成。

## 回调边界

官网已确认异步包络为 `resp_code:String(5) Y`、`resp_desc:String(512) Y`、`sign:String(2048) Y`、`data:String(JSON Object) N`。`data` 中已知字段为：

| 路径 | 类型 / 必填 | 说明 |
| --- | --- | --- |
| `data.sub_resp_code` / `data.sub_resp_desc` | `String(8) Y` / `String(512) Y` | 业务返回码与描述。 |
| `data.req_seq_id` / `data.req_date` | `String(32) Y` / `String(8) Y` | 原请求流水与日期。 |
| `data.audit_status` | `String(1) Y`：`Y/N/F` | 审核通过、审核拒绝、失败。 |
| `data.audit_desc` / `data.product_id` | `String(512) N` / `String(32) Y` | 审核描述与产品号。 |
| `data.huifu_id` / `data.apply_no` / `data.token_no` | `String(18) N` / `String(18) N` / `String(20) N` | 条件返回的商户、申请单及取现卡定位字段。 |
| `data.notify_type` / `data.elec_acct_result` | `String(1) N` / `String(JSON Object) N` | `notify_type=Z` 时为电子账户开通结果。 |

官网只说明 `sign` 对报文整体签名，未给出可核验的验签原文、成功 ACK、HTTP 超时或重试样本。这些仍为 `[需要官方确认]`：不得套用支付 `notify_url` 或 `RECV_ORD_ID_` 规则，也不得生成回调实现。
