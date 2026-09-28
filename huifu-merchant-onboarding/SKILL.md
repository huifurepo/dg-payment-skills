---
name: huifu-merchant-onboarding
description: "汇付支付/斗拱支付（Huifu Payment）商户进件、开户、KYC 与商户管理（Merchant Onboarding）。用于企业、个体工商户、小微商户或无执照个人的入驻、入网和实名认证，以及营业执照、法人、结算卡、股东、联系人、门店等资料和图片上传，涉及 file_url、file_id、huifu_id、apply_no 或 upper_huifu_id 的请求；也用于企业用户或个人用户开户、用户业务入驻、用户申请单状态和用户信息查询，以及微信、支付宝、银联、银行卡、快捷、网银、分账、代扣、余额、预授权、补贴、合单等业务的开通、补开、业务开通修改或配置修改，以及商户资料、基本信息修改、商户详情、结算信息、费率查询、申请状态、审核、实名、绑卡、电子协议和商户状态变更。支持完整字段/DTO/响应、必填条件、类型长度、枚举、Java/PHP/Python SDK、请求头、签名验签、短信验证、权限、补资料、状态延迟，以及审核、业务和电子协议通知排障。实际支付下单、查单、关单、退款、对账、收银台组件 checkout-js、支付通知或支付终态使用 huifu-pay-integration；开户开通后继续发起支付的端到端请求同时使用 huifu-merchant-onboarding 和 huifu-pay-integration。"
---

# 汇付商户进件、用户开户与入驻

## 版权声明

本 Skill 中的汇付商户进件资料整理自上海汇付支付有限公司官方开放平台与官方产品文档；原始文档及其更新维护权归汇付支付官方所有。仅作技术学习交流与接口集成辅助使用，详见 `references/shared-copyright-notice.md`。

## 执行流程

1. 先确认目标实体是支付商户还是分账/结算用户，再确认企业/个人、`sys_id` 主体角色、目标接口、接入阶段、技术栈和是否要求可运行代码。完成标准：这些维度均已唯一确定，未确定项已明确列出。
2. 区分下方开发提示与硬检查点；官网字段/协议疑义及本地 PHP TLS 风险只提醒，不触发硬检查点。其他硬检查点命中时，只暂停受影响的请求部分并问一个最高优先级问题，继续不依赖该问题的工作；`upper_huifu_id` 判断与 `sys_id` 主体角色一致，常规接口三语言真实调用仍使用对应官方 SDK，仅 PHP/Python 图片上传适用下述受控降级例外。
3. 按精确路由读取 2–5 份 reference。完成标准：完整 DTO、响应或嵌套字段任务必须同时包含对应原子接口页、完整字段目录和字段合同，其他任务不加载无关接口页。
4. 字段回答必须从完整字段目录和字段合同取值，同时核对类型、长度、Y/N/C、枚举、默认值、条件、互斥和外部资料。完成标准：每个输出字段均能追溯到完整路径、方向和全部适用约束。
5. 输出请求、同步响应、异步通知和未知协议边界；不得把查询响应复制成开通请求。完成标准：四类边界已分开，未知项标记 `[需要官方确认]` 并说明文档核对/咨询途径，继续已明确部分，用 TODO/待填配置隔离未明确部分。

本 Skill 同时处理 `/v2/merchant/*` 商户进件与 `/v2/user/*` 分账/结算用户开户，但两套 DTO、ID 角色、状态和响应模型必须隔离。支付下单、查单、关单、退款、对账、checkout-js 和支付终态使用 `$huifu-pay-integration`；不要从本 Skill 读取支付实现文档。

## 精确路由

