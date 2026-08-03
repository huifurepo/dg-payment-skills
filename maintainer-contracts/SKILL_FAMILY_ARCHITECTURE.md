# Skill 家族拆分架构决策

状态：已接受
实施基线：`ff7b6acde574f498fde9c6f0763078b0e2eea3b7`
首次拆分提交：`e12651efb2ed550af9c632d472cb39499a1746de`
当前家族：支付 `1.3.3`、商户进件 `1.0.0`

## 决策

采用“同仓库、同级独立 Skill、无运行时共享包”的 Skill 家族：

```text
skills-manifest.json
├── huifu-pay-integration/          # 支付交易
└── huifu-merchant-onboarding/      # 商户进件
```

用户只安装当前任务所需的完整 Skill 目录。跨域任务可以同时安装多个 Skill，但每个 Skill 必须独立完成入口路由、领域约束、reference 导航、版本说明和安全边界。

不建立第三个运行时 `shared-core` Skill。少量公共政策文档按领域复制并分别维护，仓库门禁检查两个包之间没有相对路径依赖。维护证据统一留在 `maintainer-contracts/`，不进入用户包。

## 采用理由

- 降低单个入口和 references 的认知负担。
- 支付与进件可以独立加载、升级、回滚和发布。
- 用户不必为纯支付问题加载 2,111 个进件字段节点。
- 领域通知、终态、安全规则不会被错误复用。
- 新模块可以沿同一注册、打包和验证接口加入，不需要重新合并旧 Skill。

放弃的方案：

- 继续维护单体 Skill：入口和路由会继续膨胀。
- 把进件作为支付 Skill 的子目录：仍需加载整个父 Skill，不能独立发布。
- 建立运行时共享 Skill：用户必须处理依赖版本，且单包不再自足。

## 模块边界

| 领域 | 所属 Skill | 不得承担 |
| --- | --- | --- |
| 支付下单、查询、关单、退款、对账、checkout-js、支付通知 | `huifu-pay-integration` | 企业/个人开户、材料、业务开通、进件状态 |
| 企业/个人进件、图片上传、业务开通与修改、基础资料修改、费率、状态、短信和进件通知边界 | `huifu-merchant-onboarding` | 支付终态、退款、对账、支付 Webhook |

跨域交接必须显式分段。例如“新商户接 JSAPI”先由进件 Skill 完成主体和业务准备，再由支付 Skill 完成交易接入；不能把进件同步响应当成可交易终态。

## 注册接口

`skills-manifest.json` 是仓库级注册表。每个新 Skill 至少声明：

- 唯一 Skill ID 和同名根目录；
- 领域、版本和 `agents/openai.yaml`；
- reference manifest；
- 入口 reference 数量上限；
- 回归 suite；
- 打包 profile；
- 如有官方冻结源，声明 source lock。

通用结构校验和打包器必须遍历 manifest，不得要求仓库永远恰好只有两个 Skill。领域专用校验可以由 profile 增加，但不能阻断无关 Skill。

## 文档迁移和完整性

拆分前共有 110 份 reference，迁移分类严格守恒：

```text
KEEP 78
MOVE 7
SPLIT 13
REWRITE_PAYMENT 8
REWRITE_ONBOARDING 2
REPO_ONLY 2
```

`reference-migration-ledger.json` 从固定 Git baseline blob 读取源内容，并对首次迁移提交中的每个目标 blob 记录 SHA-256、字节数、行数和标题清单。原样保留项必须源/目标 SHA 完全一致。另用不由 ledger builder 生成的 `reference-transformation-review.json` 逐项覆盖 23 份拆分/重写文档的 235 个 H2/H3 章节（无 H2/H3 时覆盖整份文档），为每个章节记录目标路径、处置方式和评审说明；`reference-transformation-target-lock.json` 封存该评审覆盖的 36 个目标文档当前完整字节，任何正文漂移都会使门禁失败。六条 semantic anchor 只代表额外保护的高风险约束，不代替 235 章节评审；不允许静默删除章节。

商户进件参数采用更强的机械证明：

