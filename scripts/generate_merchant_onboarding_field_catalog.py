#!/usr/bin/env python3
"""Generate the complete twelve-interface merchant-onboarding field catalog.

The official Markdown uses span IDs plus detached ``extend-table`` blocks for
nested objects. This generator resolves that graph and emits every reachable
field path. Use ``--source-dir`` with downloaded source files for reproducible
local generation, or omit it to fetch the twelve official URLs directly.
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

from skill_validation_config import onboarding_source_dir
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md"
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
    SourceSpec(
        "business_open_modify",
        "商户业务开通修改",
        "business-open-modify.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
            ("审核异步信封", "async.audit"),
            ("审核异步 data", "async.audit.data"),
            ("逐业务结果异步", "async.business"),
            ("电子协议异步", "async.agreement"),
        ),
        8,
    ),
    SourceSpec(
        "basic_info_modify",
        "商户基本信息修改",
        "basic-info-modify.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
            ("审核异步 data", "async.audit.data"),
            ("电子协议异步", "async.agreement"),
        ),
        6,
    ),
    SourceSpec(
        "rate_query",
        "商户费率信息查询",
        "rate-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("响应 data", "response.data"),
        ),
        4,
    ),
    SourceSpec(
        "status_change",
        "商户状态变更",
        "status-change.md",
        "https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
        4,
    ),
    SourceSpec(
        "sms_send",
        "商户短信发送",
        "sms-send.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("响应 data", "response.data"),
        ),
        4,
    ),
    SourceSpec(
        "multifee_config",
        "商户多费率配置",
        "multifee-config.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("响应 data", "response.data"),
        ),
        4,
    ),
    SourceSpec(
        "multifee_query",
        "商户多费率配置查询",
        "multifee-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md",
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


def refresh_sources(target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        (target_dir / source.filename).write_bytes(fetch(source.url))
    (target_dir / IMAGE_FILENAME).write_bytes(fetch(IMAGE_URL))


def clean_cell(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "；", value, flags=re.I)
    value = re.sub(r"</?font[^>]*>", "", value, flags=re.I)
    value = re.sub(r"</?(?:span|div)[^>]*>", "", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip(" ；")
    value = re.sub(r"(?:\s*；\s*){2,}", "；", value)
    # Official descriptions contain production-looking example merchant IDs,
    # identity numbers, mobile numbers and a direct image URL. They are not
    # contract values or defaults, so redact them while retaining every field
    # rule, enum, condition and external documentation address.
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


def normalize_description_links(
    value: str,
    source_url: str,
    source_headings: frozenset[str],
) -> str:
    """Resolve source-relative field links without losing their source form."""

    common_return_codes_url = (
        "https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md"
    )
    async_intro_url = (
        "https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md"
    )
    aggregation_create_url = (
        "https://paas.huifu.com/partners/lightning/api/jhzfxd.md"
    )

    def replace_link(match: re.Match[str]) -> str:
        label, target = match.groups()
        parsed = urllib.parse.urlsplit(target)
        if parsed.scheme in {"http", "https"}:
            suffix = match.group(0)
            if parsed.scheme == "http":
                suffix += "（官网原始地址为非 HTTPS，不得静默改写）"
            if parsed.hostname and parsed.hostname.endswith("huifutest.com"):
                suffix += "（官网原文测试域，不作为生产地址）"
            return suffix
        if parsed.scheme or target.startswith("//"):
            raise ValueError(f"unsupported field-description link target: {target}")
        # These public-code-table links are authored relative to the rendered
        # common-document namespace, not the nested source Markdown directory.
        if parsed.path == "api_ggcsbm.md":
            resolved = urllib.parse.urljoin(
                "https://paas.huifu.com/partners/api/doc/",
                target,
            )
        else:
            resolved = urllib.parse.urljoin(source_url, target)
        suffix = (
            f"[{label}]({resolved})"
            f"（官网相对地址原文：`{target}`）"
        )
        resolved_missing_anchor = False
        if target == "#业务返回码":
            suffix += (
                f"（公共返回码全集：[返回码]({common_return_codes_url})；"
                "接口页专属码与公共码需合并排查）"
            )
            resolved_missing_anchor = True
        elif source_url == aggregation_create_url and target == "#异步返回参数":
            suffix += (
                "（已确认同时指向"
                f"[聚合正扫异步返回参数]({aggregation_create_url}#聚合正扫异步返回参数)"
                "和"
                f"[聚合反扫异步返回参数]({aggregation_create_url}#聚合反扫异步返回参数)"
                "两套通知参数；通用传输、验签、ACK、重试与幂等规则见"
                f"[异步消息简介]({async_intro_url})）"
            )
            resolved_missing_anchor = True
        if (
            target.startswith("#")
            and target[1:] not in source_headings
            and not resolved_missing_anchor
        ):
            suffix += "（官网原始锚点在当前快照无同名标题，`[需要人工确认]`）"
        return suffix

    return re.sub(r"\[([^\]]+)\]\(([^()\s]+)\)", replace_link, value)


def split_markdown_row(line: str) -> list[str]:
    r"""Split a Markdown table row without treating ``\|`` as a delimiter."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    cells: list[str] = []
    cell: list[str] = []
    for char in body:
        if char == "|":
            trailing_backslashes = 0
            for previous in reversed(cell):
                if previous != "\\":
                    break
                trailing_backslashes += 1
            if trailing_backslashes % 2:
                cell.pop()
                cell.append("|")
                continue
            cells.append("".join(cell).strip())
            cell = []
            continue
        cell.append(char)
    cells.append("".join(cell).strip())
    return cells


