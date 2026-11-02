#!/usr/bin/env python3
"""Audit active official sources without changing active locks or Skill contracts."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

import generate_merchant_onboarding_field_catalog as merchant
import generate_user_onboarding_field_catalog as user
import generate_onboarding_extension_field_catalog as extension
from generate_payment_field_catalog import SURFACES

ROOT = Path(__file__).resolve().parent.parent


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def normalized(raw: bytes, suffix: str) -> str:
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    if suffix == ".json":
        return json.dumps(json.loads(text), ensure_ascii=False, sort_keys=True)
    # Ignore renderer identifiers only in their HTML marker positions.
    text = re.sub(r'((?:class="extend |div:extend-table ))[A-Za-z0-9_-]+', r'\1<DISPLAY_ID>', text)
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def fields(raw: bytes, source: dict, surfaces: tuple) -> dict | None:
    if source["filename"].endswith(".json"):
        doc = json.loads(raw.decode("utf-8-sig"))
        result = {}
        for item in doc.get("requestBody", {}).get("params", []):
            path = "request.data." + item["name"]
            if path in result:
                raise ValueError("duplicate JSON request parameter: " + path)
            result[path] = {key: item.get(key) for key in ("desc", "fieldType", "isRequired", "maxLength", "remark", "array")}
        return result
    if not surfaces:
        return None
    roots, nested = merchant.parse_markdown_tables(raw.decode("utf-8-sig"), source["url"])
    if len(roots) != len(surfaces):
        raise ValueError(f"root-table structure changed: expected {len(surfaces)}, found {len(roots)}")
    result, used = {}, set()
    for (_, prefix), root in zip(surfaces, roots, strict=True):
        for path, field, _depth in merchant.flatten_fields(root, nested, prefix, used):
            if path in result:
                raise ValueError("duplicate full field path: " + path)
            result[path] = {key: getattr(field, key) for key in ("label", "field_type", "length", "required", "description")}
    if set(nested) - used:
        raise ValueError("unreachable nested tables")
    return result


def delta(before: dict | None, after: dict | None) -> dict | None:
    if before is None or after is None:
        return None
    return {
        "before": len(before), "after": len(after),
        "added": [{"path": key, "after": after[key]} for key in sorted(after.keys() - before.keys())],
        "removed": [{"path": key, "before": before[key]} for key in sorted(before.keys() - after.keys())],
        "changed": [{"path": key, "before": before[key], "after": after[key]} for key in sorted(before.keys() & after.keys()) if before[key] != after[key]],
    }


def sources() -> list[dict]:
    manifest = json.loads((ROOT / "skills-manifest.json").read_text())
    payment = manifest["skills"]["huifu-pay-integration"]["source_lock"]
    combined = json.loads((ROOT / manifest["skills"]["huifu-merchant-onboarding"]["source_lock"]).read_text())
    locks = {"payment": payment, **{name: item["path"] for name, item in combined["source_locks"].items()}}
    configurations = {
        "merchant_onboarding": {item.key: item.root_labels for item in merchant.SOURCES},
        "user_onboarding": {item.key: item.surfaces for item in user.SOURCES},
        "onboarding_extension": {item.key: item.surfaces for item in extension.SOURCES},
        "payment": SURFACES,
    }
    directories = {"payment": "payment", "merchant_onboarding": "merchant-onboarding", "user_onboarding": "user-onboarding", "onboarding_extension": "onboarding-extension"}
    result = []
    for domain, name in locks.items():
        lock = json.loads((ROOT / name).read_text())
        for item in lock["sources"]:
            previous = ROOT / "maintainer-contracts/official-sources" / directories[domain] / lock["source_snapshot_id"] / item["filename"]
            if sha(previous.read_bytes()) != item["sha256"]:
                raise ValueError("baseline digest mismatch: " + str(previous))
            result.append({**item, "domain": domain, "directory": directories[domain], "baseline_lock": name, "baseline_file": str(previous.relative_to(ROOT)), "surfaces": configurations[domain].get(item["key"], ())})
    if len({item["url"] for item in result}) != len(result):
        raise ValueError("duplicate active source URLs")
    return result


def review(item: dict, date: str) -> dict:
    result = {key: item[key] for key in ("key", "title", "url", "domain", "baseline_lock", "baseline_file")}
    before = (ROOT / item["baseline_file"]).read_bytes()
    result["before_sha256"] = sha(before)
    try:
        request = Request(item["url"], headers={"User-Agent": "huifu-official-document-audit/1.0"})
        with urlopen(request, timeout=25) as response:
            after = response.read()
            result["http_status"] = response.status
            result["resolved_url"] = response.url
        text = after.decode("utf-8-sig")
        if item["filename"].endswith(".json"):
            json.loads(text)
        elif not text.lstrip().startswith(("<style", "#", "<!--")):
            raise ValueError("unexpected document format or HTML error page")
        destination = ROOT / "maintainer-contracts/official-sources" / item["directory"] / date / item["filename"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and destination.read_bytes() != after:
            raise ValueError("refusing to overwrite an existing snapshot")
        if not destination.exists():
            destination.write_bytes(after)
        result.update({"after_file": str(destination.relative_to(ROOT)), "after_sha256": sha(after), "retrieved_at": datetime.now(timezone.utc).isoformat()})
        result["byte_changed"] = before != after
        result["content_changed"] = normalized(before, destination.suffix) != normalized(after, destination.suffix)
        update = re.search(r"最近更新时间[：:]\s*([0-9.\-/]+)", text)
        result["page_updated_at"] = update[1] if update else None
        try:
            comparison = delta(fields(before, item, item["surfaces"]), fields(after, item, item["surfaces"]))
            result["field_comparison"] = comparison
        except (ValueError, KeyError) as error:
            if before == after:
                result["field_review_note"] = "字节未变；该旧版页面使用所属领域的专用解析器复核：" + str(error)
            else:
                result["field_review_error"] = str(error)
            comparison = None
        field_change = comparison and any(comparison[key] for key in ("added", "removed", "changed"))
        result["result"] = "unchanged" if not result["byte_changed"] else "format_only" if not result["content_changed"] else "field_changed" if field_change else "text_or_example_changed"
        if result["byte_changed"]:
            result["unified_diff"] = list(difflib.unified_diff(before.decode("utf-8-sig").splitlines(), text.splitlines(), fromfile=item["baseline_file"], tofile=result["after_file"], lineterm=""))
    except Exception as error:
        result.update({"result": "fetch_or_format_failed", "error": str(error)})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.source_date):
        parser.error("source-date must be YYYY-MM-DD")
    stem = ROOT / f"maintainer-contracts/official-document-audit-{args.source_date}"
    if stem.with_suffix(".json").exists() or stem.with_suffix(".md").exists():
        parser.error("refusing to overwrite an existing audit; choose a new source date")
    entries = sources()
    reviewed = {}
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        work = {pool.submit(review, item, args.source_date): index for index, item in enumerate(entries)}
        for future in as_completed(work):
            reviewed[work[future]] = future.result()
    results = [reviewed[index] for index in range(len(entries))]
    counts = {status: sum(item["result"] == status for item in results) for status in ("unchanged", "format_only", "field_changed", "text_or_example_changed", "fetch_or_format_failed")}
    report = {"schema_version": 1, "date": args.source_date, "mode": "audit-only", "source_count": len(results), "counts": counts, "active_contracts_modified": False, "sources": results}
    stem = ROOT / f"maintainer-contracts/official-document-audit-{args.source_date}"
    stem.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [f"# {args.source_date} 现有官方文档更新检查", "", f"逐一检查{len(results)}个活动来源；统计：`{json.dumps(counts, ensure_ascii=False)}`。本报告只记录差异，未切换活动来源或修改既有Skill合同。", "", "完整增删改、原始SHA、抓取状态及逐行差异见同名JSON。字段解析结构变化单独标记，不能计作字段无变化。", "", "| 领域 | 文档 | 结果 | 字段增/删/改 | 表结构核验 |", "| --- | --- | --- | --- | --- |"]
    for item in results:
        comparison = item.get("field_comparison")
        summary = "/".join(str(len(comparison[k])) for k in ("added", "removed", "changed")) if comparison else "—"
        lines.append(f"| {item['domain']} | [{item['title']}]({item['url']}) | {item['result']} | {summary} | {item.get('field_review_error', item.get('field_review_note', '通过' if comparison else '正文/示例单独比较'))} |")
    stem.with_suffix(".md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"source_count": len(results), "counts": counts, "report": str(stem.relative_to(ROOT))}, ensure_ascii=False))
    return 1 if counts["fetch_or_format_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
