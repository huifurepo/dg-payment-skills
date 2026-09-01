#!/usr/bin/env python3
"""Generate the complete locked payment API field-path catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from generate_merchant_onboarding_field_catalog import (
    escape_table,
    flatten_fields,
    parse_markdown_tables,
)
from validation_runtime import require_assertions_enabled
from skill_validation_config import PAYMENT_SOURCE_LOCK, payment_source_dir


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
LOCK = PAYMENT_SOURCE_LOCK
DEFAULT_OUTPUT = (
    ROOT / "huifu-pay-integration/references/payment-complete-field-catalog.md"
)


@dataclass(frozen=True)
class PaymentSource:
    key: str
    title: str
    filename: str
    url: str
    sha256: str
    surfaces: tuple[tuple[str, str], ...]


# Root tables are kept in the exact order of each locked official page. Prefixes
# make request, sync response and each async surface distinct, so a repeated leaf
# name is never used as an identity key.
SURFACES: dict[str, tuple[tuple[str, str], ...]] = {
    "aggregation-create": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("正扫异步信封", "async.forward"),
        ("正扫异步 resp_data", "async.forward.resp_data"),
        ("正扫解冻异步 data", "async.forward.unfreeze"),
        ("反扫异步信封", "async.reverse"),
        ("反扫异步 resp_data", "async.reverse.resp_data"),
    ),
    "aggregation-query": (
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "aggregation-close": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "aggregation-close-query": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "aggregation-refund": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
        ("退款异步载荷（官网未标外层字段名）", "async.unconfirmed_payload"),
    ),
    "aggregation-refund-query": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "reconciliation-v2": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
    "hosting-h5": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("支付异步 resp_data", "async.resp_data"),
    ),
    "hosting-alipay-mini": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("支付异步 resp_data", "async.resp_data"),
    ),
    "hosting-wechat-mini": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("支付异步 resp_data", "async.resp_data"),
        ("拆单支付异步 resp_data", "async.split.resp_data"),
    ),
    "hosting-douyin": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("支付异步载荷（官网未标外层字段名）", "async.unconfirmed_payload"),
    ),
    "hosting-query": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
    ),
    "hosting-refund": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("退款异步 data", "async.data"),
    ),
    "hosting-refund-query": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
    ),
    "hosting-close": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
        ("关单异步 resp_data", "async.resp_data"),
    ),
    "hosting-splitpay-query": (
        ("请求信封", "request"),
        ("请求 data", "request.data"),
        ("同步响应信封", "response"),
        ("同步响应 data", "response.data"),
    ),
    "split-detail-query": (
        ("请求信封", "request"),
        ("同步响应信封", "response"),
        ("请求 data", "request.data"),
        ("同步响应 data", "response.data"),
    ),
}


DISPLAY_NOTE = "方便文档展示"
AGGREGATION_QUERY_METHOD_GROUP = "response.data.method_expand"
KNOWN_STRING_JSON_SURFACES = {
    ("aggregation-create", "async.forward.resp_data"),
    ("aggregation-create", "async.reverse.resp_data"),
    ("hosting-h5", "async.resp_data"),
    ("hosting-alipay-mini", "async.resp_data"),
    ("hosting-wechat-mini", "async.resp_data"),
    ("hosting-wechat-mini", "async.split.resp_data"),
    ("hosting-close", "async.resp_data"),
}
UNKNOWN_NAMED_SURFACES = {
    ("hosting-refund", "async.data"),
}
UNKNOWN_OUTER_SURFACES = {
    ("aggregation-refund", "async.unconfirmed_payload"),
    ("hosting-douyin", "async.unconfirmed_payload"),
}
KNOWN_STRING_JSON_PATHS = {
    ("aggregation-create", "request.data.terminal_device_data"),
}


def normalized_path(path: str, display_paths: set[str]) -> str | None:
    """Remove only source-declared display nodes, never same-name real fields."""
    parts = path.split(".")
    for display_path in sorted(display_paths, key=lambda item: item.count(".")):
        display_parts = display_path.split(".")
        if parts[: len(display_parts)] != display_parts:
            continue
        if len(parts) == len(display_parts):
            return None
        del parts[len(display_parts) - 1]
    return ".".join(parts)


def is_string_json(field: object) -> bool:
    field_type = str(getattr(field, "field_type", "")).lower()
    description = str(getattr(field, "description", "")).lower()
    return field_type == "string" and "json" in description


def strip_string_array_marker(path: str) -> str:
    return path[:-2] if path.endswith("[]") else path


def decoded_from(container: str, actual: str) -> str:
    if actual == container:
        return "$[]" if container.endswith("[]") else "$"
    suffix = actual[len(container) + 1 :]
    return ("$[]." if container.endswith("[]") else "$.") + suffix


def transport_paths(
    path: str,
    flattened: list[tuple[str, object, int]],
    display_paths: set[str],
    source_key: str,
    surface_prefix: str,
) -> tuple[str, str]:
    """Return the wire field and the path after decoding a String(JSON) field."""
    actual = normalized_path(path, display_paths)
    if actual is None:
        return (
            "—（官网展示分组，不存在该 wire key）",
            "—（官网展示分组，不参与解码）",
        )
    surface = (source_key, surface_prefix)
    if surface in UNKNOWN_OUTER_SURFACES:
        return (
            "—（官网未标异步外层字段名）",
            "—（[需要官方确认]：异步外层字段名和编码）",
        )
    if surface in UNKNOWN_NAMED_SURFACES:
        return (
            surface_prefix,
            "—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）",
        )
    if source_key == "split-detail-query" and (
        actual == "response.data.split_trans_responses[]"
        or actual.startswith("response.data.split_trans_responses[].")
    ):
        suffix = actual[len("response.data.split_trans_responses[]") :]
        return (
            "response.data.split_trans_responses",
            "$[]" + suffix + "（String(JSON Array) 解码结果）",
        )

    containers: dict[str, bool] = {}
    if surface in KNOWN_STRING_JSON_SURFACES:
        containers[surface_prefix] = True
    for candidate_path, candidate_field, _depth in flattened:
        if candidate_path in display_paths:
            continue
        candidate_type = str(getattr(candidate_field, "field_type", "")).lower()
        if candidate_type != "string":
            continue
        has_children = any(
            other_path.startswith(candidate_path + ".")
            for other_path, _other_field, _other_depth in flattened
        )
        if not is_string_json(candidate_field) and not has_children:
            continue
        candidate = normalized_path(candidate_path, display_paths)
        if candidate and (actual == candidate or actual.startswith(candidate + ".")):
            containers[candidate] = (
                is_string_json(candidate_field)
                or (source_key, candidate) in KNOWN_STRING_JSON_PATHS
            )
    if not containers:
        return actual, "—（直接 JSON 路径）"
    ordered = sorted(containers, key=lambda item: item.count("."))
    container = ordered[0]
    wire = strip_string_array_marker(container)
    if not containers[container]:
        return wire, "—（[需要官方确认]：String 子表编码）"
    if actual == container:
        kind = "String(JSON Array)" if container.endswith("[]") else "String(JSON)"
        return wire, f"—（{kind} 容器）"
    inner = [item for item in ordered[1:] if actual == item or actual.startswith(item + ".")]
    if not inner:
        return wire, decoded_from(container, actual)
    nested = inner[-1]
    nested_path = decoded_from(container, nested)
    if not containers[nested]:
        return wire, nested_path + " => [需要官方确认]：String 子表编码"
    if actual == nested:
        kind = "String(JSON Array)" if nested.endswith("[]") else "String(JSON)"
        return wire, nested_path + f"（{kind} 容器）"
    return (
        wire,
        nested_path + " => JSON decode => " + decoded_from(nested, actual),
    )


def confirmation_status(field: object) -> str:
    unknown: list[str] = []
    field_type = str(getattr(field, "field_type", "—"))
    length = str(getattr(field, "length", "—"))
    required = str(getattr(field, "required", "—"))
    if field_type == "—":
        unknown.append("类型")
    if length == "—" and field_type.lower() not in {"json", "object", "array"}:
        unknown.append("长度")
    if required == "—":
        unknown.append("必填")
    if unknown:
        return "[需要官方确认]：" + "/".join(unknown)
    if length == "—":
        return "N/A：结构字段长度"
    return "已确认"


def reviewed_description(source_key: str, path: str, description: str) -> str:
    """Append owner-confirmed corrections without mutating locked source bytes."""
    if (
        source_key == "aggregation-query"
        and path == "response.data.trade_type"
    ):
        return (
            description
            + "；[接入方确认勘误] 官网说明中第二个 `A_NATIVE: 支付宝付款码` "
            "应为 `A_MICROPAY: 支付宝付款码`；当前成功示例已使用正确值 `A_MICROPAY`"
        )
    return description


def load_sources() -> tuple[str, Path, tuple[PaymentSource, ...]]:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    source_date = lock["source_date"]
    source_dir = payment_source_dir()
    by_key = {item["key"]: item for item in lock["sources"]}
    if set(SURFACES) - set(by_key):
        raise ValueError(f"payment source lock missing API keys: {sorted(set(SURFACES) - set(by_key))}")
    sources = tuple(
        PaymentSource(
            key=key,
            title=by_key[key]["title"],
            filename=by_key[key]["filename"],
            url=by_key[key]["url"],
            sha256=by_key[key]["sha256"],
            surfaces=surfaces,
        )
        for key, surfaces in SURFACES.items()
    )
    return source_date, source_dir, sources


def render_source(source: PaymentSource, source_dir: Path) -> tuple[str, dict[str, object]]:
    content = (source_dir / source.filename).read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    if digest != source.sha256:
        raise ValueError(f"{source.filename}: source digest changed")
    roots, nested = parse_markdown_tables(
        content.decode("utf-8-sig"),
        source.url,
    )
    if len(roots) != len(source.surfaces):
        raise ValueError(
            f"{source.filename}: expected {len(source.surfaces)} root tables, found {len(roots)}"
        )

    used: set[str] = set()
    seen_paths: set[str] = set()
    surface_counts: dict[str, int] = {}
    max_depth = 0
    chunks = [
        f"## {source.title}",
        "",
        f"- 原始地址：<{source.url}>",
        f"- SHA-256：`{digest}`",
        "",
    ]
    for (label, prefix), fields in zip(source.surfaces, roots, strict=True):
        flattened = flatten_fields(fields, nested, prefix, used)
        if source.key == "split-detail-query" and prefix == "response.data":
            split_parent = "response.data.split_trans_responses"
            flattened = [
                (
                    split_parent + "[]" + path[len(split_parent) :]
                    if path == split_parent or path.startswith(split_parent + ".")
                    else path,
                    field,
                    depth,
                )
                for path, field, depth in flattened
            ]
        display_paths = {
            path
            for path, field, _depth in flattened
            if DISPLAY_NOTE in field.description
        }
        if source.key == "aggregation-query" and prefix == "response.data":
            # The official table renders one child row per trade_type, but the
            # integration owner confirmed these rows are documentation groups:
            # method_expand is decoded once and its scene fields are flat.
            display_paths.update(
                path
                for path, _field, _depth in flattened
                if path.rsplit(".", 1)[0] == AGGREGATION_QUERY_METHOD_GROUP
            )
        chunks.extend(
            (
                f"### {label}",
                "",
                "| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |",
                "| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |",
            )
        )
        for path, field, depth in flattened:
            if path in seen_paths:
                raise ValueError(f"{source.filename}: duplicate complete path {path}")
            seen_paths.add(path)
            max_depth = max(max_depth, depth)
            wire, decoded = transport_paths(
                path,
                flattened,
                display_paths,
                source.key,
                prefix,
            )
            chunks.append(
                f"| `{escape_table(path)}` | `{escape_table(wire)}` | "
                f"`{escape_table(decoded)}` | "
                f"{escape_table(field.label)} | "
                f"`{escape_table(field.field_type)}` | `{escape_table(field.length)}` | "
                f"`{escape_table(field.required)}` | "
                f"{escape_table(confirmation_status(field))} | "
                f"{escape_table(reviewed_description(source.key, path, field.description))} |"
            )
        chunks.append("")
        surface_counts[label] = len(flattened)

    unreachable = sorted(set(nested) - used)
    if unreachable:
        raise ValueError(f"{source.filename}: unreachable extend-tables: {unreachable}")
    summary = {
        "fields": sum(surface_counts.values()),
        "extend_tables": len(nested),
        "max_depth": max_depth,
        "surface_counts": surface_counts,
    }
    return "\n".join(chunks), summary


def render_catalog() -> str:
    source_date, source_dir, sources = load_sources()
    rendered: list[str] = []
    summaries: list[tuple[PaymentSource, dict[str, object]]] = []
    for source in sources:
        section, summary = render_source(source, source_dir)
        rendered.append(section)
        summaries.append((source, summary))
    total = sum(int(summary["fields"]) for _, summary in summaries)
    header = [
        "# 支付接口完整字段路径目录",
        "",
        f"> 生成来源：`{LOCK.name}` 锁定的 `{source_date}` 官方快照；共 "
        f"{len(summaries)} 个 API、{total:,} 个接口内完整路径。",
        "",
        "## 目录",
        "",
        "- 使用规则",
        "- 生成覆盖摘要",
        *(f"- {source.title}" for source, _summary in summaries),
        "",
        "## 使用规则",
        "",
        "1. 字段身份必须使用“接口 + 数据面 + 合同定位路径”，禁止按叶字段名或实际 JSON 路径去重；同一 wire 字段可因交易分支不同而拥有不同合同。",
        "2. 数组仅按官方 `Array/jsonArray` 语义添加 `[]`；Object、String(JSON) 不因名称含 `_list` 自动改成数组。",
        "3. “合同定位路径”忠实保留官网展示树；只有官方说明明确写出“只为方便文档展示”或本地已记录接口所有者确认的节点才从 wire/解码路径移除。聚合交易查询 `response.data.method_expand` 下的 `T_*` / `A_*` / `U_*` 行是场景分组，不是 wire key；`method_expand` 只解码一次，场景字段在解码后的对象根层平铺。聚合查询及退款查询响应中的 `tx_metadata` 没有该说明，必须保留为真实 String(JSON) 容器。",
        "4. “wire 字段路径”只标线上报文中的字段；String(JSON) 子字段必须先从该容器反序列化，再使用“解码后路径”。Object/Array 的真实嵌套路径直接出现在 wire JSON 中。",
        "5. 官网把父字段定义为 String 且展开子表时，子字段绝不直接扩展成 wire 路径：有 JSON 线索时按 String(JSON) 建模；无线索时把子表编码标为 `[需要官方确认]`。String(JSON Array) 的 `[]` 只属于解码路径，不属于 wire key。",
        "6. 官网未标异步外层字段名时，合同定位路径使用 `unconfirmed_payload` 作为目录数据面标签，但 wire 列必须明确为未知，禁止把该标签发明成真实字段；只标出 `data`、未说明编码时也不得猜 JSON 与 String(JSON)。",
        "7. 类型、长度或必填为空时原样保留 `—`；“确认状态”逐行区分结构字段的 `N/A` 和必须标记的 `[需要官方确认]`，不得把未知长度解释为无限制。",
        "8. 本目录提供字段合同；场景条件、SDK、安全硬停、通知终态和勘误仍需联读对应原子 reference。",
        "9. 官方字段说明中的绝对链接保持原值；`#锚点` 或相对链接会按该接口的“原始地址”解析成可点击绝对地址，并同时保留官网相对地址原文。已确认的坏锚点会追加规范目标：`#业务返回码` 补公共返回码全集，聚合下单 `notify_url` 的 `#异步返回参数` 同时补正扫、反扫通知参数及异步消息简介。它们只是规范资料指针，不是字段默认值。`notify_url`、`jump_url`、下载地址、二维码等说明里的裸 URL 示例属于运行时值或格式示例，不得当作外部资料或建议值。",
        "",
        "## 生成覆盖摘要",
        "",
        "| API | 字段路径数 | 扩展表数 | 最大路径深度 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for source, summary in summaries:
        header.append(
            f"| {source.title} | {summary['fields']} | "
            f"{summary['extend_tables']} | {summary['max_depth']} |"
        )
    header.extend(("", f"合计：`{total:,}` 个接口内完整字段路径。", ""))
    return "\n".join((*header, *rendered)).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = render_catalog()
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"generated payment catalog differs: {args.output}")
        print(f"payment field catalog is current: {args.output}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"generated payment field catalog: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
