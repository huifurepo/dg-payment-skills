---
name: huifu-dougong-hostingpay-base
display_name: 汇付支付斗拱SDK基础
description: "汇付支付斗拱SDK基础 Skill：公共参数、协议规则、多语言 SDK 入口、Java 适配说明、错误码和 SDK 初始化。当开发者首次接入汇付托管支付或需要了解公共配置时使用。所有托管支付 Skill 的前置依赖。触发词：汇付接入、公共参数、签名规则、错误码、SDK 初始化、dg-java-sdk。"
version: 1.1.0
author: "jiaxiang.li | 内容版权：上海汇付支付有限公司"
homepage: https://paas.huifu.com/open/home/index.html
license: CC-BY-NC-4.0
compatibility:
  - openclaw
dependencies:
  - huifu-dougong-pay-shared-base
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

# 汇付斗拱支付 - 基础 Skill

本 Skill 是所有汇付托管支付业务 Skill 的公共基座，包含接入总览、鉴权流程、SDK 初始化和公共参数说明。

## 适配版本与复核信息

| 项目 | 内容 |
| --- | --- |
| Skill 版本 | `1.1.0` |
| 当前适配 SDK | `dg-java-sdk` `3.0.34`（当前仓库示例基线） |
| 最后复核日期 | `2026-04-08` |
| 官方文档来源 | 汇付开放平台 Java SDK 文档、托管支付相关接口文档、加验签说明、异步消息说明 |

## 多语言说明

从 `v1.1.0` 开始，这个 base skill 也按多语言底座来组织。  
协议规则和公共参数优先放在前面。  
语言安装方式、运行时要求和当前覆盖边界，统一看这里：

- [server-sdk-matrix.md](../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md)

当前仓库里，Java 资料最完整。  
其他语言先补入口和最小说明，后面再继续补充。

## 协议规则入口

真正语言无关的规则，统一看这两份：

