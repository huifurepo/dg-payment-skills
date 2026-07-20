# 服务端 SDK 能力矩阵

这份矩阵用于说明官方语言支持范围、当前 Skill 包的真实覆盖边界，以及 PHP / Python 官方 SDK 的默认落地方式。

## 目录

- 官方语言支持概览
- 当前 Skill 包的真实覆盖范围
- 新增接口 SDK 兼容性
- 商户进件 SDK 证据
- 当前版本口径
- PHP 默认落地方式
- Python 默认落地方式
- 读法建议
- 语言边界提醒

## 官方语言支持概览

| 语言 | 官方安装方式 | 最低运行时 | 当前说明 |
| --- | --- | --- | --- |
| Java | Maven | JDK 8+ | 聚合支付和托管支付都有稳定基线 |
| PHP | Composer `huifurepo/dg-php-sdk` | PHP 7.4+ | 托管支付覆盖核心场景；聚合支付已覆盖下单、查询、关单、退款、对账主链路 |
| Python | pip `dg-sdk` | Python 3.x；本地 SDK classifier 只列到 3.7，实际项目需安装验证 | 聚合支付和托管支付核心场景已覆盖，当前 Skill 基线为 `dg-sdk 2.0.23` |
| C# | NuGet | .NET 4.8+ | 当前只保留入口说明 |
| Go | go mod | Go 1.16+ | 当前只保留入口说明 |

## 当前 Skill 包的真实覆盖范围

| 能力 | Java | PHP | Python | C# / Go |
| --- | --- | --- | --- | --- |
| 协议规则说明 | 完整 | 完整 | 完整 | 入口说明 |
| SDK / API 安装说明 | 完整 | 完整 | 完整 | 入口说明 |
| 初始化说明 | 完整 | 完整 | 完整 | 入口说明 |
| 请求头对齐策略 | 完整 | JSON 主链路可对齐；`CURLFile` multipart 缺失 Skill 来源头和网关版本头，阻断 | 完整；需显式配置 `jpt_x_skill_source`，`jpt-x-skill-huifu_id` 由请求 `huifu_id` 推导 | 需人工对照 |
| 聚合支付业务实现 | 完整 | 核心主链路覆盖 | 核心主链路覆盖 | 暂不提供 |
| 托管支付业务实现 | 完整 | 核心场景覆盖 | 核心场景覆盖 | 暂不提供 |

## 新增接口 SDK 兼容性

> `2026-06-11` 以 `docs/sdk` 最新 Java/PHP/Python SDK 源码核对。这里区分“独立场景 Request 类”和“通过共用 request 承载的场景化用法”。

| 新增接口 | Java SDK | PHP SDK | Python SDK | Skill 输出规则 |
| --- | --- | --- | --- | --- |
| 抖音直连下单 `pre_order_type=4` | 使用托管预下单 `V2TradeHostingPaymentPreorderH5Request`，设置 `pre_order_type=4`，`dy_data` 走 `extendInfo` | 使用托管预下单 `V2TradeHostingPaymentPreorderH5Request`，设置 `pre_order_type=4`，`dy_data` 走 `setExtendInfo(...)` / params | 使用托管预下单 `V2TradeHostingPaymentPreorderH5Request`，设置 `pre_order_type="4"`，`dy_data` 通过 `.post(extend_infos)` | 抖音直连是托管预下单场景，不是独立 SDK 类；不要生成 `Dypreorder` / `Douyin` 类，`dy_data` 必须是 JSON 字符串 |
| 拆单支付订单查询 `splitpay/query` | `V2TradeHostingPaymentSplitpayQueryRequest` | `V2TradeHostingPaymentSplitpayQueryRequest` | `V2TradeHostingPaymentSplitpayQueryRequest` | 三语言均可生成官方 request 类代码；字段为 `req_date`、`req_seq_id`、`huifu_id`、`org_req_date`、`org_req_seq_id`，不要用普通 `queryorderinfo` 替代 |

## 商户进件 SDK 证据

本节只记录随 1.3.2 本地核验的生产 SDK 源码事实，不替代官方文档的条件字段、权限、材料、响应枚举或联调验收。不得把 SDK 示例中的密钥、商户号、图片 URL、证件、银行卡、手机号或流水复制到 Skill。

