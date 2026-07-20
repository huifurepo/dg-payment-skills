# 发布检查清单

发版前建议逐项检查当前单 Skill 包。

## 结构检查

- `huifu-pay-integration/SKILL.md` 是否是唯一正式 Skill 入口
- `references/` 是否保持单层平铺，不再依赖旧目录跳转
- Skill 包内是否已移除本地 PHP 模板资产和非官方自维护 client
- 是否已经移除二维码等非 Skill 必需资源
- 新增 Python reference 是否已登记到仓库根目录 `./scripts/skill_validation_config.py`
- `shared-webhook-signing.md` 是否已登记到仓库根目录 `./scripts/skill_validation_config.py` 的 `EXPECTED_REFERENCES`
- `shared-local-sandbox.md` 是否已登记到仓库根目录 `./scripts/skill_validation_config.py` 的 `EXPECTED_REFERENCES`
- 1.3.2 商户进件原子 reference、完整字段目录和外部资料索引是否保持单层平铺，并被主 `SKILL.md` 或 `shared-overview.md` 正确引用

## 规范检查

- `SKILL.md` frontmatter 是否只使用 Agent Skills 规范允许字段
- `name` 是否与目录名一致
- `description` 是否说明“做什么”和“什么时候用”
- `agents/openai.yaml` 是否已生成且与主 Skill 当前口径一致
- 主 `SKILL.md` 是否控制在 `500` 行以内

## 内容检查

- 托管支付 Java SDK 版本是否仍为 `3.0.39`
- 聚合支付 Java SDK 版本是否仍为 `1.0.5`
- PHP SDK 包基线是否仍为 `huifurepo/dg-php-sdk 2.0.29`，并且安装、升级、备用下载口径一致
- Python SDK 包基线是否仍为 `dg-sdk 2.0.23`，并且安装、初始化、生产环境变量清单、来源头口径一致；安装或版本核对失败时不得无版本安装或降级
- 前端 JS SDK 是否避免描述为“最新版”，并写清以项目锁定版本接入、升级前查询 npm registry
- `HUIFU_SKILL_SOURCE` 是否都写成 `<skill_source>`；local-sandbox `1.0.1` 的冻结 r4 快照是否明确使用 `hfps/1.3.1;sandbox/1.0.1`，官方联调和生产使用 `hfps/1.3.2`
- 图片 `file_url` 是否严格按 Java multipart 文本字段、PHP/Python JSON 的已核验差异输出受控片段；Java 末参是否固定为 `isPage=true` 并明确请求签名保留、响应验签跳过；PHP `CURLFile` 是否因缺失 Skill 埋点头且关闭签名/验签而阻断；本地二进制文件、图片标识/重试、审核/电子协议回调未确认项是否标 `[需要官方确认]`，且没有生成实现；逐业务通知只在存在 `ord_id` 时说明官网 ACK，不外推验签或重试
- `merchant-onboarding-field-contracts.md` 是否保留六接口官网 URL、核验日期、公共信封、第一层请求字段、企业/个人必填 `card_info` 叶子合同与精确状态路径；其他未展开嵌套对象是否明确不得生成完整请求
- `merchant-onboarding-complete-field-catalog.md` 是否保留六接口 169/129/442/9/551/93 条具名路径、父对象、官网来源 URL 与 SHA-256，且已执行 `python3 scripts/validate_merchant_onboarding_complete_catalog.py`
- `merchant-onboarding-external-resources.md` 是否按字段路径保留外部资料的原始地址，未把回调、APP 下载、二维码、图片等示例/运行时 URL 当作官方资料或默认值
- 发布/CI 是否设置 `HUIFU_SDK_ROOT` 并执行 SDK 源码证据校验；未设置时只能标为本地快检，不能作为发布验收
- 是否已执行 `python3 scripts/scan_sensitive_examples.py`，且商户进件示例没有私钥、真实商户号、图片 URL、身份证、银行卡、手机号或生产流水
- 商户详情响应的证件、银行卡、手机号、图片、`token_no`、二维码和签约链接是否未进入示例、日志或 fixture
- 逐页接口文档里的公共请求参数段，是否都明确写出 `jpt-x-skill-source` 约束
- 逐页接口文档是否都写清“Java 与 PHP 都要求 `jpt-x-skill-source`，且在 `data.huifu_id` 存在时都要带 `jpt-x-skill-huifu_id`；当前 Java SDK 基线自动补，PHP 仅无文件 JSON 主链路在 `MerConfig.skill_source` 已配置时自动补”；企业/个人及图片不传可选 `huifu_id` 时，是否继续阻断 PHP `2.0.29` 的无保护读取，但只把 Python `2.0.23` 的空值商户头作为 SDK 兼容性提示和联调/上线前验证，未把问题抛给客户、未污染业务报文，且没有把 PHP multipart 外推为自动带头
- 企业与个人进件是否统一使用 `async_return_url`，并禁止生成支付字段 `notify_url`；Java 企业进件扩展字段是否落在 `extendInfoMap.async_return_url`
- 聚合支付 PHP 覆盖边界是否已明确为下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- Python 聚合支付覆盖边界是否已明确为下单、扫码交易查询、关单、关单查询、退款、退款查询、对账
- Python 托管支付覆盖边界是否已明确为预下单、查询、关单、退款、退款查询、对账
- Python 文档是否明确 `dg-sdk 2.0.23` 会从请求 `data.huifu_id` 自动推导 `jpt-x-skill-huifu_id`，且 `MerConfig` 不再接收 `jpt_x_skill_huifu_id`
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
- `canonical-regression-prompts.md` 是否保留当前 8 条安装后可快速复测的主路径 Prompt

