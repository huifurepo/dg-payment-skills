#!/usr/bin/env python3
"""Generate the complete user-onboarding field catalog.

The official Markdown stores nested schemas in detached ``extend-table``
blocks.  This generator resolves that graph, emits every reachable field path,
and can operate only on the immutable source snapshot selected by the user
onboarding source lock.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
from skill_validation_config import USER_ONBOARDING_SOURCE_LOCK
LOCK = USER_ONBOARDING_SOURCE_LOCK
DEFAULT_OUTPUT = (
    ROOT
    / "huifu-merchant-onboarding/references/user-onboarding-complete-field-catalog.md"
)


@dataclass(frozen=True)
class SourceSpec:
    key: str
    title: str
    filename: str
    url: str
    surfaces: tuple[tuple[str, str], ...]


SOURCES = (
    SourceSpec(
        "user_enterprise",
        "企业用户开户",
        "enterprise.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxzc.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    SourceSpec(
        "user_individual",
        "个人用户开户",
        "individual.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxzc.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    SourceSpec(
        "user_business_open",
        "用户业务入驻",
        "business-open.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrz.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
            ("异步通知信封", "async"),
            ("异步通知 data", "async.data"),
        ),
    ),
    SourceSpec(
        "user_apply_query",
        "用户申请单状态查询",
        "application-status-query.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhsqdzt.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    SourceSpec(
        "user_detail_query",
        "用户信息查询",
        "detail-query.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhywcx.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    SourceSpec(
        "user_enterprise_modify",
        "企业用户基本信息修改",
        "enterprise-modify.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxxg.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    SourceSpec(
        "user_individual_modify",
        "个人用户基本信息修改",
        "individual-modify.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxxg.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    SourceSpec(
        "user_business_modify",
        "用户业务入驻修改",
        "business-modify.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrzxg.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
            ("异步通知信封", "async"),
            ("异步通知 data", "async.data"),
        ),
    ),
    SourceSpec(
        "user_list_query",
        "用户列表查询",
        "list-query.md",
        "https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhlbcx.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
)


@dataclass(frozen=True)
class Field:
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


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "huifu-user-skill-field-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def locked_source_dir() -> Path:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    snapshot_id = lock.get("source_snapshot_id", lock["source_date"])
    return (
        ROOT
        / "maintainer-contracts/official-sources/user-onboarding"
        / snapshot_id
    )


def refresh_sources(target: Path, source_key: str | None = None) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        if source_key is not None and source.key != source_key:
            continue
        (target / source.filename).write_bytes(fetch(source.url))


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


def parse_page_field_notes(text: str) -> dict[str, str]:
    """Collect field-specific notes that the official page keeps outside tables."""
    notes: dict[str, str] = {}
    for line in visible_lines(text):
        match = re.match(r"^\s*-\s*\[([A-Za-z0-9_]+)\]\s*[：:]\s*(.+?)\s*$", line)
        if not match:
            continue
        name, description = match.groups()
        if name in notes:
            raise ValueError(f"duplicate page-level field note for {name}")
        notes[name] = clean(description)
    return notes


def parse_explicit_page_field_notes(source_key: str, text: str) -> dict[str, str]:
    """Resolve unlabelled official notes whose target fields are unambiguous."""
    if source_key == "user_enterprise_modify":
        matches = [
            clean(line.strip().removeprefix("- "))
            for line in visible_lines(text)
            if line.strip().startswith("- 如要修改法人证件")
        ]
        if len(matches) != 1:
            raise ValueError(
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
        clean(line.strip().removeprefix("- "))
        for line in visible_lines(text)
        if line.strip().startswith("- 系统会做法人姓名与身份证号的实名认证")
    ]
    if len(matches) != 1:
        raise ValueError(
            "enterprise identity-verification note must occur exactly once"
        )
    return {
        "request.data.legal_name": matches[0],
        "request.data.legal_cert_no": matches[0],
    }


def clean(value: str) -> str:
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


def normalize_links(value: str, source_url: str) -> str:
    def replace(match: re.Match[str]) -> str:
        label, target = match.groups()
        parsed = urllib.parse.urlsplit(target)
        if parsed.scheme in {"http", "https"}:
            return match.group(0)
        if parsed.scheme or target.startswith("//"):
            raise ValueError(f"unsupported documentation link: {target}")
        resolved = urllib.parse.urljoin(source_url, target)
        return f"[{label}]({resolved})（官网相对地址原文：`{target}`）"

    return re.sub(r"\[([^\]]+)\]\(([^()\s]+)\)", replace, value)


def redact_field_examples(name: str, description: str) -> str:
    if name not in SENSITIVE_EXAMPLE_FIELDS:
        return description
    return re.sub(
        r"(示例值\s*[：:])[^；|]*",
        r"\1[官网敏感示例已脱敏]",
        description,
    )


def split_row(row: str) -> list[str]:
    body = row.strip().removeprefix("|").removesuffix("|")
    cells: list[str] = []
    cell: list[str] = []
    for char in body:
        if char == "|":
            slash_count = 0
            for previous in reversed(cell):
                if previous != "\\":
                    break
                slash_count += 1
            if slash_count % 2:
                cell.pop()
                cell.append("|")
                continue
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
    cells.append("".join(cell).strip())
    return cells


def logical_row(lines: list[str], index: int) -> tuple[str, int]:
    row = lines[index].strip()
    index += 1
    while not row.rstrip().endswith("|"):
        if index >= len(lines) or "<!-- extend:end -->" in lines[index]:
            raise ValueError(f"unterminated table row near line {index}")
        continuation = lines[index].strip()
        if not continuation or continuation.startswith(("<!--", "#")):
            break
        if continuation.startswith("|") and continuation != "|":
            break
        row = f"{row} {continuation}"
        index += 1
    return row, index


def table_columns(row: str) -> dict[str, int] | None:
    """Return semantic column indexes for an official contract table.

    The newer onboarding pages are not consistent about Markdown emphasis or
    the order of the ``长度`` and ``必填`` columns.  Resolve columns from the
    header instead of silently interpreting the page's visual order as the
    older fixed schema.  Three-column enum/reference tables are deliberately
    excluded from the wire-field catalog.
    """

    cells = split_row(row)
    headings = [clean(cell).strip("* ") for cell in cells]
    if len(headings) < 6 or headings[0] not in {"参数", "出参名"}:
        return None

    def find(*names: str) -> int:
        for index, heading in enumerate(headings):
            if heading in names:
                return index
        raise ValueError(f"missing contract-table column {names}: {headings}")

    return {
        "name": 0,
        "label": 1,
        "kind": find("定义", "类型"),
        "length": find("长度"),
        "required": find("必填", "非空"),
        "description": find("说明"),
    }


def parse_field(
    row: str,
    source_url: str,
    columns: dict[str, int],
) -> Field | None:
    cells = split_row(row)
    if len(cells) <= max(columns.values()):
        return None
    raw_name = cells[columns["name"]]
    child_match = re.search(r'class="[^"]*\bextend\s+([\w-]+)[^"]*"', raw_name)
    name = clean(raw_name).strip("* ")
    if not name or name in {"参数", "出参名"}:
        return None
    description = normalize_links(
        clean(" | ".join(cells[columns["description"] :])),
        source_url,
    ) or "—"
    description = redact_field_examples(name, description)
    kind = clean(cells[columns["kind"]]) or "—"
    return Field(
        name=name,
        label=clean(cells[columns["label"]]) or "—",
        kind=kind,
        length=clean(cells[columns["length"]]) or "—",
        required=clean(cells[columns["required"]]) or "—",
        description=description,
        child=child_match.group(1) if child_match else None,
        array=kind.lower() == "array" or "jsonarray" in description.lower(),
    )


def parse_tables(text: str, source_url: str) -> tuple[list[list[Field]], dict[str, list[Field]]]:
    lines = visible_lines(text)
    tables: list[tuple[str | None, list[Field]]] = []
    pending: str | None = None
    index = 0
    while index < len(lines):
        marker = re.search(r"div:extend-table\s+([\w-]+)-table", lines[index])
        if marker:
            pending = marker.group(1)
        columns = table_columns(lines[index])
        if columns is None:
            index += 1
            continue
        table_id, pending = pending, None
        rows: list[Field] = []
        index += 2
        if table_id is None:
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                row, index = logical_row(lines, index)
                field = parse_field(row, source_url, columns)
                if field:
                    rows.append(field)
        else:
            while index < len(lines) and "<!-- extend:end -->" not in lines[index]:
                if lines[index].lstrip().startswith("|"):
                    row, index = logical_row(lines, index)
                    field = parse_field(row, source_url, columns)
                    if field:
                        rows.append(field)
                else:
                    index += 1
        tables.append((table_id, rows))
    roots = [rows for table_id, rows in tables if table_id is None]
    nested = {table_id: rows for table_id, rows in tables if table_id is not None}
    return roots, nested


def flatten(
    fields: list[Field],
    nested: dict[str, list[Field]],
    prefix: str,
    used: set[str],
    stack: tuple[str, ...] = (),
) -> list[tuple[str, Field, int]]:
    result: list[tuple[str, Field, int]] = []
    for field in fields:
        base = f"{prefix}.{field.name}"
        path = f"{base}[]" if field.array else base
        result.append((path, field, path.count(".") + 1))
        if not field.child:
            continue
        if field.child in stack:
            raise ValueError(f"nested table cycle at {field.child}")
        if field.child not in nested:
            raise ValueError(f"missing extend-table {field.child} for {path}")
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


def escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_source(spec: SourceSpec, content: bytes) -> tuple[str, dict[str, object]]:
    text = content.decode("utf-8-sig")
    roots, nested = parse_tables(text, spec.url)
    page_notes = parse_page_field_notes(text)
    page_note_matches = {name: 0 for name in page_notes}
    explicit_page_notes = parse_explicit_page_field_notes(spec.key, text)
    explicit_page_note_matches = {path: 0 for path in explicit_page_notes}
    if len(roots) != len(spec.surfaces):
        raise ValueError(
            f"{spec.filename}: expected {len(spec.surfaces)} root tables, found {len(roots)}"
        )
    used: set[str] = set()
    sections = [
        f"## {spec.title}",
        "",
        f"- 原始地址：<{spec.url}>",
        f"- SHA-256：`{hashlib.sha256(content).hexdigest()}`",
        "- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。",
        "",
    ]
    counts: dict[str, int] = {}
    all_paths: list[str] = []
    max_depth = 0
    for (label, prefix), fields in zip(spec.surfaces, roots, strict=True):
        flattened = flatten(fields, nested, prefix, used)
        counts[label] = len(flattened)
        all_paths.extend(path for path, _field, _depth in flattened)
        max_depth = max(max_depth, *(depth for _path, _field, depth in flattened))
        sections.extend(
            [
                f"### {label}",
                "",
                "| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |",
                "| --- | --- | --- | ---: | :---: | --- |",
            ]
        )
        for path, field, _depth in flattened:
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
            sections.append(
                f"| `{escape(path)}` | {escape(field.label)} | `{escape(field.kind)}` | "
                f"`{escape(field.length)}` | `{escape(field.required)}` | "
                f"{escape(description)} |"
            )
        sections.append("")
    unreachable = sorted(set(nested) - used)
    if unreachable:
        raise ValueError(f"{spec.filename}: unreachable extend-tables: {unreachable}")
    invalid_page_notes = {
        name: count for name, count in page_note_matches.items() if count != 1
    }
    if invalid_page_notes:
        raise ValueError(
            f"{spec.filename}: page-level field notes must resolve once: "
            f"{invalid_page_notes}"
        )
    invalid_explicit_page_notes = {
        path: count
        for path, count in explicit_page_note_matches.items()
        if count != 1
    }
    if invalid_explicit_page_notes:
        raise ValueError(
            f"{spec.filename}: explicit page-level field notes must resolve once: "
            f"{invalid_explicit_page_notes}"
        )
    return "\n".join(sections), {
        "source": spec.url,
        "sha256": hashlib.sha256(content).hexdigest(),
        "root_tables": len(roots),
        "extend_tables": len(nested),
        "surface_counts": counts,
        "total_fields": len(all_paths),
        "max_depth": max_depth,
    }


def build_catalog(source_dir: Path) -> tuple[str, dict[str, dict[str, object]]]:
    sections: list[str] = []
    summaries: dict[str, dict[str, object]] = {}
    for spec in SOURCES:
        content = (source_dir / spec.filename).read_bytes()
        section, summary = render_source(spec, content)
        sections.append(section)
        summaries[spec.key] = summary

    summary_rows = [
        f"| {spec.title} | {summaries[spec.key]['total_fields']} | "
        f"{summaries[spec.key]['extend_tables']} | {summaries[spec.key]['max_depth']} |"
        for spec in SOURCES
    ]
    header = """# 用户进件完整字段目录

