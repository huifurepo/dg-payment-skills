# Huifu Payment local-sandbox 本地联调套件最终方案

> 版本：Final Draft 1.0
> 适用基线：当前 `huifu-pay-integration` Skill `1.3.0` 及其 `references/` 契约快照
> 文档性质：产品、架构、安全、协议、测试和发布的一体化落地方案

---

## 1. 最终结论

建议继续推进 `local-sandbox`，但应将其定义为**独立发布、协议驱动、默认离线、仅使用合成数据的本地支付联调工具**，不能放入正式 Skill 包，也不能承担官方联调、通道验收或生产准入职责。

最终边界固定为：

```text
Skill                 = 接入副驾驶、文档路由、代码生成约束
local-sandbox         = 本地协议模拟、闭环演练、故障注入、自检报告
汇付官方联调环境      = 真实接口、真实权限、真实通道和产品能力验收
生产环境              = 上线配置、真实交易、真实风控与资金结果验证
```

必须长期保留以下声明：

```text
本地联调通过，不代表官方联调通过。
本地联调通过，不代表具备生产上线条件。
local-sandbox 不创建真实交易，不验证真实商户权限、通道、费率、风控或资金结果。
```

### 1.1 可以保留的原方案方向

- Go 单二进制和三端交付方向正确。
- Skill、沙箱、官方联调和生产环境的职责拆分正确。
- Contract、Fixture、状态机、异步通知、故障注入和脱敏报告方向正确。
- 默认仅监听本机、无自动更新、无默认遥测、无远程脚本执行方向正确。
- SHA-256、代码签名、SBOM、构建 provenance 和制品级验证方向正确。
- 第一期先做 Headless API、契约和报告，再做 UI 的节奏正确。

### 1.2 必须修正后才能开发的关键问题

1. **同步响应 envelope 写错**：`resp_code`、`resp_desc` 必须放在响应 `data` 内，顶层只保留 `sign` 和 `data`。
2. **第一期接口必填字段不准确**：聚合下单缺少 `goods_desc`，`notify_url` 不是硬必填；托管预下单的 `project_id` 位于 `hosting_data` JSON 字符串内，且缺少 `goods_desc`、`hosting_data.project_title`；托管查单的条件组合也需修正。
3. **版本基线必须以当前仓库事实为准**：当前技能包实际版本为 `1.3.0`，沙箱契约基线应锁定到当前 `huifu-pay-integration 1.3.0` 的 reference 快照，不能再引用过期基线。
4. **Skill 引用入口必须以现有文件为准**：当前仓库已存在 `huifu-pay-integration/references/official-service-source-index.md`，可以作为官网资料源和下载页登记入口；如新增专门的 `shared-local-sandbox.md`，必须同步更新路由、校验清单和版本说明。
5. **测试密钥模型不完整**：请求签名与响应/通知签名是两个信任方向，至少需要“商户测试身份”和“网关测试身份”两套 RSA 密钥对。
6. **密钥策略自相矛盾**：原方案同时写了“测试私钥持久化”和“默认不保存密钥”，必须统一口径。
7. **归档哈希存在自引用风险**：归档内部不能包含声明自身归档 SHA-256 的 manifest；需要拆成包内 `build-info.json` 和包外 `release-manifest.json`。
8. **Admin token CLI 传参不安全**：`--admin-token <token>` 会进入命令历史和进程列表，应删除，改为自动生成、token 文件或标准输入。
9. **所有 API 都要求 JSON 不准确**：支付网关 API 使用 JSON；接口 `notify_url` 通常应按 `application/x-www-form-urlencoded` 模拟 `sign + resp_data`；控台 Webhook 才是原始 JSON 事件体。
10. **支付、退款、关单状态混在一个状态机中**：退款和关单应是独立操作聚合，不能把支付成功状态直接改成退款处理中。
11. **代码静态扫描结论过强**：正则扫描不能证明“使用了官方 SDK”或“生产闭环正确”，只能输出建议性或启发式结论。
12. **外部分发许可证未解决**：当前仓库许可证为 CC BY-NC 4.0；如作为官网或商业产品分发，必须先完成代码许可证、协议资料使用授权和商标命名审查。
13. **源码包白名单不足**：当前上传源码包中存在 `.git/`、`.claude/settings.local.json`、`.DS_Store` 和 `__pycache__/*.pyc`，正式源码制品必须全部排除。

---

## 2. 产品目标与非目标

### 2.1 产品目标

第一版应解决五类问题：

1. 在本地模拟聚合支付和托管支付的核心请求、同步响应、查单、页面回调和异步通知。
2. 验证请求 envelope、必要请求头、条件字段、JSON 字符串字段、签名和状态判断是否符合当前 Skill 契约。
3. 支持处理中、成功、失败、超时、重复通知、乱序通知、验签失败和错误回包等可重放场景。
4. 生成可脱敏分享、但不会被误读为官方验收结果的本地自检报告。
5. 提供 Windows、Linux、macOS 可独立下载和校验的制品。

### 2.2 明确非目标

- 不模拟真实商户开通状态、渠道权限、支付机构路由、费率、风控、结算和资金账户。
- 不访问真实汇付生产或联调接口。
- 不读取接入项目的真实 `.env`、证书、私钥或商户配置。
- 不自动执行用户代码，不提供“上传代码后自动运行”的能力。
- 不保证所有官方 SDK 都支持把 API 基础地址切换到本地。
- 不以静态扫描、Fixture 回放或本地报告作为上线准入结论。
- 不自动联网检查更新，不使用 `latest.zip`，不执行 `curl | bash`。

---

## 3. 总体架构

### 3.1 单进程、双监听面设计

推荐继续采用一个 Go 二进制，但逻辑和网络上拆成两个监听面：

```text
┌──────────────────────────────────────────────────────┐
│ hf-payment-local-sandbox                             │
│                                                      │
│  Gateway Plane（支付协议面）                         │
│  - /v4/trade/payment/*                               │
│  - /v2/trade/hosting/payment/*                       │
│  - 仅模拟支付协议，不暴露管理能力                    │
│                                                      │
│  Control Plane（本机控制面）                         │
│  - 本地 UI                                           │
│  - /__health/*                                       │
│  - /__admin/*                                        │
│  - 场景、状态、通知、报告和测试凭据管理              │
│                                                      │
│  Core                                                │
│  - contract/rules                                    │
│  - scenario engine                                   │
│  - event store/state projection                      │
│  - signing/notify/redaction/report                   │
└──────────────────────────────────────────────────────┘
```

默认地址建议：

```text
Control URL: http://127.0.0.1:8765
Gateway URL: http://127.0.0.1:8766
```

双监听面的价值：

- 即使未来显式开放 Gateway 给局域网，也不会把 Admin API 一起暴露。
- UI 和 Admin 始终只在 loopback 上运行。
- 支付协议路由与管理路由不会相互污染。
- 安全测试和访问控制边界更清晰。

### 3.2 模块划分

