from __future__ import annotations

import ast
import json
import os
import re
import io
import importlib.util
from pathlib import Path
from types import SimpleNamespace

from skill_validation_config import EXPECTED_SKILL_DIR, EXPECTED_SKILL_FILE, PAYMENT_SPEC, REPO_ROOT, ValidationState, sdk_version
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


PYTHON_SDK_VERSION = sdk_version("python")
PYTHON_SDK_HEADER_VERSION = f"python_{PYTHON_SDK_VERSION}"
PYTHON_CONTRACT_FILES = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "CHANGELOG.md",
    EXPECTED_SKILL_FILE,
    EXPECTED_SKILL_DIR / "references" / "shared-overview.md",
    EXPECTED_SKILL_DIR / "references" / "shared-server-sdk-matrix.md",
    EXPECTED_SKILL_DIR / "references" / "shared-request-header-policy.md",
    REPO_ROOT / "maintainer-contracts" / "shared-versioning-policy.md",
    REPO_ROOT / "maintainer-contracts" / "shared-release-checklist.md",
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
    validate_onboarding_python_versions(state)
    validate_python_initialization(state)


def onboarding_python_version_errors(text: str) -> list[str]:
    """Validate current facts, not mere occurrence of a version in history."""
    current = current_sdk_text(text)
    values = re.findall(r"^\|\s*Python SDK(?: 当前版本)?\s*\|\s*`(?:dg-sdk\s+)?([0-9]+(?:\.[0-9]+){2})`[^|\n]*\|", current, re.M)
    problems = current_python_claim_errors(current)
    if values != [PYTHON_SDK_VERSION]:
        problems.append(f"Python SDK current row must be {PYTHON_SDK_VERSION}, found {values}")
    if re.search(r"^\|\s*Python SDK (?:已核验源码基线|目标版本)\s*\|", current, re.M):
        problems.append("Use one current Python SDK row; old target/evidence split belongs in dated history")
    return problems


def current_sdk_text(text: str) -> str:
    """Exclude explicitly titled historical sections, not arbitrary old numbers."""
    lines: list[str] = []
    history_level: int | None = None
    for line in text.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level, title = len(heading[1]), heading[2]
            if history_level is not None and level <= history_level:
                history_level = None
            if re.search(r"历史|此前阶段|先前阶段|History|Historical", title, re.I):
                history_level = level
        if history_level is None:
            lines.append(line)
    return "\n".join(lines)


def current_python_claim_errors(text: str) -> list[str]:
    """Recognize SDK selections, install pins and SDK-generated header values."""
    problems: list[str] = []
    version_pattern = r"[0-9]+(?:\.[0-9]+){2}"
    for line in current_sdk_text(text).splitlines():
        # Explicit historical prose is allowed; a later current assertion on the
        # same line is still a current claim and must not hide behind that label.
        if re.search(r"历史|此前|当时|先前|旧版", line) and not re.search(r"当前|本次|现在|安装|pip install|python_", line):
            continue
        patterns = (
            rf"(?:dg-sdk|dg_sdk)\s*(?:==|[ `])\s*`?({version_pattern})",
            rf"python_({version_pattern})",
            rf"Python(?: SDK)?(?:\s*当前版本|\s*目标版本|\s*已核验源码基线)?\s*[`：:为是| ]+\s*`?({version_pattern})",
            rf"Python(?:\s+当前)?\s+SDK[^。；;\n]*?`({version_pattern})`",
        )
        for pattern in patterns:
            for match in re.finditer(pattern, line, re.I):
                if match[1] != PYTHON_SDK_VERSION:
                    problems.append(f"stale current Python SDK claim {match[1]} (expected {PYTHON_SDK_VERSION}): {line.strip()}")
        if re.match(r"^\|\s*Python(?:\s|`)", line):
            cells = line.split("|")
            if len(cells) > 2:
                versions = re.findall(version_pattern, cells[2])
                if versions and versions != [PYTHON_SDK_VERSION]:
                    problems.append(f"stale current Python matrix selection: {cells[2].strip()}")
    return problems


