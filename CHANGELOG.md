# Changelog

## Payment `1.5.0` / Onboarding `1.1.0` — `2026-10-25`

### 新增

- 支付新增延时交易确认、V3确认查询、确认退款、确认退款查询，以及账户余额、账务流水和异步汇总查询七接口；进件新增商户子账户开通与配置修改两接口。
- 新增九份原子参考、两份独立完整字段目录和SDK矩阵；独立解析核对368个新增字段路径，核验8接口×3语言精确Request路由及真实Python序列化与覆盖探针。汇总查询未找到专属Request，使用官方通用入口。

### 同步与修复

- 复查78份既有来源，13份变化、65份不变；同步托管合单/子单请求、查询及通知、商户开通状态、用户协议与外扣配置、通知类型及编码，以及企业/个人开户sys_id上下级关系注记。
- 当前支付31 API / 3,334路径，进件36 API / 3,534路径，总67 API / 6,868路径。旧目录另存审计基线，日期化来源锁和历史评测保持不变。
- 公共来源头同步hfps/1.5.0与hfms/1.1.0；两个description继续限制300字符。独立包provenance同时绑定基础来源、SDK及新增接口锁。

### 文档缺口

- 交易确认退款查询JSON仅有正式请求定义，不补造响应合同；交易确认通知resp_data编码和分账对象类型冲突保留。
- 汇总接口的异步说明与同步参数表、summary_list字符串与数组示例冲突保留；未声明通知验签原文、ACK和重试不外推其他产品协议。
- 本轮不表示SDK升级、真实网关联调、发布或全量模型回归通过。逐页证据与方案复查见maintainer-contracts中10-25记录。

### 验证

- 全量本地门禁通过，包含来源与字段独立比较、SDK证据、签名向量、敏感示例扫描、两包独立构建及Go沙箱测试；详细复查新增9个接口与4个跨域案例，当前172例规则及正反例自检通过，两个Skill基础校验及300字符description限制通过。
- 完整差异、九接口归属、资料缺口与验证范围见[本轮结果](maintainer-contracts/interface-expansion-2026-10-25.md)。
- [详细复查](maintainer-contracts/interface-expansion-detailed-review-2026-10-25.md)重新核对87份在线来源，补明确认退款退回原商户账户、账户配置与账务查询分工，清理进件目录误带的支付说明，并将新增案例接入运行器和来源指纹。
- 2026-11-01交付前重新执行全量本地门禁及暂存内容扫描；API来源继续使用10-25快照，发布包从干净提交重新生成，真实模型及网关联调范围保持上述记录。

## Payment `1.4.0` / Onboarding `1.0.5` — `2026-10-18`

### 新增

- 支付新增余额支付、支付查询、退款、退款查询、手续费试算、付款关系提交和短信验证码七接口，提供 Java/PHP/Python 官方 SDK 适配及完整字段、条件必填、状态和通知说明。
- 更新支付与进件的官方来源、字段目录及差异证据：支付覆盖24个接口、2,930条字段路径；进件覆盖34个接口、3,366条字段路径。

### 调整与修复

- 两轮复核78份官方文档，同步聚合查询公共信封、托管支付字段与嵌套 JSON 编码，以及图片上传、业务开通修改、统一页面查询和支付宝实名结构。支付使用10-10来源锁，进件使用10-08来源锁，历史来源及冻结沙箱保持不变。
- 统一核验 Lightning Java `1.0.6`、通用 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 的官方固定提交或制品；补全 Python 初始化与配置绑定、Java 包名、三语言响应形状和 PHP 错误响应处理。
- 精简两个 Skill 的执行流程和按需读取规则，合并四份重复导览，将四份维护者回归提示移出安装包并保留历史归档；明确支付、商户和用户的实体及交接边界。
- 将两个 `description` 分别压缩至273和292字符，补充余额支付及进件管理场景，并保留跨 Skill 路由说明；同步路由词校验并加入300字符上限。
- 修正审核签名、图片格式校验、外部资料地址、字段审计覆盖、平台分配 ID 保真，以及聚合通知 `trans_type` 与原订单 `trade_type` 的核对方式。
- 更新来源、SDK、示例、独立打包和回归校验；修正过期断言及正常业务枚举被误判为模型认证故障的问题。

### 验证与已知限制

- 10-18提交前本地门禁通过，覆盖字段与来源、三语言 SDK 证据、签名向量、代码示例、独立打包及 Go 沙箱测试；159个案例的回归规则自检通过。本次未重新运行真实模型全量评测或网关联调。
- 10-10真实模型评测覆盖159个不同案例，并完成后续定向重测；最新完整一轮严格通过66/159，后续局部结果不代表最终候选全量通过，详见[提测前报告](maintainer-contracts/pre-submission-live-evaluation-2026-10-10.md)。
- 历史官方网关联调覆盖6个接口、9次查询或试算请求；Python `2.0.28` 商户费率查询存在小数重编码导致的验签兼容问题，Java `3.0.41` 官方入口有成功对照。资金、短信及真实回调闭环尚未覆盖。
- 两轮来源复核和入口整理证据分别见[10-08复核](maintainer-contracts/api-review-2026-10-08.md)、[10-10复核](maintainer-contracts/api-review-2026-10-10.md)及[Skill 整理报告](maintainer-contracts/skill-review-2026-10-10.md)；版本记录不代表已完成正式发布验收。

## Merchant Onboarding Skill `1.0.4` — `2026-09-28`

- 更新 34 个进件接口的 3,367 条字段路径及 2026-09-22 来源快照，保留历史锁。
- 采用本地 Java 3.0.41、PHP 2.0.31、Python 2.0.28 证据；电子合同改用 agreement 路由及官方 SDK 通用入口。
- 更新用户分级配置、费率原生数组、进件文档、回归与 API/SDK 打包溯源。
- 仅合入进件；支付保持 1.3.5 和原有包内容、SDK 与来源记录。

## Unreleased merchant-onboarding transport-boundary correction — `2026-09-18`

- 修正“通用入口仅服务图片接口”的误阻断：官方 SDK 自带通用调用入口（Java `BasePayClient.request(Map, funcCode, ...)`，内部将 `funcCode` 的 `.` 替换为 `/` 拼接 URL，复用同一签名、验签、请求头与 TLS 链路）属于官方主链路，可用于 SDK 无专属 Request/路由的常规接口（含商户费率查询），不限于图片接口，也不属于受控降级；因无类型化封装兜底，字段须逐项对照字段合同构造。
- “仅 `/v2/supplementary/picture` 允许通用 POST/自写 HTTP”的例外边界不变：其限制对象是离开官方 SDK 的手写实现。
- 同步更新 SKILL.md、shared-server-sdk-matrix、费率查询页、回归用例与真实模型回归规则；不改变接口、字段、SDK 版本基线或 `skill_source`，Skill 版本保持 `1.0.3` / `hfms/1.0.3`。

