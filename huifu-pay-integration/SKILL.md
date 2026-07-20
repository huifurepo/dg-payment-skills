---
name: huifu-pay-integration
description: "汇付支付接入副驾驶：适用于首次接入、存量改造、聚合支付、托管支付、抖音直连、拆单支付查询、checkout-js、本地沙箱、PHP/Java/Python SDK、验签、异步通知、商户进件/通道权限/FAQ排查、上线检查、版本升级提示。"
---

# 汇付支付集成

## 版权声明

本 Skill 包中的汇付支付、斗拱支付接口资料整理自上海汇付支付有限公司官方开放平台与官方产品文档；原始文档及其更新维护权归汇付支付官方所有。本 Skill 包仅作技术学习交流与接口集成辅助使用，详细口径见 `references/shared-copyright-notice.md`。

1.3.2 目标：在接入副驾驶基础上补齐商户进件六接口完整字段路径、外部资料索引和 SDK 安全边界。先判断开发者处境，再推荐产品线、商户进件资料路径、接入方案、本地沙箱演练、参数/返回/代码片段检查、问题修复建议和上线检查。默认只读取当前场景必需的 3-5 份本地 reference。

## 什么时候使用

- 第一次接入汇付支付，需要判断聚合支付、托管支付还是 checkout-js。
- 已有订单系统、支付代码、回调逻辑或退款逻辑，需要增量接入汇付。
- 用户要联调方案、方案卡、配置清单、必测项、问题排查或上线检查。
- 用户要用 local-sandbox / 本地沙箱做正式联调前的本地闭环演练、报告校验或故障注入。
- 用户贴出请求参数、返回参数、错误信息或代码片段，需要定位风险。
- 用户遇到商户进件、接口权限、数据权限、通道配置、appid/openid、授权目录、Webhook 收不到、退款/对账/取现/发票类 FAQ 问题。
- 用户询问当前 Skill 版本、如何更新 Skill、是否最新版、能力缺失是否需要升级。

## 什么时候不要使用

- 用户已经明确指定某份本地 reference，只需要读取那一份。
- 用户已经在某个专题文档内，当前问题只和该专题参数、返回字段或代码示例有关。
- 非汇付支付、非斗拱、非支付接入相关问题，不使用本 Skill。

## 执行顺序

1. 从用户表达和可见项目上下文提取 7 个标签：用户类型、产品线、阶段、技术栈、端形态、当前目标、是否存量系统。
2. 用户显式询问版本或升级时，直达 `references/skill-version-policy.md`。
3. 检查“🔴 CHECKPOINT · HARD STOP”；命中后只输出硬检查点并等待确认。
4. 未命中硬检查点时，优先使用下面的精确场景路由；没有精确项时再用产品线与阶段回退路由。
5. 选择 3-5 份本地 reference；官网 URL 只作来源追溯和人工刷新，不计入本轮 references。
6. 首次接入输出接入判断卡和方案卡；存量接入输出存量改造建议卡；其他场景按用户意图输出对应卡片。最后应用技术栈规则、全局边界和反例黑名单。

路由优先级固定为：版本/升级 > 硬检查点 > 精确场景路由 > 产品线与阶段回退路由 > 首次接入默认流程。多处命中时只执行最高优先级入口。

Reference 裁剪规则：命中单行时严格使用该行文档；用户同时提出两个独立目标时才合并。合并后超过 5 份时，只保留主场景入口、关键专题、最终确认/验签、技术栈适配、FAQ/排查入口，其他方向写成“暂不读取”。进件字段、类型、长度、必填、SDK 或请求/响应问题先读精确原子接口与字段合同；FAQ 只在权限、通道、审核结果或排障现象出现时补读。退款 `setOrgReqSeqId` 编译报错必须同时覆盖 `hostingpay-faq.md` 和 `hostingpay-refund.md`。

进件字段生成必须按“接口 + 请求/响应方向 + 完整路径”从字段合同取值，并同时核对类型、长度、Y/N/C、枚举、默认值、条件、互斥和补充材料。官网示例值不是默认值；没有本地约束的字段标记 `[需要官方确认]` 并停止赋值。尤其不得把详情查询响应的 `online_flag/quick_flag/withhold_flag=1/0` 写入业务开通请求；业务开通请求三者只能是字符串 `Y/N`。

FAQ 原始目录和原文不随 Skill 分发，只使用本地规则化摘要。

跨场景补读约束：

- 方案类最多读取方案选择和方案卡两份 copilot 文档。
- Java 代码先读同目录 `shared-server-sdk-matrix.md`，再按产品线选择 SDK；项目版本未知或不同时先核对实际源码。
- 命中分期、费率、贴息、通道准入、大额、网银、资金/结算/发票/投诉/风险能力时，补读同目录 `official-service-source-index.md`，只整理字段位置和升级人工材料，不给开通、费率、准入、风控或可上线结论。
- 本地沙箱转真实联调、公开上线或官方能力边界时，补读上线检查和官方资料源索引。维护者最小复测读 canonical regression 文档，完整回归使用仓库级脚本。

### 精确场景路由