def repository_python_summary_errors(text: str) -> list[str]:
    """Check the current repository summary without reading older release facts."""
    summary = re.search(
        r"^## (?:当前版本与来源[^\n]*|Unreleased SDK[^\n]*)\n(.*?)(?=^#{1,3} |\Z)",
        text, re.M | re.S,
    )
    if summary is None:
        return ["Current repository version summary is missing"]
    versions = re.findall(
        r"Python(?:\s+当前)?\s+SDK[^。；;\n]*?`([0-9]+(?:\.[0-9]+){2})`",
        summary[1],
    )
    problems = current_python_claim_errors(summary[1])
    if versions != [PYTHON_SDK_VERSION]:
        problems.append(f"Current repository Python SDK summary must be {PYTHON_SDK_VERSION}, found {versions}")
    return problems


def validate_onboarding_python_versions(state: ValidationState) -> None:
    root = REPO_ROOT / "huifu-merchant-onboarding"
    for path in (root / "SKILL.md", root / "references/skill-version-policy.md"):
        for problem in onboarding_python_version_errors(path.read_text(encoding="utf-8")):
            state.error(f"{path.relative_to(REPO_ROOT)}: {problem}")
    matrix = root / "references/shared-server-sdk-matrix.md"
    matrix_text = current_sdk_text(matrix.read_text(encoding="utf-8"))
    if f"| Python `dg-sdk` / `dg_sdk` | `{PYTHON_SDK_VERSION}` |" not in matrix_text:
        state.error("Onboarding SDK matrix must select the active local Python SDK version")
    valid = f"| Python SDK | `{PYTHON_SDK_VERSION}` |\n"
    fixtures = (
        ("current table shows actual SDK", valid, False),
        ("historical prose remains valid", valid + "历史 Python SDK 2.0.25。", False),
        ("historical table remains valid", valid + "## 历史\n| Python SDK | `2.0.25` |", False),
        ("reject stale current SDK", valid.replace(PYTHON_SDK_VERSION, "2.0.25"), True),
        ("reject old evidence row in current table", valid + "| Python SDK 已核验源码基线 | `2.0.25` |", True),
        ("reject contradictory current prose", valid + "当前 Python SDK 为 2.0.26。", True),
        ("reject stale installation pin", valid + "pip install dg-sdk==2.0.25", True),
        ("reject stale header", valid + "jpt-sdk_version: python_2.0.25", True),
        ("reject history-only expected version", f"## 历史\n{valid}", True),
    )
    for label, text, should_fail in fixtures:
        if bool(onboarding_python_version_errors(text)) != should_fail:
            state.error(f"Onboarding Python version regression failed: {label}")
    state.ok(f"Current Python {PYTHON_SDK_VERSION} table/history boundaries checked ({len(fixtures)} fixtures)")
    summary_cases = 0
    for heading, claim in (
        ("## 当前版本与来源（2026-09-24）", "当前 Python SDK 统一为用户新提供的"),
        ("## Unreleased SDK / version-information refresh", "两包 Python 当前 SDK 统一为用户提供并核验声明的"),
    ):
        for current, historical, should_fail in (
            (PYTHON_SDK_VERSION, "2.0.25", False),
            ("2.0.25", PYTHON_SDK_VERSION, True),
            ("2.0.26", PYTHON_SDK_VERSION, True),
        ):
            text = f"{heading}\n{claim} `{current}`。\n## 历史\nPython SDK `{historical}`。"
            if bool(repository_python_summary_errors(text)) != should_fail:
                state.error(f"Repository Python summary regression failed: {heading}, current={current}")
            summary_cases += 1
    state.ok(f"Repository current summary/history boundaries checked ({summary_cases} fixtures)")


