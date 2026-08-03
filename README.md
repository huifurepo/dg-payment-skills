# 汇付支付 Skills

本仓库提供两个可独立安装、独立升级和独立回滚的汇付 Skill：

| Skill | 版本 | 使用场景 |
| --- | --- | --- |
| `huifu-pay-integration` | `1.3.3` | 聚合支付、托管支付、checkout-js、下单、查单、关单、退款、对账、支付通知、本地沙箱和支付上线 |
| `huifu-merchant-onboarding` | `1.0.0` | 企业/个人商户进件、图片资料、业务开通与修改、基本信息修改、费率、状态、短信及进件通知 |

用户只需加载当前任务相关的 Skill。只有从商户开户持续做到支付交易的跨域任务，才同时加载两个。

## 选择 Skill

| 用户目标 | 加载 |
| --- | --- |
| 发起支付、查单、退款、对账或接 checkout-js | `$huifu-pay-integration` |
| 企业/个人开户、上传资料、开通/修改业务、修改资料、查费率或进件状态 | `$huifu-merchant-onboarding` |
| 新商户开户后立即接支付 | 两个 Skill；先完成进件状态，再交接支付 |
| 本地沙箱演练 | `$huifu-pay-integration`；进件 Skill 不提供沙箱端点 |

两个 Skill 之间没有运行时文件依赖，也不会通过相对路径读取对方的 references。

## 目录

```text
huifu-pay-integration/
├── SKILL.md
├── agents/openai.yaml
└── references/                  # 支付专属，101 份

huifu-merchant-onboarding/
├── SKILL.md
├── agents/openai.yaml
└── references/                  # 进件专属，27 份

maintainer-contracts/            # 仓库维护证据，不进入任何 Skill ZIP
├── payment-references.json
├── onboarding-references.json
├── reference-migration-ledger.json
├── reference-transformation-review.json
├── merchant-onboarding-source-lock.json
└── official-sources/

tests/regression/
├── payment.json                 # 55 个历史主用例
├── onboarding.json              # 20 个历史用例 + 9 个新增接口/路由用例
└── cross-route.json             # 31 个跨 Skill 路由用例
```

`skills-manifest.json` 是两个 Skill 的版本、目录、reference manifest、回归套件和打包配置入口。`maintainer-contracts/`、`scripts/`、`tests/` 和 `local-sandbox/` 都不进入独立 Skill ZIP。

完整的边界决策、迁移证明、打包合同和未来新增模块流程见 `maintainer-contracts/SKILL_FAMILY_ARCHITECTURE.md`。

## 支付 Skill

入口：[huifu-pay-integration/SKILL.md](huifu-pay-integration/SKILL.md)

主要能力：

- 聚合支付和托管支付的 Java、PHP、Python 接入。
- checkout-js 前端组件及服务端终态闭环。
- 下单、查单、关单、退款、对账和支付通知。
- 请求头、签名、验签、幂等和请求字段保留。
- `hf-payment-local-sandbox` 本地演练。

支付前置未满足时，支付 Skill 只说明需要完成账户/渠道准备，并把具体进件实施交给 `$huifu-merchant-onboarding`。

## 商户进件 Skill

入口：[huifu-merchant-onboarding/SKILL.md](huifu-merchant-onboarding/SKILL.md)

精确接口：

| 接口 | reference | 当前字段路径数 |
| --- | --- | ---: |
| 企业商户进件 | `merchant-onboarding-enterprise.md` | 177 |
| 个人商户进件 | `merchant-onboarding-individual.md` | 129 |
| 商户业务开通 | `merchant-onboarding-business-open.md` | 442 |
| 图片上传 | `merchant-onboarding-image-upload.md` | 9 |
| 商户详细信息查询 | `merchant-onboarding-detail-query.md` | 559 |
| 申请单状态查询 | `merchant-onboarding-application-status-query.md` | 93 |
| 商户业务开通修改 | `merchant-onboarding-business-open-modify.md` | 434 |
| 商户基本信息修改 | `merchant-onboarding-basic-info-modify.md` | 199 |
| 商户费率信息查询 | `merchant-onboarding-rate-query.md` | 35 |
| 商户状态变更 | `merchant-onboarding-status-change.md` | 14 |
| 商户短信发送 | `merchant-onboarding-sms-send.md` | 20 |

