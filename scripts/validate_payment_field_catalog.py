#!/usr/bin/env python3
"""Independently compare the payment field catalog with all locked API tables."""

from __future__ import annotations

import json
from pathlib import Path

from validate_merchant_onboarding_source_contract import (
    flatten,
    source_tables,
    split_catalog_row,
)
from validation_runtime import require_assertions_enabled
from skill_validation_config import PAYMENT_SOURCE_LOCK, payment_source_dir


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
LOCK = PAYMENT_SOURCE_LOCK
CATALOG = ROOT / "huifu-pay-integration/references/payment-complete-field-catalog.md"
EXPECTED_TOTAL = 3096
COMMON_RETURN_CODES_URL = (
    "https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md"
)
ASYNC_INTRO_URL = (
    "https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md"
)
AGGREGATION_CREATE_URL = (
    "https://paas.huifu.com/partners/lightning/api/jhzfxd.md"
)

# Deliberately independent from the generator. A wrong root-table order or prefix
# must not make generation and validation agree on the same bad data surface.
VALIDATION_SURFACES: dict[str, tuple[tuple[str, str], ...]] = {
    "aggregation-create": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("正扫异步信封", "async.forward"),
        ("正扫异步 resp_data", "async.forward.resp_data"),
        ("正扫解冻异步 data", "async.forward.unfreeze"),
        ("反扫异步信封", "async.reverse"),
        ("反扫异步 resp_data", "async.reverse.resp_data"),
    ),
    "aggregation-query": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "aggregation-close": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "aggregation-close-query": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "aggregation-refund": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("退款异步载荷（官网未标外层字段名）", "async.unconfirmed_payload"),
    ),
    "aggregation-refund-query": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "reconciliation-v2": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "hosting-h5": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("支付异步 resp_data", "async.resp_data"),
    ),
    "hosting-alipay-mini": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("支付异步 resp_data", "async.resp_data"),
    ),
    "hosting-wechat-mini": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("支付异步 resp_data", "async.resp_data"),
        ("拆单支付异步 resp_data", "async.split.resp_data"),
    ),
    "hosting-douyin": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("支付异步 resp_data", "async.resp_data"),
    ),
    "hosting-query": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
    ),
    "hosting-refund": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("退款异步 data", "async.data"),
    ),
    "hosting-refund-query": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
    ),
    "hosting-close": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("关单异步 resp_data", "async.resp_data"),
    ),
    "hosting-splitpay-query": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
    ),
    "split-detail-query": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
}

VALIDATION_SURFACES.update({
    "balance-pay": (("请求信封", "request"), ("同步响应信封", "response"), ("请求 data", "request.data"), ("同步响应 data", "response.data"), ("支付异步信封", "async"), ("支付异步 resp_data", "async.resp_data")),
    "balance-pay-query": (("请求信封", "request"), ("同步响应信封", "response"), ("请求 data", "request.data"), ("同步响应 data", "response.data")),
    "balance-refund": (("请求信封", "request"), ("同步响应信封", "response"), ("请求 data", "request.data"), ("同步响应 data", "response.data")),
    "balance-refund-query": (("请求信封", "request"), ("同步响应信封", "response"), ("请求 data", "request.data"), ("同步响应 data", "response.data")),
    "fee-calc": (("请求信封", "request"), ("同步响应信封", "response"), ("请求 data", "request.data"), ("同步响应 data", "response.data")),
    "pay-relation": (("请求信封", "request"), ("同步响应信封", "response"), ("请求 data", "request.data"), ("同步响应 data", "response.data")),
    "balance-sms": (("请求信封", "request"), ("同步响应信封", "response"), ("请求 data", "request.data"), ("同步响应 data", "response.data")),
})


DISPLAY_NOTE = "方便文档展示"
AGGREGATION_QUERY_METHOD_GROUP = "response.data.method_expand"
STRING_ENCODED_SURFACES = {
    ("aggregation-create", "async.forward.resp_data"),
    ("aggregation-create", "async.reverse.resp_data"),
    ("hosting-h5", "async.resp_data"),
    ("hosting-alipay-mini", "async.resp_data"),
    ("hosting-wechat-mini", "async.resp_data"),
    ("hosting-wechat-mini", "async.split.resp_data"),
    ("hosting-close", "async.resp_data"),
}
NAMED_BUT_ENCODING_UNKNOWN_SURFACES = {("hosting-refund", "async.data"), ("balance-pay", "async.resp_data"), ("hosting-douyin", "async.resp_data"), ("delay-confirm", "async.resp_data")}
OUTER_NAME_UNKNOWN_SURFACES = {
    ("aggregation-refund", "async.unconfirmed_payload"),
}
SOURCE_CONFIRMED_STRING_PATHS = {
    ("aggregation-create", "request.data.terminal_device_data"),
}


