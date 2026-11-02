#!/usr/bin/env python3
"""Publish dated onboarding snapshots and calculated deltas, never old locks."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import generate_merchant_onboarding_field_catalog as merchant
import generate_onboarding_extension_field_catalog as extension
import generate_user_onboarding_field_catalog as user
from skill_validation_config import (
    MANIFEST_FILE, ONBOARDING_SPEC, PAYMENT_SOURCE_LOCK, PAYMENT_SPEC,
    SDK_SOURCE_LOCK, load_sdk_source_lock, onboarding_source_date,
)

ROOT = Path(__file__).resolve().parent.parent
CONFLICTS = {
    "merchant": [
        "enterprise request.data.material_card_info is Y while its description limits requiredness to enterprise private settlement",
        "enterprise request.data.material_card_info.branch_code length is 8 while its example has 12 characters",
        "several Object types (including jxf_fee_info and business-open wx_zl_conf certificate_info/sales_info) still describe jsonObject strings",
        "business-modify wx_zl_pay_conf_list is String with no declared JSON shape although it has nested fields",
        "business-modify async.business.huifu_id still describes and exemplifies a product ID",
    ],
    "user": [
        "user business modify response.data is String while the success example is a JSON object",
        "user business open is_priority_receipt is C while its P0 description says optional and supplies a default",
        "user business modify is_priority_receipt is C and says P0 required while also describing an empty-value default",
        "balance_pay_config and account_recharge_config fee_rate/fee_fix_amt are both Y while descriptions require at least one",
        "user business request balance_pay_config.out_fee_flag does not declare its enum; response enums cannot define request behavior",
        "user list result is String/jsonArray while its example is a native array",
    ],
    "extension": [
        "contract list result_list is String/jsonArray while its success example is a native array",
        "lower-merchant permission retains a merchant-detail response example and omits required request data.product_id from its example",
        "unified web onboarding retains business success-code, URL-length and async audit req_date-length inconsistencies",
        "unified web query pay_scene link label disagrees with its target; length 2 now agrees with example 01",
        "WeChat configuration no longer defines formal synchronous/async envelopes; synchronous scalar lengths are absent",
        "WeChat configuration query contains swapped required/length columns, APPID length inconsistencies and an inner-only success example",
        "WeChat real-name fields marked N contain conditional-required descriptions",
        "WeChat real-name query qrcode_data ambiguously describes base64, image content and HTML",
        "Alipay support_credentials is now explicitly a JSON-object string and conditionally required for micro merchants; old array conflict closed",
        "Alipay real-name financial and region examples remain inconsistent with their conditions",
        "Alipay real-name query success example omits response.sign",
    ],
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def page_update(path: Path) -> str | None:
    if path.suffix != ".md":
        return None
    match = re.search(r"(?:最近)?更新时间[：:]\s*(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})", path.read_text(encoding="utf-8-sig"))
    return f"{match[1]}-{int(match[2]):02d}-{int(match[3]):02d}" if match else None


def official_endpoint(path: Path, previous_endpoint: str) -> str:
    """Read the explicit endpoint, rather than inheriting stale lock metadata."""
    if path.suffix == ".json":
        uri = "/" + json.loads(path.read_text(encoding="utf-8"))["uri"].lstrip("/")
        if previous_endpoint.removeprefix("POST ") != uri:
            raise ValueError("image URI changed; HTTP method requires independent confirmation")
        return previous_endpoint
    document = path.read_text(encoding="utf-8-sig")
    endpoints = set(re.findall(r"(?:POST</span>|请求URL[：:]\s*)https://api\.huifu\.com(/v\d+/[A-Za-z0-9/_-]+)", document))
    if len(endpoints) != 1:
        raise ValueError(f"{path.name}: expected one explicit official endpoint, found {sorted(endpoints)}")
    return "POST " + endpoints.pop()


def field_records(catalog: str) -> dict[tuple[str, str], tuple[str, ...]]:
    title = ""
    records = {}
    for line in catalog.splitlines():
        if line.startswith("## "):
            title = line[3:]
        elif line.startswith("| `"):
            cells = tuple(part.strip().strip("`") for part in re.split(r"(?<!\\)\|", line)[1:-1])
            if len(cells) != 6 or (title, cells[0]) in records:
                raise ValueError(f"invalid/duplicate catalog row: {line}")
            records[title, cells[0]] = cells[1:]
    return records


def path_totals(catalog: str) -> dict[str, int]:
    records = field_records(catalog)
    parent = sum(any(title == other_title and other != path and (other.startswith(path + ".") or other.startswith(path + "[]."))
                     for other_title, other in records) for title, path in records)
    request = sum(path.startswith("request") for _, path in records)
    callback = sum(path.startswith("async") for _, path in records)
    return {"fields": len(records), "request": request, "response": len(records) - request - callback,
            "callback": callback, "parent": parent, "leaf": len(records) - parent}


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_new_lock_paths(*paths: Path) -> None:
    existing = [str(path.relative_to(ROOT)) for path in paths if path.exists()]
    if existing:
        raise ValueError(f"refusing to overwrite versioned onboarding source lock(s): {', '.join(existing)}; use a new --source-date")


def refresh_sdk_metadata() -> dict:
    """Reuse dated source evidence; generating API metadata is not an SDK test."""
    sdk = load_sdk_source_lock()
    versions = {name: item["version"] for name, item in sdk["components"].items()}
    return {
        "sdk_reviewed_at": sdk["verified_at"],
        "sdk_versions": versions,
        "python_sdk": {"target_version": versions["python"], "verified_source_version": versions["python"], "target_source_verified": True},
    }


def previous_review(path: Path) -> dict:
    """Find a candidate's original API review without confusing it with its parent."""
    refresh = json.loads(path.read_text(encoding="utf-8"))
    binding = refresh.get("source_review")
    if binding is not None:
        review_path = ROOT / binding["path"]
        if digest(review_path) != binding["sha256"]:
            raise ValueError("previous API source-review SHA differs")
        reviewed = json.loads(review_path.read_text(encoding="utf-8"))
        if reviewed["refresh_id"] != binding["refresh_id"] or reviewed["refresh_id"] != refresh["source_review_id"]:
            raise ValueError("previous API source-review identity differs")
        return reviewed
    if "source_review_id" in refresh:
        binding = refresh["previous_refresh"]
        if binding["refresh_id"] != refresh["source_review_id"]:
            raise ValueError("previous candidate lacks its original API review binding")
        review_path = ROOT / binding["path"]
        if digest(review_path) != binding["sha256"]:
            raise ValueError("previous API source-review SHA differs")
        return json.loads(review_path.read_text(encoding="utf-8"))
    return refresh