## Merchant onboarding Skill `1.0.3` — `2026-09-15`

### 新增

- 新增电子合同重发、列表查询、拒签，下级商户权限配置，统一页面进件及查询，以及微信/支付宝 AT 管理共12个接口；冻结12份官方原文并机械生成548个完整字段路径。
- 十二接口均新增原子 reference、完整字段目录、字段合同、来源索引、SDK 能力矩阵和12个 canonical 回归场景。九个商户/AT 接口锁定三语言官方 Request 类；三个电子合同接口未验证到专属类，禁止手写生产 HTTP。
- 进件 Skill 由 `1.0.2` 升级至 `1.0.3`，默认来源标识同步为 `hfms/1.0.3`；与支付 Skill 同时参与时使用 `hfps/1.3.5;hfms/1.0.3`。

### 变更

- 复审既有13个商户接口：字段路径由2,183增至2,207；业务开通、修改与详情新增抖音配置，多处 JSON 容器改为 String，多费率响应明确为 String(JSON Array)，费率查询合同得到修正。
- 复审既有9个用户接口：字段总数仍为554，21项合同变化；多处 JSON 容器改为 String，用户号、D1 和条件必填文案同步官网，并保留当前仍存在的正式表/示例冲突。
- 三个子域合计34个接口、3,309个字段路径。交易分账明细查询在线 SHA 与支付来源锁一致，继续归 `huifu-pay-integration 1.3.5`，未修改其接口合同。

### 复查修复

- 纠正当前商户来源锁中三个与官方原文不一致的路由元数据：商户费率查询 `/v2/merchant/fee-rate/query`、商户状态变更 `/v2/merchant/busi/modify/busistatus`、商户短信发送 `/v2/merchant/basicdata/sms/send`；历史来源锁保持不变，并新增原文路由反向校验。
- 清理回归集中的旧字段数量和旧 wire 口径，新增12个扩展接口的可执行回归规则；当前四套回归共152例，其中商户进件套件44例。
- 扩展接口字段目录改由独立解析器逐节点复核548个字段，同时锁定微信实名查询字段表外九值状态表、19个活动资料链接及统一页面查询 `pay_scene` 链接文字/目标冲突，防止只校验字段表导致关键信息遗漏。

### 安全

- 对官方字段名、类型、长度、条件、示例或回调协议冲突一律保真记录并执行硬停，不推断修复；未确认的电子合同和扩展接口生产传输不得降级为手写 HTTP。

## Unreleased online-document refresh — `2026-08-31`

- 重新锁定并逐字段复审支付37页、商户13页和用户9页在线接口文档；历史来源锁保持不可变。
- 支付目录仍为2,656节点：聚合查询成功示例已使用 `A_MICROPAY`，仅保留正式说明中重复 `A_NATIVE` 的笔误；交易分账明细 `split_trans_responses` 修正为 String(JSON Array)，16个子字段保留数组层级。
- 商户目录由2,155增至2,183节点：新增企业 `head_type`、业务开通及修改的捷行付/线上费率字段、详情查询响应字段；删除企业请求旧 `material_card_info.card_type`；多费率长度、String(JSON) 与 `A/W` 场景口径同步官网。
- 用户目录保持554节点，但关闭开户 `file_list`、响应签名、用户号角色、个人证件示例、详情返回码/D1/外扣账户示例和列表 String/数组/ID长度等已被官网修正的旧冲突；仍保留业务入驻修改的真实未决编码与条件冲突。
- 二次复审关闭开户短信标识、业务入驻 D1 示例和修改通知数组的过期冲突；将业务入驻新增的 `elec_receipt_config/elec_card_list` 未决 wire 纳入硬停，并修正商户 String 空长度叶字段统计为58。
- 本轮尚未发布，不升级 Skill 版本：支付继续使用 `1.3.5` / `hfps/1.3.5`，进件继续使用 `1.0.2` / `hfms/1.0.2`；新增的来源与刷新证明链作为同版本候选更新。

所有重要变更记录在此文件中，格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## Payment Skill `1.3.5` — `2026-08-24`

### 新增

- 新增交易分账明细查询 `POST /v2/trade/trans/split/query`，冻结官方原文与 SHA-256，机械生成29个完整路径：请求7、同步响应22、无异步通知。
- 锁定 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24` 的 `V2TradeTransSplitQueryRequest`、精确路由和仅三个声明字段；官网无可选请求字段，扩展映射必须为空。
- 新增原子 reference、入口路由、SDK 矩阵、来源锁增量门禁和回归用例；支付 Skill 升级为 `1.3.5`，默认来源标识同步为 `hfps/1.3.5`。

### 修复

- 保留 `split_trans_responses` 参数表 `Array` 与成功示例 `String(JSON Array)` 的官方冲突，在正式编码确认前禁止生成生产解析。
- 成功示例独有的顶层 `response.data.huifu_id` 不进入字段目录或 DTO；查询边界锁定为已开通分账能力商户的180天内记录。

## Merchant onboarding Skill `1.0.2` — `2026-08-24`

### 新增

- 新增商户多费率配置 `POST /v2/merchant/busi/multiFee/config`，冻结官方原文与 SHA-256，机械生成27个完整路径：请求15、同步响应12、无异步通知。
- 锁定 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24` 的 `V2MerchantBusiMultifeeConfigRequest` 与精确路由；三个 SDK 只声明定位字段，微信/支付宝配置必须通过 exact-key 扩展写入并禁止覆盖声明字段。
- 新增原子 reference、入口路由、SDK 矩阵、字段合同和回归用例；进件 Skill 版本升级为 `1.0.2`，默认来源标识同步为 `hfms/1.0.2`。
- 新增商户多费率配置查询 `POST /v2/merchant/busi/multiFee/query`，冻结第二轮官方快照并机械生成17个完整路径：请求8、同步响应9、无异步通知；锁定三语言 `V2MerchantBusiMultifeeQueryRequest`、精确路由和 `fee_sign` exact-key 扩展边界。
- 新增企业用户基本信息修改 `POST /v2/user/basicdata/ent/modify`，在不覆盖历史五接口锁的前提下追加官方原文，机械生成37个完整路径：请求32、同步响应5、无异步通知；用户子域当前合计391个节点。
- 锁定三语言 `V2UserBasicdataEntModifyRequest` 与精确路由；生成类只声明 `req_date/req_seq_id/huifu_id/legal_cert_nationality`，其余正式字段通过 exact-key 扩展传入并拒绝覆盖四个声明字段。
- 新增个人用户基本信息修改 `POST /v2/user/basicdata/indv/modify`，在企业修改 r1 快照后仅追加一份官方原文，机械生成26个完整路径：请求21、同步响应5、无异步通知；用户子域当前合计417个节点。
- 锁定三语言 `V2UserBasicdataIndvModifyRequest` 与精确路由；生成类只声明 `req_date/req_seq_id/huifu_id`，其余正式字段通过 exact-key 扩展传入并拒绝覆盖三个声明字段。
- 新增用户业务入驻修改 `POST /v2/user/busi/modify`，在个人修改 r2 快照后仅追加一份官方原文，机械生成120个完整路径：请求85、同步响应11、异步通知24；用户子域当前合计537个节点。
- 锁定三语言 `V2UserBusiModifyRequest` 与精确路由；生成类只声明 `req_date/req_seq_id/huifu_id/sign_user_info`，最终 `sign_user_info` 为官网 Object：Java 的 String setter 用受控 exact-key 覆盖，PHP 可直接传数组，Python 可直接赋 dict；其余扩展拒绝覆盖三个定位字段。
- 新增用户列表查询 `POST /v2/user/list/query`，在业务入驻修改 r3 快照后仅追加一份官方原文，机械生成17个完整路径：请求8、同步响应9、无异步通知；用户子域当前合计554个节点。
- 锁定三语言 `V2UserListQueryRequest` 与精确路由；生成类只声明 `legal_cert_no/req_date/req_seq_id`，可选 `upper_huifu_id` 通过 exact-key 扩展传入并拒绝覆盖三个声明字段。

