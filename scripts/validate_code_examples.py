#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import time
from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = REPO_ROOT / "huifu-pay-integration"
CODE_FENCE_PATTERN = re.compile(r"```([^\n`]*)\n(.*?)\n```", re.S)
DEFAULT_COMMAND_TIMEOUT_SECONDS = 10.0
DEFAULT_TOTAL_TIMEOUT_SECONDS = 300.0
SUPPORTED_JS_LANGUAGES = {"js", "javascript"}
SUPPORTED_PYTHON_LANGUAGES = {"python", "py"}
LANGUAGE_ALIASES = {
    "json": "json",
    "xml": "xml",
    "bash": "bash",
    "sh": "bash",
    "js": "js",
    "javascript": "js",
    "php": "php",
    "java": "java",
    "python": "python",
    "py": "python",
}
FORBIDDEN_JAVA_PATTERNS = {
    "HttpClientUtils.sendPost": "Java 示例不得回退手写 HTTP",
    "curl_setopt": "服务端示例不得回退 curl_setopt",
    "setProcutId(": "Java 示例不得使用旧产品号 setter",
}


FORBIDDEN_PYTHON_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\brequests\s*\."), "Python examples must not hand-write requests HTTP flows"),
    (re.compile(r"\bhttpx\s*\."), "Python examples must not hand-write httpx HTTP flows"),
    (re.compile(r"\burllib\.request\b"), "Python examples must not hand-write urllib HTTP flows"),
    (re.compile(r"\bHostingClient\b"), "Python examples must not create HostingClient"),
    (re.compile(r"\bAggregationClient\b"), "Python examples must not create AggregationClient"),
    (re.compile(r"\bRSA\.import_key\b|\brsa\.PrivateKey\b"), "Python examples must not hand-roll RSA signing"),
)


@dataclass(frozen=True)
class CodeBlock:
    path: Path
    index: int
    language: str
    code: str


@dataclass(frozen=True)
class ValidationOptions:
    languages: frozenset[str] | None
    file_filters: tuple[str, ...]
    command_timeout: float
    total_timeout: float


@dataclass
class ValidationState:
    errors: int = 0
    started_at: float = field(default_factory=time.monotonic)
    command_timeout: float = DEFAULT_COMMAND_TIMEOUT_SECONDS
    total_timeout: float = DEFAULT_TOTAL_TIMEOUT_SECONDS

    def ok(self, message: str) -> None:
        print(f"[OK]    {message}")

    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")
        self.errors += 1

    def skip(self, message: str) -> None:
        print(f"[SKIP]  {message}")

    def remaining_timeout(self) -> float:
        elapsed = time.monotonic() - self.started_at
        return max(0.0, self.total_timeout - elapsed)

    def check_timeout(self, stage: str) -> bool:
        if self.remaining_timeout() > 0:
            return True
        self.error(f"{stage} 超过全局超时 {self.total_timeout:.0f}s")
        return False

    def subprocess_timeout(self) -> float:
        remaining = self.remaining_timeout()
        return max(0.1, min(self.command_timeout, remaining))


@dataclass(frozen=True)
class PhpStubClass:
    relative_path: str
    namespace: str
    class_name: str


@dataclass(frozen=True)
class PhpProject:
    root: Path
    sdk_root: Path


def main(argv: list[str] | None = None) -> int:
    options = parse_args(argv)
    state = ValidationState(command_timeout=options.command_timeout, total_timeout=options.total_timeout)
    blocks = collect_code_blocks(options)
    print("=== 示例代码校验 ===\n")
    run_stage("JSON examples", "json", options, state, lambda: validate_json_blocks(blocks, state))
    run_stage("XML examples", "xml", options, state, lambda: validate_xml_blocks(blocks, state))
    run_stage("Bash examples", "bash", options, state, lambda: validate_bash_blocks(blocks, state))
    run_stage("JavaScript examples", "js", options, state, lambda: validate_javascript_blocks(blocks, state))
    run_stage("Python examples", "python", options, state, lambda: validate_python_blocks(blocks, state))
    run_stage("PHP examples", "php", options, state, lambda: validate_php_blocks(blocks, state))
    run_stage("Java policy checks", "java", options, state, lambda: validate_java_constraints(blocks, state))
    print(f"\n=== 示例代码结果: {state.errors} errors ===")
    return state.errors


