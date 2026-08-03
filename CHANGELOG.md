# Changelog

所有重要变更记录在此文件中，格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

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
