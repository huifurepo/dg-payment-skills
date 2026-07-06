#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin


APP_NAME = "hf-payment-local-sandbox"
UPDATE_INDEX_SCHEMA_VERSION = "1.0"
DEFAULT_PUBLIC_BASE_URL = "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/"
DEFAULT_DOC_URL = "https://paas.huifu.com/docs/devtools/#/skillsv1_0"
DEFAULT_OUTPUT_NAME = "hf-payment-local-sandbox-latest.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate public local-sandbox update index JSON.")
    parser.add_argument("--manifest", required=True, help="Path to dist/release-manifest.json")
    parser.add_argument("--public-base-url", default=DEFAULT_PUBLIC_BASE_URL, help="Public URL prefix that contains the uploaded archives")
    parser.add_argument("--release-notes-url", default=DEFAULT_DOC_URL)
    parser.add_argument("--download-page-url", default=DEFAULT_DOC_URL)
    parser.add_argument("--download-mode", choices=("preview-package", "platform-archives"), default="preview-package")
    parser.add_argument("--preview-package", help="Path to hf-payment-local-sandbox-latest-preview.zip")
    parser.add_argument("--preview-package-name", default="hf-payment-local-sandbox-latest-preview.zip")
    parser.add_argument("--output", help=f"Output path. Defaults to manifest parent's ../{DEFAULT_OUTPUT_NAME}")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    manifest = read_json(manifest_path)
    output = Path(args.output).resolve() if args.output else manifest_path.parent.parent / DEFAULT_OUTPUT_NAME
    payload = update_index_payload(
        manifest=manifest,
        public_base_url=args.public_base_url,
        release_notes_url=args.release_notes_url,
        download_page_url=args.download_page_url,
        download_mode=args.download_mode,
        preview_package=Path(args.preview_package).resolve() if args.preview_package else default_preview_package(manifest_path),
        preview_package_name=args.preview_package_name,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_sha256 = sha256_file(output)
    output.with_suffix(output.suffix + ".sha256").write_text(f"{output_sha256}  {output.name}\n", encoding="utf-8")
    print(json.dumps({
        "ok": True,
        "output": str(output),
        "sha256": output_sha256,
        "version": payload["latest_version"],
        "downloads": len(payload["downloads"]),
    }, ensure_ascii=False))
    return 0


def update_index_payload(
    *,
    manifest: dict[str, object],
    public_base_url: str,
    release_notes_url: str,
    download_page_url: str,
    download_mode: str,
    preview_package: Path,
    preview_package_name: str,
) -> dict[str, object]:
    name = str(manifest.get("name") or "")
    if name != APP_NAME:
        raise SystemExit(f"manifest name must be {APP_NAME!r}, got {name!r}")
    version = str(manifest.get("release") or "")
    if not version:
        raise SystemExit("manifest release is missing")
    targets = manifest.get("targets")
    if not isinstance(targets, list) or not targets:
        raise SystemExit("manifest targets are missing")
    downloads: dict[str, dict[str, object]] = {}
    preview_meta = preview_package_meta(preview_package, preview_package_name, public_base_url)
    for target in targets:
        if not isinstance(target, dict):
            continue
        goos = str(target.get("goos") or "")
        goarch = str(target.get("goarch") or "")
        archive = target.get("archive")
        if not goos or not goarch or not isinstance(archive, dict):
            raise SystemExit("target is missing goos/goarch/archive")
        archive_name = str(archive.get("name") or "")
        if not archive_name:
            raise SystemExit(f"{goos}/{goarch} archive name is missing")
        if download_mode == "platform-archives":
            downloads[f"{goos}_{goarch}"] = {
                "name": archive_name,
                "url": urljoin(ensure_slash(public_base_url), archive_name),
                "sha256": str(archive.get("sha256") or ""),
                "size_bytes": int(archive.get("size_bytes") or 0),
            }
        else:
            item = dict(preview_meta)
            item["platform_archive_name"] = archive_name
            item["platform_archive_sha256"] = str(archive.get("sha256") or "")
            item["platform_archive_size_bytes"] = int(archive.get("size_bytes") or 0)
            downloads[f"{goos}_{goarch}"] = item
    return {
        "schema_version": UPDATE_INDEX_SCHEMA_VERSION,
        "name": APP_NAME,
        "channel": str(manifest.get("release_channel") or "preview"),
        "latest_version": version,
        "version": version,
        "published_at": now_utc(),
        "generated_from": "release-manifest.json",
        "contract_bundle": str(manifest.get("contract_bundle") or ""),
        "source_skill_version": str(manifest.get("source_skill_version") or ""),
        "release_notes_url": release_notes_url,
        "download_page_url": download_page_url,
        "download_mode": download_mode,
        "preview_package": preview_meta,
        "code_signed": bool(manifest.get("code_signed")),
        "notarized": bool(manifest.get("notarized")),
        "downloads": downloads,
    }


def default_preview_package(manifest_path: Path) -> Path:
    return manifest_path.parent.parent / DEFAULT_OUTPUT_NAME.replace(".json", "-preview.zip")


def preview_package_meta(path: Path, public_name: str, public_base_url: str) -> dict[str, object]:
    meta: dict[str, object] = {
        "name": public_name,
        "url": urljoin(ensure_slash(public_base_url), public_name),
        "sha256": "",
        "size_bytes": 0,
    }
    if path.is_file():
        meta["sha256"] = sha256_file(path)
        meta["size_bytes"] = path.stat().st_size
    return meta


def sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_slash(value: str) -> str:
    return value if value.endswith("/") else value + "/"


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