| 场景 | 最小 reference 集 |
| --- | --- |
| 进件能力总览 | `references/shared-overview.md`、`references/merchant-onboarding-field-contracts.md` |
| 用户开户能力总览和用户/商户边界 | `references/user-onboarding-shared-overview.md`、`references/user-onboarding-field-contracts.md` |
| 企业商户进件 | `references/merchant-onboarding-enterprise.md`、`references/merchant-onboarding-field-contracts.md` |
| 无执照个人商户进件 | `references/merchant-onboarding-individual.md`、`references/merchant-onboarding-field-contracts.md` |
| 图片上传或文件标识 | `references/merchant-onboarding-image-upload.md`、`references/merchant-onboarding-field-contracts.md` |
| 首次业务开通，或补开银行卡、银联等仍由 `/busi/open` 承载的能力 | `references/merchant-onboarding-business-open.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户详细信息查询 | `references/merchant-onboarding-detail-query.md`、`references/merchant-onboarding-field-contracts.md` |
| 申请单状态查询 | `references/merchant-onboarding-application-status-query.md`、`references/merchant-onboarding-field-contracts.md` |
| 微信/支付宝/抖音补开，线上业务开通，或已开通能力的参数、费率修改 | `references/merchant-onboarding-business-open-modify.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户基本信息修改 | `references/merchant-onboarding-basic-info-modify.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户费率信息查询 | `references/merchant-onboarding-rate-query.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户状态开通或关闭 | `references/merchant-onboarding-status-change.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户短信发送或验证码核实 | `references/merchant-onboarding-sms-send.md`、`references/merchant-onboarding-field-contracts.md` |
| 商户多费率配置或修改微信/支付宝场景底价 | `references/merchant-onboarding-multifee-config.md`、`references/merchant-onboarding-field-contracts.md` |
| 查询商户多费率配置或按 `fee_sign` 定位配置 | `references/merchant-onboarding-multifee-query.md`、`references/merchant-onboarding-field-contracts.md` |
| 企业用户开户 | `references/user-onboarding-enterprise.md`、`references/user-onboarding-field-contracts.md` |
| 企业用户基本信息修改 | `references/user-onboarding-enterprise-modify.md`、`references/user-onboarding-field-contracts.md` |
| 个人用户开户 | `references/user-onboarding-individual.md`、`references/user-onboarding-field-contracts.md` |
| 个人用户基本信息修改 | `references/user-onboarding-individual-modify.md`、`references/user-onboarding-field-contracts.md` |
| 用户业务入驻 | `references/user-onboarding-business-open.md`、`references/user-onboarding-field-contracts.md`、`references/user-onboarding-platform-contracts.md` |
| 用户业务入驻修改 | `references/user-onboarding-business-modify.md`、`references/user-onboarding-field-contracts.md`、`references/user-onboarding-platform-contracts.md` |
| 用户列表查询 | `references/user-onboarding-list-query.md`、`references/user-onboarding-field-contracts.md`、`references/user-onboarding-platform-contracts.md` |
| 用户非同名对公结算卡申请状态 | `references/user-onboarding-application-status-query.md`、`references/user-onboarding-field-contracts.md` |
| 用户基本信息和业务配置查询 | `references/user-onboarding-detail-query.md`、`references/user-onboarding-field-contracts.md` |
| 电子合同重发 | `references/onboarding-electronic-contract-resend.md`、`references/onboarding-extension-field-contracts.md` |
| 电子合同列表查询 | `references/onboarding-electronic-contract-list-query.md`、`references/onboarding-extension-field-contracts.md` |
| 电子合同拒签 | `references/onboarding-electronic-contract-reject.md`、`references/onboarding-extension-field-contracts.md` |
| 开通下级商户权限配置 | `references/merchant-onboarding-lower-merchant-permission.md`、`references/onboarding-extension-field-contracts.md` |
| 商户统一进件页面跳转 | `references/merchant-onboarding-unified-web.md`、`references/onboarding-extension-field-contracts.md` |
| 统一进件页面版查询 | `references/merchant-onboarding-unified-web-query.md`、`references/onboarding-extension-field-contracts.md` |
| 微信商户配置或配置查询 | `references/merchant-onboarding-wechat-config.md` 或 `references/merchant-onboarding-wechat-config-query.md`、`references/onboarding-extension-field-contracts.md` |
| 微信实名认证或状态查询 | `references/merchant-onboarding-wechat-realname.md` 或 `references/merchant-onboarding-wechat-realname-query.md`、`references/onboarding-extension-field-contracts.md` |
| 支付宝实名申请或申请单查询 | `references/merchant-onboarding-alipay-realname.md` 或 `references/merchant-onboarding-alipay-realname-query.md`、`references/onboarding-extension-field-contracts.md` |
| 完整商户 DTO、响应或嵌套字段 | 商户原子页、`references/merchant-onboarding-complete-field-catalog.md`、`references/merchant-onboarding-field-contracts.md` |
| 完整用户 DTO、响应或嵌套字段 | 用户原子页、`references/user-onboarding-complete-field-catalog.md`、`references/user-onboarding-field-contracts.md` |
| 完整扩展接口 DTO、响应或嵌套字段 | 扩展原子页、`references/onboarding-extension-complete-field-catalog.md`、`references/onboarding-extension-field-contracts.md` |
| 字段说明命中网页、编码表、XLSX 或协议 | 上一行基础上补 `references/merchant-onboarding-external-resources.md` |
| 用户字段命中地区、MCC、证件、银行或文件编码 | 用户原子页、`references/user-onboarding-external-resources.md` |
| 扩展接口字段命中签名、返回码、渠道号、地区、图片或微信第三方资料 | 扩展原子页、`references/onboarding-extension-external-resources.md` |
| 商户十一个已有专属类的 JSON 接口 SDK | `references/shared-server-sdk-matrix.md`、`references/merchant-onboarding-field-contracts.md` |
| 九个用户接口 SDK | `references/user-onboarding-shared-server-sdk-matrix.md`、用户原子页 |
| 十二个扩展接口的 SDK 能力与降级边界 | `references/onboarding-extension-shared-server-sdk-matrix.md`、扩展原子页 |
| 费率查询 SDK 可用性 | `references/merchant-onboarding-rate-query.md`、`references/shared-server-sdk-matrix.md` |
| 图片上传 SDK 可用性与语言差异 | `references/merchant-onboarding-image-upload.md`、`references/shared-server-sdk-matrix.md` |
| `skill_source` 与 SDK 请求头边界 | `references/shared-request-header-policy.md` |
| 用户接口请求字段保真与 `skill_source` | `references/user-onboarding-shared-request-field-preservation.md`、`references/shared-request-header-policy.md` |
| 签名、验签和凭据 | `references/shared-signing-v2.md`、`references/shared-credential-boundary.md` |
| 用户接口 wire、公共参数、凭据、加验签和异步通知 | `references/user-onboarding-platform-contracts.md`、`references/user-onboarding-shared-signing-v2.md`、`references/user-onboarding-shared-credential-boundary.md` |
| 审核、逐业务或电子协议通知 | 对应原子接口页；输出前执行“未知通知边界自检” |
| 权限、状态延迟、补资料或通道配置 FAQ | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` |
| 错误码 | `references/merchant-onboarding-error-codes.md` |
| 用户接口错误、权限、状态延迟或补资料排查 | `references/user-onboarding-error-codes.md`、`references/user-onboarding-faq.md`、`references/user-onboarding-copilot-troubleshooting-playbooks.md` |
| 基础编码、公共参数或名词解释 | `references/merchant-onboarding-external-resources.md`、`references/merchant-onboarding-error-codes.md`；具体字段仍补对应原子接口页 |
| 版本与升级 | `references/skill-version-policy.md` |
| 用户接口来源、冲突与回归 | `references/user-onboarding-official-service-source-index.md`、`references/user-onboarding-canonical-regression-prompts.md` |
| 扩展能力总览 | `references/onboarding-extension-shared-overview.md`、`references/onboarding-extension-field-contracts.md` |
| 扩展接口来源、外部资料、官方冲突与回归 | `references/onboarding-extension-official-service-source-index.md`、`references/onboarding-extension-external-resources.md`、`references/onboarding-extension-canonical-regression-prompts.md` |

