# 汇付支付 Skill 产品包

这是一个面向第三方客户的 Huifu 接入 Skill 包，用来帮助开发者借助 AI 工具完成汇付支付 / 斗拱 SDK 接入开发、联调排查、本地沙箱演练和上线检查。

README 按 **接入向导 -> 方案选择 -> 产品线 -> 开发任务 -> 技术栈** 导航，先帮你定位入口，再进入对应文档。当前仓库已收敛为单 Skill：

- 正式 Skill：`huifu-pay-integration`
- 服务端技术栈：Java、PHP、Python；C#、Go 保留入口说明
- 前端支付组件：Node.js / Browser
- 产品能力主线：聚合支付、托管支付、前端支付组件、抖音直连、拆单支付查询
- 1.3.1 Copilot 能力：首次接入、存量/疑似存量识别、存量系统增量接入、联调方案卡、问题解决中心、FAQ 排查、参数检查、本地沙箱入口、上线检查和技术支持升级

选择建议：优先使用聚合支付，接入更快、更轻量；当你需要托管收银台、项目制预下单或前端 checkout 能力时，再进入托管支付和前端支付组件路径。

## 如何开始

下文中的 `references/...` 均指 `huifu-pay-integration/references/...`。

### 1. 先按接入目标定位

| 目标 | 从这里开始 | 说明 |
| --- | --- | --- |
| 第一次接入，不知道怎么选 | `references/copilot-onboarding.md` | 识别首次/存量、产品线、阶段、技术栈和当前目标 |
| 需要推荐聚合/托管/checkout-js | `references/copilot-solution-selection.md` | 输出为什么选、为什么暂不选其他方案 |
| 需要联调步骤和必测项 | `references/copilot-solution-cards.md` | 18 张方案卡，覆盖 P0/P1 场景 |
| 已有订单系统或当前项目已有订单/支付/回调代码要接汇付 | `references/copilot-existing-system.md` | 输出新增、保留、人工确认和状态映射；第一次接汇付不等于新建空项目 |
| 报错、参数、返回或代码片段排查 | `references/copilot-troubleshooting-playbooks.md`、`references/copilot-parameter-review.md` | 输出问题判断、检查顺序、修复动作和验证方式 |
| 商户进件、接口权限、通道配置、appid/openid、Webhook FAQ | `references/merchant-onboarding-faq.md`、`references/copilot-troubleshooting-playbooks.md` | 基于 FAQ 目录的脱敏规则化摘要，不包含原始 FAQ 文件 |
| 本地沙箱演练、报告校验或故障注入 | `references/shared-local-sandbox.md` | 使用 local-sandbox 做正式联调前的本地协议模拟和自检报告 |
| 上线前检查 | `references/copilot-go-live-checklist.md` | 输出通用和存量系统上线检查清单 |
| 查询当前版本或更新 Skill | `references/skill-version-policy.md` | 说明当前本地版本、升级触发条件和用户可执行更新方式 |
| 安装后快速复测 | `references/canonical-regression-prompts.md` | 8 条随 Skill 分发的最小回归 Prompt |

### 2. 再按产品线定位

| 产品线 | 适合什么场景 | 从这里开始 |
| --- | --- | --- |
| 汇付支付集成（总入口） | 第一次接入汇付，需要先判断产品线、开发任务和阅读顺序 | `huifu-pay-integration/SKILL.md` |
| 聚合支付 | 标准支付场景，想尽快完成服务端接入 | `references/aggregation-quickstart.md` |
| 托管支付（服务端） | 需要项目制预下单、托管收银台、查询 / 退款闭环 | `references/hostingpay-quickstart.md` |
| 前端支付组件 | 需要在商户自有页面嵌入 checkout 或单支付按钮 | `references/checkout-js.md` |

### 3. 再按开发任务进入

| 开发任务 | 聚合支付 | 托管支付 / 前端支付组件 |
| --- | --- | --- |
| 初始化 / 公共配置 | `references/aggregation-base.md` | `references/hostingpay-base.md` |
| 下单 / 预下单 | `references/aggregation-order.md` | `references/hostingpay-preorder.md`；抖音直连补 `references/hostingpay-preorder-douyin-direct.md` |
| 查询 / 关单 / 对账 | `references/aggregation-query.md` | `references/hostingpay-query.md`；拆单支付查询补 `references/hostingpay-query-splitpay.md` |
| 退款 | `references/aggregation-refund.md` | `references/hostingpay-refund.md` |
| 收银台组件接入 / 单支付按钮 | 不适用 | `references/checkout-js.md` |

### 4. 最后按技术栈落地