def validate_python_initialization(state: ValidationState) -> None:
    """Run documented initialization against the actual local constructor offline."""
    functions: list[tuple[Path, ast.FunctionDef]] = []
    for path in PYTHON_ENV_DOC_FILES:
        blocks = re.findall(r"```python\n(.*?)```", path.read_text(encoding="utf-8"), re.S)
        for block in blocks:
            tree = ast.parse(block)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "MerConfig":
                    keywords = {item.arg for item in node.keywords}
                    if node.args or not {"private_key", "public_key", "sys_id", "product_id", "sign_type", "jpt_x_skill_source"} <= keywords:
                        state.error(f"{path.name}: MerConfig must use all six named arguments to prevent credential slot swaps")
            functions.extend((path, node) for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "init_huifu_sdk")
    if len(functions) != len(PYTHON_ENV_DOC_FILES):
        state.error("Both Python adapters must contain an executable initialization example")
    sdk_root = os.environ.get("HUIFU_SDK_ROOT")
    if not sdk_root:
        state.warning("Local Python constructor/header runtime probe not run: HUIFU_SDK_ROOT is unset")
        return
    from validate_merchant_onboarding_sdk_evidence import resolve_python_sdk, python_source_version
    try:
        python = resolve_python_sdk(Path(sdk_root).resolve())
        actual_version = python_source_version(python)
        config_namespace: dict = {}
        exec(compile((python / "core/mer_config.py").read_text(encoding="utf-8"), "local_mer_config", "exec"), config_namespace)
        config_class = config_namespace["MerConfig"]
        params_namespace: dict = {}
        exec(compile((python / "core/param_handler.py").read_text(encoding="utf-8"), "local_param_handler", "exec"), params_namespace)
        # Execute the actual request class, stubbing crypto and excluding imports/HTTP.
        # This tests constructor and header/data behavior, not cryptographic correctness.
        request_tree = ast.parse((python / "core/api_request.py").read_text(encoding="utf-8"))
        request_class = next(node for node in request_tree.body if isinstance(node, ast.ClassDef) and node.name == "ApiRequest")
        def unexpected_sm2(*args):
            raise AssertionError("RSA example unexpectedly selected SM2")
        request_namespace = {
            "json": json, "pop_empty_value": params_namespace["pop_empty_value"],
            "sort_dict": params_namespace["sort_dict"],
            "rsa_sign": lambda key, data: (True, "offline-signature-stub"),
            "sm2_sign": unexpected_sm2, "log_error": lambda message: None,
        }
        exec(compile(ast.Module(body=[request_class], type_ignores=[]), "local_api_request", "exec"), request_namespace)
        request = request_namespace["ApiRequest"]
        for path, function in functions:
            sdk = SimpleNamespace(DGClient=SimpleNamespace(), MerConfig=config_class)
            source = f"hfps/{PAYMENT_SPEC.version}"
            sentinels = {"HUIFU_RSA_PRIVATE_KEY": "offline-private-key", "HUIFU_RSA_PUBLIC_KEY": "offline-public-key",
                         "HUIFU_SYS_ID": "offline-system-id", "HUIFU_PRODUCT_ID": "offline-product-id", "HUIFU_SKILL_SOURCE": source}
            environment = {"dg_sdk": sdk, "require_env": sentinels.__getitem__}
            exec(compile(ast.Module(body=[function], type_ignores=[]), path.name, "exec"), environment)
            environment["init_huifu_sdk"]()
            config = sdk.DGClient.mer_config
            if config.sign_type != "RSA" or config.jpt_x_skill_source != source:
                raise AssertionError(f"{path.name}: initialization loses algorithm or source")
            if (config.private_key, config.public_key, config.sys_id, config.product_id) != tuple(sentinels[key] for key in ("HUIFU_RSA_PRIVATE_KEY", "HUIFU_RSA_PUBLIC_KEY", "HUIFU_SYS_ID", "HUIFU_PRODUCT_ID")):
                raise AssertionError(f"{path.name}: credential configuration slots are swapped")
            for merchant in ("offline-merchant-a", "offline-merchant-b", ""):
                data = {"huifu_id": merchant, "req_seq_id": "offline-probe"}
                request.build(config.product_id, config.sys_id, config.private_key, config.public_key,
                              "https://unused.invalid/v2/offline", data, actual_version, True, True,
                              jpt_x_skill_source=config.jpt_x_skill_source, sign_type=config.sign_type)
                headers, body = request._build_request_info("https://unused.invalid", data, None)
                if headers.get("signType") != "RSA" or headers.get("jpt-x-skill-source") != source:
                    raise AssertionError("algorithm/source header mismatch")
                if headers.get("jpt-x-skill-huifu_id") != merchant or headers.get("jpt-sdk_version") != PYTHON_SDK_HEADER_VERSION:
                    raise AssertionError("request merchant or version header mismatch")
                if body.get("sign") != "offline-signature-stub" or "jpt-x-skill-source" in body["data"]:
                    raise AssertionError("request signing/source placement mismatch")
                if body.get("sys_id") != sentinels["HUIFU_SYS_ID"] or body.get("product_id") != sentinels["HUIFU_PRODUCT_ID"]:
                    raise AssertionError("credential material entered the system/product envelope slots")
        # The SDK accepts a fifth positional source as sign_type; our examples
        # must reject that misuse, not claim the SDK rejects it itself.
        wrong = config_class("unused", "unused", "unused", "unused", source)
        if wrong.sign_type == "RSA" or wrong.jpt_x_skill_source:
            raise AssertionError("constructor compatibility changed; revisit positional-argument regression")
        explicit_source = "hfps/1.3.1;caller/offline"
        explicit = config_class("unused", "unused", "unused", "unused", sign_type="RSA", jpt_x_skill_source=explicit_source)
        request.build(explicit.product_id, explicit.sys_id, explicit.private_key, explicit.public_key,
                      "https://unused.invalid/v2/offline", {"upper_huifu_id": "offline-upper"}, actual_version,
                      True, True, jpt_x_skill_source=explicit.jpt_x_skill_source, sign_type=explicit.sign_type)
        explicit_headers, _ = request._build_request_info("https://unused.invalid", request.request_params, None)
        if explicit_headers.get("jpt-x-skill-source") != explicit_source or explicit_headers.get("jpt-x-skill-huifu_id") != "":
            raise AssertionError("explicit source was rewritten or upper_huifu_id was mistaken for merchant header")
        validate_python_request_surface(python)
        validate_python_transport_boundary(request, request_namespace)
        validate_python_crypto(python, state)
    except (OSError, ValueError, SyntaxError, AssertionError, KeyError, StopIteration) as exc:
        state.error(f"Local Python initialization/header probe failed: {exc}")
        return
    state.ok("Local Python constructor + documented initialization + RSA/source/version/merchant headers passed offline (including negative control)")