| 用户场景 | 最小 reference 集 |
| --- | --- |
| 首次接入、产品线不明 | `references/shared-overview.md`、`references/copilot-onboarding.md`、`references/copilot-solution-selection.md` |
| 普通 Java 服务端首次接聚合支付、要接入判断卡 | `references/shared-overview.md`、`references/copilot-onboarding.md`、`references/aggregation-quickstart.md`、`references/aggregation-customer-preparation.md` |
| 存量系统新增汇付支付；当前项目已有订单、支付、回调、退款或状态机代码 | `references/shared-overview.md`、`references/copilot-existing-system.md`、`references/copilot-solution-selection.md` |
| 存量系统补退款 / 退款查询 | `references/copilot-existing-system.md`，再按产品线补 `references/aggregation-refund.md` 或 `references/hostingpay-refund.md` |
| 存量系统改回调 / 重复通知 / 幂等 | `references/copilot-existing-system.md`、`references/copilot-troubleshooting-playbooks.md`、`references/shared-async-notify.md` |
| 已完成托管预下单和最终确认，只接 checkout-js | `references/checkout-js.md`、`references/checkout-js-callback-and-confirmation.md`、`references/hostingpay-async-webhook.md`；输出固定写“本轮已跳过托管 quickstart/base/preorder/query 等已完成阶段。” |
| checkout-js 先决能力未确认 | `references/copilot-onboarding.md`、`references/checkout-js-create-preorder-contract.md`，触发硬检查点 |
| 聚合查单 / 关单 / 合单关单 / 对账 | `references/aggregation-query.md`；只在关单补 `aggregation-query-trade-close.md` / `aggregation-query-close-query.md`，只在对账补 `aggregation-query-reconciliation.md` |
| PHP 聚合支付下单 / 官方 PHP SDK 代码 | `references/aggregation-order.md`、`references/aggregation-php-adapter.md`、`references/aggregation-query-php-scenarios.md`；需要核对安装版本时再补 `references/shared-server-sdk-matrix.md` |
| 抖音直连下单 / `pre_order_type=4` | `references/hostingpay-preorder.md`、`references/hostingpay-preorder-douyin-direct.md`、`references/hostingpay-async-webhook.md` |
| 拆单支付订单查询 / `splitpay/query` | `references/hostingpay-query.md`、`references/hostingpay-query-splitpay.md`；需追溯微信小程序拆单来源时再补 `references/hostingpay-preorder-wechat-mini.md` |
| 抖音直连或拆单新增接口是否三语言 SDK 兼容 | `references/shared-server-sdk-matrix.md`、`references/hostingpay-preorder-douyin-direct.md`、`references/hostingpay-query-splitpay.md` |
| PHP 模板或 SDK 示例 | `references/shared-server-sdk-matrix.md`，再按产品线补 `references/aggregation-php-adapter.md` 或 `references/hostingpay-php-adapter.md` |
| Python 模板或 SDK 示例 | `references/shared-server-sdk-matrix.md`，再按产品线补 `references/aggregation-python-adapter.md` 或 `references/hostingpay-python-adapter.md` |
| 仅询问 DTO / Controller 已接收字段的保留规则或代码边界 | `references/shared-request-field-preservation.md`；可说明聚合/托管的公共边界，不因产品线未明硬停 |
| 参数、返回、代码片段排查 | `references/copilot-parameter-review.md`、`references/copilot-troubleshooting-playbooks.md` |
| 企业/个体商户基础信息进件 | `references/merchant-onboarding-enterprise.md`、同目录 `merchant-onboarding-field-contracts.md` |
| 无执照个人商户基础信息进件 | `references/merchant-onboarding-individual.md`、同目录 `merchant-onboarding-field-contracts.md` |
| 商户进件图片上传 / 文件标识 | `references/merchant-onboarding-image-upload.md`、同目录 `merchant-onboarding-field-contracts.md` |
| 进件完整字段清单、DTO、完整响应结构、嵌套路径或字段外部资料 | `references/merchant-onboarding-complete-field-catalog.md`、同目录 `merchant-onboarding-field-contracts.md`；命中外部网页、编码表、XLSX、第三方渠道指引或固定协议时再补同目录 `merchant-onboarding-external-resources.md`；最后按主体/接口补 1 份原子 reference |
| 商户进件 `file_url` 三语言 SDK 差异 | `references/merchant-onboarding-image-upload.md`、`references/shared-server-sdk-matrix.md`；输出前执行“进件未知边界自检” |
| 商户进件五个 JSON 接口的 Java 日志安全初始化 / Request 类盘点 | `references/merchant-onboarding-field-contracts.md`、`references/shared-server-sdk-matrix.md`；不逐份加载五个原子接口页；回答必须说明公共 `AbstractRequest`、`BasePay.debug` 默认 `true`、统一关闭时点，以及关闭调试不影响签名/验签 |
| 商户业务开通 / 补开 / 渠道结果 | `references/merchant-onboarding-business-open.md`、同目录 `merchant-onboarding-field-contracts.md` |
| 基础进件已有 `huifu_id`、业务已提交，判断是否可交易 | 按主体读取 `merchant-onboarding-enterprise.md` 或 `merchant-onboarding-individual.md`，再读 `merchant-onboarding-business-open.md`、`merchant-onboarding-application-status-query.md`、`merchant-onboarding-field-contracts.md` |
| 商户详细信息核对 | `references/merchant-onboarding-detail-query.md`、同目录 `merchant-onboarding-field-contracts.md` |
| 商户申请单审核或渠道状态查询 | `references/merchant-onboarding-application-status-query.md`、同目录 `merchant-onboarding-field-contracts.md` |
| 进件审核、逐业务或电子协议回调 | 企业审核读 `merchant-onboarding-enterprise.md`；个人审核读 `merchant-onboarding-individual.md`；逐业务/协议读 `merchant-onboarding-business-open.md`；不读取支付 `shared-async-notify.md` 或控台 Webhook 规则；输出前执行“进件未知边界自检” |
| 进件 FAQ、接口权限或通道配置排查 | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` |
| 进件已返回 `huifu_id` 但业务开通失败、实名状态延迟或提示补资料 | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md`、`references/merchant-onboarding-business-open.md`、`references/merchant-onboarding-application-status-query.md`；必须分别检查业务开通、银行卡、结算、取现、`token_no`、实名和补资料 |
| 聚合微信 JSAPI 的 `sub_mch_id` / `sub_appid` / `sub_openid` 绑定、URL 未注册或 `redirect_uri` | `references/merchant-onboarding-faq.md`、`references/aggregation-order-method-wechat.md`、`references/copilot-troubleshooting-playbooks.md` |
| Webhook 找不到 `sign`、服务商收不到下属机构事件，或询问与 `notify_url` 的验签差异 | `references/shared-webhook-signing.md`、`references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` |
| 对账文件未生成/重新生成、DM 取现额度或手续费发票 | `references/merchant-onboarding-faq.md`、`references/official-service-source-index.md`、`references/aggregation-query-reconciliation.md`、`references/copilot-troubleshooting-playbooks.md` |
| 官网 FAQ 的 URL 未注册 / `redirect_uri` 域名不一致 | `references/official-service-source-index.md`、`references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md`；只使用本地摘要，不实时访问官网 |
| 本地沙箱 / local-sandbox / 本地模拟支付 / 沙箱报告 / 故障注入 | `references/shared-local-sandbox.md`，再按产品线补异步通知、查询或上线检查文档 |
| 本地沙箱通过后准备官方联调或上线 | `references/shared-local-sandbox.md`、`references/copilot-go-live-checklist.md`；必须明说不代表官方联调通过、不代表具备生产上线条件，且不验证真实商户权限、通道、费率、风控或资金结果 |
| 托管 Java SDK 方法拼写 / setter 编译 FAQ / 退款 `setOrgReqSeqId` 编译报错 | `references/hostingpay-faq.md`、`references/hostingpay-refund.md` |
| 官网能力、不覆盖能力、生产失败定责、转人工材料或排查后联系技术支持 | `references/copilot-troubleshooting-playbooks.md`、`references/official-service-source-index.md` |
| 上线前检查 | `references/copilot-go-live-checklist.md`、`references/copilot-existing-system.md` |
| Skill 版本、更新方式、能力缺失是否升级 | `references/skill-version-policy.md` |

