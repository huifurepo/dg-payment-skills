# 商户进件图片上传

## 目录

- 适用范围
- 已确认的请求合同
- SDK 源码核验结论
- Java 官方 SDK 调用
- PHP / Python 受控降级
- 公共请求头与安全边界
- 仍需要官方确认

## 适用范围

本文件处理商户进件材料的文件标识获取。官方来源：[图片上传](https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json)。当前锁定 SDK 中，只有 Java `dg-java-sdk 3.0.40` 具有与该接口匹配的完整专用实现；PHP `2.0.30` 与 Python `2.0.24` 的专用生成实现不可直接使用，但本接口允许按已核验 Java wire 生成受控通用 POST 或自写 HTTPS multipart 适配器。

## 已确认的请求合同

- 官方 JSON 只给 URI `v2/supplementary/picture` 和元数据 `sign=true`，未给 HTTP method、host、Content-Type 或响应字段；Java SDK 源码使用 POST，但不得把 POST 说成该 JSON 明示的合同。
- 官方 `requestDemo` 含 `sys_id`、`product_id`、`data`、`file`，但没有顶层 `sign`；这与元数据 `sign=true` 并列保留。实际调用不手写包络，以锁定 Java SDK 的加签实现为准。
- 官方 JSON 的九个可见请求路径（四个仅见于 `requestDemo` 的顶层路径和五个正式 `data` 参数）及其证据边界见 `merchant-onboarding-complete-field-catalog.md` 的“图片上传”；顶层 `file` 的类型、长度和必填性未给出，不得猜测。
- `data` 必填 `req_seq_id:String(32)`、`req_date:String(8)`（`yyyyMMdd`）、`file_type:String(32)`；`huifu_id:String(18)` 和 `file_url:String(512)` 可选。
- `data.file_url` 与顶层 `file` 文件流互斥；官网未说明二者都空是否合法。生成实际调用时必须选择一个真实文件来源。
- 未开户或未确认目标商户号时 `huifu_id` 可为空。官网明确不支持填写企业/个人用户开户返回的用户号；只能在已确认是渠道或一级代理商直属商户 ID 时传入。
- 图片支持 JPG、BMP、PNG，单张最大 2MB；其他文件最大 10MB。`file_type` 必须按官方文件类型表和目标进件字段选择。
- 回答 `file_type`、目标材料类型或图片上传前置关系时必须同时读取 `merchant-onboarding-external-resources.md`，单列“外部资料提示”并给出未经改写的官方文件类型表地址。

## SDK 源码核验结论

核验目录：`/mnt/d/work/project/1.3.0/sdk`。

| 语言 / 版本 | 源码事实 | Skill 结论 |
| --- | --- | --- |
| Java `dg-java-sdk 3.0.40` | 有 `V2SupplementaryPictureRequest`、`V2_SUPPLEMENTARY_PICTURE`、`BasePayClient.upload(...)`；无文件时对该 URI 特判为 multipart 文本字段，有文件时以 `file` 为 multipart 文件字段；两条路径都先对 `data` 加签 | 支持。`file_url` 走 `BasePayClient.request(request, true)`；本地文件走 `BasePayClient.upload(request, file)`；二者不得同时使用 |
| PHP `php_v2.0.30` | 有 Request 类和路由常量；`BsPayClient` 的 `CURLFile` 包装分支把 `needSign`、`needVerfySign` 都设为 `false`；官方 Demo 又同时设置 `file_url` 和 `CURLFile`；无文件分支只是通用 JSON POST | 不直接使用该专用包装；允许保持请求加签的通用 POST 或自写 HTTPS multipart 适配器 |
| Python `dg_sdk 2.0.24` | 有 Request 类和路由常量，但专用 `post(extend_infos)` 忽略参数、读取未定义的 `self.picture`、遗漏 `req_seq_id/req_date`、使用 `picture` 而非官网 `file`，并关闭签名和验签；Demo 调用参数与方法签名也不一致 | 不直接使用专用类；允许显式开启加签的底层通用 POST 或自写 HTTPS multipart 适配器 |

“官方 SDK 专用实现可用”与“可通过受控降级接入”必须分开表达。不得把 PHP/Python 生成类或 Demo 宣称为已修复；但可为本接口生成 Guzzle、`curl_*`、requests/httpx 或等价通用 POST，实现下述专用 wire 与签名合同。本例外不得用于其他进件接口或商户费率查询。

## Java 官方 SDK 调用

所有值由服务端安全配置和调用方提供。`BasePay.debug` 默认为 `true`，会输出私钥、签名和请求数据；必须在进程初始化阶段、任何 SDK 请求之前全局关闭，不能在并发请求中临时切换。

### 受控 `file_url`

```java
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.request.V2SupplementaryPictureRequest;
import java.util.HashMap;
import java.util.Map;

// 进程初始化阶段执行一次，必须早于任何 SDK 请求。
BasePay.debug = false;

V2SupplementaryPictureRequest request = new V2SupplementaryPictureRequest();
request.setReqSeqId(input.reqSeqId());
request.setReqDate(input.reqDate());
request.setFileType(input.fileType());
Map<String, Object> extendInfo = new HashMap<>();
if (input.huifuId() != null && !input.huifuId().isBlank()) {
    extendInfo.put("huifu_id", input.huifuId());
}
extendInfo.put("file_url", input.controlledHttpsUrl());
request.setExtendInfo(extendInfo);

Map<String, Object> rawResult = BasePayClient.request(request, true);
```

