---
name: "huifu-prepay-api"
description: "[前端项目使用]实现汇付支付预下单 API 集成。当用户需要实现支付/预下单功能、创建支付请求，或提到“预支付”“ 的时候调用
---

# 汇付支付预支付接口

实现汇付侧预支付接口对接，用于发起支付请求并获取支付跳转链接。

## 触发场景

- 用户需要实现预支付/下单支付功能
- 用户提到"预支付"、"汇付支付"、"支付接口"
- 用户需要创建支付请求并跳转到支付页面

## 接口信息

- **端点**: `/hfpay/preOrder`
- **方法**: POST
- **Content-Type**: application/json

## 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| huifuId | string | 是 | 汇付商户ID |
| transAmt | string | 是 | 交易金额（保留两位小数） |
| goodsDesc | string | 是 | 商品描述 |

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
| uniqueId | string | 唯一请求标识 |
| data | object | 预支付详情对象 |

### data 对象字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| time_expire | string | 订单过期时间（格式：yyyyMMddHHmmss） |
| hosting_data | string | 托管数据（JSON字符串） |
| resp_desc | string | 业务响应描述 |
| pre_order_id | string | 预支付订单ID |
| trans_amt | string | 交易金额 |
| goods_desc | string | 商品描述 |
| pre_order_type | string | 预支付类型 |
| jump_url | string | **支付跳转链接（关键字段）** |
| usage_type | string | 用途类型 |
| req_seq_id | string | 请求流水号 |
| product_id | string | 产品ID |
| req_date | string | 请求日期（格式：yyyyMMdd） |
| resp_code | string | 业务响应码 |
| huifu_id | string | 汇付商户ID |
| order_type | string | 订单类型 |
| current_time | string | 当前时间（格式：yyyyMMddHHmmss） |

## 响应示例

```json
{
  "respCode": "00000000",
  "respDesc": "操作成功",
  "uniqueId": "d4b7ee5942904bfdab0f8c53340aa578",
  "data": {
    "time_expire": "20260310214157",
    "hosting_data": "{\"project_id\":\"PROJECTID2023101225142567\",\"project_title\":\"收银台标题\",\"request_type\":\"P\",\"callback_url\":\"https://paas.huifu.com\",\"private_info\":\"商户私有信息test\"}",
    "resp_desc": "操作成功",
    "pre_order_id": "H202603102131570034276413",
    "trans_amt": "0.10",
    "goods_desc": "dawanji",
    "pre_order_type": "1",
    "jump_url": "https://api.huifu.com/hostingh5/?jump_id=H202603102131570034276413&huifu_id=6666000109133323&bank_switch=Y",
    "usage_type": "P",
    "req_seq_id": "20260310213157551a24fbwn704exdo",
    "product_id": "YYZY",
    "req_date": "20260310",
    "resp_code": "00000000",
    "huifu_id": "6666000109133323",
    "order_type": "HT",
    "current_time": "20260310213157"
  }
}
```

## 代码示例

详细代码示例请参考：

- [JavaScript 示例](./reference/javascript-example.md)
- [Vue 3 Composition API 示例](./reference/vue3-example.md)
- [React 示例](./reference/react-example.md)

## 注意事项

1. 金额需要使用 `toFixed(2)` 保留两位小数
2. 成功响应后需要跳转到 `jump_url` 完成支付
3. 注意 `time_expire` 过期时间，订单超时后需重新下单
4. `req_seq_id` 为请求流水号，可用于后续交易查询
5. 需要处理网络异常和业务错误
6. 建议添加 loading 状态提升用户体验
