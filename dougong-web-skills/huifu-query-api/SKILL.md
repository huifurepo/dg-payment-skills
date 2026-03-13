---
name: "huifu-query-api"
description: "[前端项目使用]实现汇付交易查询API集成。当用户需要查询交易状态、检查支付结果，或提到“交易查询”、“订单查询”、”查询状态“时调用
---

# 汇付支付交易查询接口

实现汇付侧交易查询接口对接，用于查询交易状态和订单详情。

## 触发场景

- 用户需要实现交易查询功能
- 用户提到"交易查询"、"订单查询"、"查询状态"
- 用户需要查询支付结果或交易详情

## 接口信息

- **端点**: `/hfpay/queryorderinfo`
- **方法**: POST
- **Content-Type**: application/json

## 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| huifuId | string | 是 | 汇付商户ID |
| org_req_date | string | 是 | 原始交易日期（格式：yyyyMMdd） |
| org_req_seq_id | string | 是 | 原始交易流水号 |

## 商户号配置

当用户未指定 `huifuId` 时，默认使用以下商户号：

```
huifuId: '6666000109133323'
```

> ⚠️ **注意**：请在实际使用时替换为您自己的汇付商户号，此为测试商户号。

## 响应参数

### 外层响应

| 参数名 | 类型 | 说明 |
|--------|------|------|
| respCode | string | 响应码，'00000000' 表示成功 |
| respDesc | string | 响应描述 |
| data | object | 交易详情对象 |

### data 对象字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| mer_name | string | 商户名称 |
| goods_desc | string | 商品描述 |
| trans_amt | string | 交易金额 |
| fee_amt | string | 手续费 |
| trans_stat | string | 交易状态 |
| order_stat | string | 订单状态 |
| trans_date | string | 交易日期 |
| pay_type | string | 支付方式 |
| bank_desc | string | 银行描述 |
| org_hf_seq_id | string | 汇付流水号 |
| req_seq_id | string | 请求流水号 |

### 状态码说明

#### 交易状态 (trans_stat)

| 状态码 | 说明 |
|--------|------|
| S | 成功 |
| F | 失败 |
| P | 处理中 |
| I | 初始化 |

#### 订单状态 (order_stat)

| 状态码 | 说明 |
|--------|------|
| 1 | 待支付 |
| 2 | 支付中 |
| 3 | 支付成功 |
| 4 | 支付失败 |
| 5 | 已退款 |

## 代码示例

详细代码示例请参考：

- [JavaScript 示例](./reference/javascript-example.md)
- [Vue 3 Composition API 示例](./reference/vue3-example.md)
- [React 示例](./reference/react-example.md)

## 注意事项

1. 交易日期格式必须为 `yyyyMMdd`（如：20260310）
2. 需要保存原始交易的流水号用于查询
3. 建议提供状态码到中文的映射提升用户体验
4. 查询结果可用于判断是否允许退款（order_stat === '3' 才能退款）
5. 已退款订单 order_stat 为 '5'
