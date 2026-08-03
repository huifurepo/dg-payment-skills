#!/usr/bin/env python3
"""Build the immutable 1.3.2 reference migration ledger before the split."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_COMMIT = "ff7b6acde574f498fde9c6f0763078b0e2eea3b7"
MIGRATION_COMMIT = "e12651efb2ed550af9c632d472cb39499a1746de"
SOURCE_ROOT = "huifu-pay-integration/references"

MOVE = {
    "merchant-onboarding-application-status-query.md",
    "merchant-onboarding-business-open.md",
    "merchant-onboarding-complete-field-catalog.md",
    "merchant-onboarding-detail-query.md",
    "merchant-onboarding-enterprise.md",
    "merchant-onboarding-external-resources.md",
    "merchant-onboarding-individual.md",
}
SPLIT = {
    "canonical-regression-prompts.md",
    "copilot-troubleshooting-playbooks.md",
    "hostingpay-error-codes.md",
    "merchant-onboarding-faq.md",
    "official-service-source-index.md",
    "shared-copyright-notice.md",
    "shared-credential-boundary.md",
    "shared-overview.md",
    "shared-request-field-preservation.md",
    "shared-request-header-policy.md",
    "shared-server-sdk-matrix.md",
    "shared-signing-v2.md",
    "skill-version-policy.md",
}
REWRITE_PAYMENT = {
    "aggregation-customer-preparation.md",
    "aggregation-order-method-alipay.md",
    "aggregation-order-method-unionpay.md",
    "aggregation-order-method-wechat.md",
    "copilot-solution-cards.md",
    "hostingpay-async-webhook.md",
    "shared-async-notify.md",
    "shared-local-sandbox.md",
}
REWRITE_ONBOARDING = {
    "merchant-onboarding-field-contracts.md",
    "merchant-onboarding-image-upload.md",
}
REPO_ONLY = {
    "shared-release-checklist.md",
    "shared-versioning-policy.md",
}


def baseline_bytes(relative_path: str) -> bytes:
    """Read canonical bytes from the declared baseline commit."""
    return commit_bytes(BASELINE_COMMIT, relative_path)


def commit_bytes(commit: str, relative_path: str) -> bytes:
    """Read a Git blob so the ledger is independent of checkout line endings."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{relative_path}"],
            cwd=REPO_ROOT,
        )
    except subprocess.CalledProcessError as exc:
        raise FileNotFoundError(f"{relative_path} is missing from {commit}") from exc


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def headings(text: str) -> list[dict[str, object]]:
    result = []
    for line_number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if match:
            result.append(
                {
                    "level": len(match.group(1)),
                    "heading": match.group(2),
                    "source_line": line_number,
                }
            )
    return result


def destinations(name: str, category: str) -> list[dict[str, object]]:
    if category == "KEEP":
        return [
            {
                "scope": "payment",
                "path": f"huifu-pay-integration/references/{name}",
                "operation": "keep",
                "expect_byte_identical": True,
            }
        ]
    if category == "MOVE":
        return [
            {
                "scope": "onboarding",
                "path": f"huifu-merchant-onboarding/references/{name}",
                "operation": "move",
                "expect_byte_identical": True,
            }
        ]
    if category == "REWRITE_PAYMENT":
        return [
            {
                "scope": "payment",
                "path": f"huifu-pay-integration/references/{name}",
                "operation": "rewrite",
                "expect_byte_identical": False,
            }
        ]
    if category == "REWRITE_ONBOARDING":
        return [
            {
                "scope": "onboarding",
                "path": f"huifu-merchant-onboarding/references/{name}",
                "operation": "rewrite",
                "expect_byte_identical": False,
            }
        ]
    if category == "REPO_ONLY":
        return [
            {
                "scope": "repo",
                "path": f"maintainer-contracts/{name}",
                "operation": "move",
                "expect_byte_identical": True,
            }
        ]
    payment_name = "payment-operations-faq.md" if name == "merchant-onboarding-faq.md" else name
    onboarding_name = (
        "merchant-onboarding-error-codes.md" if name == "hostingpay-error-codes.md" else name
    )
    return [
        {
            "scope": "payment",
            "path": f"huifu-pay-integration/references/{payment_name}",
            "operation": "split",
            "expect_byte_identical": False,
        },
        {
            "scope": "onboarding",
            "path": f"huifu-merchant-onboarding/references/{onboarding_name}",
            "operation": "split",
            "expect_byte_identical": False,
        },
    ]


