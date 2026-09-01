# 汇付支付 Skills

本仓库提供两个可独立安装、独立升级和独立回滚的汇付 Skill：

| Skill | 版本 | 使用场景 |
| --- | --- | --- |
| `huifu-pay-integration` | `1.3.5` | 聚合支付、托管支付、checkout-js、下单、查单、关单、退款、对账、支付通知、本地沙箱和支付上线 |
| `huifu-merchant-onboarding` | `1.0.2` | 企业/个人商户进件、商户多费率配置及查询，以及企业/个人用户开户、用户业务入驻及修改、申请状态、用户信息查询和企业/个人用户基本信息修改 |

用户只需加载当前任务相关的 Skill。商户进件与分账/结算用户开户都由同一个进件 Skill 路由；只有跨到支付交易领域时才组合加载支付 Skill。

## 选择 Skill

| 用户目标 | 加载 |
| --- | --- |
| 发起支付、查单、退款、对账或接 checkout-js | `$huifu-pay-integration` |
| 企业/个人商户开户、上传商户资料、开通/修改商户业务、查费率或进件状态 | `$huifu-merchant-onboarding` |
| 创建分账/结算企业或个人用户、用户业务入驻或查询用户配置 | `$huifu-merchant-onboarding` |
| 新商户开户后立即接支付 | 两个 Skill；先完成进件状态，再交接支付 |
| 本地沙箱演练 | `$huifu-pay-integration`；进件 Skill 不提供沙箱端点 |

两个 Skill 之间没有运行时文件依赖，也不会通过相对路径读取对方的 references。

## 目录

