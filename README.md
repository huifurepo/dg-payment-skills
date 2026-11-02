# 汇付支付 Skills

本仓库提供两个可独立安装、独立升级和独立回滚的汇付 Skill：

| Skill | 版本 | 使用场景 |
| --- | --- | --- |
| `huifu-pay-integration` | `1.5.0` | 延时交易、账户余额与账务查询、余额支付、聚合支付、托管支付、checkout-js、下单、查单、关单、退款、对账、支付通知、本地沙箱和支付上线 |
| `huifu-merchant-onboarding` | `1.1.0` | 企业/个人商户进件、用户开户、子账户开通/修改、电子合同、统一页面进件、下级权限及微信/支付宝 AT 管理 |

用户只需加载当前任务相关的 Skill。商户进件与分账/结算用户开户由进件 Skill 处理，余额与账务查询由支付 Skill 处理；同时涉及开户配置与支付或账务时组合加载两个 Skill。

## 选择 Skill

| 用户目标 | 加载 |
| --- | --- |
| 发起支付、查单、退款、对账或接 checkout-js | `$huifu-pay-integration` |
| 企业/个人商户开户、上传资料、开通/修改业务、电子合同、页面进件、AT 配置/实名或进件状态 | `$huifu-merchant-onboarding` |
| 创建分账/结算企业或个人用户、用户业务入驻或查询用户配置 | `$huifu-merchant-onboarding` |
| 新商户开户后立即接支付 | 两个 Skill；先完成进件状态，再交接支付 |
| 本地沙箱演练 | `$huifu-pay-integration`；进件 Skill 不提供沙箱端点 |

两个 Skill 之间没有运行时文件依赖，也不会通过相对路径读取对方的 references。


## 当前版本更新（2026-10-25）

支付1.5.0新增交易确认、V3确认查询、确认退款、确认退款查询，以及账户余额、账务流水和汇总结果查询；进件1.1.0新增商户子账户开通与修改。九接口按支付7、进件2独立路由。支付当前31 API / 3,334字段路径，进件36 API / 3,534字段路径。

78份既有文档已重新获取：13份变化、65份不变。已同步6份托管合单/子单字段、商户详情开通状态、用户通知与协议/外扣配置及开户sys_id关系注记。SDK仍使用10-08锁定证据；8个新增接口的三语言专属类与路由已核验，汇总查询使用官方通用入口。JSON退款查询无正式响应、汇总查询同步/异步矛盾及通知协议缺口明确保留。

方案及复查见[执行方案](maintainer-contracts/interface-expansion-2026-10-25-plan.md)，逐页差异见[文档检查](maintainer-contracts/official-document-audit-2026-10-25.md)，接口归属、特殊合同与验证见[本轮结果](maintainer-contracts/interface-expansion-2026-10-25.md)。基础与新增目录分别校验，历史来源与沙箱保持不变。源码交付以 Git 提交记录为准，版本及本地检查不代表已完成平台发布、真实资金联调或全量模型评测。

后续[详细复查](maintainer-contracts/interface-expansion-detailed-review-2026-10-25.md)覆盖87份在线来源与本轮完整变更，并解释账户管理五接口为何分配到两个Skill；补齐后的172例规则及正反例自检通过。

## 上一轮版本更新（2026-10-10，历史记录）

支付 skill 1.4.0 新增余额支付、支付查询、退款、退款查询、手续费试算、付款关系提交和发送短信验证码七接口，并提供 Java/PHP/Python 官方 SDK 调用参考。支付目录覆盖24个API、2,930条完整字段路径。短信没有专属 Request，使用精确路由的官方通用入口。

重新下载并比较用户提供的78份官方文档：支付44份、进件34份，发现6份已有文档变更。进件 skill 同步为1.0.5，目录共3,366条路径；修正图片上传、业务开通修改、统一页面查询和支付宝实名结构。旧来源锁及沙箱 r1-r4 保留。Java3.0.41、Lightning1.0.6、PHP2.0.31、Python2.0.28从官方固定提交/制品重新核验；PHP现有TLS事实只作非阻断提示。

第二轮复核78份文档，8份托管支付页变化、70份不变；支付路径总数仍2,930。改动清单、开发及复审见 [第二轮方案](maintainer-contracts/api-review-2026-10-10-plan.md) 和 [复核结果](maintainer-contracts/api-review-2026-10-10.md)。第一轮记录见 [10-08报告](maintainer-contracts/api-review-2026-10-08.md)。活动来源、SDK与版本由 `skills-manifest.json` 选择。本次开发不表示发布或真实资金联调。

第三轮整理两个Skill入口，合并四份重复导览、移出四份维护者回归提示，历史版本页原字节归档；原始来源与完整字段目录保持不变。方案见 [第三轮整理方案](maintainer-contracts/skill-review-2026-10-10-plan.md)。旧发布指南已标明历史适用版本，候选整理结果不代表已发布。

