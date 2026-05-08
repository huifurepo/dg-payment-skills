#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = REPO_ROOT / "scripts" / "huifu-payment-test-prompts.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / ".tmp" / "real-model-regression"
DEFAULT_TIMEOUT_SECONDS = 300
ASCII_WORKSPACE = Path("/tmp/hf-payment-skills-regression-workspace")
ASCII_WORKSPACE_MARKER = ".real-model-regression-workspace"


@dataclass(frozen=True)
class CaseRule:
    required_groups: tuple[tuple[str, ...], ...]
    forbidden: tuple[str, ...] = ()


@dataclass(frozen=True)
class PromptCase:
    case_id: int
    prompt: str
    expected: str


@dataclass
class CaseResult:
    case_id: int
    passed: bool
    missing: list[str]
    forbidden_hits: list[str]
    output_path: Path
    returncode: int


RULES: dict[int, CaseRule] = {
    1: CaseRule((("shared-overview",), ("hostingpay-quickstart",), ("hostingpay-customer-preparation",))),
    2: CaseRule((("aggregation-refund",), ("aggregation-php-adapter",), ("aggregation-query-php-scenarios",), ("Payment::refund", "refundQuery"), ("skill_source", "MerConfig.skill_source"))),
    3: CaseRule((("checkout-js",), ("checkout-js-callback-and-confirmation",), ("hostingpay-query",), ("hostingpay-async-webhook",), ("前端回调不等于", "前端回调不能", "不是最终成功", "callback 只传", "不改终态", "不能直接改已支付", "不要直接改订单为已支付", "不要信前端 callback"))),
    4: CaseRule((("checkout-js",), ("checkout-js-integration-flow", "checkout-js-create-preorder-contract"), ("checkout-js-callback-and-confirmation",), ("hostingpay-async-webhook",), ("跳过", "不再读", "暂时不要读"))),
    5: CaseRule((("jpt-x-skill-source",), ("jpt-x-skill-huifu_id",), ("HTTP 请求头", "HTTP 头", "请求头"), ("MerConfig.skill_source",), ("自动",))),
    6: CaseRule((("Java",), ("MerConfig.setSkillSource",), ("jpt-x-skill-source",), ("jpt-x-skill-huifu_id",), ("huifu_id",))),
    7: CaseRule((("huifurepo/dg-php-sdk", "dg-php-sdk"), ("BsPayClient::postRequest",), ("request 类", "request类", "V2TradeHostingPaymentPreorderH5Request"), ("skill_source",))),
    8: CaseRule((("硬检查点",), ("checkout-js",), ("不能单独", "不能直接"), ("托管预下单",), ("查单", "异步通知"))),
    9: CaseRule((("aggregation-order",), ("aggregation-php-adapter",), ("aggregation-query-php-scenarios",), ("Payment::create", "$payment->create", "->create("), ("TradePaymentCreateRequest",))),
    10: CaseRule((("aggregation-query",), ("aggregation-php-adapter",), ("aggregation-query-php-scenarios",), ("Payment::query", "$payment->query", "->query("), ("close()", "closeQuery", "$payment->close", "->close("), ("落库", "持久化"))),
    11: CaseRule((("BsPayClient::postRequest", "$client->postRequest"), ("V2TradeCheckFilequeryRequest",), ("aggregation-query",), ("aggregation-php-adapter",), ("aggregation-query-php-scenarios",))),
    12: CaseRule((("dg-java-sdk",), ("V2TradeCheckFilequeryRequest",), ("aggregation-query",), ("aggregation-query-reconciliation",), ("手写 HTTP", "不要给"))),
    13: CaseRule((("hostingpay-refund",), ("hostingpay-refund-query",), ("req_date",), ("req_seq_id",), ("huifu_id",), ("ord_amt",), ("org_req_date",), ("loan_flag", "垫资"), ("risk_check_data",), ("bank_info_data", "银行大额"))),
    14: CaseRule((("aggregation-refund",), ("aggregation-refund-query",), ("tx_metadata.acct_split_bunch", "acct_split_bunch"), ("combinedpay_data",), ("device_type=4", "device_type`=4", "device_type` 为 `4"), ("org_hf_seq_id",), ("org_req_seq_id",), ("mer_ord_id",))),
    15: CaseRule((("huifurepo/dg-php-sdk",), ("2.0.26",), ("composer require",), ("composer update", "--with-all-dependencies"), ("api.github.com/repos/huifurepo/bspay-php-sdk/zipball", "备用下载", "GitHub"), ("BsPaySdk/init.php", "init.php"), ("BsPay::init",), ("skill_source",), ("HUIFU_SDK_ROOT",), ("HUIFU_SYS_ID",), ("HUIFU_RSA_PRIVATE_KEY",), ("require_once",), ("request 类", "request类", "TradePaymentCreateRequest"))),
}


