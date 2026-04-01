## 目录

- [接口概述](#接口概述)
- [阅读地图](#阅读地图)
- [支付场景路由](#支付场景路由)
- [SDK 入口与实现要点](#sdk-入口与实现要点)
- [分册说明](#分册说明)

# 聚合下单接口总览

> 本文依据 2025-11-05 官方文档整理，适用于 `v4/trade/payment/create`。
> 本文件只负责导航与总览，完整参数已按主题拆分到多个 reference。

## 接口概述

| 属性 | 值 |
|------|-----|
| 请求方式 | `POST` |
| 汇付 API 端点 | `https://api.huifu.com/v4/trade/payment/create` |
| SDK Request 类 | `TradePaymentCreateRequest` |
| SDK Client 方法 | `Factory.Payment.Common().create(request)` |
| Content-Type | `application/json` |

说明：

- 聚合支付将微信、支付宝、银联等多种支付方式统一到一个下单 API。
- 请求和响应整体都需要签名，验签规则见 `donggong-aggregation-pay-base/references/tech-spec.md`。
- `method_expand`、`tx_metadata`、异步 `resp_data` 里的多个字段，外层通常是 `String`，值内容是 JSON 字符串。
- 下单结果不能只看 `resp_code`；官方特别强调最终交易状态以 `trans_stat` 为准。
- 交易完成后除标准异步通知外，还支持额外发送 Webhook 事件。

## 阅读地图

| 文档 | 内容 |
|------|------|
| [aggregate-order-request.md](aggregate-order-request.md) | 公共请求参数、`data` 顶层字段、`trade_type` 与 `limit_pay_type` |
| [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) | 微信公众号 / 小程序 / APP / 反扫的请求与回调字段 |
| [aggregate-order-method-alipay.md](aggregate-order-method-alipay.md) | 支付宝 JS / 正扫 / 反扫的请求与回调字段 |
| [aggregate-order-method-unionpay.md](aggregate-order-method-unionpay.md) | 银联 JS / 正扫 / 反扫的请求与回调字段 |
| [aggregate-order-tx-metadata.md](aggregate-order-tx-metadata.md) | `tx_metadata`、`payment_fee`、分账与手续费扩展结构 |
| [aggregate-order-response.md](aggregate-order-response.md) | 同步返回、异步回调、解冻通知、反扫回调差异 |
| [aggregate-order-errors.md](aggregate-order-errors.md) | 业务返回码、反扫返回码、文档勘误与实现备注 |

## 支付场景路由

| 用户场景 | `trade_type` | 同步返回关键字段 | 详细文档 |
|----------|--------------|------------------|----------|
| 微信公众号支付 | `T_JSAPI` | `pay_info` | [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) |
| 微信小程序支付 | `T_MINIAPP` | `pay_info` | [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) |
| 微信 APP 支付 | `T_APP` | `pay_info` | [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) |
| 微信付款码反扫 | `T_MICROPAY` | 同步受理结果 | [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) |
| 支付宝 JS 支付 | `A_JSAPI` | `pay_info` | [aggregate-order-method-alipay.md](aggregate-order-method-alipay.md) |
| 支付宝正扫 | `A_NATIVE` | `qr_code` | [aggregate-order-method-alipay.md](aggregate-order-method-alipay.md) |
| 支付宝付款码反扫 | `A_MICROPAY` | 同步受理结果 | [aggregate-order-method-alipay.md](aggregate-order-method-alipay.md) |
| 银联 JS 支付 | `U_JSAPI` | `pay_info` | [aggregate-order-method-unionpay.md](aggregate-order-method-unionpay.md) |
| 银联正扫 | `U_NATIVE` | `qr_code` | [aggregate-order-method-unionpay.md](aggregate-order-method-unionpay.md) |
| 银联付款码反扫 | `U_MICROPAY` | 同步受理结果 | [aggregate-order-method-unionpay.md](aggregate-order-method-unionpay.md) |

## SDK 入口与实现要点

`TradePaymentCreateRequest` 的核心字段：

| 字段 | 建议传入方式 | 说明 |
|------|--------------|------|
| `reqDate` | `setReqDate()` | 请求日期，`yyyyMMdd`；官方表标 N，但实务上建议始终传 |
| `reqSeqId` | `setReqSeqId()` | 请求流水号，当天唯一 |
| `huifuId` | `setHuifuId()` | 商户号 |
| `tradeType` | `setTradeType()` | 交易类型 |
| `transAmt` | `setTransAmt()` | 交易金额 |
| `goodsDesc` | `setGoodsDesc()` | 商品描述 |
| `methodExpand` | `setMethodExpand()` 或 `client.optional("method_expand", ...)` | 渠道扩展参数 |
| `delayAcctFlag` | `setDelayAcctFlag()` | 延迟标识 |

其余业务字段在本 skill 库的 SDK 接入实践中更稳妥的方式：

- `notify_url`、`remark`、`acct_id`、`time_expire`、`fee_flag`
- `limit_pay_type`、`channel_no`、`pay_scene`
- `term_div_coupon_type`、`fq_mer_discount_flag`
- `tx_metadata`

统一建议通过 `client.optional(key, value)` 传入；如果你当前 SDK 版本恰好提供独立 setter，也可以直接使用 setter。

实现注意：

- 成功受理后务必保存 `req_seq_id` 和 `req_date`。
- 二维码类场景使用 `qr_code`，JS / 小程序 / APP 类场景使用 `pay_info`。
- 反扫场景的同步返回不等于最终成功，仍要依赖 `trans_stat` 与异步通知。
- 查询、关单、退款等后续动作都依赖最初下单保存的流水号。

## 分册说明

- `aggregate-order-request.md` 负责“怎么发请求”。
- `aggregate-order-method-*.md` 负责“不同支付渠道怎样组织 `method_expand`、怎样解析渠道返回”。
- `aggregate-order-tx-metadata.md` 负责“分账、补贴、设备、手续费补贴”。
- `aggregate-order-response.md` 负责“同步 / 异步 / 解冻回调”。
- `aggregate-order-errors.md` 负责“返回码 + 勘误”。

这种拆分方式保留完整型 reference 的可读性，同时避免单文件超过项目的 500 行限制。