def parse_field_row(
    line: str,
    source_url: str,
    source_headings: frozenset[str],
) -> Field | None:
    cells = split_markdown_row(line)
    if len(cells) < 6:
        return None
    raw_name = cells[0]
    child_match = re.search(r'class="[^"]*\bextend\s+([\w-]+)[^"]*"', raw_name)
    child_id = child_match.group(1) if child_match else None
    name = clean_cell(raw_name)
    if not name or name == "参数":
        return None
    description = normalize_description_links(
        clean_cell(" | ".join(cells[5:])),
        source_url,
        source_headings,
    )
    # Do not infer an array from a ``*_list`` name. The business-open source
    # explicitly defines some such fields as Object (for example
    # contact_file_list and sales_scenes_file_list).
    is_array = field_type_is_array = clean_cell(cells[2]).lower() == "array"
    normalized_description = description.lower()
    is_array = field_type_is_array or "jsonarray" in normalized_description
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


def consume_markdown_row(lines: list[str], index: int) -> tuple[str, int]:
    """Return one logical pipe-table row and the next unread line index."""
    row = lines[index].strip()
    if not row.startswith("|"):
        raise ValueError(f"expected Markdown table row at line {index + 1}")
    index += 1
    while not row.rstrip().endswith("|"):
        if index >= len(lines) or "<!-- extend:end -->" in lines[index]:
            raise ValueError(f"unterminated Markdown table row near line {index}")
        continuation = lines[index].strip()
        if not continuation or continuation.startswith(("<!--", "#")):
            return row, index
        if continuation.startswith("|") and continuation != "|":
            # A few official rows omit their final delimiter without carrying
            # content onto the next physical line. Leave the following row
            # unread instead of merging two distinct fields.
            return row, index
        row = f"{row} {continuation}"
        index += 1
    return row, index


def parse_markdown_tables(
    text: str,
    source_url: str,
) -> tuple[list[list[Field]], dict[str, list[Field]]]:
    # Preserve active one-line ``extend`` markers while excluding genuinely
    # commented-out multi-line blocks. The status-change source contains a
    # retired ``file_list`` contract inside such a block; treating it as live
    # would invent fields that the official page explicitly removed.
    lines: list[str] = []
    inside_multiline_comment = False
    for line in text.splitlines():
        if inside_multiline_comment:
            if "-->" in line:
                inside_multiline_comment = False
            continue
        if "<!--" in line and "-->" not in line:
            inside_multiline_comment = True
            continue
        lines.append(line)
    source_headings = frozenset(
        re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
        for line in lines
        if (match := re.match(r"^#{1,6}\s+(.+?)\s*$", line))
    )
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
                logical_row, index = consume_markdown_row(lines, index)
                field = parse_field_row(logical_row, source_url, source_headings)
                if field is not None:
                    rows.append(field)
        else:
            # Official docs contain wrapped rows whose continuation line has no
            # leading pipe. Continue to the explicit extend:end marker while
            # assembling every physical fragment into one logical table row.
            while index < len(lines) and "<!-- extend:end -->" not in lines[index]:
                if lines[index].lstrip().startswith("|"):
                    logical_row, index = consume_markdown_row(lines, index)
                    field = parse_field_row(
                        logical_row,
                        source_url,
                        source_headings,
                    )
                    if field is not None:
                        rows.append(field)
                else:
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
    array_typo_paths: frozenset[str] = frozenset(),
) -> list[tuple[str, Field, int]]:
    flattened: list[tuple[str, Field, int]] = []
    for field in fields:
        base_path = f"{prefix}.{field.name}" if prefix else field.name
        description = field.description.lower()
        typo_array = base_path in array_typo_paths
        if typo_array:
            if not (
                "josnarray" in description
                and "集合" in field.description
                and "多条" in field.description
            ):
                raise ValueError(f"registered array typo evidence changed: {base_path}")
        elif "josnarray" in description:
            raise ValueError(f"unregistered josnArray marker: {base_path}")
        # Preserve scalar JSON arrays as arrays even when the official row has
        # no extend-table. Array identity comes from the declared type/format,
        # not from whether child fields happen to be documented.
        suffix = "[]" if field.is_array or typo_array else ""
        path = f"{base_path}{suffix}"
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
                array_typo_paths,
            )
        )
    return flattened


