---
name: huifu-dougong-hostingpay-cashier-preorder
display_name: 汇付支付斗拱统一收银台预下单
description: "汇付支付斗拱统一收银台预下单 Skill：覆盖 H5/PC、支付宝小程序、微信小程序三种预下单场景。参数表和业务规则按协议字段组织，Java SDK 调用方式放在语言适配入口里。当开发者需要创建托管支付订单时使用。触发词：托管预下单、收银台预下单、H5支付、小程序支付、创建托管订单。"
version: 1.1.0
author: "jiaxiang.li | 内容版权：上海汇付支付有限公司"
homepage: https://paas.huifu.com/open/home/index.html
license: CC-BY-NC-4.0
compatibility:
  - openclaw
dependencies:
  - huifu-dougong-hostingpay-base
metadata:
  openclaw:
    requires:
      config:
        - HUIFU_PRODUCT_ID
        - HUIFU_SYS_ID
        - HUIFU_RSA_PRIVATE_KEY
        - HUIFU_RSA_PUBLIC_KEY
        - HUIFU_NOTIFY_URL
        - HUIFU_PROJECT_ID
        - HUIFU_PROJECT_TITLE
        - HUIFU_CALLBACK_URL
---

> **版权声明**：本 Skill 内容来源于上海汇付支付有限公司官方开放平台文档，版权归属上海汇付支付有限公司。如有疑问可咨询汇付支付客服：400-820-2819 / cs@huifu.com
>
> **Source**: Official Open Platform documentation of Shanghai Huifu Payment Co., Ltd.
>
> **Copyright**: Shanghai Huifu Payment Co., Ltd.

---

# 统一收银台 - 预下单

覆盖三种预下单场景：H5/PC、支付宝小程序、微信小程序。

## 适配版本与复核信息

| 项目 | 内容 |
| --- | --- |
| Skill 版本 | `1.1.0` |
| 当前适配 SDK | `dg-java-sdk` `3.0.34` |
| 最后复核日期 | `2026-04-08` |
| 官方文档来源 | 汇付开放平台托管支付预下单接口文档、Java SDK 文档、加验签说明、异步消息说明 |

## 运行依赖与凭据边界

本 Skill 依赖 [huifu-dougong-hostingpay-base](../huifu-dougong-hostingpay-base/SKILL.md) 提供公共运行时。凭据使用规则与存放边界见 [credential-boundary.md](../huifu-dougong-pay-shared-base/governance/credential-boundary.md)。

本文中出现的 `sign`、`cert_no`、`download_url` 等示例值均为占位写法或字段名说明，不提供真实签名串、密文证件号或可复用下载地址。

> **前置依赖**：首次接入请先阅读 [huifu-dougong-hostingpay-base](../huifu-dougong-hostingpay-base/SKILL.md) 完成 SDK 初始化。

> **开发前先补两步**：先核对 [客户前置准备清单](../huifu-dougong-hostingpay-base/references/customer-preparation.md)，再按 [参数校验与 JSON 构造规范](../huifu-dougong-hostingpay-base/references/payload-construction.md) 建模。像 `project_id`、`notify_url`、`callback_url`、`sub_openid`、`devs_id` 这类值都不应由模型猜测。

> **官方产品文档补充约束**：托管支付接入前还要完成控台项目创建、支付方式启用、费率配置、授权绑定和应用 ID 获取。`hosting_data.project_id`、`miniapp_data.seq_id`、`split_pay_flag` 对应权限、`notify_url` 合规性，都有明确的业务前置条件，不是只靠接口参数就能补出来的。

## 协议规则入口

这份 Skill 主要讲预下单场景。  
真正跨语言共用的协议规则，统一看共享资料：

