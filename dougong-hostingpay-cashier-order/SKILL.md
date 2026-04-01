---
name: dougong-hostingpay-cashier-order
description: "汇付托管支付（dg-java-sdk）预下单 Skill：覆盖 H5/PC、支付宝小程序、微信小程序三种预下单场景。当开发者需要通过收银台托管方式创建支付订单时使用。触发词：托管预下单、收银台预下单、H5支付、小程序支付、创建托管订单。"
license: MIT
compatibility: "Java 8+, Maven, Spring Boot 2.x/3.x"
source: "https://github.com/niceforbear/huifu-hosting-payment"
dependencies:
  - dougong-hostingpay-pay-base
env:
  - HUIFU_NOTIFY_URL
  - HUIFU_PROJECT_ID
  - HUIFU_PROJECT_TITLE
  - HUIFU_CALLBACK_URL
metadata:
  author: jiaxiang.li
  version: 1.0.0
  bins: java, mvn
---

# 统一收银台 — 预下单

覆盖三种预下单场景：H5/PC、支付宝小程序、微信小程序。

> **前置依赖**：首次接入请先阅读 [dougong-hostingpay-pay-base](../dougong-hostingpay-pay-base/SKILL.md) 完成 SDK 初始化。

> **开发前先补两步**：先核对 [客户前置准备清单](../dougong-hostingpay-pay-base/references/customer-preparation.md)，再按 [参数校验与 JSON 构造规范](../dougong-hostingpay-pay-base/references/payload-construction.md) 建模。像 `project_id`、`notify_url`、`callback_url`、`sub_openid`、`devs_id` 这类值都不应由模型猜测。

> **官方产品文档补充约束**：托管支付接入前还要完成控台项目创建、支付方式启用、费率配置、授权绑定和应用 ID 获取。`hosting_data.project_id`、`miniapp_data.seq_id`、`split_pay_flag` 对应权限、`notify_url` 合规性，都有明确的业务前置条件，不是只靠接口参数就能补出来的。

## 端到端支付流程

完整的支付链路包含 5 个阶段，开发者需理解全流程后再接入各接口：

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────┐     ┌──────────┐
│ ① 预下单  │────→│ ② 用户支付 │────→│ ③ 异步通知    │────→│ ④ 查询确认 │────→│ ⑤ 退款    │
│ (本 Skill) │     │ (前端跳转) │     │ (回调 notify) │     │ (二次校验) │     │ (可选)    │
└──────────┘     └──────────┘     └──────────────┘     └──────────┘     └──────────┘
```

### ① 预下单（本 Skill）

调用 `v2/trade/hosting/payment/preorder` 获得 `jump_url`，同时**保存 `req_seq_id` 和 `req_date`**（后续所有操作都需要）。

### ② 用户支付

- **H5/PC**：前端通过 `window.location.href = jump_url` 或 HTTP 302 重定向到收银台
- **小程序**：使用返回的 scheme_code 或 gh_id + path 拉起支付
- 支付完成后的页面回跳只代表前端流程结束，不代表后端可以直接把订单改成成功

### ③ 接收异步通知

汇付将交易结果 POST 到 `notify_url`，关键要点：
- 收到后返回 `RECV_ORD_ID_` + req_seq_id（5 秒内），否则汇付重试最多 3 次
- 以 `hf_seq_id` 为幂等键防止重复处理
- 详细接收示例见 [tech-spec.md 异步通知接收完整指南](../dougong-hostingpay-pay-base/references/tech-spec.md#异步通知接收完整指南)

### ④ 二次查询确认

即使收到异步通知，仍建议调用查询接口做二次确认：
- 接口：`v2/trade/hosting/payment/queryorderinfo`（见 [dougong-hostingpay-cashier-query](../dougong-hostingpay-cashier-query/SKILL.md)）
- 当同步返回 `trans_stat=P`（处理中）时，启动轮询：**间隔 5 秒，最多 30 次**
- 若 150 秒后仍为 P，记录异常日志并人工介入，**不要自动关单**
- 这一点与官方托管产品文档一致：前端回调和异步通知都不能替代关键业务环节的主动查询确认

### ⑤ 退款（可选）

当 `trans_stat=S` 后需退款：
- 接口：`v2/trade/hosting/payment/htRefund`（见 [dougong-hostingpay-cashier-refund](../dougong-hostingpay-cashier-refund/SKILL.md)）
- 退款需使用原交易的 `req_seq_id` 和 `req_date`

---

## 触发词

- "预下单"、"支付预下单"、"创建订单"、"下单接口"
- "H5 支付"、"PC 支付"、"H5 预下单"
- "支付宝小程序支付"、"支付宝小程序预下单"
- "微信小程序支付"、"微信小程序预下单"

## 场景路由

根据用户支付方式选择对应场景：

| 用户意图 | 场景 | pre_order_type | 详细说明 |
|---------|------|---------------|---------|
| H5/PC 网页支付 | H5/PC 预下单 | 1 | 见 [h5-pc-preorder.md](references/h5-pc-preorder.md) |
| 支付宝小程序支付 | 支付宝小程序预下单 | 2 | 见 [alipay-mini-preorder.md](references/alipay-mini-preorder.md) |
| 微信小程序支付 | 微信小程序预下单 | 3 | 见 [wechat-mini-preorder.md](references/wechat-mini-preorder.md) |

## 官方前置条件

| 场景 | 开发前必须完成什么 | 关键值 |
|------|------------------|-------|
| H5 / PC | 在合作伙伴控台创建托管项目、启用支付方式、记录 `project_id` | `hosting_data.project_id` |
| H5 / PC 微信支付 | 先配置微信授权域名 `api.huifu.com/hostingH5/` | 微信支付可用性 |
| 微信小程序 | 完成小程序托管授权、代码发布、绑定 appid 生成应用 ID，并开通微信支付产品 / 费率 | `miniapp_data.seq_id` |
| 微信小程序拆单支付 | 先特批并开通拆单支付权限 | `split_pay_flag` |
| 支付宝小程序 | 开通托管支付权限并配置支付宝费率 | `app_data`、`alipay_data` |
| 全场景异步通知 | 准备公网可达且满足官方约束的 `notify_url` | `notify_url` |

### H5/PC 参考文档索引

- 总览与示例：`references/h5-pc-preorder.md`
- 顶层请求参数：`references/h5-pc-preorder-request.md`
- 渠道扩展请求参数：`references/h5-pc-preorder-channel.md`
- 顶层同步/异步返回：`references/h5-pc-preorder-response.md`
- 渠道扩展返回参数：`references/h5-pc-preorder-response-channel.md`
- 错误码与排查：`references/h5-pc-preorder-errors.md`

## 汇付 API 端点

| 属性 | 值 |
|-----|-----|
| API 路径 | `v2/trade/hosting/payment/preorder` |
| 请求方式 | POST |
| Content-Type | application/json |

## 通用架构

三种预下单场景共享分层架构：

```
HFPayController (@RestController, /hfpay)
    └── POST /preOrder → hostingPayService.preOrder(req)

