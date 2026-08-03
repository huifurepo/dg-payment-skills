# 服务端 SDK 能力矩阵

这份矩阵用于说明官方语言支持范围、当前 Skill 包的真实覆盖边界，以及 PHP / Python 官方 SDK 的默认落地方式。

## 目录

- 官方语言支持概览
- 当前 Skill 包的真实覆盖范围
- 新增接口 SDK 兼容性
- 当前版本口径
- PHP 默认落地方式
- Python 默认落地方式
- 读法建议
- 语言边界提醒
- 调试日志硬停
- 传输安全硬停

## 官方语言支持概览

先区分制品身份：

- Lightning 极速版专用 SDK：当前明确发布证据只有 Java `dg-lightning-sdk 1.0.5`。
- 通用斗拱 SDK：Java/PHP/Python 可以包含 V4 Endpoint 的 Request/facade，但不能因此称为“Lightning 专用 SDK”。
- HTTP API 本身不限定实现语言；没有专用 SDK 不等于该语言不能接入，但原始 HTTP 路径必须另行验证签名、请求头、TLS 和响应验签。

| 语言 | 官方安装方式 | 最低运行时 | 当前说明 |
| --- | --- | --- | --- |
| Java | Maven | JDK 8+ | Lightning `1.0.5` 与通用 `3.0.40` 均关闭证书链和主机名校验，联调/生产可运行代码硬停 |
| PHP | Composer `huifurepo/dg-php-sdk` | PHP 7.4+ | API/Request 能力可核对，但锁定制品关闭 TLS 对端校验，生产代码硬停 |
| Python | pip `dg-sdk` | Python 3.x；本地 SDK classifier 只列到 3.7，实际项目需安装验证 | 聚合支付和托管支付核心场景已覆盖，当前 Skill 基线为 `dg-sdk 2.0.24` |
| C# | NuGet | .NET 4.8+ | 当前只保留入口说明 |
| Go | go mod | Go 1.16+ | 当前只保留入口说明 |

## 当前 Skill 包的真实覆盖范围

| 能力 | Java | PHP | Python | C# / Go |
| --- | --- | --- | --- | --- |
| 协议规则说明 | 完整 | 完整 | 完整 | 入口说明 |
| SDK / API 安装说明 | 完整 | 完整 | 完整 | 入口说明 |
| 初始化说明 | 完整 | 完整 | 完整 | 入口说明 |
| 请求头对齐策略 | 完整 | JSON 主链路可对齐；`CURLFile` multipart 已携带三个 SDK/Skill 头，但关闭签名/验签，仍阻断 | 完整；需显式配置 `jpt_x_skill_source`，`jpt-x-skill-huifu_id` 由请求 `huifu_id` 推导 | 需人工对照 |
| 聚合支付业务实现 | 完整 | 核心主链路覆盖 | 核心主链路覆盖 | 暂不提供 |
| 托管支付业务实现 | 完整 | 核心场景覆盖 | 核心场景覆盖 | 暂不提供 |

## 新增接口 SDK 兼容性

> `2026-07-28` 以用户提供的 Java/PHP/Python SDK 源码树核对。这里区分“独立场景 Request 类”和“通过共用 request 承载的场景化用法”；分发 provenance 仍需发布侧单独验证。

| 新增接口 | Java SDK | PHP SDK | Python SDK | Skill 输出规则 |
| --- | --- | --- | --- | --- |
| 抖音直连下单 `pre_order_type=4` | `V2TradeHostingPaymentPreorderDyRequest` | `V2TradeHostingPaymentPreorderDyRequest` | `V2TradeHostingPaymentPreorderDyRequest` | 当前三语言基线均有专属类，功能码仍指向共用 preorder Endpoint；`dy_data` 必须是 JSON 字符串 |
| 拆单支付订单查询 `splitpay/query` | `V2TradeHostingPaymentSplitpayQueryRequest` | `V2TradeHostingPaymentSplitpayQueryRequest` | `V2TradeHostingPaymentSplitpayQueryRequest` | 三语言均可生成官方 request 类代码；字段为 `req_date`、`req_seq_id`、`huifu_id`、`org_req_date`、`org_req_seq_id`，不要用普通 `queryorderinfo` 替代 |

## 当前版本口径

