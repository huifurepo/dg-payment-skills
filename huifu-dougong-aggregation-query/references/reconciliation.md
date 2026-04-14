## 目录

- [接口概述](#接口概述)
- [请求参数](#请求参数)
- [返回参数](#返回参数)
- [SDK 调用示例](#sdk-调用示例)
- [对账文件说明](#对账文件说明)
- [请求 JSON 示例](#请求-json-示例)
- [返回 JSON 示例](#返回-json-示例)
- [注意事项](#注意事项)

# 交易结算对账单查询

## 接口概述

| 属性 | 值 |
|-----|-----|
| 汇付 API 端点 | `v2/trade/check/filequery` |
| 请求方式 | POST |
| 建议业务接口 | `POST /api/pay/reconciliation` |

> **注意**：对账单查询接口使用 dg-java-sdk 的方式调用（非 Lightning SDK），因为 Lightning SDK 未封装此接口。如果项目中只引入了 dg-lightning-sdk，需要手动构造 HTTP 请求。

## 请求参数

data

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| req_date | String(8) | Y | 请求日期 yyyyMMdd |
| req_seq_id | String(128) | Y | 请求流水号 |
| huifu_id | String(18) | Y | 渠道/商户 ID |
| file_date | String(8) | Y | 文件生成日期 yyyyMMdd（交易日期+1天，字段名固定为 `file_date`） |
| bill_type | String(128) | N | 文件类型（字段名固定为 `bill_type`，见下表） |

### 字段命名约束

- 请求字段名固定为 `file_date`。
- “文件生成日期”只是中文释义，不是建议把字段改成 `bill_date`、`generate_date`。
- 如果生成对外请求 DTO、Controller 参数或接口文档，应直接保留 `file_date`。
- 请求字段名固定为 `bill_type`。
- “文件类型”只是中文释义，不是建议把字段改成 `file_type`。
- 如果生成对外请求 DTO、Controller 参数或接口文档，应直接保留 `bill_type`。
- 除非用户已有存量接口必须兼容，否则不要通过 `file_type` 入参再映射回 `bill_type`。

### bill_type 文件类型

| 值 | 说明 |
|---|------|
| TRADE_BILL | 交易对账单 |
| SPLIT_BILL | 分账对账单 |
| WITHDRAWAL_BILL | 出金对账单 |
| SETTLE_BILL | 结算对账单 |
| TRADE_BILL_MONTH | 月交易对账单 |
| SETTLE_BILL_MONTH | 月结算对账单 |
| SETTLE_USER_BILL | 用户结算对账单 |
| SETTLE_BILL_USER_MONTH | 用户月结算对账单 |
| SETTLE_FUND_BILL | 结算资金对账单 |

## 返回参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| resp_code | String(8) | Y | 业务返回码 |
| resp_desc | String(512) | Y | 业务返回描述 |
| req_date | String(8) | Y | 请求日期 |
| req_seq_id | String(128) | Y | 请求流水号 |
| file_details | Array | N | 文件信息（文件生成后有值） |
| task_details | Array | N | 文件生成任务信息 |

### file_details 数组元素

| 参数 | 说明 |
|------|------|
| download_url | 平台返回的文件地址字段 |
| file_date | 文件日期 |
| file_id | 文件 ID |
| file_Name | 文件名 |
| huifu_id | 商户号 |
| bill_type | 文件类型 |

### task_details 数组元素

| 参数 | 说明 |
|------|------|
| data_date | 数据日期 |
| download_url | 返回地址字段 |
| file_id | 文件 ID |
| file_name | 文件名 |
| bill_type | 文件类型 |
| huifu_id | 商户号 |
| task_start_time | 任务开始时间 |
| task_end_time | 任务结束时间 |
| task_stat | 任务状态：S=成功 |

## SDK 调用示例

由于 Lightning SDK 未直接封装对账单查询，以下提供两种调用方式：

### 方式 1：使用 dg-java-sdk（推荐，如果项目已引入）

```java
// 需要 dg-java-sdk 依赖
// 按照 huifu-dougong-hostingpay-base 的方式初始化后调用
// 具体 Request 类参见 dg-java-sdk 文档
```

### 方式 2：手动构造 HTTP 请求

```java
import com.huifu.dg.lightning.utils.RsaUtils;
import com.huifu.dg.lightning.utils.JsonUtils;
import com.huifu.dg.lightning.utils.HttpClientUtils;

// 1. 构建 data
JSONObject data = new JSONObject();
data.put("req_date", "20250321");
data.put("req_seq_id", "20250321100000recon001");
data.put("huifu_id", "6666000123123123");
data.put("file_date", "20250320");
data.put("bill_type", "TRADE_BILL"); // 字段名固定，不要写成 file_type

// 2. 签名
String sortedData = JsonUtils.sort4JsonString(data.toJSONString(), 10);
String sign = RsaUtils.sign(sortedData, rsaPrivateKey);

// 3. 构建完整请求
JSONObject request = new JSONObject();
request.put("sys_id", sysId);
request.put("product_id", productId);
request.put("data", data);
request.put("sign", sign);

// 4. POST 请求
String response = HttpClientUtils.sendPost(
    "https://api.huifu.com/v2/trade/check/filequery",
    request.toJSONString()
);

// 5. 解析响应，下载 file_details 中的 download_url
```

反例与正例：

```java
// ✗ 不推荐：前端/DTO 传 file_type，服务端再翻译成 bill_type
req.setFileType("TRADE_BILL");
data.put("bill_type", req.getFileType());

// ✓ 推荐：请求模型直接使用 bill_type
req.setBillType("TRADE_BILL");
data.put("bill_type", req.getBillType());
```

## 对账文件说明

### 生成时间

| 文件类型 | 跑批时间 | 建议取文件时间 |
|---------|---------|-------------|
| 交易数据/分账 | 每日 3:00 | 产品介绍最新口径建议 12:00 后 |
| 出金对账单 | 每日 10:30 | 11:30 后 |
| 结算对账单 | 每日 17:00 | 18:00 后 |

### 文件格式

- 接口支持 1 年内账单下载，控台下载暂未见时间限制说明
- 常规账单下载链接通常对应压缩文件，压缩包内多为 csv
- `SETTLE_FUND_BILL` 模板文件为 `.xlsx`，不要把所有账单都按 csv 解析
- 单个文件记录数超过 400,000 条时，会拆分为多个 csv

### 文件名规则

| 类型 | 文件名格式 |
|------|----------|
| 交易数据 | 年月日_商户号_order_批次号.csv |
| 结算对账单 | 年月日_商户号_settle_批次号.csv |
| 出金对账单 | 年月日_商户号_outcash_批次号.csv |
| 分账对账单 | 年月日_商户号_split_批次号.csv |
| 用户结算 | 年月日_商户号_settleuser_批次号.csv |
| 结算资金 | 年月日_商户号_settlefund.xlsx |

## 请求 JSON 示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "sign": "RSA签名",
    "data": {
        "file_date": "20240428",
        "bill_type": "TRADE_BILL",
        "req_seq_id": "20240506094347392bzgooscof4vgn0",
        "req_date": "20240506",
        "huifu_id": "6666000109133323"
    }
}
```

## 返回 JSON 示例

```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "查询成功",
        "file_details": [
            {
                "download_url": "<PLATFORM_RETURNED_DOWNLOAD_URL>",
                "file_date": "20230803",
                "file_id": "f577ea48-033b-3f08-8ae5-994ec0996053",
                "file_Name": "20230803_6666000111546360_order.zip",
                "huifu_id": "6666000111546360",
                "bill_type": "TRADE_BILL"
            }
        ],
        "task_details": [
            {
                "data_date": "20230802",
                "download_url": "<PLATFORM_RETURNED_DOWNLOAD_URL>",
                "file_id": "f577ea48-033b-3f08-8ae5-994ec0996053",
                "file_name": "20230803_6666000111546360_order.zip",
                "bill_type": "TRADE_BILL",
                "huifu_id": "6666000111546360",
                "task_end_time": "20230803183238",
                "task_start_time": "20230803183237",
                "task_stat": "S"
            }
        ]
    }
}
```

## 注意事项

1. `file_date` 填写交易日期 +1 天（即对账单生成日期），字段名固定为 `file_date`
2. 每天查询次数建议**不超过 3 次**
3. 如果 `file_details` 为空，查看 `task_details`：task_stat=S 但无文件表示前一日无记录
4. 下载链接有有效期，需及时下载
5. 交易账单实收金额与结算金额不一致时，计算方式：交易金额 - 手续费 - 退款金额 + 退款手续费
6. 交易/分账文件不要按旧经验在 04:00 左右立即拉取，最新产品介绍口径建议保守到 12:00 后再取
