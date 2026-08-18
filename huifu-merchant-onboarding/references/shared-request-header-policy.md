# 商户进件请求头策略

## 核心规则

| 请求头 | 来源 |
| --- | --- |
| `jpt-x-skill-source` | 显式合同值；未配置时按当前请求实际加载并参与生成的 Skill 组合生成确定性默认值 |
| SDK 版本头 | 由对应官方 SDK 生成 |

商户九个与用户五个已有专属 Request 类的 JSON 接口优先使用官方 SDK 主链路，不自行维护签名/HTTP client。商户费率信息查询在锁定 SDK 中没有专属类，不能声称 SDK 已支持。

默认 `skill_source`：

| 当前请求实际参与的 Skill | 默认值 |
| --- | --- |
| 仅 `huifu-merchant-onboarding 1.0.1`，无论使用商户还是用户接口 | `hfms/1.0.1` |
| `huifu-pay-integration` 与 `huifu-merchant-onboarding` 都参与当前请求 | `hfps/1.3.4;hfms/1.0.1` |

组合顺序固定为支付、进件，中间只使用一个英文分号且不加空格。不得因为两个来源都通过同一个 SDK 配置项传入而丢掉其中一个。调用方显式提供经确认的合同值时原样透传，不再追加默认值或 `sys_id`。

## Java

- 商户九个与用户五个已有专属 Request 类的 JSON 接口使用公共请求链路，并按 `/v2/merchant/*`、`/v2/user/*` 精确隔离。
- 在任何请求前全局设置 `BasePay.debug = false`。
- 图片 `file_url` 使用 `BasePayClient.request(request, true)` 和 URI 特判的 multipart 文本字段；本地文件使用 `BasePayClient.upload(request, file)`。两种来源互斥，均保留请求签名、跳过响应验签。

## PHP

- 商户九个与用户五个已有专属 Request 类的 JSON 接口走官方无文件 JSON 路径。
- 不直接使用 `BsPayClient::postRequest($request, new CURLFile(...))`：该包装层关闭请求签名和响应验签。
- 图片接口允许使用保持 `data` 加签的通用 POST 或自写 HTTPS multipart 适配器；`file_url` 模式也必须发 multipart 文本字段，不能照搬无文件 JSON 分支。

## Python

- `MerConfig` 第五参数是 `jpt_x_skill_source`。
- 图片专用 Request 存在字段、文件键、签验和方法签名缺陷，不能直接调用。底层 `DGTools.request_post` 仅在显式 `need_sign=True`、补齐官网字段并使用顶层 `file` multipart 键时可用于本地文件模式；`file_url` 模式使用符合相同 multipart 合同的通用 POST/自写 HTTPS 适配器。

## 明确禁止

1. 除 `/v2/supplementary/picture` 的 PHP/Python 受控降级外，绕开 SDK 另写签名或 HTTP 主链路。
2. 在两个 Skill 都参与当前请求时只保留一个来源值，或把组合顺序、分号格式交给模型自由发挥。
3. 把图片 JSON、multipart 和通知协议当成同一报文规则。