| 项目 | 版本 |
| --- | --- |
| 托管支付 Java SDK | `dg-java-sdk 3.0.40` |
| 聚合支付 Java SDK | `dg-lightning-sdk 1.0.5` |
| PHP SDK 包 | `huifurepo/dg-php-sdk 2.0.30` |
| Python SDK 包 | `dg-sdk 2.0.24` |
| 前端 JS SDK | `@dg-elements/js-sdk`，项目锁定版本 |

## PHP 默认落地方式

PHP 场景默认使用官方 Composer 包 `huifurepo/dg-php-sdk`，业务入口优先采用：

- 聚合支付核心主链路：`BsPaySdk\core\Payment`
- 聚合对账与托管支付：`BsPayClient::postRequest()`
- request 类提供 `funcCode`
- `params` 数组承载实际业务字段（适用于 `postRequest()` 路径）

当前 Skill 包的 PHP SDK 包基线是 `2.0.30`，优先通过 Composer 安装或升级：

```bash
composer require "huifurepo/dg-php-sdk:^2.0.30"
composer update huifurepo/dg-php-sdk --with-all-dependencies
composer show huifurepo/dg-php-sdk
test -f vendor/huifurepo/dg-php-sdk/BsPaySdk/init.php
```

Composer 不可用时，可以使用 Packagist 元数据指向的 GitHub 分发包手动下载当前基线：

- `https://api.github.com/repos/huifurepo/bspay-php-sdk/zipball/refs/tags/2.0.30`
- 解压后设置 `HUIFU_SDK_ROOT=/absolute/path/to/BsPaySdk`
- 必须执行 `test -f "$HUIFU_SDK_ROOT/init.php"` 确认实际 SDK 路径

官方 PHP SDK 文档在 2026-04-24 直接校验时仍只列到 `v2.0.25`，且 `php-sdk_v2.0.25.7z` OSS 地址返回 404；不能用旧版本可访问链接静默替代当前 `2.0.30` 基线。

当前 Skill 包不再内置 PHP 模板资产或非官方自维护 client。

## 调试日志硬停

- PHP SDK 自带 `init.php` 默认 `DEBUG=false`，但官方 `BsPayDemo/loader.php` 和 `Composer/BsPayConfig.php` 会在 SDK 初始化前定义 `DEBUG=true`。
- 调试开启后，`BsPayRequestV2` 会记录包含 `rsa_merch_private_key` 的 `MerConfig`、完整请求体和完整响应。
- PHP 联调/生产必须在加载任何 SDK、Demo/Composer 配置以及调用 `BsPay::init` 之前固定 `DEBUG=false`；不得使用 Demo/Composer loader，启动检查必须拒绝已定义为 `true` 的进程。不能证明时停止生成可运行实现。

## 传输安全硬停

- Lightning Java `1.0.5` 与通用 Java `3.0.40` 的实际 `HttpClientUtils` 都安装信任所有证书的 `X509TrustManager`，并让 `HostnameVerifier` 恒返回 `true`；关闭 `BasePay.debug` 只能阻止敏感日志，不能修复 TLS。未取得验证证书链和主机名的官方安全制品或经批准传输层前，不得生成联调或生产可运行代码，且必须以错证书、过期证书和错域名测试证明拒绝连接。
- 锁定的 PHP `2.0.30` 在 `BsPayRequestV2.php` 中设置 `CURLOPT_SSL_VERIFYPEER=false`。输出可运行代码前必须扫描实际安装源码：对端校验必须启用，`CURLOPT_SSL_VERIFYHOST` 必须为 `2`。
- 未通过上述检查时，只可解释字段、Request 类、产品边界和升级条件；不得把手写 HTTP、自制 wrapper、关闭校验或信任所有证书称为官方安全方案。

读取规则：

- 核对来源头时读 `references/shared-request-header-policy.md`
- 核对 API / `notify_url` 签名时读 `references/shared-signing-v2.md`
- 核对控台 Webhook 验签时读 `references/shared-webhook-signing.md`
- 需要确认官方 SDK 实现细节时，检查项目实际安装的 `huifurepo/dg-php-sdk` 源码
- 拆单支付订单查询可使用官方 `V2TradeHostingPaymentSplitpayQueryRequest`
- 抖音直连下单使用 `V2TradeHostingPaymentPreorderDyRequest`；旧基线才回退到 H5 Request + `pre_order_type=4`
- 不要回到历史自维护 PHP client 方案