提测前已进行真实模型评测和子代理官方网关联调，修复SDK初始化、响应验签消费边界、过期摘要及通知字段方向。现有资料支持6个接口、9次真实查询/试算请求；Python2.0.28商户费率查询验签兼容问题仍有局部能力缺口，Java3.0.41官方入口已验证成功。严格模型回归仍未全通过，支付/退款资金、短信及真实回调未覆盖。问题、修复与逐轮证据见 [提测前评测报告](maintainer-contracts/pre-submission-live-evaluation-2026-10-10.md) 和 [修复方案](maintainer-contracts/pre-submission-live-evaluation-2026-10-10-plan.md)。

## 上一版商户进件 1.0.4 更新（2026-09-28，历史记录）

上一版商户进件采用 2026-09-22 的 34 接口、3,367 条字段路径（商户 2,210、用户 611、扩展 546），本地 SDK 证据为 Java 3.0.41、PHP 2.0.31、Python 2.0.28。三个电子合同使用 `/v2/agreement/*` 精确路由和官方 SDK 通用入口。当前进件 API/SDK 来源及刷新记录由 `skills-manifest.json` 选择。

该次仅合入商户进件；当时支付维持 1.3.5 及原有来源、SDK 文档和包内容。历史进件复审记录中伴随支付版本只表示当时的工作区快照，不改变支付当前发布状态。

## 目录

```text
huifu-pay-integration/
├── SKILL.md
├── agents/openai.yaml
└── references/                  # 支付专属，119 份

huifu-merchant-onboarding/
├── SKILL.md
├── agents/openai.yaml
└── references/                  # 商户、用户与扩展进件合同，72 份

maintainer-contracts/            # 仓库维护证据，不进入任何 Skill ZIP
├── payment-references.json
├── onboarding-references.json
├── reference-migration-ledger.json
├── reference-transformation-review.json
├── merchant-onboarding-source-lock.json             # 2026-07-29 历史锁
├── merchant-onboarding-source-lock-2026-08-10.json  # 历史十一接口锁
├── merchant-onboarding-source-lock-2026-08-24.json  # 十二接口历史锁（r1）
├── merchant-onboarding-source-lock-2026-08-24-r2.json # 历史十三接口锁
├── merchant-onboarding-source-lock-2026-08-31.json # 历史十三接口锁
├── merchant-onboarding-source-lock-2026-09-22.json # 历史十三接口锁
├── merchant-onboarding-1.0.2-source-lock.json       # 1.0.2 r1 历史组合锁
├── merchant-onboarding-1.0.2-r2-source-lock.json    # 历史组合发布锁
├── user-onboarding-source-lock.json                 # 历史五接口锁
├── user-onboarding-source-lock-2026-08-24-r1.json  # 六接口历史锁
├── user-onboarding-source-lock-2026-08-24-r2.json  # 七接口历史锁
├── user-onboarding-source-lock-2026-08-24-r3.json  # 八接口历史锁
├── user-onboarding-source-lock-2026-08-24-r4.json  # 历史九接口锁
├── user-onboarding-source-lock-2026-08-31.json     # 历史九接口锁
├── user-onboarding-source-lock-2026-09-22.json     # 历史九接口锁
├── onboarding-extension-source-lock-2026-09-22.json # 历史十二扩展接口锁
├── merchant-onboarding-1.0.2-r3-source-lock.json    # 六用户接口历史组合锁
├── merchant-onboarding-1.0.2-r4-source-lock.json    # 七用户接口历史组合锁
├── merchant-onboarding-1.0.2-r5-source-lock.json    # 八用户接口历史组合锁
├── merchant-onboarding-1.0.2-r6-source-lock.json    # 历史组合发布锁
├── merchant-onboarding-1.0.2-r7-source-lock.json    # 1.0.2 历史组合发布锁
├── merchant-onboarding-1.0.3-source-lock-2026-09-22.json       # 历史34接口组合发布锁
└── official-sources/

tests/regression/
├── payment.json                 # 65 个支付主用例
├── onboarding.json              # 44 个商户进件主用例
├── user-onboarding.json         # 15 个用户开户、入驻、查询与维护用例
└── cross-route.json             # 支付、商户进件与用户开户跨域路由用例
```

`skills-manifest.json` 是两个 Skill 的版本、目录、reference manifest、回归套件和打包配置入口。`maintainer-contracts/`、`scripts/`、`tests/` 和 `local-sandbox/` 都不进入独立 Skill ZIP。

完整的边界决策、迁移证明、打包合同和未来新增模块流程见 `maintainer-contracts/SKILL_FAMILY_ARCHITECTURE.md`。

## 支付 Skill

入口：[huifu-pay-integration/SKILL.md](huifu-pay-integration/SKILL.md)

主要能力：

