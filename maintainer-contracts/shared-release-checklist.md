# 发布检查清单

发版前逐项检查 manifest 中登记的每个 Skill。支付与商户进件必须能够独立构建、独立验证、独立升级和独立回滚；用户开户与十二个扩展接口作为进件 `1.0.5` 的子域随同一包发布。

## 结构检查

- `skills-manifest.json` 是否登记全部正式 Skill、版本、领域、reference manifest 和打包 profile
- `huifu-pay-integration/SKILL.md` 与 `huifu-merchant-onboarding/SKILL.md` 是否分别为支付和进件入口；进件入口是否同时精确路由 `/v2/merchant/*` 与 `/v2/user/*`
- 每个 `references/` 是否保持单层平铺，不通过相对路径读取另一个 Skill
- 每个 Skill 顶层是否只包含 `SKILL.md`、`agents/`、`references/`
- reference 新增、删除或改名是否同步对应 `maintainer-contracts/*-references.json`
- `maintainer-contracts/`、`scripts/`、`tests/`、`local-sandbox/` 和另一个 Skill 是否都未进入当前 ZIP
- `reference-migration-ledger.json` 是否仍能从固定 Git 基线和迁移提交验证 110 份历史 reference
- 冻结的 `local-sandbox` 与 `release-preview` 是否相对拆分基线无变化

## 规范检查

- `SKILL.md` frontmatter 是否只使用 Agent Skills 规范允许字段
- `name` 是否与目录名一致
- `description` 是否说明“做什么”和“什么时候用”
- 两个 `description` 是否均不超过300字符（含英文和标点），并保留所属领域及跨 Skill 路由
- `agents/openai.yaml` 是否已生成且与主 Skill 当前口径一致
- 主 `SKILL.md` 是否控制在 `500` 行以内

## 内容检查