def carried_cross_skill_review(review: dict, payment_lock: dict) -> dict:
    """Retain the original retrieval date across repeated API-only refreshes."""
    split_source = next(item for item in payment_lock["sources"] if item["key"] == "split-detail-query")
    carried = dict(review["cross_skill_review"])
    carried.update(
        source_lock=str(PAYMENT_SOURCE_LOCK.relative_to(ROOT)),
        source_key=split_source["key"],
        locked_sha256=split_source["sha256"],
        changed=carried["online_sha256"] != split_source["sha256"],
        version_action=f"keep huifu-pay-integration at {PAYMENT_SPEC.version}",
        evidence_retrieved_at=carried.get("evidence_retrieved_at", review["retrieved_at"]),
        evidence_scope="Carried historical ownership/source comparison, not a new online payment retrieval.",
    )
    return carried


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-date", required=True)
    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    current = manifest["skills"]["huifu-merchant-onboarding"]
    parser.add_argument("--previous-source-date", default=onboarding_source_date())
    parser.add_argument("--previous-combined-lock", type=Path, default=ROOT / current["source_lock"])
    parser.add_argument("--previous-refresh", type=Path, default=ROOT / current["refresh_contract"])
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    for value in (args.source_date, args.previous_source_date):
        datetime.strptime(value, "%Y-%m-%d")
    if args.source_date <= args.previous_source_date:
        raise ValueError("source date must follow the previous snapshot")
    previous_combined = args.previous_combined_lock.resolve()
    previous_refresh = args.previous_refresh.resolve()
    old_refresh = json.loads(previous_refresh.read_text(encoding="utf-8"))
    old_review = previous_review(previous_refresh)
    old_combined = json.loads(previous_combined.read_text(encoding="utf-8"))
    # Resolve and validate predecessors before any source/catalog writes.
    previous_combined.relative_to(ROOT)
    previous_refresh.relative_to(ROOT)
    aggregate_bindings = [item for item in old_refresh["source_locks"].values() if item["path"] == previous_combined.relative_to(ROOT).as_posix()]
    if len(aggregate_bindings) != 1 or aggregate_bindings[0]["sha256"] != digest(previous_combined):
        raise ValueError("previous candidate does not bind the selected aggregate")
    for entry in old_combined["source_locks"].values():
        path = ROOT / entry["path"]
        prior_lock = json.loads(path.read_text(encoding="utf-8"))
        if digest(path) != entry["sha256"] or prior_lock.get("source_date", prior_lock.get("verified_at", "")[:10]) != args.previous_source_date:
            raise ValueError("previous aggregate and --previous-source-date disagree")
    sdk_metadata = refresh_sdk_metadata()
    verified = datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")
    groups = (("merchant", "merchant-onboarding", merchant), ("user", "user-onboarding", user),
              ("extension", "onboarding-extension", extension))
    locks = {name: ROOT / f"maintainer-contracts/{group}-source-lock-{args.source_date}.json" for name, group, _ in groups}
    combined_path = ROOT / f"maintainer-contracts/merchant-onboarding-{ONBOARDING_SPEC.version}-source-lock-{args.source_date}.json"
    refresh_path = ROOT / f"maintainer-contracts/api-refresh-onboarding-online-review-{args.source_date}.json"
    ensure_new_lock_paths(*locks.values(), combined_path, refresh_path)
    catalogs, source_links, deltas, pending = {}, {}, {}, []
    for name, group, module in groups:
        prior_path = ROOT / f"maintainer-contracts/{group}-source-lock-{args.previous_source_date}.json"
        prior = json.loads(prior_path.read_text(encoding="utf-8"))
        prior_dir = ROOT / "maintainer-contracts/official-sources" / group / prior["source_snapshot_id"]
        current_dir = ROOT / "maintainer-contracts/official-sources" / group / args.source_date
        if args.fetch:
            module.refresh_sources(current_dir)
        catalog, summaries = module.build_catalog(current_dir)
        old_catalog, _ = module.build_catalog(prior_dir)
        before, after = field_records(old_catalog), field_records(catalog)
        added, removed = after.keys() - before.keys(), before.keys() - after.keys()
        changed = {key for key in before.keys() & after.keys() if before[key] != after[key]}
        totals = path_totals(catalog)
        totals.update({kind: sum(item[kind] for item in summaries.values()) for kind in ("root_tables", "extend_tables")})
        entries = []
        for old in prior["sources"]:
            source = dict(old)
            path = current_dir / source["filename"]
            source["endpoint"] = official_endpoint(path, old["endpoint"])
            summary = summaries[source["key"]]
            counts = summary["surface_counts"]
            source.update(official_page_update=page_update(path), sha256=digest(path), field_count=summary["total_fields"],
                          request_fields=sum(v for k, v in counts.items() if "请求" in k and "响应" not in k),
                          response_fields=sum(v for k, v in counts.items() if "响应" in k and "异步" not in k),
                          callback_fields=sum(v for k, v in counts.items() if "异步" in k),
                          root_tables=summary["root_tables"], extend_tables=summary["extend_tables"])
            entries.append(source)
        old_hashes = {item["key"]: item["sha256"] for item in prior["sources"]}
        lock = {"schema_version": 1, "source_date": args.source_date, "source_snapshot_id": args.source_date,
                "previous_source_lock": {"path": str(prior_path.relative_to(ROOT)), "sha256": digest(prior_path)},
                "verified_at": verified, "sources": entries, "totals": totals,
                "api_refresh": {"refresh_id": f"api-refresh-{name}-online-review-{args.source_date}",
                                "changed_source_keys": [item["key"] for item in entries if item["sha256"] != old_hashes[item["key"]]],
                                "field_paths_added": len(added), "field_paths_removed": len(removed), "field_paths_changed": len(changed),
                                "document_conflicts": CONFLICTS[name]}}
        if name == "extension":
            lock["introduced_in_skill_version"] = "1.0.3"
        pending.extend(((locks[name], lock), (module.DEFAULT_OUTPUT, catalog)))
        source_links[group.replace("-", "_")] = {"path": str(locks[name].relative_to(ROOT)), "field_paths": totals["fields"]}
        catalogs[name] = {"path": str(module.DEFAULT_OUTPUT.relative_to(ROOT)),
                          "sha256": hashlib.sha256(catalog.encode()).hexdigest(), "field_paths": totals["fields"]}
        deltas.update({f"{name}_paths_added": len(added), f"{name}_paths_removed": len(removed),
                       f"{name}_paths_changed": len(changed), f"{name}_catalog_total": totals["fields"]})
    # Parse every source before publishing any catalog or lock.
    for path, payload in pending:
        if isinstance(payload, str):
            path.write_text(payload, encoding="utf-8")
        else:
            write_json(path, payload)
    for entry in source_links.values():
        entry["sha256"] = digest(ROOT / entry["path"])
    combined_total = sum(item["field_paths"] for item in catalogs.values())
    write_json(combined_path, {"schema_version": 1, "skill": "huifu-merchant-onboarding", "version": ONBOARDING_SPEC.version,
                "refresh_revision": args.source_date, "scope": f"Review of all 34 base onboarding sources for onboarding {ONBOARDING_SPEC.version}; additional APIs are locked separately.",
                "previous_combined_lock": {"path": str(previous_combined.relative_to(ROOT)), "sha256": digest(previous_combined)},
                "source_locks": source_links, "catalogs": catalogs, "totals": {"interfaces": 34, "field_paths": combined_total}})
    # Keep the split-query ownership review tied to the active payment snapshot.
    payment_lock = json.loads(PAYMENT_SOURCE_LOCK.read_text(encoding="utf-8"))
    cross_skill_review = carried_cross_skill_review(old_review, payment_lock)
    refresh_sources = {f"{key}_current": {"path": item["path"], "sha256": item["sha256"]} for key, item in source_links.items()}
    refresh_sources[f"onboarding_{ONBOARDING_SPEC.version.replace('.', '_')}"] = {"path": str(combined_path.relative_to(ROOT)), "sha256": digest(combined_path)}
    refresh_sources["local_sdk_current"] = {"path": str(SDK_SOURCE_LOCK.relative_to(ROOT)), "sha256": digest(SDK_SOURCE_LOCK)}
    deltas["combined_total"] = combined_total
    write_json(refresh_path, {"schema_version": 1, "refresh_id": f"api-refresh-onboarding-online-review-{args.source_date}",
               "requested_at": args.source_date, "retrieved_at": verified, "api_source_date": args.source_date,
               **sdk_metadata,
               "version_state": {"reason": "User-confirmed existing-document synchronization; additional interfaces have independent source evidence.",
                                 "huifu-merchant-onboarding": ONBOARDING_SPEC.version, "huifu-pay-integration": PAYMENT_SPEC.version},
               "previous_refresh": {"path": str(previous_refresh.relative_to(ROOT)), "sha256": digest(previous_refresh), "refresh_id": old_refresh["refresh_id"]},
               "source_locks": refresh_sources, "catalogs": catalogs,
               "scope": ["13 merchant, 9 user, 12 extension official APIs", "Reuse independently dated local SDK evidence: " + ", ".join(f"{name} {version}" for name, version in sdk_metadata["sdk_versions"].items())],
               "field_delta": deltas, "cross_skill_review": cross_skill_review,
               "preserved_boundaries": [
                   "Historical source locks, candidate records, source bytes and frozen assets remain unchanged",
                   f"Current Skill versions remain onboarding {ONBOARDING_SPEC.version} and payment {PAYMENT_SPEC.version}",
                   "SDK evidence retains its own verification date; an API refresh does not rerun SDK verification",
                   "Unclear fields and known TLS findings remain non-blocking developer advisories",
                   "No SDK mutation, live business request, real-model run, commit or publication is implied",
               ],
               "release_rule": f"All {combined_total:,} fields, immutable sources, SDK evidence, regressions and package gates must pass before publishing huifu-merchant-onboarding {ONBOARDING_SPEC.version}."})
    print(f"Published {combined_total} paths across 34 sources; skill version remains {ONBOARDING_SPEC.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
