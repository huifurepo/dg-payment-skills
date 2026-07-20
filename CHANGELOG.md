# Changelog

所有重要变更记录在此文件中，格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

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
- Skill 来源标识在生产与官方联调环境更新为 `hfps/1.3.2`；local-sandbox 工具升级为 `1.0.1`、报告 schema 升级为 `1.8`，继续使用冻结的 r4 契约资产，沙箱来源为 `hfps/1.3.1;sandbox/1.0.1`。
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
- Java 图片 `file_url` 固定使用 `isPage=true`，保留请求签名、跳过 SDK 响应验签；PHP `CURLFile` multipart 因缺少 Skill 来源头且关闭签名/验签，继续阻断可运行代码。
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

## [1.1.0] - 2026-04-08

### 新增
- 共享协议层、运行时矩阵、客户前置准备、payload construction、async webhook、Java adapter、版本治理和发布检查清单。

## [1.0.0] - 2026-04-07

### 新增
- 聚合支付与托管支付基础 Skill、参数表、错误码和接口说明。
