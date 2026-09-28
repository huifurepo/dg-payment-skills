#!/usr/bin/env python3
"""Exercise the field-catalog generator through its command-line interface."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

from generate_merchant_onboarding_field_catalog import (
    flatten_fields,
    parse_field_row,
)
from skill_validation_config import onboarding_source_dir
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts/generate_merchant_onboarding_field_catalog.py"
SOURCE_DIR = onboarding_source_dir()

EXPECTED_COUNTS = {
    "企业商户进件": 177,
    "个人商户进件": 129,
    "商户业务开通": 460,
    "图片上传": 9,
    "商户详细信息查询": 578,
    "申请单状态查询": 93,
    "商户业务开通修改": 452,
    "商户基本信息修改": 199,
    "商户费率信息查询": 35,
    "商户状态变更": 14,
    "商户短信发送": 20,
    "商户多费率配置": 27,
    "商户多费率配置查询": 17,
}


def section_text(text: str, title: str) -> str:
    match = re.search(
        rf"^## {re.escape(title)}\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.M | re.S,
    )
    if not match:
        raise AssertionError(f"missing interface section: {title}")
    return match.group("body")


def main() -> int:
    native_array = parse_field_row(
        '| fee_rate_type | 费率类型 | Array<string> | 117 | N | 示例值：["T1"] |',
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md",
        frozenset(),
    )
    assert native_array is not None and native_array.is_array
    native_paths = flatten_fields([native_array], {}, "request.data", set())
    assert native_paths[0][0] == "request.data.fee_rate_type[]"
    assert native_array.field_type == "Array<string>", "HTML cleanup erased array subtype"
    typo_fixture = (
        '| <span class="extend fixture_child">other_list</span> | 其他集合 | '
        "String | | N | josnArray格式；此集合可能有多条数据 |"
    )
    fixture_url = (
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/"
        "api_shjj_shxxxxcx_kyc.md"
    )
    typo_field = parse_field_row(typo_fixture, fixture_url, frozenset())
    assert typo_field is not None and not typo_field.is_array
    try:
        flatten_fields(
            [typo_field],
            {"fixture_child": []},
            "request.data",
            set(),
        )
    except ValueError as exc:
        assert "unregistered josnArray marker" in str(exc)
    else:
        raise AssertionError("unregistered josnArray typo was accepted globally")

    scalar_array_fixture = (
        "| pay_channel_id_list | 子渠道号 | String | | N | "
        'String集合，jsonArray格式；示例值：["JQF00001"] |'
    )
    scalar_array_field = parse_field_row(
        scalar_array_fixture,
        fixture_url,
        frozenset(),
    )
    assert scalar_array_field is not None and scalar_array_field.is_array
    scalar_array_paths = flatten_fields(
        [scalar_array_field],
        {},
        "response.data.qry_wx_conf_list[]",
        set(),
    )
    assert scalar_array_paths[0][0] == (
        "response.data.qry_wx_conf_list[].pay_channel_id_list[]"
    ), "scalar jsonArray without an extend-table lost its array marker"
    relative_link_fixture = (
        "| pay_scene | 支付场景 | String | 2 | Y | "
        "参见[微信支付场景](api_ggcsbm.md#微信支付场景) |"
    )
    relative_link_field = parse_field_row(
        relative_link_fixture,
        fixture_url,
        frozenset(),
    )
    assert relative_link_field is not None
    assert (
        "https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景"
        in relative_link_field.description
    )
    assert "官网相对地址原文：`api_ggcsbm.md#微信支付场景`" in (
        relative_link_field.description
    )

    with tempfile.TemporaryDirectory(prefix="huifu-field-catalog-") as temp_dir:
        output = Path(temp_dir) / "catalog.md"
        subprocess.run(
            [
                sys.executable,
                "-B",
                str(GENERATOR),
                "--source-dir",
                str(SOURCE_DIR),
                "--output",
                str(output),
            ],
            cwd=ROOT,
            check=True,
        )
        text = output.read_text(encoding="utf-8")

    for title, expected in EXPECTED_COUNTS.items():
        actual = sum(
            line.startswith("| `") for line in section_text(text, title).splitlines()
        )
        assert actual == expected, f"{title}: expected {expected} paths, found {actual}"
        assert sum(EXPECTED_COUNTS.values()) == 2210

    target = next(
        line
        for line in text.splitlines()
        if line.startswith(
            "| `response.data.mer_config_info.online_fee_conf_list[].bus_type`"
        )
    )
    assert "5：B2C网银充值" in target, "wrapped bus_type enum 5 was truncated"
    assert "6：代扣支付" in target, "wrapped bus_type enum 6 was truncated"
    business_modify = section_text(text, "商户业务开通修改")
    assert "async.business.reg_result_list[].business_stat" in business_modify
    assert "async.business.reg_result_list.business_stat" not in business_modify
    assert "josnArray格式" in business_modify
    detail_query = section_text(text, "商户详细信息查询")
    assert (
        "response.data.qry_wx_conf_list[].pay_channel_id_list[]" in detail_query
    )
    assert (
        "response.data.qry_wx_conf_list[].pay_channel_id_list`" not in detail_query
    )
    print(
        "merchant-onboarding field-catalog generation validated: "
        "2210 paths, native string arrays, wrapped descriptions and relative links preserved"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
