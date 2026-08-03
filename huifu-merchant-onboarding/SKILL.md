---
name: huifu-merchant-onboarding
description: "汇付商户进件与开户管理：用于企业/个人商户进件或开户、图片上传、商户业务开通、业务开通修改、基本信息修改、费率查询、商户状态变更、短信验证、商户详情、申请状态及进件通知；不用于支付下单、查单、关单、退款、对账、checkout-js 或支付终态，这些任务使用 huifu-pay-integration。"
---

# 汇付商户进件

## 版权声明

本 Skill 中的汇付商户进件资料整理自上海汇付支付有限公司官方开放平台与官方产品文档；原始文档及其更新维护权归汇付支付官方所有。仅作技术学习交流与接口集成辅助使用，详见 `references/shared-copyright-notice.md`。

## 执行流程

1. 确认主体类型、`sys_id` 主体角色、目标接口、接入阶段、技术栈和是否要求可运行代码。完成标准：这些维度均已唯一确定，未确定项已明确列出。
2. 检查下方硬检查点；命中时停止生成实现，只问一个最高优先级问题。完成标准：已记录命中或未命中的具体理由，且 `upper_huifu_id` 判断与 `sys_id` 主体角色一致。
3. 按精确路由读取 2–5 份 reference。完成标准：完整 DTO、响应或嵌套字段任务必须同时包含对应原子接口页、完整字段目录和字段合同，其他任务不加载无关接口页。
4. 字段回答必须从完整字段目录和字段合同取值，同时核对类型、长度、Y/N/C、枚举、默认值、条件、互斥和外部资料。完成标准：每个输出字段均能追溯到完整路径、方向和全部适用约束。
5. 输出请求、同步响应、异步通知和未知协议边界；不得把查询响应复制成开通请求。完成标准：四类边界已分开，所有未知项均标记 `[需要官方确认]`。

本 Skill 只处理商户进件。支付下单、查单、关单、退款、对账、checkout-js 和支付终态使用 `$huifu-pay-integration`；不要从本 Skill 读取支付实现文档。

## 精确路由

| 场景 | 最小 reference 集 |
| --- | --- |
| 进件能力总览 | `references/shared-overview.md`、`references/merchant-onboarding-field-contracts.md` |
| 企业商户进件 | `references/merchant-onboarding-enterprise.md`、`references/merchant-onboarding-field-contracts.md` |
| 无执照个人商户进件 | `references/merchant-onboarding-individual.md`、`references/merchant-onboarding-field-contracts.md` |
| 图片上传或文件标识 | `references/merchant-onboarding-image-upload.md`、`references/merchant-onboarding-field-contracts.md` |
| 首次业务开通，或补开银行卡、银联等仍由 `/busi/open` 承载的能力 | `references/merchant-onboarding-business-open.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户详细信息查询 | `references/merchant-onboarding-detail-query.md`、`references/merchant-onboarding-field-contracts.md` |
| 申请单状态查询 | `references/merchant-onboarding-application-status-query.md`、`references/merchant-onboarding-field-contracts.md` |
| 微信/支付宝补开，线上业务开通，或已开通能力的参数、费率修改 | `references/merchant-onboarding-business-open-modify.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户基本信息修改 | `references/merchant-onboarding-basic-info-modify.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户费率信息查询 | `references/merchant-onboarding-rate-query.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户状态开通或关闭 | `references/merchant-onboarding-status-change.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户短信发送或验证码核实 | `references/merchant-onboarding-sms-send.md`、`references/merchant-onboarding-field-contracts.md` |
| 完整 DTO、完整响应或嵌套字段 | 按上表目标接口选择对应原子接口页，再读 `references/merchant-onboarding-complete-field-catalog.md`、`references/merchant-onboarding-field-contracts.md` |
| 字段说明命中网页、编码表、XLSX 或协议 | 上一行基础上补 `references/merchant-onboarding-external-resources.md` |
| 九个已有专属类的 JSON 接口 SDK | `references/shared-server-sdk-matrix.md`、`references/merchant-onboarding-field-contracts.md` |
| 费率查询 SDK 可用性 | `references/merchant-onboarding-rate-query.md`、`references/shared-server-sdk-matrix.md` |
| `file_url` 三语言差异 | `references/merchant-onboarding-image-upload.md`、`references/shared-server-sdk-matrix.md` |
| 请求头、`huifu_id` 和 `skill_source` | `references/shared-request-header-policy.md` |
| 签名、验签和凭据 | `references/shared-signing-v2.md`、`references/shared-credential-boundary.md` |
| 审核、逐业务或电子协议通知 | 对应原子接口页；输出前执行“未知通知边界自检” |
| 权限、状态延迟、补资料或通道配置 FAQ | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` |
| 错误码 | `references/merchant-onboarding-error-codes.md` |
| 基础编码、公共参数或名词解释 | `references/merchant-onboarding-external-resources.md`、`references/merchant-onboarding-error-codes.md`；具体字段仍补对应原子接口页 |
| 版本与升级 | `references/skill-version-policy.md` |