只说“补开”时，先同时确认具体能力/渠道和当前开通状态；不得只按“是否完成首次开通”猜选接口。锁定官方规则至少包括：银行卡、银联业务开通仍走 `/v2/merchant/busi/open`；微信、支付宝、抖音补开走 `/v2/merchant/busi/modify`。其他能力必须读取两个原子页和完整字段目录后按官方适用范围判断。

## 字段完整性规则

- 当前商户十三接口官方冻结来源日期为 `2026-09-22`；历史快照保持不可变，本轮在线复审有十页原文字节变化。
- 十三接口字段路径数量为 `177 / 129 / 460 / 9 / 578 / 93 / 452 / 199 / 35 / 14 / 20 / 27 / 17`，合计 `2,210`。
- 字段方向合计为 1,277 个请求、753 个同步响应和 180 个通知节点；完整路径对比新增82、删除79、同路径属性变化194，不能把容器路径变化误当成全部新增业务字段。
- `2026-08-10` 复审中，企业进件、个人进件和基本信息修改页的官网更新时间变为 `2026.08.07`；三页仅将 `activated_products` 的说明补全为 `01：一体化收款产品，02：账户与资金产品，03：业财数通产品`，字段、类型、长度、必填性和嵌套均未变化。此前企业进件新增的 `material_card_info` 七个路径、线下场景门店图片条件及详情响应同名路径继续保留。
- 父对象也计入路径；数组按官方 `Array/Array<string>/jsonArray` 定义判断，不按 `*_list` 名称猜测。业务开通修改逐业务通知 `reg_result_list` 本轮正式类型已为 Array，即使说明仍误拼 `josnArray` 也有正式类型依据保留 `[]`。`wx_zl_pay_conf_list:String(512)` 未明确对象/数组形态，不得仅按名称推断。
- 不得按叶字段名去重。企业、个人进件及基本信息修改中的 `request.data.prov_id/area_id` 是经营省市，`request.data.card_info.prov_id/area_id` 是结算卡省市；企业进件还包含 `request.data.material_card_info.prov_id/area_id` 作为补充对公同名账户，详情响应另有 `response.data.material_card_info.prov_id/area_id`。适用时各完整父路径分别生成，不能合并或提升。当前官网已将此前多处 `Object` 类型列修正为 `String`；`card_info` 与 `material_card_info` 都按 String(JSON Object) 整体序列化或反序列化。
- 详情响应的 `response.data.material_card_info.prov_id/area_id` 又是一组独立的银行省市路径；先反序列化 `response.data.material_card_info` 字符串，再只在该父对象内解析，不能与响应顶层或其他卡列表中的同名字段合并。
- 官网示例值不是默认值。没有本地约束的字段标记 `[需要官方确认]`，不猜值；可保留 TODO/待填配置，继续其他字段和业务框架，并提示开发者核对对应文档。
- 当前十三页官网仍有未填写说明或标量长度的字段。完整目录以 `—` 原样保留；不得根据字段中文名、同名路径、SDK 类型或示例补写，生成严格 DTO 前标记 `[需要官方确认]`。
- 商户多费率配置的 `wx_conf_list/ali_conf_list` 为 `String/jsonArray格式`，请求路径保留 `[]`，wire 各发送一层 String(JSON Array)。响应 `conf_list:String/jsonArray格式` 已明确按数组解码并保留 `[]`。`pay_way` 当前只允许 `A=支付宝/W=微信`。
- 商户多费率配置查询的可选 `fee_sign:String(32) N` 由 exact-key 扩展传入；官网未定义省略后的精确返回范围、数量或分页语义，不得承诺返回全部配置。响应 `conf_list` 同样按 String(JSON Array) 解码。
- 业务开通、业务开通修改和详情查询保留抖音配置及完整子路径；费率查询 `fee_rate_type:Array<string>(117) N` 本轮已明确为原生字符串数组，不再序列化成字符串。企业进件 `material_card_info` 为 Y 但正文仍附条件；其请求支行长度8与同请求12位示例冲突。详情响应长度12是独立方向合同，不与请求共用长度；新增 `fee_rate_file_list` 必须区分开通和修改的完整父路径。
- 企业进件和详情查询的股东列表分别包含 `request.data.share_holder_info_list[].mobile_no` 和 `response.data.share_holder_info_list[].mobile_no`。
- 详情查询的 `online_flag/quick_flag/withhold_flag=1/0` 只用于解析；业务开通请求对应字段只能使用字符串 `Y/N`。
- 命中字段说明中的外部文档或文件时，单列“外部资料提示”，给出完整字段路径、触发条件和未经改写的原始地址；官网只给相对地址时，同时给出相对原文与按已登记官方文档命名空间（无例外时按来源页）解析后的绝对地址，不能把解析结果冒充原文。未读取正文时要求人工核验；回调、跳转、下载、二维码或图片裸 URL 示例不是资料或默认值。