- 聚合支付、托管支付和余额支付的 Java、PHP、Python 接入。
- 余额手续费试算、付款关系和短信验证。
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
| 商户业务开通 | `merchant-onboarding-business-open.md` | 460 |
| 图片上传 | `merchant-onboarding-image-upload.md` | 8 |
| 商户详细信息查询 | `merchant-onboarding-detail-query.md` | 583 |
| 申请单状态查询 | `merchant-onboarding-application-status-query.md` | 93 |
| 商户业务开通修改 | `merchant-onboarding-business-open-modify.md` | 452 |
| 商户基本信息修改 | `merchant-onboarding-basic-info-modify.md` | 199 |
| 商户费率信息查询 | `merchant-onboarding-rate-query.md` | 35 |
| 商户状态变更 | `merchant-onboarding-status-change.md` | 14 |
| 商户短信发送 | `merchant-onboarding-sms-send.md` | 20 |
| 商户多费率配置 | `merchant-onboarding-multifee-config.md` | 27 |
| 商户多费率配置查询 | `merchant-onboarding-multifee-query.md` | 17 |

完整目录共 2,214 个节点，包括 1,276 个请求、758 个同步响应和 180 个通知节点。父对象、数组、类型、长度、Y/N/C、说明和来源 SHA 见：

- `huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md`
- `huifu-merchant-onboarding/references/merchant-onboarding-field-contracts.md`
- `huifu-merchant-onboarding/references/merchant-onboarding-external-resources.md`

当前商户来源快照复审于 `2026-10-25`。十三接口合计2,214个节点；本轮商户详情新增5个业务开通状态。历史图片与状态合同继续保留。费率查询改原生Array<string>；企业补充结算卡Y与条件描述、支行号长度8与示例12仍有冲突。`upper_huifu_id`角色、门店照片和独立卡父路径不变；股东手机号继续保留，但详情不再声明股东cert_no：

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
| 用户业务入驻 | `POST /v2/user/busi/open` | 149 |
| 用户业务入驻修改 | `POST /v2/user/busi/modify` | 151 |
| 非同名对公结算卡申请状态查询 | `POST /v2/user/apply/query` | 21 |
| 用户信息查询 | `POST /v2/user/basicdata/query` | 166 |
| 用户列表查询 | `POST /v2/user/list/query` | 17 |

用户子域完整目录共644个节点，包括345个请求、227个同步响应和72个通知节点。进件 Skill 在内部强制区分 `userHuifuId` 与 `merchantHuifuId`，不得因 wire 键同为 `huifu_id` 而复用 DTO。图片上传的 `data.huifu_id` 只支持直属商户号，不支持用户开户返回的用户号。

当前九接口活动快照为 `2026-10-25`；本轮6页变化，新增33条路径与6项属性变化，补充开户sys_id关系注记。通知新增E/A/U/Z类型、协议列表和失败原因，account_info改为String(JSON Object)，agreement_info_list为String(JSON Array)；查询同名account_info仍为原生Object，必须按方向处理；双Y手续费与“至少一个”描述冲突仍保留。用户业务入驻及其修改是两个声明异步通知的接口。

## 进件扩展能力（同属商户进件 Skill）

| 接口 | Endpoint | 字段路径数 |
| --- | --- | ---: |
| 电子合同重发 | `POST /v2/agreement/elect/signurl/resend` | 13 |
| 电子合同列表查询 | `POST /v2/agreement/apply/list` | 40 |
| 电子合同拒签 | `POST /v2/agreement/elect/rejectsign` | 12 |
| 开通下级商户权限配置 | `POST /v2/merchant/busi/head/config` | 141 |
| 商户统一进件（页面版） | `POST /v2/merchant/url/forward` | 59 |
| 统一进件页面版查询 | `POST /v2/merchant/busi/status/query` | 51 |
| 微信商户配置 | `POST /v2/merchant/busi/config` | 31 |
| 微信商户配置查询 | `POST /v2/merchant/busi/config/query` | 32 |
| 微信实名认证 | `POST /v2/merchant/busi/realname` | 51 |
| 微信实名认证状态查询 | `POST /v2/merchant/busi/realname/query` | 22 |
| 支付宝实名申请提交 | `POST /v2/merchant/busi/ali/realname/apply` | 69 |
| 支付宝实名申请单查询 | `POST /v2/merchant/busi/ali/realname/query` | 25 |

扩展目录共546个节点（请求340、同步响应161、异步45）。九个商户/AT路由有专属Request；三个电子合同的新agreement路由没有匹配专属类，使用经验证的官方SDK通用入口，不得用旧invoice类替代，也不生成手写生产HTTP。当前真实冲突保留在 `onboarding-extension-field-contracts.md`。

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