def expected_description(
    description: str,
    source_url: str,
    source_key: str,
    path: str,
) -> str:
    """Independently model the two owner-confirmed broken-anchor mappings."""
    business_suffix = "（官网相对地址原文：`#业务返回码`）"
    broken_marker = "（官网原始锚点在当前快照无同名标题，`[需要人工确认]`）"
    if business_suffix in description:
        description = description.replace(
            business_suffix + broken_marker,
            business_suffix,
        )
        description = description.replace(
            business_suffix,
            business_suffix
            + f"（公共返回码全集：[返回码]({COMMON_RETURN_CODES_URL})；"
            "接口页专属码与公共码需合并排查）",
        )
    notify_suffix = "（官网相对地址原文：`#异步返回参数`）"
    if source_url == AGGREGATION_CREATE_URL and notify_suffix in description:
        description = description.replace(
            notify_suffix + broken_marker,
            notify_suffix,
        )
        description = description.replace(
            notify_suffix,
            notify_suffix
            + "（已确认同时指向"
            + f"[聚合正扫异步返回参数]({AGGREGATION_CREATE_URL}#聚合正扫异步返回参数)"
            + "和"
            + f"[聚合反扫异步返回参数]({AGGREGATION_CREATE_URL}#聚合反扫异步返回参数)"
            + "两套通知参数；通用传输、验签、ACK、重试与幂等规则见"
            + f"[异步消息简介]({ASYNC_INTRO_URL})）",
        )
    if source_key == "aggregation-query" and path == "response.data.trade_type":
        description += (
            "；[接入方确认勘误] 官网说明中第二个 `A_NATIVE: 支付宝付款码` "
            "应为 `A_MICROPAY: 支付宝付款码`；当前成功示例已使用正确值 `A_MICROPAY`"
        )
    return description


def expected_normalized_path(path: str, display_paths: set[str]) -> str | None:
    parts = path.split(".")
    for display_path in sorted(display_paths, key=lambda item: item.count(".")):
        display_parts = display_path.split(".")
        if parts[: len(display_parts)] != display_parts:
            continue
        if len(parts) == len(display_parts):
            return None
        del parts[len(display_parts) - 1]
    return ".".join(parts)