- [signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- [async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md)

如果你要确认的是“协议怎么规定”，先看共享资料。  
如果你要找的是“Java 怎么落代码”，再看下面的 Java 适配说明和 references。

## 凭据要求与使用边界

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

**凭据使用与存放边界**：
- 本 Skill 是**文档型基础 Skill**，只声明接入方应用需要准备哪些配置，不会在 Skill 包内保存、落库、缓存或回传这些凭据
- `HUIFU_PRODUCT_ID`、`HUIFU_SYS_ID`、`HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 应由接入方项目的环境变量、CI/CD Secret 或密钥管理系统持有，而不是写入本仓库
- 这些值在业务应用启动后由 Spring Boot 配置装载，并传给 `dg-java-sdk` 的 `MerConfig` / `BasePay.initWithMerConfig()`，用于**请求签名和响应验签**
- 安装或阅读本 Skill 不会触发任何凭据采集、网络上传、文件写入或本地持久化动作；真实使用发生在接入方应用代码运行时
- 上线前应确认生产密钥只存在于受控运行环境中，并限制日志、调试输出和开发者本地副本

## 触发词

- "汇付接入"、"汇付支付"、"斗拱支付"
- "公共参数"、"签名规则"、"加签验签"
- "错误码"、"返回码"、"业务返回码"
- "SDK 初始化"、"汇付 SDK"、"dg-java-sdk"

## 接入总览

汇付斗拱支付采用「基础 Skill + 业务 Skill」分层架构：

```text
huifu-dougong-hostingpay-base/       (current: 公共基座，管理凭据和 SDK 初始化)
huifu-dougong-hostingpay-cashier-preorder/  (统一收银台 - 预下单，H5/PC、支付宝小程序、微信小程序)
huifu-dougong-hostingpay-cashier-query/  (统一收银台 - 交易查询与关单)
huifu-dougong-hostingpay-cashier-refund/ (统一收银台 - 退款与退款查询)
```

业务 Skill 通过 `dependencies: [huifu-dougong-hostingpay-base]` 声明依赖，不直接管理凭据。

## 接入流程

```text
1. 获取商户配置 -> 2. 确认语言运行时 -> 3. 看共享协议规则 -> 4. 进入语言适配说明 -> 5. 调用业务接口
```

### 步骤 1：获取配置

先准备公共配置项。  
这些值是跨语言通用的。

### 步骤 2：先看语言运行时矩阵

不同语言的安装方式和运行时要求不一样。  
先看这份总表：

- [server-sdk-matrix.md](../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md)

### 步骤 3：先看协议规则

真正语言无关的规则，统一看这里：

- [signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- [async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md)

### 步骤 4：Java 适配说明

当前仓库里的完整初始化示例，还是以 Java 为主。  
如果你现在用的是 Java，再继续看下面这部分。

显式的 Java 适配层文件在这里：

- [references/language-adapters/java.md](references/language-adapters/java.md)

### 步骤 5：注入环境变量（Java 示例）

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

### 步骤 6：SDK 安装与初始化（Java）

详见 [sdk-quickstart.md](references/sdk-quickstart.md)

## 鉴权流程

所有汇付 API 请求都需要签名：

1. **请求签名**：SDK 自动使用商户 RSA 私钥对请求 `data` 字段签名，生成 `sign` 字段
2. **响应验签**：SDK 自动使用汇付 RSA 公钥验证响应签名
3. **开发者无需手动处理签名**，SDK 内部已封装

协议级说明看共享资料：

- [signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md)
- [async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md)

## 参考资料索引

| 文件 | 内容 |
|-----|------|
| [../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md](../huifu-dougong-pay-shared-base/runtime/server-sdk-matrix.md) | 服务端多语言能力矩阵 |
| [../huifu-dougong-pay-shared-base/protocol/signing-v2.md](../huifu-dougong-pay-shared-base/protocol/signing-v2.md) | V2 签名规则（语言无关） |
| [../huifu-dougong-pay-shared-base/protocol/async-notify.md](../huifu-dougong-pay-shared-base/protocol/async-notify.md) | 异步通知规则（语言无关） |
| [quickstart.md](references/quickstart.md) | 5 分钟快速接入指南 |
| [customer-preparation.md](references/customer-preparation.md) | 客户前置准备清单、参数来源矩阵、各业务前置条件 |
| [payload-construction.md](references/payload-construction.md) | 必填 / 条件必填校验、对象字段完整性、JSON 字符串构造规范 |
| [language-adapters/java.md](references/language-adapters/java.md) | Java 适配层文件，集中放 Java 运行时和调用约束 |
| [common-params.md](references/common-params.md) | 公共请求/返回参数说明 |
| [tech-spec.md](references/tech-spec.md) | Java 适配补充（Spring Boot、HTTP 状态码、IP 白名单、历史 Java 示例） |
| [async-webhook.md](references/async-webhook.md) | `notify_url` 回调与 Webhook 使用说明 |
| [error-codes.md](references/error-codes.md) | 统一错误码 |
| [sdk-quickstart.md](references/sdk-quickstart.md) | SDK 安装 + 初始化代码示例 |
| [faq.md](references/faq.md) | 托管支付常见问题汇总 |

## Java 适配说明

下面这些内容都属于 Java 适配层，不属于协议层：

- `references/language-adapters/java.md` 这份显式 Java 适配层文件
- `sdk-quickstart.md` 里的 `dg-java-sdk` 安装和初始化
- `tech-spec.md` 里的 Spring Boot 兼容性
- `BasePayClient.request()` 这类 Java SDK 调用方式
- `setProcutId()` 这类 Java SDK 特有细节

如果你不是 Java 项目，重点先看共享协议层和运行时矩阵。

## 联调环境

在正式上线前，使用汇付联调（沙箱）环境进行测试，**不会产生真实扣款**。

### 切换到联调环境

```java
BasePay.prodMode = BasePay.MODE_TEST;  // 切换到联调环境
```

**注意**：上线前务必切回 `MODE_PROD`，建议通过环境变量控制：

```yaml
huifu:
  mode: ${HUIFU_MODE:prod}  # 默认生产，联调时设置环境变量 HUIFU_MODE=test
```

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

---

> 版权声明与联系方式见 [copyright-notice.md](../huifu-dougong-pay-shared-base/governance/copyright-notice.md)
