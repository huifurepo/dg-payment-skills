#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from urllib.parse import urljoin


APP_NAME = "hf-payment-local-sandbox"
DEFAULT_PUBLIC_BASE_URL = "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local-sandbox preview wrapper bundle and public update index.")
    parser.add_argument("--release-dir", required=True, help="Path like release-preview/1.0.0")
    parser.add_argument("--version", required=True)
    parser.add_argument("--public-base-url", default=DEFAULT_PUBLIC_BASE_URL)
    parser.add_argument("--skill-version", default="1.3.1")
    args = parser.parse_args()

    release_dir = Path(args.release_dir).resolve()
    dist_dir = release_dir / "dist"
    require(dist_dir.is_dir(), "dist directory is missing")
    manifest_path = dist_dir / "release-manifest.json"
    require(manifest_path.is_file(), "dist/release-manifest.json is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("release") == args.version, "manifest release mismatch")
    require(manifest.get("release_channel") == "preview", "manifest release_channel must be preview")
    require(manifest.get("build_dirty") is False, "preview artifacts must be built from a clean git worktree")

    versioned_zip = release_dir / f"{APP_NAME}-{args.version}-preview.zip"
    latest_zip = release_dir / f"{APP_NAME}-latest-preview.zip"
    update_index = release_dir / f"{APP_NAME}-latest.json"

    versioned_sha = validate_file_sha(versioned_zip)
    latest_sha = validate_file_sha(latest_zip)
    require(versioned_sha == latest_sha, "versioned preview zip and latest preview zip sha256 mismatch")
    update_index_sha = validate_file_sha(update_index)

    validate_sha_file(versioned_zip, versioned_sha)
    validate_sha_file(latest_zip, latest_sha)
    validate_sha_file(update_index, update_index_sha)
    validate_zip(versioned_zip, release_dir, dist_dir)
    validate_zip(latest_zip, release_dir, dist_dir)
    validate_update_index(update_index, args.version, args.skill_version, latest_zip, latest_sha, args.public_base_url, manifest)

    print(json.dumps({
        "ok": True,
        "release_dir": str(release_dir),
        "version": args.version,
        "latest_preview_zip_sha256": latest_sha,
        "latest_json_sha256": update_index_sha,
    }, ensure_ascii=False))
    return 0


def validate_file_sha(path: Path) -> str:
    require(path.is_file(), f"{path.name} is missing")
    require(path.stat().st_size > 0, f"{path.name} is empty")
    return sha256_file(path)


def validate_sha_file(path: Path, expected_sha: str) -> None:
    sha_path = path.with_suffix(path.suffix + ".sha256")
    require(sha_path.is_file(), f"{sha_path.name} is missing")
    parts = sha_path.read_text(encoding="utf-8").strip().split()
    require(len(parts) >= 2, f"{sha_path.name} must contain '<sha256>  <filename>'")
    require(parts[0] == expected_sha, f"{sha_path.name} sha256 mismatch")
    require(parts[1] == path.name, f"{sha_path.name} filename mismatch")


def validate_zip(path: Path, release_dir: Path, dist_dir: Path) -> None:
    root_docs = ["README.md", "USAGE.md"]
    for name in root_docs:
        doc = release_dir / name
        require(doc.is_file(), f"{name} is missing")
        require(doc.stat().st_size > 0, f"{name} is empty")
    expected = sorted([*root_docs, *(f"dist/{p.name}" for p in dist_dir.iterdir() if p.is_file())])
    require(len(expected) > len(root_docs), "dist directory has no files")
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        require(not bad, f"{path.name} has bad zip member {bad}")
        actual = sorted(name for name in zf.namelist() if not name.endswith("/"))
    require(actual == expected, f"{path.name} file set mismatch")
    required = {"README.md", "USAGE.md", "dist/release-manifest.json", "dist/release-readiness.json", "dist/SHA256SUMS.txt"}
    require(required.issubset(set(actual)), f"{path.name} missing required dist files")


def validate_update_index(path: Path, version: str, skill_version: str, latest_zip: Path, latest_sha: str, public_base_url: str, manifest: dict[str, object]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "1.0", "update index schema_version mismatch")
    require(data.get("name") == APP_NAME, "update index name mismatch")
    require(data.get("channel") == "preview", "update index channel mismatch")
    require(data.get("latest_version") == version, "update index latest_version mismatch")
    require(data.get("version") == version, "update index version mismatch")
    require(data.get("source_skill_version") == skill_version, "update index source_skill_version mismatch")
    require(data.get("download_mode") == "preview-package", "update index download_mode mismatch")

    expected_url = urljoin(ensure_slash(public_base_url), latest_zip.name)
    expected_size = latest_zip.stat().st_size
    preview_package = data.get("preview_package")
    require(isinstance(preview_package, dict), "update index preview_package missing")
    validate_download_meta(preview_package, latest_zip.name, expected_url, latest_sha, expected_size, "preview_package")

    downloads = data.get("downloads")
    require(isinstance(downloads, dict) and downloads, "update index downloads missing")
    expected_platforms = manifest_platform_archives(manifest, path.parent / "dist")
    require(set(downloads) == set(expected_platforms), "update index platform download set mismatch")
    for key, item in downloads.items():
        require(isinstance(item, dict), f"download {key} must be object")
        validate_download_meta(item, latest_zip.name, expected_url, latest_sha, expected_size, f"download {key}")
        expected_archive = expected_platforms[key]
        require(item.get("platform_archive_name") == expected_archive["name"], f"download {key} platform_archive_name mismatch")
        require(item.get("platform_archive_sha256") == expected_archive["sha256"], f"download {key} platform_archive_sha256 mismatch")
        require(item.get("platform_archive_size_bytes") == expected_archive["size_bytes"], f"download {key} platform_archive_size_bytes mismatch")


def validate_download_meta(item: dict[str, object], name: str, url: str, sha256: str, size: int, label: str) -> None:
    require(item.get("name") == name, f"{label} name mismatch")
    require(item.get("url") == url, f"{label} url mismatch")
    require(item.get("sha256") == sha256, f"{label} sha256 mismatch")
    require(item.get("size_bytes") == size, f"{label} size_bytes mismatch")


def manifest_platform_archives(manifest: dict[str, object], dist_dir: Path) -> dict[str, dict[str, object]]:
    targets = manifest.get("targets")
    require(isinstance(targets, list) and targets, "manifest targets missing")
    archives: dict[str, dict[str, object]] = {}
    for target in targets:
        require(isinstance(target, dict), "manifest target must be object")
        goos = target.get("goos")
        goarch = target.get("goarch")
        archive = target.get("archive")
        require(is_nonempty_string(goos), "manifest target goos missing")
        require(is_nonempty_string(goarch), "manifest target goarch missing")
        require(isinstance(archive, dict), f"manifest target {goos}_{goarch} archive missing")
        key = f"{goos}_{goarch}"
        require(key not in archives, f"duplicate manifest target {key}")
        name = archive.get("name")
        sha256 = archive.get("sha256")
        size = archive.get("size_bytes")
        require(is_nonempty_string(name), f"manifest target {key} archive name missing")
        require(is_hex_sha256(sha256), f"manifest target {key} archive sha256 invalid")
        require(isinstance(size, int) and size > 0, f"manifest target {key} archive size invalid")
        archive_path = dist_dir / str(name)
        require(archive_path.is_file(), f"manifest target {key} archive file missing")
        require(sha256_file(archive_path) == sha256, f"manifest target {key} archive sha256 does not match file")
        require(archive_path.stat().st_size == size, f"manifest target {key} archive size does not match file")
        archives[key] = {"name": name, "sha256": sha256, "size_bytes": size}
    return archives


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_slash(value: str) -> str:
    return value if value.endswith("/") else value + "/"


def is_hex_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def require(condition: object, message: str) -> None:
    if not condition:
        raise SystemExit(message)


if __name__ == "__main__":
    raise SystemExit(main())
