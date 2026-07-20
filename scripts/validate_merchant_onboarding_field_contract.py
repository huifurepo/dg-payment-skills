#!/usr/bin/env python3
"""Guard the source-backed merchant-onboarding field-contract index."""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "huifu-pay-integration/references/merchant-onboarding-field-contracts.md"
EXTERNAL_RESOURCES = ROOT / "huifu-pay-integration/references/merchant-onboarding-external-resources.md"

EXTERNAL_RESOURCE_REQUIRED = (
    "外部资料提示",
    "未经改写、未经缩短的原始地址",
    "未读取外部文件内容，请按原始地址人工核验",
    "示例或运行时 URL",
    "https://paas.huifu.com/open/doc/guide/#/api_v2jqyq",
    "http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%95%86%E6%88%B7%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B",
    "https://paas.huifu.com/partners/api/doc/api_ggcsbm.md",
    "KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx",
    "KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx",
    "KYC-%E4%BD%99%E9%A2%9D%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx",
    "KYC-%E5%88%86%E8%B4%A6%E5%8A%9F%E8%83%BD%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E%281%29.xlsx",
    "%E4%BB%A3%E6%89%A3%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx",
    "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm",
    "https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx",
    "https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc",
    "https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html",
    "https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/applysubject_new/chapter6_1.shtml",
    "api_ggcsbm.md#微信支付场景",
    "https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景",
    "http://service.example.com/to/path",
    "https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#网关返回码",
    "原址不在 Skill 中复述",
    "response.data.qry_wx_conf_list[].pay_scene",
    "response.data.wx_conf_result_list[].pay_scene",
)

EXTERNAL_RESOURCE_FORBIDDEN = (
    "data.wx_config_list[].pay_scene",
)

# High-risk field/type/length/required markers from the six official pages.
# Complete path coverage is validated separately against the generated catalog.
REQUIRED = {
    "enterprise": ("企业商户进件", "req_seq_id String(32) Y", "card_info String(JSON Object) Y", "legal_cert_end_date String(8) C", "async_return_url String(120) N", "`branch_code`", "`cert_validity_type`"),
    "individual": ("个人商户进件", "req_seq_id String(32) Y", "mcc String(7) Y", "settle_card_front_pic String(64) Y", "head_huifu_id String(18) C", "`bank_code`", "`cert_begin_date`"),
    "business": (
        "商户业务开通",
        "huifu_id/upper_huifu_id String(18) Y",
        "agreement_info String(JSON Object) C",
        "agreement_info.agreement_async_return_url",
        "busi_async_return_url String(128) N",
        "业务开通请求 `data.online_flag/quick_flag/withhold_flag`",
        "仅 `Y/N`",
        "`1=外扣`、`2=内扣`，默认 `2`",
        "`01=基本户`、`02=现金户`、`05=充值户`、`09=营销户`，默认 `01`",
        "目前仅支持企业商户",
        "`7011/7296/7512`",
        "`mer_bus_type` 的完整公开枚举",
        "`withhold_flag=Y` 时必填",
        "示例值只演示格式",
    ),
    "image": ("图片上传", "官网仅给 URI `/v2/supplementary/picture`，未给 method", "当前 SDK 适配证据使用 `POST`", "file_type String(32) Y", "file_url String(512) N", "huifu_id String(18) N", "顶层 `file` 互斥"),
    "detail": (
        "商户详细信息查询",
        "req_seq_id String(32) Y",
        "req_date String(8) Y",
        "huifu_id String(18) Y",
        "data.resp_code String(8) Y",
        "详情查询响应 `data.online_flag/quick_flag/withhold_flag`",
        "`1=开通`、`0=未开通`、空=未配置",
        "只用于解析，不得复制回业务开通请求",
        "详情响应 `sms_send_flag=Y/N`",
    ),
    "status": ("申请单状态查询", "apply_no String(18) Y", "data.apply_status", "data.reg_status", "bank_card_conf_status", "bind_card_status", "cash_status", "settle_status", "union_conf_status", "out_order_funds_status", "均为 `String(1)`：`P/S/F`", "`P=处理中`、`S=成功`、`F=失败`", "data.wx_zl_config.apply_state", "`String(32)`：`S/P/N/F/C`", "data.ali_zl_config[].apply_status"),
    "callbacks": ("reg_result_list[].business_stat", "zl_async_info.apply_state", "agreement_info_list[].con_stat", "ord_id:String(44)", "RECV_ORD_ID_", "[需要官方确认]", "逐业务通知外层包装待官方样本确认"),
    "headers": ("jpt-x-skill-source: <skill_source>", "jpt-x-skill-huifu_id: <data.huifu_id>", "Java、PHP、Python SDK 主链路"),
    "java-security": ("五个 JSON 接口和图片 `file_url` 模式", "公共 `AbstractRequest`", "`BasePay.debug` 默认为 `true`", "BasePay.debug = false;", "任何 SDK 请求之前", "不得在并发请求中临时切换", "五个 JSON 接口保留请求签名和响应验签", "图片 `file_url` 必须使用 `isPage=true`", "保留请求签名但跳过响应验签"),
}

