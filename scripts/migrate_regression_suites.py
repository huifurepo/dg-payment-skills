#!/usr/bin/env python3
"""Assign the canonical cases to one primary Skill and emit suite files."""

from __future__ import annotations

import json
from pathlib import Path

from validation_runtime import require_assertions_enabled


require_assertions_enabled()


REPO_ROOT = Path(__file__).resolve().parent.parent
LEGACY = REPO_ROOT / "scripts/huifu-payment-test-prompts.json"
OUTPUT_DIR = REPO_ROOT / "tests/regression"
ONBOARDING_IDS = {52, *range(57, 85), 87, 88, 89, *range(301, 313)}


def main() -> int:
    cases = json.loads(LEGACY.read_text(encoding="utf-8"))
    payment = []
    onboarding = []
    for item in cases:
        case_id = int(item["id"])
        suite = "onboarding" if case_id in ONBOARDING_IDS else "payment"
        item["suite"] = suite
        if suite == "onboarding":
            item["prompt"] = item["prompt"].replace(
                "$huifu-pay-integration", "$huifu-merchant-onboarding"
            )
            item["expected"] = item["expected"].replace(
                "huifu-pay-integration", "huifu-merchant-onboarding"
            )
            onboarding.append(item)
        else:
            payment.append(item)
    assert len(payment) == 65
    assert len(onboarding) == 44
    LEGACY.write_text(
        json.dumps(cases, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, selected in (("payment.json", payment), ("onboarding.json", onboarding)):
        (OUTPUT_DIR / name).write_text(
            json.dumps(selected, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"regression suites generated: payment={len(payment)}, onboarding={len(onboarding)}, primary ownership={len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
