# 商户进件服务端 SDK 能力矩阵

## 目录

- [版本基线](#版本基线)
- [九个已有专属类的 JSON 接口](#九个已有专属类的-json-接口)
- [费率查询缺口](#费率查询缺口)
- [图片上传](#图片上传)
- [调试日志硬停](#调试日志硬停)
- [传输安全硬停](#传输安全硬停)
- [语言边界](#语言边界)

## 版本基线

以下结论来自用户提供的 SDK 源码目录；维护仓库另行锁定三棵源码树摘要并执行编译/加载检查，该证据文件不随 Skill 包发布。官方分发 URL、tag 或提交未提供，因此不能把该证据表述为“官方发布来源已验证”。

| SDK | 核验版本 | 结论 |
| --- | --- | --- |
| Java `dg-java-sdk` | `3.0.40` | 九个 JSON Request 类可用；图片 `file_url` 有 URI 特判 |
| PHP `huifurepo/dg-php-sdk` | `2.0.30` | 九个 JSON Request 类可用；本地 `CURLFile` 路径仍因关闭签名/验签而阻断 |
| Python `dg-sdk` / `dg_sdk` | `2.0.24` | 九个 JSON Request 模块可用；无文件图片走 `DGTools.request_post` |

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

- 使用官方 Request/SDK 主链路。
- 业务侧提供当天唯一的 `req_date/req_seq_id`。
- 请求 `data` 保留签名；同步响应有 `sign` 时验签。
- SDK 类存在不证明接口权限、材料条件或审核结果。

## 费率查询缺口

三语言锁定 SDK 中均未找到 `/v2/merchant/fee-rate/query` 的专属 Request 类或路由常量。不得声称 SDK 已覆盖商户费率信息查询，也不得用支付费率、详情查询或名称相近的类替代。字段解释仍读取 `merchant-onboarding-rate-query.md` 与完整字段目录；可运行代码等待新版官方 SDK 或官方通用调用证据。

## 图片上传

| 语言 | `file_url` | 本地文件 |
| --- | --- | --- |
| Java | 图片 URI 特判；末参 `isPage=true`；请求签名保留、响应验签跳过 | 有传输实现，但跨语言合同未确认，不生成通用实现 |
| PHP | 无文件时 JSON 路径可调用 | `CURLFile` 分支已携带 Skill 头，但关闭签名/验签，阻断 |
| Python | 无文件 `file_url` 使用通用 `DGTools.request_post`，默认请求签名和响应验签 | 专用 `V2SupplementaryPictureRequest` 仅本地文件，显式 `need_sign=False, need_verfy_sign=False`，且内部 `picture` 与官网 `file` 不一致，阻断 |

## 调试日志硬停

- Java `BasePay.debug` 默认 `true`，会输出私钥、签名和请求数据；必须在进程初始化阶段、任何请求前全局设置为 `false`，且不得并发临时切换。
- PHP SDK 自带 `init.php` 默认 `DEBUG=false`，但官方 `BsPayDemo/loader.php` 和 `Composer/BsPayConfig.php` 会在 SDK 初始化前定义 `DEBUG=true`。开启后 `BsPayRequestV2` 会记录含 `rsa_merch_private_key` 的 `MerConfig`、完整请求体与完整响应。
- PHP 联调/生产必须在加载 SDK、Demo/Composer 配置和调用 `BsPay::init` 之前固定 `DEBUG=false`；不得使用 Demo loader，启动检查必须拒绝已被定义为 `true` 的进程。不能证明时停止生成可运行实现。

## 传输安全硬停

- 锁定的通用 Java `3.0.40` 在公共 `HttpClientUtils` 中安装信任所有证书的 `X509TrustManager`，并让 `HostnameVerifier.verify()` 恒返回 `true`。`BasePay.debug=false` 只处理敏感日志，不能修复 TLS。
- 锁定的 PHP `2.0.30` 在公共 `BsPayRequestV2.php` 中设置 `CURLOPT_SSL_VERIFYPEER=false`，且当前源码没有可证明的 `CURLOPT_SSL_VERIFYHOST=2`。
- 上述公共传输路径同时承载九个进件 JSON Request。未取得启用证书链和主机名校验的官方安全制品或经批准传输层，并通过错证书、过期证书和错域名拒绝测试前，只能解释字段、Request 类和升级条件；不得生成 Java/PHP 联调或生产可运行代码，也不得用手写 HTTP、信任所有证书或关闭校验绕过。

## 语言边界

- 企业/个人进件没有 `data.huifu_id`。
- PHP `2.0.30` 会无保护读取缺失键，产生 warning/空头风险；无论 warning 是否升级为异常，都阻断对应 PHP 可运行代码。
- Python `2.0.24` 会发送空的 `jpt-x-skill-huifu_id`，只作兼容性提示，不要求客户判断，也不伪造字段。
- SDK 连接重试不是进件业务重试；未知业务重试语义标记 `[需要官方确认]`。
- 图片响应文件标识、服务端拉取 URL 的结果和通知协议仍需官方确认。
