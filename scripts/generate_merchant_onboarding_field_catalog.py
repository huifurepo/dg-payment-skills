#!/usr/bin/env python3
"""Generate the complete six-interface merchant-onboarding field catalog.

The official Markdown uses span IDs plus detached ``extend-table`` blocks for
nested objects. This generator resolves that graph and emits every reachable
field path. Use ``--source-dir`` with downloaded source files for reproducible
local generation, or omit it to fetch the six official URLs directly.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "huifu-pay-integration/references/merchant-onboarding-complete-field-catalog.md"
)


@dataclass(frozen=True)
class SourceSpec:
    key: str
    title: str
    filename: str
    url: str
    root_labels: tuple[tuple[str, str], ...]
    expected_root_tables: int


SOURCES = (
    SourceSpec(
        "enterprise",
        "企业商户进件",
        "enterprise.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
            ("审核异步信封", "async.audit"),
            ("审核异步 data", "async.audit.data"),
        ),
        6,
    ),
    SourceSpec(
        "individual",
        "个人商户进件",
        "individual.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
            ("审核异步信封", "async.audit"),
            ("审核异步 data", "async.audit.data"),
        ),
        6,
    ),
    SourceSpec(
        "business_open",
        "商户业务开通",
        "business-open.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
            ("申请审核异步信封", "async.audit"),
            ("申请审核异步 data", "async.audit.data"),
            ("逐业务结果异步", "async.business"),
            ("电子协议异步", "async.agreement"),
        ),
        8,
    ),
    SourceSpec(
        "detail_query",
        "商户详细信息查询",
        "detail-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("响应 data", "response.data"),
        ),
        4,
    ),
    SourceSpec(
        "status_query",
        "申请单状态查询",
        "status-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("响应 data", "response.data"),
        ),
        4,
    ),
)

IMAGE_URL = "https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json"
IMAGE_FILENAME = "image-upload.json"


@dataclass
class Field:
    name: str
    label: str
    field_type: str
    length: str
    required: str
    description: str
    child_id: str | None = None
    is_array: bool = False


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "huifu-skill-field-audit/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def load_source(source_dir: Path | None, filename: str, url: str) -> bytes:
    if source_dir is not None:
        return (source_dir / filename).read_bytes()
    return fetch(url)


def clean_cell(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "；", value, flags=re.I)
    value = re.sub(r"</?font[^>]*>", "", value, flags=re.I)
    value = re.sub(r"</?(?:span|div)[^>]*>", "", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip(" ；")
    # Resolve the two relative links present in the official query pages so the
    # generated local reference remains clickable and preserves the original
    # public target instead of pointing into this repository.
    value = value.replace(
        "](api_ggcsbm.md",
        "](https://paas.huifu.com/partners/api/doc/api_ggcsbm.md",
    )
    # Official descriptions contain production-looking example merchant IDs,
    # identity numbers, mobile numbers and a direct image URL. They are not
    # contract values or defaults, so redact them while retaining every field
    # rule, enum, condition and external documentation address.
    value = re.sub(
        r"\[[^\]]*\]\(https?://[^)\s]+\.(?:jpe?g|png|bmp)(?:\?[^)]*)?\)",
        "[官网示例图片已省略]",
        value,
        flags=re.I,
    )
    value = re.sub(
        r"https?://[^\s)]+\.(?:jpe?g|png|bmp)(?:[?#][^\s)]*)?",
        "[官网示例图片已省略]",
        value,
        flags=re.I,
    )
    value = re.sub(r"(?<!\d)1[3-9]\d{9}(?!\d)", "[官网示例已脱敏]", value)
    value = re.sub(r"(?<!\d)\d{16,32}(?!\d)", "[官网示例已脱敏]", value)
    return value


def parse_field_row(line: str) -> Field | None:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) < 6:
        return None
    raw_name = cells[0]
    child_match = re.search(r'class="[^"]*\bextend\s+([\w-]+)[^"]*"', raw_name)
    child_id = child_match.group(1) if child_match else None
    name = clean_cell(raw_name)
    if not name or name == "参数":
        return None
    description = clean_cell(" | ".join(cells[5:]))
    # Do not infer an array from a ``*_list`` name. The business-open source
    # explicitly defines some such fields as Object (for example
    # contact_file_list and sales_scenes_file_list).
    is_array = field_type_is_array = clean_cell(cells[2]).lower() == "array"
    is_array = field_type_is_array or "jsonarray" in description.lower()
    return Field(
        name=name,
        label=clean_cell(cells[1]),
        field_type=clean_cell(cells[2]) or "—",
        length=clean_cell(cells[3]) or "—",
        required=clean_cell(cells[4]) or "—",
        description=description or "—",
        child_id=child_id,
        is_array=is_array,
    )


def parse_markdown_tables(text: str) -> tuple[list[list[Field]], dict[str, list[Field]]]:
    lines = text.splitlines()
    tables: list[tuple[str | None, list[Field]]] = []
    pending_id: str | None = None
    index = 0
    while index < len(lines):
        id_match = re.search(r"div:extend-table\s+([\w-]+)-table", lines[index])
        if id_match:
            pending_id = id_match.group(1)
        if not re.match(r"^\|\s*参数", lines[index]):
            index += 1
            continue

        table_id = pending_id
        pending_id = None
        rows: list[Field] = []
        index += 2  # skip the alignment row
        if table_id is None:
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                field = parse_field_row(lines[index])
                if field is not None:
                    rows.append(field)
                index += 1
        else:
            # Official docs contain at least one wrapped row without a leading
            # pipe. Continue to the explicit extend:end marker and collect all
            # subsequent valid rows instead of truncating the nested table.
            while index < len(lines) and "<!-- extend:end -->" not in lines[index]:
                if lines[index].lstrip().startswith("|"):
                    field = parse_field_row(lines[index])
                    if field is not None:
                        rows.append(field)
                index += 1
        tables.append((table_id, rows))

    roots = [rows for table_id, rows in tables if table_id is None]
    nested = {table_id: rows for table_id, rows in tables if table_id is not None}
    return roots, nested


def escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def flatten_fields(
    fields: list[Field],
    nested: dict[str, list[Field]],
    prefix: str,
    visited_ids: set[str],
    stack: tuple[str, ...] = (),
) -> list[tuple[str, Field, int]]:
    flattened: list[tuple[str, Field, int]] = []
    for field in fields:
        suffix = "[]" if field.is_array and field.child_id else ""
        path = f"{prefix}.{field.name}{suffix}" if prefix else f"{field.name}{suffix}"
        depth = path.count(".") + 1
        flattened.append((path, field, depth))
        if field.child_id is None:
            continue
        if field.child_id in stack:
            raise ValueError(f"nested table cycle detected: {' -> '.join((*stack, field.child_id))}")
        child_fields = nested.get(field.child_id)
        if child_fields is None:
            raise ValueError(f"missing extend-table for {path}: {field.child_id}")
        visited_ids.add(field.child_id)
        flattened.extend(
            flatten_fields(
                child_fields,
                nested,
                path,
                visited_ids,
                (*stack, field.child_id),
            )
        )
    return flattened


def render_surface(
    label: str,
    prefix: str,
    fields: list[Field],
    nested: dict[str, list[Field]],
    visited_ids: set[str],
) -> tuple[str, int, int]:
    flattened = flatten_fields(fields, nested, prefix, visited_ids)
    lines = [
        f"### {label}",
        "",
        "| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |",
        "| --- | --- | --- | ---: | :---: | --- |",
    ]
    for path, field, _depth in flattened:
        lines.append(
            f"| `{escape_table(path)}` | {escape_table(field.label)} | "
            f"`{escape_table(field.field_type)}` | `{escape_table(field.length)}` | "
            f"`{escape_table(field.required)}` | {escape_table(field.description)} |"
        )
    lines.append("")
    max_depth = max((depth for _path, _field, depth in flattened), default=0)
    return "\n".join(lines), len(flattened), max_depth


def render_markdown_source(spec: SourceSpec, content: bytes) -> tuple[str, dict[str, object]]:
    text = content.decode("utf-8-sig")
    roots, nested = parse_markdown_tables(text)
    if len(roots) != spec.expected_root_tables:
        raise ValueError(
            f"{spec.filename}: expected {spec.expected_root_tables} root tables, found {len(roots)}"
        )
    if len(spec.root_labels) != len(roots):
        raise ValueError(f"{spec.filename}: root label count mismatch")

    visited_ids: set[str] = set()
    rendered: list[str] = [
        f"## {spec.title}",
        "",
        f"- 原始地址：<{spec.url}>",
        f"- SHA-256：`{hashlib.sha256(content).hexdigest()}`",
        "- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。",
        "",
    ]
    surface_counts: dict[str, int] = {}
    max_depth = 0
    for (label, prefix), fields in zip(spec.root_labels, roots, strict=True):
        surface_text, count, surface_depth = render_surface(
            label, prefix, fields, nested, visited_ids
        )
        rendered.append(surface_text)
        surface_counts[label] = count
        max_depth = max(max_depth, surface_depth)

    unreachable = sorted(set(nested) - visited_ids)
    if unreachable:
        raise ValueError(f"{spec.filename}: unreachable extend-tables: {unreachable}")
    summary = {
        "source": spec.url,
        "sha256": hashlib.sha256(content).hexdigest(),
        "root_tables": len(roots),
        "extend_tables": len(nested),
        "surface_counts": surface_counts,
        "total_fields": sum(surface_counts.values()),
        "max_depth": max_depth,
    }
    return "\n".join(rendered), summary


def render_image_source(content: bytes) -> tuple[str, dict[str, object]]:
    document = json.loads(content)
    params = document["requestBody"]["params"]
    lines = [
        "## 图片上传",
        "",
        f"- 原始地址：<{IMAGE_URL}>",
        f"- SHA-256：`{hashlib.sha256(content).hexdigest()}`",
        f"- URI：`{document['uri']}`；接口元数据 `sign={str(document['sign']).lower()}`。官方 JSON 未给 HTTP method、host 或 Content-Type。",
        "- 官方 JSON 未定义响应字段；不得猜测 `file_id`、其他响应路径或重试语义。",
        "",
        "### 请求信封与 data",
        "",
        "| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |",
        "| --- | --- | --- | ---: | :---: | --- |",
        "| `request.sys_id` | — | `—` | `—` | `—` | 仅见于 `requestDemo`；官方 JSON 未给正式顶层 schema。 |",
        "| `request.product_id` | — | `—` | `—` | `—` | 仅见于 `requestDemo`；官方 JSON 未给正式顶层 schema。 |",
        "| `request.data` | — | `—` | `—` | `—` | 仅见于 `requestDemo`；`requestBody.params` 定义下列五个 data 字段。 |",
        "| `request.file` | 图片文件流 | `—` | `—` | `—` | 仅见于 `requestDemo`，且字段说明只确认它与 `request.data.file_url` 不能同时上传；不得猜测类型或必填性。 |",
    ]
    for item in params:
        description = clean_cell(item.get("remark", ""))
        lines.append(
            "| `request.data.{}` | {} | `{}` | `{}` | `{}` | {} |".format(
                escape_table(item["name"]),
                escape_table(item.get("desc", "")),
                escape_table(item.get("fieldType", "—")),
                escape_table(item.get("maxLength", "—") or "—"),
                escape_table(item.get("isRequired", "—")),
                escape_table(description),
            )
        )
    lines.append("")
    summary = {
        "source": IMAGE_URL,
        "sha256": hashlib.sha256(content).hexdigest(),
        "root_tables": 1,
        "extend_tables": 0,
        "surface_counts": {"请求信封与 data": 4 + len(params)},
        "total_fields": 4 + len(params),
        "max_depth": 3,
    }
    return "\n".join(lines), summary


def build_catalog(source_dir: Path | None) -> tuple[str, dict[str, dict[str, object]]]:
    sections: list[str] = []
    summary: dict[str, dict[str, object]] = {}
    for spec in SOURCES:
        content = load_source(source_dir, spec.filename, spec.url)
        section, source_summary = render_markdown_source(spec, content)
        sections.append(section)
        summary[spec.key] = source_summary
    image_content = load_source(source_dir, IMAGE_FILENAME, IMAGE_URL)
    image_section, image_summary = render_image_source(image_content)
    sections.insert(3, image_section)
    summary["image_upload"] = image_summary

    header = """# 商户进件六接口完整字段目录

