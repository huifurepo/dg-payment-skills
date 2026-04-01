---
name: donggong-aggregation-aggregate-order
description: "汇付聚合支付（dg-lightning-sdk）下单 Skill：覆盖微信公众号/小程序/APP、支付宝JS/正扫、银联JS/正扫、微信/支付宝/银联付款码等全场景聚合支付下单。当开发者需要通过聚合支付方式创建支付订单时使用。触发词：聚合支付下单、微信支付下单、支付宝下单、银联下单、二维码支付、付款码支付。"
license: MIT
compatibility: "Java 8+, Maven, Spring Boot 2.x/3.x"
source: "https://github.com/niceforbear/huifu-hosting-payment"
dependencies:
  - donggong-aggregation-pay-base
env:
  - HUIFU_NOTIFY_URL
metadata:
  author: jiaxiang.li
  version: 1.0.0
  bins: java, mvn
---

# 聚合支付 — 下单

覆盖微信/支付宝/银联全场景聚合支付下单。

> **前置依赖**：首次接入请先阅读 [donggong-aggregation-pay-base](../donggong-aggregation-pay-base/SKILL.md) 完成 SDK 初始化。

> **开发前先补两步**：先核对 [客户前置准备清单](../donggong-aggregation-pay-base/references/customer-preparation.md)，再按 [参数校验与 JSON 构造规范](../donggong-aggregation-pay-base/references/payload-construction.md) 建模。`sub_openid`、`buyer_id`、`auth_code`、`devs_id`、`customer_ip` 这些值都不能让模型自行猜测。

> **官方开发指引补充约束**：接入前还要完成渠道业务开通、应用配置或授权绑定。微信公众号 / 小程序场景的 `sub_openid`、支付宝 JS 的 `buyer_id`、银联 JS 的 `user_id`、各类反扫的 `auth_code`，都必须来自真实获取链路；前端支付完成回调也不等于最终交易成功。

