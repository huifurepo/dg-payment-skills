---
name: dougong-hostingpay-cashier-query
description: "汇付托管支付（dg-java-sdk）查询与关单 Skill：托管交易支付状态查询、托管交易关单、交易结算对账单查询。当开发者需要查询收银台托管订单状态、关闭未支付的托管订单或查询对账单时使用。触发词：托管交易查询、收银台订单查询、托管关单、收银台关单、托管对账单。"
license: MIT
compatibility: "Java 8+, Maven, Spring Boot 2.x/3.x"
source: "https://github.com/niceforbear/huifu-hosting-payment"
dependencies:
  - dougong-hostingpay-pay-base
metadata:
  author: codecodeing
  version: 1.0.0
  bins: java, mvn
---

# 统一收银台 — 查询、关单与对账

托管交易支付状态查询 + 托管交易关单 + 交易结算对账单查询。

> **前置依赖**：首次接入请先阅读 [dougong-hostingpay-pay-base](../dougong-hostingpay-pay-base/SKILL.md) 完成 SDK 初始化。

> **进入本 Skill 前先确认**：上游下单侧已经沉淀 `req_date`、`req_seq_id`、`party_order_id`、`hf_seq_id` 等定位键；具体来源和保留策略见 [客户前置准备清单](../dougong-hostingpay-pay-base/references/customer-preparation.md)。

> **官方文档补充约束**：托管产品文档明确建议在关键业务环节通过反查接口确认非终态订单状态；对账单能力也要求先在控台配置对账文件生成后再查询下载。

## 触发词

- "托管交易查询"、"收银台订单查询"、"托管订单状态"、"查询托管支付结果"
- "托管关单"、"收银台关单"、"关闭托管订单"、"取消托管订单"
- "托管对账单"、"托管对账"、"收银台对账单"、"结算对账"

## 场景路由

| 用户意图 | 场景 | 详细说明 |
|---------|------|---------|
| 查询订单支付状态 | 托管交易查询 | 见 [payment-status-query.md](references/payment-status-query.md) |
| 关闭未支付订单 | 托管交易关单 | 见 [trade-close.md](references/trade-close.md) |
| 查询对账单 | 交易结算对账单查询 | 见 [reconciliation.md](references/reconciliation.md) |

## 汇付 API 端点

| 场景 | API 路径 | 请求方式 |
|------|---------|---------|
| 交易查询 | `v2/trade/hosting/payment/queryorderinfo` | POST |
| 交易关单 | `v2/trade/hosting/payment/close` | POST |
| 对账单查询 | `v2/trade/check/filequery` | POST |

## 通用架构

```
HFPayController (@RestController, /hfpay)
    ├── POST /queryorderinfo  → hostingPayService.queryOrderInfo(req)
    ├── POST /closeOrder      → hostingPayService.closeOrder(req)
    └── POST /checkFileQuery  → hostingPayService.checkFileQuery(req)

HostingPayService (@Service)
    ├── queryOrderInfo()  → V2TradeHostingPaymentQueryorderinfoRequest → BasePayClient.request()
    ├── closeOrder()      → V2TradeHostingPaymentCloseRequest          → BasePayClient.request()
    └── checkFileQuery()  → V2TradeCheckFilequeryRequest               → BasePayClient.request()
```

## SDK Request 类对照

| 场景 | SDK Request 类 |
|------|---------------|
| 交易查询 | `V2TradeHostingPaymentQueryorderinfoRequest` |
| 交易关单 | `V2TradeHostingPaymentCloseRequest` |
| 对账单查询 | `V2TradeCheckFilequeryRequest` |

## 查询请求参数摘要

| 参数 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| reqDate | setReqDate() | String(8) | Y | 本次查询的请求日期 |
| reqSeqId | setReqSeqId() | String(64) | Y | 本次查询的请求流水号 |
| huifuId | setHuifuId() | String(32) | C | 商户号；不填时必填 partyOrderId |
| orgReqDate | setOrgReqDate() | String(8) | C | 原交易的请求日期；不填时必填 partyOrderId |
| orgReqSeqId | setOrgReqSeqId() | String(64) | C | 原交易的请求流水号；不填时必填 partyOrderId |
| partyOrderId | setPartyOrderId() | String(64) | C | 商户订单号；不填时必须提供 huifuId + orgReqDate + orgReqSeqId |

> 完整字段说明见 [payment-status-query.md](references/payment-status-query.md)

## 查询返回参数摘要

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 查询接口受理返回码；仍需继续看 `order_stat`、`trans_stat`、`close_stat` |
| trans_stat | String(1) | **交易状态**：P=处理中、S=成功、F=失败、I=初始（罕见） |
| trans_amt | String(14) | 交易金额 |
| org_req_seq_id | String(128) | 原交易请求流水号 |
| org_hf_seq_id | String(128) | 汇付全局流水号 |
| order_stat | String(1) | 预下单状态：1=已支付、2=支付中、3=已退款、4=处理中、5=失败、6=部分退款 |
| close_stat | String(1) | 关单状态：P=处理中、S=成功、F=失败 |
| ref_amt | String(14) | 可退金额（元） |
| pay_type | String(16) | 交易类型（返回字段名固定为 `pay_type`，不要按其他接口习惯改成 `trans_type`） |
| goods_desc | String(40) | 商品描述 |
| is_div | String(1) | 是否分账交易 |