只说“补开”时，先同时确认具体能力/渠道和当前开通状态；不得只按“是否完成首次开通”猜选接口。锁定官方规则至少包括：银行卡、银联业务开通仍走 `/v2/merchant/busi/open`；微信、支付宝补开走 `/v2/merchant/busi/modify`。其他能力必须读取两个原子页和完整字段目录后按官方适用范围判断。

## 字段完整性规则

- 当前官方冻结来源日期为 `2026-07-29`。
- 十一接口字段路径数量为 `177 / 129 / 442 / 9 / 559 / 93 / 434 / 199 / 35 / 14 / 20`，合计 `2,111`。
- 字段方向合计为 1,218 个请求、713 个同步响应和 180 个通知节点。
- `2026-07-29` 抓取中，企业进件新增请求 `material_card_info` 及 6 个子字段，其他十页与 `2026-07-28` 快照逐字节一致；官网页面自身仍标最近更新时间 `2026.07.28`。此前刷新还将企业进件三项门店图片从无条件 `Y` 改为 `C`，并统一说明 `scene_type` 含线下场景时必填；详情响应新增自己的 `material_card_info` 及 6 个子字段。
- 父对象也计入路径；数组按官方 `Array/jsonArray` 定义判断，不按 `*_list` 名称猜测。唯一已登记例外是业务开通修改逐业务通知的 `reg_result_list`：官网误拼为 `josnArray`，且同一行明确“集合可能有多条数据”，因此保留 `async.business.reg_result_list[]`；不得把该例外外推到其他 `_list` 字段。
- 不得按叶字段名去重。企业、个人进件及基本信息修改中的 `request.data.prov_id/area_id` 是经营省市，`request.data.card_info.prov_id/area_id` 是结算卡省市；企业进件还新增 `request.data.material_card_info.prov_id/area_id` 作为补充对公同名账户，详情响应另有 `response.data.material_card_info.prov_id/area_id`。适用时各完整父路径分别生成，不能合并或提升。`card_info` 是 String(JSON)；`material_card_info` 的官网类型列虽为 Object，本项目已确认以“jsonObject字符串”说明为准，request/response wire 均按 String(JSON Object) 整体序列化或反序列化，类型列差异只作为官网勘误保留。
- 详情响应的 `response.data.material_card_info.prov_id/area_id` 又是一组独立的银行省市路径；先反序列化 `response.data.material_card_info` 字符串，再只在该父对象内解析，不能与响应顶层或其他卡列表中的同名字段合并。
- 官网示例值不是默认值。没有本地约束的字段标记 `[需要官方确认]` 并停止赋值。
- 企业进件和详情查询的股东列表分别包含 `request.data.share_holder_info_list[].mobile_no` 和 `response.data.share_holder_info_list[].mobile_no`。
- 详情查询的 `online_flag/quick_flag/withhold_flag=1/0` 只用于解析；业务开通请求对应字段只能使用字符串 `Y/N`。
- 命中字段说明中的外部文档或文件时，单列“外部资料提示”，给出完整字段路径、触发条件和未经改写的原始地址；官网只给相对地址时，同时给出相对原文与按已登记官方文档命名空间（无例外时按来源页）解析后的绝对地址，不能把解析结果冒充原文。未读取正文时要求人工核验；回调、跳转、下载、二维码或图片裸 URL 示例不是资料或默认值。

## 🔴 CHECKPOINT · HARD STOP

命中以下任一情况时，首行输出 `🔴 CHECKPOINT · HARD STOP：硬检查点。`，列出当前判断和本轮 references，只问一个最高优先级问题：

1. 要生成企业、个人商户的可运行请求，但主体类型未确认。
2. 要生成联调或生产请求，但 `sys_id`、`product_id`、`sys_id` 主体角色、真实材料来源或 RSA 密钥安全来源未确认；仅当 `sys_id` 主体为渠道商时，还必须确认真实 `upper_huifu_id`，总部商户主体可按官网合同省略。未显式配置 `skill_source` 时使用下述确定性默认值，不因此硬停。
3. 要实现本地图片文件流上传，但 multipart 字段、签名原文或响应协议仍未获得官方样本。
4. 要实现审核、逐业务或电子协议通知，但外层包装、验签原文、ACK、HTTP、超时或重试协议未确认。
5. 本地 SDK 源码与官方文档在请求头、签名、版本或字段上冲突。
6. 用户要求 Java 或 PHP 联调/生产可运行代码，但锁定的通用 Java `3.0.40` 或 PHP `2.0.30` 仍关闭 TLS 证书链、对端或主机名校验；在经批准的安全制品通过源码和错证书、过期证书、错域名测试前不得输出可上线实现。
7. 用户要求 PHP 联调或生产可运行代码，但不能证明在加载 SDK、Demo/Composer 配置和调用 `BsPay::init` 之前已将全局 `DEBUG` 固定为 `false`，或仍使用会定义 `DEBUG=true` 的官方 Demo/Composer 入口。

