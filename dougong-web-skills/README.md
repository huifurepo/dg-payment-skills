# 前端调用后端汇付支付技能目录

本目录包含汇付支付相关的三个 API 集成技能。

## 技能列表

| 技能 | 说明 | 触发关键词 |
|------|------|-----------|
| [huifu-prepay-api](./huifu-prepay-api/) | 汇付支付预下单 API | 预支付、支付接口、创建支付请求 |
| [huifu-query-api](./huifu-query-api/) | 汇付交易查询 API | 交易查询、订单查询、查询状态 |
| [huifu-refund-api](./huifu-refund-api/) | 汇付退款 API | 退款、refund、申请退款 |

## 使用方式

当需要使用对应功能时，调用相应的技能即可：

- `/huifu-prepay-api` - 实现支付/预下单功能
- `/huifu-query-api` - 查询交易状态和订单详情
- `/huifu-refund-api` - 处理退款申请

## 各技能详情

### 1. huifu-prepay-api (预下单)

- **端点**: `/hfpay/preOrder`
- **用途**: 发起支付请求并获取支付跳转链接
- **返回**: `jump_url` 支付跳转链接

### 2. huifu-query-api (交易查询)

- **端点**: `/hfpay/queryorderinfo`
- **用途**: 查询交易状态和订单详情
- **返回**: 订单状态 `order_stat` (1-待支付, 3-支付成功, 5-已退款)

### 3. huifu-refund-api (退款)

- **端点**: `/hfpay/htRefund`
- **用途**: 对已支付订单发起退款
- **前提**: 订单状态为 `order_stat === '3'` (支付成功)

## 代码示例

每个技能目录下都包含参考示例：

- `reference/javascript-example.md` - 原生 JavaScript
- `reference/vue3-example.md` - Vue 3 Composition API
- `reference/react-example.md` - React
