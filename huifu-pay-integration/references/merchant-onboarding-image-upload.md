# 商户进件图片上传

## 目录

- 适用范围
- 已确认的请求合同
- `file_url` 模式：已核验的语言边界
- 公共请求头
- P0：仍需要官方确认
- 使用边界

## 适用范围

本文件处理商户进件材料的文件标识获取。官方来源：[图片上传](https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json)。只对已由当前生产 SDK 证实的 `file_url` 模式给出受控调用片段；本地二进制文件模式和回调不生成实现。

## 已确认的请求合同

- 官方 JSON 只给 URI `v2/supplementary/picture` 和元数据 `sign=true`，未给 HTTP method、host 或 Content-Type；当前 SDK 适配证据使用 POST，但不得把 POST 说成该 JSON 明示的合同。
- 官方 JSON 的九个可见请求路径（四个仅见于 `requestDemo` 的顶层路径和五个正式 `data` 参数）及其证据边界见 `merchant-onboarding-complete-field-catalog.md` 的“图片上传”；顶层 `file` 的类型、长度和必填性未给出，不得猜测。
- 文档的 `requestDemo` 含 `sys_id`、`product_id`、`data`、`file`，不含 `sign`；签名要求来自接口元数据的 `sign=true` 和 SDK 签名路径，不得从示例虚构 `sign` 字段或推断请求不签名。文件流字段名为顶层 `file`。
- `data` 必填 `req_seq_id:String(32)`、`req_date:String(8)`（`yyyyMMdd`）、`file_type:String(32)`；`huifu_id:String(18)` 和 `file_url:String(512)` 可选。完整字段路径见 `merchant-onboarding-complete-field-catalog.md`，高风险约束见 `merchant-onboarding-field-contracts.md`。
- `data.file_url` 与顶层 `file` 文件流互斥；未开户或未确认目标商户号时 `huifu_id` 可为空。仅在值已确认是本次目标 `huifu_id` 时传入。
- 官网明确 `huifu_id` 不支持填写“企业商户进件”或“个人商户进件”接口返回的用户号；必须确认手中标识确为本接口允许的直属商户 ID，不能看到 18 位标识就直接复用。
- 图片支持 JPG、BMP、PNG，单张最大 2MB；其他文件最大 10MB。`file_type` 必须按官方文件类型表和目标进件字段选择。
- 回答 `file_type`、目标材料类型或图片上传前置关系时必须同时读取 `merchant-onboarding-external-resources.md`，单列 `外部资料提示` 并给出文件类型表/图片上传文档的未经改写原始地址。官网 `file_url` 图片和请求中的占位图片 URL 只是示例，不复述原址，也不是外部资料或默认文件地址。

## `file_url` 模式：已核验的语言边界

官网只明确 `file_url` 与本地 `file` 不能同时上传，没有说明二者都空是否合法；不得把互斥改写成官网“必须二选一”。生成实际上传方案时，本 Skill 选择其中一个真实文件来源，没有来源则标 `[需要调用方补充]`。**本 Skill 安全策略**要求 URL 来自受控 HTTPS 对象存储并使用短时授权，且在业务层校验 scheme、允许 host、有效期和可访问性；不得直传任意用户 URL。URL、资料内容、请求流水和商户号均不得写入代码、日志或测试样例。

回答三语言 `file_url` 差异时必须同时保留四点：`file_url`/`file` 互斥且官网未说明二者都空是否合法、来源值使用 `hfps/1.3.2` 或环境变量占位、URL/密钥不落样例，以及不得猜测图片标识、重试或回调。

| 语言 / 已核验 SDK | 调用入口 | 实际传输形态 | 受控片段边界 |
| --- | --- | --- | --- |
| Java `dg-java-sdk 3.0.39` | `BasePayRequest.requestBasePay` | SDK 对该 URI 使用 multipart 文本字段，不是 JSON；`data` 仍由 SDK 签名 | 使用当前源码的 `setProductId(...)` 和显式 `"default"` merchant key；末参必须为 `isPage=true`：请求签名保留，响应验签跳过；SDK 的 `BasePay.debug` 默认是 `true`，必须在任何 SDK 请求前全局设为 `false` |
| PHP `php_v2.0.29` | `BsPay::post` | 无本地文件时使用 JSON | 当前 SDK 在来源头路径会读取 `huifu_id`；受控片段仅用于已确认 `huifu_id`，未开户的可选字段场景需官方/SDK 修复确认，不能用空值掩盖 |
| Python `dg_sdk 2.0.23` | `dg_sdk.DGTools.request_post` | 无本地文件时使用 JSON | `MerConfig` 第五参数只能是 `jpt_x_skill_source`；省略或传 `hfps/1.3.2`，不得填商户号；缺少可选 `huifu_id` 时的空埋点头仅作兼容性提示，不阻断 `file_url` 方案 |

## 公共请求头