### 修复

- 请求 `wx_conf_list/ali_conf_list` 按官网 `Object` 类型列与 `jsonArray` 说明保留数组 wire；响应 `conf_list` 按单个 `Object` 解析，不因 `_list` 名称添加数组层级。
- 保留响应 `pay_scene` 的 `T=微信` 与 `pay_way` 的 `W=微信` 官方冲突，执行层禁止生成 `T`，等待官方澄清。
- 多费率配置的 `req_date` 官网长度为空，保留 `String Y / —`，不从其他接口复制 `String(8)`。
- 多费率查询响应 `conf_list:Object N` 按单对象解析；查询页明确 `pay_way=W` 为微信，不继承配置页 `pay_scene=T` 的文档冲突，也不虚构省略 `fee_sign` 后的返回数量或分页语义。
- 企业用户修改保留法人证件类型与有效期四字段同步填写要求；`file_list` 继续按 String(JSON Array) 传输，不因字段目录的 `[]` 路径改成原生数组。
- 保留企业用户修改请求 `huifu_id` 的企业用户接口/“汇付客户Id”与“直属商户ID”说明冲突；正式请求在角色确认前硬停。
- 保留个人用户修改请求 `huifu_id` 的个人用户接口/“汇付客户Id”与“直属商户ID”说明冲突；正式请求在角色确认前硬停。正式 `cert_validity_type` 仅允许 `0/1`，拒绝请求示例中的 `2`；文件子项长度保持本页64位口径。
- 保留用户业务入驻修改的 `elec_receipt_config` Object/jsonObject字符串、`elec_card_list` 与异步 `resp_business` Object/jsonArray、`delay_flag` 枚举/日期示例及无效回调地址示例冲突；电子回单 wire 未确认前硬停，合法请求示例仍不得提升为 fixture 或默认合同。
- 保留用户列表查询 `user_list_info_list` 正式 `String` 与成功示例原生数组的冲突，不擅自增加 `[]` 或选择 wire；列表项两个 ID 的正式长度2与示例16位冲突同样等待官方确认，请求与成功响应示例分别缺少正式必填的 `request.sign/response.sign`，生产仍必须加签并验签。

## Payment Skill `1.3.4` — `2026-08-16`

### 变更

- 支付 Skill 版本由 `1.3.3` 升至 `1.3.4`，默认来源标识同步由 `hfps/1.3.3` 更新为 `hfps/1.3.4`；支付与进件共同参与时使用 `hfps/1.3.4;hfms/1.0.1`。
- 本次补丁升级不修改冻结的 local-sandbox `r1–r4` 合同、样例包及其 `hfps/1.3.1;sandbox/1.0.1` 来源标识。

## Merchant onboarding Skill `1.0.1` — `2026-08-11`

- 重新下载并复审全部16个商户/用户接口：五个用户接口与既有来源逐字节一致；十一商户接口字段总数仍为2,111，企业进件、个人进件和基本信息修改页仅补全 `activated_products` 的 `01=一体化收款产品` 描述，字段、类型、必填性和嵌套均未变化。

### 新增