### 用户开户与维护接口

- 用户接口活动快照为 `2026-09-22`；字段路径为 `43 / 34 / 136 / 15 / 165 / 37 / 26 / 138 / 17`，合计611，其中请求333、同步响应220、异步通知58。与商户目录合计2,821个字段路径，但两个目录必须分别校验，不能按叶字段名合并。
- 九页官网都把外层 `response.data` 标为 `N`；业务入驻修改仍为 String，其余为 Json。用户列表查询的 `user_list_info_list` 当前为 String/jsonArray格式，按 String(JSON Array) 解码；成功示例却使用原生数组，必须保留冲突。成功缺失按协议异常，网关或异常响应 DTO 仍允许父节点整体缺失。
- `C` 统一按条件必填执行。个人用户只允许 `card_type=1`，企业用户按条件允许 `0/1/2/4`；合法 `card_info` 中 `card_name` 必填，e账户卡 `mp` 在 `card_type=1` 时要求、`card_type=0` 时不要求。
- String(JSON) 必须按 `user-onboarding-platform-contracts.md` 的完整路径矩阵逐层编码/解码；不得把嵌套对象全部扁平化、把原生 Object 变成字符串或对 String(JSON) 二次序列化。
- 用户九页中四页原文字节变化，新增57个路径、同路径属性变化6项。`account_level` 支持 LV1/LV2/LV3，LV3 仅企业；`balance_pay_config/account_recharge_config/delay_pay_config` 请求为 String(JSON)，查询这三组及 `account_info` 为 Object，异步 `account_info` 也是 Object。余额/充值收费两字段 Y 与“至少一个”仍冲突；账户验证及实名链接未声明的行为不得推断。用户目录已没有长度为空的标量叶字段，结构父节点空长度和原文空说明仍保留 `—`。完整条件与 wire 见用户字段合同和平台合同。
- 企业/个人用户开户、企业/个人用户基本信息修改、用户申请状态和用户详情没有官方异步方向；用户业务入驻及其修改接口声明异步通知。
- 领域层必须区分表示用户号的 `userHuifuId` 与表示商户号的 `merchantHuifuId`。用户开户返回的 ID 不能写入图片上传 `data.huifu_id`；图片上传该字段只支持直属商户号。

