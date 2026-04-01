# 聚合下单请求参数

> 本文只覆盖请求侧参数；渠道扩展参数请继续阅读各渠道分册。

## 公共请求参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `sys_id` | 系统号 | String | 32 | Y | 渠道商 / 商户的 `huifu_id` |
| `product_id` | 产品号 | String | 32 | Y | 汇付分配的产品号 |
| `sign` | 加签结果 | String | 512 | Y | 对整个请求报文签名 |
| `data` | 数据 | Json | - | Y | 业务请求参数 |

## `data` 顶层字段

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `req_date` | 请求日期 | String | 8 | N | `yyyyMMdd` |
| `req_seq_id` | 请求流水号 | String | 128 | Y | 请求流水号 |
| `huifu_id` | 商户号 | String | 32 | Y | 商户号 |
| `trade_type` | 交易类型 | String | 16 | Y | 见下方枚举 |
| `trans_amt` | 交易金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| `goods_desc` | 商品描述 | String | 128 | Y | 商品描述 |
| `remark` | 备注 | String | 255 | N | 原样返回 |
| `acct_id` | 账户号 | String | 9 | N | 指定收款账户号，仅支持基本户、现金户 |
| `time_expire` | 交易有效期 | String | 14 | N | `yyyyMMddHHmmss` |
| `delay_acct_flag` | 延迟标识 | String | 1 | N | `Y`=延迟，`N`=不延迟，默认 `N` |
| `fee_flag` | 手续费扣款标识 | Integer | 1 | N | `1`=外扣，`2`=内扣 |
| `limit_pay_type` | 禁用支付方式 | String | 128 | N | 见下方枚举 |
| `channel_no` | 渠道号 | String | 32 | N | 自有渠道号 |
| `pay_scene` | 场景类型 | String | 2 | N | 微信业务开通类型 |
| `term_div_coupon_type` | 分账遇到优惠的处理规则 | String | 2 | N | `1`=按比例分，`2`=按顺序保障，`3`=只给交易商户 |
| `fq_mer_discount_flag` | 商户贴息标记 | String | 1 | N | `Y`=商户全额贴息，`P`=商户部分贴息 |
| `notify_url` | 异步通知地址 | String | 504 | N | HTTP 或 HTTPS 地址 |
| `method_expand` | 交易类型扩展参数 | String(JSON Object) | - | Y | 按 `trade_type` 选择对应结构 |
| `tx_metadata` | 扩展参数集合 | String(JSON Object) | - | C | 分账、补贴、设备等交易能力扩展 |

## `trade_type` 枚举

| 枚举值 | 场景 | 详细文档 |
|--------|------|----------|
| `T_JSAPI` | 微信公众号支付 | [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) |
| `T_MINIAPP` | 微信小程序支付 | [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) |
| `T_APP` | 微信 APP 支付 | [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) |
| `T_MICROPAY` | 微信付款码反扫 | [aggregate-order-method-wechat.md](aggregate-order-method-wechat.md) |
| `A_JSAPI` | 支付宝 JS 支付 | [aggregate-order-method-alipay.md](aggregate-order-method-alipay.md) |
| `A_NATIVE` | 支付宝正扫 | [aggregate-order-method-alipay.md](aggregate-order-method-alipay.md) |
| `A_MICROPAY` | 支付宝付款码反扫 | [aggregate-order-method-alipay.md](aggregate-order-method-alipay.md) |
| `U_JSAPI` | 银联 JS 支付 | [aggregate-order-method-unionpay.md](aggregate-order-method-unionpay.md) |
| `U_NATIVE` | 银联正扫 | [aggregate-order-method-unionpay.md](aggregate-order-method-unionpay.md) |
| `U_MICROPAY` | 银联付款码反扫 | [aggregate-order-method-unionpay.md](aggregate-order-method-unionpay.md) |

## 官方开发指引确认的关键字段来源

