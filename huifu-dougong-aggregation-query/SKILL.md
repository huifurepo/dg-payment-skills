---
name: huifu-dougong-aggregation-query
display_name: 汇付支付聚合支付查询关单与对账
description: "汇付支付聚合支付查询与关单的斗拱SDK Skill：覆盖聚合交易查询、聚合交易关单、关单查询、对账单查询。参数表和业务规则按协议字段组织，Java SDK 调用方式放在语言适配入口里。当开发者需要查询聚合支付订单状态或关闭未支付的聚合订单时使用。触发词：聚合交易查询、聚合订单查询、聚合关单、聚合交易关闭、对账单。"
version: 1.1.0
author: "jiaxiang.li | 内容版权：上海汇付支付有限公司"
homepage: https://paas.huifu.com/open/home/index.html
license: CC-BY-NC-4.0
compatibility:
  - openclaw
dependencies:
  - huifu-dougong-aggregation-base
metadata:
  openclaw:
    requires:
      config:
        - HUIFU_PRODUCT_ID
        - HUIFU_SYS_ID
        - HUIFU_RSA_PRIVATE_KEY
        - HUIFU_RSA_PUBLIC_KEY
---

> **版权声明**：本 Skill 内容来源于上海汇付支付有限公司官方开放平台文档，版权归属上海汇付支付有限公司。如有疑问可咨询汇付支付客服：400-820-2819 / cs@huifu.com
>
> **Source**: Official Open Platform documentation of Shanghai Huifu Payment Co., Ltd.
>
> **Copyright**: Shanghai Huifu Payment Co., Ltd.

---

# 聚合支付 - 查询、关单与对账

交易查询 + 交易关单 + 关单查询 + 对账单查询。

## 适配版本与复核信息

| 项目 | 内容 |
| --- | --- |
| Skill 版本 | `1.1.0` |
| 当前适配 SDK | `dg-lightning-sdk` `1.0.3` |
| 最后复核日期 | `2026-04-08` |
| 官方文档来源 | 汇付开放平台聚合支付查询/关单/对账接口文档、Java SDK 文档、异步消息说明 |

## 运行依赖与凭据边界

本 Skill 依赖 [huifu-dougong-aggregation-base](../huifu-dougong-aggregation-base/SKILL.md) 提供公共运行时。凭据使用规则与存放边界见 [credential-boundary.md](../huifu-dougong-pay-shared-base/governance/credential-boundary.md)。

> **前置依赖**：首次接入请先阅读 [huifu-dougong-aggregation-base](../huifu-dougong-aggregation-base/SKILL.md) 完成 SDK 初始化。

> **进入本 Skill 前先确认**：上游下单侧已经保存 `req_date`、`req_seq_id`、`hf_seq_id`、`party_order_id` 等查询键；具体来源和客户准备项见 [customer-preparation.md](../huifu-dougong-aggregation-base/references/customer-preparation.md)。

> **官方开发指引补充约束**：微信 / 支付宝 / 银联多个渠道文档都明确要求，用户前端页面收到支付完成回调后，后端仍需调用查询订单 API 确认最终状态。

## 协议规则入口

- [signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- [async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md)

## 语言适配入口

这份 Skill 的查询字段、关单限制和对账字段，都是语言无关的。  
具体语言怎么初始化和发请求，先看这里：

- [huifu-dougong-aggregation-base/SKILL.md](../huifu-dougong-aggregation-base/SKILL.md)
- [server-sdk-matrix.md](../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md)

## 触发词

- "聚合交易查询"、"聚合订单查询"、"聚合订单状态"、"查询聚合支付结果"
- "聚合关单"、"聚合交易关闭"、"关闭聚合订单"
- "聚合关单查询"、"关单状态"
- "对账单"、"对账"、"账单查询"、"结算对账"

## 场景路由

| 用户意图 | 场景 | 详细说明 |
|---------|------|---------|
| 查询订单支付状态 | 聚合交易查询 | 见 [payment-query.md](references/payment-query.md) |
| 关闭未支付订单 | 聚合交易关单 | 见 [trade-close.md](references/trade-close.md) |
| 查询关单结果 | 关单查询 | 见 [close-query.md](references/close-query.md) |
| 查询对账单 | 对账单查询 | 见 [reconciliation.md](references/reconciliation.md) |

## 使用场景说明

### 交易查询

- 用户支付后未收到异步通知，需主动确认支付结果
- 收到异步通知后做二次确认
- 反扫支付返回处理中（用户需输入密码），轮询确认
- 当 `trans_stat=P` 时，建议**间隔 5 秒轮询，最多 30 次**（150 秒）

### 交易关单

- 用户长时间未支付，主动关闭订单释放资源
- 仅支持**微信和支付宝**交易，银联/数字货币不支持
- 原交易已是终态（成功/失败）的，关单会失败
- **不允许关闭一分钟以内的订单**

### 关单查询

- 发起关单请求后未收到结果，查询关单状态

### 对账单查询

- 查询交易/结算/分账/出金/用户结算等对账文件
- 接口支持 1 年内账单下载；控台下载当前口径暂未限制时间范围
- 对账文件按 T+1/D+1 规则生成；最新产品介绍口径建议交易/分账文件 `12:00` 后下载，出金对账单 `10:30` 跑批后一小时，结算对账单 `17:00` 跑批后一小时
- 每天建议不超过 3 次查询
- 请求字段名固定为 `file_date` 和 `bill_type`；不要按中文释义改写成 `bill_date`、`generate_date` 或 `file_type`

## 注意事项

1. 查询需要传入 `huifu_id`，并使用 `out_ord_id`、`hf_seq_id`、`req_seq_id` 三选一作为查询键；`req_date` 为条件必填，建议在按 `req_seq_id` 查询时一并传入
2. 关单需要传入 `req_date`、`req_seq_id`、`huifu_id`、`org_req_date`，并在 `org_hf_seq_id`、`org_req_seq_id` 中二选一定位原交易
3. 关单查询需要传入 `req_date`、`req_seq_id`、`huifu_id`、`org_req_date`，并在 `org_hf_seq_id`、`org_req_seq_id` 中二选一；且只能通过原交易查询关单状态
4. 关单后用户将无法再对该订单进行支付
5. 已支付成功的订单**无法关单**，只能走退款流程
6. 银联二维码交易**不支持关单**
7. 建议收到异步通知后仍调用查询接口做二次确认
8. 常规对账单下载结果通常是压缩文件，压缩包内多为 csv；`SETTLE_FUND_BILL` 模板为 `.xlsx`，不要把所有账单都按 csv 解析
9. 对账单查询请求参数应直接使用 `file_date` 和 `bill_type`，不要额外设计 `bill_date/generate_date -> file_date` 或 `file_type -> bill_type` 映射层

> 快速接入代码示例见 [quickstart.md](references/quickstart.md)。

---

> 版权声明与联系方式见 [copyright-notice.md](../huifu-dougong-pay-shared-base/governance/copyright-notice.md)
