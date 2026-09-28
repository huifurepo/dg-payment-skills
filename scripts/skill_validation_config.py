from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict


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


class SourceDigest(TypedDict):
    path: str
    sha256: str


class SDKComponent(TypedDict):
    version: str
    relative_root: str
    version_file: str
    file_count: int
    tree_sha256: str
    selected_sources: list[SourceDigest]


class SDKSourceLock(TypedDict):
    schema_version: int
    verified_at: str
    components: dict[str, SDKComponent]


SDK_SOURCE_LOCK = REPO_ROOT / json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))["sdk_source_lock"]


def load_sdk_source_lock() -> SDKSourceLock:
    """Read the manifest-selected local-source evidence, not a remote SDK registry."""
    payload = json.loads(SDK_SOURCE_LOCK.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("components"), dict):
        raise ValueError("invalid active SDK source lock")
    for name, component in payload["components"].items():
        if not isinstance(component.get("version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", component["version"]):
            raise ValueError(f"{name}: invalid SDK source version")
        root = component.get("relative_root")
        if not isinstance(root, str) or not root or Path(root).is_absolute() or ".." in Path(root).parts:
            raise ValueError(f"{name}: invalid SDK relative root")
    return payload


def sdk_version(name: str) -> str:
    return load_sdk_source_lock()["components"][name]["version"]


def sdk_root_relative(name: str) -> str:
    return load_sdk_source_lock()["components"][name]["relative_root"]


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
PAYMENT_SOURCE_LOCK = (
    REPO_ROOT / "maintainer-contracts/payment-source-lock-2026-08-31.json"
)
ONBOARDING_SOURCE_LOCK = (
    REPO_ROOT / "maintainer-contracts/merchant-onboarding-source-lock-2026-09-22.json"
)
USER_ONBOARDING_SOURCE_LOCK = (
    REPO_ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-09-22.json"
)
ONBOARDING_EXTENSION_SOURCE_LOCK = (
    REPO_ROOT / "maintainer-contracts/onboarding-extension-source-lock-2026-09-22.json"
)


def load_payment_source_lock() -> dict[str, object]:
    return json.loads(PAYMENT_SOURCE_LOCK.read_text(encoding="utf-8"))


def payment_source_dir() -> Path:
    lock = load_payment_source_lock()
    snapshot_id = lock.get("source_snapshot_id", lock.get("source_date"))
    if not isinstance(snapshot_id, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}(?:-r\d+)?", snapshot_id
    ):
        raise ValueError("payment source lock has no valid source snapshot id")
    return REPO_ROOT / "maintainer-contracts/official-sources/payment" / snapshot_id


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
    lock = load_onboarding_source_lock()
    snapshot_id = lock.get("source_snapshot_id", onboarding_source_date())
    if not isinstance(snapshot_id, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}(?:-r\d+)?", snapshot_id
    ):
        raise ValueError("merchant onboarding source lock has no valid source snapshot id")
    return (
        REPO_ROOT
        / "maintainer-contracts/official-sources/merchant-onboarding"
        / snapshot_id
    )


def load_user_onboarding_source_lock() -> dict[str, object]:
    return json.loads(USER_ONBOARDING_SOURCE_LOCK.read_text(encoding="utf-8"))


def user_onboarding_source_dir() -> Path:
    lock = load_user_onboarding_source_lock()
    snapshot_id = lock.get("source_snapshot_id", lock.get("source_date"))
    if not isinstance(snapshot_id, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}(?:-r\d+)?", snapshot_id
    ):
        raise ValueError("user onboarding source lock has no valid snapshot id")
    return REPO_ROOT / "maintainer-contracts/official-sources/user-onboarding" / snapshot_id


def load_onboarding_extension_source_lock() -> dict[str, object]:
    return json.loads(ONBOARDING_EXTENSION_SOURCE_LOCK.read_text(encoding="utf-8"))


def onboarding_extension_source_dir() -> Path:
    lock = load_onboarding_extension_source_lock()
    snapshot_id = lock.get("source_snapshot_id", lock.get("source_date"))
    if not isinstance(snapshot_id, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}(?:-r\d+)?", snapshot_id
    ):
        raise ValueError("onboarding extension source lock has no valid snapshot id")
    return REPO_ROOT / "maintainer-contracts/official-sources/onboarding-extension" / snapshot_id

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