### 存量系统判断

存量判断优先看业务系统证据，不只看用户是否说出“存量”二字。

判为存量或疑似存量的条件：

- 用户表达包含“已有订单系统、现有项目、线上商城、已有支付渠道、已有回调、已有退款、已有状态机、PaymentService、OrderService、NotifyController、RefundService”等信号。
- 当前工作区或用户贴出的代码里出现订单、支付服务、回调入口、退款、查单、发货/权益开通、订单状态枚举或状态机等业务链路信号。
- 用户说“第一次接汇付”但同时存在上面任一业务系统证据时，判断为“存量业务系统首次接入汇付”，不是新建空项目。

只有用户明确说明“从零新建空项目、没有现有订单/支付/回调/退款/状态机”，才把“是否存量”写成“否”。证据不足时写“未确认”或“疑似存量”，不要直接写“不是存量项目”。命中存量或疑似存量时，优先读取 `references/copilot-existing-system.md`，输出新增、保留、人工确认和回归检查。

## 检查点机制

### 软检查点

软检查点不等待用户回复。用于说明主动跳过已完成阶段、排除相邻产品线、提醒 checkout-js 依赖托管预下单和最终确认。

### 🔴 CHECKPOINT · HARD STOP 硬检查点

硬检查点必须等待用户确认后再继续。只在以下情况触发：

1. 无法区分聚合支付、托管支付、checkout-js 三条主链路。
2. 无法区分服务端接入、前端页面接入、最终状态确认。
3. 用户要求现成代码，但当前组合无模板且存在多条回退路径。
4. 用户只推进 checkout-js 前端，但未确认托管预下单、异步通知验签/幂等和查单补偿闭环。
5. 用户要求可直接联调、可上线或生产可用代码，但缺少生产/联调环境、`sys_id`、`product_id`、商户号/`huifu_id`、RSA 密钥安全来源、`skill_source`、`notify_url`、渠道标识；托管场景还缺 `project_id`、托管项目状态或 H5/PC `callback_url`。
6. 本地 SDK 源码与文档口径冲突，且冲突点属于请求头、签名、版本或能力覆盖。
7. 用户要求生成或提交企业/个体或无执照个人的可运行联调/生产进件请求，但主体类型、`sys_id` / `product_id` / `upper_huifu_id` 权限、真实材料可得性未确认；或要求本地图片流上传、进件审核/电子协议回调实现而该协议仍标记 `[需要官方确认]`。纯字段解释、状态分层、详情/申请状态查询和 `file_url` 安全边界不因材料未确认而硬停。

纯文档阅读顺序、能力说明和缺口盘点不触发硬检查点。即使 checkout-js 的异步通知闭环尚未完成，也应给出组件、回调确认和异步通知的最小阅读链路，并把未完成项标成前置缺口；只有用户要求生成或提交可运行接入代码时才按上面的硬检查点停止。

仅询问“已接收的 DTO / Controller 字段应如何保留”或要求说明代码边界时，直接读取 `references/shared-request-field-preservation.md`；该规则在聚合和托管支付中一致，不因具体退款产品线未明而硬停。用户未要求完整 SDK 请求代码时，不得将“给代码边界”扩大解读为“要求可运行代码”。

