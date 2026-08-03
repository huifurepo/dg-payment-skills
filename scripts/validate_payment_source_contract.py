#!/usr/bin/env python3
"""Validate the locked 36-page payment source snapshot and high-risk anchors."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from refresh_payment_sources import SOURCES, semantic_digest
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "maintainer-contracts/payment-source-lock.json"

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
}


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert lock["source_count"] == len(SOURCES) == 36
    source_dir = (
        ROOT
        / "maintainer-contracts/official-sources/payment"
        / lock["source_date"]
    )
    locked = {item["key"]: item for item in lock["sources"]}
    expected = {item.key: item for item in SOURCES}
    assert set(locked) == set(expected), "payment source keys changed"

    for key, spec in expected.items():
        item = locked[key]
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
        text = raw.decode("utf-8-sig")
        for anchor in HIGH_RISK_ANCHORS.get(key, ()):
            assert anchor in text, f"{key}: missing high-risk anchor {anchor}"

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

    print("payment source contract validated: 36 locked pages and high-risk anchors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