本文件由仓库维护脚本从六份官方原文机械生成。它负责“字段不遗漏”；高风险枚举、默认值、条件冲突和输出边界仍同时读取 `merchant-onboarding-field-contracts.md` 及对应接口 reference。

安全说明：官方说明中的商户号、证件号、手机号、长流水和示例图片 URL 已机械脱敏；这些示例本来就不是默认值。字段规则、枚举、条件、材料编号和外部资料地址不做脱敏。

## 目录

- [生成覆盖摘要](#生成覆盖摘要)
- [企业商户进件](#企业商户进件)
- [个人商户进件](#个人商户进件)
- [商户业务开通](#商户业务开通)
- [图片上传](#图片上传)
- [商户详细信息查询](#商户详细信息查询)
- [申请单状态查询](#申请单状态查询)

使用规则：

1. 回答任一接口字段问题时，先在本文件定位完整路径，再读取对应接口 reference 的约束说明。
2. 不得只读取顶层字段后推断嵌套对象；必须沿 `[]` / 对象路径读到叶子层。
3. 官方表格自身冲突时保留原始类型、长度、必填和说明，不自行“修正”；在答案中明确标记 `[官方文档口径冲突]`。
4. 字段说明引用外部网页或文件时，再读取 `merchant-onboarding-external-resources.md` 并给出原始地址。

## 生成覆盖摘要

| 接口 | 字段路径总数 | 扩展表数量 | 最大路径深度 |
| --- | ---: | ---: | ---: |
"""
    ordered_keys = (
        "enterprise",
        "individual",
        "business_open",
        "image_upload",
        "detail_query",
        "status_query",
    )
    title_by_key = {spec.key: spec.title for spec in SOURCES} | {"image_upload": "图片上传"}
    summary_lines = []
    for key in ordered_keys:
        item = summary[key]
        summary_lines.append(
            f"| {title_by_key[key]} | {item['total_fields']} | {item['extend_tables']} | {item['max_depth']} |"
        )
    catalog = header + "\n".join(summary_lines) + "\n\n" + "\n".join(sections)
    return catalog.rstrip() + "\n", summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    catalog, summary = build_catalog(args.source_dir)
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != catalog:
            print(f"catalog is stale: {args.output}", file=sys.stderr)
            return 1
        print(f"catalog is current: {args.output}")
    else:
        args.output.write_text(catalog, encoding="utf-8")
        print(f"generated: {args.output}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