```text
huifu-pay-integration/
├── SKILL.md
├── agents/openai.yaml
└── references/                  # 支付专属，102 份

huifu-merchant-onboarding/
├── SKILL.md
├── agents/openai.yaml
└── references/                  # 商户进件及用户开户入驻，52 份

maintainer-contracts/            # 仓库维护证据，不进入任何 Skill ZIP
├── payment-references.json
├── onboarding-references.json
├── reference-migration-ledger.json
├── reference-transformation-review.json
├── merchant-onboarding-source-lock.json             # 2026-07-29 历史锁
├── merchant-onboarding-source-lock-2026-08-10.json  # 历史十一接口锁
├── merchant-onboarding-source-lock-2026-08-24.json  # 十二接口历史锁（r1）
├── merchant-onboarding-source-lock-2026-08-24-r2.json # 历史十三接口锁
├── merchant-onboarding-source-lock-2026-08-31.json # 当前十三接口锁
├── merchant-onboarding-1.0.2-source-lock.json       # 1.0.2 r1 历史组合锁
├── merchant-onboarding-1.0.2-r2-source-lock.json    # 历史组合发布锁
├── user-onboarding-source-lock.json                 # 历史五接口锁
├── user-onboarding-source-lock-2026-08-24-r1.json  # 六接口历史锁
├── user-onboarding-source-lock-2026-08-24-r2.json  # 七接口历史锁
├── user-onboarding-source-lock-2026-08-24-r3.json  # 八接口历史锁
├── user-onboarding-source-lock-2026-08-24-r4.json  # 历史九接口锁
├── user-onboarding-source-lock-2026-08-31.json     # 当前九接口锁
├── merchant-onboarding-1.0.2-r3-source-lock.json    # 六用户接口历史组合锁
├── merchant-onboarding-1.0.2-r4-source-lock.json    # 七用户接口历史组合锁
├── merchant-onboarding-1.0.2-r5-source-lock.json    # 八用户接口历史组合锁
├── merchant-onboarding-1.0.2-r6-source-lock.json    # 历史组合发布锁
├── merchant-onboarding-1.0.2-r7-source-lock.json       # 当前组合发布锁
└── official-sources/

tests/regression/
├── payment.json                 # 58 个支付主用例
├── onboarding.json              # 20 个历史用例 + 12 个新增接口/路由/安全用例
├── user-onboarding.json         # 15 个用户开户、入驻、查询与维护用例
└── cross-route.json             # 支付、商户进件与用户开户跨域路由用例
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
| 商户业务开通 | `merchant-onboarding-business-open.md` | 452 |
| 图片上传 | `merchant-onboarding-image-upload.md` | 9 |
| 商户详细信息查询 | `merchant-onboarding-detail-query.md` | 567 |
| 申请单状态查询 | `merchant-onboarding-application-status-query.md` | 93 |
| 商户业务开通修改 | `merchant-onboarding-business-open-modify.md` | 444 |
| 商户基本信息修改 | `merchant-onboarding-basic-info-modify.md` | 199 |
| 商户费率信息查询 | `merchant-onboarding-rate-query.md` | 35 |
| 商户状态变更 | `merchant-onboarding-status-change.md` | 14 |
| 商户短信发送 | `merchant-onboarding-sms-send.md` | 20 |
| 商户多费率配置 | `merchant-onboarding-multifee-config.md` | 27 |
| 商户多费率配置查询 | `merchant-onboarding-multifee-query.md` | 17 |

完整目录共 2,183 个节点，包括 1,261 个请求、742 个同步响应和 180 个通知节点。父对象、数组、类型、长度、Y/N/C、说明和来源 SHA 见：

- `huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md`
- `huifu-merchant-onboarding/references/merchant-onboarding-field-contracts.md`
- `huifu-merchant-onboarding/references/merchant-onboarding-external-resources.md`

当前商户来源快照复审于 `2026-08-31`。十三接口合计2,183个节点；相对上一快照新增 `head_type`、捷行付/线上费率和详情响应字段，删除企业请求旧 `material_card_info.card_type`，并修正多费率长度、String(JSON) 与场景说明。`request.data.upper_huifu_id:String(18) C`、线下场景门店图片条件和其余 `material_card_info` 路径继续保留。相比 1.3.2 的 1,393 字段，旧六接口新增：

- `request.data.share_holder_info_list[].mobile_no`
- `response.data.share_holder_info_list[].mobile_no`

另有一项已记录的历史说明纠正：详情查询
`response.data.mer_config_info.online_fee_conf_list[].bus_type` 补回官方表格跨物理行中的
`5/6` 枚举和示例值；路径、方向、类型、长度和必填性均未变化。
历史新增五接口机械展开702个节点；后续每轮历史来源锁继续保持不可变。`scripts/validate_onboarding_source_refresh.py` 守护历史刷新，当前独立解析器逐项比较全部十三接口的字段属性。

## 用户开户与入驻能力（同属商户进件 Skill）

入口：[huifu-merchant-onboarding/SKILL.md](huifu-merchant-onboarding/SKILL.md)

| 接口 | Endpoint | 字段路径数 |
| --- | --- | ---: |
| 企业用户开户 | `POST /v2/user/basicdata/ent` | 43 |
| 个人用户开户 | `POST /v2/user/basicdata/indv` | 34 |
| 企业用户基本信息修改 | `POST /v2/user/basicdata/ent/modify` | 37 |
| 个人用户基本信息修改 | `POST /v2/user/basicdata/indv/modify` | 26 |
| 用户业务入驻 | `POST /v2/user/busi/open` | 118 |
| 用户业务入驻修改 | `POST /v2/user/busi/modify` | 120 |
| 非同名对公结算卡申请状态查询 | `POST /v2/user/apply/query` | 15 |
| 用户信息查询 | `POST /v2/user/basicdata/query` | 144 |
| 用户列表查询 | `POST /v2/user/list/query` | 17 |

用户子域完整目录共554个节点，包括307个请求、199个同步响应和48个通知节点。进件 Skill 在内部强制区分 `userHuifuId` 与 `merchantHuifuId`，不得因 wire 键同为 `huifu_id` 而复用 DTO。图片上传的 `data.huifu_id` 只支持直属商户号，不支持用户开户返回的用户号。

当前九接口活动快照为 `2026-08-31`；字段总数仍为554，但官网已修正开户文件数组、业务入驻及详情字段、用户号角色、用户列表数组与 ID 长度等合同。独立生成器和独立解析器逐节点核对；用户业务入驻及其修改是两个声明异步通知的接口。

## 官方来源

当前商户进件快照来自用户指定的十三个汇付官方地址：

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
- 商户多费率配置：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md>
- 商户多费率配置查询：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md>

同一进件 Skill 中用户开户、入驻、查询与维护能力的九个官方地址：

- 企业用户开户：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxzc.md>
- 个人用户开户：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxzc.md>
- 用户业务入驻：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrz.md>
- 用户申请单状态查询：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhsqdzt.md>
- 用户信息查询：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhywcx.md>
- 企业用户基本信息修改：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxxg.md>
- 个人用户基本信息修改：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxxg.md>
- 用户业务入驻修改：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrzxg.md>
- 用户列表查询：<https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhlbcx.md>

原始字节和 SHA 锁保存在 `maintainer-contracts/official-sources/`、两个子域来源锁及 `merchant-onboarding-1.0.2-r7-source-lock.json`，不会进入 Skill ZIP。

## 安装与更新

Codex 会从仓库级 `.agents/skills/` 和用户级 `~/.agents/skills/` 发现 Skill。ZIP 解压后应保留以 Skill 名命名的根目录，例如：

```text
.agents/skills/huifu-pay-integration/SKILL.md
.agents/skills/huifu-merchant-onboarding/SKILL.md
```

只供当前仓库使用时放入仓库根目录的 `.agents/skills/`；需要跨仓库使用时放入 `~/.agents/skills/`。不要把不同 Skill 的文件直接解压到同一个目录。

### 只安装支付

安装完整的 `huifu-pay-integration/` 目录，不要只复制部分 references。

### 只安装进件

安装完整的 `huifu-merchant-onboarding/` 目录。它不依赖支付 Skill。

### 同时安装

将所需目录分别安装为独立 Skill。不要合并它们的 references，也不要建立共享运行时 Skill。

升级和回滚按 Skill 独立进行：

- 支付 `1.3.5` 可以单独回滚到旧支付包。
- 进件 `1.0.2` 可以整体回滚到更早包。
- 旧 `1.3.2` 作为归档回退，不继续作为长期路由 Skill。

`skill_source` 优先使用显式合同值。未配置时，支付使用 `hfps/1.3.5`；商户接口和用户接口均使用 `hfms/1.0.2`；两 Skill 同时参与时使用 `hfps/1.3.5;hfms/1.0.2`。

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
- 2,183 字段目录、十三份官方来源 SHA、历史刷新守恒和独立全属性比较。
- 554 字段用户目录、九份官方来源 SHA 和独立双解析器全属性比较。
- 支付 37 页官方来源锁、17 个 API 的 2,656 条完整字段路径及独立全属性比较；交易分账明细查询按 String(JSON Array) 解码并锁定全部数组子路径。
- 支付示例代码、字段保留、敏感信息扫描和三语言官方 SDK-first 门禁；仅图片 `/v2/supplementary/picture` 对 PHP/Python 开放受控通用 POST/自写 HTTPS 降级。
- 三个独立 ZIP 的构建、文件白名单和内容 SHA。

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

发布门禁会分别以 `payment-only`、`onboarding-only`、`user-onboarding-only` 和 `all-skills` 加载模式执行58、32、15、35个真实模型案例；证据根目录必须在命令启动前不存在，脚本会原子创建它并拒绝复用旧输出。`RELEASE_OUTPUT_DIR` 也必须在命令启动前不存在，脚本最终在该目录保留并校验两个正式 ZIP、SHA 和 provenance。四个 suite 的 `run-manifest.json` 与 `summary.json` 会先被独立重放校验，再把摘要写入正式发布包的 provenance。

## 回归测试

规则自检：

```bash
python3 scripts/run_real_model_regression.py --validate-rules-only
```

支付、商户进件、用户开户和跨域路由分别运行：

```bash
python3 scripts/run_real_model_regression.py \
  --suite payment --load-mode payment-only --timeout 300

