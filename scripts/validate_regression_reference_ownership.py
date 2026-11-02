#!/usr/bin/env python3
"""Ensure single-Skill regression cases only require references they can load."""

from __future__ import annotations

import json
import re
from pathlib import Path

from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
SUITES = {
    "payment": ROOT / "huifu-pay-integration/references",
    "onboarding": ROOT / "huifu-merchant-onboarding/references",
    "user-onboarding": ROOT / "huifu-merchant-onboarding/references",
}
REFERENCE_PATTERN = re.compile(r"`([^`/]+\.md)`")


def main() -> int:
    errors: list[str] = []
    additions = json.loads((ROOT / "tests/regression/interface-expansion.json").read_text(encoding="utf-8"))
    for suite, reference_dir in SUITES.items():
        available = {path.name for path in reference_dir.glob("*.md")}
        cases = json.loads(
            (ROOT / f"tests/regression/{suite}.json").read_text(encoding="utf-8")
        )
        cases.extend(case for case in additions if case["suite"] == suite)
        for case in cases:
            required = set(REFERENCE_PATTERN.findall(case["expected"]))
            missing = sorted(required - available)
            if missing:
                errors.append(
                    f"{suite} case {case['id']}: unavailable references {missing}"
                )
    assert not errors, "\n".join(errors)
    print("single-Skill regression reference ownership validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