```text
local-sandbox/
  cmd/
    hf-payment-local-sandbox/
      main.go
  internal/
    app/                    # 生命周期、依赖装配、优雅退出
    gateway/                # 汇付协议模拟端
    control/                # UI、health、admin
    contracts/              # endpoint contract、规则和版本映射
    scenarios/              # 声明式场景引擎
    fixtures/               # 合成 fixture
    signing/                # 请求、响应、notify、webhook 签名
    credentials/            # 双测试身份、轮换和导出
    state/                  # 事件日志、状态投影、文件锁
    notify/                 # 安全投递、重试、ACK 解析
    reports/                # 报告、覆盖率和报告清单
    redaction/              # 写入前脱敏
    scanner/                # Java/PHP 建议性静态检查
    security/               # Host、CSRF、SSRF、路径和大小限制
    config/                 # CLI、默认值、配置校验
    version/                # 版本和构建信息
    assets/
      embed.go
      contracts/
      fixtures/
      web/
  tests/
  testdata/

scripts/
  build-local-sandbox.sh
  build-local-sandbox.ps1
  package-skill-release.py
  package-source-release.py
  validate-local-sandbox-release.py
```

所有静态资源、Contract、Fixture 和 UI 文件由 `go:embed` 编译进入二进制。运行时不得依赖当前工作目录中的 `web/`、`fixtures/` 或 `contracts/`。

### 3.3 状态存储方案

第一版不建议直接引入 SQLite/CGO。采用：

- 内存状态投影；
- 每次运行独立的 append-only `events.ndjson`；
- 原子写入的 `state.snapshot.json`；
- 进程级文件锁；
- 崩溃恢复时将未正常结束的运行标记为 `aborted`；
- SIGINT/SIGTERM 时先停止接流量，再落事件和报告。

该方案保持单二进制、透明可检查和 `CGO_ENABLED=0`。后续如并发或查询能力明显增长，再通过 `state.Store` 接口替换为嵌入式数据库。

---

## 4. 版本与兼容性治理

### 4.1 三类版本必须分开

```text
Sandbox Version       = 工具自身版本，例如 1.0.0
Contract Bundle       = 固化协议契约版本，例如 huifu-pay-integration-1.3.0-r1
Report Schema Version = 报告结构版本，例如 1.0
```

不能只用 `compatible_skill` 一个范围概括所有兼容关系。

### 4.2 推荐版本节奏

当前 Skill 实际版本是 `1.3.0`，因此建议：

```text
内部开发：local-sandbox 0.1.0 ~ 0.9.x
契约基线：huifu-pay-integration 1.3.0
公开首版：local-sandbox 1.0.0
```

当前 `1.3.0` 已包含 `references/official-service-source-index.md`。Phase 1~4 可以不修改正式 Skill，让沙箱独立开发和内部验证；准备公开发布且需要 Skill 内置本地沙箱入口时，再选择更新现有 `official-service-source-index.md` 或新增 `references/shared-local-sandbox.md`，并按版本策略升级到后续版本。若只是新增下载入口和使用说明，优先按补丁版本处理；若改变 Skill 路由、契约覆盖或用户输出能力，再按次版本处理。

### 4.3 兼容信息建议

包内 `build-info.json`：

```json
{
  "name": "hf-payment-local-sandbox",
  "version": "1.0.0",
  "os": "windows",
  "arch": "amd64",
  "build_commit": "<commit>",
  "build_time": "<RFC3339>",
  "go_version": "<go-version>",
  "contract_bundle": {
    "id": "huifu-pay-integration-1.3.0-r1",
    "source_skill_version": "1.3.0",
    "source_commit": "<commit>",
    "references_digest": "sha256:<digest>"
  },
  "report_schema_version": "1.0",
  "scenario_schema_version": "1.0"
}
```

包外 `release-manifest.json`：

```json
{
  "release": "1.0.0",
  "published_at": "<RFC3339>",
  "compatible_skill_ranges": [">=1.3.0 <1.4.0"],
  "contract_bundle": "huifu-pay-integration-1.3.0-r1",
  "artifacts": [
    {
      "name": "hf-payment-local-sandbox_1.0.0_windows_amd64.zip",
      "os": "windows",
      "arch": "amd64",
      "size": 0,
      "sha256": "<archive-sha256>",
      "binary_sha256": "<binary-sha256>",
      "code_signed": true,
      "notarized": false,
      "sbom": "hf-payment-local-sandbox_1.0.0_windows_amd64.spdx.json",
      "sbom_schema": "SPDX-2.3",
      "sbom_sha256": "<sbom-sha256>",
      "provenance": "provenance.intoto.jsonl",
      "provenance_sha256": "<provenance-sha256>"
    }
  ]
}
```

`release-manifest.json` 在归档生成后创建并放在下载页同级，不能再写回归档，否则会产生自引用和哈希漂移。

`compatible_skill_ranges` 表示当前 contract bundle 已验证的 Skill 契约范围，不等于“下载入口 reference 所在的 Skill 版本范围”。如果后续 Skill 仅新增 local-sandbox 下载说明，且不改变支付契约，release manifest 可继续声明兼容 `huifu-pay-integration-1.3.0-r1`；如果后续 Skill 改变 contract 或 fixture 来源，必须生成新的 contract bundle 并调整兼容范围。

---

## 5. 交付物与包结构

### 5.1 对外制品

```text
huifu-payment-skill-<skill-version>.zip
hf-payment-local-sandbox_<sandbox-version>_<os>_<arch>.<zip|tar.gz>
hf-payment-suite-source-<repo-tag>.tar.gz
SHA256SUMS.txt
SHA256SUMS.sigstore.json
release-manifest.json
release-manifest.sigstore.json
provenance.intoto.jsonl
*.spdx.json
```

### 5.2 沙箱包内结构

```text
hf-payment-local-sandbox[.exe]
README.md
LICENSE
NOTICE
THIRD_PARTY_NOTICES
build-info.json
FILES.sha256
sbom.spdx.json
start-sandbox.cmd        # Windows
start-sandbox.ps1        # Windows 可选
start-sandbox.sh         # Linux/macOS
```

说明：

- `FILES.sha256` 只校验包内二进制和文档，不校验自身，也不声明外层归档哈希。
- 外层归档 SHA-256 仅出现在下载页、`SHA256SUMS.txt` 和包外 `release-manifest.json`。
- 代码签名必须在归档前完成，归档后不得再修改二进制。

### 5.3 正式 Skill 包白名单

正式 Skill 包只允许：

```text
huifu-pay-integration/SKILL.md
huifu-pay-integration/agents/**
huifu-pay-integration/references/**
```

不得包含：

```text
local-sandbox/
scripts/
docs/
.git/
.claude/
.tmp/
__pycache__/
*.pyc
.DS_Store
README.md
CHANGELOG.md
LICENSE
构建产物和运行报告
```

### 5.4 源码包白名单

源码制品也必须通过单独白名单生成，不能直接压缩工作目录。至少排除：

- `.git/` 和 Git 历史对象；
- `.claude/`、IDE 配置和本机权限配置；
- `.DS_Store`、`Thumbs.db`；
- `__pycache__/`、`*.pyc`；
- `.tmp/`、构建目录、测试报告和运行数据；
- 本地密钥、签名材料和 CI 临时文件。

---

## 6. 运行时和数据目录

### 6.1 Go 运行时约束

- Go 单二进制；
- 静态资源统一 `go:embed`；
- Linux 首选 `CGO_ENABLED=0`；
- 使用 `-trimpath`，构建信息通过受控 `ldflags` 注入；
- `go.mod`、`go.sum` 锁定依赖；
- 不使用 UPX 压缩，避免影响代码签名、误报和可重复性；
- macOS universal binary 先合并架构，再签名和公证；
- Windows 二进制先 Authenticode 签名和时间戳，再打包。

