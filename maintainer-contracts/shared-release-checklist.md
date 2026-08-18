# 发布检查清单

发版前逐项检查 manifest 中登记的每个 Skill。支付与商户进件必须能够独立构建、独立验证、独立升级和独立回滚；用户开户作为进件 `1.0.1` 的子域随同一包发布。

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
- `agents/openai.yaml` 是否已生成且与主 Skill 当前口径一致
- 主 `SKILL.md` 是否控制在 `500` 行以内

## 内容检查

- 商户进件 Java SDK 证据版本是否仍为 `3.0.40`
- 聚合支付 Java SDK 版本是否仍为 `1.0.5`
- 商户进件 PHP SDK 证据基线是否仍为 `huifurepo/dg-php-sdk 2.0.30`
- 商户进件 Python SDK 证据基线是否仍为 `dg-sdk 2.0.24`，且来源头口径一致
- 前端 JS SDK 是否避免描述为“最新版”，并写清以项目锁定版本接入、升级前查询 npm registry
- `HUIFU_SKILL_SOURCE` 显式值是否原样透传；缺失时是否按当前请求实际参与生成的 Skill 集合分别得到仅支付 `hfps/1.3.4`、仅进件 `hfms/1.0.1`、双 Skill `hfps/1.3.4;hfms/1.0.1`，且仅安装未参与的不计入、组合顺序固定、分号两侧无空格
- 图片是否只把 Java `3.0.40` 判为官方专用实现可用：`file_url` 走 `BasePayClient.request(request, true)`，本地文件走 `BasePayClient.upload(request, file)`，两者互斥且明确请求签名保留、响应验签跳过；PHP/Python 是否拒绝已知缺陷的专用生成实现，同时仅为 `/v2/supplementary/picture` 放开保持 multipart、`data` 加签、TLS 和日志边界的通用 POST/自写 HTTPS 降级；图片标识/重试、审核/电子协议回调未确认项是否标 `[需要官方确认]`
- `merchant-onboarding-field-contracts.md` 是否保留十一接口官网 URL、核验日期、公共信封、第一层请求字段、企业/个人必填 `card_info` 叶子合同与精确状态路径；其他未展开嵌套对象是否明确不得生成完整请求
- `merchant-onboarding-complete-field-catalog.md` 是否保留十一接口 177/129/442/9/559/93/434/199/35/14/20 条具名路径、父对象、官网来源 URL 与 SHA-256，且合计严格为 2,111
- `merchant-onboarding-external-resources.md` 是否按字段路径保留外部资料的原始地址，未把回调、APP 下载、二维码、图片等示例/运行时 URL 当作官方资料或默认值
- `user-onboarding-complete-field-catalog.md` 是否严格包含43/34/118/15/144条路径，合计354=161请求+169同步响应+24通知，并锁定22个根表、26个扩展表
- 用户开户目录是否保留企业 `legal_name/legal_cert_no` 与个人 `file_list` 共3个参数表外实名认证注记绑定；是否精确锁定官网9个空说明、15个空长度标量叶字段、2个源表未写触发条件的 `C` 字段、8个请求示例异常、4个响应示例异常与五接口189个示例完整路径；是否保留五接口外层 `response.data` 均为 `N` 的源事实，并把接入方确认的成功必有原生对象作为独立决策层
- 用户域是否强制区分 `userHuifuId` 与 `merchantHuifuId`；图片上传是否禁止使用用户开户返回的用户号；用户业务入驻是否按公共异步规范实现 `data` 原文 RSA 验签、HTTP 200 + `RECV_ORD_ID_` + `req_seq_id`、5秒超时、特定重试与幂等，并与控台 Webhook 隔离
- 官网对 `C` 的历史“条件必填/条件选填”冲突是否保留为来源事实；执行层是否使用接入方确认的“条件必填”，按字段说明及主体/卡类型矩阵触发而非无条件全局必填
- 用户业务入驻异步 `data.huifu_id` 是否保留“汇付客户号/汇付分配的商户号”角色冲突，并禁止在官方确认前直接映射为 `userHuifuId` 或 `merchantHuifuId`
- 用户信息查询是否保留 `req_seq_id` 同一商户号当天唯一，按接入 wire 矩阵锁定成功外层 JSON Object、内层 String(JSON) 分组、企业/个人 `file_list` 原生数组和 `elec_card_list` 二层 String(JSON Array)，并继续保留 `out_settle_acct_type`、D1工作日费率、`resp_code:String(5)`/8位及地区示例冲突
- 发布/CI 是否设置 `HUIFU_SDK_ROOT` 并执行 SDK 源码证据校验；未设置时只能标为本地快检，不能作为发布验收
- 是否已执行 `python3 scripts/scan_sensitive_examples.py`，且商户进件示例没有私钥、真实商户号、图片 URL、身份证、银行卡、手机号或生产流水
- 商户详情响应的证件、银行卡、手机号、图片、`token_no`、二维码和签约链接是否未进入示例、日志或 fixture
- 逐页接口文档里的公共请求参数段，是否都明确写出 `jpt-x-skill-source` 约束
- 九个已有专属 JSON Request 的逐页文档是否写清 Java/PHP 的 Skill 请求头与缺失 `huifu_id` 行为；图片页是否区分 Java 官方专用实现可用与 PHP/Python 专用实现不可用，并仅为 `/v2/supplementary/picture` 放开满足 multipart、`data` 加签、TLS、来源互斥和日志边界的受控降级；所有接口是否都禁止为请求头固定、虚构或补空业务 `data.huifu_id`
- 企业、个人和基本信息修改是否明确区分 `data.prov_id/area_id`（经营省市）与 `data.card_info.prov_id/area_id`（银行所在省市），并用完整父路径阻止同名叶字段去重；是否锁定基本信息修改 `card_info.area_id:String(8)` 与首次进件 `String(6)` 的差异
- 企业与个人进件是否统一使用 `async_return_url`，并禁止生成支付字段 `notify_url`；Java 企业进件扩展字段是否落在 `extendInfoMap.async_return_url`
- 聚合支付 PHP 覆盖边界是否已明确为下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- Python 聚合支付覆盖边界是否已明确为下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- Python 托管支付覆盖边界是否已明确为预下单、查询、关单、退款、退款查询、对账
- Python 文档是否明确 `dg-sdk 2.0.24` 会从请求 `data.huifu_id` 自动推导 `jpt-x-skill-huifu_id`，且 `MerConfig` 不再接收 `jpt_x_skill_huifu_id`
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
- 支付、商户进件和用户子域的 canonical regression prompts 是否保留 manifest 登记数量的安装后快速复测 Prompt