## 🔴 CHECKPOINT · HARD STOP

命中以下任一情况时，首行输出 `🔴 CHECKPOINT · HARD STOP：硬检查点。`，列出当前判断和本轮 references，只问一个最高优先级问题：

1. 用户说“开户、进件、业务开通或查状态”但未确认目标是支付商户还是分账/结算用户，或企业/个人主体未确认。
2. 要生成联调或生产请求，但 `sys_id`、`product_id`、`sys_id` 主体角色、真实材料来源或 RSA 密钥安全来源未确认；仅当 `sys_id` 主体为渠道商时，还必须确认真实 `upper_huifu_id`，总部商户主体可按官网合同省略。未显式配置 `skill_source` 时使用下述确定性默认值，不因此硬停。
3. 要生成 PHP/Python 图片上传可运行代码，但无法保持 `/v2/supplementary/picture` 的专用 multipart 信封、`data` 加签、`file_url/file` 互斥或敏感日志边界。仅因使用通用 POST 或自写 HTTP 传输适配器不再硬停；本地SDK的TLS现状另作非阻断提示。
4. 要把用户开户返回的 `userHuifuId` 写入图片上传 `data.huifu_id`。
5. 用户要求 PHP 联调或生产可运行代码，但不能证明在加载 SDK、Demo/Composer 配置和调用 `BsPay::init` 之前已将全局 `DEBUG` 固定为 `false`，或仍使用会定义 `DEBUG=true` 的官方 Demo/Composer 入口。

纯字段解释、状态分层、详情/申请状态查询、图片 SDK 能力说明、Java 官方图片调用及满足图片专用合同的 PHP/Python 受控降级实现不硬停。

## 开发提示：待确认项不阻断

- 商户、用户及十二个扩展接口的字段、类型、长度、条件、示例、SDK/文档差异或通知协议尚不清楚时，列出完整路径、具体疑点和对应官方文档地址，提醒开发者核对；仍不了解或不清楚时，可咨询汇付官方或汇付开发者交流沟通群，不虚构群号或邀请链接。
- `[需要官方确认]` 是开发提醒，不是硬检查点，也不要求先取得官方答复才能继续所有开发。可以继续已明确的官方 SDK 调用、请求结构、DTO、业务框架和测试，将未明确部分隔离为 TODO、待填配置或独立适配点；不猜字段含义、默认值或协议，不自动选取冲突的一方。
- 未明确的审核/电子协议通知可提供处理框架与待补参数清单，明确 ACK、签验原文等适配点，不编造最终协议；用户业务入驻已有明确公共通知合同的部分照常实现。
- 本地 PHP `2.0.31` 的已知 TLS 风险暂作非阻断提醒，不要求修复证明或安全传输证据后才继续开发/联调代码生成。保留源码事实，不声称已修复，不自动修改 SDK 或关闭校验。
- 明确非法输入、错误实体ID、验签失败、凭据泄露与未经授权的真实操作仍保留原有保护；开发占位不是把未知值直接发送到真实接口的依据。