def parse_args(argv: list[str] | None) -> ValidationOptions:
    parser = argparse.ArgumentParser(description="Validate Markdown code examples in the Huifu Skill.")
    parser.add_argument(
        "--language",
        action="append",
        choices=sorted(LANGUAGE_ALIASES),
        help="Only run one language stage. Can repeat. Examples: --language php --language java",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Only scan matching Markdown file. Match by absolute path, repo-relative path, skill-relative path, or basename. Can repeat.",
    )
    parser.add_argument(
        "--command-timeout",
        type=float,
        default=DEFAULT_COMMAND_TIMEOUT_SECONDS,
        help="Timeout in seconds for each external syntax/runtime command.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TOTAL_TIMEOUT_SECONDS,
        help="Global timeout in seconds for the whole validation run.",
    )
    args = parser.parse_args(argv)
    languages = None
    if args.language:
        languages = frozenset(LANGUAGE_ALIASES[item] for item in args.language)
    return ValidationOptions(
        languages=languages,
        file_filters=tuple(args.file),
        command_timeout=args.command_timeout,
        total_timeout=args.timeout,
    )


def run_stage(
    title: str,
    language_key: str,
    options: ValidationOptions,
    state: ValidationState,
    callback,
) -> None:
    if options.languages is not None and language_key not in options.languages:
        state.skip(f"{title} skipped by --language")
        return
    if not state.check_timeout(title):
        return
    print(f"--- {title} ---")
    callback()


def collect_code_blocks(options: ValidationOptions) -> list[CodeBlock]:
    blocks: list[CodeBlock] = []
    for path in iter_markdown_files(options):
        text = path.read_text(encoding="utf-8")
        for index, match in enumerate(CODE_FENCE_PATTERN.finditer(text), start=1):
            language = match.group(1).strip() or "text"
            blocks.append(CodeBlock(path, index, language, match.group(2)))
    return blocks


def iter_markdown_files(options: ValidationOptions) -> list[Path]:
    files = [SKILL_ROOT / "SKILL.md", *sorted((SKILL_ROOT / "references").glob("*.md"))]
    if not options.file_filters:
        return files
    selected: list[Path] = []
    for raw_filter in options.file_filters:
        matches = [path for path in files if matches_file_filter(path, raw_filter)]
        if not matches:
            raise SystemExit(f"--file did not match any Skill Markdown file: {raw_filter}")
        selected.extend(matches)
    return sorted(set(selected))


def matches_file_filter(path: Path, raw_filter: str) -> bool:
    filter_text = raw_filter.replace("\\", "/").strip()
    names = {path.name, path.as_posix()}
    for root in (REPO_ROOT, SKILL_ROOT):
        try:
            names.add(path.relative_to(root).as_posix())
        except ValueError:
            pass
    candidate = Path(raw_filter)
    if candidate.exists():
        try:
            names.add(candidate.resolve().as_posix())
            names.add(path.resolve().as_posix())
        except OSError:
            pass
    return filter_text in names


def validate_json_blocks(blocks: list[CodeBlock], state: ValidationState) -> None:
    selected = [block for block in blocks if block.language == "json"]
    for block in selected:
        try:
            json.loads(block.code)
        except json.JSONDecodeError as exc:
            state.error(f"JSON 示例无效: {format_block(block)} -> {exc}")
    state.ok(f"JSON examples valid: {len(selected)}")


def validate_xml_blocks(blocks: list[CodeBlock], state: ValidationState) -> None:
    selected = [block for block in blocks if block.language == "xml"]
    for block in selected:
        try:
            ET.fromstring(block.code)
        except ET.ParseError as exc:
            state.error(f"XML 示例无效: {format_block(block)} -> {exc}")
    state.ok(f"XML examples valid: {len(selected)}")


def validate_bash_blocks(blocks: list[CodeBlock], state: ValidationState) -> None:
    selected = [block for block in blocks if block.language == "bash"]
    if not selected:
        state.ok("Bash examples valid: 0")
        return
    if shutil.which("bash") is None:
        state.ok(f"Bash examples skipped: bash not found ({len(selected)} blocks)")
        return
    for block in selected:
        result = run_subprocess(["bash", "-n"], block, state, "Bash 示例语法检查", input=block.code)
        if result is None:
            continue
        if result.returncode != 0:
            state.error(format_command_error("Bash 示例语法错误", block, result))
    state.ok(f"Bash examples valid: {len(selected)}")