| 技术栈 | 推荐入口 | 说明 |
| --- | --- | --- |
| Java | `references/shared-server-sdk-matrix.md` | 聚合支付和托管支付都有稳定基线 |
| PHP | `references/shared-server-sdk-matrix.md` | 聚合支付核心主链路和托管支付核心场景已覆盖 |
| Python | `references/shared-server-sdk-matrix.md` | 聚合支付核心主链路和托管支付核心场景已覆盖，当前 Skill 基线为 `dg-sdk 2.0.22`，生产环境变量清单见 Python adapter 文档 |
| C# / Go | `references/shared-server-sdk-matrix.md` | 当前只保留入口说明 |
| Node.js / Browser | `references/shared-frontend-sdk-matrix.md` | 前端 JS SDK 能力矩阵 |
| Node.js / Browser | `references/checkout-js.md` | 嵌入 checkout / 单支付按钮的实际入口 |

## 产品线说明

### 聚合支付

聚合支付是一条服务端主线，适合标准支付接入和快速上线。

推荐阅读顺序：

```text
references/aggregation-quickstart.md
  -> references/aggregation-base.md
  -> references/aggregation-order.md
  -> references/aggregation-query.md
  -> references/aggregation-refund.md（按需）
```

### 托管支付

托管支付的服务端主线负责 SDK 初始化、预下单、查询、关单、对账和退款。

推荐阅读顺序：

```text
references/hostingpay-quickstart.md
  -> references/hostingpay-base.md
  -> references/hostingpay-preorder.md
     -> references/hostingpay-preorder-douyin-direct.md（抖音直连时）
  -> references/hostingpay-query.md
     -> references/hostingpay-query-splitpay.md（拆单支付订单查询时）
  -> references/hostingpay-refund.md（按需）
```

### 前端支付组件

前端支付组件用于在商户自定义页面中嵌入 checkout 组件或单支付按钮，让商户自己控制页面布局、品牌样式和交互流程。

必须注意：前端 callback 不等于最终支付成功，最终订单状态必须由服务端闭环确认：异步通知先验签、解析、幂等和状态锁，再结合查单二次确认或补偿查询更新订单。

推荐主链路：

```text
服务端预下单：references/hostingpay-preorder.md
  -> 前端渲染 checkout / 按钮：references/checkout-js.md
  -> 服务端最终确认闭环：references/hostingpay-async-webhook.md + references/hostingpay-query.md
```

### 本地沙箱

本地沙箱 `hf-payment-local-sandbox` 用于正式联调前的本地协议模拟、闭环演练、故障注入和自检报告。当前 Skill `1.3.1` 只提供使用入口和边界说明，不把沙箱二进制或内部 RC 制品放入 Skill 包。

面向客户使用时，默认引导下载构建后的预览总包，不引导使用仓库里的本地编译二进制，也不要求客户安装 Go 后自行构建：

```text
https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/hf-payment-local-sandbox-latest-preview.zip
```

该 URL 当前对应 `hf-payment-local-sandbox-1.0.0-preview.zip` 的重命名分发包，内含各平台 archive、启动器、`USAGE.md`、SBOM、provenance、manifest 和 SHA256 清单。

本地沙箱控制台检查更新使用公开索引：

```text
https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/hf-payment-local-sandbox-latest.json
```

该索引由 `scripts/generate_local_sandbox_update_index.py` 从 `dist/release-manifest.json` 生成，和各平台 archive 放在同一公开目录下。

推荐阅读顺序：

```text
references/shared-local-sandbox.md
  -> references/shared-async-notify.md（通知/回包/幂等）
  -> references/copilot-go-live-checklist.md（本地通过后的上线前检查）
```

固定边界：本地沙箱通过不代表官方联调通过，不代表具备生产上线条件，也不验证真实商户权限、通道、费率、风控或资金结果。

## 共享资料层

这些共享资料不再分散在多个 Skill 中重复维护：

| 资料 | 作用 |
| --- | --- |
| `references/shared-signing-v2.md` | V2 签名规则 |
| `references/shared-async-notify.md` | 接口 `notify_url` 异步通知规则 |
| `references/shared-webhook-signing.md` | 控台 Webhook 终端密钥与 MD5 验签规则 |
| `references/shared-request-header-policy.md` | 请求头与 skill 来源字段规则 |
| `references/shared-local-sandbox.md` | 本地沙箱使用、报告、故障注入和上线前边界 |
| `references/shared-server-sdk-matrix.md` | 服务端多语言矩阵 |
| `references/shared-frontend-sdk-matrix.md` | 前端 JS SDK 矩阵 |
| `references/shared-versioning-policy.md` | 版本治理规则 |
| `references/skill-version-policy.md` | 用户侧版本提示和更新方式 |
| `references/shared-release-checklist.md` | 发布检查清单 |
| `references/official-service-source-index.md` | 业务指引、联调攻略、FAQ、AI 技能包技术支持联系方式的官方资料源索引 |
| `references/merchant-onboarding-faq.md` | 商户进件、接口/数据权限、通道、appid/openid、Webhook 和运营边界 FAQ 摘要 |
| `references/canonical-regression-prompts.md` | 最小回归 Prompt |

## Skill 内部结构

```text
huifu-pay-integration/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── copilot-*.md
    ├── shared-*.md
    ├── aggregation-*.md
    ├── hostingpay-*.md
    └── checkout-js-*.md
```