### 6.2 默认数据目录

```text
Windows: %LOCALAPPDATA%\HuifuPaymentSandbox
macOS:   ~/Library/Application Support/HuifuPaymentSandbox
Linux:   ${XDG_STATE_HOME:-~/.local/state}/huifu-payment-sandbox
```

建议目录：

```text
<data-root>/
  profiles/default/
    credentials/            # 仅合成测试凭据
    profile.json
  runs/<run-id>/
    events.ndjson
    state.snapshot.json
    reports/
  locks/
  logs/
```

权限要求：

- Unix 目录尽量使用 `0700`，私钥文件使用 `0600`；
- Windows 使用当前用户专属 ACL；
- 拒绝跟随数据目录内的危险符号链接；
- 启动前检查目录可写和剩余空间；
- 同一 profile 同时只允许一个可写实例。

### 6.3 保留和清理策略

默认建议：

```text
最大保留运行数：50
最大保留天数：30
超限时仅清理已完成且未标记 keep 的运行
```

提供：

```text
hf-payment-local-sandbox purge --older-than 30d
hf-payment-local-sandbox purge --run-id <id>
hf-payment-local-sandbox serve --ephemeral
```

`--ephemeral` 模式默认不保留状态和测试密钥，适合 CI；报告是否保留由 `--report-dir` 决定。未显式提供 `--report-dir` 时，报告写入临时目录并在退出后清理；显式提供 `--report-dir` 时，即使 `--ephemeral` 也必须生成报告，便于 CI 收集。

---

## 7. CLI 最终合约

不建议继续把所有能力塞进根级 flags。采用子命令：

```text
hf-payment-local-sandbox serve
hf-payment-local-sandbox replay
hf-payment-local-sandbox validate
hf-payment-local-sandbox report
hf-payment-local-sandbox credentials
hf-payment-local-sandbox doctor
hf-payment-local-sandbox purge
hf-payment-local-sandbox version
```

### 7.1 `serve`

```text
hf-payment-local-sandbox serve
  --open
  --no-open
  --control-port 8765
  --control-port 0
  --gateway-host 127.0.0.1
  --gateway-port 8766
  --gateway-port 0
  --scenario <scenario-id>
  --profile strict|local-dev
  --data-dir <path>
  --report-dir <path>
  --print-json
  --ephemeral
  --disable-admin
  --notify-allow <exact-url>      # 可重复
  --unsafe-expose-gateway        # 仅配合非 loopback gateway-host
  --log-format text|json
  --log-level info|warn|error
```

控制面不提供外部绑定参数，始终 loopback。
`--control-port 0` 与 `--gateway-port 0` 均表示由系统分配空闲端口，实际端口必须通过 `--print-json` 的 ready 事件输出，便于并行 CI 和本机多实例运行。

### 7.2 `replay`

用于向用户自己的本地回调地址投递**合成**通知：

```text
hf-payment-local-sandbox replay
  --fixture <fixture-id>
  --target http://127.0.0.1:8080/api/huifu/notify
  --attempts 1
  --expect-ack
  --print-json
```

`replay --target` 必须复用 `notify_url` 出站安全策略：默认仅允许 loopback/local-dev 范围，外部地址必须通过 `--notify-allow` 或等价配置显式 allowlist，且必须执行 DNS pinning、redirect 禁止和私网/metadata 地址阻断。不能把 replay 作为绕过 notify 安全策略的“直接投递”通道。

原 `--callback-mode` 含义不清，建议删除，用 `serve` 和 `replay` 分别承担服务模拟和回调重放。

### 7.3 `validate`

```text
hf-payment-local-sandbox validate contract --fixture <id>
hf-payment-local-sandbox validate code --path <dir> --language java|php
hf-payment-local-sandbox validate report --path <report-dir>
```

静态代码扫描必须满足：

- 只读；
- 不执行用户代码；
- 不跟随目录外符号链接；
- 有目录大小、文件数量和单文件大小限制；
- Java/PHP 首期支持，其他语言返回 `not_evaluated`；
- 结论标记为 `heuristic`，不输出“已证明使用官方 SDK”。

### 7.4 `credentials`

```text
hf-payment-local-sandbox credentials show
hf-payment-local-sandbox credentials export --format env|json --output <path>
hf-payment-local-sandbox credentials rotate
```

`show` 默认只显示公钥指纹和文件位置，私钥需要显式 `export`。所有输出必须带“仅限 local-sandbox，禁止用于官方联调和生产”的水印。

### 7.5 `report`、`doctor`、`purge`、`version`

```text
hf-payment-local-sandbox report --run-id <id> --format json|md|html --output <path>
hf-payment-local-sandbox doctor --json
hf-payment-local-sandbox purge --older-than 30d
hf-payment-local-sandbox purge --run-id <id>
hf-payment-local-sandbox version --json
```

`version --json` 至少输出工具版本、commit、OS/arch、contract bundle、report schema、scenario schema、build time 和签名状态。`doctor --json` 只做本机环境、端口、目录权限、证书/签名状态和包完整性自检，不访问公网。

### 7.6 机器可读输出

`--print-json` 时：

- stdout 只输出单行 JSON/NDJSON；
- 日志全部写 stderr；
- 启动成功输出 `event=ready`；
- 不能在 JSON 前后混入 banner。

示例：

```json
{
  "event": "ready",
  "version": "1.0.0",
  "contract_bundle": "huifu-pay-integration-1.3.0-r1",
  "control_url": "http://127.0.0.1:54321",
  "gateway_url": "http://127.0.0.1:54322",
  "health_url": "http://127.0.0.1:54321/__health/ready",
  "data_dir": "...",
  "report_dir": "...",
  "run_id": "..."
}
```

### 7.7 Admin token 输入

删除：

```text
--admin-token <token>
```

因为命令行参数可能出现在 shell history 和进程列表。确有 CI 需要时，只允许：

```text
--admin-token-file <path>
--admin-token-stdin
```

默认仍由程序生成高熵随机 token。`--admin-token-file` 必须校验文件 owner 和权限：类 Unix 下拒绝 group/world 可读写文件；Windows 下拒绝非当前用户或管理员可读的 ACL。文档和示例不能推荐 `echo token | ...`，需要使用文件、交互式 stdin 或 CI secret 注入机制，避免 token 进入 shell history。

### 7.8 退出码

```text
0   成功
1   一般运行错误
2   参数或配置错误
3   端口不可用
4   数据/报告目录不可写
5   制品或报告校验失败
6   安全策略阻断
7   Contract/Fixture 不兼容
8   签名或测试凭据错误
9   场景状态不允许
```

---

## 8. HTTP 协议契约

### 8.1 支付网关请求 envelope

```json
{
  "sys_id": "string",
  "product_id": "string",
  "sign": "string",
  "data": {
    "业务字段": "值"
  }
}
```

全局只硬校验：

- 顶层 `sys_id`、`product_id`、`sign`、`data`；
- `data` 必须是 JSON object；
- `Content-Type` 必须可解析为 `application/json`，charset 大小写和空格差异应容忍；
- 请求体大小、JSON 深度和字段数量在安全上限内；
- `jpt-x-skill-source`；
- 当 `data.huifu_id` 存在且非空时，校验 `jpt-x-skill-huifu_id` 与其一致。

