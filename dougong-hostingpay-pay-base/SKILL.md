---
name: dougong-hostingpay-pay-base
description: "汇付托管支付（dg-java-sdk）基础 Skill：公共参数、技术规范、签名规则、错误码、SDK 初始化。当开发者首次接入汇付托管支付或需要了解公共配置时使用。所有托管支付 Skill 的前置依赖。触发词：汇付接入、公共参数、签名规则、错误码、SDK 初始化、dg-java-sdk。"
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

# 汇付斗拱支付 — 基础 Skill

本 Skill 是所有汇付托管支付业务 Skill 的公共基座，包含接入总览、鉴权流程、SDK 初始化和公共参数说明。

## 凭据要求

本 Skill 需要以下环境变量，由开发者从汇付开放平台获取后通过环境变量注入（**严禁硬编码**）：

| 环境变量 | 用途 | 敏感级别 |
|---------|------|---------|
| `HUIFU_PRODUCT_ID` | 汇付分配的产品号（如 `YYZY`） | 普通 |
| `HUIFU_SYS_ID` | 渠道商/商户的 huifu_id | 普通 |
| `HUIFU_RSA_PRIVATE_KEY` | 商户 RSA 私钥，SDK 内部用于请求签名 | **高敏感** |
| `HUIFU_RSA_PUBLIC_KEY` | 汇付 RSA 公钥，SDK 内部用于响应验签 | 中等 |

**安全说明**：
- RSA 私钥**仅由 SDK 内部**用于对请求 `data` 字段做 SHA256WithRSA 签名，本 Skill 的指令和代码**不会直接读取、传输或打印私钥内容**
- 开发和联调阶段务必使用**联调专用密钥**，不要提供生产密钥
- 密钥通过 Spring Boot 的 `${ENV_VAR}` 机制注入，不会出现在源代码中
- 日志中避免打印完整密钥信息，RSA 私钥切勿上传到代码仓库

## 触发词

- "汇付接入"、"汇付支付"、"斗拱支付"
- "公共参数"、"签名规则"、"加签验签"
- "错误码"、"返回码"、"业务返回码"
- "SDK 初始化"、"汇付 SDK"、"dg-java-sdk"

## 接入总览

汇付斗拱支付采用「基础 Skill + 业务 Skill」分层架构：

```
dougong-hostingpay-pay-base/       ← 当前（公共基座，管理凭据和 SDK 初始化）
dougong-hostingpay-cashier-order/  ← 统一收银台 - 预下单（H5/PC、支付宝小程序、微信小程序）
dougong-hostingpay-cashier-query/  ← 统一收银台 - 交易查询与关单
dougong-hostingpay-cashier-refund/ ← 统一收银台 - 退款与退款查询
```

业务 Skill 通过 `dependencies: [dougong-hostingpay-pay-base]` 声明依赖，不直接管理凭据。

## 接入流程

```
1. 获取商户配置 → 2. 配置环境变量 → 3. 安装 SDK → 4. 初始化 SDK → 5. 调用业务接口
```

### 步骤 1-2：获取配置并注入环境变量

`application.yml` 中配置：

```yaml
huifu:
  product-id: ${HUIFU_PRODUCT_ID}
  sys-id: ${HUIFU_SYS_ID}
  rsa-private-key: ${HUIFU_RSA_PRIVATE_KEY}
  rsa-public-key: ${HUIFU_RSA_PUBLIC_KEY}
```

### 动手写业务代码前再补一步

- 先核对 [customer-preparation.md](references/customer-preparation.md)，确认哪些值必须由客户预先准备、控台开通、前端授权或终端采集。
- 再看 [payload-construction.md](references/payload-construction.md)，按“先对象建模和校验、后序列化入 SDK”的方式落代码。
- 如果字段没有明确来源，不要让模型自行猜测或补伪造默认值。

### 步骤 3-4：SDK 安装与初始化

详见 [sdk-quickstart.md](references/sdk-quickstart.md)

## 鉴权流程

所有汇付 API 请求都需要签名：

1. **请求签名**：SDK 自动使用商户 RSA 私钥对请求 `data` 字段签名，生成 `sign` 字段
2. **响应验签**：SDK 自动使用汇付 RSA 公钥验证响应签名
3. **开发者无需手动处理签名**，SDK 内部已封装

## 参考资料索引

| 文件 | 内容 |
|-----|------|
| [quickstart.md](references/quickstart.md) | 5 分钟快速接入指南 |
| [customer-preparation.md](references/customer-preparation.md) | 客户前置准备清单、参数来源矩阵、各业务前置条件 |
| [payload-construction.md](references/payload-construction.md) | 必填 / 条件必填校验、对象字段完整性、JSON 字符串构造规范 |
| [common-params.md](references/common-params.md) | 公共请求/返回参数说明 |
| [tech-spec.md](references/tech-spec.md) | 技术规范（签名、编码、限流、异步通知） |
| [async-webhook.md](references/async-webhook.md) | `notify_url` 回调与 Webhook 使用说明 |
| [error-codes.md](references/error-codes.md) | 统一错误码 |
| [sdk-quickstart.md](references/sdk-quickstart.md) | SDK 安装 + 初始化代码示例 |
| [faq.md](references/faq.md) | 托管支付常见问题汇总 |

## 联调环境

在正式上线前，使用汇付联调（沙箱）环境进行测试，**不会产生真实扣款**。

### 切换到联调环境

```java
BasePay.prodMode = BasePay.MODE_TEST;  // 切换到联调环境
```

> **注意**：上线前务必切回 `MODE_PROD`，建议通过环境变量控制：
> ```yaml
> huifu:
>   mode: ${HUIFU_MODE:prod}  # 默认生产，联调时设置环境变量 HUIFU_MODE=test
> ```

### 联调商户号申请

联调环境需要**专用的测试商户号和密钥**，不能使用生产凭据。联系汇付销售经理或技术支持申请。

## 错误处理

### SDK 异常捕获

```java
try {
    Map<String, Object> response = BasePayClient.request(request, false);
    String respCode = (String) response.get("resp_code");
    // 记录 resp_code 用于排查；订单终态仍看 trans_stat 或查单结果
} catch (BasePayException e) {
    // SDK 层面异常（签名失败、网络超时等）
    log.error("汇付SDK异常", e);
} catch (IllegalAccessException e) {
    // 反射访问异常
    log.error("参数构建异常", e);
}
```

### 常见问题排查

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| 网关验签失败 (HTTP 922) | 密钥配置不匹配 | 检查环境变量中的密钥是否与汇付后台一致 |
| 无效参数 (10000000) | 必填字段缺失或格式错误 | 检查请求参数格式，金额保留两位小数 |
| 交易正在处理中 (00000100) | 异步处理未完成 | 等待异步通知或调用查询接口确认 |
| 超时无响应 | 网络问题 | 调用查询接口确认状态，切勿直接判定失败 |

详细错误码参见 [error-codes.md](references/error-codes.md)。