纯字段解释、状态分层、详情/申请状态查询和已确认的 `file_url` 安全边界不因材料缺失而硬停。

## SDK 与图片安全边界

- Java 九个已有专属 Request 类的 JSON 接口使用公共 `AbstractRequest`，保留请求签名和同步响应验签。
- Java `3.0.40` 的公共 HTTP 客户端安装信任所有证书的 `X509TrustManager`，且 `HostnameVerifier` 恒返回 `true`；关闭调试日志不能修复 TLS，联调和生产代码必须硬停。
- Java `BasePay.debug` 默认为 `true`，会记录私钥、签名和请求数据；必须在进程初始化阶段、任何请求之前全局设为 `false`，不得并发临时切换。
- Java 图片 `file_url` 使用 `isPage=true`：保留请求签名，跳过响应验签。
- PHP 九个已有专属 Request 类的 JSON 接口走官方无文件 JSON 路径；缺少 `data.huifu_id` 时不得直接执行未保护的头部取值。
- PHP `2.0.30` 的 SDK 默认 `DEBUG=false`，但官方 `BsPayDemo/loader.php` 和 `Composer/BsPayConfig.php` 会在初始化前启用 `DEBUG=true`。调试开启时 SDK 会记录含 RSA 私钥的 `MerConfig`、完整请求体和完整响应；联调/生产必须在加载这些入口与 `BsPay::init` 前固定 `DEBUG=false`，不得使用 Demo loader，且启动检查不能允许它被后续配置改回 `true`。
- PHP `2.0.30` 的公共请求路径设置 `CURLOPT_SSL_VERIFYPEER=false`，且没有可证明的 `CURLOPT_SSL_VERIFYHOST=2`；在实际安装源码通过传输安全检查前，九个 JSON 接口同样不得输出联调或生产可运行代码。
- PHP `CURLFile` 路径在 `2.0.30` 已携带 Skill 请求头，但仍关闭请求签名和响应验签，必须阻断。
- Python 九个已有专属 Request 类的 JSON 接口使用对应 request 模块；缺少 `huifu_id` 时 SDK 会发送空头，只作兼容性提示，不伪造 `data.huifu_id`。
- 商户费率信息查询在锁定的三语言 SDK 中没有专属路由或 Request 类；不得声称 SDK 已支持或用相似类替代。
- Python SDK 的连接重试不能当成进件业务重试。

## 未知通知边界自检

交付通知方案前必须保留：

“逐业务通知外层包装待官方样本确认。审核和电子协议回调的 ACK、验签原文、HTTP 语义、超时和重试均为 `[需要官方确认]`，不得外推或生成回调实现。”

不得套用支付 `notify_url` 或控台 Webhook 的规则。

## 请求、凭据和日志

- 保留调用方已经提供的 `req_date`、`req_seq_id`、申请单号和商户号；缺失或非法时报错。
- 私钥、身份证、银行卡、手机号和图片资料不得写入前端、日志、仓库或回答示例。
- `jpt-x-skill-huifu_id` 仅来自该接口真实 `data.huifu_id`；没有时不伪造。
- 未显式配置 `skill_source` 时，按当前请求实际加载并参与生成的 Skill 集合取值：仅本 Skill 使用 `hfms/1.0.0`；支付与进件两个 Skill 都参与当前请求时使用 `hfps/1.3.3;hfms/1.0.0`。仅安装在仓库但未参与当前请求不计入；顺序固定为支付、进件，使用一个英文分号且不加空格，不得去重掉任一已参与 Skill。
- 调用方显式提供经确认的 `skill_source` 合同值时原样透传；不得再追加 `sys_id`，也不得把来源头写进业务 `data`。

## 输出要求

回答至少包含：

1. 主体类型、目标接口、阶段和技术栈。
2. 本轮实际使用的 references。
3. 请求、同步响应、通知方向和字段来源。
4. 未确认协议、外部资料和人工确认项。
5. 需要继续进入支付交易时，明确交接给 `$huifu-pay-integration`。

## 当前版本

| 项目 | 口径 |
| --- | --- |
| Skill 版本 | `1.0.0` |
| 官方来源快照 | `2026-07-29`，十一接口共 2,111 个字段路径 |
| Java SDK 证据基线 | `3.0.40` |
| PHP SDK 证据基线 | `2.0.30` |
| Python SDK 证据基线 | `2.0.24` |
| 本地沙箱 | 不提供进件沙箱端点 |
