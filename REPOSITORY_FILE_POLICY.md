# 仓库文件提交与上传策略

## 提交到 Git

- 两个 Skill 源码：
  - `huifu-pay-integration/{SKILL.md,agents/,references/}`
  - `huifu-merchant-onboarding/{SKILL.md,agents/,references/}`
- 维护证据：
  - `skills-manifest.json`
  - `maintainer-contracts/*.json`
  - `maintainer-contracts/*.md`
  - `maintainer-contracts/official-sources/**`
- 回归和校验：
  - `tests/regression/*.json`
  - `scripts/*.py`
  - `scripts/*.json`
  - `scripts/*.sh`
  - `scripts/*.ps1`
- 支付本地沙箱源码、冻结合同、fixtures 和 sample pack manifest。
- `README.md`、`CHANGELOG.md`、`.gitignore`、`.gitattributes` 和本文件。

## 独立 Skill 上传包

只上传从干净提交生成的：

- `huifu-pay-integration-<version>.zip`
- `huifu-merchant-onboarding-<version>.zip`
- 对应 `.zip.sha256`
- 对应 `.provenance.json`

每个 ZIP 只能包含一个同名 Skill 根目录及：

- `SKILL.md`
- `agents/`
- `references/`

以下内容不得进入任一 Skill ZIP：

- 另一个 Skill
- `maintainer-contracts/`
- `tests/`
- `scripts/`
- `local-sandbox/`
- README、CHANGELOG、原始官方来源和真实模型输出

## 不提交 Git

- `dist/`、`build/` 和本地生成的 ZIP/SHA。
- `release-preview/` 构建产物。
- 本地二进制和编译目录。
- `.tmp/`、`.codex-tasks/`、`__pycache__/`、pytest/mypy/ruff 缓存、日志。
- `.env*`、私钥、证书、真实材料和生产配置。

发布前必须从干净提交重新构建两个 ZIP，验证内容白名单、文件 SHA、独立解压和 provenance。
