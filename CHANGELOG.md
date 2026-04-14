# Changelog

所有重要变更记录在此文件中。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [1.1.0] - 2026-04-08

### 新增
- `huifu-dougong-pay-shared-base/` 共享协议层、运行时矩阵和发布治理
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