def render_surface(
    label: str,
    prefix: str,
    fields: list[Field],
    nested: dict[str, list[Field]],
    visited_ids: set[str],
    array_typo_paths: frozenset[str] = frozenset(),
) -> tuple[str, int, int]:
    flattened = flatten_fields(
        fields,
        nested,
        prefix,
        visited_ids,
        array_typo_paths=array_typo_paths,
    )
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
    roots, nested = parse_markdown_tables(text, spec.url)
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
        array_typo_paths = (
            frozenset({"async.business.reg_result_list"})
            if spec.key == "business_open_modify"
            else frozenset()
        )
        surface_text, count, surface_depth = render_surface(
            label,
            prefix,
            fields,
            nested,
            visited_ids,
            array_typo_paths,
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

    header = """# 商户进件十三接口完整字段目录

本文件由仓库维护脚本从十三份官方原文机械生成。它负责“字段不遗漏”；高风险枚举、默认值、条件冲突和输出边界仍同时读取 `merchant-onboarding-field-contracts.md` 及对应接口 reference。

安全说明：官方说明中的商户号、证件号、手机号、长流水和示例图片 URL 已机械脱敏；这些示例本来就不是默认值。字段规则、枚举、条件、材料编号和外部资料地址不做脱敏。

## 目录

- [生成覆盖摘要](#生成覆盖摘要)
- [企业商户进件](#企业商户进件)
- [个人商户进件](#个人商户进件)
- [商户业务开通](#商户业务开通)
- [图片上传](#图片上传)
- [商户详细信息查询](#商户详细信息查询)
- [申请单状态查询](#申请单状态查询)
- [商户业务开通修改](#商户业务开通修改)
- [商户基本信息修改](#商户基本信息修改)
- [商户费率信息查询](#商户费率信息查询)
- [商户状态变更](#商户状态变更)
- [商户短信发送](#商户短信发送)
- [商户多费率配置](#商户多费率配置)
- [商户多费率配置查询](#商户多费率配置查询)

使用规则：

1. 回答任一接口字段问题时，先在本文件定位完整路径，再读取对应接口 reference 的约束说明。
2. 不得只读取顶层字段后推断嵌套对象；必须沿 `[]` / 对象路径读到叶子层。
3. 不得按叶字段名去重：`request.data.prov_id/area_id` 是经营省市，`request.data.card_info.prov_id/area_id` 是结算卡省市；适用时两组都保留，后者只能位于 String(JSON) `card_info` 内。企业进件新增的 `request.data.material_card_info.prov_id/area_id` 属于补充对公同名账户；路径树原样保留官网 `Object` 类型列，但本项目已确认以“jsonObject字符串”说明为 wire 依据，request/response 的 `material_card_info` 均整体序列化或反序列化为 String(JSON Object)。详情响应的 `response.data.material_card_info.prov_id/area_id` 是独立响应路径。四组字段均不得合并。基本信息修改的 `card_info.area_id` 长度为 `8`，企业/个人进件对应路径长度为 `6`，新增请求 `material_card_info` 叶字段长度为空时保留 `—`。
4. 官方表格自身冲突时保留原始类型、长度、必填和说明，不自行“修正”；在答案中明确标记 `[官方文档口径冲突]`。
5. 字段说明引用外部网页或文件时，再读取 `merchant-onboarding-external-resources.md` 并给出原始地址。绝对链接保持官网值；相对链接按已登记的官方文档命名空间（无例外时按来源页）解析成可点击地址，同时保留官网相对地址原文。回调、跳转、下载、二维码或图片裸 URL 示例不是资料或默认值。

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
        "business_open_modify",
        "basic_info_modify",
        "rate_query",
        "status_change",
        "sms_send",
        "multifee_config",
        "multifee_query",
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
    parser_fixture = r"| sys_id | 系统\|编号 | String | 32 | Y | 保留\|说明 |"
    assert split_markdown_row(parser_fixture) == [
        "sys_id",
        "系统|编号",
        "String",
        "32",
        "Y",
        "保留|说明",
    ], "generator Markdown row parser does not preserve escaped pipes"
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument(
        "--locked-source-dir",
        action="store_true",
        help="read the snapshot selected by the current merchant-onboarding source lock",
    )
    parser.add_argument(
        "--refresh-source-dir",
        type=Path,
        help="download all official sources into this directory before generation",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    selected = sum(
        option is not None and option is not False
        for option in (
            args.source_dir,
            args.locked_source_dir,
            args.refresh_source_dir,
        )
    )
    if selected > 1:
        parser.error(
            "--source-dir, --locked-source-dir and --refresh-source-dir are mutually exclusive"
        )
    source_dir = args.source_dir
    if args.locked_source_dir:
        source_dir = onboarding_source_dir()
    if args.refresh_source_dir is not None:
        refresh_sources(args.refresh_source_dir)
        source_dir = args.refresh_source_dir

    catalog, summary = build_catalog(source_dir)
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