## 官方 SDK-first 与图片例外

用户接口遵循 `user-onboarding-shared-server-sdk-matrix.md` 的官方 SDK-only 传输规则；下述图片上传是唯一受控例外。

- Python 当前 SDK 为 `2.0.28`，版本和行为以用户提供的 `../sdk/dg_sdk-2.0.28/dg_sdk/` 源码为准；构造器、请求头、路由和图片边界已复核，不代表远端包可下载或真实网关联调成功。项目使用其他版本时核对实际安装源码，未明确差异留 TODO 并继续已明确部分；不清楚时可咨询汇付官方或汇付开发者交流沟通群，不设整体开发前置确认要求。
- `2026-09-24` 本地 SDK 复核：通用Java/Python主链路保留默认TLS校验；PHP `2.0.31` 仍设置 `CURLOPT_SSL_VERIFYPEER=false`。API 来源仍为 `2026-09-22`。该事实按上方开发提示非阻断说明，不作为继续使用官方 SDK 开发的前置门槛。
- Java `dg-java-sdk 3.0.41`、PHP `huifurepo/dg-php-sdk 2.0.31`、Python `dg-sdk 2.0.28` 的常规接口真实请求都使用官方 Request/Client 入口。官方 SDK 自带的通用调用入口（如 Java `BasePayClient.request(Map, funcCode, ...)`，内部把 `funcCode` 的 `.` 替换为 `/` 拼接 URL，并复用同一签名、验签、请求头与 TLS 链路）同样属于官方主链路，可用于 SDK 没有专属 Request/路由的常规接口，不限于图片接口，也不属于受控降级。唯一例外是 `/v2/supplementary/picture`：PHP/Python 的专用生成实现不可用时，可生成通用 POST 或自写 HTTP 传输适配器，但必须严格复刻图片专项 reference 的 multipart、签名、TLS 和日志合同；该例外限制的是离开官方 SDK 的手写实现，不得把例外扩散到其他接口。
- 生成的业务代码不新增trust-all、`verify=false` 或关闭TLS校验的设置，也不自动修改用户SDK；指定SDK已有TLS问题仅作提醒，不因此停止实现或要求修复证明。
- SDK 没有专属 Request/路由时，或虽有生成类/路由但实现不符合接口合同时，明确报告 SDK 能力差异；不得仅凭类名或路由常量宣称官方 SDK 已有专属支持。此时可经官方 SDK 通用调用入口生成可运行代码；因无类型化封装兜底，字段名、类型、长度、必填和 String(JSON) 编码必须逐项对照字段合同构造。商户费率查询仍禁止手写 HTTP；PHP/Python 图片上传按上述唯一例外允许受控降级。
- 多语言任务逐语言使用对应官方 SDK；一种语言成功不用于复制或反推另一语言的 DTO、wire 或签名实现。

## SDK 与图片安全边界

以下 Python 能力结论对应本地 `2.0.28` 实际源码；升级版本号并不代表图片实现缺陷已修复。

