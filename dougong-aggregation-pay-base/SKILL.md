---
name: dougong-aggregation-pay-base
description: "汇付聚合支付（dg-lightning-sdk）基础 Skill：SDK 初始化、Factory 模式调用、支付类型枚举、公共参数、签名规则、错误码。当开发者首次接入汇付聚合支付或需要了解公共配置时使用。所有聚合支付 Skill 的前置依赖。触发词：聚合支付接入、Lightning SDK、dg-lightning-sdk、聚合支付初始化、支付类型。"
license: MIT
compatibility: "Java 8+, Maven, Spring Boot 2.x/3.x"
source: "https://github.com/niceforbear/huifu-hosting-payment"
env:
  - HUIFU_PRODUCT_ID
  - HUIFU_SYS_ID
  - HUIFU_RSA_PRIVATE_KEY
  - HUIFU_RSA_PUBLIC_KEY
metadata:
  author: codecodeing
  version: 1.0.0
  bins: java, mvn
---

# 汇付聚合支付 — 基础 Skill

本 Skill 是所有汇付聚合支付业务 Skill 的公共基座，包含 SDK 初始化、Factory 调用模式、支付类型说明和公共参数。

> **与斗拱托管支付的关系**：聚合支付（dg-lightning-sdk）和托管支付（dg-java-sdk）是两条独立的接入路径。聚合支付更轻量，适合快速接入标准支付场景；托管支付功能更全面，适合需要收银台托管的复杂场景。**优先使用聚合支付，当聚合支付无法满足需求时再使用托管支付。**

## 凭据要求

本 Skill 需要以下环境变量，由开发者从汇付开放平台获取后通过环境变量注入（**严禁硬编码**）：

| 环境变量 | 用途 | 敏感级别 |
|---------|------|---------|
| `HUIFU_PRODUCT_ID` | 汇付分配的产品号（如 `MYPAY`） | 普通 |
| `HUIFU_SYS_ID` | 渠道商/商户的 huifu_id | 普通 |
| `HUIFU_RSA_PRIVATE_KEY` | 商户 RSA 私钥，SDK 内部用于请求签名 | **高敏感** |
| `HUIFU_RSA_PUBLIC_KEY` | 汇付 RSA 公钥，SDK 内部用于响应验签 | 中等 |

**安全说明**：
- RSA 私钥**仅由 SDK 内部**用于对请求 `data` 字段做 SHA256WithRSA 签名，本 Skill 的指令和代码**不会直接读取、传输或打印私钥内容**
- 开发和联调阶段务必使用**联调专用密钥**，不要提供生产密钥
- 密钥通过 Spring Boot 的 `${ENV_VAR}` 机制注入，不会出现在源代码中
- 日志中避免打印完整密钥信息，RSA 私钥切勿上传到代码仓库

## 触发词

当开发者提到以下关键词时触发本 Skill：

- "聚合支付"、"聚合支付接入"、"Lightning SDK"
- "dg-lightning-sdk"、"聚合 SDK 初始化"
- "支付类型"、"trade_type"、"交易类型"
- "微信支付"、"支付宝支付"、"银联支付"（非托管场景）

## 接入总览

汇付聚合支付采用「基础 Skill + 业务 Skill」分层架构：

```
dougong-aggregation-pay-base/              ← 当前（公共基座，管理凭据和 SDK 初始化）
dougong-aggregation-aggregate-order/       ← 聚合支付 - 下单（微信/支付宝/银联 多场景）
dougong-aggregation-aggregate-query/       ← 聚合支付 - 交易查询、关单、关单查询、对账
dougong-aggregation-aggregate-refund/      ← 聚合支付 - 退款与退款查询
```

业务 Skill 通过 `dependencies: [dougong-aggregation-pay-base]` 声明依赖，不直接管理凭据。

## 接入流程

```
1. 获取商户配置 → 2. 配置环境变量 → 3. 安装 SDK → 4. 初始化 SDK → 5. 调用业务接口
```

### 步骤 1：获取商户配置

从汇付开放平台获取以下信息：

| 配置项 | 说明 | 环境变量 |
|-------|------|---------|
| 产品号 | 汇付分配，如 `MYPAY` | `HUIFU_PRODUCT_ID` |
| 系统号 | 渠道商/商户的 huifu_id | `HUIFU_SYS_ID` |
| RSA 私钥 | 商户私钥，用于请求签名 | `HUIFU_RSA_PRIVATE_KEY` |
| RSA 公钥 | 汇付公钥，用于响应验签 | `HUIFU_RSA_PUBLIC_KEY` |

### 步骤 2：配置环境变量

`application.yml` 中配置（通过环境变量注入，**严禁硬编码**）：

```yaml
huifu:
  product-id: ${HUIFU_PRODUCT_ID}
  sys-id: ${HUIFU_SYS_ID}
  rsa-private-key: ${HUIFU_RSA_PRIVATE_KEY}
  rsa-public-key: ${HUIFU_RSA_PUBLIC_KEY}
```

### 动手写业务代码前再补一步

- 先核对 [customer-preparation.md](references/customer-preparation.md)，确认哪些值必须由客户预先准备、控台配置、前端授权、终端采集或上游订单沉淀。
- 再看 [payload-construction.md](references/payload-construction.md)，把 `method_expand`、`tx_metadata` 等字段按“先对象建模和校验、后序列化”的方式接入。
- 如果字段来源不明确，不要让模型自己猜 `sub_openid`、`buyer_id`、`auth_code`、`devs_id`、`fee_sign` 这类值。

