#!/usr/bin/env python3
"""Validate the active payment payment snapshot and its immutable predecessor."""

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
    from source_review_validation import validate_source, validate_release
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert default_lock_path(lock["source_date"]) == LOCK
    try:
        ensure_mutable_lock(HISTORICAL_LOCK)
    except ValueError:
        pass
    else:
        raise AssertionError("payment source refresher can overwrite historical lock")
    assert lock["source_count"] == len(SOURCES) == 44
    source_dir = validate_source(lock, "payment", [s.key for s in SOURCES])
    for item, spec in zip(lock["sources"], SOURCES):
        for key in ("key", "title", "filename", "url", "local_reference"):
            assert item[key] == getattr(spec, key), f"source metadata differs: {spec.key}.{key}"
        assert (ROOT / "huifu-pay-integration/references" / spec.local_reference).is_file()
        raw = (source_dir / spec.filename).read_bytes()
        assert semantic_digest(raw) == item["semantic_sha256"]
        assert page_update(raw) == item["page_updated_at"]
        for anchor in HIGH_RISK_ANCHORS.get(spec.key, ()):
            assert anchor in raw.decode("utf-8-sig"), f"missing high-risk anchor: {anchor}"
    for path, expected_hash, directory, date in (
        (HISTORICAL_LOCK, HISTORICAL_SHA256, HISTORICAL_SOURCE_DIR, "2026-07-28"),
        (PREVIOUS_LOCK, PREVIOUS_SHA256, PREVIOUS_SOURCE_DIR, "2026-08-24"),
    ):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash
        validate_snapshot(json.loads(path.read_text()), directory, date)
    release, review = validate_release("huifu-pay-integration")
    assert review["field_delta"]["catalog_total"] == lock["current_extension"]["catalog_total"] == 3096
    for metric in ("field_paths_added", "field_paths_removed", "field_paths_changed"):
        assert review["field_delta"][metric] == lock["current_extension"][metric]
    field_review = json.loads((ROOT / review["field_review"]["path"]).read_text())
    assert hashlib.sha256((ROOT / review["field_review"]["path"]).read_bytes()).hexdigest() == review["field_review"]["sha256"]
    delta = field_review["field_comparison"]["payment"]
    assert delta["after"] == review["field_delta"]["catalog_total"]
    for metric in ("added", "removed", "changed"):
        assert len(delta[metric]) == review["field_delta"][f"field_paths_{metric}"]
    print("payment source contract validated: 44 documents, immutable predecessors and reviewed bindings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