SDK 安装、升级、初始化和通用 loader 骨架不依赖聚合/托管产品线选择，也不触发产品线硬检查点。用户只要求 PHP SDK 通用骨架时，应给出安装/升级/备用包、环境变量、`BsPay::init(...)`、`HUIFU_SDK_ROOT` 和显式加载具体 request 类的完整 bootstrap；同时说明实际业务 request 仍需选定产品线，不在通用骨架中猜测接口字段。

硬检查点输出首行必须固定为 `🔴 CHECKPOINT · HARD STOP：硬检查点。`，并包含本轮实际使用的 references、当前判断、为什么不能直接继续、唯一确认问题。未确认前不输出完整阅读顺序、代码骨架或技术栈切换方案。
checkout-js 先决能力未确认时，即使用户说“不用问”“最省事”“只负责前端”，也必须输出硬检查点；固定说明“checkout-js 不能单独成立，不能只靠前端直接接入。”，不得给安装步骤、初始化代码或前端接法。

命中本地图片流上传硬检查点时，阻断后仍必须增加“已确认安全摘要”，且只写下面四项：`data.file_url` 与顶层 `file` 文件流互斥；图片仅支持 JPG/BMP/PNG 且单张最大 2MB，其他文件最大 10MB；Java `BasePay.debug` 默认开启会记录私钥、签名和请求数据，必须在进程初始化阶段、任何 SDK 请求前全局设为 `false`；这些事实不代表本地 multipart、签名原文、响应文件标识或业务重试语义已经确认，仍不得生成实现。摘要之后继续只问一个最高优先级确认问题，不展开代码、签名算法或响应解析。

唯一确认问题按优先级选择：商户进件场景先问主体类型；再问产品线/主链路、端形态和最终确认方式、生产/联调环境、`sys_id` / `product_id`、商户号/`huifu_id`、RSA 密钥安全来源和 `skill_source`；托管场景再问 `project_id`、托管项目状态、`notify_url`、`callback_url`，最后问渠道标识。同一轮只问最高优先级缺口。

### 失败模式表

| 触发条件 | 一线处理 | 仍失败兜底 |
| --- | --- | --- |
| 产品线不明或聚合/托管/checkout-js 混在一起 | 输出硬检查点，只问主链路 | 用户仍不确认时，给接入判断卡，不给代码 |
| checkout-js 前置未确认 | 输出硬检查点，确认托管预下单、异步通知验签/幂等和查单补偿闭环 | 未确认前不输出安装步骤、初始化代码或前端接法 |
| 生产/联调配置缺失却要求可上线代码 | 输出硬检查点，只问最高优先级缺口 | 缺口未补齐时只给配置清单和必测项 |
| SDK 源码与本地文档冲突 | 停止生成代码，说明冲突字段和已读来源 | 只整理人工确认材料，不自行改 SDK 口径 |
| 用户要求跳过验签、伪造成功或收到通知即改成功 | 拒绝不安全代码，给验签、幂等、查单/异步通知最终确认替代方案 | 不提供可运行的危险代码片段 |
| 用户要求费率、准入、合规、生产定责结论 | 转官方资料源索引和人工材料清单 | 不给开通、可上线、责任归属或政策结论 |
| 接口权限或数据权限认证失败 | 区分 `sys_id` 接口权限、`product_id`、`huifu_id`、`upper_huifu_id` 和请求头来源 | 不让用户随便替换商户号或产品号；整理权限开通材料 |
| 通道路由、appid/openid 或授权目录失败 | 检查通道开通、线上/线下场景、`pay_channel`/`pay_scene`、appid 绑定和 openid 来源 | 配置仍不匹配时转渠道/运营确认，不伪造 appid/openid |
| Webhook 找不到 `sign` 或收不到下属机构事件 | 先查 URL query、原始 body、endpoint key、统一接收下属机构事件配置 | 与 `notify_url` 混淆时退回两套验签边界，不继续写业务成功逻辑 |
| 退款处理中、对账文件未生成、DM 取现或发票问题 | 退款走查询轮询和降频；对账看配置、跑批和任务状态；资金/税务问题转人工 | 不换流水并发重试同一笔退款，不写支付接口代码解决取现或发票 |
| 用户明确说排查后仍解决不了或要技术支持 | 整理已排查项、脱敏材料和下一步确认点 | 给官方 AI 技能包技术支持链接 `https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support` |

## 未精确命中时的回退路由

精确场景未命中时，先读 `references/shared-overview.md`，再按产品线和阶段各补 1-2 份文档；用户已明确完成的阶段不再读取。

### 产品线裁决

| 用户目标 | 默认产品线 | 主文档 |
| --- | --- | --- |
| 标准服务端收款、扫码、付款码、小程序支付 | 聚合支付 | `aggregation-quickstart.md`、`aggregation-order.md` |
| H5/PC 收银台、项目制预下单、`project_id` | 托管支付 | `hostingpay-quickstart.md`、`hostingpay-preorder.md` |
| 抖音直连下单、抖音 H5/APP 支付、`pre_order_type=4` | 托管支付 | `hostingpay-preorder-douyin-direct.md` |
| 拆单支付订单查询、`splitpay/query` | 托管支付 | `hostingpay-query-splitpay.md` |
| 商户自有页面嵌入 checkout 或支付按钮 | checkout-js + 托管预下单 | `checkout-js.md`、`checkout-js-callback-and-confirmation.md` |
| 已有订单系统或当前项目已有订单/支付/回调/退款/状态机代码，新增汇付支付 | 存量系统增量接入 | `copilot-existing-system.md` |
| 参数、返回、错误、代码片段排查 | 问题解决中心 | `copilot-parameter-review.md`、`copilot-troubleshooting-playbooks.md` |
| 准备上线 | 上线检查 | `copilot-go-live-checklist.md` |

### 阶段主路由