def category_for(name: str) -> str:
    memberships = [
        ("MOVE", name in MOVE),
        ("SPLIT", name in SPLIT),
        ("REWRITE_PAYMENT", name in REWRITE_PAYMENT),
        ("REWRITE_ONBOARDING", name in REWRITE_ONBOARDING),
        ("REPO_ONLY", name in REPO_ONLY),
    ]
    matched = [category for category, present in memberships if present]
    if len(matched) > 1:
        raise ValueError(f"{name}: multiple migration categories: {matched}")
    return matched[0] if matched else "KEEP"


def build() -> dict[str, object]:
    names = sorted(
        line
        for line in subprocess.check_output(
            ["git", "ls-tree", "--name-only", f"{BASELINE_COMMIT}:{SOURCE_ROOT}"],
            cwd=REPO_ROOT,
            text=True,
        ).splitlines()
        if line.endswith(".md")
    )
    if len(names) != 110:
        raise ValueError(f"expected 110 baseline references, found {len(names)}")

    entries = []
    for name in names:
        relative_path = f"{SOURCE_ROOT}/{name}"
        data = baseline_bytes(relative_path)
        text = data.decode("utf-8")
        category = category_for(name)
        sealed_destinations = []
        for destination in destinations(name, category):
            destination_data = commit_bytes(MIGRATION_COMMIT, str(destination["path"]))
            destination_text = destination_data.decode("utf-8")
            sealed_destinations.append(
                {
                    **destination,
                    "migration_commit": MIGRATION_COMMIT,
                    "migration_sha256": sha256(destination_data),
                    "migration_size_bytes": len(destination_data),
                    "migration_line_count": len(destination_text.splitlines()),
                    "migration_headings": (
                        headings(destination_text)
                        if category in {"SPLIT", "REWRITE_PAYMENT", "REWRITE_ONBOARDING"}
                        else []
                    ),
                }
            )
        entries.append(
            {
                "source_path": relative_path,
                "source_basename": name,
                "source_sha256": sha256(data),
                "source_size_bytes": len(data),
                "source_line_count": len(text.splitlines()),
                "category": category,
                "destinations": sealed_destinations,
                "source_headings": headings(text) if category in {"SPLIT", "REWRITE_PAYMENT", "REWRITE_ONBOARDING"} else [],
                "cross_skill_link_allowed": False,
                "status": "completed",
            }
        )

    counts: dict[str, int] = {}
    for entry in entries:
        category = str(entry["category"])
        counts[category] = counts.get(category, 0) + 1
    expected = {
        "KEEP": 78,
        "MOVE": 7,
        "SPLIT": 13,
        "REWRITE_PAYMENT": 8,
        "REWRITE_ONBOARDING": 2,
        "REPO_ONLY": 2,
    }
    if counts != expected:
        raise ValueError(f"unexpected migration counts: {counts}")
    return {
        "schema_version": 1,
        "baseline_commit": BASELINE_COMMIT,
        "migration_commit": MIGRATION_COMMIT,
        "review_basis": (
            "All 110 baseline blobs and every post-migration destination blob are sealed by "
            "commit and SHA-256; SPLIT/REWRITE transformations also retain source and "
            "destination heading inventories for independent content review."
        ),
        "source_root": SOURCE_ROOT,
        "source_reference_count": len(entries),
        "category_counts": counts,
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "maintainer-contracts/reference-migration-ledger.json",
    )
    args = parser.parse_args()
    payload = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"generated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