推荐使用方式：

1. 先读 `references/shared-request-header-policy.md`
2. 再读对应 `*-php-adapter.md` 和 `*-php-scenarios.md`
3. 聚合支付核心主链路优先 `BsPaySdk\core\Payment`；聚合对账与托管支付优先 `BsPayClient::postRequest()`
4. 初始化 `MerConfig` 时显式配置 `skill_source`；只对已核验的无文件 JSON 主链路说明 SDK 自动带出来源头，`CURLFile` multipart 路径必须阻断
5. 排查差异时先比对本地请求报文、签名串和官方 SDK 实际源码，不引入非官方 client

## Python 默认落地方式

Python 场景默认使用官方 pip 包 `dg-sdk`，代码中 import `dg_sdk`。

当前 Skill 包的 Python SDK 包基线是 `2.0.24`。输出可运行代码前必须验证：

```bash
python3 -m pip install "dg-sdk==2.0.24"
python3 -c "import dg_sdk; print(dg_sdk.DGClient.__version__)"
```

安装或版本核对失败时必须显式报错并停止；不要静默改成无版本 `pip install dg-sdk`，也不要降级。

生产环境变量清单见 `aggregation-python-adapter.md` 与 `hostingpay-python-adapter.md`；Python 示例统一固定 `DGClient.env = "prod"`，不再生成测试环境切换函数。

业务入口优先采用：

- 聚合支付核心主链路：`dg_sdk.Payment` + `Payment*Request`
- 聚合对账：`dg_sdk.V2TradeCheckFilequeryRequest().post({})`
- 托管支付：`dg_sdk.V2TradeHostingPayment*Request().post({})`
- 抖音直连下单使用 `V2TradeHostingPaymentPreorderDyRequest`；拆单支付订单查询使用对应专属 request 类。

Python SDK 的来源头来自 `MerConfig` 和最终请求参数：

- `jpt_x_skill_source` -> HTTP header `jpt-x-skill-source`
- `data.huifu_id` -> HTTP header `jpt-x-skill-huifu_id`
- SDK 版本 -> HTTP header `jpt-sdk_version`

当前 Python SDK 会从本次请求 `data.huifu_id` 自动推导 `jpt-x-skill-huifu_id`。如果同一进程会请求多个商户号，不需要重置 `DGClient.mer_config` 的 huifu 头字段，但每个 request 对象必须设置本次真实 `huifu_id`。

## 读法建议

- 要做聚合支付初始化：读 `references/aggregation-base.md`
- 要做聚合支付下单：读 `references/aggregation-order.md`
- 要做聚合支付关单 / 查单：读 `references/aggregation-query.md`
- 要做聚合支付 Python 落地：读 `references/aggregation-python-adapter.md` 和 `references/aggregation-python-scenarios.md`
- 要做托管支付初始化：读 `references/hostingpay-base.md`
- 要做托管支付预下单：读 `references/hostingpay-preorder.md`
- 要做托管支付查询 / 关单 / 对账：读 `references/hostingpay-query.md`
- 要做托管支付退款：读 `references/hostingpay-refund.md`
- 要做托管支付 Python 落地：读 `references/hostingpay-python-adapter.md` 和 `references/hostingpay-python-scenarios.md`

## 语言边界提醒

- 聚合支付 PHP 已覆盖下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- 托管支付 PHP 已覆盖基础、预下单、查询 / 关单 / 对账、退款
- 托管支付 PHP 已有拆单支付查询和抖音直连专属 request 类
- PHP 受支持场景如果需要输出代码，必须体现官方 `huifurepo/dg-php-sdk`
- 聚合支付 Python 已覆盖下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- 托管支付 Python 已覆盖预下单、查询、关单、退款、退款查询、对账、拆单支付订单查询
- 托管支付 Python 抖音直连使用 `V2TradeHostingPaymentPreorderDyRequest`
- Python 受支持场景如果需要输出代码，必须体现官方 `dg-sdk` / `dg_sdk`
- Java 仍是聚合支付和托管支付的完整基线实现
