#!/usr/bin/env python3
"""Verify source-backed SDK claims for the five user-onboarding endpoints."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

from validate_merchant_onboarding_sdk_evidence import (
    require_ordered_text,
    require_text,
    resolve_sdk_layout,
    run_checked,
    source_tree_digest,
)
from validation_runtime import require_assertions_enabled


require_assertions_enabled()

REPO_ROOT = Path(__file__).resolve().parent.parent
SDK_LOCK = REPO_ROOT / "maintainer-contracts/merchant-onboarding-sdk-source-lock.json"

ROUTES = {
    "V2_USER_BASICDATA_ENT": "v2/user/basicdata/ent",
    "V2_USER_BASICDATA_INDV": "v2/user/basicdata/indv",
    "V2_USER_BUSI_OPEN": "v2/user/busi/open",
    "V2_USER_APPLY_QUERY": "v2/user/apply/query",
    "V2_USER_BASICDATA_QUERY": "v2/user/basicdata/query",
}
REQUEST_CLASSES = (
    "V2UserBasicdataEntRequest",
    "V2UserBasicdataIndvRequest",
    "V2UserBusiOpenRequest",
    "V2UserApplyQueryRequest",
    "V2UserBasicdataQueryRequest",
)
PYTHON_FILES = (
    "v2_user_basicdata_ent_request.py",
    "v2_user_basicdata_indv_request.py",
    "v2_user_busi_open_request.py",
    "v2_user_apply_query_request.py",
    "v2_user_basicdata_query_request.py",
)


def validate_source_lock(java: Path, php: Path, python: Path) -> list[str]:
    problems: list[str] = []
    lock = json.loads(SDK_LOCK.read_text(encoding="utf-8"))
    for language, component in (("java", java), ("php", php), ("python", python)):
        count, digest = source_tree_digest(component, language)
        expected = lock["components"][language]
        if count != expected["file_count"] or digest != expected["tree_sha256"]:
            problems.append(
                f"{language} SDK tree differs from lock: "
                f"files={count}/{expected['file_count']} "
                f"sha256={digest}/{expected['tree_sha256']}"
            )
    return problems


def validate_static_routes(java: Path, php: Path, python: Path) -> list[str]:
    problems: list[str] = []
    java_root = java / "opps-bspay-java-sdk/src/main/java/com/huifu/bspay/sdk/opps/core"
    java_requests = java_root / "request"
    java_enum = java_root / "enums/FunctionCodeEnum.java"
    php_enum = php / "enums/FunctionCodeEnum.php"
    python_enum = python / "request/request_api_urls.py"
    for request_class, python_file, (enum_name, route) in zip(
        REQUEST_CLASSES, PYTHON_FILES, ROUTES.items(), strict=True
    ):
        problems += require_text(
            java_requests / f"{request_class}.java",
            f"class {request_class}",
            f"return FunctionCodeEnum.{enum_name};",
        )
        problems += require_text(java_enum, enum_name, route.replace("/", "."))
        problems += require_text(
            php / "request" / f"{request_class}.php",
            f"class {request_class}",
            f"return FunctionCodeEnum::${enum_name};",
        )
        problems += require_text(php_enum, enum_name, route)
        problems += require_text(
            python / "request" / python_file,
            f"class {request_class}",
            f"request_post({enum_name}, required_params)",
        )
        problems += require_text(python_enum, enum_name, f'"/{route}"')

    business_java = java_requests / "V2UserBusiOpenRequest.java"
    problems += require_text(
        business_java,
        '@JSONField(name = "sign_user_info")',
        "private String signUserInfo;",
    )
    problems += require_ordered_text(
        java_root.parent / "client/BasePayClient.java",
        "Map<String, Object> params = ObjectUtils.objectToMap(request);",
        "params.putAll(request.getExtendInfos());",
        "return request(params, funcCode, merchantKey, isPage);",
    )
    problems += require_text(
        php / "core/BsPayClient.php",
        "array_merge($arrayData, $extendInfos)",
    )
    problems += require_text(
        python / "request/v2_user_busi_open_request.py",
        "required_params.update(extend_infos)",
    )
    return problems


def validate_runtime_probes(java: Path, php: Path, python: Path) -> list[str]:
    problems: list[str] = []
    problems += run_checked(
        ["mvn", "-q", "-pl", "opps-bspay-java-sdk", "-am", "-DskipTests", "compile"],
        java,
    )
    java_classes = java / "opps-bspay-java-sdk/target/classes"
    java_probe = """
