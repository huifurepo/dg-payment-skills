#!/usr/bin/env python3
"""Independently validate the twelve onboarding-extension source contracts.

The catalog generator is intentionally not imported. This validator reuses the
separately implemented source/catalog parsers from the user-onboarding audit,
binds extension-specific root surfaces itself, and compares every field
property as well as aggregate counts and non-wire tables.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import validate_user_onboarding_source_contract as independent
from skill_validation_config import ONBOARDING_EXTENSION_SOURCE_LOCK, onboarding_extension_source_dir
from validation_runtime import require_assertions_enabled


require_assertions_enabled()

ROOT = Path(__file__).resolve().parent.parent
LOCK = ONBOARDING_EXTENSION_SOURCE_LOCK
CATALOG = ROOT / "huifu-merchant-onboarding/references/onboarding-extension-complete-field-catalog.md"
COMBINED = ROOT / "maintainer-contracts/merchant-onboarding-1.0.3-source-lock-2026-09-22.json"
REFRESH = ROOT / "maintainer-contracts/api-refresh-onboarding-online-review-2026-09-22.json"
MANIFEST = ROOT / "skills-manifest.json"
REFERENCES = ROOT / "huifu-merchant-onboarding/references"
EXTERNAL_RESOURCES = REFERENCES / "onboarding-extension-external-resources.md"

EXPECTED = {
    "contract_resend": ("POST /v2/agreement/elect/signurl/resend", 13, 9, 4, 0),
    "contract_list_query": ("POST /v2/agreement/apply/list", 40, 16, 24, 0),
    "contract_reject": ("POST /v2/agreement/elect/rejectsign", 12, 8, 4, 0),
    "lower_merchant_permission": ("POST /v2/merchant/busi/head/config", 141, 132, 9, 0),
    "unified_web_onboarding": ("POST /v2/merchant/url/forward", 59, 17, 8, 34),
    "unified_web_query": ("POST /v2/merchant/busi/status/query", 51, 8, 43, 0),
    "wechat_config": ("POST /v2/merchant/busi/config", 31, 16, 4, 11),
    "wechat_config_query": ("POST /v2/merchant/busi/config/query", 32, 8, 24, 0),
    "wechat_realname": ("POST /v2/merchant/busi/realname", 51, 45, 6, 0),
    "wechat_realname_query": ("POST /v2/merchant/busi/realname/query", 22, 9, 13, 0),
    "alipay_realname": ("POST /v2/merchant/busi/ali/realname/apply", 69, 63, 6, 0),
    "alipay_realname_query": ("POST /v2/merchant/busi/ali/realname/query", 25, 9, 16, 0),
}

COMMON_SURFACES = (
    ("请求信封", "request"),
    ("响应信封", "response"),
    ("请求 data", "request.data"),
    ("同步响应 data", "response.data"),
)
CONTRACT_SURFACES = (
    ("请求信封", "request"),
    ("请求 data", "request.data"),
    ("响应信封", "response"),
    ("同步响应 data", "response.data"),
)
SURFACES = {
    "contract_resend": CONTRACT_SURFACES,
    "contract_list_query": CONTRACT_SURFACES,
    "contract_reject": CONTRACT_SURFACES,
    "lower_merchant_permission": COMMON_SURFACES,
    "unified_web_onboarding": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("异步通知信封", "async"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("审核异步 data", "async.audit.data"),
        ("业务异步 data", "async.business.data"),
    ),
    "unified_web_query": COMMON_SURFACES,
    "wechat_config": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("异步通知 data", "async.data"),
    ),
    "wechat_config_query": COMMON_SURFACES,
    "wechat_realname": COMMON_SURFACES,
    "wechat_realname_query": COMMON_SURFACES,
    "alipay_realname": COMMON_SURFACES,
    "alipay_realname_query": COMMON_SURFACES,
}

ATOMIC_REFERENCES = {
    "contract_resend": "onboarding-electronic-contract-resend.md",
    "contract_list_query": "onboarding-electronic-contract-list-query.md",
    "contract_reject": "onboarding-electronic-contract-reject.md",
    "lower_merchant_permission": "merchant-onboarding-lower-merchant-permission.md",
    "unified_web_onboarding": "merchant-onboarding-unified-web.md",
    "unified_web_query": "merchant-onboarding-unified-web-query.md",
    "wechat_config": "merchant-onboarding-wechat-config.md",
    "wechat_config_query": "merchant-onboarding-wechat-config-query.md",
    "wechat_realname": "merchant-onboarding-wechat-realname.md",
    "wechat_realname_query": "merchant-onboarding-wechat-realname-query.md",
    "alipay_realname": "merchant-onboarding-alipay-realname.md",
    "alipay_realname_query": "merchant-onboarding-alipay-realname-query.md",
}

SDK_CLASSES = (
    "V2InvoiceContractrepeatRequest",
    "V2InvoiceQueryecmsapplylistRequest",
    "V2InvoiceRejectsignRequest",
    "V2MerchantBusiHeadConfigRequest",
    "V2MerchantUrlForwardRequest",
    "V2MerchantBusiStatusQueryRequest",
    "V2MerchantBusiConfigRequest",
    "V2MerchantBusiConfigQueryRequest",
    "V2MerchantBusiRealnameRequest",
    "V2MerchantBusiRealnameQueryRequest",
    "V2MerchantBusiAliRealnameApplyRequest",
    "V2MerchantBusiAliRealnameQueryRequest",
)

APPLYMENT_STATES = (
    ("APPLYMENT_STATE_EDITTING", "编辑中", "可能在提交申请时发生错误导致，可用同一个业务申请编号重新提交"),
    ("APPLYMENT_STATE_WAITTING_FOR_AUDIT", "审核中", "请耐心等待1~2个工作日，微信支付将会完成审核"),
    ("APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT", "待确认联系信息", "请扫描微信支付返回的小程序码确认联系信息(此过程可修改超级管理员手机号)"),
    ("APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON", "待账户验证", "请扫描微信支付返回的小程序码在小程序端完成账户验证"),
    ("APPLYMENT_STATE_PASSED", "审核通过", "请扫描微信支付返回的小程序码在小程序端完成授权流程"),
    ("APPLYMENT_STATE_REJECTED", "审核驳回", "请按照驳回原因修改申请资料，并更换业务申请编码，重新提交申请"),
    ("APPLYMENT_STATE_FREEZED", "已冻结", "可能是该主体已完成过入驻，请查看驳回原因，并通知驳回原因中指定的联系人扫描微信支付返回的小程序码在小程序端完成授权流程"),
    ("APPLYMENT_STATE_CANCELED", "已作废", "表示申请单已被撤销，无需再对其进行操作"),
    ("APPLYMENT_STATE_NOAPPLY", "未申请", ""),
)

RecordKey = tuple[str, str, str]
RecordValue = tuple[str, str, str, str, str, str, str, str]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direction(path: str) -> str:
    if path.startswith("request."):
        return "request"
    if path.startswith("response."):
        return "response"
    return "callback"


def expected_records(
    lock: dict[str, object], source_dir: Path
) -> tuple[dict[RecordKey, RecordValue], dict[str, tuple[int, int]]]:
    records: dict[RecordKey, RecordValue] = {}
    table_counts: dict[str, tuple[int, int]] = {}
    for source in lock["sources"]:
        text = (source_dir / source["filename"]).read_text(encoding="utf-8-sig")
        roots, nested = independent.source_tables(text, source["url"])
        surfaces = SURFACES[source["key"]]
        assert len(roots) == len(surfaces), (
            f"{source['key']}: expected {len(surfaces)} roots, found {len(roots)}"
        )
        used: set[str] = set()
        for (surface, prefix), fields in zip(surfaces, roots, strict=True):
            for path, field in independent.flatten(fields, nested, prefix, used):
                key = (source["title"], surface, path)
                assert key not in records, f"duplicate source field: {key}"
                records[key] = (
                    direction(path),
                    field.label,
                    field.kind,
                    field.length,
                    field.required,
                    field.description,
                    source["url"],
                    source["sha256"],
                )
        assert used == set(nested), (
            f"{source['key']}: unreachable extend tables "
            f"{sorted(set(nested) - used)}"
        )
        table_counts[source["key"]] = (len(roots), len(nested))
    return records, table_counts


def actual_records(lock: dict[str, object]) -> dict[RecordKey, RecordValue]:
    source_by_title = {item["title"]: item for item in lock["sources"]}
    records: dict[RecordKey, RecordValue] = {}
    metadata: dict[str, dict[str, str]] = {}
    headings: list[str] = []
    title: str | None = None
    surface: str | None = None
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            candidate = line[3:].strip()
            headings.append(candidate)
            title = candidate if candidate in source_by_title else None
            if title:
                metadata[title] = {}
            surface = None
            continue
        if title and line.startswith("- 原始地址：<") and line.endswith(">"):
            metadata[title]["url"] = line.removeprefix("- 原始地址：<").removesuffix(">")
            continue
        if title and line.startswith("- SHA-256：`") and line.endswith("`"):
            metadata[title]["sha256"] = line.removeprefix("- SHA-256：`").removesuffix("`")
            continue
        if title and line.startswith("### "):
            surface = line[4:].strip()
            continue
        if not title or not surface or not line.startswith("| `"):
            continue
        cells = independent.split_catalog_row(line)
        assert len(cells) == 6, f"malformed catalog row: {line}"
        path = cells[0].strip("`")
        assert set(metadata[title]) == {"url", "sha256"}
        key = (title, surface, path)
        assert key not in records, f"duplicate catalog field: {key}"
        records[key] = (
            direction(path),
            cells[1],
            cells[2].strip("`"),
            cells[3].strip("`"),
            cells[4].strip("`"),
            cells[5],
            metadata[title]["url"],
            metadata[title]["sha256"],
        )
    assert headings == [
        "目录",
        "使用规则",
        "生成覆盖摘要",
        *(source["title"] for source in lock["sources"]),
    ]
    assert set(metadata) == set(source_by_title)
    return records


def structure(records: dict[RecordKey, RecordValue]) -> dict[RecordKey, str]:
    result: dict[RecordKey, str] = {}
    keys = list(records)
    for key in keys:
        title, _surface, path = key
        normalized = path.replace("[]", "")
        result[key] = (
            "parent"
            if any(
                other_title == title
                and other_path.replace("[]", "").startswith(normalized + ".")
                for other_title, _other_surface, other_path in keys
            )
            else "leaf"
        )
    return result


def markdown_tables(text: str) -> list[tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]]:
    """Parse ordinary Markdown tables outside fenced code blocks."""
    lines = independent.visible_lines(text)
    result: list[tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]] = []
    fenced = False
    cursor = 0
    while cursor + 1 < len(lines):
        stripped = lines[cursor].strip()
        if stripped.startswith("```"):
            fenced = not fenced
            cursor += 1
            continue
        if fenced or not stripped.startswith("|"):
            cursor += 1
            continue
        separator = independent.split_source_row(lines[cursor + 1])
        if not separator or not all(
            re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in separator
        ):
            cursor += 1
            continue
        header = tuple(
            independent.normalize(cell).strip("* ")
            for cell in independent.split_source_row(stripped)
        )
        rows: list[tuple[str, ...]] = []
        cursor += 2
        while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
            row, cursor = independent.consume_row(lines, cursor)
            rows.append(
                tuple(
                    independent.normalize(cell)
                    for cell in independent.split_source_row(row)
                )
            )
        result.append((header, tuple(rows)))
    return result


def validate_non_contract_tables(lock: dict[str, object], source_dir: Path) -> int:
    non_contract: list[tuple[str, tuple[str, ...], tuple[tuple[str, ...], ...]]] = []
    for source in lock["sources"]:
        text = (source_dir / source["filename"]).read_text(encoding="utf-8-sig")
        for header, rows in markdown_tables(text):
            rendered_header = "| " + " | ".join(header) + " |"
            if independent.source_table_columns(rendered_header) is None:
                non_contract.append((source["key"], header, rows))
    assert non_contract == [
        ("wechat_realname_query", ("参数值", "中文名", "说明"), APPLYMENT_STATES)
    ], f"non-contract table set changed: {non_contract}"

    required_texts = (
        REFERENCES / "merchant-onboarding-wechat-realname-query.md",
        REFERENCES / "onboarding-extension-field-contracts.md",
        REFERENCES / "onboarding-extension-canonical-regression-prompts.md",
    )
    combined_text = "\n".join(path.read_text(encoding="utf-8") for path in required_texts)
    master = (ROOT / "scripts/huifu-payment-test-prompts.json").read_text(encoding="utf-8")
    for state, label, _description in APPLYMENT_STATES:
        assert state in combined_text and state in master, f"missing state evidence: {state}"
        assert label in combined_text, f"missing state meaning: {state} {label}"
    for term in ("authorize_stat", "1=授权成功", "0=授权失败"):
        assert term in combined_text, f"missing independent authorization contract: {term}"
    return len(non_contract)


def active_markdown_urls(text: str) -> set[str]:
    visible = "\n".join(independent.visible_lines(text))
    return {
        target
        for _label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", visible)
        if target.startswith(("http://", "https://"))
    }


def validate_external_resources(lock: dict[str, object], source_dir: Path) -> int:
    source_urls: set[str] = set()
    for source in lock["sources"]:
        source_urls.update(
            active_markdown_urls(
                (source_dir / source["filename"]).read_text(encoding="utf-8-sig")
            )
        )
    index = EXTERNAL_RESOURCES.read_text(encoding="utf-8")
    missing = sorted(url for url in source_urls if url not in index)
    assert not missing, f"external resource index omits active official links: {missing}"
    for term in (
        "完整字段路径",
        "第三方微信资料不是汇付字段合同",
        "HTTP 200",
        "只证明当时可访问",
        "[需要人工访问/确认]",
    ):
        assert term in index, f"external resource policy missing: {term}"
    return len(source_urls)


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert set(lock) == {
        "schema_version",
        "source_date",
        "source_snapshot_id",
        "introduced_in_skill_version",
        "previous_source_lock",
        "verified_at",
        "sources",
        "totals",
        "api_refresh",
    }
    assert lock["schema_version"] == 1
    assert lock["source_date"] == lock["source_snapshot_id"] == "2026-09-22"
    assert lock["introduced_in_skill_version"] == "1.0.3"
    previous_path = ROOT / "maintainer-contracts/onboarding-extension-source-lock-2026-09-15.json"
    previous_sha = "d99e2f56ccd92f420c5fc91ca4042ca461f1d1be2fc92a03ad06d6d9a78c54ea"
    assert sha256(previous_path) == previous_sha, "historical extension source lock changed"
    assert lock["previous_source_lock"] == {"path": previous_path.relative_to(ROOT).as_posix(), "sha256": previous_sha}
    previous = json.loads(previous_path.read_text(encoding="utf-8"))
    previous_dir = ROOT / "maintainer-contracts/official-sources/onboarding-extension/2026-09-15"
    assert {path.name for path in previous_dir.iterdir() if path.is_file()} == {source["filename"] for source in previous["sources"]}
    for source in previous["sources"]:
        assert sha256(previous_dir / source["filename"]) == source["sha256"]
    assert len(lock["sources"]) == len(EXPECTED) == len(SURFACES) == 12
    assert [item["key"] for item in lock["sources"]] == list(EXPECTED)

    source_dir = onboarding_extension_source_dir()
    assert source_dir == ROOT / "maintainer-contracts/official-sources/onboarding-extension/2026-09-22"
    assert {path.name for path in source_dir.iterdir() if path.is_file()} == {
        item["filename"] for item in lock["sources"]
    }
    for item in lock["sources"]:
        endpoint, fields, request, response, callback = EXPECTED[item["key"]]
        assert item["endpoint"] == endpoint
        assert (
            item["field_count"],
            item["request_fields"],
            item["response_fields"],
            item["callback_fields"],
        ) == (fields, request, response, callback)
        source_path = source_dir / item["filename"]
        assert sha256(source_path) == item["sha256"]
        source_text = source_path.read_text(encoding="utf-8-sig")
        assert "https://api.huifu.com" + endpoint.removeprefix("POST ") in source_text, (
            f"{item['key']}: locked endpoint is not present in official source"
        )
        atomic = (REFERENCES / ATOMIC_REFERENCES[item["key"]]).read_text(encoding="utf-8")
        assert endpoint.removeprefix("POST ") in atomic
        assert item["sha256"] in atomic

    assert lock["totals"] == {
        "fields": 546,
        "request": 340,
        "response": 161,
        "callback": 45,
        "parent": 66,
        "leaf": 480,
        "root_tables": 51,
        "extend_tables": 43,
    }
    refresh_meta = lock["api_refresh"]
    assert refresh_meta["refresh_id"] == "api-refresh-extension-online-review-2026-09-22"
    assert refresh_meta["changed_source_keys"] == [
        "contract_resend", "contract_list_query", "contract_reject", "lower_merchant_permission",
        "unified_web_onboarding", "unified_web_query", "wechat_config", "alipay_realname",
    ]
    assert (refresh_meta["field_paths_added"], refresh_meta["field_paths_removed"], refresh_meta["field_paths_changed"]) == (26, 28, 66)
    assert len(refresh_meta["document_conflicts"]) == 11

    expected, table_counts = expected_records(lock, source_dir)
    actual = actual_records(lock)
    assert set(expected) == set(actual), (
        f"field set mismatch: missing={sorted(set(expected) - set(actual))}, "
        f"extra={sorted(set(actual) - set(expected))}"
    )
    changed = [
        (key, expected[key], actual[key])
        for key in sorted(expected)
        if expected[key] != actual[key]
    ]
    assert not changed, f"field property mismatches: {changed}"

    # Semantic prefixes do not recreate the two envelope tables removed by
    # the new WeChat page. A display-only wrapper is not a wire contract.
    wechat_title = next(source["title"] for source in lock["sources"] if source["key"] == "wechat_config")
    wechat_fields = {key[2]: value for key, value in actual.items() if key[0] == wechat_title}
    assert not {"response.sign", "response.data", "async.resp_code", "async.resp_desc", "async.sign", "async.data"} & set(wechat_fields)
    for name in ("resp_code", "resp_desc", "huifu_id", "apply_no"):
        assert wechat_fields[f"response.data.{name}"][3:5] == ("—", "N")
    assert table_counts["wechat_config"] == (4, 1)

    contract_title = next(source["title"] for source in lock["sources"] if source["key"] == "contract_list_query")
    contract_fields = {key[2]: value for key, value in actual.items() if key[0] == contract_title}
    assert contract_fields["response.data.resp_code"][3] == "8"
    for name in ("total_size", "page_num", "page_size"):
        assert contract_fields[f"response.data.{name}"][2:5] == ("String", "10", "N")
    assert "response.data.result_list[].create_time" in contract_fields
    assert "response.data.result_list[].createTime" not in contract_fields
    assert "若无协议，该字段不返回" in contract_fields["response.data.result_list[]"][5]

    for source in lock["sources"]:
        source_records = {
            key: value for key, value in actual.items() if key[0] == source["title"]
        }
        assert len(source_records) == source["field_count"]
        for name, expected_count in (
            ("request", source["request_fields"]),
            ("response", source["response_fields"]),
            ("callback", source["callback_fields"]),
        ):
            assert sum(value[0] == name for value in source_records.values()) == expected_count
        assert table_counts[source["key"]] == (
            source["root_tables"],
            source["extend_tables"],
        )

    node_structure = structure(actual)
    direction_counts = {
        name: sum(value[0] == name for value in actual.values())
        for name in ("request", "response", "callback")
    }
    structure_counts = {
        name: sum(value == name for value in node_structure.values())
        for name in ("parent", "leaf")
    }
    assert len(actual) == lock["totals"]["fields"]
    assert direction_counts == {
        name: lock["totals"][name] for name in ("request", "response", "callback")
    }
    assert structure_counts == {
        name: lock["totals"][name] for name in ("parent", "leaf")
    }
    assert sum(count[0] for count in table_counts.values()) == lock["totals"]["root_tables"]
    assert sum(count[1] for count in table_counts.values()) == lock["totals"]["extend_tables"]

    contracts = (REFERENCES / "onboarding-extension-field-contracts.md").read_text(encoding="utf-8")
    for term in (
        "page_size",
        "create_time",
        "data.product_id",
        "wx_real_name_list",
        "qrcode_data",
        "微信业务开通类型",
        "微信支付场景",
        "[需要官方确认]",
    ):
        assert term in contracts
    sdk_matrix = (REFERENCES / "onboarding-extension-shared-server-sdk-matrix.md").read_text(encoding="utf-8")
    for class_name in SDK_CLASSES:
        assert class_name in sdk_matrix
    for source_key in ("contract_resend", "contract_list_query", "contract_reject"):
        assert EXPECTED[source_key][0].removeprefix("POST ") in sdk_matrix
    assert "DGTools.request_post" in sdk_matrix and "BasePayClient.request" in sdk_matrix
    assert "三个电子合同路由均未找到专属类" not in sdk_matrix
    assert "仍不允许手写 HTTP" in sdk_matrix
    assert "不得拿来替代新 agreement 接口" in sdk_matrix

    non_contract_tables = validate_non_contract_tables(lock, source_dir)
    active_external_urls = validate_external_resources(lock, source_dir)

    combined = json.loads(COMBINED.read_text(encoding="utf-8"))
    assert combined["version"] == "1.0.3"
    assert combined["totals"] == {"interfaces": 34, "field_paths": 3367}
    assert combined["source_locks"]["onboarding_extension"]["sha256"] == sha256(LOCK)
    assert combined["catalogs"]["extension"]["sha256"] == sha256(CATALOG)

    refresh = json.loads(REFRESH.read_text(encoding="utf-8"))
    assert refresh["source_locks"]["onboarding_1_0_3"]["sha256"] == sha256(COMBINED)
    assert refresh["source_locks"]["onboarding_extension_current"]["sha256"] == sha256(LOCK)
    assert refresh["field_delta"]["combined_total"] == 3367
    assert refresh["cross_skill_review"]["changed"] is False
    assert refresh["cross_skill_review"]["online_sha256"] == refresh["cross_skill_review"]["locked_sha256"]

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["skills"]["huifu-merchant-onboarding"]
    assert manifest["version"] == "1.0.4"
    assert manifest["source_lock"] == COMBINED.relative_to(ROOT).as_posix()
    assert manifest["refresh_contract"] == "maintainer-contracts/api-refresh-onboarding-1.0.4-sdk-2.0.28-2026-09-24.json"
    release = json.loads((ROOT / manifest["refresh_contract"]).read_text(encoding="utf-8"))
    assert release["source_review_id"] == refresh["refresh_id"]
    assert release["source_review"] == {"path": REFRESH.relative_to(ROOT).as_posix(), "sha256": sha256(REFRESH), "refresh_id": refresh["refresh_id"]}
    previous_path = ROOT / "maintainer-contracts/api-refresh-onboarding-1.0.4-2026-09-24.json"
    assert sha256(previous_path) == "1adfb151fb0a35c02bd09f8f9985f62d790426752a9d7ce54af2e4326a352426"
    previous = json.loads(previous_path.read_text(encoding="utf-8"))
    assert release["previous_refresh"] == {"path": previous_path.relative_to(ROOT).as_posix(), "sha256": sha256(previous_path), "refresh_id": previous["refresh_id"]}
    assert previous["previous_refresh"] == release["source_review"]
    assert previous["source_locks"] == refresh["source_locks"]
    sdk_path = ROOT / json.loads(MANIFEST.read_text(encoding="utf-8"))["sdk_source_lock"]
    sdk = json.loads(sdk_path.read_text(encoding="utf-8"))
    assert release["source_locks"] == {**refresh["source_locks"], "local_sdk_current": {"path": sdk_path.relative_to(ROOT).as_posix(), "sha256": sha256(sdk_path)}}
    assert release["sdk_versions"] == {name: item["version"] for name, item in sdk["components"].items()}
    assert release["catalogs"] == refresh["catalogs"]
    print(
        "Independent onboarding-extension contract validated: "
        f"{len(actual)} fields; directions={direction_counts}; "
        f"structure={structure_counts}; non_contract_tables={non_contract_tables}; "
        f"active_external_urls={active_external_urls}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
