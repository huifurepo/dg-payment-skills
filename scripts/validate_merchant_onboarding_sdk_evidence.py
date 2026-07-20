#!/usr/bin/env python3
"""Verify the source-backed merchant-onboarding SDK claims without bundling the SDK."""
from __future__ import annotations

import argparse
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


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


def forbid_text_between(path: Path, start: str, end: str, *terms: str) -> list[str]:
    """Forbid terms inside a source branch delimited by stable anchors."""
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
    return [f"{path}: forbidden term in branch {start}: {term}" for term in terms if term in section]


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk-root", type=Path, default=os.environ.get("HUIFU_SDK_ROOT"))
    args = parser.parse_args()
    if args.sdk_root is None:
        parser.error("--sdk-root or HUIFU_SDK_ROOT is required")
    root = args.sdk_root.resolve()
    java = root / "bspay-java-sdk-parent-main" / "bspay-java-sdk-parent-main"
    php = root / "bspay-php-sdk-master" / "bspay-php-sdk-master" / "BsPaySdk"
    python = root / "bspay-python-sdk-feature_generator_sdk" / "dg_sdk"
    problems: list[str] = []

    routes = {
        "V2_MERCHANT_BASICDATA_ENT": "v2/merchant/basicdata/ent",
        "V2_MERCHANT_BASICDATA_INDV": "v2/merchant/basicdata/indv",
        "V2_MERCHANT_BUSI_OPEN": "v2/merchant/busi/open",
        "V2_MERCHANT_BASICDATA_QUERY": "v2/merchant/basicdata/query",
        "V2_MERCHANT_BASICDATA_STATUS_QUERY": "v2/merchant/basicdata/status/query",
    }

    java_requests = ("V2MerchantBasicdataEntRequest", "V2MerchantBasicdataIndvRequest", "V2MerchantBusiOpenRequest", "V2MerchantBasicdataQueryRequest", "V2MerchantBasicdataStatusQueryRequest")
    problems += require_text(java / "opps-bspay-java-sdk" / "pom.xml", "<version>3.0.39</version>")
    java_source = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core"
    problems += require_text(java_source / "config/MerConfig.java", "setProductId")
    problems += require_text(java_source / "BasePay.java", "public static volatile boolean debug = true;")
    abstract_request = java_source / "net/AbstractRequest.java"
    problems += require_text(abstract_request, '"v2/supplementary/picture"', "file == null", "httpPostNoFile", 'System.out.println("PRIVATE_KEY=" + privateKey)', 'System.out.println("request sign=" + requestSign)', 'System.out.println("request data = "')
    problems += require_ordered_text(abstract_request, "File file, String fileParam", "if (BasePay.debug)", 'System.out.println("PRIVATE_KEY=" + privateKey)', 'System.out.println("request sign=" + requestSign)', 'System.out.println("request data = "', '"v2/supplementary/picture".equals(uri)')
    problems += require_ordered_text(abstract_request, "File file, String fileParam", "requestSign = RsaUtils.sign", "if (isPage)", "RsaUtils.verify")
    problems += require_text(java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/client/BasePayClient.java", "isPage true 客户端不做验签操作", 'file, "file", merchantKey, true)')
    problems += require_text(java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core/utils/HttpClientUtils.java", "MultipartEntityBuilder.create", "builder.addTextBody", "ContentType.APPLICATION_FORM_URLENCODED")
    java_request_root = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core/request"
    java_enum = java / "opps-bspay-java-sdk" / "src/main/java/com/huifu/bspay/sdk/opps/core/enums/FunctionCodeEnum.java"
    for name, enum_name in zip(java_requests, routes, strict=True):
        problems += require_text(java_request_root / f"{name}.java", f"class {name}", f"return FunctionCodeEnum.{enum_name};")
    for enum_name, route in routes.items():
        problems += require_text(java_enum, enum_name, route.replace("/", "."))

    php_requests = ("V2MerchantBasicdataEntRequest", "V2MerchantBasicdataIndvRequest", "V2MerchantBusiOpenRequest", "V2MerchantBasicdataQueryRequest", "V2MerchantBasicdataStatusQueryRequest")
    problems += require_text(php / "init.php", 'define("SDK_VERSION", "php_v2.0.29")')
    problems += require_text(php / "enums/FunctionCodeEnum.php", "V2_SUPPLEMENTARY_PICTURE")
    problems += require_text(php / "core/BsPay.php", "if (empty($file))", "Content-Type:application/json", "$is_json = true", "$huifuId = $request_params['huifu_id']", "Content-Type:multipart/form-data", "$is_json = false")
    problems += require_text(php / "core/BsPayClient.php", "if (is_object($tag))", "$data['params']['needSign'] = false", "$data['params']['needVerfySign'] = false")
    problems += forbid_text_between(php / "core/BsPay.php", "Content-Type:multipart/form-data", "// 实例化 http 请求执行", "jpt-x-skill-source", "jpt-x-skill-huifu_id", "jpt-sdk_version")
    for name, enum_name in zip(php_requests, routes, strict=True):
        problems += require_text(php / "request" / f"{name}.php", f"class {name}", f"return FunctionCodeEnum::${enum_name};")
    for enum_name, route in routes.items():
        problems += require_text(php / "enums/FunctionCodeEnum.php", enum_name, route)

    python_requests = ("v2_merchant_basicdata_ent_request.py", "v2_merchant_basicdata_indv_request.py", "v2_merchant_busi_open_request.py", "v2_merchant_basicdata_query_request.py", "v2_merchant_basicdata_status_query_request.py")
    problems += require_text(python / "dg_client.py", "__version__ = '2.0.23'")
    problems += require_text(python / "__init__.py", "from dg_sdk.dg_tools import DGTools")
    problems += require_text(python / "dg_tools.py", "class DGTools", "def request_post", "return request_post")
    problems += require_text(python / "core/request_tools.py", "def request_post", "files=None", "ApiRequest.post(files)")
    problems += require_text(python / "core/api_request.py", "application/json;charset=utf-8", "params.get(\"huifu_id\", \"\")", 'header["jpt-x-skill-huifu_id"] = jpt_x_skill_huifu_id', "elif method == 'post'", "json=params", "Retry(connect=3, backoff_factor=0.5)")
    for name, enum_name in zip(python_requests, routes, strict=True):
        problems += require_text(python / "request" / name, f"from dg_sdk.request.request_api_urls import {enum_name}", f"request_post({enum_name}, required_params)")
    for enum_name, route in routes.items():
        problems += require_text(python / "request/request_api_urls.py", enum_name, f'"/{route}"')

    matrix = REPO_ROOT / "huifu-pay-integration/references/shared-server-sdk-matrix.md"
    image = REPO_ROOT / "huifu-pay-integration/references/merchant-onboarding-image-upload.md"
    enterprise = REPO_ROOT / "huifu-pay-integration/references/merchant-onboarding-enterprise.md"
    individual = REPO_ROOT / "huifu-pay-integration/references/merchant-onboarding-individual.md"
    contracts = REPO_ROOT / "huifu-pay-integration/references/merchant-onboarding-field-contracts.md"
    skill = REPO_ROOT / "huifu-pay-integration/SKILL.md"
    prompts = REPO_ROOT / "scripts/huifu-payment-test-prompts.json"
    problems += require_text(matrix, "商户进件 SDK 证据", "3.0.39", "2.0.29", "2.0.23", "无保护读取缺失键", "发送空的 `jpt-x-skill-huifu_id`", "SDK 兼容性提示", "不单独阻断", "不让客户判断", "dg_sdk.DGTools.request_post", "`BasePay.debug` 默认 `true`", "全局设为 `false`", "CURLFile", "缺少 `jpt-x-skill-source`", "关闭请求签名和响应验签")
    problems += require_text(image, "multipart 文本字段", "PHP `php_v2.0.29`", "发送空的 `jpt-x-skill-huifu_id`", "SDK 兼容性提示", "不单独阻断", "不得询问客户", "DGTools.request_post", "本地二进制文件模式", "Retry(connect=3)", "不得再实现业务自动重试", "`BasePay.debug` 默认为 `true`", "BasePay.debug = false;", "私钥、签名", "请求数据", "`requestDemo` 含 `sys_id`、`product_id`、`data`、`file`，不含 `sign`", "接口元数据的 `sign=true`", "isPage=true", "请求签名保留", "响应验签跳过", "CURLFile", "缺少 `jpt-x-skill-source`", "关闭请求签名和响应验签")
    problems += require_ordered_text(image, "Java 受控片段", "BasePay.debug = false;", "BasePayRequest.requestBasePay(", 'data, "default", true);')
    problems += forbid_text(image, 'data, "default", false);')
    for page in (enterprise, individual):
        problems += require_text(page, "async_return_url", "notify_url", "禁止")
        problems += forbid_text(page, 'extendInfoMap.put("notify_url"', 'data.put("notify_url"')
    problems += require_text(enterprise, 'extendInfoMap.put("async_return_url", request.asyncReturnUrl());')
    problems += require_text(prompts, '"id": 69', '"id": 70', '"id": 71', '"id": 74', 'data, \\"default\\", true', "请求签名保留", "跳过 SDK 响应验签", "CURLFile", "async_return_url", "notify_url", "不得询问客户")
    problems += forbid_text(matrix, "`dg_sdk.request_post")
    problems += forbid_text(image, "dg_sdk.request_post")
    problems += require_text(contracts, "核验日期：`2026-07-17`", "企业商户进件", "个人商户进件", "商户业务开通", "图片上传", "商户详细信息查询", "申请单状态查询", "agreement_info.agreement_async_return_url", "reg_result_list[].business_stat", "data.wx_zl_config.apply_state", "data.ali_zl_config[].apply_status", "RECV_ORD_ID_", "file_url String(512)", "apply_status", "五个 JSON 接口和图片 `file_url` 模式", "公共 `AbstractRequest`", "`BasePay.debug` 默认为 `true`", "BasePay.debug = false;", "任何 SDK 请求之前", "不得在并发请求中临时切换")
    problems += require_text(skill, "## SDK / 模板规则", "com.huifu.bspay.sdk.opps.core.BasePay", "公共 `AbstractRequest` 会对所有 URI 打印私钥、签名和请求数据", "BasePay.debug = false;", "进程初始化阶段、任何 SDK 请求之前", "不得在并发请求中临时切换", "不关闭请求签名或响应验签")
    for anchor in (
        "企业/个体商户基础信息进件",
        "无执照个人商户基础信息进件",
        "商户业务开通 / 补开 / 渠道结果",
        "商户详细信息核对",
        "商户申请单审核或渠道状态查询",
    ):
        problems += require_same_line(skill, anchor, "merchant-onboarding-field-contracts.md")
    problems += require_same_line(
        skill,
        "商户进件五个 JSON 接口的 Java 日志安全初始化 / Request 类盘点",
        "merchant-onboarding-field-contracts.md",
        "shared-server-sdk-matrix.md",
        "不逐份加载五个原子接口页",
        "回答必须说明公共 `AbstractRequest`、`BasePay.debug` 默认 `true`、统一关闭时点，以及关闭调试不影响签名/验签",
    )
    if problems:
        print("Merchant-onboarding SDK evidence validation failed:")
        print("\n".join(problems))
        return 1
    print("Merchant-onboarding SDK evidence validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
