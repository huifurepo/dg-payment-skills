# 汇付支付 Skill 集合

基于汇付 SDK 的支付接入技能集，包含两条接入路径：**聚合支付**（dg-lightning-sdk）和**托管支付**（dg-java-sdk）。本库内容已按对应官方 markdown 文档复核，不只整理接口参数，也补入了业务开通、控台配置、授权绑定、参数来源和客户侧校验约束。

> **选择建议**：优先使用聚合支付（Lightning），接入更快、更轻量。当聚合支付无法满足需求时（如需要收银台托管），再使用托管支付。

## 适用技术栈

- Java 8+
- Spring Boot 2.x / 3.x
- Maven
- dg-lightning-sdk 1.0.3（聚合支付）
- dg-java-sdk 3.0.34（托管支付）

## Skill 列表

### 聚合支付（dg-lightning-sdk）— 推荐

| Skill | 功能 | 前置依赖 |
|-------|------|---------|
| [donggong-aggregation-pay-base](donggong-aggregation-pay-base/) | 公共基座：SDK 初始化、Factory 模式、支付类型、公共参数 | 无 |
| [donggong-aggregation-aggregate-order](donggong-aggregation-aggregate-order/) | 聚合支付下单：微信/支付宝/银联 全场景 | donggong-aggregation-pay-base |
| [donggong-aggregation-aggregate-query](donggong-aggregation-aggregate-query/) | 交易查询 + 关单 + 关单查询 + 对账单 | donggong-aggregation-pay-base |
| [donggong-aggregation-aggregate-refund](donggong-aggregation-aggregate-refund/) | 退款申请 + 退款结果查询 | donggong-aggregation-pay-base |

### 托管支付（dg-java-sdk）

| Skill | 功能 | 前置依赖 |
|-------|------|---------|
| [dougong-hostingpay-pay-base](dougong-hostingpay-pay-base/) | 公共基座：SDK 初始化、技术规范、公共参数、错误码 | 无 |
| [dougong-hostingpay-cashier-order](dougong-hostingpay-cashier-order/) | 预下单：H5/PC、支付宝小程序、微信小程序 | dougong-hostingpay-pay-base |
| [dougong-hostingpay-cashier-query](dougong-hostingpay-cashier-query/) | 交易查询 + 关单 + 对账单 | dougong-hostingpay-pay-base |
| [dougong-hostingpay-cashier-refund](dougong-hostingpay-cashier-refund/) | 退款申请 + 退款结果查询 | dougong-hostingpay-pay-base |

## 两条路径对比

| 对比项 | 聚合支付（Lightning） | 托管支付（斗拱） |
|-------|-------------------|---------------|
| SDK | dg-lightning-sdk 1.0.3 | dg-java-sdk 3.0.34 |
| 接入难度 | 低，Factory 模式 | 中，手动构建 Request |
| 支付渠道 | 微信/支付宝/银联直接聚合（10种） | 统一收银台（H5/小程序 3种） |
| 适用场景 | 标准支付，快速上线 | 收银台托管，复杂业务 |
| API 版本 | v4（主要）+ v2 | v2 |
| 初始化差异 | `setProductId()`（正常） | `setProcutId()`（少一个d） |
| 调用方式 | `Factory.Payment.Common().create(req)` | `BasePayClient.request(req, false)` |

## 目录结构