## 端到端支付流程

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────┐     ┌──────────┐
│ ① 下单    │────→│ ② 用户支付 │────→│ ③ 异步通知    │────→│ ④ 查询确认 │────→│ ⑤ 退款    │
│ (本 Skill) │     │ (前端处理) │     │ (回调 notify) │     │ (二次校验) │     │ (可选)    │
└──────────┘     └──────────┘     └──────────────┘     └──────────┘     └──────────┘
```

### ① 下单（本 Skill）

调用 `v4/trade/payment/create` 创建支付订单，根据 trade_type 返回不同结果：
- **正扫**（NATIVE）：返回 `qr_code`（二维码 URL）
- **JS 支付**（JSAPI/MINIAPP）：返回 `pay_info`（JS 调起参数）
- **反扫**（MICROPAY）：同步返回支付结果

同时**保存 `req_seq_id` 和 `req_date`**（后续所有操作都需要）。

### ② 用户支付

- **正扫**：前端将 qr_code 生成二维码展示，用户扫码支付
- **JS 支付**：前端使用 pay_info 调起微信/支付宝/银联支付
- **反扫**：无需用户操作，商户扫描用户付款码后同步完成

### ③ 接收异步通知

汇付将交易结果 POST 到 `notify_url`：
- 返回 `RECV_ORD_ID_` + req_seq_id（5 秒内）
- 以 `hf_seq_id` 为幂等键
- 详见 [tech-spec.md](../donggong-aggregation-pay-base/references/tech-spec.md)

### ④ 二次查询确认

见 [donggong-aggregation-aggregate-query](../donggong-aggregation-aggregate-query/SKILL.md)。官方微信 / 支付宝 / 银联开发指引都明确要求：用户前端页面收到支付完成回调后，后端仍需调用查询订单 API 确认最终状态。

### ⑤ 退款（可选）

见 [donggong-aggregation-aggregate-refund](../donggong-aggregation-aggregate-refund/SKILL.md)

---

## 触发词

- "聚合支付下单"、"创建支付订单"、"发起支付"
- "微信支付下单"、"微信公众号支付"、"微信小程序支付"
- "支付宝下单"、"支付宝JS支付"、"支付宝正扫"
- "银联下单"、"银联JS"、"银联正扫"
- "付款码支付"、"反扫支付"、"扫码支付"
- "二维码支付"、"正扫支付"

## 场景路由

根据支付场景选择对应 trade_type：

| 用户意图 | trade_type | 返回关键字段 | 详细说明 |
|---------|-----------|-------------|---------|
| 微信公众号内支付 | T_JSAPI | pay_info | 见 [aggregate-order-method-wechat.md](references/aggregate-order-method-wechat.md) |
| 微信小程序支付 | T_MINIAPP | pay_info | 同上 |
| 微信APP支付 | T_APP | pay_info | 同上 |
| 微信付款码（反扫） | T_MICROPAY | 同步结果 | 同上 |
| 支付宝JS支付 | A_JSAPI | pay_info | 见 [aggregate-order-method-alipay.md](references/aggregate-order-method-alipay.md) |
| 支付宝正扫 | A_NATIVE | qr_code | 同上 |
| 支付宝付款码（反扫） | A_MICROPAY | 同步结果 | 同上 |
| 银联JS支付 | U_JSAPI | pay_info | 见 [aggregate-order-method-unionpay.md](references/aggregate-order-method-unionpay.md) |
| 银联正扫 | U_NATIVE | qr_code | 同上 |
| 银联付款码（反扫） | U_MICROPAY | 同步结果 | 同上 |

## 官方场景前置条件

| 场景 | 开发前必须完成什么 | 关键运行时值 |
|------|------------------|-------------|
| 微信公众号支付 | 准备公众号、完成商户进件并开通微信业务、配置支付授权目录 | `sub_openid` |
| 微信小程序支付 | 准备小程序、完成商户进件并开通微信业务、确认 `sub_appid` 绑定关系 | `sub_openid` |
| 支付宝 JS 支付 | 完成商户进件并开通支付宝业务 | `buyer_id` / `buyer_logon_id` |
| 银联 JS 支付 | 完成商户进件并开通银联业务、准备网页授权回调链路 | `user_id`、`customer_ip` |
| 微信 / 支付宝 / 银联付款码 | 准备扫码设备或收银终端 | `auth_code` |

## 汇付 API 端点

| 属性 | 值 |
|-----|-----|
| API 路径 | `v4/trade/payment/create` |
| 请求方式 | POST |
| Content-Type | application/json |

## 通用架构

```
PayController (@RestController, /api/pay)
    └── POST /create → payService.createOrder(req)

PayService (@Service)
    └── createOrder() → Factory.Payment.Common().create(request)

PayOrderReq (DTO)
    ├── huifuId      — 商户号（必填）
    ├── transAmt     — 交易金额（必填）
    ├── tradeType    — 支付类型（必填）
    ├── goodsDesc    — 商品描述（必填）
    ├── methodExpand — 渠道扩展参数（业务层保持对象结构，按 trade_type 决定）
    └── txMetadata   — 分账 / 设备 / 补贴对象（进入 SDK 前再序列化）
