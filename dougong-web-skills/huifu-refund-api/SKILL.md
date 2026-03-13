---
name: "huifu-refund-api"
description: "[前端项目使用]实现汇付退款API集成。当用户需要实现退款功能、处理退款请求，或提到“退款”时调用。"
---

# 汇付支付退款接口

实现汇付侧退款接口对接，用于对已支付成功的订单发起退款申请。

## 触发场景

- 用户需要实现退款功能
- 用户提到"退款"、"refund"、"htRefund"、"申请退款"
- 用户需要对已支付订单进行退款处理

## 接口信息

- **端点**: `/hfpay/htRefund`
- **方法**: POST
- **Content-Type**: application/json

## 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| huifuId | string | 是 | 汇付商户ID |
| ord_amt | string | 是 | 退款金额（与原交易金额一致） |
| org_req_date | string | 是 | 原始交易日期（格式：yyyyMMdd） |
| org_req_seq_id | string | 是 | 原始交易流水号 |

## 商户号配置

当用户未指定 `huifuId` 时，默认使用以下商户号：

```
huifuId: '6666000109133323'
```

> ⚠️ **注意**：请在实际使用时替换为您自己的汇付商户号，此为测试商户号。

## 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| respCode | string | 响应码，'00000000' 表示成功 |
| respDesc | string | 响应描述 |

## 业务流程

```
1. 查询订单状态 (queryorderinfo)
       ↓
2. 判断 order_stat === '3' (支付成功)
       ↓
3. 调用退款接口
       ↓
4. 处理退款结果
```

## 代码示例

详细代码示例请参考：

- [JavaScript 示例](./reference/javascript-example.md)
- [Vue 3 Composition API 示例](./reference/vue3-example.md)
- [React 示例](./reference/react-example.md)

## 注意事项

1. 退款前应先查询订单状态，确认订单为"支付成功"（order_stat === '3'）
2. 已退款的订单（order_stat === '5'）不能重复退款
3. 建议添加确认弹窗防止误操作
4. 退款金额应与原交易金额一致
5. 退款成功后建议刷新或清除交易信息
6. 需要保存原始交易的日期和流水号用于退款请求