- 在现有 `huifu-merchant-onboarding` 中新增企业用户开户、个人用户开户、用户业务入驻、非同名对公结算卡申请状态查询和用户信息查询五个 `/v2/user/*` 接口，版本由 `1.0.0` 升至 `1.0.1`，来源标识同步为 `hfms/1.0.1`。
- 冻结五份官方原文与 SHA-256，机械生成354个完整字段路径：请求161、同步响应169、异步通知24；两套独立解析器逐节点核对22个根表、26个扩展表及全部类型、长度、Y/N/C 和说明。
- 新增五接口三语言 SDK 证据校验，锁定 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24` 的五个专属 Request 类和精确路由，并增加 `sign_user_info` exact-key Object 覆盖运行探针。
- 新增11个用户域真实模型用例和4个跨域路由用例，覆盖 merchant/user 隔离、图片上传禁止用户号、String(JSON)、接口通知/Webhook 隔离及敏感输出。

### 安全

- 纠正由历史源码快照误推的 Java/PHP TLS 硬停：接入方确认当前官方 SDK 无该问题，Java、PHP、Python 在其他检查点通过后均使用对应官方 SDK 发起真实请求。
- 恢复 Java 图片官方 SDK 调用并复核三语言完整发送链路：Java `3.0.40` 通过 `BasePayClient.request(request, true)` / `BasePayClient.upload(request, file)` 使用专用实现；PHP/Python 的生成类仍不等于可用专用支持，但仅该图片接口允许保持 multipart、`data` 加签、TLS 和日志边界的通用 POST/自写 HTTPS 降级。
- 强制使用 `userHuifuId` / `merchantHuifuId` 语义类型隔离；图片上传 `data.huifu_id` 不得使用用户开户返回的用户号。
- 用户业务入驻通知按伙伴平台公共规范锁定 POST/UTF-8、原始 `data` 免排序 RSA 验签、HTTP 200 + `RECV_ORD_ID_` + `req_seq_id`、5秒超时和特定重试；与控台 Webhook 严格隔离并要求状态感知幂等。
- `login_password`、证件号、银行卡号、手机号、地址、邮箱、文件 ID 和 `token_no` 进入发布敏感扫描范围；Java/PHP 敏感调试日志约束继续保留，其中 PHP `DEBUG=true` 仍为生产硬停。

### 修复

- 保留用户业务入驻异步 `huifu_id` 的官网角色冲突：中文名为“汇付客户号”，说明却写“汇付分配的商户号”；禁止在官方确认前直接映射为用户号或商户号。
- 在用户信息查询原子页和共享字段合同中补充 `elec_card_list` 的 Object/jsonArray字符串冲突，并明确保留 `elec_card_list[]` 全部子路径、不得静默选择 wire 容器形态。
- 保留官网曾把 `C` 同时写成“条件必填/条件选填”的来源冲突；执行层按接入方确认统一解释为条件必填，并按字段说明及主体/卡类型矩阵触发。
- 恢复用户信息查询 `req_seq_id` 在同一商户号当天唯一的官网约束，并补充企业/个人基础信息两条 `file_list` 的 Object/jsonArray冲突及完整父路径。
- 补充用户信息查询 `out_settle_acct_type` 的 `01/02/05` 枚举与示例 `0` 冲突，以及 D1 工作日费率说明同时写“生效/不生效”的矛盾；回归同时锁定37个父节点和317个叶节点。
- 二次逐字段复审补回个人开户参数表外 `file_list` 身份证实名认证说明，并让生成器与独立校验器共同锁定页外字段注记；修正 `cert_end_date` 的“类型列/必填列”术语及开户 MCC/地区字段的完整触发条件。
- 显式登记官网9个空说明、15个空长度标量叶字段和2个触发条件未定义的 `C` 字段；补充业务入驻 D1/费率示例冲突、详情地区示例颠倒与缺失支行链接，所有无法裁决项均禁止从同名字段或示例推断。
- 再次复审补回企业参数表外的法人姓名/身份证号实名认证规则，并将其精确绑定到 `request.data.legal_name` 与 `request.data.legal_cert_no`；参数表外注记现为3个字段绑定，独立校验器同时守护4个响应示例异常。
- 收紧外部支行编码索引：`response.data.qry_cash_card_info_list[].branch_code` 的官网原行没有实际链接，不再因同名 `branch_code` 被泛化补成其他路径的支行编码地址。
- 恢复业务入驻 `card_type` 对个人主体的官网原句；随后按接入方确认锁定个人用户仅允许 `1=对私法人`，禁止 `0/2/4`，企业用户按业务条件使用 `0/1/2/4`。
- 示例校验由手写异常扩展为五接口请求/响应全覆盖：解码示例中的 String(JSON) 后锁定189个完整示例路径及指纹，申请状态查询示例也不再处于门禁盲区。
- 补回五份公共返回表的外层父节点约束：官网均标为非必填，业务入驻类型为 String、其余为 Json；随后按接入方确认锁定成功 wire 为必有原生对象，异常响应 DTO 仍允许父节点缺失。
- 接入8份公共平台资料并记录 SHA-256，补齐主动请求、同步/异步加验签、密钥角色、指定字段加解密、接口异步通知、公共编码与控台 Webhook 的协议边界。
- 落实接入方裁决：`C` 为条件必填；个人用户仅允许 `card_type=1`，企业按条件使用0/1/2/4；`card_name/mp` 按卡类型触发；String(JSON)/Object 按说明矩阵逐层编码；申请查询三字段在Y/P/N/F均返回，业务入驻成功返回 `apply_no`，五接口成功 `data` 必有。
- 使用“基础参数汇总”解决取现卡 `branch_code` 原行缺链接问题；来源目录继续保留接口页缺链事实，执行层按完整路径绑定官方银行支行编码下载入口。

## Fifth API / Skill review `2026-07-29` — versions unchanged

### 修复

- 重新抓取用户指定的 47 个官方页面：支付 36 页及进件 10 页逐字节不变；企业进件 live 页变为 SHA-256 `ce61c1f138252b0d7d29302db8d75ebc9337a25f75e38d3ec9a186d7c4e26e28`。
- 企业请求新增 `material_card_info` 父对象及 6 个子字段，企业路径由 170 增至 177，进件总数由 2,104 增至 2,111；经营省市、`card_info`、企业请求 `material_card_info`、电子账户卡及详情响应同名字段按完整父路径隔离。
- 保留官网 `material_card_info` 的 `Object` 类型列和空长度；经接入方确认后以说明列“jsonObject字符串”为 wire 依据，请求与响应均按 `String(JSON Object)` 处理，SDK exact-key 扩展传递整体序列化后的字符串。
- 将支付完整目录的 27 个 `#fragment` 字段链接解析到各自官方来源页并保留原文；对 9 个缺失同名标题的上游锚点补充已确认映射：返回码指向公共返回码全集，聚合下单 `notify_url` 同时指向正扫、反扫通知参数和异步消息简介。
- 区分规范资料、说明截图、固定字段值与运行时 URL：保留 3 处官方配置说明图片和固定 `agreement_url`，脱敏 2 条临时签名对账下载地址；测试域和非 HTTPS 原址保留但增加风险提示。
- 补齐费率查询 `pay_scene` 与企业 `material_card_info` 的字段级外部资料绑定；支付独立验证器开始比较完整官方说明并拒绝相对链接回退、说明截图丢失、签名 URL 泄露和风险标记遗漏。
- 经接入方确认，聚合查询 `method_expand` 解码后为单层平铺结构，参数表中的 `T_*` / `A_*` / `U_*` 行仅是文档分组；正式支付宝付款码枚举为 `A_MICROPAY`，字段说明中第二个 `A_NATIVE: 支付宝付款码` 和成功示例的 `A_IMICROPAY` 均按官网文档错误标注。
- 补充返回码、基础参数、名词解释与异步消息简介四个公共官方来源；公共返回码和接口专属码合并排查，`notify_url` 按 `trade_type` 区分正扫与反扫通知数据面。
- Skill 包版本与来源值保持不变：支付 `1.3.3` / `hfps/1.3.3`，进件 `1.0.0` / `hfms/1.0.0`。

