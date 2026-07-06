#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


APP_NAME = "hf-payment-local-sandbox"
SIGNING_PROFILE = "sdk-v2-sorted-json"
GOLDEN_VECTOR_VERSION = "1.0"
RELEASE_EVIDENCE_SCHEMA_VERSION = "1.0"
SOURCE_ARCHIVE_SCHEMA_VERSION = "1.0"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local-sandbox release evidence templates.")
    parser.add_argument("--dist", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--contract-bundle", required=True)
    parser.add_argument("--golden-vectors-json", default="")
    parser.add_argument("--internal-validation-json", default="")
    parser.add_argument("--artifact-smoke-json", default="")
    parser.add_argument("--source-validation-json", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    dist = Path(args.dist).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    golden = read_or_run_json(
        Path(args.golden_vectors_json) if args.golden_vectors_json else None,
        [sys.executable, str(repo_root / "scripts" / "validate_local_sandbox_golden_vectors.py"), "--strict"],
        cwd=repo_root,
    )
    internal = read_or_run_json(
        Path(args.internal_validation_json) if args.internal_validation_json else None,
        [
            sys.executable,
            str(repo_root / "scripts" / "validate_local_sandbox_release.py"),
            "--dist",
            str(dist),
            "--version",
            args.version,
            "--contract-bundle",
            args.contract_bundle,
            "--mode",
            "internal",
        ],
        cwd=repo_root,
    )
    artifact_smoke = read_json(Path(args.artifact_smoke_json)) if args.artifact_smoke_json else None
    source_validation = read_json(Path(args.source_validation_json)) if args.source_validation_json else None

    files = {
        "golden-vectors.json": golden_vector_evidence(args.version, args.contract_bundle, golden),
        "internal-validation.json": internal_validation_evidence(args.version, args.contract_bundle, internal),
        "artifact-smoke.json": artifact_smoke_evidence(args.version, args.contract_bundle, artifact_smoke),
        "source-archive.json": source_archive_evidence(args.version, args.contract_bundle, source_validation),
        "license-approval.json": approval_template(args.version, args.contract_bundle, "license-approval", "Public redistribution license approval"),
        "trademark-approval.json": approval_template(args.version, args.contract_bundle, "trademark-approval", "Trademark and product naming approval"),
        "content-authorization.json": approval_template(args.version, args.contract_bundle, "content-authorization", "Protocol material, fixture, and documentation authorization"),
        "windows-authenticode.json": signing_template(args.version, args.contract_bundle, "windows-authenticode", "Windows Authenticode signing and timestamp"),
        "macos-notarization.json": signing_template(args.version, args.contract_bundle, "macos-notarization", "macOS Developer ID signing and notarization"),
        "linux-archive-signature.json": signing_template(args.version, args.contract_bundle, "linux-archive-signature", "Linux archive signature"),
        "public-download.json": public_download_template(args.version, args.contract_bundle),
    }
    for filename, payload in files.items():
        write_json(output_dir / filename, payload)

    manifest = {
        "ok": True,
        "evidence_dir": str(output_dir),
        "schema_version": RELEASE_EVIDENCE_SCHEMA_VERSION,
        "files": {name: file_meta(output_dir / name) for name in sorted(files)},
    }
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


def base_evidence(version: str, contract_bundle: str, evidence_type: str, status: str) -> dict[str, object]:
    return {
        "schema_version": RELEASE_EVIDENCE_SCHEMA_VERSION,
        "evidence_type": evidence_type,
        "name": APP_NAME,
        "version": version,
        "contract_bundle": contract_bundle,
        "status": status,
        "generated_at": now_utc(),
    }


def golden_vector_evidence(version: str, contract_bundle: str, raw: dict[str, object]) -> dict[str, object]:
    status = "passed" if raw.get("ok") is True else "blocked"
    payload = base_evidence(version, contract_bundle, "golden-vectors", status)
    payload.update(
        {
            "signing_profile": raw.get("signing_profile", SIGNING_PROFILE),
            "golden_vector_version": raw.get("golden_vector_version", GOLDEN_VECTOR_VERSION),
            "synthetic_public_key_sha256": raw.get("synthetic_public_key_sha256", ""),
            "vectors": raw.get("vectors", []),
            "source_output_sha256": sha256_text(json.dumps(raw, ensure_ascii=False, sort_keys=True)),
        }
    )
    return payload


def internal_validation_evidence(version: str, contract_bundle: str, raw: dict[str, object]) -> dict[str, object]:
    status = "passed" if raw.get("ok") is True and internal_release_step_passed(raw) else "blocked"
    payload = base_evidence(version, contract_bundle, "internal-validation", status)
    payload.update({"validation_result": raw, "source_output_sha256": sha256_text(json.dumps(raw, ensure_ascii=False, sort_keys=True))})
    return payload


def internal_release_step_passed(raw: dict[str, object]) -> bool:
    if raw.get("mode") == "internal":
        return True
    steps = raw.get("steps")
    if not isinstance(steps, list):
        return False
    for step in steps:
        if not isinstance(step, dict):
            continue
        if step.get("name") == "validate-release-internal" and step.get("returncode") == 0:
            return True
    return False


def artifact_smoke_evidence(version: str, contract_bundle: str, raw: dict[str, object] | None) -> dict[str, object]:
    if raw is None:
        payload = base_evidence(version, contract_bundle, "artifact-smoke", "blocked")
        payload.update({"reason": "artifact smoke output was not provided", "smoke_results": []})
        return payload
    status = "passed" if raw.get("ok") is True or raw.get("status") == "passed" else "blocked"
    smoke_results = normalize_artifact_smoke_results(version, status, raw)
    payload = base_evidence(version, contract_bundle, "artifact-smoke", status)
    payload.update({"smoke_results": smoke_results, "source_output_sha256": sha256_text(json.dumps(raw, ensure_ascii=False, sort_keys=True))})
    return payload


def normalize_artifact_smoke_results(version: str, status: str, raw: dict[str, object]) -> list[dict[str, object]]:
    raw_results = raw.get("smoke_results")
    if isinstance(raw_results, list) and all(isinstance(item, dict) and item.get("target") for item in raw_results):
        return [
            {
                **item,
                "status": item.get("status", "passed" if status == "passed" else "blocked"),
                "version": item.get("version", raw.get("version", version)),
            }
            for item in raw_results
            if isinstance(item, dict)
        ]
    result: dict[str, object] = {
        "target": raw.get("target", "host"),
        "status": "passed" if status == "passed" else "blocked",
        "version": raw.get("version", version),
        "report_dir": raw.get("report_dir", ""),
    }
    if isinstance(raw_results, list):
        result["checks"] = raw_results
    return [result]


def source_archive_evidence(version: str, contract_bundle: str, raw: dict[str, object] | None) -> dict[str, object]:
    if raw is None:
        payload = base_evidence(version, contract_bundle, "source-archive", "blocked")
        payload.update(
            {
                "source_archive_schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
                "reason": "source archive validation output was not provided",
                "source_archive": {},
                "forbidden_path_count": None,
                "secret_scan_status": "not_evaluated",
                "manifest_status": "not_evaluated",
            }
        )
        return payload
    status = "passed" if raw.get("ok") is True else "blocked"
    payload = base_evidence(version, contract_bundle, "source-archive", status)
    payload.update(
        {
            "source_archive_schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
            "source_archive": {"name": Path(str(raw.get("archive", ""))).name, "sha256": "", "size_bytes": 0},
            "forbidden_path_count": raw.get("forbidden_path_count"),
            "secret_scan_status": raw.get("secret_scan_status", "not_evaluated"),
            "manifest_status": raw.get("manifest_status", "not_evaluated"),
            "validation_result": raw,
            "source_output_sha256": sha256_text(json.dumps(raw, ensure_ascii=False, sort_keys=True)),
        }
    )
    manifest_path = raw.get("manifest")
    if isinstance(manifest_path, str) and manifest_path:
        try:
            manifest = read_json(Path(manifest_path))
            source_archive = manifest.get("source_archive")
            if isinstance(source_archive, dict):
                payload["source_archive"] = source_archive
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            pass
    return payload


def approval_template(version: str, contract_bundle: str, evidence_type: str, title: str) -> dict[str, object]:
    payload = base_evidence(version, contract_bundle, evidence_type, "blocked")
    payload.update(
        {
            "title": title,
            "issuer": "",
            "approved_at": "",
            "subject": APP_NAME,
            "scope": "",
            "evidence_reference": "",
            "reason": "external legal or business approval evidence has not been supplied",
        }
    )
    return payload


def signing_template(version: str, contract_bundle: str, evidence_type: str, title: str) -> dict[str, object]:
    payload = base_evidence(version, contract_bundle, evidence_type, "blocked")
    payload.update(
        {
            "title": title,
            "issuer": "",
            "signed_at": "",
            "subject_sha256": "",
            "verification_command": "",
            "reason": "real signing or notarization evidence has not been supplied",
        }
    )
    if evidence_type == "windows-authenticode":
        payload["timestamped"] = False
    if evidence_type == "macos-notarization":
        payload["notarized_at"] = ""
        payload["stapled"] = False
    if evidence_type == "linux-archive-signature":
        payload["signature_format"] = ""
    return payload


def public_download_template(version: str, contract_bundle: str) -> dict[str, object]:
    payload = base_evidence(version, contract_bundle, "public-download", "blocked")
    payload.update(
        {
            "issuer": "",
            "approved_at": "",
            "immutable_urls": [],
            "reason": "official immutable public download URLs have not been supplied",
        }
    )
    return payload


def read_or_run_json(path: Path | None, cmd: list[str], cwd: Path) -> dict[str, object]:
    if path is not None:
        return read_json(path)
    try:
        raw = subprocess.check_output(cmd, cwd=cwd, text=True, stderr=subprocess.STDOUT, encoding="utf-8")
        return parse_json_from_output(raw)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return {"ok": False, "error": str(exc)}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(read_text_auto(path))


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8")


def parse_json_from_output(raw: str) -> dict[str, object]:
    for line in reversed(raw.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        return json.loads(line)
    return {"ok": False, "error": "no JSON object found in command output"}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_meta(path: Path) -> dict[str, object]:
    return {"name": path.name, "sha256": sha256_file(path), "size_bytes": path.stat().st_size}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