def execute_sdk_definitions(path: Path, namespace: dict) -> None:
    """Execute source definitions only, excluding package imports/initialization."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    nodes = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)


def validate_python_request_surface(python: Path) -> None:
    """Exercise real serializers with a recording transport, never HTTP."""
    routes = {
        "V2MerchantBusiHeadConfigRequest": "/v2/merchant/busi/head/config",
        "V2MerchantUrlForwardRequest": "/v2/merchant/url/forward",
        "V2MerchantBusiStatusQueryRequest": "/v2/merchant/busi/status/query",
        "V2MerchantBusiConfigRequest": "/v2/merchant/busi/config",
        "V2MerchantBusiConfigQueryRequest": "/v2/merchant/busi/config/query",
        "V2MerchantBusiRealnameRequest": "/v2/merchant/busi/realname",
        "V2MerchantBusiRealnameQueryRequest": "/v2/merchant/busi/realname/query",
        "V2MerchantBusiAliRealnameApplyRequest": "/v2/merchant/busi/ali/realname/apply",
        "V2MerchantBusiAliRealnameQueryRequest": "/v2/merchant/busi/ali/realname/query",
        "V2InvoiceContractrepeatRequest": "/v2/invoice/contractRepeat",
        "V2InvoiceQueryecmsapplylistRequest": "/v2/invoice/queryEcmsApplyList",
        "V2InvoiceRejectsignRequest": "/v2/invoice/rejectSign",
        **{f"V2TradeHostingPaymentPreorder{suffix}Request": "/v2/trade/hosting/payment/preorder"
           for suffix in ("H5", "Wx", "Ali", "Dy")},
        "V2TradeHostingPaymentQueryorderinfoRequest": "/v2/trade/hosting/payment/queryorderinfo",
        "V2TradeHostingPaymentHtrefundRequest": "/v2/trade/hosting/payment/htRefund",
        "V2TradeHostingPaymentQueryrefundinfoRequest": "/v2/trade/hosting/payment/queryRefundInfo",
        "V2TradeHostingPaymentCloseRequest": "/v2/trade/hosting/payment/close",
        "V2TradeHostingPaymentSplitpayQueryRequest": "/v2/trade/hosting/payment/splitpay/query",
        "V2TradeCheckFilequeryRequest": "/v2/trade/check/filequery",
        "V2TradeTransSplitQueryRequest": "/v2/trade/trans/split/query",
    }
    namespace = {"request_post": lambda route, params: (route, params)}
    execute_sdk_definitions(python / "request/request_api_urls.py", namespace)
    for name, expected_route in routes.items():
        filename = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + ".py"
        execute_sdk_definitions(python / "request" / filename, namespace)
        route, data = namespace[name]().post({"offline_marker": "preserved"})
        assert route == expected_route, (name, route)
        assert data["offline_marker"] == "preserved", name
    execute_sdk_definitions(python / "dg_tools.py", namespace)
    for route in ("/v2/merchant/fee-rate/query", "/v2/agreement/elect/signurl/resend", "/v2/agreement/apply/list", "/v2/agreement/elect/rejectsign"):
        namespace["request_post"] = lambda url, request_params, files=None: (url, request_params, files)
        assert namespace["DGTools"].request_post(route, {"offline": [1]}) == (route, {"offline": [1]}, None)
    try:
        namespace["DGTools"].request_post("/unused", {}, need_sign=True)
    except TypeError:
        pass
    else:
        raise AssertionError("DGTools now accepts signing switches; review image guidance")

    aggregation = {
        "create": ("PaymentCreateRequest", "/v4/trade/payment/create"),
        "query": ("PaymentQueryRequest", "/v4/trade/payment/scanpay/query"),
        "close": ("PaymentCloseRequest", "/v2/trade/payment/scanpay/close"),
        "close_query": ("PaymentCloseQueryRequest", "/v2/trade/payment/scanpay/closequery"),
        "refund": ("PaymentRefundRequest", "/v4/trade/payment/scanpay/refund"),
        "refund_query": ("PaymentRefundQueryRequest", "/v4/trade/payment/scanpay/refundquery"),
    }
    namespace["request_post"] = lambda route, params: (route, params)
    for name, _ in aggregation.values():
        execute_sdk_definitions(python / "v4" / f"{name}.py", namespace)
    execute_sdk_definitions(python / "v4/Payment.py", namespace)
    for method, (name, route) in aggregation.items():
        request = namespace[name]()
        request.req_seq_id = "offline-current"
        request.org_req_seq_id = "offline-original"
        request.org_hf_seq_id = ""
        actual_route, data = getattr(namespace["Payment"], method)(request)
        assert actual_route == route and isinstance(data, dict), method
        if method in {"close", "close_query"}:
            for first, second in (("both-a", "both-b"), ("", "")):
                request.org_req_seq_id, request.org_hf_seq_id = first, second
                try:
                    getattr(namespace["Payment"], method)(request)
                except ValueError:
                    pass
                else:
                    raise AssertionError(f"{method} accepted invalid original locator pair")

    namespace.update({"os": os, "open": lambda *args: io.BytesIO(b"synthetic-image"),
                      "request_post": lambda url, request_params, files, **kwargs:
                      dict(kwargs, url=url, request_params=request_params, files=files)})
    execute_sdk_definitions(python / "request/v2_supplementary_picture_request.py", namespace)
    picture = namespace["V2SupplementaryPictureRequest"]()
    try:
        picture.post({"file_url": "https://unused.invalid/image"})
    except AttributeError:
        pass
    else:
        raise AssertionError("image Request no longer lacks picture; review defect guidance")
    picture.picture = "/unused/offline.png"
    picture.req_date, picture.req_seq_id, picture.file_type = "20260924", "offline", "F01"
    image_call = picture.post({"file_url": "https://unused.invalid/image", "offline_marker": "ignored"})
    assert image_call["need_sign"] is False and image_call["need_verfy_sign"] is False
    assert set(image_call["files"]) == {"picture"}
    assert set(image_call["request_params"]) == {"file_type", "picture"}
    print("[OK] Python 23 extension/legacy/payment Request serializers, 6 aggregation routes, 4 generic routes and image defects (HTTP stubbed; merchant/user probes are separate)")


def validate_python_transport_boundary(request, namespace: dict) -> None:
    calls: list[dict] = []
    response = SimpleNamespace(status_code=200, text='{"data":{"offline":true}}', close=lambda: None)
    session = SimpleNamespace(mount=lambda *args: None,
                              post=lambda url, **kwargs: calls.append(kwargs) or response)
    namespace.update({"requests": SimpleNamespace(Session=lambda: session),
                      "HTTPAdapter": lambda **kwargs: None, "Retry": lambda **kwargs: None,
                      "log_info": lambda message: None, "verify_sign": lambda *args: (False, "offline-bad-signature")})
    request.request_params = {"file_url": "https://unused.invalid/image"}
    assert request.post() == {"data": {"offline": True}}
    assert "json" in calls[-1] and "data" not in calls[-1], "file_url alone must not be claimed multipart"
    request.post({"file": io.BytesIO(b"synthetic-image")})
    assert "data" in calls[-1] and "json" not in calls[-1]
    assert isinstance(calls[-1]["data"]["data"], str)
    assert "Content-Type" not in calls[-1]["headers"]
    assert all("verify" not in call for call in calls), "SDK changed requests TLS defaults"
    response.text = '{"data":{"offline":true},"sign":"synthetic-invalid"}'
    try:
        request._build_return_data(response)
    except RuntimeError:
        pass
    else:
        raise AssertionError("bad signed response was not rejected")
    print("[OK] Python JSON/multipart, unsigned-envelope and bad-signed-response boundaries (HTTP/crypto stubbed)")


def validate_python_crypto(python: Path, state: ValidationState) -> None:
    if importlib.util.find_spec("Crypto") is None:
        state.warning("Actual Python SDK RSA probe not run: PyCryptodome is unavailable; AST/stub probes do not prove cryptographic execution")
        return
    namespace: dict = {}
    exec(compile((python / "core/rsa_utils.py").read_text(encoding="utf-8"), "local_rsa_utils", "exec"), namespace)
    key = namespace["RSA"].generate(2048)
    private, public = key.export_key(pkcs=8).decode(), key.public_key().export_key().decode()
    message = json.dumps({"offline": "合成数据", "amount": "1.00"}, ensure_ascii=False, separators=(",", ":"))
    signed, signature = namespace["rsa_sign"](private, message)
    assert signed and namespace["rsa_design"](signature, message, public)[0]
    assert not namespace["rsa_design"](signature, message + "tampered", public)[0]
    state.ok("Actual SDK RSA/SHA256 sign, verify and tamper rejection passed with generated in-memory test key (no gateway/SM2 claim)")


def validate_python_contract_texts(state: ValidationState) -> None:
    for path in PYTHON_CONTRACT_FILES:
        text = current_sdk_text(path.read_text(encoding="utf-8"))
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
    for path in (EXPECTED_SKILL_FILE, *PYTHON_ENV_DOC_FILES):
        text = path.read_text(encoding="utf-8")
        if PYTHON_SDK_VERSION not in text:
            state.error(f"{path.name}: active payment SDK baseline {PYTHON_SDK_VERSION} is missing")
    for path in (REPO_ROOT / "huifu-merchant-onboarding").rglob("*.md"):
        for problem in current_python_claim_errors(path.read_text(encoding="utf-8")):
            state.error(f"{path.relative_to(REPO_ROOT)}: {problem}")
    state.ok(f"Independent Python SDK baselines checked: payment {PYTHON_SDK_VERSION}, onboarding {PYTHON_SDK_VERSION}")


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