`data.req_date`、`data.req_seq_id`、`data.huifu_id` 等必须由 endpoint contract 判断，不能作为所有接口的全局必填项。

`Accept: application/json` 只记录，不作为硬拒绝条件，避免误伤未显式发送 Accept 的官方 SDK。

### 8.2 正确的同步响应 envelope

```json
{
  "sign": "string",
  "data": {
    "resp_code": "00000000",
    "resp_desc": "受理成功",
    "req_date": "yyyyMMdd",
    "req_seq_id": "string",
    "trans_stat": "P"
  }
}
```

禁止返回：

```json
{
  "resp_code": "00000000",
  "resp_desc": "受理成功",
  "data": {},
  "sign": "..."
}
```

### 8.3 HTTP 状态码

- JSON 可解析且属于业务或协议校验失败：通常 HTTP `200`，错误码放在 `data.resp_code`；
- 无法解析 JSON、媒体类型不支持、请求体超限：HTTP `400` 或 `413`；
- Control/Admin 鉴权失败：HTTP `401/403`；
- SSRF 或安全策略阻断：Control API 返回 HTTP `403`；
- 故障注入可按场景模拟 `500`、超时、连接关闭或业务错误；
- Gateway 返回的所有沙箱自定义错误必须明确标记为非官方错误码。

建议增加响应头：

```text
X-Huifu-Sandbox: true
X-Huifu-Sandbox-Version: 1.0.0
X-Huifu-Contract-Bundle: huifu-pay-integration-1.3.0-r1
X-Huifu-Scenario-Id: <scenario>
X-Trace-Id: <trace-id>
```

沙箱错误码可以保留 `LSxxxxxx`，但必须：

- `resp_desc` 加 `[LOCAL-SANDBOX]` 前缀；
- 文档写明“不是汇付官方错误码”；
- 报告提示不要在生产业务逻辑中依赖这些错误码。

---

## 9. 第一期 endpoint 契约修正版

### 9.1 聚合支付下单

```text
POST /v4/trade/payment/create
```

硬必填 `data`：

```text
req_seq_id
huifu_id
trade_type
trans_amt
goods_desc
```

规则：

- `req_date` 官方字段口径并非硬必填，但 Skill 实务建议始终传；沙箱应标为 `recommendation_warning`，不能伪装成官方硬必填。
- `notify_url` 是可选字段，不应放在硬必填列表。
- `method_expand` 按 `trade_type` 条件校验。
- `method_expand`、`acct_split_bunch` 等是 String(JSON Object/Array) 时，需同时校验“外层字符串”和“内层 JSON 结构”，签名仍使用原始字段值。

关键响应 `data`：

```text
resp_code
resp_desc
req_date
req_seq_id
hf_seq_id
trade_type
trans_stat
qr_code 或 pay_info（按场景）
```

### 9.2 聚合支付查单

```text
POST /v4/trade/payment/scanpay/query
```

硬必填：

```text
huifu_id
```

并满足：

```text
out_ord_id | hf_seq_id | req_seq_id 三选一
```

规则：

- 使用 `req_seq_id` 查询时，建议一并传 `req_date`；
- 查单请求自身的请求流水与原交易定位字段必须区分；
- 查询动作成功不等于交易成功，最终看 `trans_stat`；
- `I/P/S/F` 均需支持。

### 9.3 托管 H5/PC 预下单

```text
POST /v2/trade/hosting/payment/preorder
```

硬必填 `data`：

```text
req_date
req_seq_id
huifu_id
trans_amt
goods_desc
pre_order_type = "1"
hosting_data
```

`hosting_data` 是 JSON 字符串，内层硬必填：

```text
project_title
project_id
```

条件规则：

- 指定单一 `trans_type` 时，`hosting_data.request_type` 在 contract 层按条件必填处理；兼容性提示只允许出现在报告说明层，不能降低字段校验强度；
- `notify_url` 可选；
- `callback_url` 只代表页面回跳，不代表支付成功；
- `project_id` 不能作为 `data` 顶层字段处理。

关键响应 `data`：

```text
resp_code
resp_desc
req_date
req_seq_id
huifu_id
pre_order_type
pre_order_id
goods_desc
jump_url
hosting_data
current_time
time_expire
```

同步预下单通常不应伪造 `trans_stat` 作为必要字段，最终交易状态通过查询或异步通知确认。

### 9.4 托管支付查单

```text
POST /v2/trade/hosting/payment/queryorderinfo
```

本次查询请求硬必填：

```text
req_date
req_seq_id
```

原交易定位条件：

```text
party_order_id
```

或：

```text
huifu_id + org_req_date + org_req_seq_id
```

不能错误写成 `huifu_id + party_order_id`。

关键响应 `data`：

```text
resp_code
resp_desc
req_date
req_seq_id
huifu_id
org_req_date
org_req_seq_id / org_hf_seq_id
pre_order_id
order_stat
trans_stat
close_stat
pay_type
```

状态判断必须同时保留 `order_stat`、`trans_stat` 和 `close_stat` 的 endpoint-specific 映射。

---

## 10. 请求头验证策略

沙箱应支持显式 client profile，而不是仅凭请求猜测语言：

```text
generic
java-aggregation
java-hosting
php-official-sdk
python-official-sdk
```

共同必查：

```text
jpt-x-skill-source: <skill_source>
```

条件必查：

```text
jpt-x-skill-huifu_id: <data.huifu_id>
```

附加规则：

- `jpt-x-skill-source` 是 HTTP header，不是 `data` 字段；
- 值按业务配置原样透传，不拼接 `sys_id`；
- Java、PHP、Python 的 SDK 版本头存在差异，只在相应 profile 中检查；
- `python-official-sdk` 对齐当前 `dg-sdk 2.0.22`，建议检查 `jpt-sdk_version=python_2.0.22`、`jpt-x-skill-source`、`jpt-x-skill-huifu_id` 与 `Content-Type` 口径；
- SDK 版本头默认作为 `warning`，不要因后续 SDK 小版本变化阻断所有协议测试；
- header 检查结果必须区分 `required`、`recommended`、`observed`。

---

## 11. 签名、验签与测试凭据

### 11.1 双测试身份

必须使用两套合成 RSA 身份：

```text
merchant-sandbox key pair
  private key: 用户本地测试客户端对请求 data 签名
  public key:  local-sandbox 网关验证请求

gateway-sandbox key pair
  private key: local-sandbox 对同步响应和 notify_url 业务体签名
  public key:  用户本地客户端验证响应和通知
```

不能只生成一套 key pair 同时扮演双方，否则无法真实表达信任方向。

### 11.2 持久化口径

最终统一为：

- 永不读取或保存真实商户密钥；
- 默认 profile 首次创建时生成并持久化**仅限沙箱的测试密钥**，便于重启后客户端配置稳定；
- 测试私钥只存于 profile credentials 目录；
- 报告、普通日志和 UI 首页不显示完整私钥；
- `--ephemeral` 时密钥只在内存中存在；
- 支持显式轮换；
- 每次导出都显示“禁止用于官方联调和生产”。

### 11.3 密钥格式

至少固定并测试：