HostingPayService (@Service)
    └── preOrder() → 根据 preOrderType 选择 Request 类 → BasePayClient.request()

HostingPayPreOrderReq (DTO, @NotBlank 校验)
    ├── huifuId      — 商户号（必填）
    ├── transAmt     — 交易金额（必填）
    ├── goodsDesc    — 商品描述（必填）
    ├── preOrderType — 预下单类型（可选，默认 "1"）
    ├── notifyUrl    — 异步通知地址（可选）
    └── hostingData / bizInfo / wxData ... — 业务层保持对象结构，进入 SDK 前再序列化
```

## 通用请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| huifu_id | String(32) | Y | 商户号 |
| req_date | String(8) | Y | 请求日期 yyyyMMdd（SDK 自动生成） |
| req_seq_id | String(64) | Y | 请求流水号（SDK 自动生成） |
| pre_order_type | String(1) | Y | 1=H5/PC、2=支付宝小程序、3=微信小程序 |
| trans_amt | String(14) | Y | 交易金额，单位元，保留两位小数，最低 0.01 |
| goods_desc | String(40) | Y | 商品描述 |
| delay_acct_flag | String(1) | N | 是否延迟入账，Y=延迟、N=不延迟，默认 N |
| notify_url | String(512) | N | 异步通知地址 |
| time_expire | String(14) | N | 交易失效时间 yyyyMMddHHmmss，默认 10 分钟 |
| fee_sign | String(32) | N | 手续费场景标识码 |

## 通用同步返回参数

以下为三种预下单场景都会返回的公共字段；场景差异字段见各自 reference。

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 接口受理返回码，用于排查；订单终态仍看 `trans_stat`、异步通知和查询结果 |
| resp_desc | String(128) | 业务响应信息 |
| req_date | String(8) | 请求日期，原样返回 |
| req_seq_id | String(64) | 请求流水号，原样返回 |
| huifu_id | String(32) | 商户号，原样返回 |

场景差异字段：

- H5/PC：`pre_order_id`、`jump_url`、`hosting_data`、`current_time`、`time_expire`
- 支付宝小程序：`trans_amt`、`jump_url`
- 微信小程序：`trans_amt`、`pre_order_id`、`miniapp_data`

> **重要**：调用成功后务必保存 `req_seq_id` 和 `req_date`，后续查询、退款、关单均需使用。

## 异步通知参数（三种场景通用）

交易完成后汇付异步回调 notify_url，关键字段：

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 业务返回码 |
| resp_desc | String(512) | 业务返回描述 |
| huifu_id | String(32) | 商户号 |
| req_date | String(8) | 请求日期 |
| req_seq_id | String(64) | 请求流水号 |
| hf_seq_id | String(40) | 汇付全局流水号 |
| trans_type | String(20) | 交易类型（T_MINIAPP/A_JSAPI 等） |
| trans_amt | String(12) | 交易金额 |
| trans_stat | String(1) | 交易状态：S=成功、F=失败 |
| is_div | String(1) | 是否分账交易 |
| is_delay_acct | String(1) | 是否延迟交易 |

> 其余异步扩展字段（如 `wx_response`、`alipay_response`、`unionpay_response`、`dy_response`、`bank_extend_param`）按具体场景查看对应 reference。

## SDK Request 类对照

| 预下单类型 | SDK Request 类 | 差异化专属字段 |
|----------|---------------|-------------|
| H5/PC (type=1) | `V2TradeHostingPaymentPreorderH5Request` | `hostingData` |
| 支付宝小程序 (type=2) | `V2TradeHostingPaymentPreorderAliRequest` | `appData` |
| 微信小程序 (type=3) | `V2TradeHostingPaymentPreorderWxRequest` | `miniappData` |

## 常见错误与排查

| 错误码 | 原因 | 排查方法 |
|-------|------|---------|
| 99010002 | 预下单请求流水重复 | 使用新的 `req_seq_id`，`SequenceTools.getReqSeqId32()` 自动生成 |
| 10000000 | 无效参数 | 检查 `huifu_id`、`trans_amt`、`goods_desc` 等必填项格式 |
| 90000000 | 交易受限 / 微信 Scheme 生成失败 | 查看 resp_desc 详情，Scheme 失败需重新配置小程序 |

**网络/系统错误**：未收到响应或超时时，调用查询接口确认状态，切勿直接判定为失败。

> 快速接入代码示例见 [quickstart.md](references/quickstart.md)。