> 渠道扩展报文与扩展对象（`wx_response`、`alipay_response`、`unionpay_response`、`dy_response`、`quick_online_response`、`bank_extend_param`、`trans_fee_allowance_info`、`fee_formula_infos`）见 [payment-status-query.md](references/payment-status-query.md)

## 关单请求参数摘要

| 参数 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| reqSeqId | setReqSeqId() | String(64) | Y | 本次关单的请求流水号 |
| reqDate | setReqDate() | String(8) | Y | 本次关单的请求日期 |
| huifuId | setHuifuId() | String(32) | Y | 商户号 |
| orgReqDate | setOrgReqDate() | String(8) | Y | 原交易的请求日期 |
| orgReqSeqId | setOrgReqSeqId() | String(64) | Y | 原交易的请求流水号 |

> 完整字段说明见 [trade-close.md](references/trade-close.md)

## 关单返回参数摘要

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 关单接口受理返回码；仍需继续看 `close_stat`、`org_trans_stat` |
| close_stat | String(1) | 关单状态：P=处理中、S=成功、F=失败 |
| org_trans_stat | String(1) | 原交易状态：P=处理中、S=成功、F=失败 |

> 异步回调参数、官方未明确列出的回调地址字段争议与示例说明见 [trade-close.md](references/trade-close.md)

## trans_stat=P 轮询策略

当查询返回 `trans_stat=P`（处理中）时，启动轮询：

- **间隔**：5 秒
- **最大次数**：30 次
- **总超时**：150 秒
- **超时处理**：记录异常日志并人工介入，**不要自动关单**

```java
int maxRetries = 30;
for (int i = 0; i < maxRetries; i++) {
    Map<String, Object> resp = BasePayClient.request(queryRequest, false);
    String stat = (String) resp.get("trans_stat");
    if (!"P".equals(stat)) break;  // 非处理中，退出轮询
    Thread.sleep(5000);
}
```

## 关单异步通知参数

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 业务响应码 |
| huifu_id | String(32) | 商户号 |
| org_req_date | String(8) | 原交易请求日期 |
| org_req_seq_id | String(64) | 原交易请求流水号 |
| org_trans_stat | String(1) | 原交易状态 |
| close_stat | String(1) | 关单状态：S=成功、F=失败 |

## 使用场景说明

### 交易查询

- 用户支付后页面未跳转，需确认支付结果
- 收到异步通知后做二次确认
- 定时轮询处理中（trans_stat=P）的订单

### 交易关单

- 用户长时间未支付，主动关闭订单
- 业务逻辑需要取消订单
- 防止用户在关单前支付导致资金问题

### 对账单查询

- 查询交易/结算/分账/出金/用户结算等对账文件
- 接口支持 1 年内账单下载；控台下载当前口径暂未限制时间范围
- 对账文件按 T+1 / D+1 跑批生成；最新产品介绍口径建议交易/分账文件 `12:00` 后下载，出金对账单 `10:30` 跑批后一小时，结算对账单 `17:00` 跑批后一小时
- 对账单查询对外请求字段应直接保持 `file_date` 和 `bill_type`；不要按中文释义改成 `bill_date`、`generate_date` 或 `file_type`

## 常见错误与排查

| 错误码 | 场景 | 说明 | 排查方法 |
|-------|------|------|---------|
| 00000000 | 查询/关单 | 处理成功 | — |
| 00000100 | 关单 | 交易处理中 | 等待异步通知确认最终状态 |
| 10000000 | 查询/关单 | 无效参数 | 检查必填字段格式 |
| 99010003 | 查询/关单 | 交易不存在 | 检查 org_req_date 和 org_req_seq_id 是否正确 |
| 30000001 | 关单 | 原交易已终态 / 关单已终态 | 已支付订单走退款流程 |
| 99999999 | 查询/关单 | 系统异常 | 稍后重试 |
| — | 对账单 | file_details 为空 | 查看 task_details 的 task_stat，S 且为空代表无交易记录 |

## 注意事项

1. 查询接口支持 `party_order_id` 单独查询；关单仍必须提供原交易的 `org_req_date` 和 `org_req_seq_id`
2. 关单后用户将无法再对该订单进行支付
3. 已支付成功的订单**无法关单**，只能走退款流程（见 [dougong-hostingpay-cashier-refund](../dougong-hostingpay-cashier-refund/SKILL.md)）
4. 建议在收到异步通知后调用查询接口做二次确认
5. 关单前建议先调用查询接口确认订单状态，避免关闭已支付订单
6. 如果用户在关单请求发出的同时完成了支付，以最终交易状态为准
7. 对账单查询通常返回一个下载链接；文件通常是 zip 包内含 csv，但结算资金对账单模板为 xlsx，补生成场景的 `file_date` 需填交易日期 `+1` 天，且对外字段名应直接保持 `file_date`
8. 对账单查询的请求字段名必须保持 `bill_type`；除非用户现有接口已经发布并要求兼容，否则不要再设计 `file_type -> bill_type` 的中间映射

> 快速接入代码示例见 [quickstart.md](references/quickstart.md)。