```text
RSA SHA256WithRSA
私钥：PKCS#8 PEM/Base64
公钥：X.509 SubjectPublicKeyInfo PEM/Base64
签名：标准 Base64
```

### 11.4 规范化签名

当前 Skill 共享规则描述为对 `data` 第一层字段按 ASCII 排序；部分技术文档又存在“所有对象 key 排序”的描述差异。因此开发前必须建立官方 SDK golden vectors：

- 用当前基线 Java 聚合 SDK 生成请求签名；
- 用当前基线 Java 托管 SDK 生成请求签名；
- 用当前基线 PHP SDK 生成请求签名；
- 固定相同 `data`、相同测试私钥；
- local-sandbox 的签名和验签必须与 SDK 结果逐字节一致；
- 若不一致，禁止对外发布，不得靠“看起来符合文档”放行。

Contract 中增加：

```text
signing_profile: sdk-parity-v1
canonicalization_version: 1
```

### 11.5 同步响应和通知

- 同步响应：对响应 `data` 生成签名；
- 用户客户端使用 gateway-sandbox public key 验签；
- `notify_url`：对原始 `resp_data` 字符串签名，不重新排序；
- Webhook：对原始 JSON body 与 endpoint key 拼接后计算 MD5，不能使用 RSA。

---

## 12. 异步通知与 Webhook

### 12.1 `notify_url` 模拟格式

建议默认模拟：

```text
POST <notify_url>
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

sign=<urlencoded-base64>&resp_data=<urlencoded-json-string>
```

处理约束：

- `resp_data` 原始字符串参与验签；
- 不得先 JSON parse 后重新序列化再验签；
- ACK 为 HTTP `200` 且 body 精确匹配：

```text
RECV_ORD_ID_<req_seq_id>
```

- 重复通知以 `hf_seq_id` 作为主要幂等键；
- 收到通知后仍应查单二次确认；
- 通知事件本身不直接把商户订单改成成功。

### 12.2 重试模型

Contract 中应区分：

```text
logical_timeout = 5s
max_retries = 3
```

由于“最多重试 3 次”可能被理解为总 3 次或首次失败后再重试 3 次，沙箱报告必须明确：

```text
initial_attempts
retry_attempts
max_total_attempts
```

第一版可默认“首次 1 次 + 最多重试 3 次”，同时允许场景覆盖。为提高本地测试速度，可提供逻辑时间缩放，但报告展示真实逻辑时间而非缩放后的墙钟时间。

### 12.3 控台 Webhook

Webhook 与 `notify_url` 必须分成两个 handler 和两套 Fixture：

```text
notify_url:
  transport = form-urlencoded
  payload = resp_data string
  verify = RSA public key
  ack = RECV_ORD_ID_<req_seq_id>

webhook:
  transport = application/json
  payload = raw body
  verify = MD5(raw_body + endpoint_key)
  ack = any 2xx
```

Webhook 不进入 Phase 1，放到扩展阶段。

---

## 13. 状态与事件模型

### 13.1 不混合不同业务聚合

建议拆为：

```text
PaymentAggregate
CloseOperation
RefundOperation[]
NotificationDelivery[]
CheckoutFlow
```

支付成功后发起退款，支付本身仍是成功，只更新：

```text
refunded_amount
refundable_amount
refund_summary
```

不能把 `PaymentState=SUCCESS` 直接改为 `REFUND_PROCESSING`。

### 13.2 支付内部状态

```text
INIT
  -> ACCEPTED
  -> PROCESSING
  -> SUCCESS
  -> FAILED
  -> CLOSED
```

对外投影：

```text
INIT/ACCEPTED/PROCESSING -> I 或 P（按 endpoint/scenario）
SUCCESS                  -> S
FAILED                   -> F
CLOSED                   -> close_stat=S，支付状态按接口定义保留
```

### 13.3 查询不应天然修改状态

查询 endpoint 本质是读取。若场景要求“第 2 次查询后成功”，实现应为：

```text
query_received
  -> scenario trigger matched
  -> scenario_state_advanced
  -> payment_transitioned_to_success
  -> query_response_projected
```

而不是把“query”本身定义成业务成功原因。报告需展示是场景触发，而非真实查询会改变交易结果。

### 13.4 幂等规则

创建类请求重复时区分：

1. 相同 `huifu_id + req_date + req_seq_id` 且 payload digest 相同：返回原结果，记录 `idempotent_replay`；
2. 幂等键相同但 payload digest 不同：阻断并记录 `idempotency_conflict`；
3. 查询请求流水与原交易流水分开存储；
4. 退款流水独立唯一；
5. 多笔退款总额不得超过支付可退金额；
6. 重复通知不重复执行商户状态变更，但仍返回成功 ACK。

### 13.5 事件结构

```json
{
  "schema_version": "1.0",
  "run_id": "string",
  "trace_id": "string",
  "event_id": "string",
  "event_type": "request_received",
  "severity": "info",
  "timestamp": "RFC3339Nano",
  "logical_time": "RFC3339Nano",
  "endpoint": "/v4/trade/payment/create",
  "scenario_id": "agg-create-processing-query-success-v1",
  "entity_type": "payment",
  "entity_ref": "payment_hmac_xxx",
  "contract_bundle": "huifu-pay-integration-1.3.0-r1",
  "details": {}
}
```

`details` 不能无限制写入任意原始报文，必须按 event type 使用显式 schema 和白名单字段。

---

## 14. 场景引擎

### 14.1 场景必须声明式

场景文件只允许 JSON/YAML 数据，不允许脚本、模板执行、动态代码和远程 URL。

示意：

```yaml
id: agg-create-processing-query-success-v1
contract_bundle: huifu-pay-integration-1.3.0-r1
initial_state: INIT
steps:
  - on: payment.create
    respond_fixture: v4-payment-create-processing
    transition: ACCEPTED
  - on: payment.query
    when: query_count == 1
    respond_fixture: v4-payment-query-processing
  - on: payment.query
    when: query_count >= 2
    transition: SUCCESS
    respond_fixture: v4-payment-query-success
    schedule_notify: payment-success-valid-sign
assertions:
  - response_acceptance_is_not_final_success
  - request_headers_valid
  - preserved_fields_match
```

### 14.2 第一期场景建议

Phase 1 Headless 核心只包含请求、同步响应、查单、状态投影和报告：

```text
AGG-01 聚合下单受理，第一次查单 P，第二次查单 S
AGG-02 聚合下单业务失败
AGG-03 聚合查单仍处理中
HOST-01 托管预下单返回 jump_url，前端 callback 后服务端查单成功
HOST-02 托管查单失败
```

Phase 2 通知闭环再加入：

```text
NOTIFY-01 合法签名通知 + 正确 ACK
NOTIFY-02 重复通知 + 幂等 ACK
NOTIFY-03 非法签名通知
NOTIFY-04 错误 ACK 后重试
```

Phase 3 安全负例再加入：

```text
SEC-01 notify_url 被安全策略阻断
```

第一版不建议只写“下单成功”，应把受理、最终状态和确认路径写进场景名，避免用户误解。

---

## 15. Contract 与 Fixture 治理

### 15.1 Contract 不是运行时解析 Markdown

维护链路：

```text
Skill references
  -> 人工提取/复核 machine-readable contract
  -> SDK golden vector 和 fixture 验证
  -> 固化 contract bundle
  -> go:embed 进入 local-sandbox
```