```
├── README.md                          # 本文件
│
├── donggong-aggregation-pay-base/                # 聚合支付 - 公共基座
│   ├── SKILL.md
│   └── references/
│       ├── quickstart.md              # 快速接入指南
│       ├── customer-preparation.md    # 客户前置准备清单与参数来源
│       ├── payload-construction.md    # 参数校验、对象建模与 JSON 序列化规范
│       ├── sdk-quickstart.md          # SDK 安装 + Factory 模式
│       ├── common-params.md           # 公共参数 + 支付类型
│       ├── error-codes.md             # 错误码
│       ├── tech-spec.md               # 技术规范
│       ├── async-webhook.md           # notify_url 回调与 Webhook
│       └── faq.md                     # 各渠道常见问题
├── donggong-aggregation-aggregate-order/         # 聚合支付 - 下单
│   ├── SKILL.md
│   └── references/
│       ├── quickstart.md              # 快速接入指南
│       ├── aggregate-order.md         # 全场景下单总览
│       ├── aggregate-order-request.md # 公共请求参数与顶层字段
│       ├── aggregate-order-method-wechat.md
│       ├── aggregate-order-method-alipay.md
│       ├── aggregate-order-method-unionpay.md
│       ├── aggregate-order-tx-metadata.md
│       ├── aggregate-order-response.md
│       └── aggregate-order-errors.md
├── donggong-aggregation-aggregate-query/         # 聚合支付 - 查询与关单
│   ├── SKILL.md
│   └── references/
│       ├── quickstart.md              # 快速接入指南
│       ├── payment-query.md           # 交易查询
│       ├── trade-close.md             # 交易关单
│       ├── close-query.md             # 关单查询
│       └── reconciliation.md          # 对账单查询
├── donggong-aggregation-aggregate-refund/        # 聚合支付 - 退款
│   ├── SKILL.md
│   └── references/
│       ├── quickstart.md              # 快速接入指南
│       ├── refund.md                  # 退款申请
│       └── refund-query.md            # 退款查询
│
├── dougong-hostingpay-pay-base/       # 托管支付 - 公共基座
│   ├── SKILL.md
│   └── references/
│       ├── quickstart.md              # 快速接入指南
│       ├── customer-preparation.md    # 客户前置准备清单与参数来源
│       ├── payload-construction.md    # 参数校验、对象建模与 JSON 序列化规范
│       ├── sdk-quickstart.md
│       ├── tech-spec.md
│       ├── async-webhook.md           # notify_url 回调与 Webhook
│       ├── common-params.md
│       ├── error-codes.md
│       └── faq.md                     # 托管支付常见问题
├── dougong-hostingpay-cashier-order/  # 托管支付 - 预下单
│   ├── SKILL.md
│   └── references/
│       ├── quickstart.md              # 快速接入指南
│       ├── h5-pc-preorder.md
│       ├── h5-pc-preorder-request.md
│       ├── h5-pc-preorder-channel.md
│       ├── h5-pc-preorder-response.md
│       ├── h5-pc-preorder-response-channel.md
│       ├── h5-pc-preorder-errors.md
│       ├── alipay-mini-preorder.md
│       └── wechat-mini-preorder.md
├── dougong-hostingpay-cashier-query/  # 托管支付 - 查询与关单
│   ├── SKILL.md
│   └── references/
│       ├── quickstart.md              # 快速接入指南
│       ├── payment-status-query.md
│       ├── trade-close.md
│       └── reconciliation.md          # 交易结算对账单查询
└── dougong-hostingpay-cashier-refund/ # 托管支付 - 退款
    ├── SKILL.md
    └── references/
        ├── quickstart.md              # 快速接入指南
        ├── refund.md
        └── refund-query.md
```

## 本次文档增强重点

这批 Skill 不是简单搬运官方字段表，重点新增了 4 类商户最容易缺失的接入信息：

- **客户前置准备清单**：把控台开通、授权绑定、参数来源、上游订单沉淀拆开说明，避免模型或商户自己猜值。
- **参数建模与序列化规范**：把 `String(JSON Object)`、`String(JSON Array)` 这类 SDK 边界字段改成“业务层先对象建模，SDK 边界再统一序列化”。
- **异步通知接收规范**：补上 `notify_url` / Webhook 区分、验签、幂等、应答格式、查询兜底，而不是只给一个能跑通的壳子。
- **返回码使用边界**：强调 `resp_code`、HTTP 返回码主要用于排查和日志，订单终态仍要以 `trans_stat`、`order_stat`、异步通知和主动查询为准。

## 初始化阅读入口

第一次接入时，不要直接从业务接口字段表开始翻。建议按下面的顺序阅读：

| 接入路径 | 第 1 份 | 第 2 份 | 第 3 份 | 解决的问题 |
|---------|--------|--------|--------|-----------|
| 聚合支付 | `donggong-aggregation-pay-base/SKILL.md` | `donggong-aggregation-pay-base/references/quickstart.md` | `donggong-aggregation-pay-base/references/customer-preparation.md` | 先确认选型、SDK 初始化方式、客户必须预先准备的真实参数 |
| 托管支付 | `dougong-hostingpay-pay-base/SKILL.md` | `dougong-hostingpay-pay-base/references/quickstart.md` | `dougong-hostingpay-pay-base/references/customer-preparation.md` | 先确认 SDK 初始化、项目号/授权/回调地址等前置条件 |

如果已经进入编码阶段，再补读两份基础文档：

- `references/payload-construction.md`：解决对象字段怎么建模、何时序列化。
- `references/async-webhook.md`：解决异步通知怎么接、怎么验签、怎么应答。

## 接入顺序

### 聚合支付（推荐）

