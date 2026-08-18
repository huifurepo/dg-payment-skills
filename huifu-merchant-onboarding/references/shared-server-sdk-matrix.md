# 商户进件服务端 SDK 能力矩阵

## 目录

- [版本基线](#版本基线)
- [九个已有专属类的 JSON 接口](#九个已有专属类的-json-接口)
- [费率查询缺口](#费率查询缺口)
- [图片上传](#图片上传)
- [调试日志硬停](#调试日志硬停)
- [官方 SDK-first 与图片例外](#官方-sdk-first-与图片例外)
- [语言边界](#语言边界)

## 版本基线

版本、类与路由来自用户提供的 SDK 源码目录，并由官方 Maven/Packagist 分发信息和接入方确认补充。维护仓库中的历史源码摘要只用于复现类与路由证据，不得再从未验证生产制品的局部 HTTP 实现推导 TLS 硬停。

| SDK | 核验版本 | 结论 |
| --- | --- | --- |
| Java `dg-java-sdk` | `3.0.40` | 九个 JSON Request 类可用；图片接口有专用 Request、URI 特判和 `upload(...)` 入口 |
| PHP `huifurepo/dg-php-sdk` | `2.0.30` | 九个 JSON Request 类可用；图片生成产物存在，但没有满足合同的可用调用路径 |
| Python `dg-sdk` / `dg_sdk` | `2.0.24` | 九个 JSON Request 模块可用；图片生成产物存在实现缺陷，不可用 |

## 九个已有专属类的 JSON 接口

三语言均包含以下 Request：

- `V2MerchantBasicdataEntRequest`
- `V2MerchantBasicdataIndvRequest`
- `V2MerchantBusiOpenRequest`
- `V2MerchantBasicdataQueryRequest`
- `V2MerchantBasicdataStatusQueryRequest`
- `V2MerchantBusiModifyRequest`
- `V2MerchantBasicdataModifyRequest`
- `V2MerchantBusiModifyBusistatusRequest`
- `V2MerchantBasicdataSmsSendRequest`

共同规则：

- 只使用官方 Request/SDK 主链路；不得为了提供三语言等价产物改走手写 HTTP+签名客户端。
- 业务侧提供当天唯一的 `req_date/req_seq_id`。
- 请求 `data` 保留签名；同步响应有 `sign` 时验签。
- SDK 类存在不证明接口权限、材料条件或审核结果。

## 费率查询缺口

三语言锁定 SDK 中均未找到 `/v2/merchant/fee-rate/query` 的专属 Request 类或路由常量。不得声称 SDK 已覆盖商户费率信息查询，也不得用支付费率、详情查询或名称相近的类替代。字段解释仍读取 `merchant-onboarding-rate-query.md` 与完整字段目录；可运行代码等待新版官方 SDK 或官方通用调用证据。

## 图片上传

| 语言 | `file_url` | 本地文件 | 总结论 |
| --- | --- | --- | --- |
| Java | `BasePayClient.request(request, true)`；图片 URI 特判为 multipart 文本字段 | `BasePayClient.upload(request, file)`；multipart 文件字段为 `file` | 支持；两种来源互斥，请求签名保留，响应验签跳过 |
| PHP | 无文件分支只是通用 JSON POST，不能直接用于 `file_url` | `BsPayClient` 的 `CURLFile` 包装分支关闭请求签名和响应验签；Demo 同时传互斥来源 | 官方专用实现不可用；允许符合图片 wire 的通用 POST/自写 HTTPS multipart 降级 |
| Python | 无文件 `DGTools.request_post` 是 JSON，不能直接用于 `file_url` | 专用 Request 忽略扩展参数、漏字段、使用错误文件键、关闭签验，Demo 方法签名不匹配；底层通用 POST 可显式开启加签并传 `file` | 官方专用实现不可用；允许符合图片 wire 的底层通用 POST/自写 HTTPS multipart 降级 |

图片能力结论必须区分“官方专用 SDK 支持”和“受控降级可实现”。单独存在 `V2SupplementaryPictureRequest`、路由常量或通用 POST 方法不算前者；PHP/Python 可使用后者，但只能用于 `/v2/supplementary/picture`，并严格保持 multipart、`data` 加签、互斥、TLS 和响应信任边界。

## 调试日志硬停

- Java `BasePay.debug` 默认 `true`，会输出私钥、签名和请求数据；必须在进程初始化阶段、任何请求前全局设置为 `false`，且不得并发临时切换。
- PHP SDK 自带 `init.php` 默认 `DEBUG=false`，但官方 `BsPayDemo/loader.php` 和 `Composer/BsPayConfig.php` 会在 SDK 初始化前定义 `DEBUG=true`。开启后 `BsPayRequestV2` 会记录含 `rsa_merch_private_key` 的 `MerConfig`、完整请求体与完整响应。
- PHP 联调/生产必须在加载 SDK、Demo/Composer 配置和调用 `BsPay::init` 之前固定 `DEBUG=false`；不得使用 Demo loader，启动检查必须拒绝已被定义为 `true` 的进程。不能证明时停止生成可运行实现。

## 官方 SDK-first 与图片例外

- 接入方确认官方 Java `3.0.40`、PHP `2.0.30` 和 Python `2.0.24` SDK 不存在此前 Skill 推断的 TLS 问题；Java/PHP 不再触发 TLS 硬停，按官方 Request/Client 生成真实调用。
- 保持 SDK 与运行时的正常证书链、对端和主机名校验，禁止 trust-all、`verify=false` 或关闭校验。这是共同上线检查，不是 Java/PHP 专属阻断。
- 常规接口不得用 `HttpClient`、OkHttp、`HttpURLConnection`、Guzzle、`curl_*`、通用 POST 包装或自实现签名/验签客户端替代官方 SDK，即使任务只称“技术链路验证”。唯一例外是 `/v2/supplementary/picture` 的 PHP/Python 受控降级；该例外必须满足图片专项 multipart、`data` 加签、TLS 与日志合同，Java 仍使用官方 SDK。
- 多语言任务分别使用三种官方 SDK；不得只让 Python 用 SDK，再为 Java/PHP 生成手写客户端。

## 语言边界

- 企业/个人进件没有 `data.huifu_id`。
- SDK 连接重试不是进件业务重试；未知业务重试语义标记 `[需要官方确认]`。
- 图片响应文件标识、服务端拉取 URL 的结果和通知协议仍需官方确认。