ATOMIC_PAGES = (
    "merchant-onboarding-enterprise.md",
    "merchant-onboarding-individual.md",
    "merchant-onboarding-business-open.md",
    "merchant-onboarding-image-upload.md",
    "merchant-onboarding-detail-query.md",
    "merchant-onboarding-application-status-query.md",
)
ATOMIC_HEADER_TERMS = (
    "merchant-onboarding-complete-field-catalog.md",
    "jpt-x-skill-source: <skill_source>",
    "jpt-x-skill-huifu_id: <data.huifu_id>",
    "Java",
    "PHP",
    "merchant-onboarding-external-resources.md",
    "外部资料提示",
)
ATOMIC_CONTRACT_TERMS = {
    "merchant-onboarding-enterprise.md": ("sign:String(2048) Y", "data.audit_status", "`Y/N/F`", "SDK 兼容性告警", "不单独阻断", "不得询问客户", "成功 ACK", "`data.async_return_url:String(120) N`", "禁止使用 `notify_url`"),
    "merchant-onboarding-individual.md": ("sign:String(512) N", "data.audit_status", "`Y/N/F`", "SDK 兼容性告警", "不单独阻断", "不得询问客户", "成功 ACK", "`data.async_return_url:String(120) N`", "禁止使用 `notify_url`"),
    "merchant-onboarding-business-open.md": (
        "reg_result_list[].business_stat",
        "zl_async_info.apply_state",
        "agreement_info_list[].con_stat",
        "`data.online_flag/quick_flag/withhold_flag`",
        "仅字符串 `Y/N`",
        "默认 `2`",
        "目前仅支持企业商户",
        "`7011/7296/7512`",
        "不得统一填 `1`",
    ),
    "merchant-onboarding-image-upload.md": ("发送空的 `jpt-x-skill-huifu_id`", "SDK 兼容性提示", "不单独阻断", "不得询问客户", "DGTools.request_post", "file_url", "顶层 `file`", "不支持填写“企业商户进件”或“个人商户进件”接口返回的用户号"),
    "merchant-onboarding-detail-query.md": ("req_seq_id:String(32)", "req_date:String(8)", "huifu_id:String(18)", "`1=开通`、`0=未开通`、空=未配置", "禁止把查询响应直接复制为开通请求", "`service_phone` 标为 `String(11)`"),
    "merchant-onboarding-application-status-query.md": ("data.bank_card_conf_status:String(1)", "data.bind_card_status:String(1)", "data.cash_status:String(1)", "data.settle_status:String(1)", "data.union_conf_status:String(1)", "data.out_order_funds_status:String(1)", "`P=处理中`、`S=成功`、`F=失败`", "data.wx_zl_config.apply_state:String(32)", "data.ali_zl_config[].apply_status:String(1)", "data.agreement_info_list[].con_stat:String(2)", "`wx_config_list[].config_type`", "页面内部不一致"),
}
FORBIDDEN = (
    "| 逐业务通知 `business_stat` |",
    "| 申请状态查询 `data.ali_zl_config[].apply_state` |",
    "dg_sdk.request_post",
    "业务开通请求 `data.online_flag/quick_flag/withhold_flag` | `String(1) N`，仅 `1/0`",
)

