#!/usr/bin/env python3
"""Verify the source-backed merchant-onboarding SDK claims without bundling the SDK."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from skill_validation_config import onboarding_source_date
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


REPO_ROOT = Path(__file__).resolve().parent.parent
SDK_LOCK = REPO_ROOT / "maintainer-contracts/merchant-onboarding-sdk-source-lock.json"


def find_component(root: Path, label: str, candidates: tuple[Path, ...], marker: Path) -> Path:
    """Resolve one SDK component from supported official archive layouts."""
    for candidate in candidates:
        path = root / candidate
        if (path / marker).is_file():
            return path
    searched = ", ".join(str(root / candidate / marker) for candidate in candidates)
    raise ValueError(f"{label} not found under SDK root {root}; searched: {searched}")


def resolve_sdk_layout(root: Path) -> tuple[Path, Path, Path]:
    if not root.is_dir():
        raise ValueError(f"SDK root is not a directory: {root}")
    java = find_component(
        root,
        "Java SDK",
        (
            Path("bspay-java-sdk-parent-main/bspay-java-sdk-parent-main"),
            Path("bspay-java-sdk-parent-generator-sdk"),
            Path("."),
        ),
        Path("opps-bspay-java-sdk/pom.xml"),
    )
    php = find_component(
        root,
        "PHP SDK",
        (
            Path("bspay-php-sdk-master/bspay-php-sdk-master/BsPaySdk"),
            Path("bspay-php-sdk-feature_generator_sdk/BsPaySdk"),
            Path("BsPaySdk"),
        ),
        Path("init.php"),
    )
    python = find_component(
        root,
        "Python SDK",
        (
            Path("bspay-python-sdk-feature_generator_sdk/dg_sdk"),
            Path("dg_sdk"),
        ),
        Path("dg_client.py"),
    )
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
    for path in root.rglob("*"):
        if not path.is_file() or any(
            part in {"target", "__pycache__", ".git"} for part in path.parts
        ):
            continue
        if language == "java":
            if path.name != "pom.xml" and path.suffix != ".java":
                continue
        elif language == "php":
            if path.suffix != ".php":
                continue
        elif path.suffix != ".py":
            continue
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
    sdk_lock = json.loads(SDK_LOCK.read_text(encoding="utf-8"))
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
    )
    problems += require_text(java / "opps-bspay-java-sdk" / "pom.xml", "<version>3.0.40</version>")
    java_source = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core"
    problems += require_text(java_source / "config/MerConfig.java", "setProductId")
    problems += require_text(java_source / "BasePay.java", "public static volatile boolean debug = true;")
    abstract_request = java_source / "net/AbstractRequest.java"
    problems += require_text(abstract_request, '"v2/supplementary/picture"', "file == null", "httpPostNoFile", 'System.out.println("PRIVATE_KEY=" + privateKey)', 'System.out.println("request sign=" + requestSign)', 'System.out.println("request data = "')
    problems += require_ordered_text(abstract_request, "File file, String fileParam", "if (BasePay.debug)", 'System.out.println("PRIVATE_KEY=" + privateKey)', 'System.out.println("request sign=" + requestSign)', 'System.out.println("request data = "', '"v2/supplementary/picture".equals(uri)')
    problems += require_ordered_text(abstract_request, "File file, String fileParam", "requestSign = RsaUtils.sign", "if (isPage)", "RsaUtils.verify")
    problems += require_text(java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/client/BasePayClient.java", "isPage true 客户端不做验签操作", 'file, "file", merchantKey, true)')
    http_client = (
        java
        / "opps-bspay-java-sdk"
        / "src/main/java/com/huifu/bspay/sdk/opps/core/utils/HttpClientUtils.java"
    )
    problems += require_text(
        http_client,
        "MultipartEntityBuilder.create",
        "builder.addTextBody",
        "ContentType.APPLICATION_FORM_URLENCODED",
        "TrustManager[] trustAllCerts",
        "X509TrustManager",
        "HostnameVerifier",
        "return true;",
        "SSLConnectionSocketFactory(sslcontext, hostnameVerifier)",
    )
    java_request_root = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core/request"
    java_enum = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core/enums/FunctionCodeEnum.java"
    for name, enum_name in zip(java_requests, routes, strict=True):
        problems += require_text(java_request_root / f"{name}.java", f"class {name}", f"return FunctionCodeEnum.{enum_name};")
    problems += forbid_text(
        java_request_root / "V2MerchantBasicdataEntRequest.java",
        "material_card_info",
    )
    for enum_name, route in routes.items():
        problems += require_text(java_enum, enum_name, route.replace("/", "."))
    problems += forbid_text(java_enum, "V2_MERCHANT_FEE_RATE_QUERY", "v2.merchant.fee-rate.query")

    php_requests = java_requests
    problems += require_text(php / "init.php", 'define("SDK_VERSION", "php_v2.0.30")')
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
        php / "core/BsPayRequestV2.php",
        "CURLOPT_SSL_VERIFYPEER, false",
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
        "jpt-x-skill-huifu_id",
        "jpt-sdk_version",
    )
    for name, enum_name in zip(php_requests, routes, strict=True):
        problems += require_text(php / "request" / f"{name}.php", f"class {name}", f"return FunctionCodeEnum::${enum_name};")
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
    )
    problems += require_text(python / "dg_client.py", "__version__ = '2.0.24'")
    problems += require_text(python / "__init__.py", "from dg_sdk.dg_tools import DGTools")
    problems += require_text(python / "dg_tools.py", "class DGTools", "def request_post", "return request_post")
    problems += require_text(python / "core/request_tools.py", "def request_post", "files=None", "need_sign=True", "need_verfy_sign=True", "ApiRequest.post(files)")
    problems += require_text(
        python / "request/v2_supplementary_picture_request.py",
        "class V2SupplementaryPictureRequest",
        "file = {'picture':",
        "need_sign=False",
        "need_verfy_sign=False",
    )
    problems += require_text(python / "core/api_request.py", "application/json;charset=utf-8", "params.get(\"huifu_id\", \"\")", 'header["jpt-x-skill-huifu_id"] = jpt_x_skill_huifu_id', "elif method == 'post'", "json=params", "Retry(connect=3, backoff_factor=0.5)")
    for name, enum_name in zip(python_requests, routes, strict=True):
        problems += require_text(python / "request" / name, f"from dg_sdk.request.request_api_urls import {enum_name}", f"request_post({enum_name}, required_params)")
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

    # Compile/load the actual SDK code so comments or dead strings cannot satisfy
    # the evidence checks by themselves.
    problems += run_checked(
        ["mvn", "-q", "-pl", "opps-bspay-java-sdk", "-am", "-DskipTests", "compile"],
        java,
    )
    java_classes = java / "opps-bspay-java-sdk" / "target/classes"
    for request_name, enum_name in zip(java_requests, routes, strict=True):
        command = [
            "javap",
            "-classpath",
            str(java_classes),
            "-c",
            f"com.huifu.bspay.sdk.opps.core.request.{request_name}",
        ]
        try:
            result = subprocess.run(
                command,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
                timeout=30,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            problems.append(f"cannot inspect compiled Java class {request_name}: {exc}")
            continue
        if result.returncode or f"FunctionCodeEnum.{enum_name}" not in result.stdout:
            problems.append(
                f"compiled Java {request_name}.getFunctionCode does not return {enum_name}"
            )

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
    problems += require_text(matrix, "服务端 SDK 能力矩阵", "九个已有专属类的 JSON 接口", "V2MerchantBusiModifyRequest", "V2MerchantBasicdataModifyRequest", "V2MerchantBusiModifyBusistatusRequest", "V2MerchantBasicdataSmsSendRequest", "费率查询缺口", "/v2/merchant/fee-rate/query", "3.0.40", "2.0.30", "2.0.24", "无保护读取缺失键", "发送空的 `jpt-x-skill-huifu_id`", "兼容性提示", "不要求客户判断", "`DGTools.request_post`", "默认请求签名和响应验签", "`V2SupplementaryPictureRequest`", "`need_sign=False, need_verfy_sign=False`", "`BasePay.debug` 默认 `true`", "全局设置为 `false`", "`CURLFile`", "已携带 Skill 头", "关闭签名/验签", "## 调试日志硬停", "`BsPayDemo/loader.php`", "`Composer/BsPayConfig.php`", "`DEBUG=true`", "`DEBUG=false`", "`rsa_merch_private_key`", "完整请求体与完整响应", "## 传输安全硬停", "X509TrustManager", "HostnameVerifier.verify()", "CURLOPT_SSL_VERIFYPEER=false", "错证书、过期证书和错域名")
    problems += require_text(image, "multipart 文本字段", "PHP `php_v2.0.30`", "发送空的 `jpt-x-skill-huifu_id`", "SDK 兼容性提示", "不单独阻断", "不得询问客户", "DGTools.request_post", "V2SupplementaryPictureRequest", "need_sign=False, need_verfy_sign=False", "默认 `need_sign=True, need_verfy_sign=True`", "本地二进制文件模式", "Retry(connect=3)", "不得再实现业务自动重试", "`BasePay.debug` 默认为 `true`", "BasePay.debug = false;", "私钥、签名", "请求数据", "`requestDemo` 含 `sys_id`、`product_id`、`data`、`file`，不含 `sign`", "接口元数据的 `sign=true`", "isPage=true", "请求签名保留", "响应验签跳过", "CURLFile", "已携带 `jpt-x-skill-source`", "关闭请求签名和响应验签", "`hfms/1.0.0`", "`hfps/1.3.3;hfms/1.0.0`")
    problems += require_ordered_text(
        image,
        "Java 静态请求形状",
        "BasePay.debug = false;",
        '"v2/supplementary/picture"',
        '"merchantKey", "default"',
        '"isPage", true',
    )
    problems += forbid_text(image, 'data, "default", false);')
    for page in (enterprise, individual):
        problems += require_text(page, "async_return_url", "notify_url", "禁止")
        problems += forbid_text(page, 'extendInfoMap.put("notify_url"', 'data.put("notify_url"')
    problems += require_text(
        enterprise,
        'extendInfoMap.put("async_return_url", request.asyncReturnUrl());',
        "三个锁定版本均没有新增 `material_card_info` 的专属字段或 setter",
        "exact-key 扩展字段能力",
        "键必须保持 `material_card_info`",
        "整体序列化得到的 JSON 字符串",
        "不能传普通嵌套 Object",
    )
    problems += require_text(prompts, '"id": 69', '"id": 70', '"id": 71', '"id": 74', 'data, \\"default\\", true', "请求签名保留", "跳过 SDK 响应验签", "CURLFile", "async_return_url", "notify_url", "不得询问客户")
    problems += forbid_text(matrix, "`dg_sdk.request_post")
    problems += forbid_text(image, "dg_sdk.request_post")
    problems += require_text(contracts, f"来源快照核验日期：`{onboarding_source_date()}`", "企业商户进件", "个人商户进件", "商户业务开通", "图片上传", "商户详细信息查询", "申请单状态查询", "商户业务开通修改", "商户基本信息修改", "商户费率信息查询", "商户状态变更", "商户短信发送", "agreement_info.agreement_async_return_url", "reg_result_list[].business_stat", "async.agreement.agreement_info_list.con_stat", "data.wx_zl_config.apply_state", "data.ali_zl_config[].apply_status", "RECV_ORD_ID_", "file_url String(512)", "apply_status", "九个已有专属 Request 类的 JSON 接口", "公共 `AbstractRequest`", "`BasePay.debug` 默认为 `true`", "BasePay.debug = false;", "任何 SDK 请求之前", "不得在并发请求中临时切换", "`BsPayDemo/loader.php`", "`Composer/BsPayConfig.php`", "`DEBUG=false`", "`DEBUG=true`", "`rsa_merch_private_key`", "完整请求体和完整响应", "不得按叶字段名去重", "request.data.card_info.prov_id", "request.data.card_info.area_id", "不能跨接口复用长度", "hfms/1.0.0", "hfps/1.3.3;hfms/1.0.0")
    problems += require_text(credentials, "进件凭据与敏感资料边界", "RSA 私钥", "禁止写入", "Java 必须", "`BasePay.debug = false`", "PHP 必须", "`BsPay::init`", "`DEBUG=false`", "`DEBUG=true`", "Demo loader", "完整请求、响应", "`hfms/1.0.0`", "`hfps/1.3.3;hfms/1.0.0`")
    problems += require_text(headers, "默认 `skill_source`", "`hfms/1.0.0`", "`hfps/1.3.3;hfms/1.0.0`", "顺序固定为支付、进件", "英文分号且不加空格", "原样透传")
    problems += require_text(skill, "## SDK 与图片安全边界", "公共 `AbstractRequest`", "私钥、签名和请求数据", "`BasePay.debug` 默认为 `true`", "进程初始化阶段、任何请求之前", "不得并发临时切换", "保留请求签名和同步响应验签", "唯一已登记例外", "`josnArray`", "`async.business.reg_result_list[]`", "`BsPayDemo/loader.php`", "`Composer/BsPayConfig.php`", "`DEBUG=true`", "`DEBUG=false`", "`BsPay::init`", "含 RSA 私钥的 `MerConfig`", "完整请求体和完整响应", "用户要求 PHP 联调或生产可运行代码", "X509TrustManager", "HostnameVerifier", "CURLOPT_SSL_VERIFYPEER=false", "错证书、过期证书、错域名测试", "`request.data.prov_id/area_id`", "`request.data.card_info.prov_id/area_id`", "`hfms/1.0.0`", "`hfps/1.3.3;hfms/1.0.0`")
    for anchor in (
        "企业商户进件",
        "无执照个人商户进件",
        "首次业务开通，或补开银行卡、银联等仍由 `/busi/open` 承载的能力",
        "商户详细信息查询",
        "申请单状态查询",
        "微信/支付宝补开，线上业务开通，或已开通能力的参数、费率修改",
        "商户基本信息修改",
        "商户费率信息查询",
        "商户状态开通或关闭",
        "商户短信发送或验证码核实",
    ):
        problems += require_same_line(skill, anchor, "merchant-onboarding-field-contracts.md")
    problems += require_same_line(
        skill,
        "九个已有专属类的 JSON 接口 SDK",
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