| 阶段 | 聚合支付 | 托管支付 / checkout |
| --- | --- | --- |
| 首次接入 | `aggregation-quickstart.md`、`aggregation-customer-preparation.md` | `hostingpay-quickstart.md`、`hostingpay-customer-preparation.md` |
| 初始化 / 公共配置 | `aggregation-base.md` | `hostingpay-base.md` |
| 下单 / 预下单 | `aggregation-order.md` | `hostingpay-preorder.md`；抖音直连补 `hostingpay-preorder-douyin-direct.md` |
| 查询 / 关单 / 对账 | `aggregation-query.md` | `hostingpay-query.md`；拆单支付查询补 `hostingpay-query-splitpay.md` |
| 退款 | `aggregation-refund.md` | `hostingpay-refund.md` |
| 前端组件 | 不适用 | `checkout-js.md`，最终确认回到 `hostingpay-query.md` 或 `hostingpay-async-webhook.md` |
| 异步通知 / 验签 / 幂等 | `aggregation-async-webhook.md` | `hostingpay-async-webhook.md` |

## 输出卡片

| 用户意图 | 输出卡片 | 详细规则 |
| --- | --- | --- |
| 不知道怎么接 | 接入判断卡 | `copilot-onboarding.md` |
| 需要联调方案 | 方案卡 | `copilot-solution-cards.md` |
| 已有系统要增量接 | 存量改造建议卡 | `copilot-existing-system.md` |
| 报错、参数、返回、代码片段 | 问题排查卡或参数检查卡 | `copilot-troubleshooting-playbooks.md`、`copilot-parameter-review.md` |
| 商户进件、权限、通道、Webhook、资金运营 FAQ | FAQ 排查卡 | 先分代码/配置/运营边界，再给检查顺序和转人工材料 |
| 上线前确认 | 上线检查卡 | `copilot-go-live-checklist.md` |
| 本地沙箱演练、报告或故障注入 | 本地沙箱检查卡 | `shared-local-sandbox.md` |

方案卡、问题排查卡和上线检查卡必须说明适用/不适用、前置配置、标准联调步骤、必测项、常见卡点、修复建议和升级人工条件；接入判断卡、存量改造建议卡和硬检查点按下面的迷你模板输出。回答中不要一次性倾倒所有 reference。
每次输出必须显式列出 `本轮实际使用的 references`，数量控制在 3-5 份；硬检查点可只列已读取入口。
暂不读、暂不推荐、禁止动作里不要继续列具体 `.md` 文件名，只写产品线或能力方向，避免 reference 文件名总数超过 5。
如果引用文档未覆盖某个卡片字段或产品能力，必须显式标注 `[需要确认]`，不要补写看似确定但无本地依据的配置、字段或步骤。
用户要求跳过验签、绕过最终确认、收到通知即改成功时，必须拒绝该不安全代码请求，并给出验签、幂等、查单/异步通知最终确认三项安全替代方案。
版本/升级类回答必须固定写明：不能主动联网检查或主动推送升级。

### 迷你输出模板

接入判断卡：
- 本轮实际使用的 references：列 3-5 份。
- 用户类型：必须逐项写明。
- 产品线：必须逐项写明。
- 阶段：必须逐项写明。
- 技术栈：必须逐项写明。
- 端形态：必须逐项写明。
- 当前目标：必须使用字段名“当前目标：”，不要写成“目标：”。
- 是否存量：必须逐项写明；证据不足时写“未确认/疑似存量”，不要直接写“否”。
- 推荐主方案：必须逐项写明。
- 暂不推荐方向：必须逐项写明。
- 还缺配置：必须逐项写明。
- 下一步：必须逐项写明。

存量改造建议卡：
- 本轮实际使用的 references：列 3-5 份。
- 存量系统增量接入：必须原样使用此标题，并说明当前是在已有系统上增量接入。
- 建议新增：必须原样使用此标题。
- 建议保留：必须原样使用此标题，并逐字写明“不重写订单系统，不直接替换原订单状态机。”
- 需要人工确认：必须原样使用此标题。
- 建议补充落库字段：必须原样使用此标题。
- 风险点：必须原样使用此标题。
- 回归检查：必须原样使用此标题。

硬检查点：
- 🔴 CHECKPOINT · HARD STOP：硬检查点。
- 本轮实际使用的 references：列已读取入口。
- 当前判断：写清已知标签。
- 固定边界：checkout-js 不能单独成立，不能只靠前端直接接入。
- 为什么不能直接继续：写清风险。
- 已确认安全摘要：仅本地图片流上传场景输出上述四项固定事实；其他硬检查点省略本项。
- 请确认：只问 1 个最短问题。

参数检查卡：
- 本轮实际使用的 references：列 3-5 份。
- 阻断结论：能否继续联调。
- 问题字段：字段名、当前值、风险。
- 修复建议：改法、必测项、需要人工确认项。

FAQ 排查卡：
- 本轮实际使用的 references：列 2-5 份。
- 问题类型：写明商户进件、接口权限、数据权限、通道配置、appid/openid、Webhook、退款、对账、取现或发票。
- 边界判断：必须三选一写成“代码可修复 / 配置需补齐 / 运营或渠道侧确认”。
- 先检查：按主体层级、权限开通、通道/授权配置、流水状态、跑批任务或资金运营顺序列 3-5 项。
- 修复动作：只给能由客户代码或控台配置完成的动作；需要开通、审核、风控、税务、额度或真实商户状态时转人工。
- 禁止动作：不得随便替换 `huifu_id`、`product_id`、appid/openid、不得并发重试处理中退款、不得用支付代码解决取现或发票。

