from __future__ import annotations

from pathlib import Path

from skill_validation_config import (
    EXPECTED_SKILL_DIR,
    EXPECTED_SKILL_TOP_LEVEL,
    LOCAL_PATH_PREFIXES,
    REPO_ROOT,
    SKIP_PARTS,
    ValidationState,
)


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def looks_like_local_path(candidate: str) -> bool:
    if "*" in candidate:
        return False
    if any(char.isspace() for char in candidate):
        return False
    if candidate.startswith(("http://", "https://", "#", "/", "$", "<")):
        return False
    return candidate.startswith(LOCAL_PATH_PREFIXES)


def validate_repo_files(state: ValidationState) -> None:
    print("\n--- 仓库辅助文件检查（非官方规范） ---")
    required_files = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "CHANGELOG.md",
    ]
    for file_path in required_files:
        if file_path.exists():
            state.ok(f"{file_path.relative_to(REPO_ROOT)} exists")
        else:
            state.warning(f"{file_path.relative_to(REPO_ROOT)} missing")


def validate_skill_top_level(state: ValidationState) -> None:
    actual = {path.name for path in EXPECTED_SKILL_DIR.iterdir()}
    missing = sorted(EXPECTED_SKILL_TOP_LEVEL - actual)
    extra = sorted(actual - EXPECTED_SKILL_TOP_LEVEL)
    if missing:
        state.error(f"missing skill top-level entries: {', '.join(missing)}")
    if extra:
        state.error(f"unexpected skill top-level entries: {', '.join(extra)}")
    if not missing and not extra:
        state.ok("skill top-level entries match upload package allowlist")


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
