#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = REPO_ROOT / "huifu-pay-integration"
REFERENCE_ROOT = SKILL_ROOT / "references"
PAYLOAD_DOC = REFERENCE_ROOT / "aggregation-payload-construction.md"
LANGUAGE_DOCS = (
    REFERENCE_ROOT / "aggregation-java-adapter.md",
    REFERENCE_ROOT / "aggregation-php-adapter.md",
    REFERENCE_ROOT / "aggregation-python-adapter.md",
    REFERENCE_ROOT / "aggregation-query-php-scenarios.md",
    REFERENCE_ROOT / "aggregation-python-scenarios.md",
)
REQUEST_BOUNDARY_DOCS = (
    REFERENCE_ROOT / "aggregation-payload-construction.md",
    REFERENCE_ROOT / "aggregation-order-request.md",
    REFERENCE_ROOT / "aggregation-order-quickstart.md",
    REFERENCE_ROOT / "aggregation-order-method-wechat.md",
    REFERENCE_ROOT / "aggregation-order-method-alipay.md",
    REFERENCE_ROOT / "aggregation-order-method-unionpay.md",
    REFERENCE_ROOT / "aggregation-base.md",
    REFERENCE_ROOT / "aggregation-customer-preparation.md",
    REFERENCE_ROOT / "aggregation-order-tx-metadata.md",
    REFERENCE_ROOT / "aggregation-refund.md",
    REFERENCE_ROOT / "aggregation-refund-quickstart.md",
)
TRADE_TYPE_KEYS = (
    "T_JSAPI",
    "T_MINIAPP",
    "T_APP",
    "T_MICROPAY",
    "A_JSAPI",
    "A_NATIVE",
    "A_MICROPAY",
    "U_JSAPI",
    "U_NATIVE",
    "U_MICROPAY",
)
FORBIDDEN_REQUEST_TX_METADATA = (
    'request.optional("tx_metadata"',
    "cmd.getTxMetadata",
    "private String txMetadata",
    "| `tx_metadata` | 顶层扩展 key",
    "| `data.tx_metadata` |",
    "保留的 `tx_metadata` 入口",
    "`tx_metadata` 在业务层应保持对象结构",
    "扩展参数集合，JSON Object 字符串",
)


class State:
    def __init__(self) -> None:
        self.errors = 0

    def ok(self, message: str) -> None:
        print(f"[OK]    {message}")

    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")
        self.errors += 1


def main() -> int:
    state = State()
    print("=== 聚合支付 payload 口径校验 ===\n")
    validate_payload_doc(state)
    validate_language_docs(state)
    validate_request_side_tx_metadata(state)
    print(f"\n=== 聚合 payload 结果: {state.errors} errors ===")
    return state.errors


def validate_payload_doc(state: State) -> None:
    text = PAYLOAD_DOC.read_text(encoding="utf-8")
    required = (
        "这些值不是 `method_expand` 的 key",
        "`tx_metadata` 本身不作为请求字段上送",
        "`acct_split_bunch`",
        "`terminal_device_data`",
        "`combinedpay_data`",
        "`combinedpay_data_fee_info`",
        "`trans_fee_allowance_info`",
    )
    require_all(PAYLOAD_DOC, text, required, state)


def validate_language_docs(state: State) -> None:
    required = (
        "这些值不是 `method_expand` 的 key",
        "`tx_metadata` 本身不作为请求字段上送",
    )
    for path in LANGUAGE_DOCS:
        require_all(path, path.read_text(encoding="utf-8"), required, state)


def validate_request_side_tx_metadata(state: State) -> None:
    for path in REQUEST_BOUNDARY_DOCS:
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_REQUEST_TX_METADATA:
            if phrase in text:
                state.error(f"{path.relative_to(REPO_ROOT)} still treats tx_metadata as a request wrapper: {phrase}")
        validate_no_wrapped_method_expand(path, text, state)


def validate_no_wrapped_method_expand(path: Path, text: str, state: State) -> None:
    for key in TRADE_TYPE_KEYS:
        if f'"{key}":' in text or f"'{key}':" in text:
            state.error(f"{path.relative_to(REPO_ROOT)} contains wrapped method_expand key example: {key}")


def require_all(path: Path, text: str, required: tuple[str, ...], state: State) -> None:
    missing = [snippet for snippet in required if snippet not in text]
    if missing:
        state.error(f"{path.relative_to(REPO_ROOT)} missing contract snippets: {', '.join(missing)}")
        return
    state.ok(f"{path.relative_to(REPO_ROOT)} contract snippets OK")


if __name__ == "__main__":
    sys.exit(main())
