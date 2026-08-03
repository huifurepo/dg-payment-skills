#!/usr/bin/env python3
"""Update exact per-Skill reference manifests from the current source tree."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "skills-manifest.json"


def main() -> int:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for skill_id, spec in payload["skills"].items():
        root = REPO_ROOT / spec["root"]
        references = sorted(path.name for path in (root / "references").glob("*.md"))
        output = REPO_ROOT / spec["reference_manifest"]
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "skill": skill_id,
                    "reference_count": len(references),
                    "references": references,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"{skill_id}: {len(references)} references -> {output.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
