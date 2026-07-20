from __future__ import annotations

from skill_validation_config import EXPECTED_SKILL_DIR, EXPECTED_SKILL_FILE, REPO_ROOT, ValidationState


PYTHON_SDK_VERSION = "2.0.23"
PYTHON_SDK_HEADER_VERSION = f"python_{PYTHON_SDK_VERSION}"
PYTHON_CONTRACT_FILES = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "CHANGELOG.md",
    EXPECTED_SKILL_FILE,
    EXPECTED_SKILL_DIR / "references" / "shared-overview.md",
    EXPECTED_SKILL_DIR / "references" / "shared-server-sdk-matrix.md",
    EXPECTED_SKILL_DIR / "references" / "shared-request-header-policy.md",
    EXPECTED_SKILL_DIR / "references" / "shared-versioning-policy.md",
    EXPECTED_SKILL_DIR / "references" / "shared-release-checklist.md",
    EXPECTED_SKILL_DIR / "references" / "aggregation-python-adapter.md",
    EXPECTED_SKILL_DIR / "references" / "aggregation-python-scenarios.md",
    EXPECTED_SKILL_DIR / "references" / "hostingpay-python-adapter.md",
    EXPECTED_SKILL_DIR / "references" / "hostingpay-python-scenarios.md",
)
PYTHON_ENV_DOC_FILES = (
    EXPECTED_SKILL_DIR / "references" / "aggregation-python-adapter.md",
    EXPECTED_SKILL_DIR / "references" / "hostingpay-python-adapter.md",
)
PYTHON_PROD_ENV_KEYS = (
    "HUIFU_SYS_ID",
    "HUIFU_PRODUCT_ID",
    "HUIFU_RSA_PRIVATE_KEY",
    "HUIFU_RSA_PUBLIC_KEY",
    "HUIFU_SKILL_SOURCE",
    "HUIFU_MERCHANT_ID",
    "HUIFU_NOTIFY_URL",
)
PYTHON_OLD_HEADER_MARKER = "| `sdk_version` | `python_"
PYTHON_BAD_HEADER_SENTENCE = "Python 官方 SDK 不会额外生成 `jpt-sdk_version`"
HOSTING_REFUND_LOCATOR_KEYS = ("org_hf_seq_id", "org_party_order_id", "org_req_seq_id")
STALE_PYTHON_SPLITPAY_PHRASES = (
    "Python 当前未发现拆单支付订单查询",
    "未发现 `V2TradeHostingPaymentSplitpayQueryRequest`",
    "不要生成不存在的 Python request 类",
    "不存在的 Python request 类",
    "Python 不要生成不存在",
    "只能在项目接受官方 `DGTools.request_post` 通用方法",
)


def validate_python_prod_contract(state: ValidationState) -> None:
    print("\n--- Python 生产接入口径检查 ---")
    validate_python_contract_texts(state)
    validate_python_env_docs(state)
    validate_hosting_python_refund_locator(state)


def validate_python_contract_texts(state: ValidationState) -> None:
    for path in PYTHON_CONTRACT_FILES:
        text = path.read_text(encoding="utf-8")
        label = path.relative_to(REPO_ROOT)
        if "2.0.192" in text or "python_2.0.192" in text:
            state.error(f"{label} still references old Python SDK 2.0.192")
        if "mertest" in text:
            state.error(f"{label} still references removed Python mertest environment")
        if PYTHON_OLD_HEADER_MARKER in text:
            state.error(f"{label} still documents Python SDK version with sdk_version instead of jpt-sdk_version")
        if PYTHON_BAD_HEADER_SENTENCE in text:
            state.error(f"{label} incorrectly says Python does not generate jpt-sdk_version")
        for phrase in STALE_PYTHON_SPLITPAY_PHRASES:
            if phrase in text:
                state.error(f"{label} still contains stale Python splitpay SDK wording: {phrase}")
    validate_python_contract_version(state)


def validate_python_contract_version(state: ValidationState) -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in PYTHON_CONTRACT_FILES)
    if PYTHON_SDK_VERSION in combined and PYTHON_SDK_HEADER_VERSION in combined and "jpt-sdk_version" in combined:
        state.ok(f"Python SDK contract uses {PYTHON_SDK_VERSION}")
        return
    state.error(
        f"Python SDK contract must mention {PYTHON_SDK_VERSION}, {PYTHON_SDK_HEADER_VERSION}, and jpt-sdk_version"
    )


def validate_python_env_docs(state: ValidationState) -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in PYTHON_ENV_DOC_FILES)
    missing = [key for key in PYTHON_PROD_ENV_KEYS if f"{key}=" not in text]
    if missing:
        state.error(f"Python environment docs missing keys: {', '.join(missing)}")
    if "mertest" in text:
        state.error("Python environment docs must not mention mertest")
    if "HUIFU_DG_ENV" not in text or 'DGClient.env = "prod"' not in text:
        state.error('Python environment docs must pin HUIFU_DG_ENV and DGClient.env = "prod"')
    if not missing and "mertest" not in text and "HUIFU_DG_ENV" in text and 'DGClient.env = "prod"' in text:
        state.ok("Python environment docs OK")


def validate_hosting_python_refund_locator(state: ValidationState) -> None:
    path = EXPECTED_SKILL_DIR / "references" / "hostingpay-python-scenarios.md"
    text = path.read_text(encoding="utf-8")
    label = path.relative_to(REPO_ROOT)
    marker = "def refund_hosting_payment"
    start = text.find(marker)
    if start < 0:
        state.error(f"{label} missing {marker} example")
        return
    end = text.find("## 托管退款查询", start)
    snippet = text[start:] if end < 0 else text[start:end]
    if not any(key in snippet for key in HOSTING_REFUND_LOCATOR_KEYS):
        keys = " / ".join(HOSTING_REFUND_LOCATOR_KEYS)
        state.error(f"{label} refund example must set one original transaction locator: {keys}")
        return
    state.ok("Hosting Python refund locator OK")


def main() -> int:
    state = ValidationState()
    print("=== Python 生产口径校验 ===\n")
    validate_python_prod_contract(state)
    print(f"\n=== 结果: {state.errors} errors, {state.warnings} warnings ===")
    if state.errors == 0:
        print("[OK] All checks passed")
    else:
        print("[ERROR] Fix errors before release")
    return state.errors


if __name__ == "__main__":
    raise SystemExit(main())