| 场景 | 关键字段 | 来源要求 |
|------|---------|---------|
| `T_JSAPI` | `sub_openid` | 必须通过当前公众号 `appid` 的网页授权流程获取 |
| `T_MINIAPP` | `sub_openid` | 必须通过当前小程序 `sub_appid` 获取，不能与其他小程序混用 |
| `A_JSAPI` | `buyer_id` | 必须通过支付宝 `user_id` 获取流程拿到 |
| `U_JSAPI` | `user_id` | 必须先走银联网页授权拿 `auth_code`，再换取 `user_id` |
| `T_MICROPAY` / `A_MICROPAY` / `U_MICROPAY` | `auth_code` | 必须来自扫码设备实时采集，不得写死在配置里 |
| `U_JSAPI` | `customer_ip` | 必须来自真实客户端 IP，不能用示例值或固定内网地址代替 |

## `limit_pay_type` 枚举

| 取值 | 说明 |
|------|------|
| `NO_CREDIT` | 禁用信用卡；使用花呗支付时不能禁用信用卡 |
| `BALANCE` | 禁用支付宝余额 |
| `MONEY_FUND` | 禁用支付宝余额宝 |
| `BANK_PAY` | 禁用网银，仅支持支付宝 |
| `DEBIT_CARD_EXPRESS` | 禁用借记卡快捷，仅支持支付宝 |
| `CREDIT_CARD_EXPRESS` | 禁用信用卡快捷，仅支持支付宝 |
| `CREDIT_CARD_CARTOON` | 禁用信用卡卡通，仅支持支付宝 |
| `CARTOON` | 禁用卡通，仅支持支付宝 |
| `PCREDIT` | 禁用支付宝花呗 |
| `PCREDIT_PAY_INSTALLMENT` | 禁用支付宝花呗分期 |
| `CREDIT_GROUP` | 禁用支付宝信用支付类型组合 |
| `COUPON` | 禁用支付宝红包 |
| `POINT` | 禁用支付宝积分 |
| `PROMOTION` | 禁用支付宝优惠 |
| `VOUCHER` | 禁用支付宝营销券 |
| `MDISCOUNT` | 禁用支付宝商户优惠 |
| `HONEY_PAY` | 禁用支付宝亲密付 |
| `MCARD` | 禁用支付宝商户预存卡 |
| `PCARD` | 禁用支付宝个人预存卡 |

## 请求示例

```json
{
  "sys_id": "6666000103334211",
  "product_id": "MCS",
  "data": {
    "req_date": "20250828",
    "req_seq_id": "202508281506304989897129zz",
    "huifu_id": "6666000108604566",
    "trade_type": "U_MICROPAY",
    "trans_amt": "0.01",
    "goods_desc": "银联反扫测试",
    "delay_acct_flag": "N",
    "method_expand": "{\"U_MICROPAY\":{\"auth_code\":\"2884138408701518074\"}}",
    "tx_metadata": "{\"terminal_device_data\":{\"device_ip\":\"10.10.0.1\"}}"
  },
  "sign": "RSA签名"
}
```

## 请求侧实现备注

- 官方把 `req_date` 标成 N，但 SDK 示例和后续查询 / 回调都依赖它，实务上建议始终传。
- 官方把 `method_expand` 标成 Y，但真实是否有强制子字段取决于 `trade_type`。
- `tx_metadata` 的完整结构见 [aggregate-order-tx-metadata.md](aggregate-order-tx-metadata.md)。

## 参数校验与构造约束

- `trade_type` 决定 `method_expand` 的对象结构，先校验场景，再决定哪些子字段必须出现。
- `method_expand`、`tx_metadata` 在业务层不要设计成裸字符串；优先用嵌套 DTO / `Map` / `List` / `ObjectNode` 建模。
- 只在调用 SDK 前做一次 JSON 序列化，不要在代码里手写长字符串常量。
- 对象一旦出现，就要保证子结构完整；不要只传一个空壳对象或半截 JSON。
- `sub_openid`、`buyer_id`、`user_id`、`auth_code`、`customer_ip`、`devs_id` 这类值若无明确来源，应先暴露缺口，不要让模型补示例值。

推荐写法：

```java
Map<String, Object> methodExpand = new HashMap<>();
methodExpand.put("T_MINIAPP", wechatMethodExpand);
request.setMethodExpand(objectMapper.writeValueAsString(methodExpand));

if (txMetadata != null) {
    request.setTxMetadata(objectMapper.writeValueAsString(txMetadata));
}
```