- Java、PHP、Python 使用 Skill 调用时都要求 `jpt-x-skill-source: <skill_source>`。Java `file_url` 特判和 PHP/Python 无文件 JSON 主链路会在配置来源值后自动补该头；不得把这个结论外推到 PHP `CURLFile` multipart 文件分支。
- 当前请求 `data.huifu_id` 存在且非空时，还必须发送 `jpt-x-skill-huifu_id: <data.huifu_id>`；Java `file_url` 与 PHP/Python 无文件 JSON 主链路按当前基线从本次请求参数推导，禁止配置固定商户号。
- `huifu_id` 在本接口为可选。PHP `2.0.29` 在配置 `MerConfig.skill_source` 后会先直接读取请求参数中的 `huifu_id`；未开户且不传 `huifu_id` 时，PHP 可运行代码必须停在 SDK 修复/升级检查点，不能用虚构或空业务字段绕过。Python `2.0.23` 在字段缺失时会发送空的 `jpt-x-skill-huifu_id`；该行为只单列为 `SDK 兼容性提示`，不单独阻断 Python `file_url` 方案，也不得询问客户是否允许空头。保持业务报文不含虚构 `huifu_id`，联调若因该头失败再升级/修复 SDK。
- PHP `2.0.29` 传入 `CURLFile` 时进入 multipart 文件分支：该分支缺少 `jpt-x-skill-source`、`jpt-x-skill-huifu_id` 和 `jpt-sdk_version`，且 `BsPayClient` 同时关闭请求签名和响应验签。当前 SDK 不满足 Skill 埋点和签名要求，必须阻断本地文件可运行代码；不得声称 multipart 会自动携带 Skill 来源头，也不得改用手写 `curl` 绕过。

Java 受控片段（所有值由密钥管理和调用方提供）：SDK `3.0.39` 的 `BasePay.debug` 默认为 `true`，会向标准输出打印私钥、签名和包含 `file_url` / `huifu_id` 的请求数据。必须在进程初始化阶段、任何 SDK 请求之前全局关闭，且不得在并发请求中临时切换。

```java
import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.net.BasePayRequest;

// 进程初始化阶段执行一次，必须早于任何 SDK 请求。
BasePay.debug = false;

Map<String, Object> data = new HashMap<>();
data.put("req_seq_id", request.reqSeqId());
data.put("req_date", request.reqDate());
data.put("file_type", request.fileType());
if (request.huifuId() != null && !request.huifuId().isBlank()) data.put("huifu_id", request.huifuId());
data.put("file_url", request.controlledHttpsUrl());
Map<String, Object> result = BasePayRequest.requestBasePay(
    "v2/supplementary/picture", data, "default", true);
```

PHP 受控片段：

```php
use BsPaySdk\core\BsPay;

function uploadPictureFromControlledUrl(array $input) {
    if (empty($input['huifu_id'])) {
        throw new InvalidArgumentException('Current PHP SDK file_url path requires a confirmed huifu_id; confirm the unregistered-merchant path with Huifu.');
    }
    $params = [
        'req_seq_id' => $input['req_seq_id'],
        'req_date' => $input['req_date'],
        'file_type' => $input['file_type'],
        'file_url' => $input['controlled_https_url'],
    ];
    $params['huifu_id'] = $input['huifu_id'];
    return (new BsPay())->post('v2.supplementary.picture', $params, '', 'default');
}
```

Python 受控片段：

```python
from dg_sdk import DGTools

params = {
    "req_seq_id": request.req_seq_id,
    "req_date": request.req_date,
    "file_type": request.file_type,
    "file_url": request.controlled_https_url,
}
if request.huifu_id:
    params["huifu_id"] = request.huifu_id
result = DGTools.request_post("/v2/supplementary/picture", params)
```

这些片段只说明 SDK 调用入口和语言差异。Java `isPage=true` 不改变其前置的 `data` 请求签名，因而请求签名保留；SDK 会在解析并校验响应 `sign` 前直接返回原始响应，因而响应验签跳过。这里的 `isPage` 是 SDK 响应处理开关，不表示图片接口是页面支付。不得推断 `result` 中的文件标识，也不得根据同步受理结果继续提交进件。Python `2.0.23` 的底层客户端固定配置 `Retry(connect=3)`，这仅是连接建立层的 SDK 内置行为，不是已确认的接口幂等或业务重试语义；调用方不得再实现业务自动重试、重放或按该行为推断受理结果。

## P0：仍需要官方确认

下列内容没有可核验的官方 SDK 或联调样本时，必须标记 `[需要官方确认]`，不得生成本地二进制上传、手写签名/验签、业务重试或回调实现：

- 本地二进制 `file` 路径的 `Content-Type`、boundary 与 `data` 序列化方式。
- PHP `CURLFile` 路径已确认缺失 Skill 埋点头并关闭请求签名和响应验签，因此直接阻断；Java/Python 本地文件路径的签名原文及跨语言兼容结论仍需官方确认。
- 成功响应内文件标识的确切字段名、失败码和幂等/重试语义。

接受脱敏样本时，样本不得包含真实图片、图片 URL、身份证、银行卡、手机号、密钥或生产流水。

## 使用边界

- 进件的图片类字段只填写本接口实际、已验签响应返回的文件标识；不传本地路径、base64、原图或臆造 `file_id`。
- SDK 生成的旧 Demo 若同时传 `file_url` 和本地文件，视为与官方互斥合同冲突的反例，不得复制。
- 图片上传失败、响应字段不明或协议未确认时，停止进件请求组装，转官方 SDK/联调验证；日志只保留脱敏关联号和不可逆摘要。
