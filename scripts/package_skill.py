#!/usr/bin/env python3
"""Build a deterministic, self-contained Skill ZIP plus provenance sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "skills-manifest.json"
PROVENANCE_SCHEMA_VERSION = 3


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_text(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO_ROOT)


def git_commit_epoch(commit: str) -> int:
    return int(git_text("show", "-s", "--format=%ct", commit))


def reproducible_build_timestamp(source_commit: str) -> tuple[int, str]:
    """Return a deterministic RFC 3339 timestamp sourced from the Git commit."""
    epoch = git_commit_epoch(source_commit)
    timestamp = datetime.fromtimestamp(epoch, timezone.utc).isoformat().replace("+00:00", "Z")
    return epoch, timestamp


def parse_evidence_argument(argument: str) -> tuple[str | None, Path]:
    """Parse an optional stable provenance label and its local evidence path."""
    if "=" not in argument:
        return None, Path(argument)
    label, raw_path = argument.split("=", 1)
    label_path = PurePosixPath(label)
    if (
        not label
        or not raw_path
        or "\\" in label
        or label_path.is_absolute()
        or label != label_path.as_posix()
        or any(part in {"", ".", ".."} for part in label_path.parts)
    ):
        raise ValueError(f"unsafe evidence label: {label!r}")
    return label, Path(raw_path)


def add_bytes(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


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


def source_bindings(manifest: dict, spec: dict, refresh: dict) -> dict[str, str]:
    """Bind both business API evidence and the selected SDK source evidence."""
    if "sdk_source_lock" not in spec:
        name = spec["source_lock"]
        digest = sha256_file(REPO_ROOT / name)
        matches = [item for item in refresh["source_locks"].values() if item["path"] == name]
        if len(matches) != 1 or matches[0]["sha256"] != digest:
            raise ValueError("refresh contract source-lock digest differs from current source lock")
        return {name: digest}
    bindings = {}
    for name in (spec["source_lock"], spec["sdk_source_lock"]):
        path = REPO_ROOT / name
        if not path.is_file():
            raise ValueError(f"source lock is missing: {name}")
        matches = [item for item in refresh["source_locks"].values() if item["path"] == name]
        digest = sha256_file(path)
        if len(matches) != 1 or matches[0]["sha256"] != digest:
            raise ValueError(f"refresh contract must bind current source lock exactly once: {name}")
        bindings[name] = digest
    sdk = json.loads((REPO_ROOT / spec["sdk_source_lock"]).read_text(encoding="utf-8"))
    versions = {name: item["version"] for name, item in sdk["components"].items()}
    if refresh.get("sdk_versions") != versions or refresh.get("sdk_reviewed_at") != sdk["verified_at"]:
        raise ValueError("refresh contract SDK versions/date differ from selected source evidence")
    if refresh.get("python_sdk") != {"target_version": versions["python"], "verified_source_version": versions["python"], "target_source_verified": True}:
        raise ValueError("refresh contract Python SDK facts differ from selected source evidence")
    for skill, entry in manifest["skills"].items():
        # A companion version is the refresh's dated snapshot, not this package's
        # release authority. Independently bumping it must not invalidate this ZIP.
        if entry["root"] == spec["root"] and refresh["version_state"].get(skill) != entry["version"]:
            raise ValueError(f"refresh contract current Skill version differs: {skill}")
    for key in ("previous_refresh", "source_review"):
        item = refresh[key]
        path = REPO_ROOT / item["path"]
        if sha256_file(path) != item["sha256"] or json.loads(path.read_text(encoding="utf-8"))["refresh_id"] != item["refresh_id"]:
            raise ValueError(f"refresh contract {key} binding differs")
    if refresh["source_review"]["refresh_id"] != refresh["source_review_id"]:
        raise ValueError("refresh contract API source review identity differs")
    return bindings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--evidence", action="append", default=[])
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if args.skill not in manifest["skills"]:
        raise SystemExit(f"unknown skill: {args.skill}")
    spec = manifest["skills"][args.skill]
    root = REPO_ROOT / spec["root"]
    status = git_text("status", "--porcelain=v1")
    if status and not args.allow_dirty:
        raise SystemExit(f"repository is dirty; commit before release packaging:\n{status}")

    source_commit = git_text("rev-parse", "HEAD")
    if status:
        files = {
            path.relative_to(REPO_ROOT).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }
    else:
        tracked = git_text(
            "ls-tree", "-r", "--name-only", source_commit, "--", str(spec["root"])
        ).splitlines()
        files = {name: git_bytes(source_commit, name) for name in tracked}
    try:
        allowed_files = package_paths(spec)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    refresh_contract_path = REPO_ROOT / str(spec["refresh_contract"])
    source_lock_path = REPO_ROOT / str(spec["source_lock"])
    if not refresh_contract_path.is_file() or not source_lock_path.is_file():
        raise SystemExit("refresh contract or source lock is missing")
    refresh_contract = json.loads(refresh_contract_path.read_text(encoding="utf-8"))
    try:
        current_source_bindings = source_bindings(manifest, spec, refresh_contract)
    except (KeyError, ValueError) as exc:
        raise SystemExit(f"invalid refresh/source binding: {exc}") from exc
    actual_files = set(files)
    if actual_files != allowed_files:
        raise SystemExit(
            "Skill source file set differs from package allowlist; "
            f"missing={sorted(allowed_files - actual_files)}, "
            f"extra={sorted(actual_files - allowed_files)}"
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = args.output_dir / f"{args.skill}-{spec['version']}.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name, data in sorted(files.items()):
            add_bytes(archive, name, data)

    evidence = {}
    for evidence_argument in args.evidence:
        try:
            explicit_key, path = parse_evidence_argument(evidence_argument)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        resolved = path if path.is_absolute() else REPO_ROOT / path
        if not resolved.is_file():
            raise SystemExit(f"evidence file missing: {path}")
        if explicit_key is not None:
            evidence_key = explicit_key
        else:
            try:
                evidence_key = resolved.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
            except ValueError:
                evidence_key = f"external/{resolved.name}"
        if evidence_key in evidence:
            raise SystemExit(f"duplicate evidence name: {evidence_key}")
        evidence[evidence_key] = sha256_file(resolved)
    source_date_epoch, built_at = reproducible_build_timestamp(source_commit)
    builder_path = REPO_ROOT / "scripts/package_skill.py"
    build_command = [
        "python3",
        "scripts/package_skill.py",
        "--skill",
        args.skill,
        "--output-dir",
        "<OUTPUT_DIR>",
    ]
    if status:
        build_command.append("--allow-dirty")
    for evidence_key in sorted(evidence):
        build_command.extend(["--evidence", f"{evidence_key}=<EVIDENCE_FILE>"])
    provenance = {
        "schema_version": PROVENANCE_SCHEMA_VERSION,
        "skill": args.skill,
        "version": spec["version"],
        "source_commit": source_commit,
        "source_dirty": bool(status),
        "git_status": status,
        "source_date_epoch": source_date_epoch,
        "built_at": built_at,
        "skills_manifest_sha256": sha256_file(MANIFEST),
        "reference_manifest_sha256": sha256_file(REPO_ROOT / spec["reference_manifest"]),
        "refresh_id": refresh_contract["refresh_id"],
        "refresh_contract": str(spec["refresh_contract"]),
        "refresh_contract_sha256": sha256_file(refresh_contract_path),
        "source_locks": current_source_bindings,
        "files": {name: sha256_bytes(data) for name, data in sorted(files.items())},
        "test_evidence": dict(sorted(evidence.items())),
        "archive": archive_path.name,
        "archive_sha256": sha256_file(archive_path),
        "build": {
            "builder": "scripts/package_skill.py",
            "builder_sha256": sha256_file(builder_path),
            "command": build_command,
            "python_version": platform.python_version(),
            "archive_format": "zip",
            "compression": "ZIP_DEFLATED",
            "entry_timestamp": "1980-01-01T00:00:00Z",
            "file_mode": "0100644",
            "timestamp_source": "git-commit",
        },
    }
    provenance_path = archive_path.with_suffix(".provenance.json")
    provenance_path.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    archive_path.with_suffix(".zip.sha256").write_text(
        f"{provenance['archive_sha256']}  {archive_path.name}\n",
        encoding="utf-8",
    )
    print(f"built: {archive_path}")
    print(f"sha256: {provenance['archive_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
