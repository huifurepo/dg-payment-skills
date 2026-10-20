"""Locate preserved historical documents after the third-round package cleanup."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "maintainer-contracts/reference-retirements-2026-10-10.json"


def retirement_entries() -> list[dict]:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))["entries"]


def historical_reference(path: Path) -> Path:
    """Resolve only explicitly retired paths; ordinary missing files remain errors."""
    relative = path.relative_to(ROOT).as_posix()
    for entry in retirement_entries():
        if entry["source"] == relative:
            return ROOT / entry["archive"]
    return path


def canonical_regression_files(skill_root: Path) -> list[Path]:
    return [
        ROOT / entry["archive"]
        for entry in retirement_entries()
        if entry["source"].startswith(skill_root.name + "/references/")
        and entry["source"].endswith("canonical-regression-prompts.md")
    ]