## API refresh `2026-07-28` / Skill version sync `2026-07-29`

### 修复

- `2026-07-29` 第四轮多智能体复审：重新下载 36 个支付页和 11 个进件页，47 个官方来源与锁定快照逐字节一致；修复进件详情 `pay_channel_id_list` 标量 `jsonArray` 丢失 `[]` 的生成器缺陷，并将详情原子页日期同步为当前锁定日期。
- 支付合同修正拆单查询 PHP 未解码 `trans_list`、`quick_online_response`/退款 `dy_response` 编码证据过度强化、聚合查询五个样例专属扩展键遗漏，以及退款 `risk_check_data.ip_addr` 与样例 `ip_address/risk_mng_info` 冲突未披露的问题。
- 支付 Skill 增加 PHP Demo/Composer `DEBUG=true` 私钥泄露硬停；`skill_source` oracle 改为完整 token 匹配并拒绝后缀污染；发布 provenance 升级到 schema 3，强制绑定 refresh ID、刷新合同和对应来源锁，Skill 包版本保持支付 `1.3.3`、进件 `1.0.0`。
- `2026-07-29`：同步更新默认 `skill_source` 与 Skill 包版本：支付为 `hfps/1.3.3` / `huifu-pay-integration 1.3.3`，进件为 `hfms/1.0.0` / `huifu-merchant-onboarding 1.0.0`，双 Skill 来源值固定为 `hfps/1.3.3;hfms/1.0.0`。
- 进件 11 页刷新到 `2026-07-28` 最新来源锁：四页将 `request.data.upper_huifu_id` 同步为 `String(18) C`；企业/个人三项门店图片统一为 `scene_type` 含线下场景时条件必填；详情响应新增 `material_card_info` 七个路径，字段总数增至 2,104。
- 图片上传签名改为特殊合同：并列记录 `sign=true` 元数据、无顶层 `sign` 的示例和官方 Python 免签实现；手写 HTTP 停止猜测签名包络。
- 支付 Skill 修正 Lightning 调试日志、PHP TLS 风险、Java timeout 类型、产品场景边界和托管精确路由；对仍锁定历史 `r4` 的本地沙箱差异增加硬停，不改写冻结资产。
- 支付侧新增 36 页官方来源锁及 16 个 API、2,627 条“接口 + 数据面 + 完整父路径”字段目录；修正 `T_MICROPAY.scene_info`、微信营销数组父级、拆单查询同名字段属性和托管退款查询响应边界，并用独立解析器逐项校验。
- 第三轮复审修正托管支付/关单异步根容器为 `resp_data`、托管退款为 `data`，抖音直连保留“官网未标外层名”的确认状态；字段目录新增合同定位、wire 与 String(JSON) 解码后三种路径，且不再错误删除聚合查询/退款查询响应中的真实 `tx_metadata`。
- 修正聚合 `U_MICROPAY` 示例混入正扫参数的问题；退款查询保留官网表格与成功示例的 `tx_metadata`/顶层字段冲突，并要求生产前确认，不静默选择其一。
- 进件侧修正 `josnArray` 官方拼写错误导致的 `reg_result_list[]` 扁平化，隔离通知与状态查询中的同名协议字段，并对 Java/PHP 关闭 TLS 校验增加生产硬停；后续于 `2026-07-29` 将支付与进件 Skill 包版本分别同步为 `1.3.3`、`1.0.0`。
- 进件字段生成新增完整父路径去重保护，明确经营省市与 `card_info` 银行省市必须分别生成；`skill_source` 增加仅支付、仅进件和双 Skill 的确定性默认值，双 Skill 固定为 `hfps/1.3.3;hfms/1.0.0`，当前来源值与包版本保持同步。
- 修正 PHP `CURLFile` multipart 的源码事实：三个 SDK/Skill 请求头已存在，但请求签名和响应验签仍关闭，因此继续硬停；同时禁止把仅安装、未参与当前请求的 Skill 计入 `skill_source`。
- 回归用例升级为行为断言：仅支付默认值必须为 `hfps/1.3.3`，双 Skill 必须为 `hfps/1.3.3;hfms/1.0.0`，省市载荷必须同时保留顶层经营省市与序列化 `card_info` 银行省市；所有使用 Python `assert` 的校验器在 `-O/-OO` 下直接拒绝运行。
- 对抗终审封堵 `skill_source` 错误组合尾随“不能省略”的极性绕过；代码示例校验扩展到两个 Skill，并禁止在进件 TLS 硬检查点下执行 Java/PHP SDK 网络调用。省市行为用例按六条真实完整路径校验，兼容分离变量及内联 `String(JSON)` 序列化。

## 商户进件能力扩展 - 2026-07-24

### 新增

- 新增商户业务开通修改、商户基本信息修改、商户费率信息查询、商户状态变更和商户短信发送 5 个官方接口 reference。
- 锁定 5 份新增官方原文；字段目录增加 702 个节点，后续第三轮官方刷新再增加 7 个详情响应节点，十一接口合计 2,104 个节点。
- 新增独立于生成器的全量来源解析器，逐项比较接口、方向、完整路径、父对象、数组层级、类型、长度、Y/N/C、说明、来源 URL 和 SHA-256。
- SDK 证据扩展到 9 个有三语言专属 Request 类的 JSON 接口；明确当前三语言 SDK 均没有商户费率查询专属路由。
- 新增进件 Case 76–84、7 个跨路由案例和 11 个安装后快速复测 Prompt，覆盖五个新增接口、支付费率反向路由、补开歧义以及银行卡、银联、微信、支付宝的精确补开接口；真实模型总数增至 115。

### 变更

- 进件 Skill description、精确路由、领域边界、外部资料索引、来源索引、版本策略和发布检查清单扩展到十一接口。
- 进件 Skill 扩展至十一接口，reference 从 22 份增加到 27 份。
- 进件 SDK 证据更新为 Java `3.0.40`、PHP `2.0.30`、Python `2.0.24`；PHP multipart 已补齐 Skill/SDK 请求头，但因本地文件路径仍关闭请求签名和响应验签而继续阻断。

### 修复

