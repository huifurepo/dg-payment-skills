# 聚合扫码交易退款

## 目录

- [接口概览](#接口概览)
- [SDK 映射](#sdk-映射)
- [公共参数](#公共参数)
- [请求参数](#请求参数)
- [同步返回参数](#同步返回参数)
- [异步返回参数](#异步返回参数)
- [请求示例](#请求示例)
- [同步返回示例](#同步返回示例)
- [业务返回码](#业务返回码)
- [实现备注与文档勘误](#实现备注与文档勘误)

## 接口概览

| 项 | 值 |
| --- | --- |
| 接口名称 | 扫码交易退款 |
| 汇付端点 | `POST /v4/trade/payment/scanpay/refund` |
| 官方最近更新时间 | `2025-11-14` |
| 支持格式 | `JSON` |
| 支持交易 | `T_JSAPI`、`T_MINIAPP`、`T_APP`、`A_JSAPI`、`A_NATIVE`、`U_NATIVE`、`U_JSAPI`、`T_MICROPAY`、`A_MICROPAY`、`U_MICROPAY` |
| 最大退款期限 | 微信 360 天，支付宝 360 天，银联二维码 360 天 |
| 签名说明 | [接入指引-开发指南](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |

交易发生后，如因用户或商户原因需要退款，可通过本接口将支付款原路退回。适用于已开通微信、支付宝、银联二维码聚合扫码功能的商户。

## SDK 映射

| 项 | 值 |
| --- | --- |
| SDK Request 类 | `TradePaymentScanpayRefundRequest` |
| 包路径 | `com.huifu.dg.lightning.models.payment` |
| SDK Client 方法 | `Factory.Payment.Common().refund(request)` |

`TradePaymentScanpayRefundRequest` 常用字段映射：

| 字段 | setter | 必填 | 说明 |
| --- | --- | --- | --- |
| `req_date` | `setReqDate()` | Y | 请求日期，`yyyyMMdd` |
| `req_seq_id` | `setReqSeqId()` | Y | 请求流水号，同一 `huifu_id` 下当天唯一 |
| `huifu_id` | `setHuifuId()` | Y | 商户号 |
| `ord_amt` | `setOrdAmt()` | Y | 申请退款金额，单位元，两位小数 |
| `org_req_date` | `setOrgReqDate()` | Y | 原交易请求日期 |
| `org_hf_seq_id` | `setOrgHfSeqId()` | C | 原交易全局流水号，三选一 |
| `org_party_order_id` | `setOrgPartyOrderId()` | C | 原交易微信/支付宝商户单号，三选一 |
| `org_req_seq_id` | `setOrgReqSeqId()` | C | 原交易请求流水号，三选一 |

无独立 setter、通常通过 `client.optional()` 或 `request.optional()` 传入的字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `remark` | N | 备注，原样返回 |
| `notify_url` | N | 退款异步通知地址 |
| `tx_metadata` | N | 扩展参数集合，JSON 字符串 |

## 公共参数

### 公共请求参数

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sys_id` | String | 32 | Y | 渠道商或商户的 `huifu_id` |
| `product_id` | String | 32 | Y | 汇付分配的产品号，例如 `YYZY` |
| `sign` | String | 512 | Y | 请求签名 |
| `data` | JSON | - | Y | 业务请求参数 |

### 公共返回参数

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `sign` | String | 512 | Y | 响应签名 |
| `data` | JSON | - | N | 业务返回体 |

## 请求参数

### `data`

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `req_date` | String | 8 | Y | 请求日期，格式 `yyyyMMdd` |
| `req_seq_id` | String | 128 | Y | 请求流水号，同一 `huifu_id` 下当天唯一 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `ord_amt` | String | 14 | Y | 申请退款金额，单位元，两位小数，最低 `0.01` |
| `org_req_date` | String | 8 | Y | 原交易请求日期，格式 `yyyyMMdd` |
| `org_hf_seq_id` | String | 128 | C | 原交易全局流水号，和 `org_party_order_id`、`org_req_seq_id` 三选一 |
| `org_party_order_id` | String | 64 | C | 原交易微信/支付宝商户单号，三选一 |
| `org_req_seq_id` | String | 128 | C | 原交易请求流水号，三选一 |
| `remark` | String | 84 | N | 备注，原样返回 |
| `notify_url` | String | 512 | N | 异步通知地址 |
| `tx_metadata` | String | - | N | 扩展参数集合，JSON 字符串 |

### 请求规则

- 原交易定位键 `org_hf_seq_id`、`org_party_order_id`、`org_req_seq_id` 三选一，不能同时为空。
- 若原交易是延时交易，退款金额 `ord_amt` 必须小于等于待确认金额。
- 数字货币退款存在“退款原因必填”的返回码约束，实务上通常通过 `remark` 承载。
- 同一笔交易支持多次部分退款，但累计退款金额不能超过可退余额。

### 请求 `tx_metadata`

`tx_metadata` 为 JSON 字符串，请求侧支持以下子结构：

| 参数 | 定义 | 说明 |
| --- | --- | --- |
| `acct_split_bunch` | Object | 分账信息 |
| `combinedpay_data` | Array | 补贴支付信息 |
| `terminal_device_data` | Object | 设备信息 |

`acct_split_bunch` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `acct_infos` | Array | 2048 | N | 分账信息列表 |

`acct_infos` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `div_amt` | String | 14 | Y | 分账金额，单位元，两位小数 |
| `huifu_id` | String | 32 | Y | 分账接收方 ID |

`combinedpay_data` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `huifu_id` | String | 32 | Y | 汇付商户号 |
| `user_type` | String | 32 | Y | `channel`、`merchant`、`agent`、`mertomer` |
| `acct_id` | String | 32 | Y | 补贴方账户号 |
| `amount` | String | 14 | Y | 补贴金额，单位元 |

`terminal_device_data` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `device_type` | String | 2 | N | `1` 手机，`2` 平板，`3` 手表，`4` PC |
| `device_ip` | String | 64 | N | 交易设备公网 IP |
| `device_mac` | String | 64 | N | 交易设备 MAC |
| `device_imei` | String | 64 | N | 设备 IMEI |
| `device_imsi` | String | 64 | N | 设备 IMSI |
| `device_icc_id` | String | 64 | N | 设备 ICCID |
| `device_wifi_mac` | String | 64 | N | 设备 WIFI MAC |
| `device_gps` | String | 64 | N | 设备 GPS |

## 同步返回参数

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | String | 8 | Y | 业务响应码，见[业务返回码](#业务返回码) |
| `resp_desc` | String | 512 | Y | 业务响应信息 |
| `product_id` | String | 32 | Y | 产品号，原样返回 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `org_hf_seq_id` | String | 128 | N | 原交易全局流水号 |
| `org_req_date` | String | 8 | N | 原交易请求日期 |
| `org_req_seq_id` | String | 128 | N | 原交易请求流水号 |
| `trans_date` | String | 8 | N | 退款交易发生日期，`yyyyMMdd` |
| `trans_time` | String | 6 | N | 退款交易发生时间，`HHMMSS` |
| `trans_finish_time` | String | 14 | N | 退款完成时间，`yyyyMMddHHmmss` |
| `trans_stat` | String | 1 | N | 退款状态，`P` 处理中，`S` 成功，`F` 失败 |
| `ord_amt` | String | 14 | Y | 退款金额，单位元 |
| `actual_ref_amt` | String | 14 | N | 实际退款金额，单位元 |
| `remark` | String | 84 | N | 备注 |
| `bank_message` | String | 256 | N | 通道返回描述 |
| `fund_freeze_stat` | String | 16 | N | 资金冻结状态，`FREEZE` 或 `UNFREEZE` |
| `pay_channel` | String | 1 | N | `A` 支付宝，`T` 微信，`U` 银联二维码，`D` 数字货币 |
| `fee_amount` | String | 14 | N | 退款返还手续费，单位元 |
| `trade_type` | String | - | N | 固定为 `TRANS_REFUND` |
| `tx_metadata` | String | - | N | 扩展参数集合，JSON 字符串 |

### 同步返回 `tx_metadata`

官方同步返回表写的是 `tx_metadata`，其子结构包括：

| 参数 | 定义 | 说明 |
| --- | --- | --- |
| `acct_split_bunch` | Object | 分账信息 |
| `combinedpay_data` | Array | 补贴支付信息 |

`acct_split_bunch` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `acct_infos` | Array | 2048 | N | 分账明细 |
| `fee_amount` | String | 14 | N | 退款返还手续费 |

`acct_infos` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `div_amt` | String | 14 | Y | 分账金额，单位元 |
| `huifu_id` | String | 32 | Y | 分账接收方 ID |

`combinedpay_data` 字段：

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `huifu_id` | String | 32 | Y | 补贴方汇付编号 |
| `user_type` | String | 32 | Y | `channel`、`branch`、`agent` |
| `acct_id` | String | 32 | Y | 补贴方账户号 |
| `amount` | String | 14 | Y | 补贴金额，单位元 |

## 异步返回参数

退款异步通知存在间联模式与直联模式两种形态。若商户开通时做了微信直连配置 `wx_zl_conf`，则属于直联模式。

| 参数 | 定义 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `resp_code` | String | 8 | Y | 业务响应码 |
| `resp_desc` | String | 512 | Y | 业务响应信息 |
| `huifu_id` | String | 32 | Y | 商户号 |
| `req_date` | String | 8 | Y | 请求日期 |
| `req_seq_id` | String | 128 | Y | 请求流水号 |
| `hf_seq_id` | String | 128 | N | 全局流水号 |
| `org_req_date` | String | 8 | N | 原交易请求日期 |
| `org_req_seq_id` | String | 128 | N | 原交易请求流水号 |
| `org_ord_amt` | String | 14 | Y | 原交易订单金额，单位元 |
| `org_fee_amt` | String | 14 | Y | 原交易手续费，单位元 |
| `trans_date` | String | 8 | Y | 退款交易发生日期 |
| `trans_time` | String | 6 | N | 退款交易发生时间 |
| `trans_finish_time` | String | 14 | N | 退款完成时间 |
| `trans_type` | String | 40 | Y | 固定为 `TRANS_REFUND` |
| `trans_stat` | String | 1 | N | 退款状态，`P`、`S`、`F` |
| `ord_amt` | String | 14 | Y | 退款金额，单位元 |
| `actual_ref_amt` | String | 14 | N | 实际退款金额，单位元 |
| `total_ref_amt` | String | 14 | Y | 原交易累计退款金额，单位元 |
| `total_ref_fee_amt` | String | 14 | Y | 原交易累计退款手续费金额，单位元 |
| `ref_cut` | String | 14 | Y | 累计退款次数 |
| `acct_split_bunch` | Object | 4000 | Y | 分账信息 |
| `party_order_id` | String | 64 | N | 微信支付宝商户单号 |
| `wx_response` | Object | 6000 | N | 微信响应报文 |
| `dc_response` | Object | 2048 | N | 数字人民币响应报文 |
| `combinedpay_data` | Array | - | N | 补贴支付信息 |
| `combinedpay_data_fee_info` | String | - | N | 补贴支付手续费承担方信息 |
| `remark` | String | 1500 | N | 备注 |
| `bank_message` | String | 256 | N | 通道返回描述 |
| `unionpay_response` | Object | 6000 | N | 银联响应报文 |
| `fund_freeze_stat` | String | 16 | N | 资金冻结状态 |
| `trans_fee_ref_allowance_info` | Object | - | N | 手续费补贴返还信息 |
| `pay_channel` | String | 1 | N | `A`、`T`、`U`、`D` |
| `is_refund_fee_flag` | String | 1 | N | 是否退还手续费，`Y` 或空为退费，`N` 为不退费 |

### 异步扩展对象

`acct_split_bunch`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `acct_infos` | Array | N | 分账明细 |
| `fee_amt` | String | Y | 退款返还手续费 |

`acct_infos`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `div_amt` | String | Y | 分账金额 |
| `huifu_id` | String | Y | 分账接收方 ID |

`wx_response`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `sub_appid` | String | N | 子商户公众账号 ID |
| `sub_mch_id` | String | N | 子商户号 |
| `org_out_trans_id` | String | N | 微信订单号 |
| `out_trans_id` | String | N | 微信退款单号 |
| `cash_fee` | String | N | 现金支付金额 |
| `cash_refund_fee` | String | N | 现金退款金额 |
| `coupon_refund_fee` | String | N | 代金券退款总金额 |
| `coupon_refund_count` | Integer | N | 退款代金券使用数量 |
| `refund_coupon_info` | Array | N | 退款代金券信息 |
| `promotion_detail` | Array | N | 优惠详情 |
| `user_received_account` | String | N | 退款入账账户 |

`refund_coupon_info`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `coupon_type` | String | N | `CASH` 或 `NO_CASH` |
| `coupon_refund_id` | String | N | 退款代金券 ID |
| `coupon_refund_fee` | String | N | 单个退款代金券支付金额 |

`promotion_detail`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `promotion_id` | String | Y | 券 ID |
| `scope` | String | N | `GLOBAL` 或 `SINGLE` |
| `type` | String | N | `COUPON` 或 `DISCOUNT` |
| `refund_amount` | String | N | 代金券退款金额 |
| `amount` | String | N | 代金券面额 |
| `goods_detail` | Array | N | 商品列表 |

`goods_detail`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `goods_id` | String | Y | 商品编码 |
| `wxpay_goods_id` | String | N | 微信支付商品编码 |
| `goods_name` | String | N | 商品名称 |
| `refund_amt` | String | Y | 商品退款金额 |
| `refund_quantity` | Integer | Y | 商品退款数量 |
| `price` | String | Y | 商品单价 |

`dc_response`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `merchant_id` | String | N | 商户号 |
| `sub_merchant_id` | String | N | 子商户号 |
| `openid` | String | N | 用户标识 |
| `sub_openid` | String | N | 用户子标识 |
| `custom_bank_code` | String | N | 客户所属运营机构代码 |
| `custom_bank_name` | String | N | 客户所属运营机构名称 |
| `coupon_refund_count` | String | N | 退款代金券使用数量 |
| `coupon_refund_list` | Array | N | 退款代金券集合 |
| `refund_recv_wallet_id` | String | N | 退款入账钱包 ID |

`coupon_refund_list`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | String | N | 退款代金券 ID |
| `type` | String | N | 退款代金券类型 |
| `amount` | String | N | 单个退款代金券支付金额 |

`combinedpay_data` 与 `combinedpay_data_fee_info`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `huifu_id` | String | Y/N | 补贴方或手续费承担方汇付编号 |
| `user_type` | String | Y | `channel`、`branch`、`agent` |
| `acct_id` | String | Y/N | 账户号 |
| `amount` | String | Y | 补贴金额 |
| `combinedpay_fee_amt` | String | N | 补贴支付手续费金额 |

`unionpay_response`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `coupon_info` | String | N | 银联优惠信息，JSON 数组字符串 |

`coupon_info`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `addnInfo` | String | N | 附加信息 |
| `spnsrId` | String | Y | 出资方 |
| `type` | String | Y | `DD01`、`CP01`、`CP02` |
| `offstAmt` | String | Y | 抵消交易金额 |
| `id` | String | N | 项目编号 |
| `desc` | String | N | 项目简称 |

`trans_fee_ref_allowance_info`：

| 参数 | 定义 | 必填 | 说明 |
| --- | --- | --- | --- |
| `receivable_ref_fee_amt` | String | Y | 退款返还总手续费 |
| `actual_ref_fee_amt` | String | Y | 退款返还商户手续费 |
| `allowance_ref_fee_amt` | String | Y | 退款返还补贴手续费 |

## 请求示例

```json
{
  "sys_id": "6666000103334211",
  "product_id": "MYPAY",
  "data": {
    "req_seq_id": "1668073286240333",
    "req_date": "20250901",
    "huifu_id": "6666000103334211",
    "ord_amt": "0.01",
    "org_req_date": "20250901",
    "org_hf_seq_id": "0029000topA250901150535P324c0a8408000000",
    "remark": "退款"
  },
  "sign": "Ghc8FKQLPqWFMpHnHV8ZVqNzCvM+/xV7WL8G+V/KtY/PsZtu2+2EABcr2SH1yRSekeTKEJffemRjXmuqTgZwsXnse9JduNRtj9Z/1t1H07V4YzpuWw8NVVT7M9q6yGB1Q+GAsW2KxEvwuuUnY1BsmMOmzrx+YH/jZ74dSsmYCdZS/SolHcqsgqbqrNUHR/q1Z6j+UmH+s+2A7WS6TvCPoZEY3XVv8uLysm1U2J/1l/4CSsKgW2PlWIBFqhRJikymUw7No+8Yz89DATcLj/9k5sCv7JzVu0G87/bvw=="
}
```

## 同步返回示例

```json
{
  "data": {
    "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000103334211\"}],\"fee_amount\":\"0.00\"}",
    "bank_message": "",
    "fee_amount": "0.00",
    "fund_freeze_stat": "FREEZE",
    "huifu_id": "6666000103334211",
    "product_id": "MYPAY",
    "ord_amt": "0.01",
    "org_hf_seq_id": "0029000topA250901150535P324c0a8408000000",
    "org_req_date": "20250901",
    "org_req_seq_id": "20250901test900001tt11zzaazz11",
    "pay_channel": "T",
    "remark": "退款",
    "resp_code": "00000100",
    "resp_desc": "交易处理中",
    "trade_type": "TRANS_REFUND",
    "trans_date": "20250901",
    "trans_stat": "P",
    "trans_time": "153948"
  }
}
```

## 业务返回码

| 返回码 | 返回描述 |
| --- | --- |
| `00000000` | 交易成功 |
| `00000100` | 交易处理中 |
| `10000000` | 入参数据不符合接口要求 |
| `20000001` | 并发冲突，请稍后重试 |
| `21000000` | 原交易请求流水号、原交易微信支付宝商户单号、原交易全局流水号不能同时为空 |
| `21000000` | 数字货币交易退款原因必填 |
| `22000000` | 产品号不存在 |
| `22000000` | 产品号状态异常 |
| `22000002` | 商户信息不存在 |
| `22000002` | 商户状态异常 |
| `22000003` | 账户信息不存在 |
| `22000004` | 暂未开通退款权限 |
| `22000004` | 暂未开通分账退款权限 |
| `22000005` | 结算配置信息不存在 |
| `23000000` | 原交易未入账，不能发起退款 |
| `23000001` | 原交易不存在 |
| `23000002` | 退款手续费承担方和原交易手续费承担方不一致 |
| `23000003` | 申请退款金额大于可退余额 / 退款金额大于待确认金额 / 手续费退款金额大于可退手续费金额 / 申请退款金额大于可退款余额 / 退款分账金额总和必须等于退款订单金额 / 账户余额不足 |
| `23000004` | 不支持预授权撤销类交易 / 不支持刷卡撤销类交易 / 优惠交易不支持部分退款 / 该交易为部分退款需传入分账串 / 优惠退款不支持传入分账串 / 分账串信息与原交易不匹配 |
| `90000000` | 业务执行失败，可用余额不足 / 交易存在风险 |
| `98888888` | 系统错误 |
| `99999999` | 系统异常，请稍后重试 |

## 实现备注与文档勘误

1. 官方“应用场景”里把银联二维码 JS 写成了 `U_JSAP`，按上下文应理解为 `U_JSAPI`。
2. 官方同步返回参数表写的是 `tx_metadata`，但返回示例却把 `acct_split_bunch` 直接放在顶层；实现时应兼容这类字段展开差异。
3. 官方异步返回表中的 `combinedpay_data_fee_info` 标为 `String/jsonObject字符串`，而其他扩展对象多以对象形式出现；落库前建议统一做 JSON 解析。
4. 当前 SDK 文档中 `remark`、`notify_url`、`tx_metadata` 没有独立 setter，接入时应通过 `client.optional()` 或 `request.optional()` 传入。
5. `resp_code=00000000` 或 `00000100` 只代表退款请求受理状态，退款最终结果仍应以异步通知或退款查询接口为准。