本文件由仓库维护脚本从锁定的官方原文机械生成，负责保证字段路径不遗漏。条件必填、官方口径冲突、路由和安全边界仍需同时读取对应的原子接口 reference。

安全说明：官网说明中的用户号、证件号、手机号、邮箱、长流水和示例图片地址已机械脱敏；字段枚举、条件、材料编号和资料链接保持原文。

## 目录

- 使用规则
- 生成覆盖摘要
- 企业用户开户
- 个人用户开户
- 用户业务入驻
- 用户申请单状态查询
- 用户信息查询
- 企业用户基本信息修改
- 个人用户基本信息修改
- 用户业务入驻修改
- 用户列表查询

## 使用规则

1. 必须以完整路径区分同名字段，不得按叶字段名合并。
2. `huifu_id` 必须结合接口与路径解释为用户号、渠道号或商户号，不得统一称为商户号。
3. String(JSON) 的对象/数组边界以完整路径保留；不得扁平化后复用商户进件 DTO。
4. 官网类型、长度、必填和示例互相冲突时，目录保留表格原值并标记为官方证据，不自行修正。
5. 异步通知仅来自用户业务入驻及其修改；本目录不补写官网未定义的 ACK、重试、去重或超时规则。

## 生成覆盖摘要

| 接口 | 字段路径总数 | 扩展表数量 | 最大路径深度 |
| --- | ---: | ---: | ---: |
"""
    catalog = header + "\n".join(summary_rows) + "\n\n" + "\n".join(sections)
    return catalog.rstrip() + "\n", summaries


def validate_summary(summary: dict[str, dict[str, object]]) -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    by_key = {source["key"]: source for source in lock["sources"]}
    for key, item in summary.items():
        expected = by_key[key]
        assert item["sha256"] == expected["sha256"], f"{key}: digest mismatch"
        assert item["total_fields"] == expected["field_count"], f"{key}: field count mismatch"
    assert sum(item["total_fields"] for item in summary.values()) == lock["totals"]["fields"]
    assert sum(item["root_tables"] for item in summary.values()) == lock["totals"]["root_tables"]
    assert sum(item["extend_tables"] for item in summary.values()) == (
        lock["totals"]["extend_tables"]
    )


def main() -> int:
    assert split_row(r"| sys_id | 系统\|编号 | String | 32 | Y | 保留\|说明 |") == [
        "sys_id",
        "系统|编号",
        "String",
        "32",
        "Y",
        "保留|说明",
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--locked-source-dir", action="store_true")
    parser.add_argument("--refresh-source-dir", type=Path)
    parser.add_argument("--refresh-source-key", choices=[source.key for source in SOURCES])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    selected = sum(
        value is not None and value is not False
        for value in (args.source_dir, args.locked_source_dir, args.refresh_source_dir)
    )
    if selected > 1:
        parser.error("source selection options are mutually exclusive")
    source_dir = args.source_dir or locked_source_dir()
    if args.refresh_source_dir is not None:
        refresh_sources(args.refresh_source_dir, args.refresh_source_key)
        source_dir = args.refresh_source_dir
    elif args.refresh_source_key is not None:
        parser.error("--refresh-source-key requires --refresh-source-dir")
    catalog, summary = build_catalog(source_dir)
    validate_summary(summary)
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != catalog:
            print(f"catalog is stale: {args.output}", file=sys.stderr)
            return 1
        print(f"catalog is current: {args.output}")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(catalog, encoding="utf-8")
        print(f"generated: {args.output}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