- 重新下载并逐字节复核原六接口，六份 SHA-256 均与既有来源锁一致，原 1,395 个节点无新增、删除或属性变化。
- 商户状态变更解析器忽略官方多行 HTML 注释内已明确废弃的 `file_list`，防止把注释文本误生成为合同字段。
- 修正业务补开路由：不能只按“是否完成首次开通”判断；银行卡、银联仍走业务开通，微信、支付宝补开走业务开通修改。
- 修正两套字段解析器对 Markdown 转义竖线的共同盲区，并用不同解析实现和故障夹具锁定类型、长度、必填性不再错列。
- 发布证据重放现在精确核对 suite、加载模式、模型和执行参数；独立发布打包入口会对固定六份真实模型证据做语义重放。
- 新增锁定官网应用场景到 Skill、两个开通原子页和 cases 81–84 的路由语义合同，并拒绝“先写正确免责声明、最终仍选择错误 Endpoint”的复合答案。
- 商户费率查询的 `fee_rate_type` 保留“String + 支持多选 + 数组样式示例”的官方冲突，不擅自决定序列化格式。
- 发布文件集合收紧为 manifest 登记文件，拒绝 `references/` 下的嵌套目录和非 Markdown 文件；真实模型证据在绑定 provenance 前执行语义重放。
- SDK 证据增加用户提供源码树摘要、Java 实际编译/字节码路由检查、PHP 实例化路由检查和 Python 隔离加载调用检查；官方分发 provenance 仍明确为未验证。

## 支付/进件 Skill 拆分 - 2026-07-24

### 新增

- 新增独立 `huifu-merchant-onboarding` Skill，覆盖企业/个人进件、图片、业务开通、详情和申请状态。
- 新增 `skills-manifest.json`、两个 reference manifest、110 文档迁移台账和双包隔离校验。
- 新增官方来源锁及原始快照；字段目录从 1,393 更新到 1,395，只允许新增企业请求和详情响应的股东手机号字段。
- 新增支付 55、进件 20 的历史用例唯一归属，以及 24 个 cross-route 用例。
- 新增两个独立 Skill ZIP 的确定性打包、SHA 和 provenance 校验。
- 新增 Skill 家族架构决策，固化模块边界、未来扩展接口、独立发布和回滚流程。

### 变更

- 支付 Skill 完成支付/进件职责拆分，移除商户进件接口实现，只保留支付前置判断和到进件 Skill 的能力交接。
- 仓库校验器、目录生成器、字段合同、SDK 证据和敏感扫描改为双 Skill 结构。
- `shared-release-checklist.md` 和 `shared-versioning-policy.md` 移入仓库维护合同，不进入任一 Skill ZIP。
- 经多智能体双轴评审补强 Git blob 迁移封存、结构化跨路由判定、带 Skill ID 的 reference 证据、强制 provenance/SHA sidecar 和 manifest 驱动打包。
- 旧 `huifu-pay-integration 1.3.2` 和本地沙箱 `r1-r4` 保持历史冻结，不重写旧版本事实或摘要。

### 修复

- 纠正 2026-07-24 官网新增的 `request.data.share_holder_info_list[].mobile_no` 与 `response.data.share_holder_info_list[].mobile_no`。
- 修复详情查询 `response.data.mer_config_info.online_fee_conf_list[].bus_type` 的跨行官方说明截断，并在来源锁中记录该历史说明纠正。
- 修复支付包敏感扫描盲区、商户标识白名单、重复 ZIP 条目、provenance schema、跨领域正文和迁移关键语义门禁。
- 修复 `huifu_id` 被误解释为账户已创建、Case 75 旧字段统计及 Payment Cases 47–51 引用进件包文档的问题。
- 修复 local-sandbox 对 Python 配置源码文本的隐藏依赖，并让 SDK 源码与严格黄金向量校验直接接受版本化 SDK 父目录。
- 补齐两个 Skill 的负向触发 description、显式隐式调用策略、全部 reference 可达性和聚合/托管 Java SDK 版本区分。
- 修复 `copilot-solution-cards.md` 对仓库级发布清单的运行时引用；迁移台账据此调整为 `KEEP 78 + MOVE 7 + SPLIT 13 + REWRITE 10 + REPO_ONLY 2 = 110`。
- 以 Git `-text` 保存六份官方原始下载字节，确保全新克隆中的来源 SHA 与字段目录可复现。
- 新增独立 transformation review，覆盖 23 份拆分/重写文档的 235 个源章节，并拒绝路由标签与正文自相矛盾的回答。
- 封存 23 份转换来源所对应的 36 个目标文档完整字节；六条 semantic anchor 明确仅是高风险子集，避免把局部锚点误报为全量语义证明。
- 发布门禁拒绝任何已存在的真实模型证据根目录，并把三个 suite 的运行清单和汇总摘要绑定进两个发布 provenance。
- 发布门禁新增全新的持久 `RELEASE_OUTPUT_DIR`，直接保留已绑定模型证据且完成校验的最终 ZIP、SHA 和 provenance。
- 对抗复审补齐 Case 47/50 的原子极性断言，拒绝跨环境/服务商混用、密钥变更不更新配置及否定“未确认分账可按交易退款”的答案；字段合同更新时间改由锁定官方原文机械核对。
- 领域边界门禁从少量端点/类名扩展为 1,395 节点目录派生的进件字段标识集合，防止字段契约片段重新落入支付 Skill。

## [1.3.2] - 2026-07-17

### 新增
- 新增企业进件、个人进件、图片上传、业务开通、商户详情和申请状态 6 份精确 API reference。
- 新增商户进件状态分层、高敏感资料处理、主体类型硬检查点和未确认上传/回调协议边界。
- 新增商户进件回归用例，并纳入真实模型 smoke 覆盖。
- 新增三语言商户进件 SDK 证据矩阵、敏感示例扫描、外部 SDK 源码校验和 r4 契约资产 SHA-256 冻结测试。
- 新增六个商户进件接口的完整字段目录，按“接口 + 请求/响应方向 + 完整路径”展开 1393 条带父容器的字段路径，并保留官网类型、长度、Y/N/C、说明与文档冲突。
- 新增字段目录生成器、来源 SHA-256、完整性校验和字段级外部资料索引。
- 真实模型回归新增 69-75 号用例，smoke 扩展为 25 条，覆盖图片上传签名/验签边界、进件回调字段、业务开通开关、外部资料和完整字段路径。