def validate_javascript_blocks(blocks: list[CodeBlock], state: ValidationState) -> None:
    selected = [block for block in blocks if block.language in SUPPORTED_JS_LANGUAGES]
    with tempfile.TemporaryDirectory() as temp_dir:
        for block in selected:
            script = Path(temp_dir) / "snippet.js"
            script.write_text(wrap_javascript(block.code), encoding="utf-8")
            result = run_subprocess(["node", "--check", str(script)], block, state, "JavaScript 示例语法检查")
            if result is None:
                continue
            if result.returncode != 0:
                state.error(format_command_error("JavaScript 示例语法错误", block, result))
            validate_create_preorder_return(block, state)
    state.ok(f"JavaScript examples valid: {len(selected)}")


def validate_create_preorder_return(block: CodeBlock, state: ValidationState) -> None:
    if "function createPreOrder" not in block.code:
        return
    if "return" in block.code:
        return
    state.error(f"createPreOrder 示例必须返回服务端预下单结果: {format_block(block)}")


def wrap_javascript(code: str) -> str:
    return "async function __snippet() {\n" + code + "\n}\n"


def validate_python_blocks(blocks: list[CodeBlock], state: ValidationState) -> None:
    selected = [block for block in blocks if block.language in SUPPORTED_PYTHON_LANGUAGES]
    for block in selected:
        validate_python_syntax(block, state)
        validate_python_forbidden_patterns(block, state)
        validate_python_official_sdk_usage(block, state)
    state.ok(f"Python examples syntax/policy-checked: {len(selected)}")


def validate_python_syntax(block: CodeBlock, state: ValidationState) -> None:
    try:
        ast.parse(block.code)
    except SyntaxError as exc:
        state.error(f"Python example syntax error: {format_block(block)} -> line {exc.lineno}: {exc.msg}")


def validate_python_forbidden_patterns(block: CodeBlock, state: ValidationState) -> None:
    for pattern, message in FORBIDDEN_PYTHON_PATTERNS:
        if pattern.search(block.code):
            state.error(f"{message}: {format_block(block)}")


def validate_python_official_sdk_usage(block: CodeBlock, state: ValidationState) -> None:
    if not block.path.name.startswith(("aggregation-python-", "hostingpay-python-")):
        return
    if not re.search(r"\b(DGClient|MerConfig|Payment[A-Za-z]*Request|V2Trade[A-Za-z]+)", block.code):
        return
    if "dg_sdk" not in block.code:
        state.error(f"Python SDK examples must use official dg_sdk: {format_block(block)}")


def validate_php_blocks(blocks: list[CodeBlock], state: ValidationState) -> None:
    selected = [block for block in blocks if block.language == "php"]
    with tempfile.TemporaryDirectory() as temp_dir:
        project = create_php_project(Path(temp_dir))
        for block in selected:
            validate_single_php_block(block, project, state)
    state.ok(f"PHP examples executable with SDK stub: {len(selected)}")


def create_php_project(root: Path) -> PhpProject:
    project_root = root / "php-project"
    sdk_root = project_root / "vendor" / "huifurepo" / "dg-php-sdk" / "BsPaySdk"
    write_php_sdk_stub(sdk_root)
    write_loader(project_root)
    return PhpProject(project_root, sdk_root)


def validate_single_php_block(block: CodeBlock, project: PhpProject, state: ValidationState) -> None:
    script = project.root / "examples" / f"snippet_{block.index}_{safe_name(block.path)}.php"
    write_file(script, normalize_php_code(block.code))
    env = php_env(project)
    lint = run_subprocess(["php", "-l", str(script)], block, state, "PHP 示例语法检查", env=env)
    if lint is None:
        return
    if lint.returncode != 0:
        state.error(format_command_error("PHP 示例语法错误", block, lint))
        return
    result = run_subprocess(["php", str(script)], block, state, "PHP 示例运行", env=env)
    if result is None:
        return
    if result.returncode != 0:
        state.error(format_command_error("PHP 示例运行失败", block, result))


def normalize_php_code(code: str) -> str:
    if code.lstrip().startswith("<?php"):
        return code
    return "<?php\n" + php_prelude() + "\n" + code


def php_prelude() -> str:
    return """
require_once dirname(__DIR__) . '/bootstrap/loader.php';
class ExampleOrder {
    public function getHfSeqId() { return 'hf_seq'; }
    public function getHuifuSeqId() { return 'hf_seq'; }
    public function getReqDate() { return date('Ymd'); }
    public function getReqSeqId() { return 'req_seq'; }
}
$order = $order ?? new ExampleOrder();
$splitOrder = $splitOrder ?? new ExampleOrder();
$refund = $refund ?? new ExampleOrder();
$refundOrder = $refundOrder ?? new ExampleOrder();
$openidFromWechat = $openidFromWechat ?? 'openid';
$clientIp = $clientIp ?? '127.0.0.1';
$optionalPayload = $optionalPayload ?? [];
$_SERVER['REMOTE_ADDR'] = $_SERVER['REMOTE_ADDR'] ?? '127.0.0.1';
$payment = $payment ?? new \\BsPaySdk\\core\\Payment();
$client = $client ?? new \\BsPaySdk\\core\\BsPayClient();
"""


