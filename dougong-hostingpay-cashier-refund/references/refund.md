## 目录

- [接口概述](#接口概述)
- [应用场景](#应用场景)
- [SDK 映射](#sdk-映射)
- [公共请求参数](#公共请求参数)
- [请求参数 data](#请求参数-data)
- [嵌套参数展开](#嵌套参数展开)
- [请求示例](#请求示例)
- [同步返回参数](#同步返回参数)
- [异步返回参数](#异步返回参数)
- [业务返回码](#业务返回码)
- [文档勘误与实现备注](#文档勘误与实现备注)

# 托管交易退款

> 本文依据 2026-03-23 官方文档整理，适用于 `v2/trade/hosting/payment/htRefund`。

## 接口概述

| 属性 | 值 |
|------|-----|
| 请求方式 | `POST` |
| 汇付 API 端点 | `https://api.huifu.com/v2/trade/hosting/payment/htRefund` |
| SDK Request 类 | `V2TradeHostingPaymentHtrefundRequest` |
| Content-Type | `application/json` |

说明：

- 支持 JSON 报文。
- 请求整体需要签名，验签规则见 `dougong-hostingpay-pay-base/references/tech-spec.md`。
- 退款结果存在异步通知，最终状态不能只看同步返回。
- 文档中的 `String(JSON Object)` / `String(JSON Array)` 表示字段外层类型仍是 `String`，但值内容需要传 JSON 字符串。

## 应用场景

- 通过托管支付预下单接口发起的交易，可以通过本接口发起退款。
- 适用于全额退款、部分退款、分账退款、线上交易退款，以及带抖音扩展参数的大促或平台退款场景。

## SDK 映射

`V2TradeHostingPaymentHtrefundRequest` 的独立 setter 字段：

| 字段 | setter | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| reqDate | `setReqDate()` | String(8) | Y | 本次退款请求日期，`yyyyMMdd` |
| reqSeqId | `setReqSeqId()` | String(128) | Y | 本次退款请求流水号，同一 `huifu_id` 下当天唯一 |
| huifuId | `setHuifuId()` | String(32) | Y | 商户号 |
| ordAmt | `setOrdAmt()` | String(14) | Y | 申请退款金额，单位元 |
| orgReqDate | `setOrgReqDate()` | String(8) | Y | 原交易请求日期，`yyyyMMdd` |
| riskCheckData | `setRiskCheckData()` | String(2048) | C | 线上交易退款必填，JSON 字符串 |
| terminalDeviceData | `setTerminalDeviceData()` | String(2048) | C | 线上交易退款必填，JSON 字符串 |
| bankInfoData | `setBankInfoData()` | String(1024) | C | 银行大额转账支付交易退款申请时必填，JSON 字符串 |

说明：

- 在本 skill 库的 Java SDK 接入实践中，`org_req_seq_id` 没有独立 setter，应通过 `setExtendInfo(Map<String, Object>)` 传入。
- `org_hf_seq_id`、`org_party_order_id`、`acct_split_bunch`、`remark`、`loan_flag`、`loan_undertaker`、`loan_acct_type`、`notify_url`、`dy_data` 也按扩展字段处理更稳妥。
- 拆单支付退款场景下，原交易定位字段只支持 `org_hf_seq_id` 或 `org_party_order_id`，不使用 `org_req_seq_id`。

## 公共请求参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| sys_id | 系统号 | String | 32 | Y | 渠道商/商户的 `huifu_id`；渠道商主体传渠道商号，直连商户主体传商户号 |
| product_id | 产品号 | String | 32 | Y | 汇付分配的产品号 |
| sign | 加签结果 | String | 512 | Y | 对整个请求报文签名 |
| data | 请求数据 | JSON | - | Y | 业务请求参数 |

## 请求参数 data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| req_date | 请求日期 | String | 8 | Y | `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 128 | Y | 同一 `huifu_id` 下当天唯一 |
| huifu_id | 商户号 | String | 32 | Y | 开户后自动生成 |
| ord_amt | 申请退款金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01`；原交易为延时交易时，退款金额必须小于等于待确认金额 |
| org_req_date | 原交易请求日期 | String | 8 | Y | `yyyyMMdd` |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | `org_hf_seq_id`、`org_party_order_id`、`org_req_seq_id` 三选一；拆单支付场景下与 `org_party_order_id` 二选一 |
| org_party_order_id | 原交易微信支付宝的商户单号 | String | 64 | N | `org_hf_seq_id`、`org_party_order_id`、`org_req_seq_id` 三选一；拆单支付场景下与 `org_hf_seq_id` 二选一 |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | `org_hf_seq_id`、`org_party_order_id`、`org_req_seq_id` 三选一；拆单支付场景下不作为定位字段 |
| acct_split_bunch | 分账对象 | String(JSON Object) | 2048 | N | 分账信息 |
| remark | 备注 | String | 84 | N | 原样返回 |
| loan_flag | 是否垫资退款 | String | 2 | N | `Y`=垫资出款，`N`=普通出款，默认 `N`；延时交易退款需在“交易确认退款”接口设置垫资，本接口不可再次设置 |
| loan_undertaker | 垫资承担者 | String | 32 | N | 垫资方的 `huifu_id`；为空则各自承担 |
| loan_acct_type | 垫资账户类型 | String | 2 | N | `01`=基本户，`05`=充值户，默认充值户 |
| risk_check_data | 安全信息 | String(JSON Object) | 2048 | C | 线上交易退款必填 |
| terminal_device_data | 设备信息 | String(JSON Object) | 2048 | C | 线上交易退款必填 |
| notify_url | 异步通知地址 | String | 512 | N | 异步通知地址 |
| bank_info_data | 大额转账支付账户信息数据 | String(JSON Object) | 1024 | C | 银行大额转账支付交易退款申请时必填 |
| dy_data | 抖音拓展参数集合 | String(JSON Object) | 2048 | N | 抖音扩展参数 |

## 嵌套参数展开

### 请求 acct_split_bunch

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_infos | 分账明细 | Array | 2048 | N | 分账明细 |

#### 请求 acct_split_bunch.acct_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| div_amt | 分账金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| huifu_id | 分账接收方 ID | String | 32 | Y | 分账接收方 ID |
| part_loan_amt | 垫资金额 | String | 12 | N | 单位元，保留两位小数；若由第三方全额垫资，则不传该字段 |

### 请求 risk_check_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| ip_addr | ip 地址 | String | 32 | N | IP 地址、经纬度、基站地址最少送一项 |
| base_station | 基站地址 | String | 64 | N | `mcc + mnc + location_cd + lbs_num` |
| latitude | 纬度 | String | 20 | N | `+` 表示北纬，`-` 表示南纬；整数位不超过 2 位，小数位不超过 6 位 |
| longitude | 经度 | String | 20 | N | `+` 表示东经，`-` 表示西经；整数位不超过 3 位，小数位不超过 5 位 |

### 请求 terminal_device_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| device_type | 设备类型 | String | 2 | N | `1`=手机，`2`=平板，`3`=手表，`4`=PC |
| device_ip | 交易设备 IP | String | 64 | N | 交易设备公网 IP；当前暂传 IPv4 格式 |
| device_mac | 交易设备 MAC | String | 64 | N | 交易设备 MAC |
| device_gps | 交易设备 GPS | String | 64 | N | 交易设备 GPS |
| device_imei | 交易设备 IMEI | String | 64 | N | 移动终端设备唯一标识 |
| device_imsi | 交易设备 IMSI | String | 64 | N | 交易设备 IMSI |
| device_icc_id | 交易设备 ICCID | String | 64 | N | 交易设备 ICCID |
| device_wifi_mac | 交易设备 WIFI MAC | String | 64 | N | 交易设备 WIFI MAC |

### 请求 bank_info_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| province | 省份 | String | 4 | C | 付款方为对公账户时必填 |
| area | 地区 | String | 4 | C | 付款方为对公账户时必填 |
| bank_code | 银行编号 | String | 8 | C | 付款方为对公账户时必填 |
| correspondent_code | 联行号 | String | 30 | C | 付款方为对公账户时必填 |
| card_acct_type | 付款方账户类型 | String | 1 | N | `E`=对公，`P`=对私，默认 `P` |

### 请求 dy_data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| refund_desc | 退款原因 | String | 200 | N | 会在下发给用户的退款消息中体现退款原因 |

### 同步返回 acct_split_bunch

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_infos | 分账明细 | Array | 2048 | N | 分账明细 |
| fee_amt | 退款返还手续费 | String | 14 | N | 单位元，保留两位小数 |

#### 同步返回 acct_split_bunch.acct_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| div_amt | 分账金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| huifu_id | 分账接收方 ID | String | 32 | Y | 分账接收方 ID |

### 同步/异步返回 unionpay_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| coupon_info | 银联优惠信息 | String(JSON Array) | - | N | 银联使用优惠活动时出现 |

#### 同步/异步返回 unionpay_response.coupon_info[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| addnInfo | 附加信息 | String | 100 | N | 内容自定义 |
| spnsrId | 出资方 | String | 20 | Y | `00010000`=银联出资；也可能为付款方机构代码或商户代码 |
| type | 项目类型 | String | 4 | Y | `DD01`=随机立减，`CP01`=抵金券 |
| offstAmt | 抵消交易金额 | String | 14 | Y | 不能为全 `0`，单位元 |
| id | 项目编号 | String | 40 | N | 用于票券编号等 |
| desc | 项目简称 | String | 40 | N | 优惠活动简称 |

### 同步/异步返回 dy_response

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| org_out_trans_id | 抖音原交易订单号 | String | 32 | N | 抖音原交易订单号 |
| out_trans_id | 抖音退款单号 | String | 32 | N | 抖音退款单号 |
| payer_refund | 用户退款金额 | String | 12 | N | 退款给用户的金额，不含所有优惠券金额，单位元 |

### 异步返回 acct_split_bunch

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| acct_infos | 分账明细 | Array | 2048 | N | 分账明细 |
| fee_amt | 退款返还手续费 | String | 14 | N | 单位元，保留两位小数 |

#### 异步返回 acct_split_bunch.acct_infos[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| div_amt | 分账金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| huifu_id | 分账接收方 ID | String | 32 | Y | 分账接收方 ID |

### 异步返回 split_fee_info

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| split_fee_flag | 分账手续费扣款标志 | String | 1 | Y | `1`=外扣，`2`=内扣 |
| total_split_fee_amt | 总分账手续费金额 | String | 14 | Y | 单位元，保留两位小数 |
| split_fee_details | 分账手续费明细 | Array | 2048 | Y | 分账手续费明细 |

#### split_fee_info.split_fee_details[]

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| split_fee_amt | 分账手续费金额 | String | 14 | Y | 单位元，保留两位小数 |
| split_fee_huifu_id | 分账手续费承担方商户号 | String | 32 | Y | 分账手续费承担方商户号 |
| split_fee_acct_id | 分账手续费承担方账号 | String | 9 | N | 分账手续费承担方账号 |

## 请求示例

```json
{
  "sys_id": "6666000123123123",
  "product_id": "MYPAY",
  "data": {
    "huifu_id": "6666000003100616",
    "req_date": "20240229",
    "req_seq_id": "52022070919803411999411514",
    "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.12\",\"huifu_id\":\"6666000003100616\"}]}",
    "ord_amt": "0.01",
    "org_hf_seq_id": "",
    "org_party_order_id": "",
    "org_req_seq_id": "202207099803123123199941",
    "org_req_date": "20240229",
    "risk_check_data": "{\"risk_mng_info\":{\"sub_trade_type\":\"4300\"},\"ip_address\":\"127.0.0.1\"}",
    "terminal_device_data": "{\"device_type\":\"4\"}",
    "notify_url": "http://www.baidu.com"
  },
  "sign": "dJCZn/tVUuzKh13ACOAcCSl/E6OvR018DXX1FZjqXVjQ5qpezzsEK7CJZRo91QFioC4EF/kI1ju04wlCBrRus7+/axbIXJlCAsNBR4Ixwz6N0gc1V8U0zB3jsDfOXYZleJKhcju3M+bJJ/5ne+LbvKhP8L0R3Fpc4+P7PH5Vf2Of7DDwyWApqstr75IppK/h8JedI8yt1lfQD5d2AEg5n8aGAmGMyy9V17UfcH153BSqP8gsJACKlkfEep2hQnR+2MG+wwvkfZReQKcpR3NgMAlGpcxyFRUF3X1nor/Cz5N9rxZW2IjNHmVZ9EMcIJKdby55RLkBf3b2kYZrCaHCTQ=="
}
```

## 同步返回参数

### 公共返回参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| sign | 签名 | String | 512 | Y | 对响应整体签名 |
| data | 响应内容体 | JSON | - | N | 业务返回参数 |

### data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| resp_code | 业务响应码 | String | 8 | Y | `00000000` 表示退款请求已受理 |
| resp_desc | 业务响应信息 | String | 512 | Y | 业务返回描述 |
| product_id | 产品号 | String | 32 | Y | 交易时传入，原样返回 |
| huifu_id | 商户号 | String | 32 | Y | 商户号 |
| req_date | 请求日期 | String | 8 | Y | `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 128 | Y | 原样返回 |
| hf_seq_id | 全局流水号 | String | 128 | N | 扫码交易返回 |
| org_req_date | 原交易请求日期 | String | 8 | N | `yyyyMMdd` |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | 原交易请求流水号 |
| org_hf_seq_id | 原交易全局流水号 | String | 128 | N | 线上交易返回 |
| trans_time | 退款交易发生时间 | String | 14 | N | 扫码交易返回 |
| trans_stat | 交易状态 | String | 1 | N | `P`=处理中，`S`=成功，`F`=失败 |
| ord_amt | 退款金额 | String | 14 | Y | 单位元，保留两位小数 |
| actual_ref_amt | 实际退款金额 | String | 14 | N | 扫码交易返回 |
| acct_split_bunch | 分账信息 | String(JSON Object) | 2048 | N | 见上文“同步返回 acct_split_bunch” |
| unionpay_response | 银联返回的响应报文 | String(JSON Object) | 6000 | N | 扫码交易返回 |
| dy_response | 抖音返回的响应报文 | String(JSON Object) | 6000 | N | 抖音响应报文 |
| remark | 备注 | String | 84 | N | 原样返回 |
| bank_code | 通道返回码 | String | 64 | N | 通道返回码 |
| bank_message | 通道返回描述 | String | 256 | N | 通道返回描述 |
| fee_amt | 手续费金额 | String | 14 | N | 线上交易返回 |

### 同步成功示例

```json
{
  "data": {
    "acct_split_bunch": "{\"acct_infos\":[{\"div_amt\":\"0.12\",\"huifu_id\":\"6666000003100616\"}]}",
    "actual_ref_amt": "",
    "bank_code": "00000000",
    "bank_message": "成功",
    "hf_seq_id": "0056default240305162924Pa41a9ac1984fd843",
    "huifu_id": "6666000003100616",
    "mer_name": "顺顺利利的简称tes",
    "ord_amt": "0.01",
    "org_hf_seq_id": "0056default240305161117P559c0a8209b00000",
    "org_req_date": "20240229",
    "org_req_seq_id": "202207099803123123199941",
    "req_date": "20240229",
    "req_seq_id": "52022070919803411999411514",
    "trans_stat": "S",
    "trans_time": "20240305162924"
  }
}
```

## 异步返回参数

> 退款结果通过异步通知返回；异步回调体为 `data`。

### data

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| resp_code | 业务响应码 | String | 8 | Y | 业务响应码 |
| resp_desc | 业务响应信息 | String | 512 | Y | 业务返回描述 |
| huifu_id | 商户号 | String | 32 | Y | 商户号 |
| mer_name | 商户名称 | String | 128 | Y | 线上交易返回 |
| req_date | 请求日期 | String | 8 | Y | `yyyyMMdd` |
| req_seq_id | 请求流水号 | String | 128 | Y | 退款请求流水号 |
| hf_seq_id | 全局流水号 | String | 128 | N | 退款全局流水号 |
| org_req_date | 原交易请求日期 | String | 8 | N | `yyyyMMdd` |
| org_req_seq_id | 原交易请求流水号 | String | 128 | N | 原交易请求流水号 |
| org_ord_amt | 原交易订单金额 | String | 14 | Y | 单位元，保留两位小数 |
| org_fee_amt | 原交易手续费 | String | 14 | Y | 单位元，保留两位小数 |
| trans_date | 退款交易发生日期 | String | 8 | Y | `yyyyMMdd` |
| trans_time | 退款交易发生时间 | String | 6 | N | `HHMMSS` |
| trans_finish_time | 退款完成时间 | String | 14 | N | `yyyyMMddHHmmss` |
| trans_type | 交易类型 | String | 40 | Y | 当前仅 `TRANS_REFUND` |
| trans_stat | 交易状态 | String | 1 | N | `P`=处理中，`S`=成功，`F`=失败 |
| ord_amt | 退款金额 | String | 14 | Y | 单位元，保留两位小数 |
| actual_ref_amt | 实际退款金额 | String | 14 | N | 扫码交易返回 |
| total_ref_amt | 原交易累计退款金额 | String | 14 | Y | 单位元，保留两位小数 |
| total_ref_fee_amt | 原交易累计退款手续费金额 | String | 14 | Y | 单位元 |
| ref_cut | 累计退款次数 | String | 14 | Y | 累计退款次数 |
| acct_split_bunch | 分账信息 | String(JSON Object) | 4000 | Y | 见上文“异步返回 acct_split_bunch” |
| split_fee_info | 分账手续费信息 | String(JSON Object) | 2048 | N | 线上交易返回 |
| party_order_id | 微信支付宝的商户单号 | String | 64 | N | 用户账单商户单号 |
| fee_amt | 退款返还手续费 | String | 14 | N | 线上交易返回 |
| remark | 备注 | String | 84 | N | 原样返回 |
| bank_code | 通道返回码 | String | 64 | N | 通道返回码 |
| bank_message | 通道返回描述 | String | 256 | N | 通道返回描述 |
| unionpay_response | 银联返回的响应报文 | String(JSON Object) | 6000 | N | 银联响应报文 |
| dy_response | 抖音返回的响应报文 | String(JSON Object) | 6000 | N | 抖音响应报文 |
| bank_id | 银行编号 | String | 32 | N | 线上交易返回 |
| bank_name | 银行名称 | String | 128 | N | 线上交易返回 |

## 业务返回码

| 返回码 | 返回描述 | 处理 |
|--------|----------|------|
| 00000000 | 退款请求受理成功 | 同步返回仅表示已受理，最终结果以异步 `trans_stat` 或退款查询结果为准 |
| 其他 | 参见官方业务返回码页面 | 结合 `resp_desc`、`bank_code`、`bank_message` 排查 |

## 文档勘误与实现备注

- 请求示例中的 `risk_check_data` 使用了 `risk_mng_info` 和 `ip_address`，但参数表只定义了 `ip_addr`、`base_station`、`latitude`、`longitude`；当前按官方参数表保留字段定义，并显式记录示例冲突。
- 公共返回参数表声明同步响应顶层 `sign` 必返，但官方成功示例只展示了 `data`，没有 `sign`。
- 同步返回参数表没有 `mer_name`，但官方成功示例中出现了 `mer_name`；当前将其视为示例可见字段，而非稳定同步返回字段。
- 同步返回参数表将 `resp_code`、`resp_desc`、`product_id` 标记为必返，但官方成功示例中未展示这几个字段；实现时应以字段表为准，不要仅依赖示例。
- 同名字段 `trans_time` 在同步返回中表现为 14 位时间串示例，在异步返回中又定义为 6 位 `HHMMSS`；消费方不要复用同一解析规则。
- `unionpay_response.coupon_info` 在父表中写为 `String`，说明里又标注为 `jsonArray`；当前按“字符串承载 JSON 数组”理解。
- 本 skill 库的退款 reference/FAQ 明确 `org_req_seq_id` 无独立 setter，应通过 `setExtendInfo(Map)` 传入；这是 SDK 接入层约束，不是官方接口字段约束。
