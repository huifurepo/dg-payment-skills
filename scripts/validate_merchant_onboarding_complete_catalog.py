#!/usr/bin/env python3
"""Validate the generated six-interface merchant-onboarding field catalog."""

from __future__ import annotations

import re
import json
from pathlib import Path

from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md"
GENERATOR = ROOT / "scripts/generate_merchant_onboarding_field_catalog.py"
EXTERNAL_INDEX = (
    ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-external-resources.md"
)
SOURCE_LOCK = ROOT / "maintainer-contracts/merchant-onboarding-source-lock.json"

EXPECTED_COUNTS = {
    "企业商户进件": 177,
    "个人商户进件": 129,
    "商户业务开通": 442,
    "图片上传": 9,
    "商户详细信息查询": 559,
    "申请单状态查询": 93,
    "商户业务开通修改": 434,
    "商户基本信息修改": 199,
    "商户费率信息查询": 35,
    "商户状态变更": 14,
    "商户短信发送": 20,
}

REQUIRED_PATHS = (
    "request.data.beneficiary_info[].bo_name",
    "request.data.share_holder_info_list[].mobile_no",
    "response.data.elec_acct_config.elec_card_list[].bind_card_msg",
    "async.audit.data.elec_acct_result.sign_agreement_id",
    "request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_file_list[].file_id",
    "request.data.merge_pay_config_info.merge_pay_config.merge_pay_mode",
    "async.business.reg_result_list[].real_name_applyment_stat",
    "request.data.file_url",
    "response.data.mer_config_info.online_fee_conf_list[].bus_type",
    "response.data.split_bill_result[].acct_split_bunch_list[].fee_rate",
    "response.data.wx_config_list[].config_value",
    "response.data.agreement_info_list[].agreement_link",
    "response.data.share_holder_info_list[].mobile_no",
    "request.data.merge_pay_config_info.merge_pay_config.merge_pay_mode",
    "request.data.card_info.card_no",
    "response.data.wx_fee_rate_list[].pay_type",
    "request.data.upd_status_reason",
    "request.data.elec_acct_sign_seq_id",
)

SOURCE_URLS = (
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md",
    "https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md",
    "https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md",
)

SOURCE_SHA256 = tuple(
    item["sha256"]
    for item in json.loads(SOURCE_LOCK.read_text(encoding="utf-8"))["sources"]
)


def section_text(text: str, title: str) -> str:
    match = re.search(
        rf"^## {re.escape(title)}\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.M | re.S,
    )
    if not match:
        raise AssertionError(f"missing interface section: {title}")
    return match.group("body")


def field_rows(section: str) -> list[str]:
    return [line for line in section.splitlines() if line.startswith("| `")]


def main() -> int:
    assert CATALOG.exists(), f"missing catalog: {CATALOG}"
    assert GENERATOR.exists(), f"missing generator: {GENERATOR}"
    assert EXTERNAL_INDEX.exists(), f"missing external-resource index: {EXTERNAL_INDEX}"
    text = CATALOG.read_text(encoding="utf-8")
    external_text = EXTERNAL_INDEX.read_text(encoding="utf-8")

    for title, expected in EXPECTED_COUNTS.items():
        section = section_text(text, title)
        actual = len(field_rows(section))
        assert actual == expected, f"{title}: expected {expected} paths, found {actual}"
        summary_row = rf"\| {re.escape(title)} \| {expected} \|"
        assert re.search(summary_row, text), f"{title}: stale summary count"

    for path in REQUIRED_PATHS:
        assert f"`{path}`" in text, f"missing critical nested path: {path}"
    for url in SOURCE_URLS:
        assert url in text, f"missing original source URL: {url}"
    for digest in SOURCE_SHA256:
        assert f"SHA-256：`{digest}`" in text, f"missing source digest: {digest}"

    business = section_text(text, "商户业务开通")
    assert "request.data.wx_zl_conf.contact_info.contact_file_list[]" not in business
    assert "request.data.wx_zl_conf.sales_info.sales_scenes_file_list[]" not in business
    assert "request.data.wx_zl_conf.contact_info.contact_file_list`" in business
    assert "request.data.wx_zl_conf.sales_info.sales_scenes_file_list`" in business
    assert "async.agreement.agreement_info_list[]" not in business
    assert "async.agreement.agreement_info_list.con_stat" in business

    business_modify = section_text(text, "商户业务开通修改")
    assert "async.business.reg_result_list[].business_stat" in business_modify
    assert "async.business.reg_result_list.business_stat" not in business_modify
    assert "async.agreement.agreement_info_list[]" not in business_modify
    assert "async.agreement.agreement_info_list.con_stat" in business_modify

    basic_modify = section_text(text, "商户基本信息修改")
    assert "async.agreement.agreement_info_list[]" not in basic_modify
    assert "async.agreement.agreement_info_list.con_stat" in basic_modify

    image = section_text(text, "图片上传")
    assert "官方 JSON 未给 HTTP method、host 或 Content-Type" in image
    assert "官方 JSON 未定义响应字段" in image
    assert "`request.sign`" not in image
    assert "`request.file` | 图片文件流 | `—` | `—` | `—`" in image

    status = section_text(text, "申请单状态查询")
    assert "response.data.wx_config_list[].pay_scene" not in status
    assert "response.data.wx_config_list[].config_value" in status
    assert "response.data.agreement_info_list[].con_stat" in status

    detail = section_text(text, "商户详细信息查询")
    bus_type_row = next(
        line
        for line in detail.splitlines()
        if line.startswith(
            "| `response.data.mer_config_info.online_fee_conf_list[].bus_type`"
        )
    )
    assert "5：B2C网银充值" in bus_type_row
    assert "6：代扣支付" in bus_type_row

    status_change = section_text(text, "商户状态变更")
    assert "request.data.file_list" not in status_change
    assert "request.data.upd_status_reason" in status_change

    assert "字段说明引用外部网页或文件时" in text
    assert "[官方文档口径冲突]" in text

    # Every linked field instruction must be routable to the explicit external
    # resource notice. The one excluded link is the official file_url example,
    # which the index deliberately classifies as a runtime/example URL.
    linked_urls = set(re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", text))
    runtime_examples = {
        "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/guide/jinjian/%E8%90%A5%E4%B8%9A%E6%89%A7%E7%85%A71-2.png"
    }
    unrouted = sorted(url for url in linked_urls - runtime_examples if url not in external_text)
    assert not unrouted, f"field links missing from external-resource index: {unrouted}"
    exact_external_bindings = {
        "response.data.qry_wx_conf_list[].pay_scene": (
            "https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景"
        ),
        "response.data.wx_conf_result_list[].pay_scene": (
            "https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景"
        ),
        "response.data.wx_fee_rate_list[].pay_scene": (
            "https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景"
        ),
        "request.data.material_card_info.prov_id/area_id": (
            "https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm"
        ),
        "request.data.material_card_info.branch_code": (
            "https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm"
        ),
    }
    external_lines = external_text.splitlines()
    for field_path, url in exact_external_bindings.items():
        assert any(
            field_path in line and url in line
            for line in external_lines
        ), f"missing exact external-resource binding: {field_path} -> {url}"
    assert "十个 Markdown JSON 接口顶层 `sign`（不含图片上传）" in external_text
    for url in runtime_examples:
        assert url not in external_text, f"runtime example must not be promoted to a resource: {url}"
    print(
        "merchant-onboarding complete catalog validated: "
        f"{sum(EXPECTED_COUNTS.values())} interface-scoped field paths"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
