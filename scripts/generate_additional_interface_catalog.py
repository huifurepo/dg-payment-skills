#!/usr/bin/env python3
"""Generate separately locked additions, preserving the existing API catalogs."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import generate_merchant_onboarding_field_catalog as base
import generate_payment_field_catalog as payment
from interface_expansion_config import ROOT, DATE, PAYMENT, ONBOARDING, VERSIONS, CATALOGS, LOCKS, INTERFACES
from validation_runtime import require_assertions_enabled

require_assertions_enabled()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(item, raw):
    if item.filename.endswith(".json"):
        doc = json.loads(raw.decode("utf-8-sig"))
        assert "/" + doc["uri"].lstrip("/") == item.route
        fields = [base.Field(p["name"], base.clean_cell(p.get("desc", "")) or "—", p.get("fieldType") or "—", p.get("maxLength") or "—", p.get("isRequired") or "—", base.clean_cell(p.get("remark", "")) or "—") for p in doc["requestBody"]["params"]]
        roots, nested = [fields], {}
    else:
        assert "https://api.huifu.com" + item.route in raw.decode("utf-8-sig")
        roots, nested = base.parse_markdown_tables(raw.decode("utf-8-sig"), item.url)
    assert len(roots) == len(item.surfaces), (item.key, len(roots), len(item.surfaces))
    lines = ["## " + item.title, "", f"- 官方来源：<{item.url}>", f"- SHA-256：`{hashlib.sha256(raw).hexdigest()}`", ""]
    if item.filename.endswith(".json"):
        lines += ["本来源仅含正式请求data；requestDemo只作演示，不定义公共信封类型/必填或响应。未公布同步响应、通知、HTTP方法；SDK的POST是独立源码事实。", ""]
    used, seen, totals = set(), set(), {}
    for (label, prefix), fields in zip(item.surfaces, roots, strict=True):
        flat = base.flatten_fields(fields, nested, prefix, used)
        totals[label] = len(flat)
        lines += ["### " + label, "", "| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for path, field, _ in flat:
            assert path not in seen, (item.key, path)
            seen.add(path)
            wire, decoded = payment.transport_paths(path, flat, set(), item.key, prefix)
            cells = [path, wire, decoded, field.label, field.field_type, field.length, field.required, payment.confirmation_status(field), field.description]
            lines.append("| " + " | ".join("`" + base.escape_table(c) + "`" if index in (0, 1, 2, 4, 5, 6) else base.escape_table(c) for index, c in enumerate(cells)) + " |")
        lines.append("")
    assert not (set(nested) - used), item.key
    return "\n".join(lines), {"fields": len(seen), "surfaces": totals, "root_tables": len(roots), "nested_tables": len(nested)}


def build(skill, lock):
    sections, summaries = [], []
    records = {entry["key"]: entry for entry in lock["sources"]}
    for item in INTERFACES:
        if item.skill != skill:
            continue
        entry = records[item.key]
        path = ROOT / entry["path"]
        assert digest(path) == entry["sha256"], str(path)
        section, summary = render(item, path.read_bytes())
        sections.append(section); summaries.append((item, summary))
    total = sum(summary["fields"] for _, summary in summaries)
    title = "新增支付接口完整字段目录" if skill == PAYMENT else "商户子账户配置完整字段目录"
    scope_note = ('JSON退款查询只覆盖正式请求；汇总查询的正式返回表保留官网同步章节位置，正文异步描述的矛盾与通知协议缺口见原子参考，不能自动外推为完整Webhook。' if skill == PAYMENT else "两接口管理商户子账户及结算配置；开通与修改的必填性分别保留，审核通知与账户可用状态不得混同。未公布的通知协议见对应原子参考。")
    lines = ["# " + title, "", f"来源日期：{DATE}。共{len(summaries)}个接口、{total}条完整字段路径。基础目录及其历史锁独立保留。", "", "## 目录", "", "- 使用规则", "- 覆盖摘要", *["- " + item.title for item, _ in summaries], "", "## 使用规则", "", "字段身份为接口＋方向＋完整路径，不能按叶字段名去重。类型、长度和Y/N/C为空时保留未知；C按条件必填。String(JSON)逐层编码/解码，数组标记不是wire字段名。官网表与示例冲突须联读原子参考；本目录不将示例修成合同。", "", scope_note, "", "## 覆盖摘要", "", "| 接口 | 字段路径 | 根表 | 嵌套表 |", "| --- | --- | --- | --- |"]
    for item, summary in summaries:
        lines.append(f"| {item.title} | {summary['fields']} | {summary['root_tables']} | {summary['nested_tables']} |")
    return ("\n".join(lines) + "\n\n" + "\n\n".join(sections)).rstrip() + "\n", total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for skill in VERSIONS:
        lock = json.loads((ROOT / LOCKS[skill]).read_text())
        text, total = build(skill, lock)
        path = ROOT / lock["catalog"]["path"]
        if args.check:
            assert path.read_text() == text and digest(path) == lock["catalog"]["sha256"]
            assert total == lock["totals"]["field_paths"]
        else:
            path.write_text(text)
        print(skill, "catalog verified:", total)


if __name__ == "__main__":
    main()
