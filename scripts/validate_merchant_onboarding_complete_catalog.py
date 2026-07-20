#!/usr/bin/env python3
"""Validate the generated six-interface merchant-onboarding field catalog."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "huifu-pay-integration/references/merchant-onboarding-complete-field-catalog.md"
GENERATOR = ROOT / "scripts/generate_merchant_onboarding_field_catalog.py"
EXTERNAL_INDEX = (
    ROOT / "huifu-pay-integration/references/merchant-onboarding-external-resources.md"
)

EXPECTED_COUNTS = {
    "企业商户进件": 169,
    "个人商户进件": 129,
    "商户业务开通": 442,
    "图片上传": 9,
    "商户详细信息查询": 551,
    "申请单状态查询": 93,
}

REQUIRED_PATHS = (
    "request.data.beneficiary_info[].bo_name",
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
)

SOURCE_URLS = (
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md",
    "https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md",
)

SOURCE_SHA256 = (
    "403435d34acf0553eaa67838bc85a34d34aace19cb5f3dbed0ee49480a14e7a7",
    "97a4262af54c475c548c02eb8590a63712029d66ce9d88f52838af5b0ebfecb2",
    "4c539102b0611d9fa25e4ff675b6f8551199d80b2d44181bb59947ace6c70919",
    "e1acf74e60436d069f3c605c19b24aab6d703494e1ebdd8c90b11104e4646125",
    "1517450f61f37ef4d4e8ca913ef1704c8a072f577e3a65dc5c901af669bf038d",
    "89f51fdbca529b1f7166aeba1d5d24eb16469fd153cd09cafbf811d9e68f050f",
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

    image = section_text(text, "图片上传")
    assert "官方 JSON 未给 HTTP method、host 或 Content-Type" in image
    assert "官方 JSON 未定义响应字段" in image
    assert "`request.sign`" not in image
    assert "`request.file` | 图片文件流 | `—` | `—` | `—`" in image

    status = section_text(text, "申请单状态查询")
    assert "response.data.wx_config_list[].pay_scene" not in status
    assert "response.data.wx_config_list[].config_value" in status

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
    for url in runtime_examples:
        assert url not in external_text, f"runtime example must not be promoted to a resource: {url}"
    print(
        "merchant-onboarding complete catalog validated: "
        f"{sum(EXPECTED_COUNTS.values())} interface-scoped field paths"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