def main() -> int:
    args = parse_args()
    cases = select_cases(load_cases(), args.case)
    output_dir = make_output_dir(args.output_dir)
    workspace = prepare_ascii_workspace()
    results = [run_case(case, output_dir, workspace, args) for case in cases]
    write_summary(output_dir, results)
    print_summary(output_dir, results)
    return 0 if all(result.passed for result in results) else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run real-model regression for huifu skill prompts.")
    parser.add_argument("--case", type=int, action="append", help="Run only selected case id. Can repeat.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for raw outputs and summary.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--model", default=None, help="Optional model override for codex exec.")
    parser.add_argument("--skip-run", action="store_true", help="Evaluate existing outputs in output dir.")
    return parser.parse_args()


def load_cases() -> list[PromptCase]:
    data = json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))
    return [PromptCase(int(item["id"]), item["prompt"], item["expected"]) for item in data]


def select_cases(cases: list[PromptCase], selected: list[int] | None) -> list[PromptCase]:
    if not selected:
        return cases
    selected_set = set(selected)
    return [case for case in cases if case.case_id in selected_set]


def make_output_dir(output_dir: Path | None) -> Path:
    if output_dir is not None:
        target = output_dir if output_dir.is_absolute() else REPO_ROOT / output_dir
        target.mkdir(parents=True, exist_ok=True)
        return target
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = DEFAULT_OUTPUT_ROOT / stamp
    target.mkdir(parents=True, exist_ok=True)
    return target


def prepare_ascii_workspace() -> Path:
    if ASCII_WORKSPACE.is_symlink():
        target = ASCII_WORKSPACE.resolve(strict=False)
        if target != REPO_ROOT:
            raise RuntimeError(f"ASCII workspace symlink points to {target}")
        ASCII_WORKSPACE.unlink()
    if ASCII_WORKSPACE.exists():
        marker = ASCII_WORKSPACE / ASCII_WORKSPACE_MARKER
        if not marker.exists():
            raise RuntimeError(f"ASCII workspace exists without marker: {ASCII_WORKSPACE}")
        shutil.rmtree(ASCII_WORKSPACE)
    shutil.copytree(REPO_ROOT, ASCII_WORKSPACE, ignore=ignore_workspace_entry)
    (ASCII_WORKSPACE / ASCII_WORKSPACE_MARKER).write_text(str(REPO_ROOT) + "\n", encoding="utf-8")
    return ASCII_WORKSPACE


def ignore_workspace_entry(path: str, names: list[str]) -> set[str]:
    ignored = {".git", ".tmp", "__pycache__"}
    return {name for name in names if name in ignored or name.endswith(".7z")}