- [signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- [async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md)

## 语言适配入口

这份 Skill 里的参数表、场景路由和状态说明，都是语言无关的。  
具体语言怎么初始化 SDK、怎么发请求，先看这里：

- [huifu-dougong-hostingpay-base/SKILL.md](../huifu-dougong-hostingpay-base/SKILL.md)
- [server-sdk-matrix.md](../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md)

前端如果要渲染托管收银台，不在这里做，直接看：

- [huifu-dougong-hostingpay-checkout-js/SKILL.md](../huifu-dougong-hostingpay-checkout-js/SKILL.md)

## 端到端支付流程

完整的支付链路包含 5 个阶段，开发者需理解全流程后再接入各接口：

```text
[1] 预下单 (本 Skill)
  -> [2] 用户支付 (前端跳转)
  -> [3] 异步通知 (回调 notify)
  -> [4] 查询确认 (二次校验)
  -> [5] 退款 (可选)
```

### 步骤 1：预下单（本 Skill）

调用 `v2/trade/hosting/payment/preorder` 获得 `jump_url`，同时**保存 `req_seq_id` 和 `req_date`**（后续所有操作都需要）。

### 步骤 2：用户支付

- **纯跳转模式**：H5/PC 可以继续使用 `window.location.href = jump_url` 或 HTTP 302 直接跳转收银台
- **前端自定义收银台模式**：如果页面自己渲染支付入口，直接接 [huifu-dougong-hostingpay-checkout-js](../huifu-dougong-hostingpay-checkout-js/SKILL.md)，由前端通过 `HFPay` 和 `createPreOrder` 拉起支付
- **小程序模式**：使用返回的 scheme_code 或 gh_id + path 拉起支付
- **前后端对齐规则**：`pre_order_type=1` 对应 H5/PC，`pre_order_type=2` 对应支付宝小程序，`pre_order_type=3` 对应微信小程序
- 支付完成后的页面回跳只代表前端流程结束，不代表后端可以直接把订单改成成功

### 步骤 3：接收异步通知

汇付将交易结果 POST 到 `notify_url`，关键要点：
- 收到后返回 `RECV_ORD_ID_` + req_seq_id（5 秒内），否则汇付重试最多 3 次
- 以 `hf_seq_id` 为幂等键防止重复处理
- 详细接收示例见 [tech-spec.md 异步通知接收完整指南](../huifu-dougong-hostingpay-base/references/tech-spec.md#异步通知接收完整指南)

### 步骤 4：二次查询确认

即使收到异步通知，仍建议调用查询接口做二次确认：
- 接口：`v2/trade/hosting/payment/queryorderinfo`（见 [huifu-dougong-hostingpay-cashier-query](../huifu-dougong-hostingpay-cashier-query/SKILL.md)）
- 当同步返回 `trans_stat=P`（处理中）时，启动轮询：**间隔 5 秒，最多 30 次**
- 若 150 秒后仍为 P，记录异常日志并人工介入，**不要自动关单**
- 这一点与官方托管产品文档一致：前端回调和异步通知都不能替代关键业务环节的主动查询确认

### 步骤 5：退款（可选）

当 `trans_stat=S` 后需退款：
- 接口：`v2/trade/hosting/payment/htRefund`（见 [huifu-dougong-hostingpay-cashier-refund](../huifu-dougong-hostingpay-cashier-refund/SKILL.md)）
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

```text
接口层
  +- 接收前端或业务系统的预下单请求
  +- 校验商户号、金额、商品描述、项目参数、回调地址

业务逻辑层
  +- 根据 pre_order_type 选择对应的预下单场景
  +- 组装托管支付请求报文
  +- 调用对应语言 SDK 或 HTTP 客户端发起 `v2/trade/hosting/payment/preorder`
  +- 保存 req_seq_id / req_date / pre_order_id 供查单和退款复用

请求对象
  |- huifu_id
  |- trans_amt
  |- goods_desc
  |- pre_order_type
  |- notify_url
  +- hosting_data / app_data / miniapp_data 等对象字段
```

下面出现的 SDK Request 类名，是 Java 适配层的写法。  
如果你不是 Java 项目，参数结构仍按本 Skill 的协议字段来实现。

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

---

> 版权声明与联系方式见 [copyright-notice.md](../huifu-dougong-pay-shared-base/governance/copyright-notice.md)
