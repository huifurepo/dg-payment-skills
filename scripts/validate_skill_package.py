#!/usr/bin/env python3
"""Validate a Skill archive against current source and its provenance sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from validation_runtime import require_assertions_enabled


require_assertions_enabled()


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "skills-manifest.json"
PROVENANCE_SCHEMA_VERSION = 3
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_PROVENANCE_FIELDS = {
    "schema_version",
    "skill",
    "version",
    "source_commit",
    "source_dirty",
    "git_status",
    "source_date_epoch",
    "built_at",
    "skills_manifest_sha256",
    "reference_manifest_sha256",
    "refresh_id",
    "refresh_contract",
    "refresh_contract_sha256",
    "source_locks",
    "files",
    "test_evidence",
    "archive",
    "archive_sha256",
    "build",
}
REQUIRED_BUILD_FIELDS = {
    "builder",
    "builder_sha256",
    "command",
    "python_version",
    "archive_format",
    "compression",
    "entry_timestamp",
    "file_mode",
    "timestamp_source",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_text(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO_ROOT)


def no_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key in provenance: {key}")
        result[key] = value
    return result


def load_provenance(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=no_duplicate_json_keys,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"invalid provenance JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("provenance root must be an object")
    return payload


def validate_zip_names(names: list[str]) -> None:
    """Reject archive names whose extraction result is ambiguous or unsafe."""
    if len(names) != len(set(names)):
        duplicates = sorted({name for name in names if names.count(name) > 1})
        raise ValueError(f"duplicate ZIP entry: {duplicates}")
    folded: dict[str, str] = {}
    for name in names:
        if "\\" in name:
            raise ValueError(f"ZIP entry uses a backslash path separator: {name}")
        path = Path(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"unsafe ZIP entry path: {name}")
        normalized = name.casefold()
        previous = folded.get(normalized)
        if previous is not None and previous != name:
            raise ValueError(
                f"case-insensitive ZIP path collision: {previous!r} and {name!r}"
            )
        folded[normalized] = name


def package_paths(spec: dict[str, object]) -> set[str]:
    root = str(spec["root"])
    reference_manifest = json.loads(
        (REPO_ROOT / str(spec["reference_manifest"])).read_text(encoding="utf-8")
    )
    references = reference_manifest["references"]
    if any(
        not isinstance(name, str)
        or PurePosixPath(name).name != name
        or not name.endswith(".md")
        for name in references
    ):
        raise ValueError("reference manifest must contain direct Markdown filenames")
    return {
        f"{root}/SKILL.md",
        f"{root}/{spec['agents_file']}",
        *(f"{root}/references/{name}" for name in references),
    }


def require_sha256(value: object, label: str) -> None:
    if not isinstance(value, str) or not SHA256_PATTERN.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")


def validate_provenance_schema(provenance: dict[str, object]) -> None:
    missing = REQUIRED_PROVENANCE_FIELDS - set(provenance)
    if missing:
        raise ValueError(f"missing required provenance fields: {sorted(missing)}")
    if provenance["schema_version"] != PROVENANCE_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported provenance schema_version: {provenance['schema_version']!r}"
        )
    scalar_types = {
        "skill": str,
        "version": str,
        "source_commit": str,
        "source_dirty": bool,
        "git_status": str,
        "source_date_epoch": int,
        "built_at": str,
        "refresh_id": str,
        "refresh_contract": str,
        "archive": str,
    }
    for key, expected_type in scalar_types.items():
        if not isinstance(provenance[key], expected_type):
            raise ValueError(f"provenance {key} must be {expected_type.__name__}")
    source_commit = provenance["source_commit"]
    if not isinstance(source_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("provenance source_commit must be a full lowercase Git SHA")
    for key in (
        "skills_manifest_sha256",
        "reference_manifest_sha256",
        "refresh_contract_sha256",
        "archive_sha256",
    ):
        require_sha256(provenance[key], f"provenance {key}")
    for key in ("files", "test_evidence", "source_locks"):
        mapping = provenance[key]
        if not isinstance(mapping, dict):
            raise ValueError(f"provenance {key} must be an object")
        for name, digest_value in mapping.items():
            if not isinstance(name, str):
                raise ValueError(f"provenance {key} keys must be strings")
            require_sha256(digest_value, f"provenance {key}[{name!r}]")
    build = provenance["build"]
    if not isinstance(build, dict):
        raise ValueError("provenance build must be an object")
    missing_build = REQUIRED_BUILD_FIELDS - set(build)
    if missing_build:
        raise ValueError(f"missing required provenance build fields: {sorted(missing_build)}")
    if build.get("builder") != "scripts/package_skill.py":
        raise ValueError("provenance build builder mismatch")
    require_sha256(build.get("builder_sha256"), "provenance build builder_sha256")
    if not isinstance(build.get("command"), list) or not all(
        isinstance(part, str) for part in build["command"]
    ):
        raise ValueError("provenance build command must be a string array")
    for key in REQUIRED_BUILD_FIELDS - {"command"}:
        if not isinstance(build.get(key), str):
            raise ValueError(f"provenance build {key} must be a string")
    if build.get("timestamp_source") != "git-commit":
        raise ValueError("provenance timestamp source must be git-commit")


def validate_refresh_source_bindings(
    provenance: dict[str, object],
    spec: dict[str, object],
) -> None:
    refresh_contract_name = str(spec["refresh_contract"])
    source_lock_name = str(spec["source_lock"])
    if provenance["refresh_contract"] != refresh_contract_name:
        raise ValueError("provenance refresh contract path differs from Skill manifest")
    refresh_contract_path = REPO_ROOT / refresh_contract_name
    source_lock_path = REPO_ROOT / source_lock_name
    if not refresh_contract_path.is_file() or not source_lock_path.is_file():
        raise ValueError("refresh contract or source lock is missing")
    refresh_contract = json.loads(refresh_contract_path.read_text(encoding="utf-8"))
    if provenance["refresh_id"] != refresh_contract["refresh_id"]:
        raise ValueError("provenance refresh ID differs from refresh contract")
    if provenance["refresh_contract_sha256"] != sha256(
        refresh_contract_path.read_bytes()
    ):
        raise ValueError("provenance refresh contract SHA differs from current contract")
    expected_source_locks = {
        source_lock_name: sha256(source_lock_path.read_bytes()),
    }
    if provenance["source_locks"] != expected_source_locks:
        raise ValueError("provenance source-lock map differs from Skill manifest")
    matching_source_locks = [
        item
        for item in refresh_contract["source_locks"].values()
        if item["path"] == source_lock_name
    ]
    if len(matching_source_locks) != 1:
        raise ValueError("refresh contract does not bind the Skill source lock exactly once")
    if matching_source_locks[0]["sha256"] != expected_source_locks[source_lock_name]:
        raise ValueError("refresh contract source-lock digest differs from current source lock")


def validate_reproducible_build_metadata(
    provenance: dict[str, object],
    skill: str,
) -> None:
    source_commit = str(provenance["source_commit"])
    expected_epoch = int(git_text("show", "-s", "--format=%ct", source_commit))
    expected_built_at = (
        datetime.fromtimestamp(expected_epoch, timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
    if provenance["source_date_epoch"] != expected_epoch:
        raise ValueError("provenance source_date_epoch differs from Git commit")
    if provenance["built_at"] != expected_built_at:
        raise ValueError("provenance built_at differs from deterministic Git timestamp")
    build = provenance["build"]
    assert isinstance(build, dict)
    builder = REPO_ROOT / str(build["builder"])
    if not builder.is_file() or build["builder_sha256"] != sha256(builder.read_bytes()):
        raise ValueError("provenance builder digest differs from current builder")
    expected_command = [
        "python3",
        "scripts/package_skill.py",
        "--skill",
        skill,
        "--output-dir",
        "<OUTPUT_DIR>",
    ]
    if provenance["source_dirty"]:
        expected_command.append("--allow-dirty")
    for evidence_key in sorted(provenance["test_evidence"]):
        expected_command.extend(["--evidence", f"{evidence_key}=<EVIDENCE_FILE>"])
    if build["command"] != expected_command:
        raise ValueError("provenance canonical build command mismatch")


def validate_published_version_facts(
    skill_text: str,
    policy_text: str,
    skill: str,
    version: str,
) -> None:
    if f"| Skill 版本 | `{version}` |" not in skill_text:
        raise ValueError(f"{skill}: SKILL.md version differs from manifest {version}")
    if f"| Skill | `{skill} {version}` |" not in policy_text:
        raise ValueError(
            f"{skill}: references/skill-version-policy.md differs from manifest {version}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--allow-dirty-provenance", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    spec = manifest["skills"][args.skill]
    try:
        allowed_files = package_paths(spec)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    provenance_path = args.archive.with_suffix(".provenance.json")
    checksum_path = args.archive.with_suffix(".zip.sha256")
    if not provenance_path.is_file() or not checksum_path.is_file():
        raise SystemExit("package provenance and SHA-256 sidecars are required")
    try:
        provenance = load_provenance(provenance_path)
        validate_provenance_schema(provenance)
        validate_reproducible_build_metadata(provenance, args.skill)
        validate_refresh_source_bindings(provenance, spec)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    current_status = git_text("status", "--porcelain=v1")
    if provenance.get("source_dirty"):
        expected = {
            name: sha256((REPO_ROOT / name).read_bytes())
            for name in sorted(allowed_files)
        }
    else:
        source_commit = provenance.get("source_commit")
        expected = {
            name: sha256(git_bytes(str(source_commit), name))
            for name in sorted(allowed_files)
        }
    with zipfile.ZipFile(args.archive) as archive:
        archive_names = archive.namelist()
        try:
            validate_zip_names(archive_names)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        names = set(archive_names)
        if names != set(expected):
            raise SystemExit(
                f"archive file set mismatch; missing={sorted(set(expected)-names)}, "
                f"extra={sorted(names-set(expected))}"
            )
        for name, expected_digest in expected.items():
            actual = sha256(archive.read(name))
            if actual != expected_digest:
                raise SystemExit(f"{name}: archive content differs from source")
        root = str(spec["root"])
        try:
            validate_published_version_facts(
                archive.read(f"{root}/SKILL.md").decode("utf-8"),
                archive.read(f"{root}/references/skill-version-policy.md").decode("utf-8"),
                args.skill,
                str(spec["version"]),
            )
        except (KeyError, UnicodeDecodeError, ValueError) as exc:
            raise SystemExit(str(exc)) from exc
    archive_digest = sha256(args.archive.read_bytes())
    expected_checksum = f"{archive_digest}  {args.archive.name}\n"
    if checksum_path.read_text(encoding="utf-8") != expected_checksum:
        raise SystemExit("SHA-256 sidecar mismatch")
    if provenance.get("archive") != args.archive.name:
        raise SystemExit("provenance archive name mismatch")
    if provenance.get("archive_sha256") != archive_digest:
        raise SystemExit("provenance archive SHA mismatch")
    if provenance.get("skill") != args.skill or provenance.get("version") != spec["version"]:
        raise SystemExit("provenance skill/version mismatch")
    if provenance.get("skills_manifest_sha256") != sha256(MANIFEST.read_bytes()):
        raise SystemExit("provenance skills manifest SHA mismatch")
    reference_manifest = REPO_ROOT / spec["reference_manifest"]
    if provenance.get("reference_manifest_sha256") != sha256(reference_manifest.read_bytes()):
        raise SystemExit("provenance reference manifest SHA mismatch")
    if provenance.get("files") != expected:
        raise SystemExit("provenance file map mismatch")
    if provenance.get("source_commit") != git_text("rev-parse", "HEAD"):
        raise SystemExit("provenance source commit mismatch")
    source_dirty = provenance.get("source_dirty")
    if not isinstance(source_dirty, bool):
        raise SystemExit("provenance source_dirty must be boolean")
    if bool(provenance.get("git_status")) != source_dirty:
        raise SystemExit("provenance dirty flag and git status disagree")
    if source_dirty and not args.allow_dirty_provenance:
        raise SystemExit("dirty-source provenance is not valid for release")
    if provenance.get("git_status") != current_status:
        raise SystemExit("provenance git status differs from current source")
    print(f"package validated: {args.skill} ({len(expected)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
