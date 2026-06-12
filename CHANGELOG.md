# Changelog

所有重要变更记录在此文件中，格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

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