运行时不读取 Skill 目录，不依赖用户安装 Skill，也不解析在线文档。

### 15.2 Contract 结构

每个 endpoint contract 至少包含：

```text
endpoint
method
source_skill_version
source_reference
source_reference_digest
reviewed_at
reviewer
request_envelope
headers
required_fields
conditional_rules
stringified_json_fields
response_envelope
state_projection
signing_profile
fixtures
```

建议采用 JSON Schema 2020-12 处理结构校验，并配套自定义 rule engine 处理：

- 三选一/二选一；
- 条件必填；
- 金额比较；
- JSON 字符串内层结构；
- header 与 body 一致性；
- `req_seq_id` 唯一性；
- 状态迁移和退款金额不变量。

### 15.3 Fixture 元数据

```json
{
  "fixture_schema_version": "1.0",
  "id": "v4-payment-create-processing",
  "endpoint": "/v4/trade/payment/create",
  "scenario_id": "agg-create-processing-query-success-v1",
  "source_reference": "aggregation-order-response.md",
  "source_reference_digest": "sha256:...",
  "synthetic": true,
  "contains_production_data": false,
  "expected_state_transitions": ["INIT->ACCEPTED"],
  "expected_assertions": ["headers", "signature", "field-preservation"]
}
```

### 15.4 Contract drift 门禁

CI 计算参与 contract 的 references digest。出现以下情况必须失败：

- reference 内容改变但 contract bundle 未升级；
- endpoint contract 改变但 fixture 未更新；
- fixture 改变但预期状态和断言未更新；
- 签名 canonicalization 改变但 golden vector 未升级；
- report schema 改变但 schema version 未升级。

---

## 16. Admin、UI 与本地 Web 安全

### 16.1 Health 与 Admin 分离

无需鉴权、且只返回最小信息：

```text
GET /__health/live
GET /__health/ready
GET /__version
```

必须鉴权：

```text
/__admin/*
```

这样 CI smoke 不需要绕过 Admin token。

### 16.2 安全 token bootstrap

启动时生成高熵 admin token。浏览器打开 UI 时建议：

1. CLI 用 URL fragment 打开页面，例如 `#bootstrap=<one-time-token>`；
2. fragment 不发送给 HTTP 服务；
3. 前端 JS 将一次性 token POST 到 `/__admin/session`；
4. 服务端校验后设置 `HttpOnly; SameSite=Strict` 会话 cookie；
5. 页面立刻 `history.replaceState` 移除 fragment；
6. 状态变更请求同时要求 CSRF header；
7. 一次性 token 使用后失效。

不得把 admin token 放在 query string、日志、报告或浏览器 Referer 中。

### 16.3 Web 安全基线

- Control listener 只绑定 loopback；
- 严格校验 `Host`；
- CORS 默认关闭；
- Admin state-changing API 只接受 JSON；
- 校验 Origin；CLI token 模式与浏览器 session 模式分开；
- `Content-Security-Policy: default-src 'self'`；
- `Referrer-Policy: no-referrer`；
- `X-Content-Type-Options: nosniff`；
- `X-Frame-Options: DENY` 或 CSP `frame-ancestors 'none'`；
- `Cache-Control: no-store` 用于 Admin 和凭据页面；
- UI 不加载 CDN、字体、统计或任何外部资源；
- `--disable-admin` 时 UI 进入只读或完全关闭，不能保留可写入口。

### 16.4 服务端资源限制

- 请求体大小上限；
- header 大小上限；
- JSON 最大深度和字段数；
- `ReadHeaderTimeout`、`ReadTimeout`、`WriteTimeout`、`IdleTimeout`；
- 并发上限；
- 报告和事件上限；
- 所有文件名和路径做 traversal 校验。

---

## 17. notify_url 出站安全与 SSRF

### 17.1 默认策略

默认只允许精确 loopback 目标：

```text
localhost
127.0.0.0/8
::1
```

请求中出现外部 `notify_url` 时：

- 记录目标的脱敏形式；
- 不发起网络请求；
- 报告 `blocked_by_default`；
- 用户必须通过重复的 `--notify-allow <exact-url>` 显式授权。

### 17.2 allowlist 规则

- 只允许精确 scheme + host + port，不接受通配域名；
- 禁止 userinfo 和 fragment；
- query 在 strict profile 中拒绝；
- 不跟随任何重定向；
- DNS 解析后检查全部 A/AAAA 地址；
- 实际拨号固定到已校验 IP，避免 DNS rebinding；
- 阻断 metadata、link-local、multicast、unspecified 和未授权 private 地址；
- IPv4、IPv6、IPv4-mapped IPv6、十进制/十六进制/混淆 IP 都要测试；
- 报告中不记录完整 query、Authorization 或 Cookie。

### 17.3 `strict` 与 `local-dev` profile

```text
strict:
  按当前 Skill/官方通知约束校验 URL、无 query、无 redirect、端口规则

local-dev:
  可允许 loopback 上的任意高位端口
  但报告必须标记“本地便利模式，未满足严格通知 URL 约束”
```

默认使用 `strict`。用户显式选择 `local-dev` 才放宽本机端口。

---

## 18. 报告、脱敏和分享

### 18.1 报告结构

```text
<run-id>/reports/
  summary.json
  assertions.json
  events.ndjson
  final-state.json
  contract-coverage.json
  endpoint-coverage.json
  fixture-coverage.json
  notify-attempts.json
  security-findings.json
  trace.md
  index.html
  report-manifest.json
```

`report-manifest.json` 记录每个报告文件的 SHA-256，便于分享后检查完整性，但不代表官方签名或官方认证。

### 18.2 断言结果

所有检查项使用：

```text
pass
fail
warning
not_evaluated
```

并附：

```text
evidence_type = runtime | contract | static | heuristic
```

禁止用一个总体绿色勾表示“接入已完成”。建议摘要分栏：

```text
协议运行检查
异步闭环检查
安全检查
静态建议检查
未覆盖事项
```

### 18.3 写入前脱敏

禁止“先落原文再清洗”。进入事件和报告前完成字段级脱敏。

禁止落盘：

- 任何真实或沙箱私钥全文；
- Authorization、Cookie、session/admin token；
- 身份证、银行卡、手机号；
- openid、buyer_id、auth_code；
- 完整商户号、订单号、流水号；
- 完整外部 IP；
- `notify_url` query；
- 原始签名串和完整验签原文。

不要使用无盐 `hash8`。采用每次运行独立随机密钥的 HMAC-SHA256：

```text
huifu_id_hmac_ab12cd34ef
order_hmac_91fe...
```

这样同一运行内可关联，运行之间不可直接关联，也降低低熵值字典反查风险。

### 18.4 HTML 报告

- 自包含，不访问外部资源；
- 默认只读；
- 带明显水印；
- 不嵌入密钥或 token；
- 报告标题固定为“本地自检报告”；
- 不出现“认证通过”“官方验收通过”“生产就绪”。

---

## 19. 验证 Skill 生成代码的正确边界

### 19.1 三种能力分级

1. **Runtime validation**：用户自己运行应用并指向 Gateway，沙箱观察实际协议行为，可信度最高。
2. **Fixture/contract validation**：用户自行运行测试并消费 fixture，沙箱校验输入输出，适合 SDK 无 endpoint override 的情况。
3. **Static advisory scan**：只扫描源码模式，识别风险模式，结论仅供建议。