TOP_LEVEL_FIELDS = {
    "enterprise": (
        "### 企业进件 `data`",
        "### 个人进件 `data`",
        "req_seq_id req_date upper_huifu_id reg_name short_name receipt_name mer_en_name ent_type mcc busi_type scene_type license_pic license_code license_type license_validity_type license_begin_date license_end_date found_date reg_capital business_scope reg_prov_id reg_area_id reg_district_id reg_detail prov_id area_id district_id detail_addr legal_name legal_cert_type legal_cert_no legal_cert_validity_type legal_cert_begin_date legal_cert_end_date legal_mobile_no legal_addr legal_cert_back_pic legal_cert_front_pic beneficiary_info contact_name contact_mobile_no contact_email sms_send_flag login_name service_phone reg_acct_pic card_info settle_config settle_card_front_pic settle_cert_back_pic settle_cert_front_pic auth_entrust_pic cash_config head_office_flag use_head_info_flag head_huifu_id mer_url mer_icp store_header_pic store_indoor_pic store_cashier_desk_pic ext_mer_id remarks async_return_url elec_acct_config share_holder_info_list extended_material_list activated_products",
    ),
    "individual": (
        "### 个人进件 `data`",
        "### 业务开通 `data`",
        "req_seq_id req_date upper_huifu_id reg_name short_name mcc scene_type prov_id area_id district_id detail_addr legal_cert_no legal_cert_begin_date legal_cert_validity_type legal_cert_end_date legal_addr legal_cert_back_pic legal_cert_front_pic occupation contact_mobile_no contact_email card_info settle_card_front_pic settle_config cash_config sms_send_flag login_name mer_url mer_icp store_header_pic store_indoor_pic store_cashier_desk_pic ext_mer_id remarks async_return_url head_office_flag head_huifu_id elec_acct_config extended_material_list activated_products",
    ),
    "business": (
        "### 业务开通 `data`",
        "### 必填 `card_info`",
        "req_seq_id req_date huifu_id upper_huifu_id short_name sign_user_info online_flag quick_flag withhold_flag mer_bus_type out_fee_flag out_fee_huifuid out_fee_acct_type ali_conf_list ali_zl_conf alipay_pre_auth_flag wx_conf_list wx_zl_conf wechatpay_pre_auth_flag union_conf_list bank_card_conf online_fee_conf_list online_pay_fee_conf_list online_busi_type online_media_info_list balance_pay_config out_order_funds_config combine_pay_config hb_fq_fee_config split_conf_info delay_flag forced_delay_flag use_chains_flag extended_material_list agreement_info enter_fee enter_fee_flag online_refund platform_refund support_revoke async_return_url busi_async_return_url recon_resp_addr uni_app_payment_config fund_collection_flag surrogate_config_list large_amt_pay_config half_pay_host_flag agent_recheck_config online_recharge_flag refund_mend_open_flag jxf_conf_info merge_pay_config_info bill_payment_flag withhold_pay_scene recon_resp_sys_id",
    ),
}

