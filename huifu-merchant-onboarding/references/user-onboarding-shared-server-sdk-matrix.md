# 用户开户服务端 SDK 能力矩阵

## 版本基线

结论来自用户提供且由维护仓库锁定的本地 SDK 源码。类和 URI 的存在不证明官方分发来源、接口权限、材料条件、审核结果或通知协议。

| SDK | 版本 | 五接口专属类 | 生产结论 |
| --- | --- | --- | --- |
| Java `dg-java-sdk` | `3.0.40` | 已找到 | 使用官方 Request/Client；先关闭敏感调试 |
| PHP `huifurepo/dg-php-sdk` | `2.0.30` | 已找到 | 使用官方 Request/Client；DEBUG/Demo 入口仍需独立检查 |
| Python `dg-sdk` / `dg_sdk` | `2.0.24` | 已找到 | 使用官方 Request；仍需字段与网关探针 |

## 五个精确类与 URI

三语言均应只使用对应专属 Request，不得按后缀复用 merchant 类：

| Request 类 | URI |
| --- | --- |
| `V2UserBasicdataEntRequest` | `/v2/user/basicdata/ent` |
| `V2UserBasicdataIndvRequest` | `/v2/user/basicdata/indv` |
| `V2UserBusiOpenRequest` | `/v2/user/busi/open` |
| `V2UserApplyQueryRequest` | `/v2/user/apply/query` |
| `V2UserBasicdataQueryRequest` | `/v2/user/basicdata/query` |

共同要求：保留 SDK 请求签名和同步响应验签；显式传入业务流水和日期。SDK 连接重试不能解释成开户或入驻业务重试。

## 官方合同优先与运行探针

- 生成类可能把官方 `C` 字段建模成 required 或发送空字符串，例如开户有效期/国籍/地址、企业登录名以及业务入驻 `sign_user_info`。以官方 Y/N/C 和条件说明为准。
- `file_list`、`elec_card_list`、`resp_business`、公共返回 `data` 的来源类型曾冲突；wire 已由说明与接入方矩阵裁决，不要仅靠类属性名决定，也不得偏离 `user-onboarding-platform-contracts.md`。
- `sign_user_info` 官网类型为 Object，部分 SDK定义或序列化边界可能不同。使用 exact-key 扩展字段时必须保持键名，在脱敏运行探针中记录最终 JSON 类型、签名输入和网关结果。
- 探针不能绕过签名、验签、TLS 或敏感日志安全要求。

## 调试日志硬停

- Java `BasePay.debug` 默认 `true`，可能记录私钥、签名和请求数据。进程初始化、任何请求之前全局固定为 `false`，不得并发临时切换。
- PHP SDK 主配置默认可为 `DEBUG=false`，但官方 Demo/Composer 入口可能在 `BsPay::init` 前定义 `DEBUG=true`，进而记录含 RSA 私钥的配置、完整请求和响应。
- PHP 联调/生产不得加载启用 DEBUG 的 Demo loader；启动检查必须在加载 SDK 和初始化前拒绝 `DEBUG=true`，且不能被后续配置改回。

## 官方 SDK-only 传输规则

- 接入方确认官方 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24` SDK 不存在此前 Skill 推断的 TLS 问题；Java/PHP 不再因 TLS 硬停，五接口均使用各自官方 Request/Client。
- 保持 SDK/运行时正常的证书链和主机名校验，不设置 trust-all、`verify=false` 或关闭校验；TLS 作为共同上线检查，不阻断官方 SDK 代码生成。
- 禁止用 `HttpClient`、OkHttp、`HttpURLConnection`、Guzzle、`curl_*`、通用 POST 或自实现签名/验签客户端替代官方 SDK。三语言交付分别使用官方 SDK，不允许只让 Python 使用 SDK。

企业/个人开户的业务合同没有 `data.huifu_id`，请求 DTO 按官网字段生成，不增加合同外业务字段。