- 通用 Java SDK 版本是否与活动 SDK 锁一致：`3.0.41`
- 聚合支付 Java SDK 版本是否与活动 SDK 锁一致：Lightning `1.0.6`
- PHP SDK 版本是否与活动 SDK 锁一致：`huifurepo/dg-php-sdk 2.0.31`
- 支付与进件 Python SDK 是否均与活动 SDK 锁一致：`dg-sdk 2.0.28`
- 前端 JS SDK 是否避免描述为“最新版”，并写清以项目锁定版本接入、升级前查询 npm registry
- `HUIFU_SKILL_SOURCE` 显式值是否原样透传；缺失时是否按当前请求实际参与生成的 Skill 集合分别得到仅支付 `hfps/1.4.0`、仅进件 `hfms/1.0.5`、双 Skill `hfps/1.4.0;hfms/1.0.5`，且仅安装未参与的不计入、组合顺序固定、分号两侧无空格
- 图片是否只把 Java `3.0.41` 判为官方专用实现可用：`file_url` 走 `BasePayClient.request(request, true)`，本地文件走 `BasePayClient.upload(request, file)`，两者互斥且明确请求签名保留、响应验签跳过；PHP/Python 是否依据当前源码保留已知专用实现缺陷，同时仅为 `/v2/supplementary/picture` 放开保持 multipart、`data` 加签、TLS 和日志边界的通用 POST/自写 HTTPS 降级；Python 本次分发缺少 Demo 不视为核心能力缺失，不冒充已检查旧 Demo；图片标识/重试、审核/电子协议回调未确认项是否标 `[需要官方确认]` 并允许继续明确部分
- `merchant-onboarding-field-contracts.md` 是否保留十三接口官网 URL、核验日期、公共信封、第一层请求字段、企业/个人必填 `card_info` 叶子合同与精确状态路径；其他未展开嵌套对象是否明确不得生成完整请求
- `merchant-onboarding-complete-field-catalog.md` 是否与活动十三接口来源锁逐项一致，保留具名路径、父对象、官网来源 URL 与 SHA-256，合计 2,209；各接口数量以机械目录摘要和独立验证器为准
- `onboarding-extension-complete-field-catalog.md` 是否与活动十二接口来源锁逐项一致，合计546，并逐项登记官方冲突；各接口数量以机械目录摘要为准
- `merchant-onboarding-external-resources.md` 是否按字段路径保留外部资料的原始地址，未把回调、APP 下载、二维码、图片等示例/运行时 URL 当作官方资料或默认值
- `user-onboarding-complete-field-catalog.md` 是否与活动九接口来源锁逐项一致，合计611=333请求+220同步响应+58通知；根表、扩展表、父节点和叶节点数量由当前机械目录及独立验证器核对，不沿用旧快照计数
- 用户目录是否保留既有3个实名认证注记及企业修改4个法人证件同步填写注记，共7个参数表外绑定；空说明、空长度和未写 `C` 触发条件的源事实是否按当前完整目录保留而非从示例补齐；是否保留九接口外层 `response.data` 的正式定义，并按 `user-onboarding-field-contracts.md` 与平台合同分层记录当前未解决的示例/编码/条件冲突，关闭已被官网修正的旧冲突
- 用户域是否强制区分 `userHuifuId` 与 `merchantHuifuId`；图片上传是否禁止使用用户开户返回的用户号；用户业务入驻及其修改是否按公共异步规范实现 `data` 原文 RSA 验签、HTTP 200 + `RECV_ORD_ID_` + `req_seq_id`、5秒超时、特定重试与幂等，并与控台 Webhook 隔离
- 官网对 `C` 的历史“条件必填/条件选填”冲突是否保留为来源事实；执行层是否使用接入方确认的“条件必填”，按字段说明及主体/卡类型矩阵触发而非无条件全局必填
- 用户业务入驻异步 `data.huifu_id` 是否按当前正式说明映射为 `userHuifuId`，并禁止误用 `merchantHuifuId`
- 用户信息查询是否保留 `req_seq_id` 同一商户号当天唯一，按接入 wire 矩阵锁定成功外层 JSON Object、内层 String(JSON) 分组、企业/个人 `file_list` 原生数组和 `elec_card_list` 二层 String(JSON Array)，并使用当前8位 `resp_code`、`01` 外扣账户示例和 D1 生效说明
- 发布/CI 是否设置 `HUIFU_SDK_ROOT` 并执行 SDK 源码证据校验；未设置时只能标为本地快检，不能作为发布验收
- 是否已执行 `python3 scripts/scan_sensitive_examples.py`，且商户进件示例没有私钥、真实商户号、图片 URL、身份证、银行卡、手机号或生产流水
- 商户详情响应的证件、银行卡、手机号、图片、`token_no`、二维码和签约链接是否未进入示例、日志或 fixture
- 逐页接口文档里的公共请求参数段，是否都明确写出 `jpt-x-skill-source` 约束
- 十一个已有专属 JSON Request 的逐页文档是否写清 Java/PHP/Python 的 Skill 请求头、扩展字段与业务字段边界；图片页是否区分 Java 官方专用实现可用与 PHP/Python 专用实现不可用，并仅为 `/v2/supplementary/picture` 放开满足 multipart、`data` 加签、TLS、来源互斥和日志边界的受控降级；所有接口是否都禁止为请求头固定、虚构或补空业务 `data.huifu_id`
- 企业、个人和基本信息修改是否明确区分 `data.prov_id/area_id`（经营省市）与 `data.card_info.prov_id/area_id`（银行所在省市），并用完整父路径阻止同名叶字段去重；是否锁定基本信息修改 `card_info.area_id:String(8)` 与首次进件 `String(6)` 的差异
- 企业与个人进件是否统一使用 `async_return_url`，并禁止生成支付字段 `notify_url`；Java 企业进件扩展字段是否落在 `extendInfoMap.async_return_url`
- 聚合支付 PHP 覆盖边界是否已明确为下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- Python 聚合支付覆盖边界是否已明确为下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- Python 托管支付覆盖边界是否已明确为预下单、查询、关单、退款、退款查询、对账
- 进件 Python 文档是否明确 `dg-sdk 2.0.28` 从请求 `data.huifu_id` 推导 `jpt-x-skill-huifu_id`，且 `MerConfig` 不接收 `jpt_x_skill_huifu_id`；第五参数是算法，来源使用 `jpt_x_skill_source` 关键字，SDK 版本头由实际 SDK 生成而非手写覆盖
- Python 文档是否直接列出生产环境变量清单，示例固定 `DGClient.env = "prod"`，SDK 版本请求头为 `jpt-sdk_version`，且不再上传独立 env 示例文件
- Python 示例是否明确不要复制官方 SDK `README.rst` 示例里的测试密钥
- 前端回调不等于最终支付成功的边界是否在主 Skill 和 checkout 文档里都已保留
- 本地沙箱是否明确“本地通过不代表官方联调通过、不代表生产可上线”，且没有把沙箱二进制、内部 RC 制品或真实密钥放入 Skill 包
- 本地沙箱安装/启动口径是否默认指向构建后的 preview 总包 `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/hf-payment-local-sandbox-latest-preview.zip`，并明确普通客户不使用仓库本地二进制、不需要安装 Go 自行构建
- 本地沙箱检查更新索引 `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/hf-payment-local-sandbox-latest.json` 是否由 `dist/release-manifest.json` 生成并与各平台 archive 放在同一公开目录
- 接入向导、方案选择、18 张方案卡、存量系统、问题排查、参数检查、上线检查是否都保留升级人工和拒答边界
- 官方业务指引、联调攻略、FAQ 是否只作为资料源索引与脱敏摘要，没有复制大图、真实商户数据或完整 FAQ 库
- `official-service-source-index.md` 是否已检查采集日期、覆盖状态、不覆盖/转人工菜单和 AI 技能包技术支持入口，并明确官网 URL 只用于来源追溯和人工刷新
- `skill-version-policy.md` 是否已检查当前版本、升级触发条件、用户更新方式，并明确 Skill 不主动联网检查或推送升级
- 支付、商户进件和用户子域的 canonical regression prompts 是否在维护者归档中保留 manifest 登记数量，且不进入安装包

