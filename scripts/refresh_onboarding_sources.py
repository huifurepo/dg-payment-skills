#!/usr/bin/env python3
"""Refresh and lock the complete merchant and user onboarding source sets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_merchant_onboarding_field_catalog as merchant
import generate_user_onboarding_field_catalog as user


ROOT = Path(__file__).resolve().parent.parent
MERCHANT_PREVIOUS = ROOT / "maintainer-contracts/merchant-onboarding-source-lock-2026-08-24-r2.json"
USER_PREVIOUS = ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r4.json"

MERCHANT_ENDPOINTS = {
    "enterprise": "POST /v2/merchant/basicdata/ent",
    "individual": "POST /v2/merchant/basicdata/indv",
    "business_open": "POST /v2/merchant/busi/open",
    "image_upload": "POST /v2/supplementary/picture",
    "detail_query": "POST /v2/merchant/basicdata/query",
    "status_query": "POST /v2/merchant/basicdata/status/query",
    "business_open_modify": "POST /v2/merchant/busi/modify",
    "basic_info_modify": "POST /v2/merchant/basicdata/modify",
    "rate_query": "POST /v2/merchant/busi/config/query",
    "status_change": "POST /v2/merchant/status/change",
    "sms_send": "POST /v2/merchant/sms/send",
    "multifee_config": "POST /v2/merchant/busi/multiFee/config",
    "multifee_query": "POST /v2/merchant/busi/multiFee/query",
}

USER_ENDPOINTS = {
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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def page_update(path: Path) -> str | None:
    if path.suffix != ".md":
        return None
    text = path.read_text(encoding="utf-8-sig")
    match = re.search(r"(?:最近)?更新时间[：:]\s*(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})", text)
    if not match:
        return None
    year, month, day = match.groups()
    return f"{year}-{int(month):02d}-{int(day):02d}"


def path_totals(catalog: str) -> dict[str, int]:
    groups: list[list[str]] = []
    paths: list[str] = []
    current: list[str] = []
    for line in catalog.splitlines():
        if line.startswith("## ") and not line.startswith("## 生成覆盖摘要"):
            if current:
                groups.append(current)
            current = []
        match = re.match(r"\| `([^`]+)` \|", line)
        if match:
            path = match.group(1)
            paths.append(path)
            current.append(path)
    if current:
        groups.append(current)
    parent = sum(
        any(
            other != path
            and (other.startswith(path + ".") or other.startswith(path + "[]."))
            for other in group
        )
        for group in groups
        for path in group
    )
    request = sum(path.startswith("request") for path in paths)
    callback = sum(path.startswith("async") for path in paths)
    response = len(paths) - request - callback
    return {
        "fields": len(paths),
        "request": request,
        "response": response,
        "callback": callback,
        "parent": parent,
        "leaf": len(paths) - parent,
    }


def source_entry(spec, summary: dict[str, object], source_dir: Path, endpoint: str) -> dict[str, object]:
    path = source_dir / spec.filename
    return {
        "key": spec.key,
        "title": spec.title,
        "filename": spec.filename,
        "url": spec.url,
        "endpoint": endpoint,
        "official_page_update": page_update(path),
        "sha256": digest(path),
        "field_count": summary["total_fields"],
        "request_fields": sum(v for k, v in summary["surface_counts"].items() if "请求" in k and "响应" not in k),
        "response_fields": sum(v for k, v in summary["surface_counts"].items() if "响应" in k and "异步" not in k),
        "callback_fields": sum(v for k, v in summary["surface_counts"].items() if "异步" in k),
        "root_tables": summary["root_tables"],
        "extend_tables": summary["extend_tables"],
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_new_lock_paths(*paths: Path) -> None:
    existing = [path for path in paths if path.exists()]
    if existing:
        names = ", ".join(str(path.relative_to(ROOT)) for path in existing)
        raise ValueError(
            f"refusing to overwrite versioned onboarding source lock(s): {names}; "
            "use a new --source-date"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    verified = datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")
    merchant_lock_path = ROOT / f"maintainer-contracts/merchant-onboarding-source-lock-{args.source_date}.json"
    user_lock_path = ROOT / f"maintainer-contracts/user-onboarding-source-lock-{args.source_date}.json"
    ensure_new_lock_paths(merchant_lock_path, user_lock_path)

    merchant_dir = ROOT / "maintainer-contracts/official-sources/merchant-onboarding" / args.source_date
    user_dir = ROOT / "maintainer-contracts/official-sources/user-onboarding" / args.source_date
    if args.fetch:
        merchant.refresh_sources(merchant_dir)
        user_dir.mkdir(parents=True, exist_ok=True)
        for spec in user.SOURCES:
            user.refresh_sources(user_dir, spec.key)

    merchant_catalog, merchant_summary = merchant.build_catalog(merchant_dir)
    user_catalog, user_summary = user.build_catalog(user_dir)
    merchant_catalog_path = ROOT / "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md"
    user_catalog_path = ROOT / "huifu-merchant-onboarding/references/user-onboarding-complete-field-catalog.md"
    merchant_catalog_path.write_text(merchant_catalog, encoding="utf-8")
    user_catalog_path.write_text(user_catalog, encoding="utf-8")

    merchant_specs = list(merchant.SOURCES)
    merchant_entries = [
        source_entry(spec, merchant_summary[spec.key], merchant_dir, MERCHANT_ENDPOINTS[spec.key])
        for spec in merchant_specs
    ]
    image_summary = merchant_summary["image_upload"]
    image_path = merchant_dir / merchant.IMAGE_FILENAME
    merchant_entries.insert(3, {
        "key": "image_upload", "title": "图片上传", "filename": merchant.IMAGE_FILENAME,
        "url": merchant.IMAGE_URL, "endpoint": MERCHANT_ENDPOINTS["image_upload"],
        "official_page_update": None, "sha256": digest(image_path),
        "field_count": image_summary["total_fields"],
        "request_fields": image_summary["total_fields"], "response_fields": 0, "callback_fields": 0,
        "root_tables": image_summary["root_tables"], "extend_tables": image_summary["extend_tables"],
    })
    merchant_totals = path_totals(merchant_catalog)
    merchant_totals["root_tables"] = sum(item["root_tables"] for item in merchant_summary.values())
    merchant_totals["extend_tables"] = sum(item["extend_tables"] for item in merchant_summary.values())
    merchant_lock = {
        "schema_version": 1,
        "source_date": args.source_date,
        "source_snapshot_id": args.source_date,
        "previous_source_lock": {"path": str(MERCHANT_PREVIOUS.relative_to(ROOT)), "sha256": digest(MERCHANT_PREVIOUS)},
        "verified_at": verified,
        "sources": merchant_entries,
        "totals": merchant_totals,
        "api_refresh": {
            "refresh_id": f"api-refresh-merchant-online-review-{args.source_date}",
            "changed_source_keys": ["enterprise", "individual", "business_open", "detail_query", "business_open_modify", "multifee_config", "multifee_query"],
            "field_paths_added": 29, "field_paths_removed": 1, "field_paths_changed": 45,
            "document_conflicts": [
                "response.data.conf_list is String with a child table but the document does not define object-versus-array encoding",
                "request.data.jxf_conf_info.jxf_fee_info.fee_charge_type appears only in examples and is excluded from the formal catalog",
                "request.data.jxf_conf_info.jxf_fee_info.quota_issue_fee_rate says two decimals while the example uses four",
            ],
        },
    }

    user_entries = [
        source_entry(spec, user_summary[spec.key], user_dir, USER_ENDPOINTS[spec.key])
        for spec in user.SOURCES
    ]
    user_totals = path_totals(user_catalog)
    user_totals["root_tables"] = sum(item["root_tables"] for item in user_summary.values())
    user_totals["extend_tables"] = sum(item["extend_tables"] for item in user_summary.values())
    user_lock = {
        "schema_version": 1,
        "source_date": args.source_date,
        "source_snapshot_id": args.source_date,
        "previous_source_lock": {"path": str(USER_PREVIOUS.relative_to(ROOT)), "sha256": digest(USER_PREVIOUS)},
        "verified_at": verified,
        "sources": user_entries,
        "totals": user_totals,
        "api_refresh": {
            "refresh_id": f"api-refresh-user-online-review-{args.source_date}",
            "changed_source_keys": [spec.key for spec in user.SOURCES if spec.key != "user_apply_query"],
            "field_paths_added": 5, "field_paths_removed": 5, "field_paths_changed": 43,
            "document_conflicts": [
                "user business modify response.data is String while the success example is a JSON object",
                "user business open elec_receipt_config is Object while its description says jsonObject string",
                "user business modify elec_receipt_config is Object while its description says jsonObject string",
                "user business open and modify elec_card_list are Object while their descriptions say jsonArray string",
                "user business modify is_priority_receipt is C while its P0 description says optional",
                "user business modify weekday_fix_amt and weekday_fee_rate still contain contradictory D1 behavior",
            ],
        },
    }

    write_json(merchant_lock_path, merchant_lock)
    write_json(user_lock_path, user_lock)
    print(f"merchant: {merchant_totals['fields']} fields; user: {user_totals['fields']} fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