```
① donggong-aggregation-pay-base       获取商户配置 → 安装 SDK → 初始化 Factory
       ↓
② donggong-aggregation-aggregate-order 调用下单接口 → 获取 qr_code/pay_info → 用户支付
       ↓
③ donggong-aggregation-aggregate-query 查询支付结果 / 关闭超时订单 / 查询对账单
       ↓
④ donggong-aggregation-aggregate-refund（可选）发起退款 → 查询退款结果
```

### 托管支付

```
① dougong-hostingpay-pay-base     获取商户配置 → 安装 SDK → 初始化
       ↓
② dougong-hostingpay-cashier-order 调用预下单接口 → 用户支付 → 接收异步通知
       ↓
③ dougong-hostingpay-cashier-query 查询支付结果（二次确认）/ 关闭超时订单
       ↓
④ dougong-hostingpay-cashier-refund（可选）发起退款 → 查询退款结果
```

## 环境变量

所有 Skill 共用以下环境变量，**严禁硬编码**：

| 变量 | 说明 | 聚合支付 | 托管支付 |
|------|------|---------|---------|
| `HUIFU_PRODUCT_ID` | 汇付分配的产品号 | Y | Y |
| `HUIFU_SYS_ID` | 渠道商/商户的 huifu_id | Y | Y |
| `HUIFU_RSA_PRIVATE_KEY` | 商户 RSA 私钥 | Y | Y |
| `HUIFU_RSA_PUBLIC_KEY` | 汇付 RSA 公钥 | Y | Y |
| `HUIFU_NOTIFY_URL` | 支付异步通知地址 | Y | Y |
| `HUIFU_REFUND_NOTIFY_URL` | 退款异步通知地址 | Y | Y |
| `HUIFU_PROJECT_ID` | 托管项目 ID | - | Y |
| `HUIFU_PROJECT_TITLE` | 托管项目名称 | - | Y |
| `HUIFU_CALLBACK_URL` | 支付完成后前端回调地址 | - | N |

## 客户前置准备与参数建模

环境变量只覆盖了“全局固定配置”。真正影响接口能否顺利落地的，还有大量客户预先开通、控台配置、前端授权、终端采集和上游订单沉淀的数据，这些值**不能让模型自行猜测**。

开始写业务代码前，先阅读对应接入路径的两份基础文档：

| 接入路径 | 客户前置准备 | 参数校验与构造 |
|---------|-------------|---------------|
| 聚合支付 | [donggong-aggregation-pay-base/references/customer-preparation.md](donggong-aggregation-pay-base/references/customer-preparation.md) | [donggong-aggregation-pay-base/references/payload-construction.md](donggong-aggregation-pay-base/references/payload-construction.md) |
| 托管支付 | [dougong-hostingpay-pay-base/references/customer-preparation.md](dougong-hostingpay-pay-base/references/customer-preparation.md) | [dougong-hostingpay-pay-base/references/payload-construction.md](dougong-hostingpay-pay-base/references/payload-construction.md) |

统一要求：

- 必填、非必填、条件必填参数在客户侧接口层先做校验和拦截，不要把缺参请求直接放进 SDK。
- 官方开发指引里要求的业务开通、项目创建、费率配置、应用授权绑定、对账文件配置，也属于“客户前置准备”的一部分，不是单纯补字段。
- 文档里标注为 `String(JSON Object)`、`String(JSON Array)` 的字段，只代表 **SDK 边界类型** 是字符串，不代表业务层应该把对象建模成裸字符串。
- 优先在业务层使用嵌套 DTO / `Map` / `List` / `ObjectNode` 完整建模，做完校验后再统一序列化为 JSON 字符串传给 SDK。
- 如果参数值没有明确来源，例如客户未提供 `project_id`、`sub_openid`、`buyer_id`、`devs_id`、`fee_sign`、`payer_client_ip` 等，模型不应擅自补默认值或伪造占位值。
- 多个官方渠道开发指引都明确写了：前端支付完成回调不等于最终成功，后端仍需调用查询接口确认订单状态。

## 快速开始

1. **聚合支付**：阅读 [donggong-aggregation-pay-base/SKILL.md](donggong-aggregation-pay-base/SKILL.md) 完成 SDK 初始化
2. **托管支付**：阅读 [dougong-hostingpay-pay-base/SKILL.md](dougong-hostingpay-pay-base/SKILL.md) 完成 SDK 初始化
3. 根据业务场景选择对应 Skill 的 SKILL.md 开始接入

## 文档说明

- 客户交付应优先阅读各 skill 下的 `SKILL.md` 与 `references/` 文档，这些内容已按当前结构整理并校验。
- 每条基础路径下的 `quickstart.md` 都补了“文件阅读地图”，明确每个文件相比官方字段表新增或强化了什么、什么时候该看它。