- Java的商户十一个已有专属Request类使用公共 `AbstractRequest` 合同，用户九个专属Request类沿用各语言公共骨架。扩展中九个商户/AT路由有专属Request；三个电子合同最新路由为 `/v2/agreement/elect/signurl/resend`、`/v2/agreement/apply/list`、`/v2/agreement/elect/rejectsign`，本地三SDK无匹配专属类，使用官方通用入口并保留签验。新增的 `V2Invoice*` 类仍指向旧invoice路由，不得作为新接口替代，也不得手写生产HTTP。
- Java `BasePay.debug` 默认为 `true`，会记录私钥、签名和请求数据；必须在进程初始化阶段、任何请求之前全局设为 `false`，不得并发临时切换。
- 当前锁定版本只有 Java 图片上传专用实现可用：`file_url` 使用官方 `BasePayClient.request(request, true)`，本地文件使用 `BasePayClient.upload(request, file)`；两种来源互斥。两条路径均保留请求签名，`isPage=true` 会在响应验签前返回原始响应包装，不得假定文件标识字段。PHP/Python 仅按受控降级合同实现，不得宣称其专用 SDK 已支持。
- PHP 十一个已有专属 Request 类的 JSON 接口走官方无文件 JSON 路径。
- PHP `2.0.31` 的SDK默认 `DEBUG=false`，但官方Demo/Composer入口会先启用 `DEBUG=true`，日志包含私钥、请求和响应。联调/生产必须在任何SDK加载/初始化前固定false，不得用Demo loader；TLS源码现状另作非阻断提醒。
- PHP `2.0.31` 虽有图片Request/路由，但 `BsPayClient::postRequest($request, new CURLFile(...))` 仍关闭请求签名和响应验签，官方Demo还同时传互斥来源，不能直接使用。受控图片传输必须保持请求加签、正确multipart、TLS及日志边界。
- Python专属JSON Request使用对应模块；图片Request的扩展/字段/文件键/签验缺陷仍在。需控制 `need_sign=True` 的图片底层入口是 `dg_sdk.core.request_tools.request_post`，不是不接受该开关的 `DGTools.request_post`。本地文件用顶层 `file` 键并补齐官网字段；`file_url` 模式必须发送图片规定的multipart文本字段，不能走普通JSON分支。
- Python `2.0.28` 的 `MerConfig` 第五参数为 `sign_type`，第六为 `jpt_x_skill_source`，使用显式关键字 `sign_type="RSA", jpt_x_skill_source=...`；不把来源传第五位置，也不因存在SM2分支自动切换算法。
- 三语言常规接口必须逐语言使用官方 SDK；禁止把 Python 官方 SDK 产物复制成 Java/PHP 手写 HTTP 等价实现。仅 PHP/Python 图片上传允许按本节受控降级，Java 图片上传仍必须使用官方 SDK。
- 商户费率信息查询在锁定的三语言 SDK 中没有专属路由或 Request 类；不得声称 SDK 已有专属类支持或用相似类替代，可经官方 SDK 通用调用入口生成可运行代码，并逐项对照费率查询字段合同。
- Python SDK 的连接重试不能当成进件业务重试。

## 未知通知边界自检

交付商户通知方案前必须保留：

“逐业务通知外层包装待核对。审核和电子协议回调的 ACK、验签原文、HTTP 语义、超时和重试均为 `[需要官方确认]`：请开发者查看对应官方文档，不清楚时咨询汇付官方或汇付开发者交流沟通群。可继续处理框架、已明确业务逻辑与测试，未明确协议留 TODO/适配点，不擅自外推或编造最终值。”

不得套用支付 `notify_url` 或控台 Webhook 的规则。用户业务入驻的 `async_return_url` 已按公共规范锁定 POST/UTF-8、原始 `data` 免排序 RSA 验签、HTTP 200 + `RECV_ORD_ID_` + `req_seq_id`、5秒超时和特定重试；读取 `user-onboarding-platform-contracts.md`，不得把该规则反向外推到商户通知。

## 请求、凭据和日志

- 保留调用方已经提供的 `req_date`、`req_seq_id`、申请单号和商户号；缺失或非法时报错。
- 私钥、身份证、银行卡、手机号和图片资料不得写入前端、日志、仓库或回答示例。
- 未显式配置 `skill_source` 时，本 Skill 的商户、用户或扩展接口参与生成都使用 `hfms/1.0.4`；支付与本 Skill 都参与当前请求时使用 `hfps/1.3.5;hfms/1.0.4`。仅安装在仓库但未参与当前请求不计入；顺序固定为支付、进件，使用一个英文分号且不加空格，不得去重掉任一已参与 Skill。
- 调用方显式提供经确认的 `skill_source` 合同值时原样透传；不得再追加 `sys_id`，也不得把来源头写进业务 `data`。

## 输出要求

回答至少包含：

1. 实体类型（支付商户或分账/结算用户）、主体类型、目标接口、阶段和技术栈。
2. 本轮实际使用的 references。
3. 请求、同步响应、通知方向和字段来源。
4. 未确认协议、外部资料和人工确认项。
5. 需要继续进入支付交易时，明确交接给 `$huifu-pay-integration`。

## 当前版本

| 项目 | 口径 |
| --- | --- |
| Skill 版本 | `1.0.4` |
| Skill 来源标识 | `hfms/1.0.4` |
| 官方来源快照 | `2026-09-22`：商户十三接口2,210条、用户九接口611条、扩展十二接口546条，共34接口3,367条 |
| Java SDK 证据基线 | `3.0.41` |
| PHP SDK 证据基线 | `2.0.31` |
| Python SDK | `2.0.28` |
| 本地沙箱 | 不提供进件沙箱端点 |