上线检查卡：
- 本轮实际使用的 references：列 3-5 份。
- 检查项：通用上线检查、存量系统检查、必测项、灰度回滚、日志脱敏。
- 托管 H5/PC 必含：`project_id`、托管项目状态、`notify_url`、`callback_url` 只做前端回跳、异步通知验签/幂等和查单补偿闭环。
- 输出前逐项自检上一行六个托管 H5/PC 要素；只列 `project_id` 而漏掉“托管项目状态可交易”仍视为不完整。
- 禁止动作：必须写明“不定责”，并说明不把真实密钥写入仓库或前端。

本地沙箱检查卡：
- 本轮实际使用的 references：列 2-5 份，必须包含 `shared-local-sandbox.md`。
- 当前目标：写明安装/启动、协议演练、通知重放、报告校验、故障注入或上线前证据。
- 下载与运行：安装/启动类回答必须优先给构建后的 preview 总包 `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/hf-payment-local-sandbox-latest-preview.zip`，并说明解压后按 Windows、macOS Intel、macOS Apple Silicon 或 Linux 选择 `dist/` 内平台包；不得把 Skill 包或仓库工作区里的本地二进制当作客户分发方式，也不得要求普通客户安装 Go 后自行构建。
- 来源字段：local-sandbox `1.0.1` 的冻结 r4 快照使用 `hfps/1.3.1;sandbox/1.0.1`；官方联调或生产环境使用 `hfps/1.3.2`，不要携带 `;sandbox/...` 后缀。
- 可验证：写明本地可验证的请求、签名、通知、查单补偿、状态流转和报告完整性。
- 不可验证：写明不能验证真实权限、通道、费率、风控、资金结果或官方验收；失败态异步通知与 `resp_code`/`trans_stat` 分叉当前不可注入；接收侧幂等需接入方自证。

## SDK / 模板规则

C#、Go、Rust、Node、.NET、Ruby、Kotlin、Scala、Swift、C++ 不生成完整模板；只给受支持主链路或协议级阅读路径。

### Java

- 聚合支付业务主链路使用 `dg-lightning-sdk 1.0.5`；托管支付、聚合支付对账和商户进件使用 `dg-java-sdk 3.0.39`。
- Java 如果输出可运行代码，必须显式出现 `MerConfig.setSkillSource(...)`；官方 SDK 在配置后自动补 HTTP 请求头 `jpt-x-skill-source`，并在请求 `data.huifu_id` 存在且非空时自动补 `jpt-x-skill-huifu_id`。
- Java 使用 `com.huifu.bspay.sdk.opps.core.BasePay`（`dg-java-sdk 3.0.39`）时，`BasePay.debug` 默认为 `true`，公共 `AbstractRequest` 会对所有 URI 打印私钥、签名和请求数据。任何可运行代码都必须在进程初始化阶段、任何 SDK 请求之前执行一次 `BasePay.debug = false;`，不得在并发请求中临时切换；关闭调试输出不关闭请求签名或响应验签。
- Java 图片 `file_url` 调用 `BasePayRequest.requestBasePay(...)` 时末参必须是 `isPage=true`；SDK 在该判断前完成请求签名，因此请求签名保留，但会在响应验签前返回原始响应，因此响应验签跳过。不得传 `false`，也不得把 `isPage` 解释成关闭请求签名。
- Java 托管 SDK `dg-java-sdk 3.0.39` 的 `MerConfig` 产品号 setter 是 `setProductId(...)`；不要再生成旧文档中的 `setProcutId(...)`。
- Java 项目已安装 SDK 版本未知或不同于当前基线时，先核对服务端 SDK 矩阵和项目实际源码；未确认前不输出固定版本依赖、setter 名或新增接口 request 类代码。
- Java 输出代码、DTO、Controller、Service 或 SDK Request 组装逻辑时，必须同时读取字段保留规则（`references/shared-request-field-preservation.md`），保留外部 DTO / Controller 已接收的 `req_date`、`req_seq_id`、金额、商户号、项目号、通知地址和原交易定位键。

### PHP

- PHP 当前 Skill 包基线为 `huifurepo/dg-php-sdk 2.0.29`。
- 新项目安装：`composer require "huifurepo/dg-php-sdk:^2.0.29"`；旧版本项目先调整版本约束，再执行 `composer update huifurepo/dg-php-sdk --with-all-dependencies`。
- Composer 不可用时，使用当前基线备用下载地址 `https://api.github.com/repos/huifurepo/bspay-php-sdk/zipball/refs/tags/2.0.29`，解压后设置 `HUIFU_SDK_ROOT` 并校验 `BsPaySdk/init.php`。
- 聚合支付核心支付主链路优先 `BsPaySdk\core\Payment`；聚合对账与托管支付优先 `BsPayClient::postRequest()`。
- PHP 可运行代码必须包含 SDK 安装/升级说明、`init.php` 检查、`BsPay::init(...)`、`skill_source`、`HUIFU_SDK_ROOT` 和环境变量准备。
- PHP `2.0.29` 传 `CURLFile` 的 multipart 路径缺少 `jpt-x-skill-source`、`jpt-x-skill-huifu_id`、`jpt-sdk_version`，且关闭请求签名和响应验签；必须阻断本地文件可运行代码，不得外推成自动带来源头或改用手写 `curl` 绕过。
- 不生成 `HostingClient`、`AggregationClient` 或自写 `curl` 的业务代码。

### Python