import java.util.Map;
import com.huifu.bspay.sdk.opps.core.request.*;
import com.huifu.bspay.sdk.opps.core.utils.ObjectUtils;
public class UserOnboardingSdkProbe {
  private static void route(BaseRequest request, String expected) {
    if (!expected.equals(request.getFunctionCode().getCode())) throw new RuntimeException(expected);
  }
  public static void main(String[] args) throws Exception {
    route(new V2UserBasicdataEntRequest(), "v2.user.basicdata.ent");
    route(new V2UserBasicdataIndvRequest(), "v2.user.basicdata.indv");
    route(new V2UserBusiOpenRequest(), "v2.user.busi.open");
    route(new V2UserApplyQueryRequest(), "v2.user.apply.query");
    route(new V2UserBasicdataQueryRequest(), "v2.user.basicdata.query");
    V2UserBusiOpenRequest request = new V2UserBusiOpenRequest();
    request.setSignUserInfo("stale-string");
    request.addExtendInfo("sign_user_info", Map.of("type", "LEGAL"));
    Map<String,Object> params = ObjectUtils.objectToMap(request);
    params.putAll(request.getExtendInfos());
    if (!(params.get("sign_user_info") instanceof Map)) throw new RuntimeException("object override failed");
  }
}
"""
    with tempfile.TemporaryDirectory(prefix="huifu-user-sdk-java-") as directory:
        probe_root = Path(directory)
        source = probe_root / "UserOnboardingSdkProbe.java"
        classpath_file = probe_root / "classpath.txt"
        source.write_text(java_probe, encoding="utf-8")
        problems += run_checked(
            [
                "mvn",
                "-q",
                "-pl",
                "opps-bspay-java-sdk",
                "dependency:build-classpath",
                f"-Dmdep.outputFile={classpath_file}",
            ],
            java,
        )
        dependency_classpath = (
            classpath_file.read_text(encoding="utf-8").strip()
            if classpath_file.is_file()
            else ""
        )
        java_classpath = os.pathsep.join(
            part for part in (str(java_classes), dependency_classpath) if part
        )
        problems += run_checked(
            ["javac", "-encoding", "UTF-8", "-cp", java_classpath, str(source)],
            probe_root,
        )
        problems += run_checked(
            [
                "java",
                "-cp",
                os.pathsep.join((java_classpath, str(probe_root))),
                "UserOnboardingSdkProbe",
            ],
            probe_root,
        )

    php_script = [f'require "{(php / "init.php").as_posix()}";']
    for request_class, (enum_name, route) in zip(
        REQUEST_CLASSES, ROUTES.items(), strict=True
    ):
        php_script.extend(
            (
                f'require "{(php / "request" / f"{request_class}.php").as_posix()}";',
                rf'$r = new \BsPaySdk\request\{request_class}();',
                f'if ($r->getFunctionCode() !== "{route}") exit(3);',
            )
        )
    php_script.extend(
        (
            rf'$r = new \BsPaySdk\request\V2UserBusiOpenRequest();',
            '$r->setSignUserInfo("stale-string");',
            '$r->setExtendInfo(array("sign_user_info" => array("type" => "LEGAL")));',
            rf'$c = new \BsPaySdk\core\BsPayClient();',
            '$wire = $c->objectToArray($r)["params"];',
            'if (!is_array($wire["sign_user_info"]) || $wire["sign_user_info"]["type"] !== "LEGAL") exit(4);',
        )
    )
    problems += run_checked(["php", "-r", " ".join(php_script)])

    python_probe = r'''\
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
    spec = importlib.util.spec_from_file_location("sdk_case", root / "request" / case["file"])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    request = getattr(module, case["class"])()
    extend = {"sign_user_info": {"type": "LEGAL"}} if case["class"] == "V2UserBusiOpenRequest" else {}
    route, params = request.post(extend)
    assert route == "/" + case["route"]
    if extend:
        assert isinstance(params["sign_user_info"], dict)
'''
    cases = [
        {"file": filename, "class": request_class, "enum": enum_name, "route": route}
        for filename, request_class, (enum_name, route) in zip(
            PYTHON_FILES, REQUEST_CLASSES, ROUTES.items(), strict=True
        )
    ]
    problems += run_checked(
        [sys.executable, "-c", python_probe, str(python), json.dumps(cases)]
    )
    return problems


def validate_published_contracts() -> list[str]:
    problems: list[str] = []
    root = REPO_ROOT / "huifu-merchant-onboarding"
    problems += require_text(
        root / "references/user-onboarding-shared-server-sdk-matrix.md",
        "3.0.40",
        "2.0.30",
        "2.0.24",
        *REQUEST_CLASSES,
        "sign_user_info",
        "exact-key",
        "TLS",
        "DEBUG",
        "官方 SDK-only 传输规则",
        "不存在此前 Skill 推断的 TLS 问题",
        "五接口均使用各自官方 Request/Client",
        "HttpClient",
        "OkHttp",
        "Guzzle",
        "自实现签名/验签客户端",
        "三语言交付分别使用官方 SDK",
    )
    problems += require_text(
        root / "SKILL.md",
        "用户五个专属",
        "用户号",
        "商户号",
        "hfms/1.0.1",
        "官方 SDK-only 传输规则",
        "不存在本 Skill 曾推断的 TLS 硬停问题",
        "真实请求都使用官方 Request/Client",
    )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk-root", type=Path, default=os.environ.get("HUIFU_SDK_ROOT"))
    args = parser.parse_args()
    if args.sdk_root is None:
        parser.error("--sdk-root or HUIFU_SDK_ROOT is required")
    try:
        java, php, python = resolve_sdk_layout(args.sdk_root.resolve())
    except ValueError as exc:
        parser.error(str(exc))
    problems = []
    problems += validate_source_lock(java, php, python)
    problems += validate_static_routes(java, php, python)
    problems += validate_runtime_probes(java, php, python)
    problems += validate_published_contracts()
    if problems:
        print("User-onboarding SDK evidence validation failed:")
        print("\n".join(problems))
        return 1
    print(
        "User-onboarding SDK evidence validation passed "
        f"(java={java}, php={php}, python={python})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
