# Changelog

所有重要变更记录在此文件中。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [1.2.0] - 2026-04-24

### 新增
- Agent Skills 官方规范对齐文档 `docs/agent-skills-spec.md`
- 基于官方规范的新校验器 `scripts/validate_skills.py`
- 共享请求头约束文档 `huifu-pay-integration/references/shared-request-header-policy.md`
- 控台 Webhook 终端密钥与 MD5 验签规则文档 `huifu-pay-integration/references/shared-webhook-signing.md`
- 托管支付 PHP 场景文档（预下单、查询/关单/对账、退款）
- 聚合支付 PHP 适配说明与扫码关单 / 关单查询场景文档
- 单 Skill 平铺 references 结构与官方 PHP SDK 落地入口

### 变更
- 对外发布结构收敛为单 Skill：`huifu-pay-integration`
- 主 `SKILL.md` 改为总入口路由，业务与共享资料收敛到 `references/`
- `SKILL.md` frontmatter 收敛到 Agent Skills 官方字段集合，版本信息改为在正文与仓库级文档维护
- 托管支付 Java 基线版本更新为 `dg-java-sdk 3.0.36`
- 聚合支付 Java 基线版本更新为 `dg-lightning-sdk 1.0.5`
- 前端收银台 JS SDK 版本说明改为按项目锁定版本接入，升级前查询 npm registry，不在 Skill 中声称“最新版”
- `HUIFU_SKILL_SOURCE` 最终上送值保留为 `<skill_source>`，不再追加 `sys_id`
- 服务端能力矩阵明确为“托管支付提供完整 PHP 路径，聚合支付当前提供扫码关单 / 关单查询 PHP 路径”

### 修复
- 校验器移除对历史非官方版本字段的依赖，改为校验正文与仓库发布结构的一致性
- README 更新为单 Skill 结构说明，并移除上传无关项误导
- Skill 包移除二维码与平台隐藏文件依赖
- 明确区分接口 `notify_url` RSA 验签与控台 Webhook MD5 验签，避免两套密钥体系混用

## [1.1.0] - 2026-04-08

### 新增
- 共享协议层、运行时矩阵和发布治理
- 多语言入口（server-sdk-matrix.md、frontend-sdk-matrix.md）
- 客户前置准备清单（customer-preparation.md）
- 参数建模与 JSON 序列化规范（payload-construction.md）
- 异步通知接收规范（async-webhook.md）
- Java 显式适配层（language-adapters/java.md）
- 版本治理规则和发布检查清单
- 凭据使用边界集中文档（credential-boundary.md）
- 版权声明集中文档（copyright-notice.md）
- 端到端冒烟测试指南（docs/smoke-test.md）
- 自动化校验脚本（scripts/validate-skills.sh）
- checkout-js 预留 references/ 目录

### 变更
- 许可证从 MIT 修正为 CC-BY-NC-4.0
- 新增集中版权声明文档 `copyright-notice.md`，供各 SKILL.md 统一对照
- 业务 Skill 的凭据边界说明抽取到共享文档
- release-checklist.md 修正 Skill 数量为 10
- 所有 Skill 版本升至 1.1.0

### 修复
- README 目录树补齐 language-adapters/ 层
- README 目录树补齐新增治理文档和顶层文件
- 10 个 SKILL.md 的正文版本表与 frontmatter 版本同步为 `1.1.0`
- README 中 `HUIFU_CALLBACK_URL` 的场景说明与 skill metadata 保持一致
- `validate-skills.sh` 增强版本一致性和许可证精确校验

## [1.0.0] - 2026-04-07

### 新增
- 聚合支付 4 个 Skill（pay-base、aggregate-order、aggregate-query、aggregate-refund）
- 托管支付 4 个 Skill（pay-base、cashier-order、cashier-query、cashier-refund）
- 基础参数表、错误码和接口说明