完整目录共 2,111 个节点，包括 1,218 个请求、713 个同步响应和 180 个通知节点。父对象、数组、类型、长度、Y/N/C、说明和来源 SHA 见：

- `huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md`
- `huifu-merchant-onboarding/references/merchant-onboarding-field-contracts.md`
- `huifu-merchant-onboarding/references/merchant-onboarding-external-resources.md`

当前官方来源快照核验于 `2026-07-29`。十一接口为 2,111 个节点；企业进件相对 `2026-07-28` 快照新增请求 `material_card_info` 七个路径，其余十页逐字节一致。此前四页将 `request.data.upper_huifu_id` 同步为 `String(18) C`，企业/个人门店图片统一为线下场景条件必填，详情响应新增 `material_card_info` 七个路径。相比 1.3.2 的 1,393 字段，旧六接口新增：

- `request.data.share_holder_info_list[].mobile_no`
- `response.data.share_holder_info_list[].mobile_no`

另有一项已记录的历史说明纠正：详情查询
`response.data.mer_config_info.online_fee_conf_list[].bus_type` 补回官方表格跨物理行中的
`5/6` 枚举和示例值；路径、方向、类型、长度和必填性均未变化。
新增五接口机械展开 702 个节点；详情刷新与本轮企业请求刷新各新增 7 个节点，总数变为 2,111。`scripts/validate_onboarding_source_refresh.py` 会拒绝旧六接口字段删除、未登记的新增及任何未在来源锁中登记的属性或说明修改；独立解析器还会逐项比较全部十一接口的字段属性。

## 官方来源

本次进件快照来自用户指定的十一个汇付官方地址：

- 企业商户进件：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md>
- 个人商户进件：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md>
- 商户业务开通：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md>
- 图片上传：<https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json>
- 商户详情查询：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md>
- 申请状态查询：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md>
- 商户业务开通修改：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md>
- 商户基本信息修改：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md>
- 商户费率信息查询：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md>
- 商户状态变更：<https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md>
- 商户短信发送：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md>

原始字节和 SHA 锁保存在 `maintainer-contracts/official-sources/` 与 `merchant-onboarding-source-lock.json`，不会进入 Skill ZIP。

## 安装与更新

Codex 会从仓库级 `.agents/skills/` 和用户级 `~/.agents/skills/` 发现 Skill。ZIP 解压后应保留以 Skill 名命名的根目录，例如：

```text
.agents/skills/huifu-pay-integration/SKILL.md
.agents/skills/huifu-merchant-onboarding/SKILL.md
```

只供当前仓库使用时放入仓库根目录的 `.agents/skills/`；需要跨仓库使用时放入 `~/.agents/skills/`。不要把两个 Skill 的文件直接解压到同一个目录。

### 只安装支付

安装完整的 `huifu-pay-integration/` 目录，不要只复制部分 references。

### 只安装进件

安装完整的 `huifu-merchant-onboarding/` 目录。它不依赖支付 Skill。

### 同时安装

将两个目录分别安装为两个 Skill。不要合并它们的 references，也不要建立共享运行时 Skill。

升级和回滚按 Skill 独立进行：

- 支付 `1.3.3` 可以单独回滚到旧支付包。
- 进件 `1.0.0` 可以单独移除或回滚。
- 旧 `1.3.2` 作为归档回退，不继续作为长期路由 Skill。

`skill_source` 优先使用显式合同值。未配置时按当前请求实际加载并参与生成的 Skill 集合生成确定性默认值：仅支付为 `hfps/1.3.3`，仅进件为 `hfms/1.0.0`，两者都参与为 `hfps/1.3.3;hfms/1.0.0`；仅安装但未参与当前请求不计入，组合顺序固定且分号两侧不加空格。

## 本地沙箱

沙箱只属于支付 Skill，继续使用冻结的 `huifu-pay-integration-1.3.0-r4` 合同、fixtures、digest 和 sample pack。拆分不会改名、重算或向其中加入进件端点。