### 变更
- Skill 来源标识在生产与官方联调环境更新为 `hfps/1.3.3`；local-sandbox 工具升级为 `1.0.1`、报告 schema 升级为 `1.8`，继续使用冻结的 r4 契约资产，沙箱来源为 `hfps/1.3.1;sandbox/1.0.1`。
- local-sandbox 的 `reference_digest_validation` 明确报告冻结快照证据，不再把当前 `1.3.2` Skill 源码误判为 r4 源码；r4 资产继续由 SHA-256 冻结测试保护。
- local-sandbox r4 改为只校验自身登记的历史 Skill 快照，允许后续 Skill 新增 reference，未修改 r4 bundle、端点、fixture 或发布制品。
- 商户进件五个 JSON 接口补充 Java `3.0.39`、PHP `2.0.29`、Python `2.0.23` 的可选 Request 类证据；图片接口仅开放按语言区分的 `file_url` 受控片段，本地文件、响应标识/重试和进件回调继续阻断。
- Java `dg-java-sdk 3.0.39` 的进件调用统一要求在进程初始化、任何 SDK 请求前设置 `BasePay.debug=false`，覆盖五个 JSON 接口和图片 `file_url`，避免公共 `AbstractRequest` 默认调试输出泄露私钥、签名和请求资料；申请状态查询补齐六个基础配置状态的 `P/S/F` 枚举。
- 图片上传合同区分接口元数据 `sign=true` 与未列 `sign` 的 `requestDemo`，不再误称示例含 `sign`；新增五个 JSON 接口 Java 安全初始化真实模型回归与源码顺序门禁。
- 真实模型 forbidden 门禁改为对高风险断言按分句识别前置/后置否定，并在匹配前去除 Markdown 行内代码标记；新增正反边界样例，修复开户请求、回调 ACK、协议地址和前端支付终态的假阳性/假阴性。
- 真实模型证据运行改为干净提交、全新目录和只读隔离工作区，清单绑定提交/源码/逐 case 输出 SHA-256；修复幂等分支 `return true`、权限否定、图片重试边界、详情白名单和 Java 全局日志开关等安全等价表达的误拒。
- 托管 H5/PC 上线检查增加“托管项目状态可交易”输出前自检；业务开通回调边界显式区分已知逐业务 ACK、未确认外层包装、审核/电子协议 ACK 及三类通知的未确认协议项。
- 字段生成先查完整字段目录，再查高风险字段合同；官网示例值不得当作默认值，查询响应的同名开关不得回填业务开通请求。
- 企业/个人进件审核回调统一使用 `async_return_url`，禁止误用支付字段 `notify_url`。
- Java 图片 `file_url` 固定使用 `isPage=true`，保留请求签名、跳过 SDK 响应验签；PHP `CURLFile` multipart 已携带三个 SDK/Skill 头，但因关闭签名/验签继续阻断可运行代码。
- Python `2.0.23` 在缺少业务 `data.huifu_id` 时发送空商户来源头的行为只作 SDK 兼容性提示，不污染业务报文，也不把 SDK 行为抛给客户确认。

## [1.3.1] - 2026-07-03

### 新增
- 新增 `references/shared-local-sandbox.md`，作为 `hf-payment-local-sandbox` 本地协议模拟、报告校验、故障注入和上线前边界的正式入口。
- 主 `SKILL.md` 增加本地沙箱快速路由和“本地沙箱检查卡”，用于回答安装/启动、沙箱报告、通知重放、故障注入和上线前证据衔接问题。
- README、共享总览、版本策略和发布检查清单同步新增本地沙箱能力说明。

### 变更
- Skill 包版本升级为 `1.3.1`；本次升级不改变支付接口契约，`hf-payment-local-sandbox 1.0.0` 仍锁定 contract bundle `huifu-pay-integration-1.3.0-r4`。
- 本地沙箱预览版推进到 `1.0.0`，Skill 中的本地沙箱来源字段同步为 `hfps/1.3.1;sandbox/1.0.0`，公开预览包和更新索引继续使用 `latest-preview.zip` / `latest.json` 固定入口。
- 版本提示策略更新为当前本地 Skill 版本 `1.3.1`，继续明确 Skill 不能主动联网检查或主动推送升级。

### 修复（测评优化轮）
- 修复 P0：补齐 `hosting.payment.splitpay_query` 缺失的 `sample-hosting-splitpay-query-success` 脱敏变体 fixture（由 `import_local_sandbox_samples.py` 从真实脱敏样例重新生成），`go test`、`doctor`、`validate contract` 全部转绿。
- 修复 P1 数据竞争：`handleAggregationCreate/Query`、`handleHostingPreorder/Query` 在 `mu.Unlock()` 后改为仅使用锁内快照 `pc := *payment`，消除并发同键查询时对 `*payment` 的锁外解引用；新增 `TestConcurrentAggregationQueryNoDataRace` 配合 `go test -race` 回归。
- 修复假绿：`scripts/validate_python_contract.py` 补 `__main__` 主入口，独立运行不再静默 exit 0。

### 变更（测评优化轮）
- 新增 `scripts/validate_contract_fixtures.py`：纯 Python、零工具链依赖的 fixture 引用完整性前置快检，已接入 `validate_local_sandbox_all.py`（`go-test` 之前），杜绝 P0 类缺陷在无 Go 环境下被放行。
- 安全加固：`money.parseAmountFen` 增加金额上限防 `int64` 溢出回绕；`pinned_http.doPinned` 禁用 keep-alive 避免空闲连接累积；服务器补 `ReadTimeout/WriteTimeout/IdleTimeout`；新增 `recoverPanic` 中间件包裹 control/gateway 避免单请求 panic 断连；`authorized`/`validCSRF` 改用 `crypto/subtle.ConstantTimeCompare`；`--gateway-host` 非本地时打印安全告警。
- 文档口径统一：幂等键口径以 `shared-async-notify.md` 复合键为 canonical，`hostingpay-faq.md`/`hostingpay-java-tech-spec.md`/`aggregation-java-tech-spec.md` 单键处补"最简形态，完整口径见"指针；`SKILL.md` "字段保真规则"统一为"字段保留规则"并显式命名 `references/shared-request-field-preservation.md`；`shared-overview.md` npm registry 查询补联网守卫；1.3.0 日期口径统一为"基线 06-02 / API 06-10 / Copilot 06-12"；README 显式区分 12 条 runner smoke 与 8 条 canonical 回归集；本地沙箱检查卡"不可验证"项补充"失败态异步通知分叉不可注入、接收侧幂等需接入方自证"。
- `reference-digests.json` 同步重算 5 个改动文件的 sha256。
### 边界
- 本地沙箱通过不代表官方联调通过，不代表具备生产上线条件，也不验证真实商户权限、通道、费率、风控或资金结果。
- Skill 包仍只包含 `SKILL.md`、`agents/` 和 `references/`，不内置沙箱二进制、内部 RC 制品、真实密钥或生产配置。