def expected_transport(
    path: str,
    flattened: list[tuple[str, object]],
    display_paths: set[str],
    source_key: str,
    surface_prefix: str,
) -> tuple[str, str]:
    actual = expected_normalized_path(path, display_paths)
    if actual is None:
        return (
            "—（官网展示分组，不存在该 wire key）",
            "—（官网展示分组，不参与解码）",
        )
    surface_key = (source_key, surface_prefix)
    if surface_key in OUTER_NAME_UNKNOWN_SURFACES:
        return (
            "—（官网未标异步外层字段名）",
            "—（[需要官方确认]：异步外层字段名和编码）",
        )
    if surface_key in NAMED_BUT_ENCODING_UNKNOWN_SURFACES:
        return (
            surface_prefix,
            f"—（[需要官方确认]：外层 {surface_prefix.rsplit('.', 1)[-1]} 的 JSON/String(JSON) 编码）",
        )
    if source_key == "pay-relation" and (actual == "response.data.pay_relations" or actual.startswith("response.data.pay_relations.")):
        return ("response.data.pay_relations", "—（[需要官方确认]：正式说明 jsonArry 的数组编码）")
    if source_key == "split-detail-query" and (
        actual == "response.data.split_trans_responses[]"
        or actual.startswith("response.data.split_trans_responses[].")
    ):
        decoded = "$[]" if actual == "response.data.split_trans_responses[]" else "$[]" + actual.split("[]", 1)[1]
        return (
            "response.data.split_trans_responses",
            f"{decoded}（String(JSON Array) 解码结果）",
        )

    containers: dict[str, bool] = {}
    if surface_key in STRING_ENCODED_SURFACES:
        containers[surface_prefix] = True
    for candidate_path, candidate_field in flattened:
        if candidate_path in display_paths:
            continue
        description = candidate_field.description.lower()
        if candidate_field.kind.lower() != "string":
            continue
        has_descendants = any(
            other_path.startswith(candidate_path + ".")
            for other_path, _other_field in flattened
        )
        if "json" not in description and not has_descendants:
            continue
        candidate = expected_normalized_path(candidate_path, display_paths)
        if candidate and (actual == candidate or actual.startswith(candidate + ".")):
            containers[candidate] = (
                "json" in description
                or (source_key, candidate) in SOURCE_CONFIRMED_STRING_PATHS
            )
    if not containers:
        return actual, "—（直接 JSON 路径）"
    ordered = sorted(containers, key=lambda item: item.count("."))
    container = ordered[0]
    wire = container[:-2] if container.endswith("[]") else container
    if not containers[container]:
        return wire, "—（[需要官方确认]：String 子表编码）"
    if actual == container:
        kind = "String(JSON Array)" if container.endswith("[]") else "String(JSON)"
        return wire, f"—（{kind} 容器）"
    decoded = lambda parent, child: (
        ("$[]." if parent.endswith("[]") else "$.")
        + child[len(parent) + 1 :]
    )
    inner = [item for item in ordered[1:] if actual == item or actual.startswith(item + ".")]
    if not inner:
        return wire, decoded(container, actual)
    nested = inner[-1]
    nested_key = nested.removesuffix("[]")
    nested_path = decoded(container, nested_key)
    if not containers[nested]:
        return wire, nested_path + " => [需要官方确认]：String 子表编码"
    if actual == nested:
        kind = "String(JSON Array)" if nested.endswith("[]") else "String(JSON)"
        return wire, nested_path + f"（{kind} 容器）"
    return (
        wire,
        nested_path + " => JSON decode => " + decoded(nested, actual),
    )


def expected_status(field: object) -> str:
    unknown: list[str] = []
    if field.kind == "—":
        unknown.append("类型")
    if field.length == "—" and field.kind.lower() not in {"json", "object", "array"}:
        unknown.append("长度")
    if field.required == "—":
        unknown.append("必填")
    if unknown:
        return "[需要官方确认]：" + "/".join(unknown)
    if field.length == "—":
        return "N/A：结构字段长度"
    return "已确认"


def expected_records() -> dict[
    tuple[str, str, str], tuple[str, str, str, str, str, str]
]:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    source_dir = payment_source_dir()
    records: dict[tuple[str, str, str], tuple[str, str, str, str]] = {}
    for source in lock["sources"]:
        key = source["key"]
        if key not in VALIDATION_SURFACES:
            continue
        roots, nested = source_tables(
            (source_dir / source["filename"]).read_text(encoding="utf-8-sig"),
            source["url"],
        )
        surfaces = VALIDATION_SURFACES[key]
        assert len(roots) == len(surfaces), (key, len(roots), len(surfaces))
        used: set[str] = set()
        for (surface, prefix), fields in zip(surfaces, roots, strict=True):
            flattened = list(flatten(fields, nested, prefix, used))
            if key == "split-detail-query" and prefix == "response.data":
                split_parent = "response.data.split_trans_responses"
                flattened = [
                    (
                        split_parent + "[]" + path[len(split_parent) :]
                        if path == split_parent or path.startswith(split_parent + ".")
                        else path,
                        field,
                    )
                    for path, field in flattened
                ]
            display_paths = {
                path for path, field in flattened if DISPLAY_NOTE in field.description
            }
            if key == "aggregation-query" and prefix == "response.data":
                display_paths.update(
                    path
                    for path, _field in flattened
                    if path.rsplit(".", 1)[0] == AGGREGATION_QUERY_METHOD_GROUP
                )
            transport_fields = [(path, field) for path, field in flattened]
            for path, field in flattened:
                identity = (source["title"], surface, path)
                assert identity not in records, f"duplicate source identity: {identity}"
                wire, decoded = expected_transport(
                    path,
                    transport_fields,
                    display_paths,
                    key,
                    prefix,
                )
                records[identity] = (
                    wire,
                    decoded,
                    field.kind,
                    field.length,
                    field.required,
                    expected_status(field),
                    expected_description(
                        field.description,
                        source["url"],
                        key,
                        path,
                    ),
                )
        assert used == set(nested), (
            source["filename"],
            sorted(set(nested) - used),
        )
    return records


