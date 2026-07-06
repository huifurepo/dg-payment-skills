# 仓库文件提交与上传策略

本文档用于区分哪些文件进入 Git，哪些文件只作为发布时手动上传产物，哪些文件只保留在本机。

## 需要提交到 Git

- 技能包源码与文档：
  - `README.md`
  - `CHANGELOG.md`
  - `huifu-pay-integration/SKILL.md`
  - `huifu-pay-integration/agents/openai.yaml`
  - `huifu-pay-integration/references/**/*.md`
- 本地沙箱源码与配置：
  - `local-sandbox/*.go`
  - `local-sandbox/go.mod`
  - `local-sandbox/USAGE.md`
  - `local-sandbox/ui-assets/*.png`
  - `local-sandbox/contracts/**/*.json`
- 样例与派生合同证据：
  - `local-sandbox/sample-packs/huifu-pay-integration-1.3.0-r4/manifest.json`
  - `local-sandbox/sample-packs/huifu-pay-integration-1.3.0-r4/sample.schema.json`
  - `local-sandbox/sample-packs/huifu-pay-integration-1.3.0-r4/samples/*.json`
  - `local-sandbox/contracts/huifu-pay-integration-1.3.0-r4/fixtures/sample-*.json`
- 校验、打包、发布脚本：
  - `scripts/*.py`
  - `scripts/*.json`
- 仓库治理文件：
  - `.gitignore`
  - `.gitattributes`
  - `REPOSITORY_FILE_POLICY.md`

## 不提交 Git，但需要手动上传或归档

- 技能包上传产物：
  - `huifu-pay-integration_*.zip`
  - `huifu-pay-integration.7z`
- 本地沙箱 preview 下载包：
  - `release-preview/<version>/hf-payment-local-sandbox-<version>-preview.zip`
  - `release-preview/<version>/hf-payment-local-sandbox-<version>-preview.zip.sha256`
- 本地沙箱内部 RC 制品：
  - `release-preview/<version>/dist/*`
  - 或全量验证输出目录中的 `dist/*`
- 可选样例包归档：
  - `local-sandbox/sample-packs/*.zip`

手动上传前应从干净提交重新生成产物，并同步发布 SHA256。

## 不提交 Git，也不作为正式上传产物

- 本地编译二进制：
  - `local-sandbox/hf-payment-local-sandbox`
  - `local-sandbox/hf-payment-local-sandbox.exe`
- 临时构建目录：
  - `build/`
  - `dist/`
  - `local-sandbox/build/`
  - `local-sandbox/dist/`
- 本机临时、缓存和日志：
  - `.tmp/`
  - `.codex-tasks/`
  - `__pycache__/`
  - `.pytest_cache/`
  - `skill-sandbox-assessment-*.md`
  - `*.log`
  - `*.tmp`
- 本地配置、证书和密钥：
  - `.env`
  - `.env.*`
  - `*.pem`
  - `*.key`
  - `*.p12`
  - `*.pfx`

这些路径已在 `.gitignore` 中记录。