## [1.3.0] - 2026-06-02

### 新增
- 接入副驾驶 reference 层：接入向导、方案选择、方案卡、存量系统接入、问题解决中心、参数检查、上线检查、官方资料源索引、版本升级策略和最小回归 Prompt。
- 18 张联调方案卡框架，覆盖聚合支付、托管支付、checkout-js、异步通知、上线验收和存量系统增量接入。
- 托管支付新增抖音直连下单和拆单支付订单查询 reference，版本仍保持 `1.3.0`。
- 存量系统改造建议卡，明确建议新增、建议保留、人工确认、补充落库字段、风险点和回归检查。
- 商户进件、接口/数据权限、通道配置、appid/openid、Webhook 和资金运营类 FAQ 脱敏摘要与排查入口。
- 本地官方资料源索引，按业务指引、联调攻略、FAQ 和 AI 技能包技术支持入口做本地覆盖矩阵、不覆盖/转人工菜单与联系方式沉淀；官网 URL 仅用于来源追溯、人工刷新和技术支持入口。
- 用户侧 Skill 版本与升级提示策略，覆盖当前版本、升级触发条件、用户可执行更新方式和能力缺失提示口径。
- 官方 Python SDK 落地口径：聚合支付与托管支付核心场景使用 `dg-sdk 2.0.22` / `dg_sdk`，SDK 版本请求头为 `jpt-sdk_version=python_2.0.22`。
- Windows/CI 门禁入口：`scripts/validate-skills.ps1` 与增强后的 `scripts/validate-skills.sh` 支持静态校验、真实模型 smoke 和全量回归。

### 变更
- 主 `SKILL.md` 从“文档路由”升级为“接入副驾驶”判断入口，先识别用户类型、产品线、阶段、技术栈、端形态、当前目标和是否存量系统。
- 存量系统判断从“用户是否明说存量”调整为结合用户表达和可见项目上下文；“第一次接汇付”但已有订单、支付、回调、退款或状态机代码时按存量业务系统首次接汇付处理。
- 主 `SKILL.md` 增加抖音直连下单与拆单支付订单查询快速路由，明确抖音直连是托管预下单 `pre_order_type=4` 场景，拆单查询不能与普通托管查单混用。
- 主 `SKILL.md` 增加快速路由表、已完成阶段跳过规则、checkout-js 硬检查点、唯一确认问题优先级和 5 类输出卡片模板。
- 问题排查和转人工口径补充官方 AI 技能包技术支持入口，要求先整理脱敏材料，再给联系方式，不把联系方式当作接口文档依据。
- 最终支付状态口径统一为服务端闭环确认：异步通知验签、解析、幂等和状态锁，必要时结合查单二次确认或补偿查询。
- SDK 基线统一为：托管支付 Java `dg-java-sdk 3.0.38`、聚合支付 Java `dg-lightning-sdk 1.0.5`、PHP `huifurepo/dg-php-sdk 2.0.27`、Python `dg-sdk 2.0.22`。
- 来源头示例值统一更新为 `hfps/1.3.0`；`HUIFU_SKILL_SOURCE` 最终上送值保持 `<skill_source>` 原样透传。
- README 更新为 1.3.0 接入向导优先的导航结构，并补充 Python、版本升级和安装后最小复测入口。
- `agents/openai.yaml` 默认提示统一为输出接入方案、联调排查、上线检查、PHP/Java/Python 落地或版本升级提示，并列出本轮实际使用的 references。

### 修复
- `scripts/validate_skills.py` 的 reference 清单纳入 1.3.0 新增文档、Python 文档和 `shared-webhook-signing.md`。
- `scripts/validate_code_examples.py` 在 Windows 缺少 `bash` 时给出可理解的跳过/提示，在 Linux/CI 环境继续强校验，并支持阶段输出、`--language`、`--file`、命令超时和全局超时。
- `scripts/run_real_model_regression.py` 覆盖 1-55 号用例，统一强制 evidence、限制 reference 数量，并为高风险场景增加正则 forbidden 断言；支持 `--smoke`、`--workspace`、`--codex-executable` 和 `CODEX_EXECUTABLE`。
- 发布检查清单补充官方资料源索引采集日期、覆盖状态、不覆盖菜单、Python contract、`.tmp/`、`__pycache__/`、`*.pyc` 发布排除项。
- Python 托管退款示例补充原交易定位键 `org_req_seq_id`，并增加校验规则确保托管退款至少体现 `org_hf_seq_id` / `org_party_order_id` / `org_req_seq_id` 之一。
- 修正 references 中失效的仓库级脚本链接，避免发布校验 broken inline path。

## [1.2.2] - 2026-05-18

### 新增
- 官方 Python SDK 落地 reference：聚合支付 adapter / scenarios、托管支付 adapter / scenarios。
- Python 生产环境变量清单收敛到 Python adapter 文档，不再上传独立 env 示例文件。

### 变更
- SDK 基线更新为托管支付 Java `dg-java-sdk 3.0.38`、PHP `huifurepo/dg-php-sdk 2.0.27`、Python `dg-sdk 2.0.22`。
- Python 来源头口径修正为 `MerConfig.jpt_x_skill_source` 提供 `jpt-x-skill-source`，`jpt-x-skill-huifu_id` 由 SDK 从最终请求 `data.huifu_id` 自动推导。

## [1.2.0] - 2026-04-24

### 新增
- 单 Skill 平铺 references 结构、官方 PHP SDK 落地入口、共享请求头策略、Webhook 验签、PHP 场景文档和校验脚本。

### 变更
- 对外发布结构收敛为单 Skill：`huifu-pay-integration`。
- 托管支付 Java 基线版本更新为 `dg-java-sdk 3.0.38`，聚合支付 Java 基线版本更新为 `dg-lightning-sdk 1.0.5`。
- `HUIFU_SKILL_SOURCE` 最终上送值保持 `<skill_source>`，不再追加 `sys_id`。

## 共享协议层建设 - 2026-04-08

### 新增
- 共享协议层、运行时矩阵、客户前置准备、payload construction、async webhook、Java adapter、版本治理和发布检查清单。

## [1.0.0] - 2026-04-07

### 新增
- 聚合支付与托管支付基础 Skill、参数表、错误码和接口说明。