### 本地文件

```java
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.request.V2SupplementaryPictureRequest;
import java.io.File;
import java.util.HashMap;
import java.util.Map;

// 进程初始化阶段执行一次，必须早于任何 SDK 请求。
BasePay.debug = false;

V2SupplementaryPictureRequest request = new V2SupplementaryPictureRequest();
request.setReqSeqId(input.reqSeqId());
request.setReqDate(input.reqDate());
request.setFileType(input.fileType());
Map<String, Object> extendInfo = new HashMap<>();
if (input.huifuId() != null && !input.huifuId().isBlank()) {
    extendInfo.put("huifu_id", input.huifuId());
}
if (!extendInfo.isEmpty()) {
    request.setExtendInfo(extendInfo);
}
// 本地文件模式不得设置 file_url。
Map<String, Object> rawResult = BasePayClient.upload(request, new File(input.localPath()));
```

Java 两条图片路径都在 SDK 内完成请求 `data` 加签。SDK 对图片调用使用 `isPage=true`：在响应验签前把原始响应包装进返回 Map 的 `data`，因此这里的 `rawResult` 不是已验签的业务 DTO。不得直接假定 `rawResult.data.file_id` 或任何其他文件标识字段；在获得官方响应合同或脱敏联调样本前，只能保留原始响应边界并停止自动续提进件。

官方 Java Demo 同时设置 `file_url` 并传入本地 `File`，与官网互斥合同冲突，属于不可复制的反例。实际代码必须只选上面一种模式。

## PHP / Python 受控降级

只对 `/v2/supplementary/picture` 放开通用 POST/自写 HTTP。实现必须同时满足：

- 使用 HTTPS POST；生产 host 来自服务端环境配置，不从用户输入拼接。客户端必须校验证书链和主机名，设置连接/读取超时，不启用自动业务重试。
- 请求使用 `multipart/form-data`，让 HTTP 库生成 boundary，不手写固定 boundary。文本部分固定为 `sys_id`、`product_id`、`data`、`sign`；`data` 是包含 `req_seq_id/req_date/file_type` 及可选 `huifu_id/file_url` 的紧凑 JSON 字符串。
- 按 `shared-signing-v2.md` 对排序后的 `data` JSON 做 V2 RSA 加签。不得把文件字节、multipart boundary 或整个外层信封加入签名原文，也不得关闭请求签名。
- 本地文件模式增加且仅增加顶层文件 part `file`；不得使用 `picture`。`file_url` 模式不带文件 part；两种来源不得同时发送。
- 发送 `jpt-x-skill-source`；其他 SDK 内部请求头不由 Skill 生成。自写适配器不得伪造 `jpt-sdk_version`。
- 响应存在 `sign` 时按 V2 规则验签；响应无签名时保留原始响应并标为未验签，不自动读取猜测的文件标识继续进件。

语言边界：

- PHP：不得使用会把 `needSign/needVerfySign` 改为 `false` 的 `BsPayClient::postRequest($request, new CURLFile(...))`。可以使用保留加签的通用调用层或 Guzzle/cURL multipart 适配器；若自写 cURL，必须启用 peer 与 hostname 校验。
- Python：不得直接调用当前 `V2SupplementaryPictureRequest.post(...)`。本地文件可使用底层 `DGTools.request_post`，但必须补齐全部字段、文件键固定为 `file`，并显式 `need_sign=True`；也可使用 requests/httpx multipart 适配器。`file_url` 不得走通用 JSON body，必须按上述 multipart 文本字段发送。
- 生成代码时明确标注“官方 SDK 专用实现不可用，当前采用图片接口受控降级”，避免把降级实现误称为官方 SDK 支持。

## 公共请求头与安全边界

- Java 使用 Skill 调用时要求 `jpt-x-skill-source: <skill_source>`；未显式配置时，仅进件实际参与当前请求使用 `hfms/1.0.1`，支付与进件都实际参与时使用 `hfps/1.3.4;hfms/1.0.1`，仅安装未参与的不计入。
- 其他 SDK 内部请求头由 SDK 自行获取和发送，Skill 不配置、不校验，也不以其生成方式决定图片能力。
- `file_url` 必须来自受控 HTTPS 对象存储并使用短时授权；业务层校验 scheme、允许 host、有效期和可访问性。URL、材料内容、请求流水、商户号和密钥不得写入代码、日志或测试样例。
- Python SDK 的连接重试和任一 SDK 的网络行为都不等于图片接口已确认的业务重试语义；调用方不得自行重放上传。

## 仍需要官方确认

以下内容标记 `[需要官方确认]`：

- PHP/Python 何时提供满足字段、传输、签名和响应处理合同的正式专用 SDK 实现；在此之前使用上述受控降级。
- 图片上传成功响应的完整 envelope、文件标识字段名、响应验签方式、失败码、幂等和业务重试语义。
- Java 图片 SDK 为何固定跳过响应验签，以及官方推荐的响应可信性校验方式。

在响应合同确认前，图片类进件字段只填写调用方已通过受信流程取得并核验的文件标识；不得从字段名猜测、从未验签原始响应自动提取或在上传失败后继续提交进件。