- Python 当前 Skill 包基线为 `dg-sdk 2.0.23`，import 名为 `dg_sdk`。
- 新项目安装：`python3 -m pip install "dg-sdk==2.0.23"`；版本核对使用 `python3 -c "import dg_sdk; print(dg_sdk.DGClient.__version__)"`。
- Python 生产环境必须固定 `DGClient.env = "prod"`，并显式传入 `MerConfig(private_key, public_key, sys_id, product_id, jpt_x_skill_source)`。
- `jpt_x_skill_source` 最终成为 HTTP 请求头 `jpt-x-skill-source`；SDK 会从最终请求参数里的 `huifu_id` 自动生成 HTTP 请求头 `jpt-x-skill-huifu_id`，并用 `jpt-sdk_version=python_2.0.23` 上送 SDK 版本。
- 聚合支付核心支付主链路优先 `dg_sdk.Payment` + `Payment*Request`；聚合对账与托管支付优先 SDK request 类 `.post({})`。
- 安装或版本核对失败时显式报错并停止；不要无版本安装、降级、生成自维护 `HostingClient` / `AggregationClient` 或手写 `requests` 版本。

## 全局边界

- 不猜测 `project_id`、`callback_url`、`notify_url`、`sub_openid`、`buyer_id`、`buyer_logon_id`、`auth_code`、`devs_id`、`fee_sign` 等运行时值。
- 不把 `HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 写入前端、仓库或示例常量。
- 外部 DTO / Controller 已接收的 `req_date`、`req_seq_id`、金额、商户号、项目号、通知地址或原交易定位键，生成代码时必须保留入参或原样映射；缺失或非法时显式报错。
- `HUIFU_SKILL_SOURCE` 最终上送值保持 `<skill_source>` 原样透传，不追加 `sys_id`；local-sandbox `1.0.1` 的冻结 r4 快照由业务配置显式传入 `hfps/1.3.1;sandbox/1.0.1`，生产和官方联调只传 `hfps/1.3.2`。
- 商户进件的企业、个人、业务开通、详情和申请状态五个 JSON 接口已由 Java `3.0.39`、PHP `2.0.29`、Python `2.0.23` 源码证实存在可选专属 Request 类；仍不得把 SDK 封装外推成资料权限、实际响应或回调结论。企业和个人进件审核异步地址只能使用 `async_return_url`，禁止使用支付字段 `notify_url`。字段是否存在、完整嵌套路径、类型、长度、Y/N/C 和官方说明必须先查 `merchant-onboarding-complete-field-catalog.md`；枚举、默认值、冲突和安全边界再查 `merchant-onboarding-field-contracts.md`，两者不得互相替代。图片只对 `file_url` 输出按语言区分的受控调用片段：Java 是 multipart 文本字段并固定 `isPage=true`，请求签名保留、响应验签跳过；PHP/Python 无文件时是 JSON。PHP `CURLFile` 因缺失 Skill 埋点头并关闭签名/验签而阻断；其他本地二进制文件、图片标识/重试继续标 `[需要官方确认]`。仅逐业务通知在有 `ord_id` 时可说明官网规定的 ACK，但其外层包装仍待官方样本；审核和电子协议通知的 ACK，以及三类通知的验签原文、HTTP 语义、编码、超时和重试均为 `[需要官方确认]`，不得生成回调实现。
- 企业/个人进件及图片请求没有真实 `data.huifu_id` 时，绝不为埋点头虚构、补空或固定该业务字段。Python `2.0.23` 会发送空的 `jpt-x-skill-huifu_id`，这是开发侧 SDK 兼容性告警和联调/上线前验证项，**不得仅因此触发业务硬检查点，也不得询问客户“是否允许空请求头”或要求客户替 SDK 行为背书**。业务资料和权限已确认时继续给出 Python SDK 接入方案，并单列 `SDK 兼容性提示`：说明当前行为、不得污染业务报文、联调若拒绝该头则升级/修复 SDK 后复测。PHP `2.0.29` 对缺失 `huifu_id` 的无保护读取可能被提升为异常，仍阻断对应 PHP 可运行代码，但确认问题只能面向开发者询问实际 SDK 版本/源码是否已修复，不询问客户是否接受空头。
- 商户业务开通的开关不是统一布尔编码：请求 `online_flag/quick_flag/withhold_flag` 与支付宝/微信预授权使用字符串 `Y/N`；`out_fee_flag` 使用 `1/2` 且默认 `2`；`out_fee_acct_type` 使用 `01/02/05/09` 且默认 `01`。支付宝和微信预授权目前仅支持企业商户及汇付 MCC `7011/7296/7512`。详情查询响应的同名开关 `1/0/空` 只用于解析，禁止回填请求。未确认主体、MCC、真实业务选择和补充材料时不得把任一开关统一写成 `1`。
- 商户进件字段说明命中外部文档、编码表、XLSX、第三方渠道指引或固定协议地址时，必须读取 `merchant-onboarding-external-resources.md` 并单列 `外部资料提示`：写全字段路径、资料用途/触发条件、可点击链接和未经改写的明文原始地址。未实际读取外部文件正文时必须明说并要求人工核验；地址失效仍保留原始地址并标 `[需要人工访问/确认]`。回调、商户主页、二维码、图片和 APP 下载地址等示例/运行时 URL 不是官方资料，不得作为默认值或推荐地址。
- 用户要求字段清单、DTO、参数示例或完整响应结构时，必须从 `merchant-onboarding-complete-field-catalog.md` 的对应接口和方向逐路径读到所有叶子，父对象也要保留；禁止凭原子 reference 的摘要声称“字段已经列全”，禁止根据 `*_list` 名称猜数组。官网表格的类型、长度、必填栏与说明发生矛盾时原样保留并标 `[官方文档口径冲突]`，不得自行统一。
- 前端支付 callback 不等于最终支付成功；最终状态必须经服务端闭环确认：异步通知先验签、解析、幂等/状态锁，必要时通过查单二次确认或补偿查询，再更新订单状态。
- 新增接口 SDK 兼容性先区分“同一端点的场景化用法”和“独立 Request 类”：抖音直连固定复用托管 `preorder` request，以 `pre_order_type=4` 和 `dy_data` 区分，Java/PHP/Python 均无独立抖音 Request 类；必须写清“不要生成不存在的类名”。
- 拆单支付订单查询必须走 `splitpay/query`，不要和普通托管 `queryorderinfo` 混用；Java/PHP/Python 最新 SDK 均有 `V2TradeHostingPaymentSplitpayQueryRequest`。
- 不回答费率、合规、政策审批、通道准入结论；不提供绕过验签、绕过风控、伪造支付成功或跳过查单确认的代码。
- 生产问题不定责，只整理升级人工材料。回答必须明说“升级人工”，并逐项列出环境、产品线/接口、SDK 及版本、脱敏标识、脱敏请求/响应、请求/平台流水、时间线、脱敏日志、影响范围和已做动作；缺项不得省略，应标为待补。
- 官网 URL 只用于来源追溯和人工刷新，不作为普通回答的本轮实际使用 reference；要求实时核对官网最新口径时，说明需要人工或联网核验。
- 官方 AI 技能包技术支持链接只在用户明确要求联系支持、问题超出本地覆盖或排查后仍解决不了时给出：`https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support`。它是联系方式，不列入“本轮实际使用的 references”。
- Skill 不能主动联网检查或主动推送升级，不能保证当前就是维护方最新版；只有用户触发版本/升级问题时，才基于本地版本策略提示更新路径。

### 🔴 进件未知边界输出自检

命中对应场景时，输出必须保留下面的边界原句；缺少任一句都不得交付：

- `file_url` 三语言边界：“Java 必须使用 `isPage=true`，请求签名保留、响应验签跳过；`BasePay.debug` 默认开启时会记录私钥、签名和请求数据（含 `file_url`）。PHP `CURLFile` multipart 缺失 Skill 埋点头并关闭签名/验签，必须阻断。不猜测响应文件标识字段，响应、业务重试和回调语义均为 `[需要官方确认]`。”
- 进件通知边界：“逐业务通知外层包装待官方样本确认。审核和电子协议回调的 ACK、验签原文、HTTP 语义、超时和重试均为 `[需要官方确认]`，不得外推或生成回调实现。”
- 外部资料边界：“命中字段说明中的外部文档或文件时，必须单列 `外部资料提示`，给出完整字段路径、触发条件和未经改写的原始地址；未读取外部文件正文时明确要求人工核验。示例或运行时 URL 不是官方资料，也不是默认值。”

## 反例黑名单

| 不要做 | 风险 | 替代做法 |
| --- | --- | --- |
| 把 checkout-js 当前端独立接入 | 前端拿不到可信终态 | 先确认托管预下单、异步通知验签/幂等和查单补偿闭环 |
| 把 `resp_code=00000000`、`jump_url` 或前端 callback 当支付成功 | 同步受理或页面回跳不是交易终态 | 最终状态看异步通知验签、幂等和查单/补偿查询 |
| 把 local-sandbox 通过当成官方联调或生产准入 | 本地工具只模拟协议和合成场景 | 进入官方联调环境和上线检查，补真实权限、签名、公证、授权和下载证据 |
| 为抖音直连下单编造独立 SDK Request 类 | Java/PHP/Python 最新 SDK 均没有 `Dypreorder` / `Douyin` 类 | 使用托管预下单 request，固定 `pre_order_type=4`，`dy_data` 按抖音直连文档序列化 |
| 用普通托管 `queryorderinfo` 替代拆单支付订单查询 | 看不到拆单子交易状态 | 拆单查询走 `splitpay/query`，逐条读取 `trans_list[].trans_stat` |
| 为省事重写 `req_date`、`req_seq_id`、金额、商户号或原交易定位键 | 破坏幂等、查单、退款和对账定位 | 保留外部 DTO / Controller 已接收入参，缺失或非法时报错 |
| 生成绕过验签、伪造成功、跳过查单确认的代码 | 直接造成资损和状态错判 | 拒绝危险代码，给安全替代流程 |
| 对费率、合规、通道准入或生产失败定责 | 本地资料不能自动判断这些结论 | 整理脱敏升级材料，转人工确认 |

## 当前版本事实

| 项目 | 当前口径 |
| --- | --- |
| Skill 包版本 | `1.3.2` |
| Skill 包发布日期 | `2026-07-17` |
| 1.3.2 merchant onboarding field refresh | 新增六接口完整字段目录、外部资料索引和图片上传 SDK 安全边界；未确认上传/回调协议只输出确认清单 |
| 1.3.0 refresh | 基线 `2026-06-02`；API 子刷新 `2026-06-10`（抖音直连下单、拆单支付订单查询、聚合字段）；Copilot/支持子刷新 `2026-06-12`（存量识别、FAQ 排查、转人工入口） |
| 聚合支付 Java SDK | `dg-lightning-sdk 1.0.5` |
| PHP SDK 包 | `huifurepo/dg-php-sdk 2.0.29` |
| Python SDK 包 | `dg-sdk 2.0.23`，import 名为 `dg_sdk`，SDK 版本请求头为 `jpt-sdk_version=python_2.0.23` |
| 前端收银台 JS SDK | `@dg-elements/js-sdk`，接入时以项目锁定版本为准；只有用户明确要求且当前环境允许联网时才查询 npm registry |
