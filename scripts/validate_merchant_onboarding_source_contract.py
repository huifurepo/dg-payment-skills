#!/usr/bin/env python3
"""Independently compare all locked onboarding source fields with the catalog.

This validator intentionally does not import the catalog generator. It uses a
separate parser and compares every node and property, not just aggregate counts.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

from skill_validation_config import onboarding_source_dir
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "maintainer-contracts/merchant-onboarding-source-lock-2026-08-10.json"
SOURCE_DIR = onboarding_source_dir()
CATALOG = ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md"


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


SURFACES: dict[str, tuple[tuple[str, str], ...]] = {
    "enterprise": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("审核异步信封", "async.audit"),
        ("审核异步 data", "async.audit.data"),
    ),
    "individual": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("审核异步信封", "async.audit"),
        ("审核异步 data", "async.audit.data"),
    ),
    "business_open": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("申请审核异步信封", "async.audit"),
        ("申请审核异步 data", "async.audit.data"),
        ("逐业务结果异步", "async.business"),
        ("电子协议异步", "async.agreement"),
    ),
    "detail_query": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("响应 data", "response.data"),
    ),
    "status_query": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("响应 data", "response.data"),
    ),
    "business_open_modify": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("审核异步信封", "async.audit"),
        ("审核异步 data", "async.audit.data"),
        ("逐业务结果异步", "async.business"),
        ("电子协议异步", "async.agreement"),
    ),
    "basic_info_modify": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("审核异步 data", "async.audit.data"),
        ("电子协议异步", "async.agreement"),
    ),
    "rate_query": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("响应 data", "response.data"),
    ),
    "status_change": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "sms_send": (
        ("请求信封", "request"),
        ("响应信封", "response"),
        ("请求 data", "request.data"),
        ("响应 data", "response.data"),
    ),
}


def classify_root(fields: list[RawField]) -> str:
    """Classify a root table from its field signature, not document position."""
    names = {field.name for field in fields}
    if "sys_id" in names and {"product_id", "sign", "data"} <= names:
        return "request"
    if names == {"sign", "data"}:
        return "response"
    if {"resp_code", "resp_desc", "sign", "data"} <= names:
        return "async.audit"
    if "audit_status" in names:
        return "async.audit.data"
    if "agreement_info_list" in names and "sub_resp_code" in names:
        return "async.agreement"
    if "sub_resp_code" in names and ({"notify_type", "ord_id", "reg_result_list"} & names):
        return "async.business"
    if "resp_code" in names:
        return "response.data"
    if {"req_seq_id", "req_date"} <= names:
        return "request.data"
    raise AssertionError(f"cannot independently classify root fields: {sorted(names)}")


def normalize(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "；", value, flags=re.I)
    value = re.sub(r"</?font[^>]*>", "", value, flags=re.I)
    value = re.sub(r"</?(?:span|div)[^>]*>", "", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip(" ；")
    value = re.sub(r"(?:\s*；\s*){2,}", "；", value)
    def redact_example_image_link(match: re.Match[str]) -> str:
        label = match.group(1)
        if any(term in label for term in ("说明", "配置", "限制", "参见", "注意")):
            return match.group(0)
        return "[官网示例图片已省略]"

    value = re.sub(
        r"\[([^\]]*)\]\(https?://[^)\s]+\.(?:jpe?g|png|bmp)(?:\?[^)]*)?\)",
        redact_example_image_link,
        value,
        flags=re.I,
    )
    value = re.sub(
        r"(?<!\]\()https?://[^\s)]+\.(?:jpe?g|png|bmp)(?:[?#][^\s)]*)?",
        "[官网示例图片已省略]",
        value,
        flags=re.I,
    )
    value = re.sub(r"(?<!\d)1[3-9]\d{9}(?!\d)", "[官网示例已脱敏]", value)
    value = re.sub(r"(?<!\d)\d{16,32}(?!\d)", "[官网示例已脱敏]", value)
    def redact_ephemeral_signed_url(match: re.Match[str]) -> str:
        url = match.group(0)
        if any(
            key in url
            for key in ("Signature=", "Expires=", "OSSAccessKeyId=")
        ):
            return "[官网临时签名 URL 示例已省略]"
        return url

    value = re.sub(
        r"https?://[^\s；|]+",
        redact_ephemeral_signed_url,
        value,
        flags=re.I,
    )
    return value


def independently_normalize_description_links(
    value: str,
    source_url: str,
    source_headings: frozenset[str],
) -> str:
    """Resolve field links independently from the catalog generator."""

    def replace_link(match: re.Match[str]) -> str:
        label, target = match.groups()
        split = urllib.parse.urlsplit(target)
        if split.scheme in {"http", "https"}:
            suffix = match.group(0)
            if split.scheme == "http":
                suffix += "（官网原始地址为非 HTTPS，不得静默改写）"
            if split.hostname and split.hostname.endswith("huifutest.com"):
                suffix += "（官网原文测试域，不作为生产地址）"
            return suffix
        if split.scheme or target.startswith("//"):
            raise AssertionError(
                f"unsupported field-description link target: {target}"
            )
        if split.path == "api_ggcsbm.md":
            absolute = urllib.parse.urljoin(
                "https://paas.huifu.com/partners/api/doc/",
                target,
            )
        else:
            absolute = urllib.parse.urljoin(source_url, target)
        suffix = (
            f"[{label}]({absolute})"
            f"（官网相对地址原文：`{target}`）"
        )
        if target.startswith("#") and target[1:] not in source_headings:
            suffix += "（官网原始锚点在当前快照无同名标题，`[需要人工确认]`）"
        return suffix

    return re.sub(r"\[([^\]]+)\]\(([^()\s]+)\)", replace_link, value)


def visible_lines(text: str) -> list[str]:
    result: list[str] = []
    hidden = False
    for line in text.splitlines():
        if hidden:
            if "-->" in line:
                hidden = False
            continue
        if "<!--" in line and "-->" not in line:
            hidden = True
            continue
        result.append(line)
    return result


def logical_row(lines: list[str], start: int) -> tuple[str, int]:
    row = lines[start].strip()
    cursor = start + 1
    while not row.rstrip().endswith("|"):
        if cursor >= len(lines) or "<!-- extend:end -->" in lines[cursor]:
            raise AssertionError(f"unterminated source row at line {start + 1}")
        continuation = lines[cursor].strip()
        if not continuation or continuation.startswith(("<!--", "#")):
            break
        if continuation.startswith("|") and continuation != "|":
            break
        row = f"{row} {continuation}"
        cursor += 1
    return row, cursor


def split_source_row(row: str) -> list[str]:
    """Independently protect Markdown-escaped pipes before splitting cells."""
    body = row.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    marker = "\0HUFIU_ESCAPED_PIPE\0"
    if marker in body:
        raise AssertionError("reserved Markdown parser marker found in source")
    protected = re.sub(r"(?<!\\)\\\|", marker, body)
    return [cell.replace(marker, "|").strip() for cell in protected.split("|")]


def source_field(
    row: str,
    source_url: str,
    source_headings: frozenset[str],
) -> RawField | None:
    cells = split_source_row(row)
    if len(cells) < 6:
        return None
    child_match = re.search(r'class="[^"]*\bextend\s+([\w-]+)[^"]*"', cells[0])
    name = normalize(cells[0])
    if not name or name == "参数":
        return None
    kind = normalize(cells[2]) or "—"
    description = independently_normalize_description_links(
        normalize(" | ".join(cells[5:])),
        source_url,
        source_headings,
    ) or "—"
    return RawField(
        name=name,
        label=normalize(cells[1]),
        kind=kind,
        length=normalize(cells[3]) or "—",
        required=normalize(cells[4]) or "—",
        description=description,
        child=child_match.group(1) if child_match else None,
        # Known source typos are resolved by exact interface-scoped paths in
        # ``flatten``; do not make ``josnArray`` a global synonym here.
        array=(
            kind.lower() == "array"
            or "jsonarray" in description.lower()
        ),
    )


def source_tables(
    text: str,
    source_url: str,
) -> tuple[list[list[RawField]], dict[str, list[RawField]]]:
    lines = visible_lines(text)
    source_headings = frozenset(
        re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
        for line in lines
        if (match := re.match(r"^#{1,6}\s+(.+?)\s*$", line))
    )
    tables: list[tuple[str | None, list[RawField]]] = []
    pending: str | None = None
    cursor = 0
    while cursor < len(lines):
        marker = re.search(r"div:extend-table\s+([\w-]+)-table", lines[cursor])
        if marker:
            pending = marker.group(1)
        if not re.match(r"^\|\s*参数", lines[cursor]):
            cursor += 1
            continue
        table_id, pending = pending, None
        rows: list[RawField] = []
        cursor += 2
        if table_id is None:
            while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
                row, cursor = logical_row(lines, cursor)
                field = source_field(row, source_url, source_headings)
                if field:
                    rows.append(field)
        else:
            while cursor < len(lines) and "<!-- extend:end -->" not in lines[cursor]:
                if lines[cursor].lstrip().startswith("|"):
                    row, cursor = logical_row(lines, cursor)
                    field = source_field(row, source_url, source_headings)
                    if field:
                        rows.append(field)
                else:
                    cursor += 1
        tables.append((table_id, rows))
    roots = [rows for table_id, rows in tables if table_id is None]
    nested = {table_id: rows for table_id, rows in tables if table_id is not None}
    return roots, nested


def flatten(
    fields: list[RawField],
    nested: dict[str, list[RawField]],
    prefix: str,
    used: set[str],
    stack: tuple[str, ...] = (),
    array_typo_paths: frozenset[str] = frozenset(),
) -> list[tuple[str, RawField]]:
    result: list[tuple[str, RawField]] = []
    for field in fields:
        base_path = f"{prefix}.{field.name}"
        description = field.description.lower()
        typo_array = base_path in array_typo_paths
        if typo_array:
            assert (
                "josnarray" in description
                and "集合" in field.description
                and "多条" in field.description
            ), f"registered array typo evidence changed: {base_path}"
        else:
            assert "josnarray" not in description, (
                f"unregistered josnArray marker: {base_path}"
            )
        # A scalar String can still be a JSON array without an extend-table.
        # Preserve the declared array identity independently of child rows.
        suffix = "[]" if field.array or typo_array else ""
        path = f"{base_path}{suffix}"
        result.append((path, field))
        if not field.child:
            continue
        assert field.child not in stack, f"source table cycle: {field.child}"
        assert field.child in nested, f"missing source child table: {field.child}"
        used.add(field.child)
        result.extend(
            flatten(
                nested[field.child],
                nested,
                path,
                used,
                (*stack, field.child),
                array_typo_paths,
            )
        )
    return result


def record(
    title: str,
    surface: str,
    path: str,
    field: RawField,
    url: str,
    digest: str,
) -> tuple[tuple[str, str, str], tuple[str, ...]]:
    direction = (
        "request"
        if path.startswith("request.")
        else "response"
        if path.startswith("response.")
        else "callback"
    )
    return (
        (title, surface, path),
        (
            direction,
            field.label,
            field.kind,
            field.length,
            field.required,
            field.description,
            url,
            digest,
        ),
    )


def expected_records(lock: dict[str, object]) -> dict[tuple[str, str, str], tuple[str, ...]]:
    result: dict[tuple[str, str, str], tuple[str, ...]] = {}
    for source in lock["sources"]:
        key = source["key"]
        if key == "image_upload":
            document = json.loads((SOURCE_DIR / source["filename"]).read_bytes())
            synthetic = (
                RawField("sys_id", "—", "—", "—", "—", "仅见于 `requestDemo`；官方 JSON 未给正式顶层 schema。", None, False),
                RawField("product_id", "—", "—", "—", "—", "仅见于 `requestDemo`；官方 JSON 未给正式顶层 schema。", None, False),
                RawField("data", "—", "—", "—", "—", "仅见于 `requestDemo`；`requestBody.params` 定义下列五个 data 字段。", None, False),
                RawField("file", "图片文件流", "—", "—", "—", "仅见于 `requestDemo`，且字段说明只确认它与 `request.data.file_url` 不能同时上传；不得猜测类型或必填性。", None, False),
            )
            for field in synthetic:
                item = record(
                    source["title"],
                    "请求信封与 data",
                    f"request.{field.name}",
                    field,
                    source["url"],
                    source["sha256"],
                )
                assert item[0] not in result
                result[item[0]] = item[1]
            for param in document["requestBody"]["params"]:
                field = RawField(
                    param["name"],
                    param.get("desc", ""),
                    param.get("fieldType", "—"),
                    param.get("maxLength", "—") or "—",
                    param.get("isRequired", "—"),
                    normalize(param.get("remark", "")) or "—",
                    None,
                    False,
                )
                item = record(
                    source["title"],
                    "请求信封与 data",
                    f"request.data.{field.name}",
                    field,
                    source["url"],
                    source["sha256"],
                )
                assert item[0] not in result
                result[item[0]] = item[1]
            continue

        text = (SOURCE_DIR / source["filename"]).read_text(encoding="utf-8-sig")
        roots, nested = source_tables(text, source["url"])
        surfaces = {prefix: surface for surface, prefix in SURFACES[key]}
        expected_prefixes = set(surfaces)
        classified = [(classify_root(fields), fields) for fields in roots]
        actual_prefixes = {prefix for prefix, _ in classified}
        assert len(actual_prefixes) == len(classified), (
            f"{source['filename']}: duplicate independently classified root: {classified}"
        )
        assert actual_prefixes == expected_prefixes, (
            f"{source['filename']}: root signatures map to {sorted(actual_prefixes)}, "
            f"expected {sorted(expected_prefixes)}"
        )
        used: set[str] = set()
        for prefix, fields in classified:
            surface = surfaces[prefix]
            array_typo_paths = (
                frozenset({"async.business.reg_result_list"})
                if key == "business_open_modify"
                else frozenset()
            )
            for path, field in flatten(
                fields,
                nested,
                prefix,
                used,
                array_typo_paths=array_typo_paths,
            ):
                item = record(
                    source["title"],
                    surface,
                    path,
                    field,
                    source["url"],
                    source["sha256"],
                )
                assert item[0] not in result, f"duplicate expected node: {item[0]}"
                result[item[0]] = item[1]
        assert used == set(nested), (
            f"{source['filename']}: unreachable active tables: {sorted(set(nested) - used)}"
        )
    return result


def split_catalog_row(line: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [cell.strip().replace("\\|", "|") for cell in cells]


def actual_records(lock: dict[str, object]) -> dict[tuple[str, str, str], tuple[str, ...]]:
    sources = {source["title"]: source for source in lock["sources"]}
    result: dict[tuple[str, str, str], tuple[str, ...]] = {}
    interface = surface = ""
    text = CATALOG.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("## "):
            interface, surface = line[3:].strip(), ""
        elif line.startswith("### "):
            surface = line[4:].strip()
        elif line.startswith("| `"):
            cells = split_catalog_row(line)
            assert len(cells) == 6, f"invalid catalog row: {line[:120]}"
            path = cells[0].strip("`")
            source = sources[interface]
            direction = (
                "request"
                if path.startswith("request.")
                else "response"
                if path.startswith("response.")
                else "callback"
            )
            key = (interface, surface, path)
            assert key not in result, f"duplicate catalog node: {key}"
            result[key] = (
                direction,
                cells[1],
                cells[2].strip("`"),
                cells[3].strip("`"),
                cells[4].strip("`"),
                cells[5],
                source["url"],
                source["sha256"],
            )
    for source in lock["sources"]:
        section = re.search(
            rf"^## {re.escape(source['title'])}\n(?P<body>.*?)(?=^## |\Z)",
            text,
            flags=re.M | re.S,
        )
        assert section, f"missing catalog source section: {source['title']}"
        body = section.group("body")
        assert source["url"] in body, f"{source['title']}: source URL mismatch"
        assert source["sha256"] in body, f"{source['title']}: source SHA mismatch"
    return result


def parent_and_array_properties(
    records: dict[tuple[str, str, str], tuple[str, ...]]
) -> dict[tuple[str, str, str], tuple[str, int, str]]:
    by_scope: dict[str, set[str]] = {}
    for interface, surface, path in records:
        by_scope.setdefault(interface, set()).add(path)
    properties: dict[tuple[str, str, str], tuple[str, int, str]] = {}
    for key in records:
        interface, surface, path = key
        paths = by_scope[interface]
        parents = [
            candidate
            for candidate in paths
            if path.startswith(f"{candidate}.")
        ]
        parent = max(parents, key=len) if parents else ""
        node_type = "parent" if any(other.startswith(f"{path}.") for other in paths) else "leaf"
        properties[key] = (parent, path.count("[]"), node_type)
    return properties


def onboarding_route_contract_errors(
    skill_text: str,
    open_reference: str,
    modify_reference: str,
    official_open: str,
    official_modify: str,
    onboarding_cases: list[dict[str, object]],
) -> list[str]:
    """Bind public routing guidance to the locked official application clauses."""
    errors: list[str] = []
    required_text = {
        "official business-open supplementary rule": (
            official_open,
            "首次未开通的业务可再次调用此接口进行业务补开",
        ),
        "official modify channel exception": (
            official_modify,
            "银联、银行卡业务开通仍通过",
        ),
        "official modify WeChat/Alipay rule": (
            official_modify,
            "商户微信、支付宝业务补开",
        ),
        "Skill open route": (
            skill_text,
            "银行卡、银联业务开通仍走 `/v2/merchant/busi/open`",
        ),
        "Skill modify route": (
            skill_text,
            "微信、支付宝补开走 `/v2/merchant/busi/modify`",
        ),
        "Skill ambiguity rule": (
            skill_text,
            "同时确认具体能力/渠道和当前开通状态",
        ),
        "business-open reference supplementary rule": (
            open_reference,
            "银联、银行卡业务开通仍使用本接口",
        ),
        "business-open reference repeat-call rule": (
            open_reference,
            "首次未开通的业务再次调用本接口补开",
        ),
        "business-open-modify WeChat/Alipay rule": (
            modify_reference,
            "微信/支付宝补开",
        ),
        "business-open-modify UnionPay/card exception": (
            modify_reference,
            "银联、银行卡业务开通仍使用 `merchant-onboarding-business-open.md`",
        ),
    }
    for label, (text, anchor) in required_text.items():
        if anchor not in text:
            errors.append(f"{label}: missing {anchor}")
    expected_cases = {
        81: ("/v2/merchant/busi/open", "银行卡"),
        82: ("/v2/merchant/busi/open", "银联"),
        83: ("/v2/merchant/busi/modify", "微信"),
        84: ("/v2/merchant/busi/modify", "支付宝"),
    }
    cases_by_id = {
        int(item["id"]): item
        for item in onboarding_cases
        if isinstance(item, dict) and isinstance(item.get("id"), int)
    }
    for case_id, (endpoint, channel) in expected_cases.items():
        case = cases_by_id.get(case_id)
        if case is None:
            errors.append(f"route regression case {case_id} is missing")
            continue
        case_text = f"{case.get('prompt', '')}\n{case.get('expected', '')}"
        if endpoint not in case_text or channel not in case_text:
            errors.append(
                f"route regression case {case_id} must bind {channel} to {endpoint}"
            )
    return errors


def main() -> int:
    parser_fixture = r"| sys_id | 系统\|编号 | String | 32 | Y | 保留\|说明 |"
    assert split_source_row(parser_fixture) == [
        "sys_id",
        "系统|编号",
        "String",
        "32",
        "Y",
        "保留|说明",
    ], "independent Markdown row parser does not preserve escaped pipes"
    route_errors = onboarding_route_contract_errors(
        (ROOT / "huifu-merchant-onboarding/SKILL.md").read_text(encoding="utf-8"),
        (
            ROOT
            / "huifu-merchant-onboarding/references/merchant-onboarding-business-open.md"
        ).read_text(encoding="utf-8"),
        (
            ROOT
            / "huifu-merchant-onboarding/references/merchant-onboarding-business-open-modify.md"
        ).read_text(encoding="utf-8"),
        (SOURCE_DIR / "business-open.md").read_text(encoding="utf-8"),
        (SOURCE_DIR / "business-open-modify.md").read_text(encoding="utf-8"),
        json.loads((ROOT / "tests/regression/onboarding.json").read_text(encoding="utf-8")),
    )
    assert not route_errors, "onboarding route contract mismatch: " + "; ".join(route_errors)
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    for source in lock["sources"]:
        raw = (SOURCE_DIR / source["filename"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == source["sha256"], (
            f"{source['filename']}: locked byte digest mismatch"
        )

    expected = expected_records(lock)
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
    expected_structure = parent_and_array_properties(expected)
    actual_structure = parent_and_array_properties(actual)
    assert expected_structure == actual_structure, "parent/array/node-type properties differ"

    counts_by_interface = {
        source["title"]: sum(key[0] == source["title"] for key in actual)
        for source in lock["sources"]
    }
    assert counts_by_interface == {
        source["title"]: source["field_count"] for source in lock["sources"]
    }
    direction_counts = {
        direction: sum(value[0] == direction for value in actual.values())
        for direction in ("request", "response", "callback")
    }
    structure_counts = {
        node_type: sum(value[2] == node_type for value in actual_structure.values())
        for node_type in ("parent", "leaf")
    }
    assert direction_counts == {
        key: lock["totals"][key] for key in ("request", "response", "callback")
    }
    assert structure_counts == {
        key: lock["totals"][key] for key in ("parent", "leaf")
    }
    assert len(actual) == lock["totals"]["fields"]
    print(
        "independent onboarding source contract validated: "
        f"{len(actual)} unique nodes; directions={direction_counts}; "
        f"structure={structure_counts}; interfaces={counts_by_interface}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
