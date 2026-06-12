#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = REPO_ROOT / "huifu-pay-integration"
REFERENCE_ROOT = SKILL_ROOT / "references"
PRESERVATION_DOC = REFERENCE_ROOT / "shared-request-field-preservation.md"
HOSTING_PAYLOAD_DOC = REFERENCE_ROOT / "hostingpay-payload-construction.md"
AGGREGATION_PAYLOAD_DOC = REFERENCE_ROOT / "aggregation-payload-construction.md"
PYTHON_DOCS = (
    REFERENCE_ROOT / "aggregation-python-scenarios.md",
    REFERENCE_ROOT / "hostingpay-python-scenarios.md",
)
PHP_DOCS = (
    REFERENCE_ROOT / "aggregation-query-php-scenarios.md",
    REFERENCE_ROOT / "hostingpay-preorder-php-scenarios.md",
    REFERENCE_ROOT / "hostingpay-query-php-scenarios.md",
    REFERENCE_ROOT / "hostingpay-refund-php-scenarios.md",
)


class State:
    def __init__(self) -> None:
        self.errors = 0

    def ok(self, message: str) -> None:
        print(f"OK:    {message}")

    def error(self, message: str) -> None:
        print(f"ERROR: {message}")
        self.errors += 1


def main() -> int:
    state = State()
    print("=== 请求字段保留契约校验 ===\n")
    validate_preservation_doc(state)
    validate_payload_docs(state)
    validate_language_docs(state)
    print(f"\n=== 请求字段保留结果: {state.errors} errors ===")
    return state.errors


def validate_preservation_doc(state: State) -> None:
    if not PRESERVATION_DOC.is_file():
        state.error(f"missing contract doc: {relative(PRESERVATION_DOC)}")
        return
    require_all(
        PRESERVATION_DOC,
        PRESERVATION_DOC.read_text(encoding="utf-8"),
        (
            "外部请求字段保留规则",
            "`req_date`",
            "`req_seq_id`",
            "不得在 Builder、Service、SDK Request 组装层重新生成并覆盖",
            "缺失或非法时显式报错",
            "禁止 Java 形态",
            "禁止 PHP 形态",
            "禁止 Python 形态",
            "$request->setReqDate(date('Ymd'));",
            'request.req_date = datetime.now().strftime("%Y%m%d")',
        ),
        state,
    )


def validate_payload_docs(state: State) -> None:
    require_all(
        HOSTING_PAYLOAD_DOC,
        HOSTING_PAYLOAD_DOC.read_text(encoding="utf-8"),
        (
            "private String reqDate;",
            "private String reqSeqId;",
            "request.setReqDate(cmd.getReqDate());",
            "request.setReqSeqId(cmd.getReqSeqId());",
            "不要在 Builder 里重新生成并覆盖",
        ),
        state,
    )
    require_all(
        AGGREGATION_PAYLOAD_DOC,
        AGGREGATION_PAYLOAD_DOC.read_text(encoding="utf-8"),
        ("request.setReqDate(cmd.getReqDate());", "request.setReqSeqId(cmd.getReqSeqId());"),
        state,
    )


def validate_language_docs(state: State) -> None:
    for path in PYTHON_DOCS + PHP_DOCS:
        require_all(
            path,
            path.read_text(encoding="utf-8"),
            (
                "外部 DTO / Controller 已接收",
                "必须保留入参",
                "缺失或非法时显式报错",
            ),
            state,
        )


def require_all(path: Path, text: str, snippets: tuple[str, ...], state: State) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        state.error(f"{relative(path)} missing snippets: {', '.join(missing)}")
        return
    state.ok(f"{relative(path)} field preservation contract OK")


def relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


if __name__ == "__main__":
    sys.exit(main())