### 步骤 3-4：SDK 安装与初始化

详见 [sdk-quickstart.md](references/sdk-quickstart.md)

## 鉴权流程

所有汇付 API 请求都需要签名：

1. **请求签名**：SDK 自动使用商户 RSA 私钥对请求 `data` 字段签名，生成 `sign` 字段
2. **响应验签**：SDK 自动使用汇付 RSA 公钥验证响应签名
3. **开发者无需手动处理签名**，SDK 内部已封装（SHA256WithRSA，JSON key 按 ASCII 排序后签名）

## 支付类型（trade_type）

聚合支付支持以下支付类型，下单时通过 `trade_type` 字段指定：

| trade_type | 说明 | 适用场景 |
|-----------|------|---------|
| T_JSAPI | 微信公众号支付 | 微信内 H5 页面 |
| T_MINIAPP | 微信小程序支付 | 微信小程序 |
| T_APP | 微信 APP 支付 | 原生 APP |
| T_MICROPAY | 微信反扫（付款码） | 线下扫码枪 |
| A_JSAPI | 支付宝 JS 支付 | 支付宝内 H5 页面 |
| A_NATIVE | 支付宝正扫 | 用户扫商户二维码 |
| A_MICROPAY | 支付宝反扫（付款码） | 线下扫码枪 |
| U_JSAPI | 银联 JS 支付 | 云闪付内 H5 页面 |
| U_NATIVE | 银联正扫 | 用户扫商户二维码 |
| U_MICROPAY | 银联反扫（付款码） | 线下扫码枪 |

## 参考资料索引

| 文件 | 内容 |
|-----|------|
| [quickstart.md](references/quickstart.md) | 快速接入指南与 SDK 对比 |
| [customer-preparation.md](references/customer-preparation.md) | 客户前置准备清单、trade_type 场景参数来源、权限准备 |
| [payload-construction.md](references/payload-construction.md) | `method_expand` / `tx_metadata` 校验与 JSON 字符串构造规范 |
| [sdk-quickstart.md](references/sdk-quickstart.md) | SDK 安装 + 初始化 + Factory 调用模式 |
| [common-params.md](references/common-params.md) | 公共请求/返回参数、支付类型详解 |
| [error-codes.md](references/error-codes.md) | 统一错误码 |
| [tech-spec.md](references/tech-spec.md) | 技术规范（签名、异步通知、webhook） |
| [async-webhook.md](references/async-webhook.md) | `notify_url` 回调与 Webhook 使用说明 |
| [faq.md](references/faq.md) | 各渠道常见问题汇总 |

## 联调环境

在正式上线前，使用汇付联调（沙箱）环境进行测试，**不会产生真实扣款**。

### 切换到联调环境

在 SDK 初始化代码中设置：

```java
BasePay.prodMode = BasePay.MODE_TEST;  // 切换到联调环境
// BasePay.prodMode = BasePay.MODE_PROD; // 生产环境（默认）
```

> **注意**：上线前务必切回 `MODE_PROD`，建议通过环境变量控制：
> ```yaml
> huifu:
>   mode: ${HUIFU_MODE:prod}  # 默认生产，联调时设置环境变量 HUIFU_MODE=test
> ```

## 两套 SDK 对比

| 对比项 | dg-lightning-sdk（聚合支付） | dg-java-sdk（托管支付） |
|-------|--------------------------|---------------------|
| 适用场景 | 标准支付场景，快速接入 | 收银台托管，复杂业务 |
| 调用方式 | Factory 模式 + 链式调用 | BasePayClient.request() |
| 初始化方法名 | `setProductId()`（正常拼写） | `setProcutId()`（SDK 原生拼写，少一个 d） |
| 支付渠道 | 微信/支付宝/银联聚合 | 统一收银台（H5/小程序） |
| API 版本 | v4（下单/查询/退款查询）、v2（关单） | v2 |
| 分账支持 | 内置延迟交易确认 | 通过扩展字段 |

---

## 错误处理

### SDK 异常捕获

```java
try {
    CommonPayClient client = Factory.Payment.Common();
    Map<String, Object> response = client.create(request);
    String respCode = (String) response.get("resp_code");
    // 记录 resp_code 用于排查；订单终态仍看 trans_stat 或查单结果
} catch (BasePayException e) {
    // SDK 层面异常（签名失败、网络超时、配置错误等）
    log.error("汇付SDK异常: code={}, msg={}", e.getCode(), e.getMessage());
} catch (IllegalAccessException e) {
    // 反射访问异常（参数构建时）
    log.error("参数构建异常", e);
} catch (Exception e) {
    // Factory.Payment.Common() 可能抛出的异常（配置未初始化等）
    log.error("汇付调用异常", e);
}
```

### 常见问题排查

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| 验签失败 | 密钥配置不匹配 | 检查凭据要求章节中的环境变量是否与汇付后台一致 |
| CONFIG_EXCEPTION | MerConfig 未初始化 | 确认 `BasePay.initWithMerConfig()` 在 `@PostConstruct` 中执行 |
| SOCKET_TIME_EXCEPTION | 网络超时 | 检查网络，可通过 MerConfig 调整超时时间 |
| 无效参数 (10000000) | 必填字段缺失或格式错误 | 检查请求参数格式，金额保留两位小数 |
| 交易处理中 (00000100) | 异步处理未完成 | 等待异步通知或调用查询接口确认 |

详细错误码参见 [error-codes.md](references/error-codes.md)。