def actual_records() -> dict[
    tuple[str, str, str], tuple[str, str, str, str, str, str]
]:
    records: dict[
        tuple[str, str, str], tuple[str, str, str, str, str, str]
    ] = {}
    interface = surface = ""
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") and line not in {
            "## 使用规则",
            "## 生成覆盖摘要",
            "## 目录",
        }:
            interface, surface = line[3:].strip(), ""
        elif line.startswith("### "):
            surface = line[4:].strip()
        elif line.startswith("| `"):
            cells = split_catalog_row(line)
            assert len(cells) == 9, line[:160]
            path = cells[0].strip("`")
            identity = (interface, surface, path)
            assert identity not in records, f"duplicate catalog identity: {identity}"
            records[identity] = (
                cells[1].strip("`"),
                cells[2].strip("`"),
                *(cell.strip("`") for cell in cells[4:8]),
                cells[8],
            )
    return records


def validate_decoding_fixtures(actual: dict) -> None:
    """Execute catalog decode paths against encoded and native array payloads.

    These fixtures independently catch [] applied to an undecoded string,
    extra decoding of native objects, and mixing contracts across interfaces.
    """
    def walk(value: object, expression: str) -> list:
        assert expression.startswith("$")
        if expression.startswith("$[]"):
            assert isinstance(value, list), "array traversal before JSON decoding"
            values = value
            suffix = expression[3:]
        else:
            values = [value]
            suffix = expression[1:]
        for token in suffix.lstrip(".").split(".") if suffix else ():
            selected = []
            for node in values:
                assert isinstance(node, dict)
                child = node[token.removesuffix("[]")]
                if token.endswith("[]"):
                    assert isinstance(child, list), "array traversal before JSON decoding"
                    selected.extend(child)
                else:
                    selected.append(child)
            values = selected
        return values

    def decode(raw: str, expression: str) -> list:
        values = [json.loads(raw)]
        for index, stage in enumerate(expression.split(" => JSON decode => ")):
            if index:
                assert all(isinstance(value, str) for value in values), "decoding a native object"
                values = [json.loads(value) for value in values]
            values = [child for value in values for child in walk(value, stage)]
        return values

    fixtures = (
        (("托管交易查询", "同步响应 data", "response.data.unionpay_response.coupon_info[].spnsr_id"),
         {"coupon_info": json.dumps([{"spnsr_id": "00010000"}])}, ["00010000"]),
        (("托管交易退款查询", "同步响应 data", "response.data.unionpay_response.coupon_info[].offstAmt"),
         {"coupon_info": json.dumps([{"offstAmt": "1.00"}])}, ["1.00"]),
        (("H5/PC预下单", "支付异步 resp_data", "async.resp_data.fee_formula_infos[].fee_sign"),
         {"fee_formula_infos": json.dumps([{"fee_sign": "fixture-fee"}])}, ["fixture-fee"]),
        (("H5/PC预下单", "支付异步 resp_data", "async.resp_data.unionpay_response.coupon_info.spnsr_id"),
         {"unionpay_response": {"coupon_info": {"spnsr_id": "00010000"}}}, ["00010000"]),
        (("拆单支付订单查询", "同步响应 data", "response.data.trans_list[].wx_response.cash_fee"),
         [{"wx_response": json.dumps({"cash_fee": "10.00"})}], ["10.00"]),
    )
    for identity, payload, result in fixtures:
        expression = actual[identity][1]
        try:
            assert decode(json.dumps(payload), expression) == result
        except (AssertionError, TypeError, KeyError) as error:
            raise AssertionError((identity, expression)) from error
    for path in ("spnsrId", "type", "offstAmt"):
        assert actual[("托管交易退款查询", "同步响应 data", "response.data.unionpay_response.coupon_info[]."+path)][4] == "N"
    try:
        decode(json.dumps({"coupon_info": json.dumps([{"id": "fixture"}])}), "$.coupon_info[] => JSON decode => $[].id")
    except AssertionError:
        pass
    else:
        raise AssertionError("fixture accepted array traversal on an undecoded string")
    douyin = actual[("抖音直连下单", "支付异步 resp_data", "async.resp_data.trans_finish_time")]
    assert douyin[0] == "async.resp_data" and "需要官方确认" in douyin[1]
    assert douyin[2:5] == ("String", "13", "N")
    print("payment decoding fixtures validated: nested strings, native objects/arrays, optional fields and unknown notification encoding")