## 上传检查

- 当前独立 Skill 内是否只包含自己的 `SKILL.md`、`agents/`、`references/`
- 是否没有把仓库开发期校验脚本目录打进 Skill 包
- 是否没有把仓库级 `README.md`、`CHANGELOG.md`、`docs/`、`LICENSE` 当作 Skill 必需内容

## 校验检查

- 已执行 `python3 scripts/validate_skills.py`
- 已执行 `python3 scripts/validate_skill_split.py`
- 已执行 `python3 scripts/validate_aggregation_payload_contract.py`
- 已执行 `python3 scripts/validate_request_field_preservation.py`
- 已从活跃44页支付来源锁生成并独立复核24个 API 的2,930个完整节点；历史来源锁及其原始字节保持不变
- 已执行 `python3 scripts/validate_payment_sdk_evidence.py --sdk-root <sdk-root>`，锁定交易分账明细查询的三语言专属 Request、精确路由和扩展覆盖边界
- 已执行 `python3 scripts/validate_merchant_onboarding_complete_catalog.py`
- 已从锁定十三份官方原文执行字段目录生成器 `--check`
- 已执行 `python3 scripts/validate_merchant_onboarding_source_contract.py`，逐项比较全部 2,209 个节点的完整属性
- 已执行 `python3 scripts/validate_onboarding_extension_source_contract.py`，核对十二份来源、546个节点、原子页、SDK 边界和组合锁
- 已从锁定九份用户原文执行 `python3 scripts/generate_user_onboarding_field_catalog.py --locked-source-dir --check`
- 已执行 `python3 scripts/validate_user_onboarding_source_contract.py`，逐项比较全部611个节点的完整属性
- 已执行 `python3 scripts/validate_code_examples.py`
- 已执行 `python3 scripts/scan_sensitive_examples.py`
- 已执行 `python3 scripts/validate_skill_packages.py`，并确认 provenance 与 SHA sidecar 必须存在
- 两个 provenance 均使用 schema `3`；支付1.4.0绑定10-10API锁及刷新记录，进件1.0.5绑定10-08组合锁及刷新记录，两者SDK均绑定已核验10-08锁；历史文件不改写。
- 在提供 SDK 根目录的环境执行 `python3 scripts/validate_merchant_onboarding_sdk_evidence.py --sdk-root <sdk-root>`
- 在提供 SDK 根目录的环境执行 `python3 scripts/validate_user_onboarding_sdk_evidence.py --sdk-root <sdk-root>`，验证九个精确路由、三个修改接口和列表查询的声明字段精确集合及三语言 Object/extend 覆盖运行探针
- 已执行 `git diff --exit-code -- local-sandbox/contracts/`，并通过 r4 契约资产 SHA-256 冻结测试
- Windows 本地已执行 `powershell -ExecutionPolicy Bypass -File scripts\validate-skills.ps1`
- 已校验仓库级回归 Prompt JSON 是合法 JSON
- 已执行 `python3 scripts/run_real_model_regression.py --validate-rules-only`，确认 forbidden 正则与分句极性匹配器有效，边界 fixtures 的安全措辞通过、危险肯定措辞被拒，且不会误伤对应 expected
- 发布门禁设置全新的 `REAL_MODEL_EVIDENCE_ROOT`，并实际运行 `scripts/validate-release.sh`；该命令必须分别以 `payment/payment-only`、`onboarding/onboarding-only`、`user-onboarding/user-onboarding-only`、`cross-route/all-skills` 执行全部159个真实模型案例，其中两个 onboarding suite 都加载同一个进件 Skill，并用 `--skip-run` 重放校验证据语义
- `REAL_MODEL_EVIDENCE_ROOT` 在命令启动前必须不存在；脚本负责创建根目录并拒绝复用任何既有根目录
- `RELEASE_OUTPUT_DIR` 在命令启动前必须不存在；最终上传的 ZIP、SHA 和 provenance 必须直接取自该持久目录，不能另跑无 evidence 的手工打包命令
- 执行真实回归前确认 `.tmp/`、`__pycache__/`、`*.pyc` 不会进入发布包，并先提交相关源文件；正式证据运行必须是干净提交
- 真实模型 smoke 已分别按四个 suite/load-mode 在全新输出目录执行；cross-route 必须覆盖 payment、merchant onboarding 与 user onboarding 主路由
- 真实模型正式回归已按四个 suite/load-mode 组合分别留档；不得复用旧目录补跑
- 两个发布 provenance 的 `test_evidence` 均已绑定四个 suite 的 `run-manifest.json` 与 `summary.json` SHA-256
- 已核对全量目录中的 `run-manifest.json`：`head` 等于被验收提交，`source_clean=true`，源目录与隔离工作区 SHA-256 一致，case 清单完整、每个 `case-*.txt` 的 SHA-256 匹配且最终全部通过
- Windows 或 CI 指定 Codex 可执行文件时使用 `--codex-executable` 或环境变量 `CODEX_EXECUTABLE`
- 复核既有真实模型输出时使用 `python scripts\run_real_model_regression.py --skip-run --output-dir <existing-output-dir>`，不得省略 `--output-dir`；仅接受当前同一提交/evaluator 的完整清单及未篡改输出，该模式仅作诊断，不形成固定提交的正式证据
- 所有相对路径引用都存在
- 删除旧目录后，文档中没有残留旧目录名的失效路径
