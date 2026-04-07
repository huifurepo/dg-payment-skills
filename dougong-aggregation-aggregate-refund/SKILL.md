---
name: dougong-aggregation-aggregate-refund
description: "汇付聚合支付（dg-lightning-sdk）退款 Skill：聚合交易退款和退款结果查询。当开发者需要对聚合支付订单发起退款或查询退款状态时使用。触发词：聚合退款、聚合退款申请、聚合退款查询、聚合退款状态。"
license: MIT
compatibility: "Java 8+, Maven, Spring Boot 2.x/3.x"
source: "https://github.com/niceforbear/huifu-hosting-payment"
dependencies:
  - dougong-aggregation-pay-base
env:
  - HUIFU_REFUND_NOTIFY_URL
metadata:
  author: codecodeing
  version: 1.0.0
  bins: java, mvn
---

# 聚合支付 — 退款

交易退款 + 退款结果查询。

> **前置依赖**：首次接入请先阅读 [dougong-aggregation-pay-base](../dougong-aggregation-pay-base/SKILL.md) 完成 SDK 初始化。

> **进入本 Skill 前先确认**：原交易定位键已经在订单侧沉淀，退款请求也按 [payload-construction.md](../dougong-aggregation-pay-base/references/payload-construction.md) 做过必填 / 条件必填校验，避免把缺少原交易标识的请求直接打到汇付。

## 触发词

- "聚合退款"、"聚合退款申请"、"聚合交易退款"
- "聚合退款查询"、"聚合退款状态"、"查询聚合退款结果"

## 场景路由

| 用户意图 | 场景 | 详细说明 |
|---------|------|---------|
| 对已支付订单发起退款 | 交易退款 | 见 [refund.md](references/refund.md) |
| 查询退款结果 | 退款结果查询 | 见 [refund-query.md](references/refund-query.md) |

## 退款流程

```
1. 确认原交易已支付成功（trans_stat=S）
2. 调用退款接口 v4/trade/payment/scanpay/refund
3. 退款 resp_code=00000100（处理中）是正常的
4. 等待异步通知或轮询退款查询接口
5. 退款成功（trans_stat=S）后执行业务退款逻辑
```

## 退款期限

| 渠道 | 最大退款期限 |
|------|-----------|
| 微信 | 360天 |
| 支付宝 | 360天 |
| 银联二维码 | 360天 |

## 注意事项

1. **退款金额不能超过原交易金额**（延时交易退款金额须≤待确认金额）
2. `resp_code=00000000` 或 `00000100` 仅表示退款请求**已受理**
3. 退款最终结果以**异步通知**或**退款查询接口**为准
4. 退款成功后资金**原路返回**给用户
5. 退款为异步处理，请做好**幂等校验**
6. 原交易定位键为 `org_hf_seq_id`、`org_party_order_id`、`org_req_seq_id` 三选一
7. `remark`、`notify_url`、`tx_metadata` 通常通过 `client.optional()` 或 `request.optional()` 传入
8. 退款查询使用的是退款标识：`org_hf_seq_id`、退款 `org_req_seq_id`、`mer_ord_id` 三选一；传退款全局流水号时 `org_req_date` 可不传
9. 退款涉及资金变动，日志中记录关键参数但**避免打印完整密钥**

## 流水号关系

退款涉及三层流水号，需清楚关联关系：

```
① 原交易下单：req_seq_id = "A001"（原支付流水号）
② 退款请求：  req_seq_id = "B001"（退款流水号），org_req_seq_id = "A001"
③ 退款查询：  org_req_seq_id = "B001"（查的是退款的流水号）
                org_hf_seq_id = 退款返回的 hf_seq_id（也可以用这个查）
```

> 快速接入代码示例见 [quickstart.md](references/quickstart.md)。
