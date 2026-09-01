#!/usr/bin/env python3
"""Guard the source-backed merchant-onboarding field-contract index."""
from __future__ import annotations

import re
from pathlib import Path

from skill_validation_config import onboarding_source_date, onboarding_source_dir


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-field-contracts.md"
EXTERNAL_RESOURCES = ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-external-resources.md"
CATALOG = ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md"
HEADER_POLICY = ROOT / "huifu-merchant-onboarding/references/shared-request-header-policy.md"
ONBOARDING_SKILL = ROOT / "huifu-merchant-onboarding/SKILL.md"
OFFICIAL_SOURCES = onboarding_source_dir()
SOURCE_DATE_FILES = {
    "enterprise": "enterprise.md",
    "individual": "individual.md",
    "business_open": "business-open.md",
    "detail_query": "detail-query.md",
    "status_query": "status-query.md",
    "business_open_modify": "business-open-modify.md",
    "basic_info_modify": "basic-info-modify.md",
    "rate_query": "rate-query.md",
    "status_change": "status-change.md",
    "sms_send": "sms-send.md",
    "multifee_config": "multifee-config.md",
    "multifee_query": "multifee-query.md",
}

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
    "response.data.wx_fee_rate_list[].pay_scene",
    "request.data.material_card_info.prov_id/area_id",
    "request.data.material_card_info.branch_code",
    "十三个接口中的十二个 Markdown JSON 接口顶层 `sign`（不含图片上传）",
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
        "huifu_id String(18) Y",
        "upper_huifu_id String(18) C",
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
    "business-modify": ("商户业务开通修改", "req_seq_id String(32) Y", "huifu_id String(18) Y", "51 组嵌套配置", "async.business.ord_id", "async.business.reg_result_list[]", "`josnArray`", "禁止采用该示例"),
    "basic-modify": ("商户基本信息修改", "upper_huifu_id String(18) C", "资料对象和条件", "审核异步", "基本信息修改 `data.card_info.area_id`", "`String(8) Y`"),
    "rate-query": ("商户费率信息查询", "fee_rate_type String N", "响应 `huifu_id:String(18) Y`", "[官方文档口径冲突]", "没有专属 Request 类"),
    "status-change": ("商户状态变更", "upd_status_reason String(512) Y", "官方多行注释中的 `file_list` 已废弃", "仅字符串 `1/0`"),
    "sms-send": ("商户短信发送", "verify_type String Y", "phone/operation_type/verify_code/elec_acct_sign_seq_id", "C 条件"),
    "multifee-config": (
        "商户多费率配置",
        "req_seq_id/req_date/huifu_id",
        "wx_conf_list/ali_conf_list",
        "String(JSON Array)",
        "响应 `conf_list:String N`",
        "内部对象/数组编码未说明",
        "旧 `T=微信` 冲突已关闭",
    ),
    "multifee-query": (
        "商户多费率配置查询",
        "fee_sign:String(32) N",
        "响应 `conf_list:String N`",
        "官网没有说明省略后的精确返回范围",
        "不能沿用旧版单 Object 假设",
    ),
    "callbacks": ("reg_result_list[].business_stat", "zl_async_info.apply_state", "async.agreement.agreement_info_list.con_stat", "没有 `Array/jsonArray`", "ord_id:String(44)", "RECV_ORD_ID_", "[需要官方确认]", "逐业务通知外层包装待官方样本确认"),
    "headers": ("jpt-x-skill-source: <skill_source>", "Java、PHP、Python SDK 主链路", "hfms/1.0.2", "hfps/1.3.5;hfms/1.0.2", "其他 SDK 内部请求头由 SDK 自行处理"),
    "same-leaf-paths": (
        "不得按叶字段名去重",
        "request.data.prov_id",
        "request.data.area_id",
        "request.data.card_info.prov_id",
        "request.data.card_info.area_id",
        "request.data.elec_acct_config.elec_card_list[].prov_id",
        "request.data.elec_acct_config.elec_card_list[].area_id",
        "不能跨接口复用长度",
    ),
    "java-security": ("十一个已有专属 Request 类的 JSON 接口", "公共 `AbstractRequest`", "`BasePay.debug` 默认为 `true`", "BasePay.debug = false;", "任何 SDK 请求之前", "不得在并发请求中临时切换", "保留请求签名和响应验签", "图片 `file_url` 走 `BasePayClient.request(request, true)`", "本地文件走 `BasePayClient.upload(request, file)`", "均保留请求签名但跳过响应验签"),
    "source-refresh": (
        onboarding_source_date(),
        "official-service-source-index.md",
        "允许增量的机器门禁保存在维护仓库",
        "upper_huifu_id",
        "scene_type",
        "material_card_info",
        "activated_products",
        "01=一体化收款产品",
        "37个目录节点的说明单元为空",
        "当前十三页共有58个叶字段的长度单元为空",
        "sys_id",
        "渠道商",
        "总部商户",
    ),
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
    "Java",
    "PHP",
    "merchant-onboarding-external-resources.md",
    "外部资料提示",
)
ATOMIC_CONTRACT_TERMS = {
    "merchant-onboarding-enterprise.md": ("sign:String(2048) Y", "data.audit_status", "`Y/N/F`", "企业基础进件请求没有 `data.huifu_id`", "按官网字段合同生成", "成功 ACK", "`data.async_return_url:String(120) N`", "禁止使用 `notify_url`", "`data.prov_id/area_id`", "`data.card_info.prov_id/area_id`", "`data.material_card_info.prov_id/area_id`", "`data.material_card_info:String(JSON Object) N`", "以说明列“jsonObject字符串”为 wire 依据", "不得发送普通嵌套 Object", "不能按叶字段名合并", "`String(64) C`", "`scene_type` 含线下场景时必填"),
    "merchant-onboarding-individual.md": ("sign:String(512) N", "data.audit_status", "`Y/N/F`", "个人基础进件请求没有 `data.huifu_id`", "按官网字段合同生成", "成功 ACK", "`data.async_return_url:String(120) N`", "禁止使用 `notify_url`", "`data.prov_id/area_id`", "`data.card_info.prov_id/area_id`", "不得按 `prov_id/area_id` 叶字段名去重", "`String(64) C`", "`scene_type` 含线下场景时必填"),
    "merchant-onboarding-business-open.md": (
        "async.business.reg_result_list[].business_stat",
        "async.business.zl_async_info.apply_state",
        "async.agreement.agreement_info_list.con_stat",
        "`data.online_flag/quick_flag/withhold_flag`",
        "仅字符串 `Y/N`",
        "默认 `2`",
        "目前仅支持企业商户",
        "`7011/7296/7512`",
        "不得统一填 `1`",
    ),
    "merchant-onboarding-image-upload.md": (
        "当前锁定 SDK 中，只有 Java",
        "BasePayClient.request(request, true)",
        "BasePayClient.upload(request, new File",
        "PHP / Python 受控降级",
        "DGTools.request_post",
        "受控通用 POST",
        "multipart/form-data",
        "`sys_id`、`product_id`、`data`、`sign`",
        "`need_sign=True`",
        "file_url",
        "顶层 `file`",
        "不支持填写企业/个人用户开户返回的用户号",
    ),
    "merchant-onboarding-detail-query.md": ("567 个具名路径", "req_seq_id:String(32)", "req_date:String(8)", "huifu_id:String(18)", "`1=开通`、`0=未开通`、空=未配置", "禁止把查询响应直接复制为开通请求", "`service_phone` 标为 `String(11)`", "`response.data.material_card_info:String(JSON Object) N`", "以说明列“jsonObject字符串”为 wire 依据", "`card_type/card_name/card_no/prov_id/area_id/branch_code`"),
    "merchant-onboarding-application-status-query.md": ("data.bank_card_conf_status:String(1)", "data.bind_card_status:String(1)", "data.cash_status:String(1)", "data.settle_status:String(1)", "data.union_conf_status:String(1)", "data.out_order_funds_status:String(1)", "`P=处理中`、`S=成功`、`F=失败`", "data.wx_zl_config.apply_state:String(32)", "data.ali_zl_config[].apply_status:String(1)", "data.agreement_info_list[].con_stat:String(2)", "`wx_config_list[].config_type`", "页面内部不一致"),
}
NEW_ATOMIC_CONTRACT_TERMS = {
    "merchant-onboarding-business-open-modify.md": (
        "444 个节点",
        "请求 382、同步响应 6、异步通知 56",
        "V2MerchantBusiModifyRequest",
        "async.business.ord_id:String(44)",
        "async.business.reg_result_list[]",
        "async.agreement.agreement_info_list.con_stat",
        "[官方文档口径冲突]",
        "RECV_ORD_ID_",
    ),
    "merchant-onboarding-basic-info-modify.md": (
        "199 个节点",
        "请求 164、同步响应 7、异步通知 28",
        "V2MerchantBasicdataModifyRequest",
        "async.agreement.agreement_info_list.con_stat",
        "不能把同步响应成功解释为",
        "`data.prov_id/area_id`",
        "`data.card_info.prov_id/area_id`",
        "`String(8) Y`",
        "`01=一体化收款产品`",
    ),
    "merchant-onboarding-rate-query.md": (
        "35 个节点",
        "请求 8、同步响应 27、无异步通知",
        "[官方文档口径冲突]",
        "request.data.huifu_id",
        "response.data.huifu_id",
        "32/18",
        "未找到 `/v2/merchant/fee-rate/query` 的专属 Request 类",
    ),
    "merchant-onboarding-status-change.md": (
        "14 个节点",
        "请求 9、同步响应 5、无异步通知",
        "V2MerchantBusiModifyBusistatusRequest",
        "禁止生成 `request.data.file_list`",
    ),
    "merchant-onboarding-sms-send.md": (
        "20 个节点",
        "请求 12、同步响应 8、无异步通知",
        "V2MerchantBasicdataSmsSendRequest",
        "data.verify_code:String(6) C",
    ),
    "merchant-onboarding-multifee-config.md": (
        "27 个节点",
        "请求 15、同步响应 12、无异步通知",
        "同一商户号当天唯一",
        "北京时间 `yyyyMMdd`",
        "直属商户 ID",
        "V2MerchantBusiMultifeeConfigRequest",
        "/v2/merchant/busi/multiFee/config",
        "wx_conf_list:String N",
        "ali_conf_list:String N",
        "data.conf_list:String N",
        "官网未说明该 String 子表是 JSON Object 还是 JSON Array",
        "旧 T/W 冲突已关闭",
        "扩展映射必须拒绝 `req_seq_id`、`req_date`、`huifu_id`",
    ),
    "merchant-onboarding-multifee-query.md": (
        "17个节点",
        "请求8、同步响应9、无异步通知",
        "同一商户号当天唯一",
        "北京时间 `yyyyMMdd`",
        "直属商户 ID",
        "V2MerchantBusiMultifeeQueryRequest",
        "/v2/merchant/busi/multiFee/query",
        "data.fee_sign:String(32) N",
        "data.conf_list:String N",
        "未说明 String 子表是对象还是数组",
        "不得自行承诺“返回全部配置”",
        "扩展映射必须拒绝 `req_seq_id`、`req_date`、`huifu_id`",
    ),
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
        "req_seq_id req_date upper_huifu_id reg_name short_name receipt_name mer_en_name ent_type mcc busi_type scene_type license_pic license_code license_type license_validity_type license_begin_date license_end_date found_date reg_capital business_scope reg_prov_id reg_area_id reg_district_id reg_detail prov_id area_id district_id detail_addr legal_name legal_cert_type legal_cert_no legal_cert_validity_type legal_cert_begin_date legal_cert_end_date legal_mobile_no legal_addr legal_cert_back_pic legal_cert_front_pic beneficiary_info contact_name contact_mobile_no contact_email sms_send_flag login_name service_phone reg_acct_pic card_info settle_config settle_card_front_pic settle_cert_back_pic settle_cert_front_pic auth_entrust_pic cash_config head_office_flag use_head_info_flag head_huifu_id mer_url mer_icp store_header_pic store_indoor_pic store_cashier_desk_pic ext_mer_id remarks async_return_url elec_acct_config share_holder_info_list extended_material_list activated_products material_card_info",
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


def locked_source_update_dates() -> dict[str, str]:
    dates: dict[str, str] = {}
    for key, filename in SOURCE_DATE_FILES.items():
        source = OFFICIAL_SOURCES / filename
        match = re.search(
            r"最近更新时间：(\d{4})\.(\d{1,2})\.(\d{1,2})",
            source.read_text(encoding="utf-8"),
        )
        if match is None:
            raise ValueError(f"{filename}: locked source update date is missing")
        year, month, day = match.groups()
        dates[key] = f"{year}-{int(month):02d}-{int(day):02d}"
    return dates


def main() -> int:
    text = CONTRACT.read_text(encoding="utf-8") if CONTRACT.is_file() else ""
    external_text = EXTERNAL_RESOURCES.read_text(encoding="utf-8") if EXTERNAL_RESOURCES.is_file() else ""
    catalog_text = CATALOG.read_text(encoding="utf-8") if CATALOG.is_file() else ""
    header_text = HEADER_POLICY.read_text(encoding="utf-8") if HEADER_POLICY.is_file() else ""
    skill_text = ONBOARDING_SKILL.read_text(encoding="utf-8") if ONBOARDING_SKILL.is_file() else ""
    missing = [f"{section}: {term}" for section, terms in REQUIRED.items() for term in terms if term not in text]
    for term in (
        "仅 `huifu-merchant-onboarding 1.0.2`",
        "`hfms/1.0.2`",
        "`hfps/1.3.5;hfms/1.0.2`",
        "顺序固定为支付、进件",
        "英文分号且不加空格",
        "显式提供经确认的合同值时原样透传",
    ):
        if term not in header_text:
            missing.append(f"shared-request-header-policy.md: {term}")
    for term in (
        "`request.data.prov_id/area_id`",
        "`request.data.card_info.prov_id/area_id`",
        "`request.data.material_card_info.prov_id/area_id`",
        "request/response wire 均按 String(JSON Object)",
        "1,261 个请求、742 个同步响应和 180 个通知节点",
        "37个字段说明为空",
        "58个 String 标量叶字段长度为空",
        "`hfms/1.0.2`",
        "`hfps/1.3.5;hfms/1.0.2`",
    ):
        if term not in skill_text:
            missing.append(f"SKILL.md: {term}")
    catalog_path_counts = {
        "| `request.data.prov_id` |": 3,
        "| `request.data.area_id` |": 3,
        "| `request.data.card_info.prov_id` |": 3,
        "| `request.data.card_info.area_id` |": 3,
        "| `request.data.material_card_info.prov_id` |": 1,
        "| `request.data.material_card_info.area_id` |": 1,
        "| `response.data.material_card_info.prov_id` |": 1,
        "| `response.data.material_card_info.area_id` |": 1,
    }
    for row_prefix, expected_count in catalog_path_counts.items():
        actual_count = catalog_text.count(row_prefix)
        if actual_count != expected_count:
            missing.append(
                f"complete catalog duplicate-path guard: {row_prefix} "
                f"expected={expected_count}, actual={actual_count}"
            )
    for term in (
        "不得按叶字段名去重",
        "`request.data.prov_id/area_id` 是经营省市",
        "`request.data.card_info.prov_id/area_id` 是结算卡省市",
        "`request.data.material_card_info.prov_id/area_id`",
        "基本信息修改的 `card_info.area_id` 长度为 `8`",
        "企业/个人进件对应路径长度为 `6`",
        "`response.data.material_card_info.prov_id/area_id`",
        "四组字段均不得合并",
    ):
        if term not in catalog_text:
            missing.append(f"complete catalog same-leaf guidance: {term}")
    if (
        "| `request.data.card_info.area_id` | 银行所在市 | `String` | `8` | `Y` |"
        not in catalog_text
    ):
        missing.append("complete catalog: basic-info-modify card_info.area_id String(8) Y")
    activated_products_row = (
        "| `request.data.activated_products` | 产品大类 | `String` | `—` | `N` | "
        "01：一体化收款产品，02：账户与资金产品，03：业财数通产品；"
        "不传为空 示例值：01,02,03 |"
    )
    if catalog_text.count(activated_products_row) != 3:
        missing.append(
            "complete catalog: three request.data.activated_products descriptions "
            "must preserve the 01/02/03 live-source wording"
        )
    catalog_rows: list[tuple[str, str, str, str, str, str]] = []
    interface = ""
    surface = ""
    for line in catalog_text.splitlines():
        if line.startswith("## "):
            interface = line[3:].strip()
            surface = ""
        elif line.startswith("### "):
            surface = line[4:].strip()
        elif line.startswith("| `"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 6:
                catalog_rows.append(
                    (
                        interface,
                        surface,
                        cells[0].strip("`"),
                        cells[2].strip("`"),
                        cells[3].strip("`"),
                        " | ".join(cells[5:]),
                    )
                )
    blank_descriptions = [row for row in catalog_rows if row[5] == "—"]
    string_leaf_blank_lengths = [
        row
        for row in catalog_rows
        if row[3] == "String"
        and row[4] == "—"
        and not any(
            child[0] == row[0]
            and child[2].startswith(row[2] + ".")
            for child in catalog_rows
        )
    ]
    if len(blank_descriptions) != 37:
        missing.append(
            "complete catalog official blank descriptions: "
            f"expected=37, actual={len(blank_descriptions)}"
        )
    if len(string_leaf_blank_lengths) != 58:
        missing.append(
            "complete catalog official blank String leaf lengths: "
            f"expected=58, actual={len(string_leaf_blank_lengths)}"
        )
    try:
        source_dates = locked_source_update_dates()
    except (OSError, ValueError) as exc:
        missing.append(str(exc))
    else:
        expected_date_clauses = (
            (
                "refreshed source dates",
                "来源快照核验日期：`2026-08-31`",
                source_dates["enterprise"] == "2026-08-26"
                and source_dates["individual"] == "2026-08-18"
                and source_dates["basic_info_modify"] == "2026-08-07",
            ),
            (
                "description-only refresh",
                "相对上一快照新增29、删除1、修改45",
                True,
            ),
            (
                "multifee source date",
                "`wx_conf_list/ali_conf_list:String N` 均按 String(JSON Array) 发送",
                source_dates["multifee_config"] == "2026-08-28",
            ),
            (
                "multifee query source date",
                "可选 `fee_sign:String(32) N` 只传真实标识",
                source_dates["multifee_query"] == "2026-08-28",
            ),
        )
        missing.extend(
            f"{label}: {clause}"
            for label, clause, compatible in expected_date_clauses
            if not compatible or clause not in text
        )
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
    for name, terms in NEW_ATOMIC_CONTRACT_TERMS.items():
        page = references / name
        page_text = page.read_text(encoding="utf-8") if page.is_file() else ""
        missing.extend(
            f"{name}: merchant-onboarding-complete-field-catalog.md"
            for _ in (0,)
            if "merchant-onboarding-complete-field-catalog.md" not in page_text
        )
        missing.extend(f"{name}: {term}" for term in terms if term not in page_text)
        missing.extend(
            f"{name}: {term}"
            for term in (
                "## 公共请求头",
                "`jpt-x-skill-source: <skill_source>`",
                "`hfms/1.0.2`",
                "`hfps/1.3.5;hfms/1.0.2`",
            )
            if term not in page_text
        )
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