市场上传包不包含 `.env`、`*.env`、`*.example` 这类环境变量示例文件。Python 生产环境变量只在 `references/aggregation-python-adapter.md` 和 `references/hostingpay-python-adapter.md` 中以清单形式维护。

## 当前版本事实

| 项目 | 当前口径 |
| --- | --- |
| Skill 包版本 | `1.3.1` |
| 1.3.1 local-sandbox refresh | `2026-06-29`，新增本地沙箱入口、报告边界和上线前证据衔接 |
| 1.3.0 API refresh | `2026-06-10`，补充抖音直连下单、拆单支付订单查询和聚合字段刷新 |
| 1.3.0 Copilot/support refresh | `2026-06-12`，补强存量项目识别、FAQ 排查、转人工材料和 AI 技能包技术支持入口 |
| 本地沙箱工具 | `hf-payment-local-sandbox 1.0.0`，contract bundle `huifu-pay-integration-1.3.0-r4` |
| 托管支付 Java SDK 常量版本 | `dg-java-sdk 3.0.38` |
| 聚合支付 Java SDK 版本 | `dg-lightning-sdk 1.0.5` |
| PHP SDK 包 | `huifurepo/dg-php-sdk 2.0.27` |
| Python SDK 包 | `dg-sdk 2.0.22`，import 名为 `dg_sdk` |
| 新增接口 SDK 兼容性 | 抖音直连是托管预下单 `pre_order_type=4` 场景，三语言使用托管预下单 request；拆单支付订单查询 Java/PHP/Python 均有 `V2TradeHostingPaymentSplitpayQueryRequest` |
| Python 生产环境变量 | 见 `references/aggregation-python-adapter.md` 与 `references/hostingpay-python-adapter.md` |
| 前端收银台 JS SDK | `@dg-elements/js-sdk`，接入时以项目锁定版本为准 |

## 开发校验

Windows 本地静态门禁：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\validate-skills.ps1
```

Linux / CI 静态门禁：

```bash
scripts/validate-skills.sh
```

真实模型回归需要可执行的 Codex CLI。smoke 与全量命令分别为：

```powershell
python scripts\run_real_model_regression.py --smoke --timeout 300
python scripts\run_real_model_regression.py --timeout 300
```

真实模型回归的 smoke 子集为 12 条（`run_real_model_regression.py:21` 的 `SMOKE_CASE_IDS`），覆盖首次接入/硬检查点/PHP 落地/禁绕验签/上线检查/字段保留/抖音直连/splitpay/合单/对账/权限/存量系统等高价值面；随 Skill 分发的 `references/canonical-regression-prompts.md` 是独立的 8 条最小回归 Prompt，两者为不同集合。

## 如何更新 Skill

Skill 不会主动联网检查或推送升级。用户看到版本差异、能力缺失或维护者发布新包时，按实际分发方式更新：

- Git 仓库使用：从维护方仓库拉取最新版本，重新加载或重启使用 Skill 的客户端，再确认 `huifu-pay-integration/SKILL.md` 中的版本事实。
- 本地目录复制：用维护方发布的新 `huifu-pay-integration` 目录整体覆盖旧目录，不要只混合替换部分 `references/` 文件。
- 内部发布包：下载维护方发布的新包后替换 Skill 目录；无法确认版本时联系维护者核验。

升级前后都不要把商户密钥、真实订单号、真实流水或生产配置写入 Skill 包。

## 文档说明

- 优先阅读 `huifu-pay-integration/SKILL.md` 与 `references/` 下的场景文档
- 1.3.1 在接入副驾驶层上新增本地沙箱入口；普通接入仍优先从 `references/copilot-onboarding.md` 和 `references/copilot-solution-selection.md` 判断场景
- 本地沙箱问题优先从 `references/shared-local-sandbox.md` 开始；本地通过不代表官方联调或生产上线通过
- 服务端接入优先从 `references/shared-server-sdk-matrix.md` 和对应 `*-base.md` 开始
- Python 服务端接入优先从 `references/shared-server-sdk-matrix.md`、`references/aggregation-python-adapter.md` 或 `references/hostingpay-python-adapter.md` 开始。
- 前端接入优先从 `references/shared-frontend-sdk-matrix.md` 和 `references/checkout-js.md` 开始
- AI 生成接入代码时，不应自行猜测商户参数、项目配置或最终支付状态
- `HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 等敏感配置只能留在服务端
- 官方业务指引、联调攻略、FAQ 和技术支持链接只作为资料源索引、脱敏摘要和联系方式，不全量复制官网内容

## 官方技术支持

如需官方技术支持或接入答疑，可通过以下官方渠道联系：

- 客服电话：400-820-2819
- 官方邮箱：cs@huifu.com
- AI 技能包技术支持：https://paas.huifu.com/docs/devtools/#/skillsv1_0?id=support

企业微信技术支持群（仅用于接入答疑 / 技术支持）：

![企业微信技术支持群](scripts/qywx_goutong.png)