## 上传检查

- 当前独立 Skill 内是否只包含自己的 `SKILL.md`、`agents/`、`references/`
- 是否没有把仓库开发期校验脚本目录打进 Skill 包
- 是否没有把仓库级 `README.md`、`CHANGELOG.md`、`docs/`、`LICENSE` 当作 Skill 必需内容

## 校验检查

- 已执行 `python3 scripts/validate_skills.py`
- 已执行 `python3 scripts/validate_skill_split.py`
- 已执行 `python3 scripts/validate_aggregation_payload_contract.py`
- 已执行 `python3 scripts/validate_request_field_preservation.py`
- 已执行 `python3 scripts/validate_merchant_onboarding_complete_catalog.py`
- 已从锁定十一份官方原文执行字段目录生成器 `--check`
- 已执行 `python3 scripts/validate_merchant_onboarding_source_contract.py`，逐项比较全部 2,111 个节点的完整属性
- 已从锁定五份用户原文执行 `python3 scripts/generate_user_onboarding_field_catalog.py --locked-source-dir --check`
- 已执行 `python3 scripts/validate_user_onboarding_source_contract.py`，逐项比较全部354个节点的完整属性
- 已执行 `python3 scripts/validate_code_examples.py`
- 已执行 `python3 scripts/scan_sensitive_examples.py`
- 已执行 `python3 scripts/validate_skill_packages.py`，并确认 provenance 与 SHA sidecar 必须存在
- 两个 provenance 均使用 schema `3`，记录 `refresh_id`、刷新合同路径/SHA 和当前 Skill 对应 source-lock 路径/SHA；进件 `1.0.1` 必须绑定同时覆盖商户与用户接口的组合来源锁
- 在提供 SDK 根目录的环境执行 `python3 scripts/validate_merchant_onboarding_sdk_evidence.py --sdk-root <sdk-root>`
- 在提供 SDK 根目录的环境执行 `python3 scripts/validate_user_onboarding_sdk_evidence.py --sdk-root <sdk-root>`，验证五个精确路由及三语言 Object/extend 运行探针
- 已执行 `git diff --exit-code -- local-sandbox/contracts/`，并通过 r4 契约资产 SHA-256 冻结测试
- Windows 本地已执行 `powershell -ExecutionPolicy Bypass -File scripts\validate-skills.ps1`
- 已校验仓库级回归 Prompt JSON 是合法 JSON
- 已执行 `python3 scripts/run_real_model_regression.py --validate-rules-only`，确认 forbidden 正则与分句极性匹配器有效，边界 fixtures 的安全措辞通过、危险肯定措辞被拒，且不会误伤对应 expected
- 发布门禁设置全新的 `REAL_MODEL_EVIDENCE_ROOT`，并实际运行 `scripts/validate-release.sh`；该命令必须分别以 `payment/payment-only`、`onboarding/onboarding-only`、`user-onboarding/user-onboarding-only`、`cross-route/all-skills` 执行全部133个真实模型案例，其中两个 onboarding suite 都加载同一个进件 Skill，并用 `--skip-run` 重放校验证据语义
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
