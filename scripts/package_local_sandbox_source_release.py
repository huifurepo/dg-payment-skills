#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path


APP_NAME = "hf-payment-local-sandbox"
SOURCE_ARCHIVE_SCHEMA_VERSION = "1.0"
ROOT_FILES = ("LICENSE", "README.md", "CHANGELOG.md", "LOCAL_SANDBOX_FINAL_PLAN.md")
SCRIPT_FILES = (
    "scripts/package_local_sandbox_release.py",
    "scripts/validate_local_sandbox_release.py",
    "scripts/generate_local_sandbox_release_evidence.py",
    "scripts/generate_local_sandbox_update_index.py",
    "scripts/package_local_sandbox_source_release.py",
    "scripts/validate_local_sandbox_source_release.py",
    "scripts/validate_local_sandbox_all.py",
    "scripts/validate_local_sandbox_samples.py",
    "scripts/validate_local_sandbox_sample_replay_contracts.py",
    "scripts/import_local_sandbox_samples.py",
)
FORBIDDEN_PARTS = {".git", ".claude", ".tmp", ".worktrees", ".codex-tasks", "__pycache__", "node_modules", "target", "dist", "build", "release-evidence", "sample-packs", ".venv", "venv"}
FORBIDDEN_NAMES = {".DS_Store", "Thumbs.db", APP_NAME}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".exe", ".dll", ".so", ".dylib", ".zip", ".tar", ".gz", ".tgz", ".7z"}
FORBIDDEN_NAME_SUFFIXES = ("_test.go",)


def main() -> int:
    parser = argparse.ArgumentParser(description="Package local-sandbox source release with an explicit whitelist.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"{APP_NAME}-source_{args.version}"
    archive_path = output_dir / f"{base_name}.tar.gz"
    source_manifest_path = output_dir / "source-manifest.json"
    prefix = f"{base_name}/"

    files = collect_source_files(repo_root)
    file_entries = []
    for rel in files:
        path = repo_root / rel
        file_entries.append({"path": rel.as_posix(), "sha256": sha256_file(path), "size_bytes": path.stat().st_size})

    inner_manifest = {
        "schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
        "name": APP_NAME,
        "version": args.version,
        "generated_at": now_utc(),
        "source_archive_schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
        "file_count": len(file_entries),
        "files": file_entries,
        "excluded_notice": "SDK golden vector script, Go test fixtures, and raw sample-packs are excluded because they contain synthetic private keys, secret-looking test values, or deidentified audit samples that must not enter public release archives. Derived sample fixtures remain in the contract bundle and are subject to source release sensitive-value scanning.",
    }

    with tarfile.open(archive_path, "w:gz") as tf:
        for rel in files:
            path = repo_root / rel
            info = tf.gettarinfo(str(path), arcname=prefix + rel.as_posix())
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            with path.open("rb") as fh:
                tf.addfile(info, fh)
        manifest_bytes = json.dumps(inner_manifest, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        info = tarfile.TarInfo(prefix + "SOURCE_RELEASE_MANIFEST.json")
        info.size = len(manifest_bytes)
        info.mtime = 0
        tf.addfile(info, fileobj=BytesReader(manifest_bytes))

    outer_manifest = {
        "schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
        "name": APP_NAME,
        "version": args.version,
        "generated_at": now_utc(),
        "source_archive_schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
        "source_archive": file_meta(archive_path),
        "file_count": len(file_entries),
        "forbidden_path_policy": {
            "forbidden_parts": sorted(FORBIDDEN_PARTS),
            "forbidden_names": sorted(FORBIDDEN_NAMES),
            "forbidden_name_suffixes": sorted(FORBIDDEN_NAME_SUFFIXES),
            "forbidden_suffixes": sorted(FORBIDDEN_SUFFIXES),
        },
    }
    write_json(source_manifest_path, outer_manifest)
    print(json.dumps({"ok": True, "archive": str(archive_path), "manifest": str(source_manifest_path), "files": len(file_entries)}, ensure_ascii=False))
    return 0


class BytesReader:
    def __init__(self, value: bytes):
        self.value = value
        self.offset = 0

    def read(self, size: int = -1) -> bytes:
        if size is None or size < 0:
            size = len(self.value) - self.offset
        chunk = self.value[self.offset:self.offset + size]
        self.offset += len(chunk)
        return chunk


def collect_source_files(repo_root: Path) -> list[Path]:
    files: set[Path] = set()
    for root_name in ROOT_FILES:
        path = repo_root / root_name
        if path.is_file():
            files.add(Path(root_name))
    for script in SCRIPT_FILES:
        path = repo_root / script
        if path.is_file():
            files.add(Path(script))
    for path in (repo_root / "local-sandbox").rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root)
        if is_forbidden(rel):
            continue
        files.add(rel)
    return sorted(files, key=lambda item: item.as_posix())


def is_forbidden(rel: Path) -> bool:
    parts = set(rel.parts)
    if parts & FORBIDDEN_PARTS:
        return True
    if rel.name in FORBIDDEN_NAMES:
        return True
    if rel.name.endswith(FORBIDDEN_NAME_SUFFIXES):
        return True
    if rel.suffix.lower() in FORBIDDEN_SUFFIXES:
        return True
    return False


def file_meta(path: Path) -> dict[str, object]:
    return {"name": path.name, "sha256": sha256_file(path), "size_bytes": path.stat().st_size}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
