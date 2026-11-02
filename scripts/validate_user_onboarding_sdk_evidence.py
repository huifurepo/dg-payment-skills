#!/usr/bin/env python3
"""Verify source-backed SDK claims for the user-onboarding endpoints."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

from skill_validation_config import sdk_version
from validate_merchant_onboarding_sdk_evidence import (
    SDK_LOCK,
    copy_java_sources,
    require_ordered_text,
    require_text,
    resolve_sdk_layout,
    run_checked,
    source_tree_digest,
    sdk_history_errors,
)
from validation_runtime import require_assertions_enabled


require_assertions_enabled()

REPO_ROOT = Path(__file__).resolve().parent.parent

ROUTES = {
    "V2_USER_BASICDATA_ENT": "v2/user/basicdata/ent",
    "V2_USER_BASICDATA_INDV": "v2/user/basicdata/indv",
    "V2_USER_BUSI_OPEN": "v2/user/busi/open",
    "V2_USER_APPLY_QUERY": "v2/user/apply/query",
    "V2_USER_BASICDATA_QUERY": "v2/user/basicdata/query",
    "V2_USER_BASICDATA_ENT_MODIFY": "v2/user/basicdata/ent/modify",
    "V2_USER_BASICDATA_INDV_MODIFY": "v2/user/basicdata/indv/modify",
    "V2_USER_BUSI_MODIFY": "v2/user/busi/modify",
    "V2_USER_LIST_QUERY": "v2/user/list/query",
}
REQUEST_CLASSES = (
    "V2UserBasicdataEntRequest",
    "V2UserBasicdataIndvRequest",
    "V2UserBusiOpenRequest",
    "V2UserApplyQueryRequest",
    "V2UserBasicdataQueryRequest",
    "V2UserBasicdataEntModifyRequest",
    "V2UserBasicdataIndvModifyRequest",
    "V2UserBusiModifyRequest",
    "V2UserListQueryRequest",
)
PYTHON_FILES = (
    "v2_user_basicdata_ent_request.py",
    "v2_user_basicdata_indv_request.py",
    "v2_user_busi_open_request.py",
    "v2_user_apply_query_request.py",
    "v2_user_basicdata_query_request.py",
    "v2_user_basicdata_ent_modify_request.py",
    "v2_user_basicdata_indv_modify_request.py",
    "v2_user_busi_modify_request.py",
    "v2_user_list_query_request.py",
)


def validate_source_lock(java: Path, php: Path, python: Path) -> list[str]:
    problems: list[str] = []
    lock = json.loads(SDK_LOCK.read_text(encoding="utf-8"))
    problems += sdk_history_errors(lock)
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
    enterprise_modify_java = (
        java_requests / "V2UserBasicdataEntModifyRequest.java"
    ).read_text(encoding="utf-8")
    declared = set(re.findall(r'@JSONField\(name = "([^"]+)"\)', enterprise_modify_java))
    expected_declared = {
        "req_date",
        "req_seq_id",
        "huifu_id",
        "legal_cert_nationality",
    }
    if declared != expected_declared:
        problems.append(
            "enterprise modify Java declared-field set differs: "
            f"{sorted(declared)} != {sorted(expected_declared)}"
        )
    enterprise_modify_php_path = php / "request/V2UserBasicdataEntModifyRequest.php"
    problems += require_text(
        enterprise_modify_php_path,
        "private $reqDate;",
        "private $reqSeqId;",
        "private $huifuId;",
        "private $legalCertNationality;",
    )
    enterprise_modify_php = enterprise_modify_php_path.read_text(encoding="utf-8")
    php_declared = set(re.findall(r"^\s+private \$(\w+);", enterprise_modify_php, re.M))
    expected_php_declared = {
        "reqDate",
        "reqSeqId",
        "huifuId",
        "legalCertNationality",
    }
    if php_declared != expected_php_declared:
        problems.append(
            "enterprise modify PHP declared-field set differs: "
            f"{sorted(php_declared)} != {sorted(expected_php_declared)}"
        )
    enterprise_modify_python_path = (
        python / "request/v2_user_basicdata_ent_modify_request.py"
    )
    problems += require_text(
        enterprise_modify_python_path,
        '"legal_cert_nationality":self.legal_cert_nationality',
        "required_params.update(extend_infos)",
    )
    enterprise_modify_python = enterprise_modify_python_path.read_text(encoding="utf-8")
    python_declared = set(
        re.findall(r'^    ([a-z][a-z0-9_]*) = ""$', enterprise_modify_python, re.M)
    )
    expected_wire_fields = {
        "req_date",
        "req_seq_id",
        "huifu_id",
        "legal_cert_nationality",
    }
    required_block = re.search(
        r"required_params = \{(?P<body>.*?)\n        \}",
        enterprise_modify_python,
        re.S,
    )
    python_required = (
        set(re.findall(r'"([a-z][a-z0-9_]*)"\s*:', required_block.group("body")))
        if required_block
        else set()
    )
    if python_declared != expected_wire_fields or python_required != expected_wire_fields:
        problems.append(
            "enterprise modify Python declared/required field sets differ: "
            f"class={sorted(python_declared)}, required={sorted(python_required)}, "
            f"expected={sorted(expected_wire_fields)}"
        )
    individual_java_path = java_requests / "V2UserBasicdataIndvModifyRequest.java"
    individual_java = individual_java_path.read_text(encoding="utf-8")
    individual_java_fields = set(
        re.findall(r'@JSONField\(name = "([^"]+)"\)', individual_java)
    )
    individual_wire_fields = {"req_seq_id", "req_date", "huifu_id"}
    if individual_java_fields != individual_wire_fields:
        problems.append(
            "individual modify Java declared-field set differs: "
            f"{sorted(individual_java_fields)} != {sorted(individual_wire_fields)}"
        )
    individual_php = (
        php / "request/V2UserBasicdataIndvModifyRequest.php"
    ).read_text(encoding="utf-8")
    individual_php_fields = set(
        re.findall(r"^\s+private \$(\w+);", individual_php, re.M)
    )
    if individual_php_fields != {"reqSeqId", "reqDate", "huifuId"}:
        problems.append(
            "individual modify PHP declared-field set differs: "
            f"{sorted(individual_php_fields)}"
        )
    individual_python = (
        python / "request/v2_user_basicdata_indv_modify_request.py"
    ).read_text(encoding="utf-8")
    individual_python_fields = set(
        re.findall(r'^    ([a-z][a-z0-9_]*) = ""$', individual_python, re.M)
    )
    individual_required_block = re.search(
        r"required_params = \{(?P<body>.*?)\n        \}", individual_python, re.S
    )
    individual_python_required = (
        set(
            re.findall(
                r'"([a-z][a-z0-9_]*)"\s*:',
                individual_required_block.group("body"),
            )
        )
        if individual_required_block
        else set()
    )
    if (
        individual_python_fields != individual_wire_fields
        or individual_python_required != individual_wire_fields
    ):
        problems.append(
            "individual modify Python declared/required field sets differ: "
            f"class={sorted(individual_python_fields)}, "
            f"required={sorted(individual_python_required)}"
        )
    business_modify_wire = {"req_seq_id", "req_date", "huifu_id", "sign_user_info"}
    business_modify_java = (
        java_requests / "V2UserBusiModifyRequest.java"
    ).read_text(encoding="utf-8")
    if set(re.findall(r'@JSONField\(name = "([^"]+)"\)', business_modify_java)) != business_modify_wire:
        problems.append("business modify Java declared-field set differs")
    for token in ("private String signUserInfo;", "setSignUserInfo(String signUserInfo)"):
        if token not in business_modify_java:
            problems.append(f"business modify Java sign_user_info type differs: missing {token}")
    business_modify_php = (
        php / "request/V2UserBusiModifyRequest.php"
    ).read_text(encoding="utf-8")
    if set(re.findall(r"^\s+private \$(\w+);", business_modify_php, re.M)) != {
        "reqSeqId", "reqDate", "huifuId", "signUserInfo"
    }:
        problems.append("business modify PHP declared-field set differs")
    if "setSignUserInfo($signUserInfo)" not in business_modify_php:
        problems.append("business modify PHP sign_user_info setter is no longer untyped")
    business_modify_python = (
        python / "request/v2_user_busi_modify_request.py"
    ).read_text(encoding="utf-8")
    business_modify_python_fields = set(
        re.findall(r'^    ([a-z][a-z0-9_]*) = ""$', business_modify_python, re.M)
    )
    business_modify_required = re.search(
        r"required_params = \{(?P<body>.*?)\n        \}", business_modify_python, re.S
    )
    business_modify_required_fields = (
        set(re.findall(r'"([a-z][a-z0-9_]*)"\s*:', business_modify_required.group("body")))
        if business_modify_required else set()
    )
    if business_modify_python_fields != business_modify_wire or business_modify_required_fields != business_modify_wire:
        problems.append("business modify Python declared/required field sets differ")
    list_query_wire = {"legal_cert_no", "req_date", "req_seq_id"}
    list_query_java = (
        java_requests / "V2UserListQueryRequest.java"
    ).read_text(encoding="utf-8")
    if set(re.findall(r'@JSONField\(name = "([^"]+)"\)', list_query_java)) != list_query_wire:
        problems.append("user list-query Java declared-field set differs")
    list_query_php = (
        php / "request/V2UserListQueryRequest.php"
    ).read_text(encoding="utf-8")
    if set(re.findall(r"^\s+private \$(\w+);", list_query_php, re.M)) != {
        "legalCertNo", "reqDate", "reqSeqId"
    }:
        problems.append("user list-query PHP declared-field set differs")
    list_query_python = (
        python / "request/v2_user_list_query_request.py"
    ).read_text(encoding="utf-8")
    list_query_python_fields = set(
        re.findall(r'^    ([a-z][a-z0-9_]*) = ""$', list_query_python, re.M)
    )
    list_query_required = re.search(
        r"required_params = \{(?P<body>.*?)\n        \}", list_query_python, re.S
    )
    list_query_required_fields = (
        set(re.findall(r'"([a-z][a-z0-9_]*)"\s*:', list_query_required.group("body")))
        if list_query_required else set()
    )
    if list_query_python_fields != list_query_wire or list_query_required_fields != list_query_wire:
        problems.append("user list-query Python declared/required field sets differ")
    return problems


def validate_runtime_probes(java: Path, php: Path, python: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="huifu-user-sdk-copy-") as directory:
        isolated = copy_java_sources(java, Path(directory) / "sdk")
        return _validate_runtime_probes(isolated, php, python)


def _validate_runtime_probes(java: Path, php: Path, python: Path) -> list[str]:
    problems: list[str] = []
    problems += run_checked(
        ["mvn", "-q", "-pl", "opps-bspay-java-sdk", "-am", "-DskipTests", "compile"],
        java,
    )
    java_classes = java / "opps-bspay-java-sdk/target/classes"
    java_probe = r"""
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
    route(new V2UserBasicdataEntModifyRequest(), "v2.user.basicdata.ent.modify");
    route(new V2UserBasicdataIndvModifyRequest(), "v2.user.basicdata.indv.modify");
    route(new V2UserBusiModifyRequest(), "v2.user.busi.modify");
    route(new V2UserListQueryRequest(), "v2.user.list.query");
    V2UserBusiOpenRequest request = new V2UserBusiOpenRequest();
    request.setSignUserInfo("{\"type\":\"LEGAL\"}");
    Map<String,Object> params = ObjectUtils.objectToMap(request);
    params.putAll(request.getExtendInfos());
    if (!"{\"type\":\"LEGAL\"}".equals(params.get("sign_user_info"))) throw new RuntimeException("String(JSON) serialization changed");
    V2UserBasicdataEntModifyRequest modify = new V2UserBasicdataEntModifyRequest();
    modify.setReqSeqId("original");
    modify.addExtendInfo("req_seq_id", "overridden");
    modify.addExtendInfo("reg_name", "updated-name");
    Map<String,Object> modifyParams = ObjectUtils.objectToMap(modify);
    modifyParams.putAll(modify.getExtendInfos());
    if (!"overridden".equals(modifyParams.get("req_seq_id"))) throw new RuntimeException("locator override behavior changed");
    if (!"updated-name".equals(modifyParams.get("reg_name"))) throw new RuntimeException("optional extension missing");
    V2UserBasicdataIndvModifyRequest indvModify = new V2UserBasicdataIndvModifyRequest();
    indvModify.setReqSeqId("original");
    indvModify.addExtendInfo("req_seq_id", "overridden");
    indvModify.addExtendInfo("mobile_no", "masked-probe");
    Map<String,Object> indvParams = ObjectUtils.objectToMap(indvModify);
    indvParams.putAll(indvModify.getExtendInfos());
    if (!"overridden".equals(indvParams.get("req_seq_id"))) throw new RuntimeException("individual locator override behavior changed");
    if (!"masked-probe".equals(indvParams.get("mobile_no"))) throw new RuntimeException("individual optional extension missing");
    V2UserBusiModifyRequest busiModify = new V2UserBusiModifyRequest();
    busiModify.setSignUserInfo("{\"type\":\"LEGAL\"}");
    Map<String,Object> busiModifyParams = ObjectUtils.objectToMap(busiModify);
    busiModifyParams.putAll(busiModify.getExtendInfos());
    if (!"{\"type\":\"LEGAL\"}".equals(busiModifyParams.get("sign_user_info"))) throw new RuntimeException("business modify String(JSON) serialization changed");
    V2UserListQueryRequest listQuery = new V2UserListQueryRequest();
    listQuery.setReqSeqId("original");
    listQuery.addExtendInfo("req_seq_id", "overridden");
    listQuery.addExtendInfo("upper_huifu_id", "6666000123120000");
    Map<String,Object> listQueryParams = ObjectUtils.objectToMap(listQuery);
    listQueryParams.putAll(listQuery.getExtendInfos());
    if (!"overridden".equals(listQueryParams.get("req_seq_id"))) throw new RuntimeException("list-query locator override behavior changed");
    if (!"6666000123120000".equals(listQueryParams.get("upper_huifu_id"))) throw new RuntimeException("list-query optional extension missing");
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
            '$r->setSignUserInfo(\'{"type":"LEGAL"}\');',
            rf'$c = new \BsPaySdk\core\BsPayClient();',
            '$wire = $c->objectToArray($r)["params"];',
            'if ($wire["sign_user_info"] !== \'{"type":"LEGAL"}\') exit(4);',
            rf'$r = new \BsPaySdk\request\V2UserBasicdataEntModifyRequest();',
            '$r->setReqSeqId("original");',
            '$r->setExtendInfo(array("req_seq_id" => "overridden", "reg_name" => "updated-name"));',
            '$wire = $c->objectToArray($r)["params"];',
            'if ($wire["req_seq_id"] !== "overridden" || $wire["reg_name"] !== "updated-name") exit(5);',
            rf'$r = new \BsPaySdk\request\V2UserBasicdataIndvModifyRequest();',
            '$r->setReqSeqId("original");',
            '$r->setExtendInfo(array("req_seq_id" => "overridden", "mobile_no" => "masked-probe"));',
            '$wire = $c->objectToArray($r)["params"];',
            'if ($wire["req_seq_id"] !== "overridden" || $wire["mobile_no"] !== "masked-probe") exit(6);',
            rf'$r = new \BsPaySdk\request\V2UserBusiModifyRequest();',
            '$r->setSignUserInfo(\'{"type":"LEGAL"}\');',
            '$wire = $c->objectToArray($r)["params"];',
            'if ($wire["sign_user_info"] !== \'{"type":"LEGAL"}\') exit(7);',
            rf'$r = new \BsPaySdk\request\V2UserListQueryRequest();',
            '$r->setReqSeqId("original");',
            '$r->setExtendInfo(array("req_seq_id" => "overridden", "upper_huifu_id" => "6666000123120000"));',
            '$wire = $c->objectToArray($r)["params"];',
            'if ($wire["req_seq_id"] !== "overridden" || $wire["upper_huifu_id"] !== "6666000123120000") exit(8);',
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
    if case["class"] == "V2UserBusiOpenRequest":
        request.sign_user_info = '{"type":"LEGAL"}'
        extend = {}
    elif case["class"] == "V2UserBusiModifyRequest":
        request.sign_user_info = '{"type":"LEGAL"}'
        extend = {}
    elif case["class"] == "V2UserBasicdataEntModifyRequest":
        request.req_seq_id = "original"
        extend = {"req_seq_id": "overridden", "reg_name": "updated-name"}
    elif case["class"] == "V2UserBasicdataIndvModifyRequest":
        request.req_seq_id = "original"
        extend = {"req_seq_id": "overridden", "mobile_no": "masked-probe"}
    elif case["class"] == "V2UserListQueryRequest":
        request.req_seq_id = "original"
        extend = {"req_seq_id": "overridden", "upper_huifu_id": "6666000123120000"}
    else:
        extend = {}
    route, params = request.post(extend)
    assert route == "/" + case["route"]
    if case["class"] == "V2UserBusiModifyRequest":
        assert params["sign_user_info"] == '{"type":"LEGAL"}'
    if extend:
        assert params["req_seq_id"] == "overridden"
        if case["class"] == "V2UserBasicdataEntModifyRequest":
            assert params["reg_name"] == "updated-name"
        elif case["class"] == "V2UserListQueryRequest":
            assert params["upper_huifu_id"] == "6666000123120000"
        else:
            assert params["mobile_no"] == "masked-probe"
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
        "3.0.41",
        "2.0.31",
        sdk_version("python"),
        *REQUEST_CLASSES,
        "sign_user_info",
        "exact-key",
        "当前官网类型为 String",
        "传一层合法 JSON Object 字符串",
        "三语言均以运行探针锁定只序列化一次",
        "TLS",
        "DEBUG",
        "官方 SDK-only 传输规则",
        "CURLOPT_SSL_VERIFYPEER=false",
        "九接口均使用各自官方 Request/Client",
        "HttpClient",
        "OkHttp",
        "Guzzle",
        "自实现签名/验签客户端",
        "三语言交付分别使用官方 SDK",
    )
    problems += require_text(
        root / "SKILL.md",
        "九个用户接口 SDK",
        "用户号",
        "商户号",
        "hfms/1.1.0",
        "references/user-onboarding-shared-server-sdk-matrix.md",
        "references/user-onboarding-platform-contracts.md",
        "TLS",
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