1. 锁定十一份官方原始字节及 SHA-256。
2. 从原始字节机械生成完整字段目录。
3. 校验接口、方向、父对象、数组路径、类型、长度、Y/N/C 和说明。
4. 从旧 1,393 节点到原六接口当前 1,395 节点只允许两个明确 ADD，并允许来源锁中唯一登记的 `bus_type` 官方说明跨行修复。
5. 五个新增接口机械增加 702 个节点，详情刷新增加 7 个响应节点，本轮企业请求刷新再增加 7 个节点，十一接口合计 2,111；独立解析器逐项比较接口、方向、路径、父对象、数组、类型、长度、Y/N/C、说明、URL 和 SHA。
6. 删除、出现第三个旧接口 ADD、任一旧字段未登记变化或新增接口属性不一致时门禁失败。

## 独立包合同

每个 ZIP 只能包含：

```text
<skill-id>/
├── SKILL.md
├── agents/
└── references/
```

构建必须来自干净提交。打包器同时生成：

- `<skill-id>-<version>.zip`
- `<skill-id>-<version>.zip.sha256`
- `<skill-id>-<version>.provenance.json`

验证器强制检查三者同时存在，并核对 archive SHA、Skill/版本、源提交、仓库状态、manifest SHA、reference manifest SHA、逐文件 SHA 和发布测试证据摘要。正式发布时，两个 provenance 都必须绑定三个真实模型 suite 的 `run-manifest.json` 与 `summary.json`，且带证据的包必须由发布门禁保留在全新的 `RELEASE_OUTPUT_DIR`；临时目录或另行手工打出的无证据包都不是正式发布物。缺少 sidecar、来源为 dirty 或包内出现另一个 Skill 都不能作为发布物。

## 回归矩阵

| Suite | 加载模式 | 目标 |
| --- | --- | --- |
| `payment` | `payment-only` | 纯支付问题可独立回答 |
| `onboarding` | `onboarding-only` | 十一个进件接口可独立回答 |
| `cross-route` | `both` | 正确选择 payment/onboarding/both |

跨路由输出使用结构化 `路由结论`，并要求 reference 证据携带 Skill ID。单领域用例不能把另一个 Skill 误判为主路由；双领域用例必须为两个 Skill 分配独立子目标。

## 新增模块流程

1. 定义领域边界和不得承担的反向边界。
2. 新建同级 Skill 目录，只放入口、agents 和 references。
3. 在 manifest 注册 Skill 和独立 reference manifest。
4. 迁移文档时先冻结源 blob 和迁移台账，再移动、拆分或重写。
5. 为官方接口建立 source lock、机械目录和允许 delta；不能只依赖计数。
6. 新增本领域主回归和跨路由回归。
7. 更新 README、CHANGELOG、版本治理和发布清单。
8. 运行独立打包；确认删除其他 Skill 后仍能使用。
9. 先发布候选包，按 Skill 独立回滚；不得要求家族内所有 Skill 同版本升级。

## 发布与回滚

- 支付和进件分别打 tag、生成包和记录 provenance。
- 仅某一领域变化时，只发布该 Skill。
- 回滚以完整目录替换为单位，不混合新旧 references。
- `skill_source` 显式合同时原样透传；缺失时按当前请求实际参与生成的 Skill 组合使用默认值：仅支付 `hfps/1.3.3`、仅进件 `hfms/1.0.0`、两者都实际参与时 `hfps/1.3.3;hfms/1.0.0`；仅安装或加载但未参与本次生成的不计入。
- 冻结沙箱 `huifu-pay-integration-1.3.0-r4` 不随拆分改名或重算。

## 评审结论

多智能体评审一致认为独立同级 Skill 方案可行，并要求在发布前补强以下门禁：

- baseline 必须读取 Git blob，不能受工作区换行影响；
- cross-route 必须验证主路由，不得只检查 Skill 名称是否出现；
- 同名 reference 必须带 Skill ID 才能作为双包证据；
- provenance 和 SHA sidecar 必须是验证必需项；
- 通用验证与打包必须由 manifest 驱动；
- 独立包不能承诺读取包外维护文件；
- 官方原文必须能机械重生成 2,111 字段目录，并由独立解析器全属性复核。

这些要求已作为当前架构的持续约束，而不是一次性人工检查。