def run_case(case: PromptCase, output_dir: Path, workspace: Path, args: argparse.Namespace) -> CaseResult:
    output_path = output_dir / f"case-{case.case_id:02d}.txt"
    returncode = 0
    if args.skip_run:
        text = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        return evaluate_case(case, text, output_path, 0)
    model_output_path = workspace / output_path.relative_to(REPO_ROOT)
    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    command = build_command(case, model_output_path, workspace, args.model)
    try:
        result = subprocess.run(command, cwd=workspace, text=True, capture_output=True, timeout=args.timeout, check=False)
        returncode = result.returncode
        if model_output_path.exists():
            output_path.write_text(model_output_path.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            output_path.write_text(format_process_output(result), encoding="utf-8")
    except subprocess.TimeoutExpired as exc:
        returncode = 124
        output_path.write_text(format_timeout_output(exc, args.timeout), encoding="utf-8")
    text = output_path.read_text(encoding="utf-8")
    return evaluate_case(case, text, output_path, returncode)


def build_command(case: PromptCase, output_path: Path, workspace: Path, model: str | None) -> list[str]:
    command = [
        "codex",
        "exec",
        "--cd",
        str(workspace),
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "--full-auto",
        "--ephemeral",
        "--color",
        "never",
        "--output-last-message",
        str(output_path),
    ]
    if model:
        command.extend(["--model", model])
    command.append(build_prompt(case))
    return command


def build_prompt(case: PromptCase) -> str:
    return (
        "你是回归受测模型。必须先读取 `huifu-pay-integration/SKILL.md`，"
        "再按该 skill 的路由读取最少必要的 `huifu-pay-integration/references/*.md`。"
        "禁止凭通用支付经验回答；最终回答必须保留实际读取的 reference 文件名、关键 SDK 类或方法。"
        "可以读取本地文件；禁止修改文件、联网或执行真实支付请求。"
        "回答控制在 500 字以内，只输出最终回答正文。\n\n"
        f"用户问题：{case.prompt}"
    )


def evaluate_case(case: PromptCase, text: str, output_path: Path, returncode: int) -> CaseResult:
    rule = RULES[case.case_id]
    missing = ["/".join(group) for group in rule.required_groups if not contains_any(text, group)]
    forbidden_hits = [term for term in rule.forbidden if term in text]
    passed = returncode == 0 and not missing and not forbidden_hits
    return CaseResult(case.case_id, passed, missing, forbidden_hits, output_path, returncode)


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def format_process_output(result: subprocess.CompletedProcess[str]) -> str:
    parts = [
        f"[returncode] {result.returncode}",
        "[stdout]",
        result.stdout.strip(),
        "[stderr]",
        result.stderr.strip(),
    ]
    return "\n".join(parts).strip() + "\n"


def format_timeout_output(exc: subprocess.TimeoutExpired, timeout: int) -> str:
    stdout = decode_timeout_stream(exc.stdout)
    stderr = decode_timeout_stream(exc.stderr)
    parts = [
        "[returncode] 124",
        f"[timeout] {timeout}",
        "[stdout]",
        stdout.strip(),
        "[stderr]",
        stderr.strip(),
    ]
    return "\n".join(parts).strip() + "\n"


def decode_timeout_stream(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def write_summary(output_dir: Path, results: list[CaseResult]) -> None:
    payload = [
        {
            "id": result.case_id,
            "passed": result.passed,
            "missing": result.missing,
            "forbidden_hits": result.forbidden_hits,
            "returncode": result.returncode,
            "output": str(result.output_path.relative_to(REPO_ROOT)),
        }
        for result in results
    ]
    (output_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_summary(output_dir: Path, results: list[CaseResult]) -> None:
    passed = sum(1 for result in results if result.passed)
    print(f"Real model regression: {passed}/{len(results)} passed")
    print(f"Output dir: {output_dir.relative_to(REPO_ROOT)}")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        details = []
        if result.returncode != 0:
            details.append(f"returncode={result.returncode}")
        if result.missing:
            details.append("missing=" + ", ".join(result.missing))
        if result.forbidden_hits:
            details.append("forbidden=" + ", ".join(result.forbidden_hits))
        suffix = " | " + "; ".join(details) if details else ""
        print(f"{status} case-{result.case_id:02d}{suffix}")


if __name__ == "__main__":
    sys.exit(main())