本地沙箱通过不代表官方联调通过，也不代表具备生产上线条件，不验证真实权限、通道、费率、风控或资金结果。

## 校验

Linux/CI：

```bash
scripts/validate-skills.sh
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\validate-skills.ps1
```

静态门禁包括：

- 两个 Skill 的结构、frontmatter、agents 元数据和 reference manifest。
- 110 份旧 reference 的迁移守恒及原样移动 SHA。
- 无跨 Skill 相对路径、无孤儿 reference。
- 2,111 字段目录、十一份官方来源 SHA、旧六接口守恒和独立全属性比较。
- 支付 36 页官方来源锁、16 个 API 的 2,627 条完整字段路径及独立全属性比较。
- 支付示例代码、字段保留、敏感信息扫描和 Java/PHP TLS 生产硬停。
- 两个独立 ZIP 的构建、文件白名单和内容 SHA。

SDK 源码证据：

```bash
HUIFU_SDK_ROOT=/path/to/sdk scripts/validate-skills.sh
```

发布门禁：

```bash
HUIFU_SDK_ROOT=/path/to/sdk \
REAL_MODEL_EVIDENCE_ROOT=/path/to/new/evidence-directory \
RELEASE_OUTPUT_DIR=/path/to/new/release-directory \
scripts/validate-release.sh
```

发布门禁会分别以 `payment-only`、`onboarding-only` 和 `both` 加载模式执行 55、29、31 个真实模型案例；证据根目录必须在命令启动前不存在，脚本会原子创建它并拒绝复用旧输出。`RELEASE_OUTPUT_DIR` 也必须在命令启动前不存在，脚本最终在该目录保留并校验两个正式 ZIP、SHA 和 provenance。三个 suite 的 `run-manifest.json` 与 `summary.json` 会先被独立重放校验，再把摘要写入两个正式发布包的 provenance。

## 回归测试

规则自检：

```bash
python3 scripts/run_real_model_regression.py --validate-rules-only
```

支付、进件和双包路由分别运行：

```bash
python3 scripts/run_real_model_regression.py \
  --suite payment --load-mode payment-only --timeout 300

python3 scripts/run_real_model_regression.py \
  --suite onboarding --load-mode onboarding-only --timeout 300

python3 scripts/run_real_model_regression.py \
  --suite cross-route --load-mode both --timeout 300
```

75 个历史用例保持唯一主归属：支付 55、进件 20；Case 47 仍属于支付。本版本新增进件 Case 76–84：76–80 行为级覆盖五个新增接口，81–84 固化银行卡、银联、微信、支付宝补开的精确接口边界。`cross-route.json` 的 31 个用例另含 7 个新增接口及相邻支付/补开歧义案例。

## 打包

```bash
python3 scripts/package_skill.py \
  --skill huifu-pay-integration \
  --output-dir dist

python3 scripts/package_skill.py \
  --skill huifu-merchant-onboarding \
  --output-dir dist
```

每次构建输出 ZIP、SHA-256 和 provenance sidecar。ZIP 文件集合严格等于对应 Skill 的 `SKILL.md`、`agents/openai.yaml` 和 reference manifest 登记的直属 Markdown；维护合同、另一个 Skill、沙箱、嵌套目录和测试脚本均不会进入。以上单独的 `package_skill.py` 命令只适合开发构建；正式上传物必须来自 `validate-release.sh` 的 `RELEASE_OUTPUT_DIR`，其 provenance 会把 115-case 三个 suite 的运行清单和汇总文件摘要绑定到 `test_evidence`。

## 安全边界

- 不将私钥、身份证、银行卡、手机号、图片资料或生产流水写入仓库、日志和回答示例。
- Java 进件 SDK 在任何请求前全局设置 `BasePay.debug=false`。
- PHP `CURLFile` 进件图片路径在 `2.0.30` 已携带来源头，但仍因关闭请求签名和响应验签而阻断。
- 未确认的进件通知 ACK、验签原文、HTTP、超时和重试只输出确认清单。
- 同步支付响应、页面回跳和前端 callback 都不是支付终态。
