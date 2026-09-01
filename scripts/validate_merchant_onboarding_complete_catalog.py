#!/usr/bin/env python3
"""Validate the generated merchant-onboarding field catalog."""

from __future__ import annotations

import hashlib
import re
import json
from pathlib import Path

from skill_validation_config import ONBOARDING_SOURCE_LOCK
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md"
GENERATOR = ROOT / "scripts/generate_merchant_onboarding_field_catalog.py"
EXTERNAL_INDEX = (
    ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-external-resources.md"
)
SOURCE_LOCK = ONBOARDING_SOURCE_LOCK
HISTORICAL_SOURCE_LOCK = ROOT / "maintainer-contracts/merchant-onboarding-source-lock.json"
R1_MERCHANT_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-source-lock-2026-08-24.json"
)
R2_MERCHANT_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-source-lock-2026-08-24-r2.json"
)
R1_COMBINED_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-1.0.2-source-lock.json"
)
R1_REFRESH_CONTRACT = (
    ROOT / "maintainer-contracts/api-refresh-merchant-multifee-config-2026-08-24.json"
)
R2_COMBINED_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-1.0.2-r2-source-lock.json"
)
R2_REFRESH_CONTRACT = (
    ROOT / "maintainer-contracts/api-refresh-merchant-multifee-query-2026-08-24.json"
)
R3_COMBINED_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-1.0.2-r3-source-lock.json"
)
R3_REFRESH_CONTRACT = (
    ROOT / "maintainer-contracts/api-refresh-user-enterprise-modify-2026-08-24.json"
)
R4_COMBINED_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-1.0.2-r4-source-lock.json"
)
R4_REFRESH_CONTRACT = (
    ROOT / "maintainer-contracts/api-refresh-user-individual-modify-2026-08-24.json"
)
R5_COMBINED_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-1.0.2-r5-source-lock.json"
)
R5_REFRESH_CONTRACT = (
    ROOT / "maintainer-contracts/api-refresh-user-business-modify-2026-08-24.json"
)
R6_COMBINED_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-1.0.2-r6-source-lock.json"
)
R6_REFRESH_CONTRACT = (
    ROOT / "maintainer-contracts/api-refresh-user-list-query-2026-08-24.json"
)
COMBINED_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/merchant-onboarding-1.0.2-r7-source-lock.json"
)
REFRESH_CONTRACT = (
    ROOT / "maintainer-contracts/api-refresh-onboarding-online-review-2026-08-31.json"
)
MANIFEST = ROOT / "skills-manifest.json"
HISTORICAL_USER_SOURCE_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock.json"
R1_USER_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r1.json"
)
R2_USER_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r2.json"
)
R3_USER_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r3.json"
)
R4_USER_SOURCE_LOCK = (
    ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r4.json"
)
USER_SOURCE_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-31.json"
USER_CATALOG = (
    ROOT / "huifu-merchant-onboarding/references/user-onboarding-complete-field-catalog.md"
)
R1_SOURCE_DIR = (
    ROOT / "maintainer-contracts/official-sources/merchant-onboarding/2026-08-24"
)
R2_SOURCE_DIR = (
    ROOT / "maintainer-contracts/official-sources/merchant-onboarding/2026-08-24-r2"
)