```

## 通用请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| huifu_id | String(32) | Y | 商户号 |
| req_date | String(8) | N | 请求日期 yyyyMMdd；官方表标非必填，但实务上建议始终传 |
| req_seq_id | String(128) | Y | 请求流水号，当天唯一 |
| trade_type | String(16) | Y | 支付类型（见场景路由表） |
| trans_amt | String(14) | Y | 交易金额，单位元，保留两位小数，最低 0.01 |
| goods_desc | String(128) | Y | 商品描述 |
| method_expand | String | C | 交易类型扩展参数（JSON），是否必填取决于 trade_type |
| notify_url | String(504) | N | 异步通知地址 |
| time_expire | String(14) | N | 交易失效时间 yyyyMMddHHmmss |
| delay_acct_flag | String(1) | N | 是否延迟入账，Y=延迟、N=不延迟 |
| fee_flag | String(1) | N | 手续费标记 |
| tx_metadata | String | N | 扩展参数集合（JSON），含分账、设备、补贴、手续费补贴 |
| remark | String(255) | N | 备注，原样返回 |

## 通用同步返回参数

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 业务响应码 |
| resp_desc | String(512) | 业务响应信息 |
| huifu_id | String(32) | 商户号 |
| req_date | String(8) | 请求日期 |
| req_seq_id | String(128) | 请求流水号 |
| hf_seq_id | String(128) | 汇付全局流水号 |
| trade_type | String(16) | 支付类型 |
| trans_amt | String(14) | 交易金额 |
| trans_stat | String(1) | 交易状态：P=处理中、S=成功、F=失败 |
| qr_code | String | 二维码 URL（正扫场景返回） |
| pay_info | String | JS 支付调起参数（JS/小程序场景返回） |
| out_trans_id | String(64) | 用户账单交易订单号 |
| party_order_id | String(64) | 用户账单商户订单号 |
| delay_acct_flag | String(1) | 是否延迟交易 |
| tx_metadata | String | 扩展参数集合（补贴、设备、手续费补贴） |
| payment_fee | String | 手续费对象 |

> **重要**：调用成功后务必保存 `req_seq_id` 和 `req_date`，后续查询、退款、关单均需使用。

## method_expand 各场景必填字段

| trade_type | 必填字段 | 说明 |
|-----------|---------|------|
| T_JSAPI | sub_appid, sub_openid | 微信公众号 AppID + 用户 OpenID |
| T_MINIAPP | sub_appid, sub_openid | 微信小程序 AppID + 用户 OpenID |
| T_APP | sub_appid | 微信 APP 场景通常至少传子商户应用 ID |
| T_MICROPAY | auth_code | 用户微信付款码（18位数字） |
| A_JSAPI | buyer_id 或 buyer_logon_id | 二选一；直连模式下还常传 `subject` 等支付宝扩展参数 |
| A_NATIVE | 按场景可选 | 官方给了完整支付宝扩展结构，营销/直连场景可能会传 |
| A_MICROPAY | auth_code | 用户支付宝付款码 |
| U_JSAPI | user_id, qr_code, customer_ip | 官方开发指引要求先通过授权流程拿到 `user_id`，且 JS 支付必传持卡人 IP |
| U_NATIVE | 按场景可选 | 官方给了与 U_JSAPI 同结构的银联扩展参数 |
| U_MICROPAY | auth_code | 用户云闪付付款码；银联侧还有 `pid_info` 等扩展字段 |

## SDK Request 类

| Request 类 | 包路径 |
|-----------|-------|
| `TradePaymentCreateRequest` | `com.huifu.dg.lightning.models.payment` |

## 常见错误与排查

| 错误码 | 原因 | 排查方法 |
|-------|------|---------|
| 10000000 | 参数校验失败 | 检查必填字段格式 |
| 20000000 | 重复交易 | 确认 req_seq_id 当天唯一 |
| 22000000 | 产品号不存在 | 检查 product_id 配置 |
| 22000002 | 商户信息不存在 | 检查 huifu_id |
| 22000005 | 分账/费率/入驻配置有误 | 检查多通道、分账、贴息和费率配置 |
| 90000000 | 业务执行失败 | 查看 resp_desc 详情 |

**网络/系统错误**：未收到响应或超时时，调用查询接口确认状态，切勿直接判定为失败。

## Reference 地图

| 文件 | 内容 |
|------|------|
| [references/aggregate-order.md](references/aggregate-order.md) | 总览与阅读导航 |
| [references/aggregate-order-request.md](references/aggregate-order-request.md) | 公共请求参数与顶层字段 |
| [references/aggregate-order-method-wechat.md](references/aggregate-order-method-wechat.md) | 微信请求与回调字段 |
| [references/aggregate-order-method-alipay.md](references/aggregate-order-method-alipay.md) | 支付宝请求与回调字段 |
| [references/aggregate-order-method-unionpay.md](references/aggregate-order-method-unionpay.md) | 银联请求与回调字段 |
| [references/aggregate-order-tx-metadata.md](references/aggregate-order-tx-metadata.md) | 分账、补贴、设备、手续费对象 |
| [references/aggregate-order-response.md](references/aggregate-order-response.md) | 同步返回、异步回调、解冻通知 |
| [references/aggregate-order-errors.md](references/aggregate-order-errors.md) | 返回码与文档勘误 |
| [references/quickstart.md](references/quickstart.md) | 快速接入摘要 |
