from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = REPO_ROOT / "skills-manifest.json"
EXPECTED_SKILL_TOP_LEVEL = {"SKILL.md", "agents", "references"}
ALLOWED_TOP_LEVEL_KEYS = {"name", "description"}
NAME_PATTERN = re.compile(r"^(?!-)(?!.*--)[a-z0-9-]{1,64}(?<!-)$")
MD_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?!https?://)(?!#)([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`\n]+)`")
SKIP_PARTS = {
    ".git",
    ".tmp",
    ".worktrees",
    ".codex-tasks",
    "node_modules",
    "docs",
    "official-sources",
}
MIN_SHORT_DESCRIPTION_LENGTH = 25
MAX_SHORT_DESCRIPTION_LENGTH = 64
LONG_REFERENCE_TOC_LINE_LIMIT = 100
LOCAL_PATH_PREFIXES = ("references/", "agents/", "scripts/")


@dataclass(frozen=True)
class SkillSpec:
    skill_id: str
    root: Path
    version: str
    domain: str
    agents_file: Path
    reference_manifest: Path
    max_reference_mentions: int
    canonical_regression_count: int

    @property
    def skill_file(self) -> Path:
        return self.root / "SKILL.md"

    @property
    def references_dir(self) -> Path:
        return self.root / "references"

    @property
    def expected_references(self) -> set[str]:
        payload = json.loads(self.reference_manifest.read_text(encoding="utf-8"))
        return set(payload["references"])


def load_skill_specs() -> tuple[SkillSpec, ...]:
    payload = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    return tuple(
        SkillSpec(
            skill_id=skill_id,
            root=REPO_ROOT / spec["root"],
            version=spec["version"],
            domain=spec["domain"],
            agents_file=REPO_ROOT / spec["root"] / spec["agents_file"],
            reference_manifest=REPO_ROOT / spec["reference_manifest"],
            max_reference_mentions=int(spec["max_reference_mentions"]),
            canonical_regression_count=int(spec["canonical_regression_count"]),
        )
        for skill_id, spec in payload["skills"].items()
    )


SKILL_SPECS = load_skill_specs()
SKILL_FILES = sorted(spec.skill_file for spec in SKILL_SPECS)
PAYMENT_SPEC = next(spec for spec in SKILL_SPECS if spec.domain == "payment")
ONBOARDING_SPEC = next(spec for spec in SKILL_SPECS if spec.domain == "onboarding")
ONBOARDING_SOURCE_LOCK = (
    REPO_ROOT / "maintainer-contracts/merchant-onboarding-source-lock.json"
)


def load_onboarding_source_lock() -> dict[str, object]:
    return json.loads(ONBOARDING_SOURCE_LOCK.read_text(encoding="utf-8"))


def onboarding_source_date() -> str:
    lock = load_onboarding_source_lock()
    source_date = lock.get("source_date")
    if not isinstance(source_date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", source_date):
        verified_at = lock.get("verified_at")
        if not isinstance(verified_at, str) or not re.match(r"\d{4}-\d{2}-\d{2}", verified_at):
            raise ValueError("merchant onboarding source lock has no valid source date")
        source_date = verified_at[:10]
    return source_date


def onboarding_source_dir() -> Path:
    return (
        REPO_ROOT
        / "maintainer-contracts/official-sources/merchant-onboarding"
        / onboarding_source_date()
    )

# Backward-compatible names for payment-only validators. New code should use
# SkillSpec and an explicit domain.
EXPECTED_SKILL_DIR = PAYMENT_SPEC.root
EXPECTED_SKILL_FILE = PAYMENT_SPEC.skill_file
EXPECTED_OPENAI_YAML = PAYMENT_SPEC.agents_file
EXPECTED_REFERENCES = PAYMENT_SPEC.expected_references
MAX_SKILL_REFERENCE_MENTIONS = PAYMENT_SPEC.max_reference_mentions


@dataclass
class ValidationState:
    errors: int = 0
    warnings: int = 0

    def ok(self, message: str) -> None:
        print(f"[OK]    {message}")

    def warning(self, message: str) -> None:
        print(f"[WARN]  {message}")
        self.warnings += 1

    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")
        self.errors += 1