EXPECTED_COUNTS = {
    "企业商户进件": 177,
    "个人商户进件": 129,
    "商户业务开通": 452,
    "图片上传": 9,
    "商户详细信息查询": 567,
    "申请单状态查询": 93,
    "商户业务开通修改": 444,
    "商户基本信息修改": 199,
    "商户费率信息查询": 35,
    "商户状态变更": 14,
    "商户短信发送": 20,
    "商户多费率配置": 27,
    "商户多费率配置查询": 17,
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
    "request.data.wx_conf_list[].fee_sign",
    "request.data.ali_conf_list[].fee_rate",
    "response.data.conf_list.pay_way",
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
    "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md",
    "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md",
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_release_provenance() -> None:
    assert sha256(HISTORICAL_SOURCE_LOCK) == (
        "242c8588f825dd6182ba474299ecbe7554357de6a7fb1720a0d5f46dc33bf9cd"
    ), "the unversioned 2026-07-29 historical source lock must remain immutable"
    assert sha256(R1_MERCHANT_SOURCE_LOCK) == (
        "3fc098c66e3018f0cb81ff424220bd4c21c3894ba602e39728aeed6a4791507e"
    ), "the merchant multi-fee configuration r1 source lock must remain immutable"
    assert sha256(R1_COMBINED_SOURCE_LOCK) == (
        "36e9a894da902298564ec50ea3c331ef45e33b43c266c242cbeea82e9535071a"
    ), "the merchant multi-fee configuration r1 combined lock must remain immutable"
    assert sha256(R1_REFRESH_CONTRACT) == (
        "c22daa1dfbc54270f4eb345230c19c2ed1aff51a1bbfc99802e61c7d034fa0c4"
    ), "the merchant multi-fee configuration r1 refresh contract must remain immutable"
    assert sha256(R2_COMBINED_SOURCE_LOCK) == (
        "56f447e95855bcd6e9a8aba4eb397a341873e653fd99c27e820290cf32a33fd0"
    ), "the merchant multi-fee query r2 combined lock must remain immutable"
    assert sha256(R2_REFRESH_CONTRACT) == (
        "a50b499bc27df26639534940849695f2ed839f57f029cf3b9202556a03e8629d"
    ), "the merchant multi-fee query r2 refresh contract must remain immutable"
    assert sha256(HISTORICAL_USER_SOURCE_LOCK) == (
        "870c49a6affb8584284398ddc86befe12ab7d40a94ef491322ea1f5a4d296169"
    ), "the five-interface user source lock must remain immutable"
    assert sha256(R1_USER_SOURCE_LOCK) == (
        "82d08b1a7a588fb22173720c79ec3992d0481c80abeaa044a3b37e90a83582e9"
    ), "the enterprise user modification r1 lock must remain immutable"
    assert sha256(R3_COMBINED_SOURCE_LOCK) == (
        "acf608d8c7e2f534ae7383f40befcc26307c431a6bd18a1a9625c1bb97c7e6c3"
    ), "the enterprise user modification r3 combined lock must remain immutable"
    assert sha256(R3_REFRESH_CONTRACT) == (
        "c35fe71763f3c0e2bb6222ae4773133b7b9cb1512716e3f04b96f73c3969c5e5"
    ), "the enterprise user modification r3 refresh must remain immutable"
    assert sha256(R2_USER_SOURCE_LOCK) == (
        "6c79cd8079d155df243681b2f206ded1af9a65095839946584c6cde008ed0d72"
    ), "the individual user modification r2 source lock must remain immutable"
    assert sha256(R4_COMBINED_SOURCE_LOCK) == (
        "17bbdfa001518ef2f1a5c77cb3d5dde4b9793e34c1963a94ad4e549c7800c75f"
    ), "the individual user modification r4 combined lock must remain immutable"
    assert sha256(R4_REFRESH_CONTRACT) == (
        "dfa97a88addcc9392353a2ed22c9861207578f92a04b71610c49320319802016"
    ), "the individual user modification r4 refresh must remain immutable"
    assert sha256(R3_USER_SOURCE_LOCK) == (
        "72d1a2d677a929ca5d073b96f508e79c0803cccfb9e5b36dc5593e9bac5a1e74"
    ), "the business user modification r3 source lock must remain immutable"
    assert sha256(R5_COMBINED_SOURCE_LOCK) == (
        "d2e96353e2ede50758030836fd0a11ebcab7e08b1855ebc02de30a2f5390f90d"
    ), "the business user modification r5 combined lock must remain immutable"
    assert sha256(R5_REFRESH_CONTRACT) == (
        "f63220556555711b9c5a30fa8b748690ceca5e6f43d3f5a7354137309516d590"
    ), "the business user modification r5 refresh must remain immutable"

    assert sha256(R6_COMBINED_SOURCE_LOCK) == (
        "ba1d358b5b8aa8bfce595facea8258e29ebf1fe7f0983042dbffbdd3ea25f243"
    ), "the list-query r6 combined lock must remain immutable"
    assert sha256(R6_REFRESH_CONTRACT) == (
        "920fa7178e0edb77aa2405745b21640876e9fb8f03e17d30c3424c97c966dae8"
    ), "the list-query r6 refresh must remain immutable"

    r1_merchant = json.loads(R1_MERCHANT_SOURCE_LOCK.read_text(encoding="utf-8"))
    r2_merchant = json.loads(R2_MERCHANT_SOURCE_LOCK.read_text(encoding="utf-8"))
    assert r2_merchant["source_snapshot_id"] == "2026-08-24-r2"
    assert r2_merchant["sources"][:-1] == r1_merchant["sources"], (
        "r2 must preserve every r1 source entry before adding the query page"
    )
    assert r2_merchant["sources"][-1] == {
        "key": "multifee_query",
        "title": "商户多费率配置查询",
        "filename": "multifee-query.md",
        "url": "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md",
        "sha256": "2122f0a613540dca2a0f33da61879730c29b581918db53825b9feb7856aaee75",
        "field_count": 17,
    }
    for source in r1_merchant["sources"]:
        filename = source["filename"]
        assert (R2_SOURCE_DIR / filename).read_bytes() == (
            R1_SOURCE_DIR / filename
        ).read_bytes(), f"r2 changed inherited source bytes: {filename}"
    assert r2_merchant["current_extension"] == {
        "refresh_id": "api-refresh-merchant-multifee-query-2026-08-24-r2",
        "previous_refresh_id": "api-refresh-merchant-multifee-config-2026-08-24-r1",
        "retrieved_at": "2026-08-24T16:23:14+08:00",
        "official_page_update": "2025-11-03",
        "added_source_keys": ["multifee_query"],
        "field_paths_added": 17,
        "field_paths_removed": 0,
        "field_paths_changed": 0,
        "document_conflicts": [],
        "inherited_extension": {
            "refresh_id": "api-refresh-merchant-multifee-config-2026-08-24-r1",
            "source_key": "multifee_config",
            "official_page_update": "2025-11-04",
            "field_paths_added": 27,
            "document_conflicts": [
                "response.data.conf_list.pay_scene uses T for WeChat while "
                "response.data.conf_list.pay_way defines W for WeChat"
            ],
        },
    }

    combined = json.loads(COMBINED_SOURCE_LOCK.read_text(encoding="utf-8"))
    assert set(combined) == {
        "schema_version",
        "skill",
        "version",
        "refresh_revision",
        "scope",
        "previous_combined_lock",
        "source_locks",
        "catalogs",
        "totals",
    }
    assert combined["schema_version"] == 1
    assert combined["skill"] == "huifu-merchant-onboarding"
    assert combined["version"] == "1.0.2"
    assert combined["refresh_revision"] == "2026-08-31"
    assert combined["scope"] == (
        "Combined immutable source evidence for thirteen merchant onboarding and "
        "management interfaces plus nine user onboarding interfaces after the "
        "2026-08-31 online review."
    )
    assert combined["previous_combined_lock"] == {
        "path": "maintainer-contracts/merchant-onboarding-1.0.2-r6-source-lock.json",
        "sha256": sha256(R6_COMBINED_SOURCE_LOCK),
    }
    assert combined["source_locks"] == {
        "merchant_onboarding": {
            "path": "maintainer-contracts/merchant-onboarding-source-lock-2026-08-31.json",
            "sha256": sha256(SOURCE_LOCK),
            "field_paths": 2183,
        },
        "user_onboarding": {
            "path": "maintainer-contracts/user-onboarding-source-lock-2026-08-31.json",
            "sha256": sha256(USER_SOURCE_LOCK),
            "field_paths": 554,
        },
    }
    assert combined["catalogs"] == {
        "merchant": {
            "path": "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md",
            "sha256": sha256(CATALOG),
        },
        "user": {
            "path": "huifu-merchant-onboarding/references/user-onboarding-complete-field-catalog.md",
            "sha256": sha256(USER_CATALOG),
        },
    }
    assert combined["totals"] == {"interfaces": 22, "field_paths": 2737}

    refresh = json.loads(REFRESH_CONTRACT.read_text(encoding="utf-8"))
    assert set(refresh) == {
        "schema_version",
        "refresh_id",
        "requested_at",
        "retrieved_at",
        "version_state",
        "previous_refresh",
        "source_locks",
        "catalogs",
        "scope",
        "field_delta",
        "preserved_boundaries",
        "release_rule",
    }
    assert refresh["schema_version"] == 1
    assert refresh["refresh_id"] == "api-refresh-onboarding-online-review-2026-08-31"
    assert refresh["requested_at"] == "2026-08-31"
    assert re.fullmatch(r"2026-08-31T\d{2}:\d{2}:\d{2}\+08:00", refresh["retrieved_at"])
    assert refresh["version_state"] == {
        "reason": "Refresh all current merchant and user onboarding pages in the unpublished huifu-merchant-onboarding 1.0.2 candidate without changing its version.",
        "huifu-merchant-onboarding": "1.0.2",
        "huifu-pay-integration": "1.3.5",
    }
    assert refresh["previous_refresh"] == {
        "path": "maintainer-contracts/api-refresh-user-list-query-2026-08-24.json",
        "sha256": sha256(R6_REFRESH_CONTRACT),
        "refresh_id": "api-refresh-user-list-query-2026-08-24-r6",
    }
    assert refresh["source_locks"] == {
        "onboarding_1_0_2": {
            "path": "maintainer-contracts/merchant-onboarding-1.0.2-r7-source-lock.json",
            "sha256": sha256(COMBINED_SOURCE_LOCK),
        },
        "merchant_onboarding_current": {
            "path": "maintainer-contracts/merchant-onboarding-source-lock-2026-08-31.json",
            "sha256": sha256(SOURCE_LOCK),
        },
        "user_onboarding_current": {
            "path": "maintainer-contracts/user-onboarding-source-lock-2026-08-31.json",
            "sha256": sha256(USER_SOURCE_LOCK),
        },
    }
    assert refresh["catalogs"] == {
        "merchant": {
            "path": "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md",
            "sha256": sha256(CATALOG),
            "field_paths": 2183,
        },
        "user": {
            "path": "huifu-merchant-onboarding/references/user-onboarding-complete-field-catalog.md",
            "sha256": sha256(USER_CATALOG),
            "field_paths": 554,
        },
    }
    assert refresh["scope"] == [
        "thirteen merchant onboarding and management interfaces",
        "nine user onboarding and management interfaces",
        "Java 3.0.40, PHP 2.0.30 and Python 2.0.24 SDK evidence",
    ]
    assert refresh["field_delta"] == {
        "merchant_paths_added": 29,
        "merchant_paths_removed": 1,
        "merchant_paths_changed": 45,
        "user_paths_added": 5,
        "user_paths_removed": 5,
        "user_paths_changed": 43,
        "merchant_catalog_total": 2183,
        "user_catalog_total": 554,
        "combined_total": 2737,
    }
    assert refresh["preserved_boundaries"] == [
        "historical merchant, user and combined source locks remain byte-identical",
        "merchant multifee conf_list remains String with unresolved object-versus-array encoding",
        "user business open elec_receipt_config/elec_card_list and business modify response.data/elec_receipt_config/elec_card_list encoding conflicts remain unresolved",
        "all current field names, directions, paths, array layers, types, lengths, Y/N/C markers and descriptions are generated from the 2026-08-31 source locks",
    ]
    assert refresh["release_rule"] == (
        "The 2,183-node merchant and 554-node user catalogs, immutable historical sources, "
        "independent source and catalog validators, SDK evidence, Skill validation, regression "
        "rules and package validation must pass before publishing huifu-merchant-onboarding 1.0.2."
    )
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["skills"][
        "huifu-merchant-onboarding"
    ]
    assert manifest["version"] == "1.0.2"
    assert manifest["source_lock"] == COMBINED_SOURCE_LOCK.relative_to(ROOT).as_posix()
    assert manifest["refresh_contract"] == REFRESH_CONTRACT.relative_to(ROOT).as_posix()


def main() -> int:
    assert CATALOG.exists(), f"missing catalog: {CATALOG}"
    assert GENERATOR.exists(), f"missing generator: {GENERATOR}"
    assert EXTERNAL_INDEX.exists(), f"missing external-resource index: {EXTERNAL_INDEX}"
    text = CATALOG.read_text(encoding="utf-8")
    external_text = EXTERNAL_INDEX.read_text(encoding="utf-8")
    validate_release_provenance()

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

    multifee_config = section_text(text, "商户多费率配置")
    assert "request.data.wx_conf_list[].pay_scene" in multifee_config
    assert "request.data.ali_conf_list[].pay_scene" in multifee_config
    assert "response.data.conf_list.pay_way" in multifee_config
    assert "response.data.conf_list[].pay_way" not in multifee_config
    assert "支付功能为W：微信" in multifee_config
    assert "支付功能为T：微信" not in multifee_config
    assert "A：支付宝 W：微信" in multifee_config

    multifee_query = section_text(text, "商户多费率配置查询")
    assert "request.data.fee_sign" in multifee_query
    assert "response.data.conf_list.pay_way" in multifee_query
    assert "response.data.conf_list[].pay_way" not in multifee_query
    assert "支付功能为W：微信" in multifee_query
    assert "支付功能为T：微信" not in multifee_query
    for undeclared in (
        "response.data.req_seq_id",
        "response.data.req_date",
        "response.data.conf_status",
    ):
        assert undeclared not in multifee_query

    source_lock = json.loads(SOURCE_LOCK.read_text(encoding="utf-8"))
    documented_conflicts = source_lock["api_refresh"]["document_conflicts"]
    assert documented_conflicts == [
        "response.data.conf_list is String with a child table but the document does not define object-versus-array encoding",
        "request.data.jxf_conf_info.jxf_fee_info.fee_charge_type appears only in examples and is excluded from the formal catalog",
        "request.data.jxf_conf_info.jxf_fee_info.quota_issue_fee_rate says two decimals while the example uses four",
    ]
    assert not any("conf_list[]" in item for item in documented_conflicts)

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
    assert "十三个接口中的十二个 Markdown JSON 接口顶层 `sign`（不含图片上传）" in external_text
    for url in runtime_examples:
        assert url not in external_text, f"runtime example must not be promoted to a resource: {url}"
    print(
        "merchant-onboarding complete catalog validated: "
        f"{sum(EXPECTED_COUNTS.values())} interface-scoped field paths"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
