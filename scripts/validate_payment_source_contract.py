#!/usr/bin/env python3
"""Validate the active 37-page payment snapshot and its immutable predecessor."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from refresh_payment_sources import (
    SOURCES,
    default_lock_path,
    ensure_mutable_lock,
    page_update,
    semantic_digest,
)
from skill_validation_config import PAYMENT_SOURCE_LOCK, payment_source_dir
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
LOCK = PAYMENT_SOURCE_LOCK
HISTORICAL_LOCK = ROOT / "maintainer-contracts/payment-source-lock.json"
HISTORICAL_SHA256 = "99520419703d114e9c639ebd409358a383f427be66057a056483741a3096a147"
PREVIOUS_LOCK = ROOT / "maintainer-contracts/payment-source-lock-2026-08-24.json"
PREVIOUS_SHA256 = "47fda740a0129528d7ae9881289d8e3fce132f55ace21e15bf0993060f65868d"
HISTORICAL_SOURCE_DIR = (
    ROOT / "maintainer-contracts/official-sources/payment/2026-07-28"
)
PREVIOUS_SOURCE_DIR = (
    ROOT / "maintainer-contracts/official-sources/payment/2026-08-24"
)


def validate_snapshot(lock: dict[str, object], source_dir: Path, label: str) -> None:
    sources = lock["sources"]
    assert isinstance(sources, list)
    expected_files = {item["filename"] for item in sources}
    actual_files = {path.name for path in source_dir.iterdir() if path.is_file()}
    assert actual_files == expected_files, (
        f"{label} payment source file set changed: "
        f"missing={sorted(expected_files - actual_files)}, "
        f"extra={sorted(actual_files - expected_files)}"
    )
    for item in sources:
        raw = (source_dir / item["filename"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"], (
            f"{label} payment source SHA changed: {item['filename']}"
        )

HIGH_RISK_ANCHORS = {
    "lightning-intro": ("微信公众号", "银联付款码"),
    "aggregation-create": ("T_APP", "method_expand", "time_expire"),
    "aggregation-close": ("银联订单不支持关单", "一分钟"),
    "reconciliation-v2": ("file_details", "task_details", "MERGE_BILL", "Array"),
    "hosting-h5": ("channel_no", "pay_scene", "hosting_data"),
    "hosting-alipay-mini": ("channel_no", "pay_scene", "hosting_data"),
    "hosting-wechat-mini": ("channel_no", "pay_scene", "hosting_data"),
    "hosting-refund": (
        "mer_name",
        "org_ord_amt",
        "total_ref_amt",
        "acct_split_bunch",
    ),
    "split-detail-query": (
        "/v2/trade/trans/split/query",
        "180天",
        "split_trans_responses",
        "consume",
        "refund",
    ),
}


def main() -> int:
    assert default_lock_path("2026-08-31") == LOCK
    try:
        ensure_mutable_lock(HISTORICAL_LOCK)
    except ValueError:
        pass
    else:
        raise AssertionError("payment source refresher can overwrite the historical lock")

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert set(lock) == {
        "schema_version",
        "source_date",
        "source_snapshot_id",
        "verified_at",
        "source_count",
        "previous_source_lock",
        "sources",
        "current_extension",
    }, "current payment source lock schema changed"
    assert {
        key: lock[key]
        for key in ("schema_version", "source_date", "source_snapshot_id", "verified_at")
    } == {
        "schema_version": 1,
        "source_date": "2026-08-31",
        "source_snapshot_id": "2026-08-31",
        "verified_at": "2026-08-31T10:26:26+08:00",
    }, "current payment source metadata changed"
    assert lock["source_count"] == len(SOURCES) == 37
    source_dir = payment_source_dir()
    locked = {item["key"]: item for item in lock["sources"]}
    expected = {item.key: item for item in SOURCES}
    assert set(locked) == set(expected), "payment source keys changed"

    for key, spec in expected.items():
        item = locked[key]
        assert set(item) == {
            "key",
            "title",
            "filename",
            "url",
            "local_reference",
            "page_updated_at",
            "sha256",
            "semantic_sha256",
        }, f"{key}: payment source metadata schema changed"
        assert item["key"] == spec.key
        assert item["title"] == spec.title
        assert item["filename"] == spec.filename
        assert item["url"] == spec.url, f"{key}: URL changed"
        assert item["local_reference"] == spec.local_reference, (
            f"{key}: local reference changed"
        )
        assert (ROOT / "huifu-pay-integration/references" / spec.local_reference).is_file(), (
            f"{key}: local reference missing"
        )
        raw = (source_dir / spec.filename).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"], (
            f"{key}: raw SHA changed"
        )
        assert semantic_digest(raw) == item["semantic_sha256"], (
            f"{key}: semantic SHA changed"
        )
        assert page_update(raw) == item["page_updated_at"], (
            f"{key}: official page update metadata changed"
        )
        text = raw.decode("utf-8-sig")
        for anchor in HIGH_RISK_ANCHORS.get(key, ()):
            assert anchor in text, f"{key}: missing high-risk anchor {anchor}"

    historical_raw = HISTORICAL_LOCK.read_bytes()
    assert hashlib.sha256(historical_raw).hexdigest() == HISTORICAL_SHA256
    historical = json.loads(historical_raw)
    validate_snapshot(historical, HISTORICAL_SOURCE_DIR, "2026-07-28")
    previous_raw = PREVIOUS_LOCK.read_bytes()
    assert hashlib.sha256(previous_raw).hexdigest() == PREVIOUS_SHA256
    previous = json.loads(previous_raw)
    validate_snapshot(previous, PREVIOUS_SOURCE_DIR, "2026-08-24")
    changed = {"aggregation-query", "split-detail-query"}
    previous_by_key = {item["key"]: item for item in previous["sources"]}
    assert set(previous_by_key) == set(locked)
    for key in set(locked) - changed:
        assert lock["sources"][[item["key"] for item in lock["sources"]].index(key)] == previous_by_key[key]
        filename = locked[key]["filename"]
        assert (source_dir / filename).read_bytes() == (PREVIOUS_SOURCE_DIR / filename).read_bytes(), (
            f"unchanged payment source changed: {key}"
        )
    assert {key for key in locked if locked[key]["sha256"] != previous_by_key[key]["sha256"]} == changed
    assert locked["aggregation-query"] == {
        "key": "aggregation-query",
        "title": "聚合交易查询",
        "filename": "aggregation-query.md",
        "url": "https://paas.huifu.com/partners/lightning/api/jyddcx.md",
        "local_reference": "aggregation-query-payment-query.md",
        "page_updated_at": "2026-05-28",
        "sha256": "9e714b3db5c041bbc4732dec8db3b084f0d1f0464b67f759986cf40276747b92",
        "semantic_sha256": "175c3580aa04f2a8bdc40b80a92cfdd9003e62af03b99f437c2608201ff8c319",
    }
    assert locked["split-detail-query"] == {
        "key": "split-detail-query",
        "title": "交易分账明细查询",
        "filename": "split-detail-query.md",
        "url": "https://paas.huifu.com/partners/api/doc/smzf/api_fzmxcx.md",
        "local_reference": "trade-split-detail-query.md",
        "page_updated_at": "2024-12-20",
        "sha256": "dcab5eb128a7987742ea339631add74ad771227d3ce557c1154d6d6a27266270",
        "semantic_sha256": "3234017656cab6ee37a6194a98ca38bf9a252b70f6a5dd665c6bef0f8769e5b5",
    }
    assert lock["previous_source_lock"] == {
        "path": "maintainer-contracts/payment-source-lock-2026-08-24.json",
        "sha256": PREVIOUS_SHA256,
    }
    assert lock["current_extension"] == {
        "refresh_id": "api-refresh-payment-online-review-2026-08-31",
        "changed_source_keys": ["aggregation-query", "split-detail-query"],
        "field_paths_added": 0,
        "field_paths_removed": 0,
        "field_paths_changed": 18,
        "document_conflicts": [
            "aggregation-query still duplicates A_NATIVE for Alipay micropay even though the success example now uses A_MICROPAY",
            "split-detail-query example-only response.data.huifu_id is excluded from the formal catalog",
        ],
        "preserved_boundaries": [
            "split_trans_responses is String(JSON Array) and all sixteen decoded child paths retain []",
            "the twenty lightning guide pages and fifteen other formal API pages are byte-identical to the previous snapshot",
        ],
    }

    refresh = json.loads(
        (ROOT / "maintainer-contracts/api-refresh-2026-07-29.json").read_text(
            encoding="utf-8"
        )
    )
    onboarding_lock = json.loads(
        (
            ROOT / "maintainer-contracts/merchant-onboarding-source-lock.json"
        ).read_text(encoding="utf-8")
    )
    assert refresh["refresh_id"] == onboarding_lock["api_refresh"]["refresh_id"], (
        "API refresh ID differs between the refresh record and onboarding source lock"
    )
    versioning_policy = (
        ROOT / "maintainer-contracts/shared-versioning-policy.md"
    ).read_text(encoding="utf-8")
    assert f"`{refresh['refresh_id']}`" in versioning_policy, (
        "shared versioning policy does not name the current API refresh ID"
    )
    assert refresh["version_state"] == {
        "reason": "The fifth review refreshes official API evidence and link handling without changing either Skill package version.",
        "huifu-pay-integration": "1.3.3",
        "huifu-merchant-onboarding": "1.0.0",
    }
    for item in refresh["source_locks"].values():
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], (
            f"refresh source-lock digest changed: {item['path']}"
        )

    current_refresh = json.loads(
        (
            ROOT
            / "maintainer-contracts/api-refresh-payment-online-review-2026-08-31.json"
        ).read_text(encoding="utf-8")
    )
    expected_current_refresh = {
        "schema_version": 1,
        "refresh_id": "api-refresh-payment-online-review-2026-08-31",
        "requested_at": "2026-08-31",
        "retrieved_at": "2026-08-31T09:49:36+08:00",
        "version_state": {
        "reason": "Refresh two changed online payment pages in the unpublished huifu-pay-integration 1.3.5 candidate without changing its version.",
        "huifu-pay-integration": "1.3.5",
        "huifu-merchant-onboarding": "1.0.2",
        },
        "previous_refresh": {
            "path": "maintainer-contracts/api-refresh-trade-split-detail-query-2026-08-24.json",
            "sha256": "16089d56916b988a9d04a4d676dbffb0a5822a12fe2755c2eca1b3467a49047f",
            "refresh_id": "api-refresh-trade-split-detail-query-2026-08-24",
        },
        "source_locks": {
            "payment_1_3_5": {
                "path": "maintainer-contracts/payment-source-lock-2026-08-31.json",
                "sha256": "e66925bfb04bcb1b7ef4024f3e5d50f13f8cc1ac2f9bb08c33227f6d324fa288",
            },
            "payment_previous_unchanged": {
                "path": "maintainer-contracts/payment-source-lock-2026-08-24.json",
                "sha256": PREVIOUS_SHA256,
            },
        },
        "catalogs": {
            "payment": {
                "path": "huifu-pay-integration/references/payment-complete-field-catalog.md",
                "sha256": "d845fb02842f700c85fd736d5a327f762edd9b87cef92fa3ec8c8a3b034839de",
                "generator": "scripts/generate_payment_field_catalog.py",
                "independent_validator": "scripts/validate_payment_field_catalog.py",
            }
        },
        "scope": [
            "POST /v2/trade/payment/jspay/query aggregation trade query",
            "POST /v2/trade/trans/split/query transaction split-detail query",
        ],
        "field_delta": {
            "field_paths_added": 0,
            "field_paths_removed": 0,
            "field_paths_changed": 18,
            "catalog_total": 2656,
        },
        "preserved_boundaries": [
            "aggregation query method_expand remains one String(JSON Object) decode and the duplicate A_NATIVE description is corrected to A_MICROPAY",
            "the aggregation-query success example now uses A_MICROPAY",
            "split_trans_responses is String(JSON Array), decoded once, and all sixteen child paths retain []",
            "example-only response.data.huifu_id remains excluded from the split-detail field catalog and DTO",
            "the other thirty-five payment pages are byte-identical to the previous snapshot",
        ],
        "release_rule": "The 2,656-node payment catalog, both immutable predecessor locks, independent source and field validators, three-language SDK evidence, Skill validation, regression rules and package validation must pass before publishing huifu-pay-integration 1.3.5.",
    }
    assert current_refresh == expected_current_refresh, "current payment refresh contract changed"
    for item in current_refresh["source_locks"].values():
        path = ROOT / item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
    catalog = current_refresh["catalogs"]["payment"]
    assert hashlib.sha256((ROOT / catalog["path"]).read_bytes()).hexdigest() == catalog["sha256"]

    print("payment source contract validated: 37 locked pages and immutable predecessor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