### 19.2 首期支持边界

当前 Skill 的完整代码落地主线是 Java 和 PHP。最终方案应写为：

- Java：官方 SDK 主链路；
- PHP：官方 `huifurepo/dg-php-sdk` 主链路；
- C#、Python、Go：当前只做协议入口说明或运行行为验证，不声称已有 Skill 业务模板覆盖；
- 不再写“Java/PHP/Python 默认走官方 SDK”。

### 19.3 静态检查规则

可提示：

- 是否出现自维护 `HostingClient`、`AggregationClient`；
- 是否用 `curl`、`requests` 作为支付业务主链路；
- 是否把 `jpt-x-skill-source` 写进 body；
- 是否把 callback/jump_url 当支付成功；
- 是否存在通知未验签、未幂等、未查单确认的明显路径；
- 是否硬编码私钥或测试密钥；
- 是否丢失上游 `req_date`、`req_seq_id`、金额、notify_url 和 project_id。

但报告必须写：

```text
静态扫描未发现某模式，不代表代码不存在该风险。
静态扫描发现某模式，也需结合上下文人工确认。
```

### 19.4 不执行用户代码

第一版明确禁止：

- 自动运行 Maven、Composer、Python、Node 或 shell；
- 自动安装依赖；
- 自动修改用户项目；
- 自动写 hosts、代理或系统证书；
- 自动把生产代码改成沙箱专用 HTTP client。

---

## 20. Skill 引用与官网入口

### 20.1 当前仓库事实

当前仓库已存在：

```text
huifu-pay-integration/references/official-service-source-index.md
```

该文件是 `1.3.0` 接入副驾驶的本地官方资料源索引，已用于官网资料源、转人工材料和 AI 技能包技术支持入口的路由。local-sandbox 公开发布时，可以优先在这里登记官网下载页和采集快照；如果需要更完整的用户使用说明，再新增专门的 `shared-local-sandbox.md`。

### 20.2 推荐做法

Phase 1~4 不修改正式 Skill，沙箱独立开发和内部验证。

准备公开发布且需要更完整的本地沙箱使用说明时，可新增：

```text
huifu-pay-integration/references/shared-local-sandbox.md
```

如果采用新增专门 reference 的方式，同时必须：

- 更新 `scripts/skill_validation_config.py` 的 `EXPECTED_REFERENCES`；
- 更新 `SKILL.md` 路由，仅在用户明确询问本地沙箱、下载、版本或校验时读取；
- Skill 版本按发布策略升级到后续版本，例如 `1.3.1` 或 `1.4.0`，不能再写成升级到当前已经存在的 `1.3.0`；
- 更新 README、CHANGELOG、shared-versioning-policy 和 shared-release-checklist；
- 明确不自动联网、不自动下载、不自动执行；
- 只记录官网页面和采集时版本快照；
- 下载和解压位置必须在 Skill 目录外。

如果只在现有 `official-service-source-index.md` 中登记下载页，也仍然属于正式 Skill 内容变更，必须同步版本说明、发布记录和校验清单。

### 20.3 下载页规则

- 允许有“当前版本”页面，但每个制品 URL 必须是版本化不可变地址；
- 不发布可变的 `latest.zip`；
- 页面展示大小、OS、架构、最低系统版本、SHA-256、代码签名状态、SBOM 和 provenance；
- 提供撤销/安全公告字段；
- 若制品被撤销，不复用原版本号和原 URL；
- Skill 中的离线快照不得声称是最新版本。

---

## 21. 许可证、版权和命名

公开发布前设为 P0 阻断项：

1. 确认 local-sandbox 源代码使用何种许可证；
2. 确认当前 CC BY-NC 4.0 是否允许计划中的官网、商业或客户分发方式；
3. 获得嵌入接口字段、示例结构、Contract 和 Fixture 所需的使用授权；
4. 确认 `Huifu`、`汇付`、`斗拱` 等产品名称和标识的使用权限；
5. 将代码许可证、资料版权和第三方依赖许可证分开表达；
6. 发布包包含 `LICENSE`、`NOTICE`、`THIRD_PARTY_NOTICES`。

不能简单把当前仓库 LICENSE 原样复制到二进制包后就视为完成合规。

---

## 22. 供应链与发布安全

### 22.1 签名层次

```text
Windows executable  -> Authenticode + timestamp
macOS executable    -> Developer ID signing + notarization
Linux archive       -> release signature + checksum + provenance
All archives        -> SHA-256 + release manifest signature
Build process       -> provenance attestation
Dependencies        -> SBOM
```

`.sig` 后缀不能没有定义。推荐固定使用 Sigstore/Cosign bundle，例如：

```text
release-manifest.sigstore.json
SHA256SUMS.sigstore.json
```

也可使用企业已有的 KMS/HSM 签名体系，但必须固定算法、密钥标识、验证命令、轮换和撤销流程。

### 22.2 Release pipeline 顺序

```text
1. 从受保护 tag/commit 检出源码
2. 校验依赖锁和构建脚本
3. 单元测试、静态分析、漏洞扫描、secret scan
4. 生成未签名二进制
5. 生成 SBOM
6. Windows/macOS 在原生 runner 完成代码签名
7. macOS 完成公证并验证
8. 生成 provenance/attestation
9. 生成归档
10. 计算归档、SBOM 和 provenance 的 SHA-256 与大小
11. 生成 release-manifest.json
12. 签名 SHA256SUMS 和 release manifest
13. 在干净环境下载制品并做最终 smoke
14. 发布到版本化不可变地址
```

### 22.3 CI 权限

- GitHub Actions 或其他 CI action 固定到 commit SHA；
- 默认最小权限；
- 构建 job 不持有代码签名私钥；
- 签名 job 使用受保护 environment 和人工审批；
- PR 构建不能访问生产签名密钥；
- 优先使用 HSM/KMS/OIDC，不导出长期私钥；
- provenance 由构建平台可信控制面生成，而不是由普通构建脚本自行声明。

### 22.4 SBOM

SBOM 必须固定具体 SPDX schema 版本，并在 manifest 中记录。不能只写文件名而不说明版本。每个 OS/arch 制品都应能关联到对应 SBOM。

---

## 23. CI 和测试矩阵

### 23.1 源码级

```text
go test ./...
go test -race ./...          # 支持的平台
go vet ./...
govulncheck ./...
contract schema tests
contract drift tests: reference digest、bundle version、fixture/state/assertion 联动
fixture schema tests
SDK signing golden vectors
state transition tests
idempotency/concurrency tests
notify retry and ACK tests
redaction property tests
report schema tests
HTTP limit tests
no telemetry/no update-check tests
```

### 23.2 协议级

至少覆盖：

- 正确与错误 envelope；
- `resp_code` 位于 `data`；
- header 与 `data.huifu_id` 一致性；
- 聚合下单 `goods_desc`；
- 聚合 `notify_url` 可选；
- 聚合查单三选一；
- 托管 `hosting_data.project_id` 和 `project_title`；
- 托管查单两组定位条件；
- String(JSON Object/Array) 保真；
- `resp_code=00000000` 但 `trans_stat=P`；
- callback/jump_url 不改变订单终态；
- notify form 编码和原文验签；
- Webhook raw body MD5（扩展阶段）。

