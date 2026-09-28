#!/usr/bin/env python3
"""Verify the source-backed merchant-onboarding SDK claims without bundling the SDK."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from skill_validation_config import SDK_SOURCE_LOCK, onboarding_source_date, sdk_root_relative, sdk_version
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


REPO_ROOT = Path(__file__).resolve().parent.parent
SDK_LOCK = SDK_SOURCE_LOCK


def find_component(root: Path, label: str, candidates: tuple[Path, ...], marker: Path, *, selected: Path | None = None) -> Path:
    """Prefer the explicitly locked layout, never a highest-version heuristic."""
    if selected is not None and (root / selected / marker).is_file():
        return root / selected
    matches = sorted({(root / candidate).resolve() for candidate in candidates if (root / candidate / marker).is_file()})
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(f"ambiguous {label} layouts under {root}: {matches}")
    searched = ", ".join(str(root / candidate / marker) for candidate in candidates)
    raise ValueError(f"{label} not found under SDK root {root}; searched: {searched}")


def python_source_version(python: Path) -> str:
    """Read the runtime declaration without importing SDK initialization or HTTP."""
    tree = ast.parse((python / "dg_client.py").read_text(encoding="utf-8"))
    versions = [node.value.value for node in ast.walk(tree)
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)
                and any(isinstance(target, ast.Name) and target.id == "__version__" for target in node.targets)]
    if len(versions) != 1:
        raise ValueError(f"expected one Python SDK runtime version declaration: {python}")
    return versions[0]


def resolve_python_sdk(root: Path) -> Path:
    python = find_component(root, "Python SDK", (
        Path("bspay-python-sdk/dg_sdk"),
        Path("bspay-python-sdk-feature_generator_sdk/dg_sdk"),
        Path("dg_sdk"),
    ), Path("dg_client.py"), selected=Path(sdk_root_relative("python")))
    actual, expected = python_source_version(python), sdk_version("python")
    if actual != expected:
        raise ValueError(f"Python SDK declaration differs from active evidence: {actual} != {expected} ({python})")
    return python


def resolve_sdk_layout(root: Path) -> tuple[Path, Path, Path]:
    if not root.is_dir():
        raise ValueError(f"SDK root is not a directory: {root}")
    java = find_component(
        root,
        "Java SDK",
        (
            Path("bspay-java-sdk"),
            Path("bspay-java-sdk-parent-main/bspay-java-sdk-parent-main"),
            Path("bspay-java-sdk-parent-generator-sdk"),
            Path("."),
        ),
        Path("opps-bspay-java-sdk/pom.xml"),
        selected=Path(sdk_root_relative("java")),
    )
    php = find_component(
        root,
        "PHP SDK",
        (
            Path("bspay-php-sdk/BsPaySdk"),
            Path("bspay-php-sdk-master/bspay-php-sdk-master/BsPaySdk"),
            Path("bspay-php-sdk-feature_generator_sdk/BsPaySdk"),
            Path("BsPaySdk"),
        ),
        Path("init.php"),
        selected=Path(sdk_root_relative("php")),
    )
    python = resolve_python_sdk(root)
    return java, php, python


def require_text(path: Path, *terms: str) -> list[str]:
    if not path.is_file():
        return [f"missing {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    return [f"{path}: missing {term}" for term in terms if term not in text]


def forbid_text(path: Path, *terms: str) -> list[str]:
    if not path.is_file():
        return [f"missing {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    return [f"{path}: forbidden stale term {term}" for term in terms if term in text]


def require_text_between(path: Path, start: str, end: str, *terms: str) -> list[str]:
    """Require terms inside a source branch delimited by stable anchors."""
    if not path.is_file():
        return [f"missing {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    start_pos = text.find(start)
    if start_pos < 0:
        return [f"{path}: missing branch start {start}"]
    end_pos = text.find(end, start_pos + len(start))
    if end_pos < 0:
        return [f"{path}: missing branch end {end}"]
    section = text[start_pos:end_pos]
    return [f"{path}: missing term in branch {start}: {term}" for term in terms if term not in section]


def require_ordered_text(path: Path, anchor: str, *terms: str) -> list[str]:
    """Require terms in order after an anchor, for security-sensitive snippets."""
    if not path.is_file():
        return [f"missing {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    anchor_pos = text.find(anchor)
    if anchor_pos < 0:
        return [f"{path}: missing ordered-text anchor {anchor}"]
    cursor = anchor_pos + len(anchor)
    for term in terms:
        cursor = text.find(term, cursor)
        if cursor < 0:
            return [f"{path}: missing ordered term after {anchor}: {term}"]
        cursor += len(term)
    return []


def require_same_line(path: Path, anchor: str, *terms: str) -> list[str]:
    """Require route dependencies on the same manifest line as the route anchor."""
    if not path.is_file():
        return [f"missing {path}"]
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    matching = [line for line in lines if anchor in line]
    if not matching:
        return [f"{path}: missing route anchor {anchor}"]
    return [f"{path}: route {anchor} missing {term}" for term in terms if not any(term in line for line in matching)]


def source_tree_digest(root: Path, language: str) -> tuple[int, str]:
    files: list[Path] = []
    for directory, child_dirs, names in os.walk(root):
        child_dirs[:] = [name for name in child_dirs if name not in {"target", "__pycache__", ".git"}]
        for name in names:
            path = Path(directory) / name
            if language == "java":
                include = path.name == "pom.xml" or path.suffix == ".java"
            else:
                include = path.suffix == (".php" if language == "php" else ".py")
            if include and path.is_file():
                files.append(path)
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return len(files), digest.hexdigest()


def sdk_history_errors(lock: dict) -> list[str]:
    previous = lock.get("previous_source_lock")
    if not isinstance(previous, dict) or not {"path", "sha256"} <= previous.keys():
        return ["current SDK evidence must bind previous_source_lock path and SHA"]
    path = REPO_ROOT / previous["path"]
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != previous["sha256"]:
        return ["historical SDK source lock SHA differs; do not relabel or overwrite historical evidence"]
    return []


def run_checked(command: list[str], cwd: Path | None = None) -> list[str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=240,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [f"cannot execute {' '.join(command)}: {exc}"]
    if result.returncode:
        output = result.stdout[-4000:].strip()
        return [
            f"command failed ({result.returncode}): {' '.join(command)}"
            + (f"\n{output}" if output else "")
        ]
    return []


def copy_java_sources(java: Path, destination: Path) -> Path:
    """Copy only build descriptors and Java sources; never compile in user SDKs."""
    for directory, child_dirs, names in os.walk(java):
        child_dirs[:] = [name for name in child_dirs if name not in {"target", ".git", "__pycache__"}]
        for name in names:
            source = Path(directory) / name
            if source.name != "pom.xml" and source.suffix != ".java":
                continue
            target = destination / source.relative_to(java)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return destination


def validate_java_runtime(java: Path, requests: tuple[str, ...], routes: dict[str, str]) -> list[str]:
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="huifu-merchant-sdk-java-") as directory:
        isolated = copy_java_sources(java, Path(directory) / "sdk")
        build_errors = run_checked(
            ["mvn", "-q", "-pl", "opps-bspay-java-sdk", "-am", "-DskipTests", "compile"], isolated
        )
        if build_errors:
            return build_errors
        classes = isolated / "opps-bspay-java-sdk/target/classes"
        for request_name, enum_name in zip(requests, routes, strict=True):
            try:
                result = subprocess.run(
                    ["javap", "-classpath", str(classes), "-c", f"com.huifu.bspay.sdk.opps.core.request.{request_name}"],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False, timeout=30,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                problems.append(f"cannot inspect Java {request_name}: {exc}")
                continue
            if result.returncode or f"FunctionCodeEnum.{enum_name}" not in result.stdout:
                problems.append(f"compiled Java {request_name} route mismatch")
    return problems


def validate_current_agreement_routes(java: Path, php: Path, python: Path) -> list[str]:
    """New invoice classes are not dedicated support for migrated agreement APIs."""
    problems: list[str] = []
    java_root = java / "opps-bspay-java-sdk/src/main/java/com/huifu/bspay/sdk/opps"
    enums = (java_root / "core/enums/FunctionCodeEnum.java", php / "enums/FunctionCodeEnum.php", python / "request/request_api_urls.py")
    lock = json.loads(SDK_LOCK.read_text(encoding="utf-8"))
    routes = lock["current_contract_routes"]
    expected = {"resend": "/v2/agreement/elect/signurl/resend", "list": "/v2/agreement/apply/list", "reject": "/v2/agreement/elect/rejectsign"}
    if routes != expected:
        problems.append("current electronic-contract route lock differs from verified API routes")
    for route in expected.values():
        for enum in enums:
            problems += forbid_text(enum, route.lstrip("/"), route.lstrip("/").replace("/", "."))
    for class_name, code in (("V2InvoiceContractrepeatRequest", "CONTRACTREPEAT"), ("V2InvoiceQueryecmsapplylistRequest", "QUERYECMSAPPLYLIST"), ("V2InvoiceRejectsignRequest", "REJECTSIGN")):
        problems += require_text(java_root / "core/request" / f"{class_name}.java", f"FunctionCodeEnum.V2_INVOICE_{code}")
        problems += require_text(php / "request" / f"{class_name}.php", f"FunctionCodeEnum::$V2_INVOICE_{code}")
    problems += require_text(java_root / "client/BasePayClient.java", "request(Map<String, Object> params, String funcCode, boolean isPage)", 'funcCode.replaceAll("\\\\.", "/")')
    problems += require_text(php / "core/BsPayClient.php", "$data = $request;", "self::post($data['funcCode'], $data['params']")
    problems += require_text(python / "dg_tools.py", "def request_post(cls, url, request_params, files=None)", "return request_post(url=url, request_params=required_params, files=files)")
    problems += require_text(python / "core/request_tools.py", "need_sign=True", "need_verfy_sign=True")
    matrix = REPO_ROOT / "huifu-merchant-onboarding/references/onboarding-extension-shared-server-sdk-matrix.md"
    problems += require_text(matrix, *expected.values(), "旧", "通用入口", "不能", "V2InvoiceContractrepeatRequest", sdk_version("python"))
    # Exercise public generic entry points with a recording boundary: never HTTP.
    php_probe = f'require {json.dumps(str(php / "init.php"))}; ' + r'''
$client = new \BsPaySdk\core\BsPayClient();
foreach (json_decode($argv[1], true) as $route) {
    if (parse_url($client->getRequestUrl(ltrim($route, '/')), PHP_URL_PATH) !== $route) exit(7);
}
'''
    problems += run_checked(["php", "-r", php_probe, json.dumps(list(expected.values()))])
    # BsPayClient uses self::post, so mock the parent boundary before loading it;
    # overriding post in a child would not intercept that early-bound call.
    php_capture = r'''
namespace BsPaySdk\core;
class BsPay {
    public function post($funcCode, $params, $file, $merchantKey) {
        return array($funcCode, $params, $file);
    }
}
require $argv[1];
$client = new BsPayClient();
foreach (json_decode($argv[2], true) as $route) {
    $params = array('req_seq_id' => 'offline-probe', 'native_array' => array('offline'));
    $code = ltrim($route, '/');
    $result = $client->postRequest(array('funcCode' => $code, 'params' => $params));
    if ($result !== array($code, $params, '')) exit(8);
}
'''
    problems += run_checked(["php", "-r", php_capture, str(php / "core/BsPayClient.php"), json.dumps(list(expected.values()))])
    python_probe = r'''
import ast, json, pathlib, sys
path = pathlib.Path(sys.argv[1]) / 'dg_tools.py'
tree = ast.parse(path.read_text(encoding='utf-8'))
node = next(item for item in tree.body if isinstance(item, ast.ClassDef) and item.name == 'DGTools')
namespace = {'request_post': lambda url, request_params, files=None: (url, request_params, files)}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), namespace)
for route in json.loads(sys.argv[2]):
    params = {'req_seq_id': 'offline-probe', 'native_array': ['offline']}
    assert namespace['DGTools'].request_post(route, params) == (route, params, None)
'''
    problems += run_checked([sys.executable, "-B", "-c", python_probe, str(python), json.dumps(list(expected.values()))])
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk-root", type=Path, default=os.environ.get("HUIFU_SDK_ROOT"))
    args = parser.parse_args()
    if args.sdk_root is None:
        parser.error("--sdk-root or HUIFU_SDK_ROOT is required")
    root = args.sdk_root.resolve()
    try:
        java, php, python = resolve_sdk_layout(root)
    except ValueError as exc:
        parser.error(str(exc))
    problems: list[str] = []
    problems += validate_current_agreement_routes(java, php, python)
    sdk_lock = json.loads(SDK_LOCK.read_text(encoding="utf-8"))
    problems += sdk_history_errors(sdk_lock)
    for language, component in (("java", java), ("php", php), ("python", python)):
        count, digest = source_tree_digest(component, language)
        expected = sdk_lock["components"][language]
        if count != expected["file_count"] or digest != expected["tree_sha256"]:
            problems.append(
                f"{language} SDK source tree differs from user-provided lock: "
                f"files={count}/{expected['file_count']} sha256={digest}/{expected['tree_sha256']}"
            )

    routes = {
        "V2_MERCHANT_BASICDATA_ENT": "v2/merchant/basicdata/ent",
        "V2_MERCHANT_BASICDATA_INDV": "v2/merchant/basicdata/indv",
        "V2_MERCHANT_BUSI_OPEN": "v2/merchant/busi/open",
        "V2_MERCHANT_BASICDATA_QUERY": "v2/merchant/basicdata/query",
        "V2_MERCHANT_BASICDATA_STATUS_QUERY": "v2/merchant/basicdata/status/query",
        "V2_MERCHANT_BUSI_MODIFY": "v2/merchant/busi/modify",
        "V2_MERCHANT_BASICDATA_MODIFY": "v2/merchant/basicdata/modify",
        "V2_MERCHANT_BUSI_MODIFY_BUSISTATUS": "v2/merchant/busi/modify/busistatus",
        "V2_MERCHANT_BASICDATA_SMS_SEND": "v2/merchant/basicdata/sms/send",
        "V2_MERCHANT_BUSI_MULTIFEE_CONFIG": "v2/merchant/busi/multiFee/config",
        "V2_MERCHANT_BUSI_MULTIFEE_QUERY": "v2/merchant/busi/multiFee/query",
    }

    java_requests = (
        "V2MerchantBasicdataEntRequest",
        "V2MerchantBasicdataIndvRequest",
        "V2MerchantBusiOpenRequest",
        "V2MerchantBasicdataQueryRequest",
        "V2MerchantBasicdataStatusQueryRequest",
        "V2MerchantBusiModifyRequest",
        "V2MerchantBasicdataModifyRequest",
        "V2MerchantBusiModifyBusistatusRequest",
        "V2MerchantBasicdataSmsSendRequest",
        "V2MerchantBusiMultifeeConfigRequest",
        "V2MerchantBusiMultifeeQueryRequest",
    )
    problems += require_text(java / "opps-bspay-java-sdk" / "pom.xml", "<version>3.0.41</version>")
    java_source = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core"
    problems += require_text(java_source / "config/MerConfig.java", "setProductId")
    problems += require_text(java_source / "BasePay.java", "public static volatile boolean debug = true;")
    abstract_request = java_source / "net/AbstractRequest.java"
    problems += require_text(abstract_request, '"v2/supplementary/picture"', "file == null", "httpPostNoFile", 'System.out.println("PRIVATE_KEY=" + privateKey)', 'System.out.println("request sign=" + requestSign)', 'System.out.println("request data = "')
    problems += require_ordered_text(abstract_request, "File file, String fileParam", "obtainSign(config, reqData)", 'System.out.println("request sign=" + requestSign)', 'System.out.println("request data = "', '"v2/supplementary/picture".equals(uri)')
    problems += require_ordered_text(abstract_request, "File file, String fileParam", "obtainSign(config, reqData)", "if (isPage)", "checkSignFlag(config, data, sign)")
    problems += require_text(abstract_request, "RsaUtils.sign(sortedData, privateKey)", "RsaUtils.verify(sortedData, publicKey, sign)", "BasePay.SM2_ALGORITHM")
    java_client = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/client/BasePayClient.java"
    problems += require_text(java_client, "isPage true 客户端不做验签操作", "upload(BaseRequest request, File file)", 'file, "file", merchantKey, true)')
    java_request_root = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core/request"
    java_enum = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core/enums/FunctionCodeEnum.java"
    problems += require_text(
        java_request_root / "V2SupplementaryPictureRequest.java",
        "class V2SupplementaryPictureRequest",
        "V2_SUPPLEMENTARY_PICTURE",
        "setReqSeqId",
        "setReqDate",
        "setFileType",
    )
    problems += require_text(java_enum, "V2_SUPPLEMENTARY_PICTURE", "v2.supplementary.picture")
    for name, enum_name in zip(java_requests, routes, strict=True):
        problems += require_text(java_request_root / f"{name}.java", f"class {name}", f"return FunctionCodeEnum.{enum_name};")
    problems += require_text(
        java_request_root / "V2MerchantBusiMultifeeConfigRequest.java",
        "setReqSeqId",
        "setReqDate",
        "setHuifuId",
    )
    problems += forbid_text(
        java_request_root / "V2MerchantBusiMultifeeConfigRequest.java",
        "wx_conf_list",
        "ali_conf_list",
    )
    problems += require_text(
        java_client,
        "params.putAll(request.getExtendInfos())",
    )
    problems += require_text(
        java_request_root / "V2MerchantBusiMultifeeQueryRequest.java",
        "setReqSeqId",
        "setReqDate",
        "setHuifuId",
    )
    problems += forbid_text(
        java_request_root / "V2MerchantBusiMultifeeQueryRequest.java",
        "fee_sign",
        "wx_conf_list",
        "ali_conf_list",
    )
    problems += forbid_text(
        java_request_root / "V2MerchantBasicdataEntRequest.java",
        "material_card_info",
    )
    for enum_name, route in routes.items():
        problems += require_text(java_enum, enum_name, route.replace("/", "."))
    problems += forbid_text(java_enum, "V2_MERCHANT_FEE_RATE_QUERY", "v2.merchant.fee-rate.query")

    php_requests = java_requests
    problems += require_text(php / "init.php", 'define("SDK_VERSION", "php_v2.0.31")')
    problems += require_text(
        php / "init.php",
        'if (!defined("DEBUG"))',
        'define("DEBUG", false)',
    )
    problems += require_text(
        php.parent / "BsPayDemo/loader.php",
        'define("DEBUG", true)',
        "SDK 初始化文件加载",
    )
    problems += require_text(
        php.parent / "Composer/BsPayConfig.php",
        'if (!defined("DEBUG"))',
        'define("DEBUG", true)',
        "BsPay::init",
    )
    problems += require_text(
        php / "config/MerConfig.php",
        "public $rsa_merch_private_key",
    )
    problems += require_text(
        php / "core/BsPay.php",
        'self::$isDebug = defined("DEBUG") && DEBUG',
        "if (self::$isDebug)",
    )
    problems += require_text(php / "enums/FunctionCodeEnum.php", "V2_SUPPLEMENTARY_PICTURE")
    problems += require_text(php / "core/BsPay.php", "if (empty($file))", "Content-Type:application/json", "$is_json = true", "$huifuId = $request_params['huifu_id']", "Content-Type:multipart/form-data", "$is_json = false")
    problems += require_text(php / "core/BsPayClient.php", "if (is_object($tag))", "$data['params']['needSign'] = false", "$data['params']['needVerfySign'] = false")
    problems += require_text(
        php / "request/V2SupplementaryPictureRequest.php",
        "class V2SupplementaryPictureRequest",
        "V2_SUPPLEMENTARY_PICTURE",
        "setReqSeqId",
        "setReqDate",
        "setFileType",
    )
    problems += require_text(
        php.parent / "BsPayDemo/V2SupplementaryPictureRequestDemo.php",
        "CURLFile",
        'extendInfoMap["file_url"]',
        "postRequest($request,new CURLFile",
    )
    problems += require_text(
        php / "core/BsPayRequestV2.php",
        'json_encode(func_get_args()',
        "post-json请求参数:",
        "post-form请求参数:",
        "curl返回参数:",
    )
    problems += require_text_between(
        php / "core/BsPay.php",
        "Content-Type:multipart/form-data",
        "// 实例化 http 请求执行",
        "jpt-x-skill-source",
        "jpt-sdk_version",
    )
    for name, enum_name in zip(php_requests, routes, strict=True):
        problems += require_text(php / "request" / f"{name}.php", f"class {name}", f"return FunctionCodeEnum::${enum_name};")
    problems += forbid_text(
        php / "request/V2MerchantBusiMultifeeConfigRequest.php",
        "wx_conf_list",
        "ali_conf_list",
    )
    problems += require_text(
        php / "core/BsPayClient.php",
        "array_merge($arrayData, $extendInfos)",
    )
    problems += forbid_text(
        php / "request/V2MerchantBusiMultifeeQueryRequest.php",
        "fee_sign",
        "wx_conf_list",
        "ali_conf_list",
    )
    problems += forbid_text(
        php / "request/V2MerchantBasicdataEntRequest.php",
        "material_card_info",
    )
    for enum_name, route in routes.items():
        problems += require_text(php / "enums/FunctionCodeEnum.php", enum_name, route)
    problems += forbid_text(
        php / "enums/FunctionCodeEnum.php",
        "V2_MERCHANT_FEE_RATE_QUERY",
        "v2/merchant/fee-rate/query",
    )

    python_requests = (
        "v2_merchant_basicdata_ent_request.py",
        "v2_merchant_basicdata_indv_request.py",
        "v2_merchant_busi_open_request.py",
        "v2_merchant_basicdata_query_request.py",
        "v2_merchant_basicdata_status_query_request.py",
        "v2_merchant_busi_modify_request.py",
        "v2_merchant_basicdata_modify_request.py",
        "v2_merchant_busi_modify_busistatus_request.py",
        "v2_merchant_basicdata_sms_send_request.py",
        "v2_merchant_busi_multifee_config_request.py",
        "v2_merchant_busi_multifee_query_request.py",
    )
    if python_source_version(python) != sdk_version("python"):
        problems.append("Python runtime declaration differs from active SDK evidence")
    problems += require_text(python / "__init__.py", "from dg_sdk.dg_tools import DGTools")
    problems += require_text(python / "dg_tools.py", "class DGTools", "def request_post", "return request_post")
    problems += require_text(python / "core/request_tools.py", "def request_post", "files=None", "need_sign=True", "need_verfy_sign=True", "ApiRequest.post(files)")
    problems += require_text(
        python / "request/v2_supplementary_picture_request.py",
        "class V2SupplementaryPictureRequest",
        "def post(self, extend_infos)",
        "self.picture",
        "file = {'picture':",
        '"picture": os.path.basename(self.picture)',
        "need_sign=False",
        "need_verfy_sign=False",
    )
    problems += forbid_text(
        python / "request/v2_supplementary_picture_request.py",
        '"req_seq_id": self.req_seq_id',
        '"req_date": self.req_date',
        "required_params.update(extend_infos)",
    )
    # The current sdist has no demo directory. Core Request behavior is tested
    # directly; historical Demo defects are not a current-source requirement.
    problems += require_text(python / "core/api_request.py", "application/json;charset=utf-8", "elif method == 'post'", "json=params", "Retry(connect=3, backoff_factor=0.5)")
    for name, enum_name in zip(python_requests, routes, strict=True):
        problems += require_text(python / "request" / name, f"from dg_sdk.request.request_api_urls import {enum_name}", f"request_post({enum_name}, required_params)")
    problems += require_text(
        python / "request/v2_merchant_busi_multifee_config_request.py",
        "required_params.update(extend_infos)",
    )
    problems += require_text(
        python / "request/v2_merchant_busi_multifee_query_request.py",
        "required_params.update(extend_infos)",
    )
    problems += forbid_text(
        python / "request/v2_merchant_basicdata_ent_request.py",
        "material_card_info",
    )
    for enum_name, route in routes.items():
        problems += require_text(python / "request/request_api_urls.py", enum_name, f'"/{route}"')
    problems += forbid_text(
        python / "request/request_api_urls.py",
        "V2_MERCHANT_FEE_RATE_QUERY",
        '"/v2/merchant/fee-rate/query"',
    )

    # Compile in a temporary copy, not in the user-owned SDK tree.
    problems += validate_java_runtime(java, java_requests, routes)

    php_script = [f'require "{(php / "init.php").as_posix()}";']
    for request_name, enum_name in zip(php_requests, routes, strict=True):
        request_file = (php / "request" / f"{request_name}.php").as_posix()
        expected_route = routes[enum_name]
        php_script.extend(
            (
                f'require "{request_file}";',
                rf'$request = new \BsPaySdk\request\{request_name}();',
                f'if ($request->getFunctionCode() !== "{expected_route}") '
                f'{{ fwrite(STDERR, "{request_name} route mismatch"); exit(3); }}',
            )
        )
    problems += run_checked(["php", "-r", " ".join(php_script)])

    python_runtime = r'''
import importlib.util
import json
import pathlib
import sys
import types

root = pathlib.Path(sys.argv[1])
cases = json.loads(sys.argv[2])
core = types.ModuleType("dg_sdk.core.request_tools")
core.request_post = lambda route, params: (route, params)
urls = types.ModuleType("dg_sdk.request.request_api_urls")
for case in cases:
    setattr(urls, case["enum"], "/" + case["route"])
sys.modules["dg_sdk"] = types.ModuleType("dg_sdk")
sys.modules["dg_sdk.core"] = types.ModuleType("dg_sdk.core")
sys.modules["dg_sdk.core.request_tools"] = core
sys.modules["dg_sdk.request"] = types.ModuleType("dg_sdk.request")
sys.modules["dg_sdk.request.request_api_urls"] = urls
for case in cases:
    path = root / "request" / case["file"]
    spec = importlib.util.spec_from_file_location("sdk_case", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    request = getattr(module, case["class"])()
    route, params = request.post({})
    assert route == "/" + case["route"], (case["class"], route)
    assert isinstance(params, dict)
'''
    python_cases = [
        {
            "file": filename,
            "class": request_name,
            "enum": enum_name,
            "route": routes[enum_name],
        }
        for filename, request_name, enum_name in zip(
            python_requests, java_requests, routes, strict=True
        )
    ]
    problems += run_checked(
        [
            sys.executable,
            "-c",
            python_runtime,
            str(python),
            json.dumps(python_cases),
        ]
    )

    matrix = REPO_ROOT / "huifu-merchant-onboarding/references/shared-server-sdk-matrix.md"
    image = REPO_ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-image-upload.md"
    enterprise = REPO_ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-enterprise.md"
    individual = REPO_ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-individual.md"
    contracts = REPO_ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-field-contracts.md"
    credentials = REPO_ROOT / "huifu-merchant-onboarding/references/shared-credential-boundary.md"
    headers = REPO_ROOT / "huifu-merchant-onboarding/references/shared-request-header-policy.md"
    skill = REPO_ROOT / "huifu-merchant-onboarding/SKILL.md"
    prompts = REPO_ROOT / "scripts/huifu-payment-test-prompts.json"
    problems += require_text(
        matrix,
        "服务端 SDK 能力矩阵",
        "十一个已有专属类的 JSON 接口",
        "V2MerchantBusiModifyRequest",
        "V2MerchantBasicdataModifyRequest",
        "V2MerchantBusiModifyBusistatusRequest",
        "V2MerchantBasicdataSmsSendRequest",
        "V2MerchantBusiMultifeeConfigRequest",
        "/v2/merchant/busi/multiFee/config",
        "V2MerchantBusiMultifeeQueryRequest",
        "/v2/merchant/busi/multiFee/query",
        "扩展映射必须拒绝这三个定位键",
        "费率查询缺口",
        "/v2/merchant/fee-rate/query",
        "3.0.41",
        "2.0.31",
        sdk_version("python"),
        "`DGTools.request_post`",
        "`V2SupplementaryPictureRequest`",
        "`BasePayClient.upload(request, file)`",
        "官方专用实现不可用",
        "受控降级可实现",
        "`BasePay.debug` 默认 `true`",
        "全局设置为 `false`",
        "`CURLFile`",
        "关闭请求签名和响应验签",
        "## 调试日志硬停",
        "`BsPayDemo/loader.php`",
        "`Composer/BsPayConfig.php`",
        "`DEBUG=true`",
        "`DEBUG=false`",
        "`rsa_merch_private_key`",
        "完整请求体与完整响应",
        "## 官方 SDK-first 与图片例外",
        "CURLOPT_SSL_VERIFYPEER=false",
        "非阻断",
        "汇付官方或汇付开发者交流沟通群",
        "常规接口不得用",
        "唯一例外是 `/v2/supplementary/picture`",
        "不得只让 Python 用 SDK",
    )
    problems += require_text(
        image,
        "当前锁定 SDK 中，只有 Java",
        "multipart 文本字段",
        "PHP `php_v2.0.31`",
        f"Python `dg_sdk {sdk_version('python')}`",
        "DGTools.request_post",
        "PHP / Python 受控降级",
        "V2SupplementaryPictureRequest",
        "`needSign`、`needVerfySign` 都设为 `false`",
        "BasePayClient.request(request, true)",
        "BasePayClient.upload(request, new File",
        "`BasePay.debug` 默认为 `true`",
        "BasePay.debug = false;",
        "私钥、签名",
        "请求数据",
        "但没有顶层 `sign`",
        "元数据 `sign=true`",
        "两条路径都先对 `data` 加签",
        "在响应验签前",
        "CURLFile",
        "受控通用 POST",
        "`sys_id`、`product_id`、`data`、`sign`",
        "`need_sign=True`",
        "不启用自动业务重试",
        "`hfms/1.0.4`",
        "`hfps/1.3.5;hfms/1.0.4`",
    )
    problems += require_ordered_text(
        image,
        "受控 `file_url`",
        "BasePay.debug = false;",
        "V2SupplementaryPictureRequest",
        "BasePayClient.request(request, true)",
    )
    problems += require_ordered_text(
        image,
        "### 本地文件",
        "BasePay.debug = false;",
        "V2SupplementaryPictureRequest",
        "BasePayClient.upload(request, new File",
    )
    problems += forbid_text(
        image,
        "function uploadPictureByUrl",
        'data, "default", false);',
    )
    for page in (enterprise, individual):
        problems += require_text(page, "async_return_url", "notify_url", "禁止")
        problems += forbid_text(page, 'extendInfoMap.put("notify_url"', 'data.put("notify_url"')
    problems += require_text(
        enterprise,
        'extendInfoMap.put("async_return_url", request.asyncReturnUrl());',
        "三个锁定版本均没有 `material_card_info` 或新 `head_type` 的专属字段/setter",
        "exact-key 扩展字段能力",
        "键必须保持 `material_card_info`",
        "整体序列化得到的 JSON 字符串",
        "不得发送普通嵌套 Object",
    )
    problems += require_text(prompts, '"id": 69', '"id": 70', '"id": 71', '"id": 74', '"id": 87', '"id": 88', '"id": 89', "请求签名保留", "响应验签跳过", "CURLFile", "官方 Demo 同时传入互斥来源", "V2MerchantBasicdataIndvRequest", "V2MerchantBusiMultifeeConfigRequest", "V2MerchantBusiMultifeeQueryRequest", "async_return_url", "notify_url", "Java HttpClient/OkHttp/HttpURLConnection", "PHP Guzzle/curl", "SDK 没有对应接口能力时报告缺口")
    problems += forbid_text(matrix, "`dg_sdk.request_post")
    problems += forbid_text(image, "dg_sdk.request_post")
    problems += require_text(contracts, f"来源快照核验日期：`{onboarding_source_date()}`", "企业商户进件", "个人商户进件", "商户业务开通", "图片上传", "商户详细信息查询", "申请单状态查询", "商户业务开通修改", "商户基本信息修改", "商户费率信息查询", "商户状态变更", "商户短信发送", "商户多费率配置", "商户多费率配置查询", "fee_sign:String(32) N", "wx_conf_list/ali_conf_list", "响应 `conf_list:String/jsonArray格式`", "按 String(JSON Array) 解码", "agreement_info.agreement_async_return_url", "reg_result_list[].business_stat", "async.agreement.agreement_info_list.con_stat", "data.wx_zl_config.apply_state", "data.ali_zl_config[].apply_status", "RECV_ORD_ID_", "file_url String(512)", "apply_status", "十一个已有专属 Request 类的 JSON 接口", "公共 `AbstractRequest`", "`BasePay.debug` 默认为 `true`", "BasePay.debug = false;", "任何 SDK 请求之前", "不得在并发请求中临时切换", "`BsPayDemo/loader.php`", "`Composer/BsPayConfig.php`", "`DEBUG=false`", "`DEBUG=true`", "`rsa_merch_private_key`", "完整请求体和完整响应", "不得按叶字段名去重", "request.data.card_info.prov_id", "request.data.card_info.area_id", "不能跨接口复用长度", "hfms/1.0.4", "hfps/1.3.5;hfms/1.0.4")
    problems += require_text(credentials, "进件凭据与敏感资料边界", "RSA 私钥", "禁止写入", "Java 必须", "`BasePay.debug = false`", "PHP 必须", "`BsPay::init`", "`DEBUG=false`", "`DEBUG=true`", "Demo loader", "完整请求、响应", "`hfms/1.0.4`", "`hfps/1.3.5;hfms/1.0.4`")
    problems += require_text(headers, "默认 `skill_source`", "`hfms/1.0.4`", "`hfps/1.3.5;hfms/1.0.4`", "顺序固定为支付、进件", "英文分号且不加空格", "原样透传")
    for path in (matrix, image, enterprise, individual, contracts, credentials, headers, skill):
        problems += forbid_text(path, "jpt-x-skill-huifu_id", "jpt_x_skill_huifu_id")
    problems += require_text(
        skill,
        "## 官方 SDK-first 与图片例外",
        "## SDK 与图片安全边界",
        "公共 `AbstractRequest`",
        "私钥、签名和请求数据",
        "`BasePay.debug` 默认为 `true`",
        "进程初始化阶段、任何请求之前",
        "不得并发临时切换",
        "并保留签验",
        "唯一受控例外",
        "`josnArray`",
        "`DEBUG=true`",
        "`DEBUG=false`",
        "`BsPay::init`",
        "TLS源码现状另作非阻断提醒",
        "用户要求 PHP 联调或生产可运行代码",
        "TLS",
        "常规接口真实请求都使用官方 Request/Client 入口",
        "唯一例外是 `/v2/supplementary/picture`",
        "通用 POST",
        "自写 HTTP 传输适配器",
        "商户费率查询仍禁止手写 HTTP",
        "PHP/Python 图片上传按上述唯一例外允许受控降级",
        "当前锁定版本只有 Java 图片上传专用实现可用",
        "BasePayClient.upload(request, file)",
        "DGTools.request_post",
        "商户多费率配置",
        "`wx_conf_list/ali_conf_list`",
        "响应 `conf_list` 同样按 String(JSON Array) 解码",
        "商户多费率配置查询",
        "`fee_sign:String(32) N`",
        "`request.data.prov_id/area_id`",
        "`request.data.card_info.prov_id/area_id`",
        "`hfms/1.0.4`",
        "`hfps/1.3.5;hfms/1.0.4`",
    )
    for anchor in (
        "企业商户进件",
        "无执照个人商户进件",
        "首次业务开通，或补开银行卡、银联等仍由 `/busi/open` 承载的能力",
        "商户详细信息查询",
        "申请单状态查询",
        "微信/支付宝/抖音补开，线上业务开通，或已开通能力的参数、费率修改",
        "商户基本信息修改",
        "商户费率信息查询",
        "商户状态开通或关闭",
        "商户短信发送或验证码核实",
        "商户多费率配置",
        "查询商户多费率配置或按 `fee_sign` 定位配置",
    ):
        problems += require_same_line(skill, anchor, "merchant-onboarding-field-contracts.md")
    problems += require_same_line(
        skill,
        "十一个已有专属类的 JSON 接口 SDK",
        "merchant-onboarding-field-contracts.md",
        "shared-server-sdk-matrix.md",
    )
    if problems:
        print("Merchant-onboarding SDK evidence validation failed:")
        print("\n".join(problems))
        return 1
    print(
        "Merchant-onboarding SDK evidence validation passed "
        f"(java={java}, php={php}, python={python})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