CARD_INFO_FIELDS = {
    "enterprise": {
        "card_type": "String(1) Y",
        "card_name": "String(128) Y",
        "card_no": "String(32) Y",
        "prov_id": "String(6) N",
        "area_id": "String(6) Y",
        "branch_code": "String(12) C",
        "cert_type": "String(2) C",
        "cert_no": "String(32) C",
        "cert_validity_type": "String(1) N",
        "cert_begin_date": "String(8) N",
        "cert_end_date": "String(8) C",
        "mp": "String(11) N",
        "is_settle_default": "String(1) N",
    },
    "individual": {
        "card_name": "String(128) Y",
        "card_no": "String(32) Y",
        "prov_id": "String(6) N",
        "area_id": "String(6) Y",
        "bank_code": "String(8) N",
        "cert_type": "String(2) Y",
        "cert_no": "String(32) Y",
        "cert_validity_type": "String(1) Y",
        "cert_begin_date": "String(8) Y",
        "cert_end_date": "String(8) C",
        "mp": "String(11) N",
        "is_settle_default": "String(1) N",
    },
}


def declared_top_level_fields(text: str, start: str, end: str) -> set[str]:
    section = text.split(start, 1)[1].split(end, 1)[0]
    fields: set[str] = set()
    pattern = re.compile(r"`([a-z0-9_/]+)\s+(?:String|Object)(?:\([^)]*\))?\s+[YNC](?:/[YNC])*`")
    for match in pattern.finditer(section):
        fields.update(match.group(1).split("/"))
    return fields


def declared_card_fields(text: str, start: str, end: str) -> dict[str, str]:
    section = text.split(start, 1)[1].split(end, 1)[0]
    fields: dict[str, str] = {}
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = line.split("|")[1:-1]
        if len(cells) < 2:
            continue
        names = re.findall(r"`([a-z][a-z0-9_]*)`", cells[0])
        contracts = re.findall(r"`(String\([^)]*\) [YNC])`", cells[1])
        if len(names) == len(contracts):
            fields.update(zip(names, contracts, strict=True))
    return fields


def main() -> int:
    text = CONTRACT.read_text(encoding="utf-8") if CONTRACT.is_file() else ""
    external_text = EXTERNAL_RESOURCES.read_text(encoding="utf-8") if EXTERNAL_RESOURCES.is_file() else ""
    missing = [f"{section}: {term}" for section, terms in REQUIRED.items() for term in terms if term not in text]
    missing.extend(
        f"merchant-onboarding-external-resources.md: {term}"
        for term in EXTERNAL_RESOURCE_REQUIRED
        if term not in external_text
    )
    forbidden_external_hits = [term for term in EXTERNAL_RESOURCE_FORBIDDEN if term in external_text]
    for section, (start, end, expected_text) in TOP_LEVEL_FIELDS.items():
        expected = set(expected_text.split())
        actual = declared_top_level_fields(text, start, end) if start in text and end in text else set()
        if actual != expected:
            missing.append(f"{section} top-level fields: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    card_sections = {
        "enterprise": ("企业 `data.card_info`", "个人 `data.card_info`"),
        "individual": ("个人 `data.card_info`", "业务开通没有跨能力"),
    }
    for section, (start, end) in card_sections.items():
        actual = declared_card_fields(text, start, end) if start in text and end in text else {}
        if actual != CARD_INFO_FIELDS[section]:
            missing.append(f"{section} card_info: expected={CARD_INFO_FIELDS[section]}, actual={actual}")
    references = CONTRACT.parent
    for name in ATOMIC_PAGES:
        page = references / name
        page_text = page.read_text(encoding="utf-8") if page.is_file() else ""
        missing.extend(f"{name}: {term}" for term in ATOMIC_HEADER_TERMS if term not in page_text)
        missing.extend(f"{name}: {term}" for term in ATOMIC_CONTRACT_TERMS[name] if term not in page_text)
    forbidden_hits = [term for term in FORBIDDEN if term in text]
    if missing or forbidden_hits or forbidden_external_hits:
        print("Merchant-onboarding field-contract validation failed:")
        if missing:
            print("\n".join(missing))
        if forbidden_hits:
            print("Forbidden stale contracts:\n" + "\n".join(forbidden_hits))
        if forbidden_external_hits:
            print("Forbidden stale external-resource paths:\n" + "\n".join(forbidden_external_hits))
        return 1
    print("Merchant-onboarding field-contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