商户进件生产/官方联调的来源值使用 `hfps/1.3.2` 或环境变量占位；不得把真实商户号、URL 或密钥写入示例。

| SDK | 已核验版本 | 五个 JSON 接口的可选 Request 类 | 图片 `file_url` 调用边界 |
| --- | --- | --- | --- |
| Java `dg-java-sdk` | `3.0.39` | `V2MerchantBasicdataEntRequest`、`V2MerchantBasicdataIndvRequest`、`V2MerchantBusiOpenRequest`、`V2MerchantBasicdataQueryRequest`、`V2MerchantBasicdataStatusQueryRequest` | `BasePayRequest.requestBasePay` 对 `v2/supplementary/picture` 走 SDK 特判的 multipart 文本字段；末参必须为 `isPage=true`。SDK 在该判断前完成 `data` 请求签名，因此请求签名保留；随后在响应验签前返回原始响应，因此响应验签跳过。`BasePay.debug` 默认 `true` 且会打印私钥和请求数据，必须在任何 SDK 请求前全局设为 `false`。当前 `MerConfig` 使用 `setProductId(...)`，不是 `setProcutId(...)`。 |
| PHP `huifurepo/dg-php-sdk` | `2.0.29` | 同名五个 `V2Merchant*Request` 类 | `BsPay::post("v2.supplementary.picture", params, "", "default")` 无本地文件时走 JSON。传 `CURLFile` 会进入 multipart 文件分支，该分支缺少 `jpt-x-skill-source`、`jpt-x-skill-huifu_id`、`jpt-sdk_version`，并关闭请求签名和响应验签；当前必须阻断，不能外推成“multipart 自动带 Skill 来源头”。 |
| Python `dg-sdk` / `dg_sdk` | `2.0.23` | 同名五个 `V2Merchant*Request` 类 | `dg_sdk.DGTools.request_post("/v2/supplementary/picture", params)` 无文件时走 JSON。`MerConfig` 第五参数是 `jpt_x_skill_source`，不是 `huifu_id`。 |

共同边界：五个 JSON 接口可选用专属 Request 类或经 SDK 通用入口调用，但业务侧仍须显式提供新的当天唯一 `req_date` / `req_seq_id`；Python 不会自动补齐它们。五个 JSON 接口默认会对请求 `data` 处理签名，并在同步响应包含 `sign` 时尝试验签；Java 图片 `file_url` 是明确例外，使用 `isPage=true` 保留请求签名但跳过响应验签。这些事实不证明图片响应的文件标识、服务端取 URL 成功、业务重试语义或进件回调协议。企业/个人进件没有 `data.huifu_id`：PHP `2.0.29` 会无保护读取缺失键，因此继续阻断对应 PHP 可运行代码；Python `2.0.23` 会发送空的 `jpt-x-skill-huifu_id`，只作 SDK 兼容性提示和联调/上线前验证，不单独阻断 Python 代码，也不让客户判断是否允许空头。任何语言都不得为埋点头污染业务报文或虚构 `data.huifu_id`；Java 条件头路径已核验可用。

本地二进制 `file` 模式不是跨语言通用能力：Java 有传输实现；PHP `CURLFile` multipart 分支缺少 Skill 埋点头并关闭请求签名和响应验签；Python 图片类字段与 Demo 不一致且关闭签名/验签。三语言都不得据此生成本地文件上传实现。

## 当前版本口径

| 项目 | 版本 |
| --- | --- |
| 托管支付 Java SDK | `dg-java-sdk 3.0.39` |
| 聚合支付 Java SDK | `dg-lightning-sdk 1.0.5` |
| PHP SDK 包 | `huifurepo/dg-php-sdk 2.0.29` |
| Python SDK 包 | `dg-sdk 2.0.23` |
| 前端 JS SDK | `@dg-elements/js-sdk`，项目锁定版本 |

## PHP 默认落地方式

PHP 场景默认使用官方 Composer 包 `huifurepo/dg-php-sdk`，业务入口优先采用：

- 聚合支付核心主链路：`BsPaySdk\core\Payment`
- 聚合对账与托管支付：`BsPayClient::postRequest()`
- request 类提供 `funcCode`
- `params` 数组承载实际业务字段（适用于 `postRequest()` 路径）