def write_php_sdk_stub(sdk_root: Path) -> None:
    write_file(sdk_root / "init.php", php_core_stub())
    for stub in php_request_stubs():
        write_file(sdk_root / stub.relative_path, php_request_stub(stub))


def php_core_stub() -> str:
    return """<?php
namespace BsPaySdk\\core;
class BsPay { public static array $config = []; public static function init(array $config, bool $prod = true): void { self::$config = $config; } }
class StubResult { public function getRspDatas(): array { return ['data' => ['trans_stat' => 'S', 'file_details' => [['download_url' => 'https://example.test/bill.csv']], 'download_url' => 'https://example.test/bill.csv', 'jump_url' => 'https://example.test/pay']]; } }
class Payment { public function create($request) { return new StubResult(); } public function query($request) { return new StubResult(); } public function close($request) { return new StubResult(); } public function closeQuery($request) { return new StubResult(); } public function refund($request) { return new StubResult(); } public function refundQuery($request) { return new StubResult(); } }
class BsPayClient { public function postRequest($request) { return new StubResult(); } }
class GenericRequest { private array $fields = []; public function __call(string $name, array $args) { if (str_starts_with($name, 'set')) { $this->fields[$name] = $args[0] ?? null; return $this; } throw new \\BadMethodCallException($name); } public function getFunctionCode(): string { return static::class; } public function getFields(): array { return $this->fields; } }
"""


def php_request_stubs() -> list[PhpStubClass]:
    return [
        PhpStubClass("request/v4/payment/TradePaymentCreateRequest.php", "BsPaySdk\\request\\v4\\payment", "TradePaymentCreateRequest"),
        PhpStubClass("request/v4/payment/TradePaymentScanpayQueryRequest.php", "BsPaySdk\\request\\v4\\payment", "TradePaymentScanpayQueryRequest"),
        PhpStubClass("request/v4/payment/TradePaymentScanpayCloseRequest.php", "BsPaySdk\\request\\v4\\payment", "TradePaymentScanpayCloseRequest"),
        PhpStubClass("request/v4/payment/TradePaymentScanpayCloseQueryRequest.php", "BsPaySdk\\request\\v4\\payment", "TradePaymentScanpayCloseQueryRequest"),
        PhpStubClass("request/v4/payment/TradePaymentScanpayRefundRequest.php", "BsPaySdk\\request\\v4\\payment", "TradePaymentScanpayRefundRequest"),
        PhpStubClass("request/v4/payment/TradePaymentScanpayRefundQueryRequest.php", "BsPaySdk\\request\\v4\\payment", "TradePaymentScanpayRefundQueryRequest"),
        PhpStubClass("request/V2TradeCheckFilequeryRequest.php", "BsPaySdk\\request", "V2TradeCheckFilequeryRequest"),
        PhpStubClass("request/V2TradeHostingPaymentCloseRequest.php", "BsPaySdk\\request", "V2TradeHostingPaymentCloseRequest"),
        PhpStubClass("request/V2TradeHostingPaymentHtrefundRequest.php", "BsPaySdk\\request", "V2TradeHostingPaymentHtrefundRequest"),
        PhpStubClass("request/V2TradeHostingPaymentPreorderAliRequest.php", "BsPaySdk\\request", "V2TradeHostingPaymentPreorderAliRequest"),
        PhpStubClass("request/V2TradeHostingPaymentPreorderH5Request.php", "BsPaySdk\\request", "V2TradeHostingPaymentPreorderH5Request"),
        PhpStubClass("request/V2TradeHostingPaymentPreorderWxRequest.php", "BsPaySdk\\request", "V2TradeHostingPaymentPreorderWxRequest"),
        PhpStubClass("request/V2TradeHostingPaymentQueryorderinfoRequest.php", "BsPaySdk\\request", "V2TradeHostingPaymentQueryorderinfoRequest"),
        PhpStubClass("request/V2TradeHostingPaymentQueryrefundinfoRequest.php", "BsPaySdk\\request", "V2TradeHostingPaymentQueryrefundinfoRequest"),
        PhpStubClass("request/V2TradeHostingPaymentSplitpayQueryRequest.php", "BsPaySdk\\request", "V2TradeHostingPaymentSplitpayQueryRequest"),
    ]