### 23.3 安全级

- Host header 攻击；
- CSRF 和跨站请求；
- token 泄漏检查；
- token query/history/referrer 检查；
- CORS 默认关闭；
- DNS rebinding；
- redirect SSRF；
- IPv4/IPv6/metadata/link-local/private 地址；
- 超大 body、深层 JSON、header bomb；
- 路径穿越和符号链接；
- 报告泄密快照；
- 数据目录权限和并发锁。

### 23.4 制品级

Windows、Ubuntu、macOS 原生 runner 均需：

- 解包；
- 校验包内容白名单；
- 校验二进制架构；
- 校验可执行位；
- `version --json`；
- `serve --control-port 0 --gateway-port 0 --print-json --ephemeral --report-dir <tmp-report-dir>`；
- 读取 ready URL；
- health 200；
- 调用四个第一期 endpoint；
- 优雅关闭并生成报告；
- 中文、空格和长路径；
- 只读目录错误；
- 端口占用；
- 校验 SHA-256、manifest、SBOM 和 provenance 关联；
- Windows 验证 Authenticode；
- macOS 验证 codesign、Gatekeeper 和 notarization；
- release/source/report/fixtures 全部 secret scan。

ARM 制品不能只“编译成功”；至少通过原生 ARM runner 或受控仿真执行基本 smoke。

---

## 24. 分阶段实施计划

### Phase 0：契约与治理冻结

必须先完成：

- 修正 response envelope；
- 修正四个第一期 endpoint 契约；
- 建立 contract bundle 和版本规则；
- 建立 Java/PHP SDK signing golden vectors；
- 确认双测试身份；
- 确认双监听面；
- 确认包内/包外 manifest；
- 完成许可证、版权和命名评审；
- 建立源码和 Skill 包白名单。

**退出条件**：所有协议争议有书面结论，无未决 P0。

### Phase 1：Headless 核心

- Go CLI 和生命周期；
- Gateway/Control 双 listener；
- 四个 endpoint；
- Contract/rule engine；
- 双测试身份和请求/响应验签；
- 事件日志、状态投影、幂等；
- JSON/Markdown 报告；
- `--print-json` 和 health；
- Windows/Linux/macOS smoke。

**退出条件**：不依赖 UI 即可完成主链路测试并导出报告。

### Phase 2：通知和 checkout 闭环

- `notify_url` form-urlencoded；
- 正确 ACK、失败重试、重复通知；
- merchant demo；
- checkout callback 后调用服务端 confirm；
- HTML 报告；
- 基础 UI 和安全 token bootstrap。

**退出条件**：能完整证明“前端回调不等于终态，需查单/异步确认”。

### Phase 3：负例、安全和建议性扫描

- timeout、500、business error、invalid signature；
- duplicate/out-of-order/delayed notify；
- query still processing；
- SSRF allowlist 和 DNS pinning；
- CSRF、Host、CSP 和资源限制；
- Java/PHP 静态建议扫描；
- 脱敏和报告完整性测试。

**退出条件**：安全测试和负例场景全部进入 CI。

### Phase 4：交易能力扩展

- 聚合退款/退款查询；
- 聚合关单/关单查询；
- 托管退款/退款查询；
- 托管关单；
- 拆单查询；
- 抖音 `pre_order_type=4`；
- Webhook MD5；
- 对账文件查询。

每新增 endpoint 必须同时增加 contract、正负 fixture、状态映射和报告覆盖。

### Phase 5：公开发布

- 如需要 Skill 内置本地沙箱入口，更新 `official-service-source-index.md` 或新增 `shared-local-sandbox.md`，并按版本策略升级到后续版本；
- 官网下载页；
- Windows Authenticode 签名、macOS Developer ID 签名与公证、Linux 归档签名；
- macOS 公证；
- SHA-256、Sigstore/企业签名；
- SBOM、provenance；
- 安全和许可证审批；
- 干净环境最终安装/解包 smoke；
- 版本化不可变下载地址。

---

## 25. 发布阻断条件

以下任一项不满足，不得进入公开下载页：

### P0 协议阻断

- 响应 `resp_code` 仍在顶层；
- 第一阶段 endpoint 必填/条件字段未和 Skill references 对齐；
- 签名结果未通过官方 SDK golden vector；
- `notify_url` 和 Webhook 两套验签混用；
- payment/refund/close 状态仍混为一个状态机；
- 报告暗示官方联调或生产就绪。

### P0 安全阻断

- Control/Admin 可被外部监听；
- Admin token 可出现在 URL query、日志、报告或 CLI 参数；
- 外部 notify 默认可访问任意 URL；
- 未完成 redirect、DNS rebinding、IPv6 和 metadata SSRF 防护；
- 真实密钥、真实商户标识、真实订单/流水、真实用户标识或生产配置可进入任一发布制品、源码包、fixture、报告或日志；
- UI 使用外部 CDN/遥测；
- 未做写入前脱敏。

### P0 发布阻断

- 无许可证、资料授权、商标命名和标识使用结论；
- Windows 未代码签名和时间戳；
- macOS 未签名/公证；
- Linux 归档未签名或签名验证流程不明确；
- 无 SHA-256、明确签名方案、SBOM 或 provenance；
- 制品 URL 可变；
- source archive 包含 `.git`、`.claude`、`.DS_Store`、pycache、本地配置或 secret scan 阳性内容；
- Skill 包混入 local-sandbox、脚本、docs 或二进制；
- manifest 和归档存在自引用或哈希不一致。

---

## 26. 最终验收标准

首个可公开版本至少应达到：

1. Windows、Linux、macOS 下载后无需额外运行时即可启动；
2. 支持聚合下单/查单、托管预下单/查单；
3. 请求和响应 envelope、请求头、条件字段与当前 contract bundle 一致；
4. Java/PHP SDK 签名 golden vector 全通过；
5. 支持合法、重复、非法签名和错误 ACK 通知；
6. callback 和 jump_url 不会直接推进业务终态；
7. 支持查单补偿和幂等；
8. Admin 始终只在 loopback，token 不泄漏；
9. 外部 notify 默认阻断，显式 allowlist 后仍有 SSRF 防护；
10. 所有日志和报告写入前脱敏；
11. 报告使用 pass/fail/warning/not_evaluated，不做上线认证；
12. Windows 发布包有 Authenticode 和时间戳，macOS 发布包有 Developer ID 签名和公证，Linux 发布包有归档签名；所有发布包都有 SHA-256、SBOM、provenance 和包内容白名单；
13. Skill 仍是纯文档 Skill，不自动下载或执行沙箱；
14. 许可证、版权和商标使用已获批准。

---

## 27. 最终建议

该方案值得推进，但第一优先级不是 UI，也不是扩展全部交易接口，而是：

```text
先修正协议契约
再锁定签名一致性
再完成 Headless 闭环
再补本地安全和报告
最后做官网签名发布
```

建议的首个里程碑不是 `1.0.0`，而是内部 `0.1.0`：只包含双监听面、四个核心接口、双测试身份、状态/事件和 JSON 报告，不包含外部 `notify_url` 投递。内部 `0.2.0` 再补通知最小闭环和 checkout 确认路径。完成 SDK golden vector、Admin/SSRF 安全测试和三端制品签名后，再发布 `1.0.0`。
