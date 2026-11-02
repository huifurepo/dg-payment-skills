#!/usr/bin/env python3
"""Independently verify locked user-onboarding sources against the catalog.

This validator deliberately does not import the catalog generator.  It uses a
separate Markdown row parser and root-table classifier, then compares every
field path and property in addition to aggregate and graph-structure counts.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

from validation_runtime import require_assertions_enabled
from skill_validation_config import USER_ONBOARDING_SOURCE_LOCK


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
LOCK = USER_ONBOARDING_SOURCE_LOCK
SEPTEMBER_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-09-15.json"
PREVIOUS_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-31.json"
HISTORICAL_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock.json"
R1_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r1.json"
R2_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r2.json"
R3_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r3.json"
R4_LOCK = ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r4.json"
CATALOG = (
    ROOT
    / "huifu-merchant-onboarding/references/user-onboarding-complete-field-catalog.md"
)
REFRESH = ROOT / "maintainer-contracts/api-refresh-user-onboarding-2026-08-10.json"
PLATFORM_CONTRACT = (
    ROOT
    / "huifu-merchant-onboarding/references/user-onboarding-platform-contracts.md"
)

EXPECTED_ENDPOINTS = {
    "user_enterprise": "POST /v2/user/basicdata/ent",
    "user_individual": "POST /v2/user/basicdata/indv",
    "user_business_open": "POST /v2/user/busi/open",
    "user_apply_query": "POST /v2/user/apply/query",
    "user_detail_query": "POST /v2/user/basicdata/query",
    "user_enterprise_modify": "POST /v2/user/basicdata/ent/modify",
    "user_individual_modify": "POST /v2/user/basicdata/indv/modify",
    "user_business_modify": "POST /v2/user/busi/modify",
    "user_list_query": "POST /v2/user/list/query",
}


SURFACE_NAMES = {
    "request": "请求信封",
    "response": "响应信封",
    "request.data": "请求 data",
    "response.data": "同步响应 data",
    "async": "异步通知信封",
    "async.data": "异步通知 data",
}


@dataclass(frozen=True)
class RawField:
    name: str
    label: str
    kind: str
    length: str
    required: str
    description: str
    child: str | None
    array: bool


SENSITIVE_EXAMPLE_FIELDS = frozenset(
    {
        "address",
        "card_name",
        "card_no",
        "cert_no",
        "cert_number",
        "contact_email",
        "contact_mobile",
        "contact_name",
        "download_url",
        "elec_acct_sign_seq_id",
        "email",
        "file_id",
        "file_name",
        "legal_cert_no",
        "legal_name",
        "license_code",
        "login_name",
        "login_password",
        "merchant_id",
        "mobile_no",
        "name",
        "operator_id",
        "qrcode",
        "qrcode_data",
        "reg_detail",
        "reg_name",
        "short_name",
        "sign_url",
        "smid",
        "token_no",
        "wx_applet_secret",
        "wx_woa_secret",
    }
)


def source_dir(lock: dict[str, object]) -> Path:
    snapshot_id = lock.get("source_snapshot_id", lock["source_date"])
    return (
        ROOT
        / "maintainer-contracts/official-sources/user-onboarding"
        / snapshot_id
    )


def visible_lines(text: str) -> list[str]:
    lines: list[str] = []
    in_comment = False
    for line in text.splitlines():
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue
        lines.append(line)
    return lines


def source_page_field_notes(text: str) -> dict[str, str]:
    """Independently collect field notes rendered outside official tables."""
    result: dict[str, str] = {}
    for line in visible_lines(text):
        match = re.fullmatch(
            r"\s*-\s*\[([A-Za-z0-9_]+)\]\s*[：:]\s*(.+?)\s*", line
        )
        if not match:
            continue
        name, description = match.groups()
        assert name not in result, f"duplicate page-level field note for {name}"
        result[name] = normalize(description)
    return result


def source_explicit_page_field_notes(
    source_key: str, text: str
) -> dict[str, str]:
    """Independently bind an unlabelled note to its two named fields."""
    if source_key == "user_enterprise_modify":
        matches = [
            normalize(line.strip().removeprefix("- "))
            for line in visible_lines(text)
            if line.strip().startswith("- 如要修改法人证件")
        ]
        assert len(matches) == 1, (
            "enterprise modify legal-certificate note must occur exactly once"
        )
        return {
            f"request.data.{name}": matches[0]
            for name in (
                "legal_cert_type",
                "legal_cert_validity_type",
                "legal_cert_begin_date",
                "legal_cert_end_date",
            )
        }
    if source_key != "user_enterprise":
        return {}
    matches = [
        normalize(line.strip().removeprefix("- "))
        for line in visible_lines(text)
        if re.match(r"^\s*-\s*系统会做法人姓名与身份证号的实名认证", line)
    ]
    assert len(matches) == 1, (
        "enterprise identity-verification note must occur exactly once"
    )
    return {
        "request.data.legal_name": matches[0],
        "request.data.legal_cert_no": matches[0],
    }


def normalize(value: str) -> str:
    value = re.sub(r"\b(Array)<(string)>", r"\1&lt;\2&gt;", value, flags=re.I)
    value = re.sub(r"<br\s*/?>", "；", value, flags=re.I)
    value = re.sub(r"</?font[^>]*>", "", value, flags=re.I)
    value = re.sub(r"</?(?:span|div)[^>]*>", "", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip(" ；")
    value = re.sub(r"(?:\s*；\s*){2,}", "；", value)
    value = re.sub(
        r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])",
        "[官网邮箱示例已脱敏]",
        value,
    )
    value = re.sub(r"(?<!\d)1[3-9]\d{9}(?!\d)", "[官网示例已脱敏]", value)
    value = re.sub(r"(?<!\d)\d{16,32}(?!\d)", "[官网示例已脱敏]", value)
    value = re.sub(
        r"(?<!\]\()https?://[^\s)]+\.(?:jpe?g|png|bmp)(?:[?#][^\s)]*)?",
        "[官网示例图片已省略]",
        value,
        flags=re.I,
    )
    return value


def resolve_links(value: str, source_url: str) -> str:
    def resolve(match: re.Match[str]) -> str:
        label, target = match.groups()
        split = urllib.parse.urlsplit(target)
        if split.scheme in {"http", "https"}:
            return match.group(0)
        assert not split.scheme and not target.startswith("//"), (
            f"unsupported source link: {target}"
        )
        absolute = urllib.parse.urljoin(source_url, target)
        return f"[{label}]({absolute})（官网相对地址原文：`{target}`）"

    return re.sub(r"\[([^\]]+)\]\(([^()\s]+)\)", resolve, value)


def redact_sensitive_example(name: str, description: str) -> str:
    if name not in SENSITIVE_EXAMPLE_FIELDS:
        return description
    return re.sub(
        r"(示例值\s*[：:])[^；|]*",
        r"\1[官网敏感示例已脱敏]",
        description,
    )


def split_source_row(row: str) -> list[str]:
    body = row.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    marker = "\0USER_ONBOARDING_ESCAPED_PIPE\0"
    assert marker not in body
    protected = re.sub(r"(?<!\\)\\\|", marker, body)
    return [cell.replace(marker, "|").strip() for cell in protected.split("|")]


def consume_row(lines: list[str], cursor: int) -> tuple[str, int]:
    row = lines[cursor].strip()
    cursor += 1
    while not row.rstrip().endswith("|"):
        assert cursor < len(lines) and "<!-- extend:end -->" not in lines[cursor], (
            f"unterminated source row near line {cursor}"
        )
        continuation = lines[cursor].strip()
        if not continuation or continuation.startswith(("<!--", "#")):
            break
        if continuation.startswith("|") and continuation != "|":
            break
        row = f"{row} {continuation}"
        cursor += 1
    return row, cursor


def source_table_columns(row: str) -> dict[str, int] | None:
    """Resolve a contract table by its declared headings, independently."""
    cells = split_source_row(row)
    headings = [normalize(cell).strip("* ") for cell in cells]
    if len(headings) < 6 or headings[0] not in {"参数", "出参名"}:
        return None

    def locate(*names: str) -> int:
        for index, heading in enumerate(headings):
            if heading in names:
                return index
        raise AssertionError(f"missing contract column {names}: {headings}")

    return {
        "name": 0,
        "label": 1,
        "kind": locate("定义", "类型"),
        "length": locate("长度"),
        "required": locate("必填", "非空"),
        "description": locate("说明"),
    }


def source_field(
    row: str,
    url: str,
    columns: dict[str, int],
) -> RawField | None:
    cells = split_source_row(row)
    if len(cells) <= max(columns.values()):
        return None
    raw_name = cells[columns["name"]]
    child_match = re.search(r'class="[^"]*\bextend\s+([\w-]+)[^"]*"', raw_name)
    name = normalize(raw_name).strip("* ")
    if not name or name in {"参数", "出参名"}:
        return None
    kind = normalize(cells[columns["kind"]]) or "—"
    description = resolve_links(
        normalize(" | ".join(cells[columns["description"] :])),
        url,
    ) or "—"
    description = redact_sensitive_example(name, description)
    return RawField(
        name=name,
        label=normalize(cells[columns["label"]]) or "—",
        kind=kind,
        length=normalize(cells[columns["length"]]) or "—",
        required=normalize(cells[columns["required"]]) or "—",
        description=description,
        child=child_match.group(1) if child_match else None,
        array=kind.lower() == "array" or "jsonarray" in description.lower(),
    )


def source_tables(text: str, url: str) -> tuple[list[list[RawField]], dict[str, list[RawField]]]:
    lines = visible_lines(text)
    tables: list[tuple[str | None, list[RawField]]] = []
    pending: str | None = None
    cursor = 0
    while cursor < len(lines):
        marker = re.search(r"div:extend-table\s+([\w-]+)-table", lines[cursor])
        if marker:
            pending = marker.group(1)
        columns = source_table_columns(lines[cursor])
        if columns is None:
            cursor += 1
            continue
        table_id, pending = pending, None
        rows: list[RawField] = []
        cursor += 2
        if table_id is None:
            while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
                row, cursor = consume_row(lines, cursor)
                field = source_field(row, url, columns)
                if field:
                    rows.append(field)
        else:
            while cursor < len(lines) and "<!-- extend:end -->" not in lines[cursor]:
                if lines[cursor].lstrip().startswith("|"):
                    row, cursor = consume_row(lines, cursor)
                    field = source_field(row, url, columns)
                    if field:
                        rows.append(field)
                else:
                    cursor += 1
        tables.append((table_id, rows))
    roots = [rows for table_id, rows in tables if table_id is None]
    nested = {table_id: rows for table_id, rows in tables if table_id is not None}
    return roots, nested


def classify_root(fields: list[RawField]) -> str:
    names = {field.name for field in fields}
    if {"sys_id", "product_id", "sign", "data"} <= names:
        return "request"
    if names == {"sign", "data"}:
        return "response"
    if {"resp_code", "resp_desc", "sign", "data"} <= names:
        return "async"
    if {"sub_resp_code", "notify_type"} <= names:
        return "async.data"
    if "resp_code" in names:
        return "response.data"
    if {"req_seq_id", "req_date"} <= names:
        return "request.data"
    raise AssertionError(f"cannot classify root table: {sorted(names)}")


def flatten(
    fields: list[RawField],
    nested: dict[str, list[RawField]],
    prefix: str,
    used: set[str],
    stack: tuple[str, ...] = (),
) -> list[tuple[str, RawField]]:
    result: list[tuple[str, RawField]] = []
    for field in fields:
        base = f"{prefix}.{field.name}"
        path = f"{base}[]" if field.array else base
        result.append((path, field))
        if not field.child:
            continue
        assert field.child in nested, f"missing extend-table: {field.child}"
        assert field.child not in stack, f"extend-table cycle: {field.child}"
        used.add(field.child)
        result.extend(
            flatten(
                nested[field.child],
                nested,
                path,
                used,
                (*stack, field.child),
            )
        )
    return result


RecordKey = tuple[str, str, str]
RecordValue = tuple[str, str, str, str, str, str, str, str]


def direction(path: str) -> str:
    if path.startswith("request."):
        return "request"
    if path.startswith("response."):
        return "response"
    return "callback"


def expected_records(
    lock: dict[str, object],
) -> tuple[dict[RecordKey, RecordValue], dict[str, tuple[int, int]]]:
    result: dict[RecordKey, RecordValue] = {}
    table_counts: dict[str, tuple[int, int]] = {}
    base = source_dir(lock)
    for source in lock["sources"]:
        text = (base / source["filename"]).read_text(encoding="utf-8-sig")
        roots, nested = source_tables(text, source["url"])
        page_notes = source_page_field_notes(text)
        page_note_matches = {name: 0 for name in page_notes}
        explicit_page_notes = source_explicit_page_field_notes(source["key"], text)
        explicit_page_note_matches = {path: 0 for path in explicit_page_notes}
        used: set[str] = set()
        prefixes: set[str] = set()
        for fields in roots:
            prefix = classify_root(fields)
            assert prefix not in prefixes, f"duplicate root surface in {source['key']}: {prefix}"
            prefixes.add(prefix)
            surface = SURFACE_NAMES[prefix]
            for path, field in flatten(fields, nested, prefix, used):
                description = field.description
                path_leaf = path.removesuffix("[]").rsplit(".", 1)[-1]
                note_prefix = "request." if path_leaf in {"sys_id", "product_id", "sign"} else "request.data."
                if path.startswith(note_prefix) and path_leaf in page_notes:
                    description = (
                        f"{description}；官网页内注意：{page_notes[path_leaf]}"
                        if description != "—"
                        else f"官网页内注意：{page_notes[path_leaf]}"
                    )
                    page_note_matches[path_leaf] += 1
                if path in explicit_page_notes:
                    description = (
                        f"{description}；官网页内注意：{explicit_page_notes[path]}"
                        if description != "—"
                        else f"官网页内注意：{explicit_page_notes[path]}"
                    )
                    explicit_page_note_matches[path] += 1
                key = (source["title"], surface, path)
                assert key not in result, f"duplicate source path: {key}"
                result[key] = (
                    direction(path),
                    field.label,
                    field.kind,
                    field.length,
                    field.required,
                    description,
                    source["url"],
                    source["sha256"],
                )
        assert used == set(nested), (
            f"unreachable nested tables in {source['key']}: {sorted(set(nested) - used)}"
        )
        assert all(count == 1 for count in page_note_matches.values()), (
            f"page-level field notes must resolve once in {source['key']}: "
            f"{page_note_matches}"
        )
        assert all(count == 1 for count in explicit_page_note_matches.values()), (
            f"explicit page-level field notes must resolve once in {source['key']}: "
            f"{explicit_page_note_matches}"
        )
        table_counts[source["key"]] = (len(roots), len(nested))
    return result, table_counts


def split_catalog_row(row: str) -> list[str]:
    body = row.strip().strip("|")
    marker = "\0CATALOG_PIPE\0"
    assert marker not in body
    body = body.replace("\\|", marker)
    return [part.replace(marker, "|").strip() for part in body.split("|")]


def actual_records(lock: dict[str, object]) -> dict[RecordKey, RecordValue]:
    source_by_title = {item["title"]: item for item in lock["sources"]}
    result: dict[RecordKey, RecordValue] = {}
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
            metadata[title]["url"] = line.removeprefix(
                "- 原始地址：<"
            ).removesuffix(">")
            continue
        if title and line.startswith("- SHA-256：`") and line.endswith("`"):
            metadata[title]["sha256"] = line.removeprefix(
                "- SHA-256：`"
            ).removesuffix("`")
            continue
        if title and line.startswith("### "):
            surface = line[4:].strip()
            continue
        if not title or not surface or not line.startswith("| `"):
            continue
        cells = split_catalog_row(line)
        assert len(cells) == 6, f"malformed catalog row: {line}"
        path = cells[0].strip("`")
        title_metadata = metadata[title]
        assert set(title_metadata) == {"url", "sha256"}, (
            f"catalog metadata missing before field rows for {title}: {title_metadata}"
        )
        key = (title, surface, path)
        assert key not in result, f"duplicate catalog path: {key}"
        result[key] = (
            direction(path),
            cells[1],
            cells[2].strip("`"),
            cells[3].strip("`"),
            cells[4].strip("`"),
            cells[5],
            title_metadata["url"],
            title_metadata["sha256"],
        )
    expected_headings = [
        "目录",
        "使用规则",
        "生成覆盖摘要",
        *(source["title"] for source in lock["sources"]),
    ]
    assert headings == expected_headings, (
        f"catalog H2 surface changed: expected={expected_headings}, actual={headings}"
    )
    assert set(metadata) == set(source_by_title), (
        f"catalog source sections mismatch: {sorted(metadata)}"
    )
    return result


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


def validate_official_undefined_fields(
    records: dict[RecordKey, RecordValue],
    node_structure: dict[RecordKey, str],
) -> tuple[int, int]:
    blank_descriptions = {
        (title, path)
        for (title, _surface, path), value in records.items()
        if value[5] == "—"
    }
    blank_scalar_lengths = {
        (key[0], key[2])
        for key, value in records.items()
        if node_structure[key] == "leaf" and value[3] == "—"
    }
    expected_descriptions = {
        ("用户业务入驻修改", "async.data"),
        ("用户信息查询", "response.data.account_info"),
        ("用户信息查询", "response.data.account_recharge_config.transfer_flag_name"),
        ("用户信息查询", "response.data.account_recharge_config.transfer_flag_no"),
    }
    expected_lengths: set[tuple[str, str]] = set()
    assert blank_descriptions == expected_descriptions, (
        "official blank-description set changed: "
        f"missing={sorted(expected_descriptions - blank_descriptions)}, "
        f"extra={sorted(blank_descriptions - expected_descriptions)}"
    )
    assert blank_scalar_lengths == expected_lengths, (
        "official blank scalar-length set changed: "
        f"missing={sorted(expected_lengths - blank_scalar_lengths)}, "
        f"extra={sorted(blank_scalar_lengths - expected_lengths)}"
    )
    return len(blank_descriptions), len(blank_scalar_lengths)


def validate_current_account_level_contract(records: dict[RecordKey, RecordValue]) -> None:
    """Pin direction-specific LV3 wire types and the new requiredness conflict."""
    fields = {(title, path): value for (title, _surface, path), value in records.items()}
    for title in ("用户业务入驻", "用户业务入驻修改"):
        level = fields[title, "request.data.account_level"]
        assert level[2:5] == ("String", "6", "N")
        assert "LV1/LV2/LV3" in level[5] and "默认LV1" in level[5]
        for config in ("balance_pay_config", "account_recharge_config", "delay_pay_config"):
            request = fields[title, f"request.data.{config}"]
            response = fields["用户信息查询", f"response.data.{config}"]
            assert request[2] == "String" and "jsonObject" in request[5] and "LV3" in request[5]
            assert response[2] == "Object", f"query {config} must not inherit request string encoding"
        for config in ("balance_pay_config", "account_recharge_config"):
            for fee in ("fee_rate", "fee_fix_amt"):
                field = fields[title, f"request.data.{config}.{fee}"]
                assert field[2:5] == ("String", "9", "Y")
                assert "不能同时为空" in field[5], "preserve Y-versus-either fee condition conflict"
        out_fee = fields[title, "request.data.balance_pay_config.out_fee_flag"]
        assert out_fee[5] == "是否交易手续费外扣", "request enum must not be borrowed from query"
        assert fields[title, "async.data.account_info"][2] == "String"
        assert "jsonObject" in fields[title, "async.data.account_info"][5]
        assert fields[title, "async.data.account_info.fail_msg"][2:5] == ("String", "256", "N")
        assert all(token in fields[title, "async.data.notify_type"][5] for token in ("E:", "A:", "U：", "Z："))
        assert fields[title, "request.data.account_recharge_config.out_fee_huifu_id"][2:5] == ("String", "18", "C")
        assert fields[title, "request.data.account_recharge_config.out_fee_acct_id"][2:5] == ("String", "16", "C")
        assert fields[title, "async.data.account_info.face_url"][2:5] == ("String", "512", "N")
        assert fields[title, "async.data.account_info.verify_ord_id"][2:5] == ("String", "32", "N")
    assert fields["企业用户开户", "request.data.ent_type"][4] == "Y"


def validate_refresh_semantic_contracts(
    records: dict[RecordKey, RecordValue],
) -> tuple[int, int, int, int]:
    def find(interface: str, path: str) -> RecordValue:
        matches = [
            value
            for (title, _surface, record_path), value in records.items()
            if title == interface and record_path == path
        ]
        assert len(matches) == 1, f"semantic field lookup failed: {interface} {path}"
        return matches[0]

    conditional_fields = (
        ("用户业务入驻", "request.data.settle_config_list[].constant_amt"),
        ("用户业务入驻修改", "request.data.settle_config_list[].is_priority_receipt"),
    )
    for interface, path in conditional_fields:
        assert find(interface, path)[4] == "C"
    for name in ("weekday_fix_amt", "weekday_fee_rate"):
        field = find("用户业务入驻修改", f"request.data.cash_config[].{name}")
        assert field[4] == "C"
        assert all(term in field[5] for term in ("D1", "工作日", "未配置", "节假日"))
        assert "不生效" not in field[5], f"resolved weekday fee conflict reintroduced: {name}"
    detail_mp = find(
        "用户信息查询", "response.data.elec_acct_config.elec_card_list[].mp"
    )
    business_card_name = find(
        "用户业务入驻", "request.data.card_info.card_name"
    )
    assert "11位数字" in detail_mp[5]
    assert "必填" not in business_card_name[5] and "选填" not in business_card_name[5]

    page_notes = (
        ("企业用户开户", "request.data.legal_name"),
        ("企业用户开户", "request.data.legal_cert_no"),
        ("个人用户开户", "request.data.file_list[]"),
        ("企业用户基本信息修改", "request.data.legal_cert_type"),
        ("企业用户基本信息修改", "request.data.legal_cert_validity_type"),
        ("企业用户基本信息修改", "request.data.legal_cert_begin_date"),
        ("企业用户基本信息修改", "request.data.legal_cert_end_date"),
    )
    for index, (interface, path) in enumerate(page_notes):
        value = find(interface, path)
        assert "官网页内注意" in value[5]
        assert ("实名认证" if index < 3 else "同步填写") in value[5]
    for interface in ("企业用户开户", "个人用户开户"):
        value = find(interface, "request.sys_id")
        assert "官网页内注意" in value[5]
        assert all(term in value[5] for term in ("总部商户", "开户", "upper_huifu_id"))
    incomplete_links: tuple[tuple[str, str], ...] = ()
    ambiguous_semantics = (("用户业务入驻", "request.data.card_info.card_type"),)
    value = find(*ambiguous_semantics[0])
    assert "0：对公" in value[5] and "4：对公非同名" in value[5]

    return (
        len(conditional_fields),
        len(page_notes) + 2,
        len(incomplete_links),
        len(ambiguous_semantics),
    )


def official_request_example(text: str) -> dict[str, object]:
    matches = re.findall(
        r"#### 请求示例\s*```json\s*(.*?)\s*```",
        text,
        flags=re.S,
    )
    assert len(matches) == 1, f"expected one official request example, found {len(matches)}"
    value = json.loads(matches[0])
    assert isinstance(value, dict)
    return value


def official_response_example(text: str) -> dict[str, object]:
    matches = re.findall(
        r"##### 返回示例.*?```json\s*(.*?)\s*```",
        text,
        flags=re.S,
    )
    assert len(matches) == 1, f"expected one official response example, found {len(matches)}"
    value = json.loads(matches[0])
    assert isinstance(value, dict)
    return value


def flatten_example_paths(value: object, prefix: str) -> set[str]:
    result: set[str] = set()
    if isinstance(value, dict):
        for name, child in value.items():
            path = f"{prefix}.{name}"
            decoded = child
            if isinstance(child, str) and child.startswith(("{", "[")):
                try:
                    decoded = json.loads(child)
                except json.JSONDecodeError:
                    decoded = child
            if isinstance(decoded, list):
                array_path = f"{path}[]"
                result.add(array_path)
                for item in decoded:
                    result.update(flatten_example_paths(item, array_path))
            else:
                result.add(path)
                result.update(flatten_example_paths(decoded, path))
    elif isinstance(value, list):
        array_path = f"{prefix}[]"
        result.add(array_path)
        for item in value:
            result.update(flatten_example_paths(item, array_path))
    return result


def validate_official_example_shape_contract(lock: dict[str, object]) -> int:
    base = source_dir(lock)
    per_interface: dict[str, dict[str, int]] = {}
    fingerprints: list[str] = []
    expected_counts = {
        "user_enterprise": {"request_paths": 29, "response_paths": 7},
        "user_individual": {"request_paths": 21, "response_paths": 7},
        "user_business_open": {"request_paths": 66, "response_paths": 6},
        "user_apply_query": {"request_paths": 8, "response_paths": 13},
        "user_detail_query": {"request_paths": 7, "response_paths": 50},
        "user_enterprise_modify": {"request_paths": 28, "response_paths": 5},
        "user_individual_modify": {"request_paths": 12, "response_paths": 5},
        "user_business_modify": {"request_paths": 49, "response_paths": 6},
        "user_list_query": {"request_paths": 7, "response_paths": 9},
    }
    for source in lock["sources"]:
        text = (base / source["filename"]).read_text(encoding="utf-8-sig")
        request_paths = flatten_example_paths(official_request_example(text), "request")
        response_paths = flatten_example_paths(official_response_example(text), "response")
        per_interface[source["key"]] = {
            "request_paths": len(request_paths),
            "response_paths": len(response_paths),
        }
        fingerprints.extend(
            f"{source['key']}|request|{path}" for path in sorted(request_paths)
        )
        fingerprints.extend(
            f"{source['key']}|response|{path}" for path in sorted(response_paths)
        )
    digest = hashlib.sha256("\n".join(fingerprints).encode("utf-8")).hexdigest()
    assert per_interface == expected_counts, (
        f"official example path counts changed: {per_interface}"
    )
    assert len(fingerprints) == 335
    assert digest == "e0e30620184c8b5a8fcc1a14f09ddfb42ad935d7692f81703a746dea7ac8b616", (
        f"official example path fingerprint changed: {digest}"
    )
    return len(fingerprints)


def validate_public_platform_contract() -> tuple[int, int]:
    expected_sources = [
        (
            "异步消息简介",
            "https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md",
            "e5f1ad5d92511c343d6bbf7d5f09ef0eee4a252bdac3b4d53934c177f6805364",
        ),
        (
            "开发规范",
            "https://paas.huifu.com/partners/start/kfgf.md",
            "340ba948aae4cb1fc6b12503b58e24d11c538b5ba70d0728ef374b0d1a4137a5",
        ),
        (
            "加签验签",
            "https://paas.huifu.com/partners/start/api_v2jqyq.md",
            "f3ddf23effad316d247033eb5d2f781e57a8d3d23260387b42470de8e1fd76c5",
        ),
        (
            "加密解密",
            "https://paas.huifu.com/partners/start/api_jiami_jiemi.md",
            "de9c44b0dc59d34a609ea6fde5437cc7d633722cd770ecadf37a13b347f4bb82",
        ),
        (
            "获取密钥",
            "https://paas.huifu.com/partners/start/guide_gsycshq.md",
            "8f79c590233daba14ba2c958ba89d4f6326f624a20bff053d5c5159ec03afab0",
        ),
        (
            "开发接入说明",
            "https://paas.huifu.com/partners/start/api_kfzn.md",
            "a50c162dcbafd71044c1c6687b6b908e050a5e5aa54267336ef75661b1f5410d",
        ),
        (
            "基础参数汇总",
            "https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md",
            "2d8b73e1009da4b2fccfae75b0bc2546acfc105b2219ada12a2af41f2b6da191",
        ),
        (
            "Webhook介绍",
            "https://paas.huifu.com/partners/devtools/doc/webhook/webhook_jieshao.md",
            "8a14a938445d9b7e15f2bce5af27b0a38708a601fbbfd88c3004a045cb333089",
        ),
    ]
    refresh = json.loads(REFRESH.read_text(encoding="utf-8"))
    actual_sources = [
        (item["name"], item["url"], item["sha256"])
        for item in refresh["public_sources"]
    ]
    assert actual_sources == expected_sources, "public platform source set changed"

    text = PLATFORM_CONTRACT.read_text(encoding="utf-8")
    for name, url, digest in expected_sources:
        assert name in text and url in text and digest in text

    required_contract_terms = (
        "HTTP 200",
        "RECV_ORD_ID_` + `async.data.req_seq_id",
        "原始 `data` 字符串",
        "异步 `data` 不排序",
        "超时默认重试3次",
        "HTTP 500-599 默认重试3次",
        "接口异步通知，不是控台 Webhook",
        "个人用户只允许对私法人卡",
        "`card_type=1`",
        "成功响应返回 `apply_no`",
        "五个接口成功响应都包含外层 `response.data`",
        "String(JSON Array)",
        "response.data.qry_cash_card_info_list[].branch_code",
    )
    for term in required_contract_terms:
        assert term in text, f"platform contract missing semantic term: {term}"

    decisions = refresh["integration_decisions"]
    assert decisions["conditional_marker"] == "C means conditionally required."
    assert decisions["card_type_subject_matrix"] == {
        "individual": ["1"],
        "enterprise": ["0", "1", "2", "4"],
    }
    assert "native JSON Object" in decisions["successful_response_data"]
    assert "Y/P/N/F" in decisions["apply_query_fields"]
    assert "apply_no" in decisions["business_open_apply_no"]
    assert "Webhook" in decisions["interface_async_reference"]
    return len(expected_sources), len(decisions)


def validate_official_request_example_anomalies(
    lock: dict[str, object], records: dict[RecordKey, RecordValue]
) -> int:
    by_key = {item["key"]: item for item in lock["sources"]}
    base = source_dir(lock)

    def load(key: str) -> dict[str, object]:
        source = by_key[key]
        text = (base / source["filename"]).read_text(encoding="utf-8-sig")
        return official_request_example(text)

    enterprise_request = load("user_enterprise")
    individual_request = load("user_individual")
    enterprise = enterprise_request["data"]
    individual = individual_request["data"]
    business = load("user_business_open")["data"]
    assert isinstance(enterprise, dict)
    assert isinstance(individual, dict)
    assert isinstance(business, dict)

    card_info = json.loads(business["card_info"])
    settle = json.loads(business["settle_config_list"])
    cash = json.loads(business["cash_config"])
    assert isinstance(card_info, dict)
    assert isinstance(settle, list) and len(settle) == 1
    assert isinstance(cash, list) and len(cash) == 1

    def formal(interface: str, path: str) -> RecordValue:
        matches = [
            value
            for (title, _surface, record_path), value in records.items()
            if title == interface and record_path == path
        ]
        assert len(matches) == 1, f"formal field lookup failed: {interface} {path}"
        return matches[0]

    formal_paths = {
        (title, path) for title, _surface, path in records
    }
    enterprise_sms = formal("企业用户开户", "request.data.sms_send_flag")
    individual_sms = formal("个人用户开户", "request.data.sms_send_flag")
    individual_file_list = formal("个人用户开户", "request.data.file_list[]")
    fixed_ratio = formal(
        "用户业务入驻", "request.data.settle_config_list[].fixed_ratio"
    )
    constant_amt = formal(
        "用户业务入驻", "request.data.settle_config_list[].constant_amt"
    )
    cash_fee_rate = formal(
        "用户业务入驻", "request.data.cash_config[].fee_rate"
    )

    checks = {
        "enterprise-sms-send-flag-y": enterprise.get("sms_send_flag") == "Y"
        and "Y" in enterprise_sms[5]
        and "N" in enterprise_sms[5],
        "individual-sms-send-flag-y": individual.get("sms_send_flag") == "Y"
        and "Y" in individual_sms[5]
        and "N" in individual_sms[5],
        "individual-file-list-string-native-array-conflict": isinstance(individual.get("file_list"), list)
        and individual_file_list[2] == "String"
        and "jsonArray" in individual_file_list[5],
        "individual-operator-id-absent": "operator_id" not in individual
        and ("个人用户开户", "request.data.operator_id") not in formal_paths,
        "business-card-info-branch-name-example-only": "bank_code" not in card_info
        and "branch_name" in card_info
        and (
            "用户业务入驻",
            "request.data.card_info.branch_name",
        )
        not in formal_paths,
        "business-d1-constant-amt-present": settle[0].get("settle_cycle") == "D1"
        and settle[0].get("constant_amt") == "1.00"
        and constant_amt[4] == "C"
        and "D1时必填" in constant_amt[5],
        "business-fixed-ratio-two-decimals": settle[0].get("fixed_ratio") == "2.00"
        and "两位" in fixed_ratio[5],
        "business-cash-fee-rate-two-decimals": cash[0].get("fee_rate") == "2.00"
        and "两位" in cash_fee_rate[5],
    }
    failed = sorted(name for name, matched in checks.items() if not matched)
    assert not failed, f"official request-example anomaly changed: {failed}"
    return len(checks)


def validate_official_response_example_anomalies(
    lock: dict[str, object], records: dict[RecordKey, RecordValue]
) -> int:
    by_key = {item["key"]: item for item in lock["sources"]}
    base = source_dir(lock)

    def load(key: str) -> dict[str, object]:
        source = by_key[key]
        text = (base / source["filename"]).read_text(encoding="utf-8-sig")
        return official_response_example(text)

    def formal(interface: str, path: str) -> RecordValue:
        matches = [
            value
            for (title, _surface, record_path), value in records.items()
            if title == interface and record_path == path
        ]
        assert len(matches) == 1, f"formal response lookup failed: {interface} {path}"
        return matches[0]

    enterprise = load("user_enterprise")
    individual = load("user_individual")
    business = load("user_business_open")
    detail = load("user_detail_query")
    business_data = formal("用户业务入驻", "response.data")
    detail_resp_code = formal("用户信息查询", "response.data.resp_code")
    enterprise_sign = formal("企业用户开户", "response.sign")
    individual_sign = formal("个人用户开户", "response.sign")
    assert isinstance(detail.get("data"), dict)

    checks = {
        "enterprise-required-sign-present": "sign" in enterprise
        and enterprise_sign[4] == "Y",
        "individual-required-sign-present": "sign" in individual
        and individual_sign[4] == "Y",
        "business-json-data-rendered-as-object": isinstance(business.get("data"), dict)
        and business_data[2] == "Json",
        "detail-resp-code-eight": len(detail["data"].get("resp_code", "")) == 8
        and detail_resp_code[3] == "8",
    }
    failed = sorted(name for name, matched in checks.items() if not matched)
    assert not failed, f"official response-example anomaly changed: {failed}"
    return len(checks)


def validate_list_query_conflicts(
    lock: dict[str, object], records: dict[RecordKey, RecordValue]
) -> int:
    source = next(item for item in lock["sources"] if item["key"] == "user_list_query")
    text = (source_dir(lock) / source["filename"]).read_text(encoding="utf-8-sig")
    request_example = official_request_example(text)
    example = official_response_example(text)
    data = example.get("data")
    assert isinstance(data, dict), "user-list success example data must remain an object"
    users = data.get("user_list_info_list")
    assert isinstance(users, list) and users, (
        "user-list success example must retain a non-empty native array"
    )

    def formal(path: str) -> RecordValue:
        matches = [
            value
            for (title, _surface, record_path), value in records.items()
            if title == "用户列表查询" and record_path == path
        ]
        assert len(matches) == 1, f"user-list formal lookup failed: {path}"
        return matches[0]

    list_field = formal("response.data.user_list_info_list[]")
    huifu_id = formal("response.data.user_list_info_list[].huifu_id")
    upper_huifu_id = formal("response.data.user_list_info_list[].upper_huifu_id")
    request_sign = formal("request.sign")
    sign = formal("response.sign")
    checks = {
        "list-string-native-array-conflict": list_field[2] == "String"
        and "jsonArray" in list_field[5]
        and isinstance(users, list),
        "list-huifu-id-length-eighteen": huifu_id[3] == "18",
        "list-upper-huifu-id-length-eighteen": upper_huifu_id[3] == "18",
        "list-required-request-sign-present": request_sign[4] == "Y"
        and "sign" in request_example,
        "list-required-sign-present": sign[4] == "Y" and "sign" in example,
    }
    failed = sorted(name for name, matched in checks.items() if not matched)
    assert not failed, f"user-list official conflict changed: {failed}"
    return len(checks)


def main() -> int:
    fixture = r"| sys_id | 系统\|编号 | String | 32 | Y | 保留\|说明 |"
    assert split_source_row(fixture) == [
        "sys_id",
        "系统|编号",
        "String",
        "32",
        "Y",
        "保留|说明",
    ]
    from source_review_validation import validate_source
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    validate_source(lock, "user-onboarding", list(EXPECTED_ENDPOINTS))
    for source in lock["sources"]:
        assert source["endpoint"] == EXPECTED_ENDPOINTS[source["key"]]

    expected, table_counts = expected_records(lock)
    actual = actual_records(lock)
    assert set(expected) == set(actual), (
        f"node set mismatch: missing={sorted(set(expected) - set(actual))}, "
        f"extra={sorted(set(actual) - set(expected))}"
    )
    changed = [
        (key, expected[key], actual[key])
        for key in sorted(expected)
        if expected[key] != actual[key]
    ]
    assert not changed, f"node property mismatches: {changed}"

    by_title = {source["title"]: source for source in lock["sources"]}
    for title, source in by_title.items():
        records = {key: value for key, value in actual.items() if key[0] == title}
        assert len(records) == source["field_count"]
        for name, expected_count in (
            ("request", source["request_fields"]),
            ("response", source["response_fields"]),
            ("callback", source["callback_fields"]),
        ):
            assert sum(value[0] == name for value in records.values()) == expected_count
        assert table_counts[source["key"]] == (
            source["root_tables"],
            source["extend_tables"],
        )

    node_structure = structure(actual)
    blank_descriptions, blank_scalar_lengths = validate_official_undefined_fields(
        actual, node_structure
    )
    validate_current_account_level_contract(actual)
    for title in ("用户业务入驻", "用户业务入驻修改"):
        assert actual[title, "异步通知 data", "async.data.agreement_info_list[]"][2] == "String"
    undefined_triggers, page_notes, incomplete_links, ambiguous_semantics = (
        validate_refresh_semantic_contracts(actual)
    )
    guarded_request_example_anomalies = validate_official_request_example_anomalies(
        lock, actual
    )
    guarded_response_example_anomalies = validate_official_response_example_anomalies(
        lock, actual
    )
    list_query_conflicts = validate_list_query_conflicts(lock, actual)
    official_example_paths = validate_official_example_shape_contract(lock)
    public_sources, integration_decisions = validate_public_platform_contract()
    direction_counts = {
        name: sum(value[0] == name for value in actual.values())
        for name in ("request", "response", "callback")
    }
    structure_counts = {
        name: sum(value == name for value in node_structure.values())
        for name in ("parent", "leaf")
    }
    assert lock["totals"] == {
        "fields": 644,
        "request": 345,
        "response": 227,
        "callback": 72,
        "parent": 78,
        "leaf": 566,
        "root_tables": 40,
        "extend_tables": 58,
    }, "current user source lock totals changed"
    assert len(actual) == lock["totals"]["fields"]
    assert direction_counts == {
        name: lock["totals"][name]
        for name in ("request", "response", "callback")
    }
    assert structure_counts == {
        name: lock["totals"][name]
        for name in ("parent", "leaf")
    }
    assert sum(value[0] for value in table_counts.values()) == lock["totals"]["root_tables"]
    assert sum(value[1] for value in table_counts.values()) == lock["totals"]["extend_tables"]
    print(
        "independent user-onboarding source contract validated: "
        f"{len(actual)} unique nodes; directions={direction_counts}; "
        f"structure={structure_counts}; roots={lock['totals']['root_tables']}; "
        f"extend={lock['totals']['extend_tables']}; "
        f"official_blank_descriptions={blank_descriptions}; "
        f"official_blank_scalar_lengths={blank_scalar_lengths}; "
        f"official_undefined_conditional_triggers={undefined_triggers}; "
        f"page_field_notes={page_notes}; official_incomplete_links={incomplete_links}; "
        f"official_ambiguous_semantics={ambiguous_semantics}; "
        f"guarded_request_example_anomalies={guarded_request_example_anomalies}; "
        f"guarded_response_example_anomalies={guarded_response_example_anomalies}; "
        f"list_query_conflicts={list_query_conflicts}; "
        f"official_example_paths={official_example_paths}; "
        f"public_sources={public_sources}; "
        f"integration_decisions={integration_decisions}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