def php_request_stub(stub: PhpStubClass) -> str:
    return f"<?php\nnamespace {stub.namespace};\nclass {stub.class_name} extends \\BsPaySdk\\core\\GenericRequest {{}}\n"


def write_loader(project_root: Path) -> None:
    write_file(project_root / "bootstrap" / "loader.php", """<?php
$huifuSdkRoot = getenv('HUIFU_SDK_ROOT') ?: dirname(__DIR__) . '/vendor/huifurepo/dg-php-sdk/BsPaySdk';
if (!is_file($huifuSdkRoot . '/init.php')) { throw new RuntimeException('未找到 dg-php-sdk'); }
if (!defined('HUIFU_SDK_ROOT')) { define('HUIFU_SDK_ROOT', rtrim($huifuSdkRoot, '/')); }
require_once HUIFU_SDK_ROOT . '/init.php';
\\BsPaySdk\\core\\BsPay::init(['sys_id' => 'sys', 'product_id' => 'prod', 'rsa_merch_private_key' => 'private', 'rsa_huifu_public_key' => 'public', 'skill_source' => 'hfps/1.3.1'], true);
""")


def php_env(project: PhpProject) -> dict[str, str]:
    env = os.environ.copy()
    env.update({
        "HUIFU_SDK_ROOT": str(project.sdk_root),
        "HUIFU_SYS_ID": "sys",
        "HUIFU_PRODUCT_ID": "prod",
        "HUIFU_RSA_PRIVATE_KEY": "private",
        "HUIFU_RSA_PUBLIC_KEY": "public",
        "HUIFU_MERCHANT_ID": "merchant",
        "HUIFU_NOTIFY_URL": "https://notify.example.test",
        "HUIFU_REFUND_NOTIFY_URL": "https://refund.example.test",
        "HUIFU_PROJECT_ID": "project",
        "HUIFU_PROJECT_TITLE": "title",
        "HUIFU_CALLBACK_URL": "https://callback.example.test",
        "HUIFU_ALIPAY_BUYER_ID": "buyer",
        "HUIFU_ALIPAY_APP_SCHEMA": "alipays://platformapi/startapp",
        "HUIFU_MINIAPP_SEQ_ID": "miniapp",
        "HUIFU_SPLIT_HUIFU_ID": "split_merchant",
        "HUIFU_SKILL_SOURCE": "hfps/1.3.1",
    })
    return env


def validate_java_constraints(blocks: list[CodeBlock], state: ValidationState) -> None:
    selected = [block for block in blocks if block.language == "java"]
    for block in selected:
        validate_java_forbidden_patterns(block, state)
    validate_named_java_constraints(state)
    state.ok(f"Java examples policy-checked: {len(selected)}")


def validate_java_forbidden_patterns(block: CodeBlock, state: ValidationState) -> None:
    for pattern, message in FORBIDDEN_JAVA_PATTERNS.items():
        if pattern in block.code:
            state.error(f"{message}: {format_block(block)}")


def validate_named_java_constraints(state: ValidationState) -> None:
    require_text_contains("references/aggregation-query-reconciliation.md", "V2TradeCheckFilequeryRequest", state)
    require_text_contains("references/aggregation-query-reconciliation.md", "BasePayClient.request", state)
    require_text_contains("references/aggregation-java-sdk-quickstart.md", "setProductId", state)
    require_text_contains("references/hostingpay-java-sdk-quickstart.md", "setProductId", state)


def require_text_contains(relative_path: str, needle: str, state: ValidationState) -> None:
    path = SKILL_ROOT / relative_path
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        state.error(f"Java 约束缺失: {relative_path} -> {needle}")


def run_subprocess(
    command: list[str],
    block: CodeBlock,
    state: ValidationState,
    action: str,
    **kwargs,
) -> subprocess.CompletedProcess[str] | None:
    if not state.check_timeout(action):
        return None
    try:
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=state.subprocess_timeout(),
            **kwargs,
        )
    except subprocess.TimeoutExpired as exc:
        state.error(f"{action}超时: {format_block(block)} -> {exc.timeout:.1f}s")
        return None


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def safe_name(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", str(path.relative_to(SKILL_ROOT)))


def format_block(block: CodeBlock) -> str:
    relative = block.path.relative_to(REPO_ROOT)
    return f"{relative} code-block#{block.index}"


def format_command_error(prefix: str, block: CodeBlock, result: subprocess.CompletedProcess[str]) -> str:
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    return f"{prefix}: {format_block(block)}\n{output}"


if __name__ == "__main__":
    sys.exit(main())