## 上传检查

- Skill 内是否只包含 `SKILL.md`、`agents/`、`references/`
- 是否没有把仓库开发期校验脚本目录打进 Skill 包
- 是否没有把仓库级 `README.md`、`CHANGELOG.md`、`docs/`、`LICENSE` 当作 Skill 必需内容

## 校验检查

- 已执行 `python3 scripts/validate_skills.py`
- 已执行 `python3 scripts/validate_aggregation_payload_contract.py`
- 已执行 `python3 scripts/validate_request_field_preservation.py`
- 已执行 `python3 scripts/validate_merchant_onboarding_complete_catalog.py`
- 已执行 `python3 scripts/validate_code_examples.py`
- 已执行 `python3 scripts/scan_sensitive_examples.py`
- 在提供 SDK 根目录的环境执行 `python3 scripts/validate_merchant_onboarding_sdk_evidence.py --sdk-root <sdk-root>`
- 已执行 `git diff --exit-code -- local-sandbox/contracts/`，并通过 r4 契约资产 SHA-256 冻结测试
- Windows 本地已执行 `powershell -ExecutionPolicy Bypass -File scripts\validate-skills.ps1`
- 已校验仓库级回归 Prompt JSON 是合法 JSON
- 已执行 `python3 scripts/run_real_model_regression.py --validate-rules-only`，确认 forbidden 正则与分句极性匹配器有效，边界 fixtures 的安全措辞通过、危险肯定措辞被拒，且不会误伤对应 expected
- 执行真实回归前确认 `.tmp/`、`__pycache__/`、`*.pyc` 不会进入发布包，并先提交相关源文件；正式证据运行必须是干净提交
- 真实模型 smoke 已在全新空输出目录执行并留档：`python scripts\run_real_model_regression.py --smoke --timeout 300 --output-dir <new-output-dir>`
- 真实模型全量已在另一个全新空输出目录一次性执行并留档：`python scripts\run_real_model_regression.py --timeout 300 --output-dir <new-output-dir>`；不得复用旧目录补跑
- 已核对全量目录中的 `run-manifest.json`：`head` 等于被验收提交，`source_clean=true`，源目录与隔离工作区 SHA-256 一致，case 清单完整、每个 `case-*.txt` 的 SHA-256 匹配且最终全部通过
- Windows 或 CI 指定 Codex 可执行文件时使用 `--codex-executable` 或环境变量 `CODEX_EXECUTABLE`
- 复核既有真实模型输出时使用 `python scripts\run_real_model_regression.py --skip-run --output-dir <existing-output-dir>`，不得省略 `--output-dir`；仅接受当前同一提交/evaluator 的完整清单及未篡改输出，该模式仅作诊断，不形成固定提交的正式证据
- 所有相对路径引用都存在
- 删除旧目录后，文档中没有残留旧目录名的失效路径