python3 scripts/run_real_model_regression.py \
  --suite onboarding --load-mode onboarding-only --timeout 300

python3 scripts/run_real_model_regression.py \
  --suite user-onboarding --load-mode user-onboarding-only --timeout 300

python3 scripts/run_real_model_regression.py \
  --suite cross-route --load-mode all-skills --timeout 300
```

当前共140个真实模型案例：支付58、商户进件32、用户开户15、跨域路由35。用户开户套件仍单独运行，但加载的是同一个 `huifu-merchant-onboarding` Skill。

## 打包

```bash
python3 scripts/package_skill.py \
  --skill huifu-pay-integration \
  --output-dir dist

python3 scripts/package_skill.py \
  --skill huifu-merchant-onboarding \
  --output-dir dist

```

每次构建输出 ZIP、SHA-256 和 provenance sidecar。ZIP 文件集合严格等于对应 Skill 的 `SKILL.md`、`agents/openai.yaml` 和 reference manifest 登记的直属 Markdown；维护合同、其他 Skill、沙箱、嵌套目录和测试脚本均不会进入。以上单独的 `package_skill.py` 命令只适合开发构建；正式上传物必须来自 `validate-release.sh` 的 `RELEASE_OUTPUT_DIR`，其 provenance 会把140-case四个 suite 的运行清单和汇总文件摘要绑定到 `test_evidence`。

## 安全边界

- 不将私钥、身份证、银行卡、手机号、图片资料或生产流水写入仓库、日志和回答示例。
- Java、PHP、Python 的常规真实请求均使用对应官方 SDK；接入方已确认当前官方 SDK 不存在此前 Skill 推断的 TLS 问题。Java `BasePay.debug=false` 与 PHP `DEBUG=false` 仍是独立敏感日志要求。
- 图片接口当前只有 Java `3.0.40` 可用官方 `BasePayClient.request/upload` 专用实现；PHP `2.0.30` 的 `CURLFile` 包装路径关闭签验，Python `2.0.24` 的专用 Request 存在字段、文件键和方法签名缺陷，不能直接调用。两种语言可仅对该图片接口使用保持 multipart、`data` 加签、TLS 和日志边界的通用 POST/自写 HTTPS 降级。
- 未确认的进件通知 ACK、验签原文、HTTP、超时和重试只输出确认清单。
- 同步支付响应、页面回跳和前端 callback 都不是支付终态。