当前 Skill 包的 PHP SDK 包基线是 `2.0.29`，优先通过 Composer 安装或升级：

```bash
composer require "huifurepo/dg-php-sdk:^2.0.29"
composer update huifurepo/dg-php-sdk --with-all-dependencies
composer show huifurepo/dg-php-sdk
test -f vendor/huifurepo/dg-php-sdk/BsPaySdk/init.php
```

Composer 不可用时，可以使用 Packagist 元数据指向的 GitHub 分发包手动下载当前基线：

- `https://api.github.com/repos/huifurepo/bspay-php-sdk/zipball/refs/tags/2.0.29`
- 解压后设置 `HUIFU_SDK_ROOT=/absolute/path/to/BsPaySdk`
- 必须执行 `test -f "$HUIFU_SDK_ROOT/init.php"` 确认实际 SDK 路径

官方 PHP SDK 文档在 2026-04-24 直接校验时仍只列到 `v2.0.25`，且 `php-sdk_v2.0.25.7z` OSS 地址返回 404；不能用旧版本可访问链接静默替代当前 `2.0.29` 基线。

当前 Skill 包不再内置 PHP 模板资产或非官方自维护 client。

读取规则：

- 核对来源头时读 `references/shared-request-header-policy.md`
- 核对 API / `notify_url` 签名时读 `references/shared-signing-v2.md`
- 核对控台 Webhook 验签时读 `references/shared-webhook-signing.md`
- 需要确认官方 SDK 实现细节时，检查项目实际安装的 `huifurepo/dg-php-sdk` 源码
- 拆单支付订单查询可使用官方 `V2TradeHostingPaymentSplitpayQueryRequest`
- 抖音直连下单没有独立 PHP Request 类，使用托管预下单 request 承载 `pre_order_type=4`，不要生成不存在的 `Dypreorder` / `Douyin` 类
- 不要回到历史自维护 PHP client 方案

推荐使用方式：

1. 先读 `references/shared-request-header-policy.md`
2. 再读对应 `*-php-adapter.md` 和 `*-php-scenarios.md`
3. 聚合支付核心主链路优先 `BsPaySdk\core\Payment`；聚合对账与托管支付优先 `BsPayClient::postRequest()`
4. 初始化 `MerConfig` 时显式配置 `skill_source`；只对已核验的无文件 JSON 主链路说明 SDK 自动带出来源头，`CURLFile` multipart 路径必须阻断
5. 排查差异时先比对本地请求报文、签名串和官方 SDK 实际源码，不引入非官方 client

## Python 默认落地方式

Python 场景默认使用官方 pip 包 `dg-sdk`，代码中 import `dg_sdk`。

当前 Skill 包的 Python SDK 包基线是 `2.0.23`。输出可运行代码前必须验证：

```bash
python3 -m pip install "dg-sdk==2.0.23"
python3 -c "import dg_sdk; print(dg_sdk.DGClient.__version__)"
```

安装或版本核对失败时必须显式报错并停止；不要静默改成无版本 `pip install dg-sdk`，也不要降级。

生产环境变量清单见 `aggregation-python-adapter.md` 与 `hostingpay-python-adapter.md`；Python 示例统一固定 `DGClient.env = "prod"`，不再生成测试环境切换函数。

业务入口优先采用：

- 聚合支付核心主链路：`dg_sdk.Payment` + `Payment*Request`
- 聚合对账：`dg_sdk.V2TradeCheckFilequeryRequest().post({})`
- 托管支付：`dg_sdk.V2TradeHostingPayment*Request().post({})`
- 抖音直连下单没有独立 request 类，使用托管预下单 request；拆单支付订单查询已有官方 request 类。

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
- 托管支付 PHP 已有拆单支付订单查询 request 类；抖音直连使用托管预下单 request 承载
- PHP 受支持场景如果需要输出代码，必须体现官方 `huifurepo/dg-php-sdk`
- 聚合支付 Python 已覆盖下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- 托管支付 Python 已覆盖预下单、查询、关单、退款、退款查询、对账、拆单支付订单查询
- 托管支付 Python 抖音直连使用托管预下单 request 承载，当前没有独立抖音 request 类
- Python 受支持场景如果需要输出代码，必须体现官方 `dg-sdk` / `dg_sdk`
- Java 仍是聚合支付和托管支付的完整基线实现