def main() -> int:
    expected = expected_records()
    actual = actual_records()
    assert len(expected) == EXPECTED_TOTAL, (len(expected), EXPECTED_TOTAL)
    assert set(actual) == set(expected), (
        f"missing={sorted(set(expected) - set(actual))[:10]} "
        f"extra={sorted(set(actual) - set(expected))[:10]}"
    )
    mismatches = [
        (identity, expected[identity], actual[identity])
        for identity in expected
        if expected[identity] != actual[identity]
    ]
    assert not mismatches, f"field property mismatches: {mismatches[:10]}"
    validate_decoding_fixtures(actual)
    catalog_text = CATALOG.read_text(encoding="utf-8")
    field_link_targets = [
        target
        for line in catalog_text.splitlines()
        if line.startswith("| `")
        for target in __import__("re").findall(r"\[[^\]]+\]\(([^)]+)\)", line)
    ]
    assert all(
        target.startswith(("http://", "https://"))
        for target in field_link_targets
    ), "generated payment field descriptions contain relative or fragment-only links"
    assert catalog_text.count("官网相对地址原文：`#") == sum(value[-1].count("官网相对地址原文：`#") for value in expected.values())
    assert catalog_text.count("官网原始锚点在当前快照无同名标题") == 0
    assert catalog_text.count("公共返回码全集：[返回码]") >= 8
    assert catalog_text.count("已确认同时指向[聚合正扫异步返回参数]") == 1
    assert "聚合反扫异步返回参数" in catalog_text
    assert "异步消息简介" in catalog_text
    assert catalog_text.count("官网原文测试域，不作为生产地址") == 4
    assert "Signature=" not in catalog_text
    assert "OSSAccessKeyId=" not in catalog_text
    assert catalog_text.count("[官网临时签名 URL 示例已省略]") == 2
    assert catalog_text.count("指定网银支付首次跳转银行页面需要打开浏览器弹窗限制") == 2
    assert "参见图片说明" in catalog_text
    assert catalog_text.count(
        "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/"
    ) == 3
    assert "](" + "https://paas.huifu.com/partners/api/doc/cpjs/[官网示例图片已省略]" not in catalog_text

    create = "聚合支付下单"
    paths = {path for interface, _surface, path in actual if interface == create}
    assert (
        "request.data.method_expand.T_MICROPAY.scene_info.store_info.address"
        in paths
    )
    assert "request.data.method_expand.T_APP.scene_info" not in paths
    assert (
        "async.forward.resp_data.wx_response.promotion_detail[].goods_detail[].quantity"
        in paths
    )
    create_records = {
        path: contract
        for (interface, _surface, path), contract in actual.items()
        if interface == create
    }
    assert create_records[
        "request.data.method_expand.T_MICROPAY.scene_info.store_info.address"
    ][0] == "request.data.method_expand"
    assert create_records[
        "request.data.method_expand.T_MICROPAY.scene_info.store_info.address"
    ][1] == "$.scene_info.store_info.address"
    assert create_records[
        "response.data.method_expand.T_APP.sub_appid"
    ][0] == "response.data.method_expand"
    assert create_records["response.data.method_expand.T_APP.sub_appid"][1] == "$.sub_appid"

    query = "聚合交易查询"
    query_records = {
        path: contract
        for (interface, _surface, path), contract in actual.items()
        if interface == query
    }
    assert query_records["response.data.method_expand.A_JSAPI"][:2] == (
        "—（官网展示分组，不存在该 wire key）",
        "—（官网展示分组，不参与解码）",
    )
    assert query_records[
        "response.data.method_expand.A_JSAPI.buyer_logon_id"
    ][:2] == ("response.data.method_expand", "$.buyer_logon_id")
    assert "=> JSON decode =>" not in query_records[
        "response.data.method_expand.A_JSAPI.buyer_logon_id"
    ][1]
    assert "[接入方确认勘误]" in query_records["response.data.trade_type"][6]
    assert "应为 `A_MICROPAY: 支付宝付款码`" in query_records[
        "response.data.trade_type"
    ][6]

    split = "拆单支付订单查询"
    split_records = {
        path: contract
        for (interface, _surface, path), contract in actual.items()
        if interface == split
    }
    assert split_records["request.data.org_req_seq_id"][:6] == (
        "request.data.org_req_seq_id",
        "—（直接 JSON 路径）",
        "String",
        "64",
        "Y",
        "已确认",
    )
    assert split_records["response.data.org_req_seq_id"][:6] == (
        "response.data.org_req_seq_id",
        "—（直接 JSON 路径）",
        "String",
        "128",
        "N",
        "已确认",
    )

    detail = "交易分账明细查询"
    detail_records = {
        path: contract
        for (interface, _surface, path), contract in actual.items()
        if interface == detail
    }
    assert len(detail_records) == 29
    assert sum(path.startswith("request") for path in detail_records) == 7
    assert sum(path.startswith("response") for path in detail_records) == 22
    assert set(path for path in detail_records if path.startswith("request.data.")) == {
        "request.data.hf_seq_id",
        "request.data.huifu_id",
        "request.data.ord_type",
    }
    assert "response.data.huifu_id" not in detail_records
    assert detail_records["request.data.ord_type"][2:5] == ("String", "20", "Y")
    assert detail_records["response.data.split_trans_responses[]"][2:5] == (
        "String",
        "—",
        "N",
    )
    split_paths = {
        path: contract for path, contract in detail_records.items()
        if path == "response.data.split_trans_responses[]"
        or path.startswith("response.data.split_trans_responses[].")
    }
    assert len(split_paths) == 17
    assert all(contract[0] == "response.data.split_trans_responses" for contract in split_paths.values())
    assert split_paths["response.data.split_trans_responses[]"][1] == "$[]（String(JSON Array) 解码结果）"
    assert all("String(JSON Array) 解码结果" in contract[1] for contract in split_paths.values())

    for interface in ("聚合支付下单", "聚合交易退款"):
        for (record_interface, _surface, path), contract in actual.items():
            if record_interface != interface or ".tx_metadata." not in path:
                continue
            assert ".tx_metadata." not in contract[0], (interface, path, contract[0])
    query_records = {
        path: contract
        for (interface, _surface, path), contract in actual.items()
        if interface == "聚合交易查询"
    }
    assert query_records["response.data.tx_metadata.acct_split_bunch"][0] == "response.data.tx_metadata"
    assert query_records["response.data.tx_metadata.acct_split_bunch"][1].startswith("$.acct_split_bunch")
    refund_query_records = {
        path: contract
        for (interface, _surface, path), contract in actual.items()
        if interface == "聚合交易退款查询"
    }
    assert refund_query_records["response.data.tx_metadata.acct_split_bunch"][0] == "response.data.tx_metadata"
    assert refund_query_records["response.data.tx_metadata.acct_split_bunch"][1].startswith("$.acct_split_bunch")
    all_paths = {path for _interface, _surface, path in actual}
    assert "async.resp_data.resp_code" in all_paths
    assert "async.split.resp_data.resp_code" in all_paths
    assert "async.unconfirmed_payload.resp_code" in all_paths
    assert "async.data.resp_code" in all_paths
    assert split_records["response.data.trans_list[].pay_type"][0] == "response.data.trans_list"
    assert split_records["response.data.trans_list[].pay_type"][1] == "$[].pay_type"
    terminal_path = "request.data.tx_metadata.terminal_device_data.device_ip"
    assert create_records[terminal_path][0] == "request.data.terminal_device_data"
    assert create_records[terminal_path][1] == "$.device_ip"
    assert create_records["async.forward.resp_data.resp_code"][0] == "async.forward.resp_data"
    assert create_records["async.forward.resp_data.resp_code"][1] == "$.resp_code"
    assert all(
        not (
            contract[2] == "String"
            and any(
                other_path.startswith(path + ".")
                for other_interface, _other_surface, other_path in actual
                if other_interface == interface
            )
            and contract[1] == "—（直接 JSON 路径）"
        )
        for (interface, _surface, path), contract in actual.items()
    )
    assert all(
        contract[5].startswith(("[需要官方确认]", "N/A", "已确认"))
        for contract in actual.values()
    )

    print(
        "payment complete field catalog validated independently: "
        f"{len(actual)} interface-scoped paths"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