新增十二接口的官方地址及 SHA 见 `onboarding-extension-official-service-source-index.md`。原始字节和 SHA 锁保存在 `maintainer-contracts/official-sources/`、三个子域来源锁及当前 `merchant-onboarding-1.1.0-source-lock-2026-10-25.json`，不会进入 Skill ZIP。用户列出的交易分账明细查询仍归支付 Skill；本轮在线SHA保持一致，仍只由支付skill负责；支付本轮升级1.5.0并新增延时交易四接口与账户查询三接口。

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

- 支付 `1.5.0` 可以单独回滚到旧支付包。
- 进件 `1.1.0` 可以整体回滚到 `1.0.4`、`1.0.3` 或更早包。
- 旧 `1.3.2` 作为归档回退，不继续作为长期路由 Skill。

`skill_source` 优先使用显式合同值。未配置时，支付使用 `hfps/1.5.0`；商户、用户和扩展接口均使用 `hfms/1.1.0`；两 Skill 同时参与时使用 `hfps/1.5.0;hfms/1.1.0`。

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
- 2,214 字段商户目录、十三份官方来源 SHA、历史刷新守恒和独立全属性比较。
- 644 字段用户目录、九份官方来源 SHA 和独立双解析器全属性比较。
- 546 字段扩展目录、十二份官方来源 SHA、当前官方冲突、SDK 边界及组合发布锁校验。
- 支付 44 页官方来源锁、24 个基础 API 的 3,096 条完整字段路径及独立全属性比较；交易分账明细查询按 String(JSON Array) 解码并锁定全部数组子路径。
- 支付示例代码、字段保留、敏感信息扫描和三语言官方 SDK-first 门禁；仅图片 `/v2/supplementary/picture` 对 PHP/Python 开放受控通用 POST/自写 HTTPS 降级。
- 新增九接口的368条字段与原始来源独立比较、八个专属SDK×三语言精确路由、Python序列化和覆盖行为离线探针。
- 两个独立 ZIP 的构建、文件白名单和内容 SHA，provenance额外绑定新增接口锁。

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

发布门禁会分别以 `payment-only`、`onboarding-only`、`user-onboarding-only` 和 `all-skills` 加载模式执行72、46、15、39个真实模型案例；证据根目录必须在命令启动前不存在，脚本会原子创建它并拒绝复用旧输出。`RELEASE_OUTPUT_DIR` 也必须在命令启动前不存在，脚本最终在该目录保留并校验两个正式 ZIP、SHA 和 provenance。四个 suite 的 `run-manifest.json` 与 `summary.json` 会先被独立重放校验，再把摘要写入正式发布包的 provenance。

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

当前共172个真实模型案例：支付72、商户进件46、用户开户15、跨域路由39。用户开户套件仍单独运行，但加载的是同一个 `huifu-merchant-onboarding` Skill；商户进件套件已纳入新增十二接口的逐接口场景。本轮另补九个延时/账户接口案例及四个账户跨域路由案例；它们接入运行器与来源指纹，本轮仅执行规则及正反例自检。

## 打包

```bash
python3 scripts/package_skill.py \
  --skill huifu-pay-integration \
  --output-dir dist

python3 scripts/package_skill.py \
  --skill huifu-merchant-onboarding \
  --output-dir dist

```

每次构建输出 ZIP、SHA-256 和 provenance sidecar。ZIP 文件集合严格等于对应 Skill 的 `SKILL.md`、`agents/openai.yaml` 和 reference manifest 登记的直属 Markdown；维护合同、其他 Skill、沙箱、嵌套目录和测试脚本均不会进入。以上单独的 `package_skill.py` 命令只适合开发构建；正式上传物必须来自 `validate-release.sh` 的 `RELEASE_OUTPUT_DIR`，其 provenance 会把159-case四个 suite 的运行清单和汇总文件摘要绑定到 `test_evidence`。

## 安全边界

- 不将私钥、身份证、银行卡、手机号、图片资料或生产流水写入仓库、日志和回答示例。
- Java、PHP、Python 的常规真实请求均使用对应官方 SDK；进件对本次本地 SDK 的 TLS 风险保留事实和非阻断咨询提示；支付已同步核验相同 SDK 基线。Java `BasePay.debug=false` 与 PHP `DEBUG=false` 仍是独立敏感日志要求。
- 进件图片接口当前只有 Java `3.0.41` 可用官方 `BasePayClient.request/upload` 专用实现；PHP `2.0.31` 的 `CURLFile` 包装路径关闭签验，Python `2.0.28` 的专用 Request 存在字段、文件键和方法签名缺陷，不能直接调用。两种语言可仅对该图片接口使用保持 multipart、`data` 加签、TLS 和日志边界的通用 POST/自写 HTTPS 降级。
- 未确认的进件通知 ACK、验签原文、HTTP、超时和重试只输出确认清单。
- 同步支付响应、页面回跳和前端 callback 都不是支付终态。
