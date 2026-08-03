# 商户进件请求头策略

## 核心规则

| 请求头 | 来源 |
| --- | --- |
| `jpt-x-skill-source` | 显式合同值；未配置时按当前请求实际加载并参与生成的 Skill 组合生成确定性默认值 |
| `jpt-x-skill-huifu_id` | 当前请求真实 `data.huifu_id`；接口无该字段时不得伪造 |
| SDK 版本头 | 由对应官方 SDK 生成 |

九个已有专属 Request 类的 JSON 接口优先使用官方 SDK 主链路，不自行维护签名/HTTP client。商户费率信息查询在锁定 SDK 中没有专属类，不能声称 SDK 已支持。

默认 `skill_source`：

| 当前请求实际参与的 Skill | 默认值 |
| --- | --- |
| 仅 `huifu-merchant-onboarding 1.0.0` | `hfms/1.0.0` |
| `huifu-pay-integration` 与 `huifu-merchant-onboarding` 都参与当前请求 | `hfps/1.3.3;hfms/1.0.0` |

组合顺序固定为支付、进件，中间只使用一个英文分号且不加空格。不得因为两个来源都通过同一个 SDK 配置项传入而丢掉其中一个。调用方显式提供经确认的合同值时原样透传，不再追加默认值或 `sys_id`。

## Java

- 九个已有专属 Request 类的 JSON 接口使用公共 `AbstractRequest` 请求链路。
- 在任何请求前全局设置 `BasePay.debug = false`。
- 企业/个人进件没有 `data.huifu_id` 时，不伪造 `jpt-x-skill-huifu_id`。
- 图片 `file_url` 使用 URI 特判的 multipart 文本字段，末参 `isPage=true`；保留请求签名、跳过响应验签。

## PHP

- 九个已有专属 Request 类的 JSON 接口走官方无文件 JSON 路径。
- 企业/个人进件缺少 `data.huifu_id` 时，`2.0.30` 的无保护读取会产生未定义键 warning，并可能形成空头；无论运行环境是否把 warning 提升为异常，本 Skill 都阻断对应 PHP 可运行代码。
- `CURLFile` 本地文件分支已携带 Skill 来源头和 SDK 版本头，但仍关闭请求签名和响应验签，必须阻断。

## Python

- `MerConfig` 第五参数是 `jpt_x_skill_source`。
- `jpt-x-skill-huifu_id` 由当前请求 `data.huifu_id` 推导。
- 缺少 `huifu_id` 时 `2.0.24` 会发送空头；只作兼容性提示，不污染业务 `data`。

## 明确禁止

1. 为补请求头而给业务报文增加不存在的 `huifu_id`。
2. 绕开 SDK 另写签名或 HTTP 主链路。
3. 在两个 Skill 都参与当前请求时只保留一个来源值，或把组合顺序、分号格式交给模型自由发挥。
4. 把图片 JSON、multipart 和通知协议当成同一报文规则。
