#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
import zipfile
from pathlib import Path


APP_NAME = "hf-payment-local-sandbox"
SIGNING_PROFILE = "sdk-v2-sorted-json"
GOLDEN_VECTOR_VERSION = "1.0"
RELEASE_EVIDENCE_SCHEMA_VERSION = "1.0"
SOURCE_ARCHIVE_SCHEMA_VERSION = "1.0"
COVERAGE_RUNNER_VERSION = "1.0"
REFERENCE_DIGEST_SCHEMA_VERSION = "1.0"
FIXTURE_RUNNER_VERSION = "1.0"
OPS_CLI_SCHEMA_VERSION = "1.0"
SAMPLE_SCHEMA_VERSION = "1.0"
SAMPLE_IMPORTER_VERSION = "1.0"
REQUIRED_RELEASE_EVIDENCE = {
    "golden-vectors": "golden-vectors.json",
    "internal-validation": "internal-validation.json",
    "artifact-smoke": "artifact-smoke.json",
    "source-archive": "source-archive.json",
    "license-approval": "license-approval.json",
    "trademark-approval": "trademark-approval.json",
    "content-authorization": "content-authorization.json",
    "windows-authenticode": "windows-authenticode.json",
    "macos-notarization": "macos-notarization.json",
    "linux-archive-signature": "linux-archive-signature.json",
    "public-download": "public-download.json",
}
TEXT_ALLOWED = {"build-info.json", "README.txt", "USAGE.md", "LICENSE", "THIRD_PARTY_NOTICES.txt"}
LAUNCHERS_BY_GOOS = {
    "windows": {"start-local-sandbox.cmd"},
    "linux": {"start-local-sandbox.sh"},
    "darwin": {"start-local-sandbox.command", "start-local-sandbox.sh"},
}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"HUIFU_SANDBOX_[A-Z_]*PRIVATE"),
    re.compile(rb"merchant_private_pem"),
    re.compile(rb"gateway_private"),
    re.compile(rb"[?&](" + b"|".join([rb"secret", rb"token", rb"key", rb"password"]) + rb")="),
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local-sandbox release candidate artifacts.")
    parser.add_argument("--dist", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--contract-bundle", required=True)
    parser.add_argument("--mode", choices=("internal", "public"), default="internal")
    parser.add_argument("--evidence-dir", default="")
    args = parser.parse_args()

    dist = Path(args.dist).resolve()
    evidence_dir = Path(args.evidence_dir).resolve() if args.evidence_dir else dist / "release-evidence"
    manifest_path = dist / "release-manifest.json"
    sha_path = dist / "SHA256SUMS.txt"
    if not manifest_path.is_file():
        fail("release-manifest.json is missing")
    if not sha_path.is_file():
        fail("SHA256SUMS.txt is missing")

    manifest = read_json(manifest_path)
    require(manifest.get("release") == args.version, "manifest release mismatch")
    require(manifest.get("contract_bundle") == args.contract_bundle, "manifest contract_bundle mismatch")
    require(manifest.get("signing_profile") == SIGNING_PROFILE, "manifest signing_profile mismatch")
    require(manifest.get("golden_vector_version") == GOLDEN_VECTOR_VERSION, "manifest golden_vector_version mismatch")
    require(manifest.get("release_evidence_schema_version") == RELEASE_EVIDENCE_SCHEMA_VERSION, "manifest release_evidence_schema_version mismatch")
    require(manifest.get("source_archive_schema_version") == SOURCE_ARCHIVE_SCHEMA_VERSION, "manifest source_archive_schema_version mismatch")
    require(manifest.get("coverage_runner_version") == COVERAGE_RUNNER_VERSION, "manifest coverage_runner_version mismatch")
    require(manifest.get("reference_digest_schema_version") == REFERENCE_DIGEST_SCHEMA_VERSION, "manifest reference_digest_schema_version mismatch")
    require(manifest.get("fixture_runner_version") == FIXTURE_RUNNER_VERSION, "manifest fixture_runner_version mismatch")
    require(manifest.get("ops_cli_schema_version") == OPS_CLI_SCHEMA_VERSION, "manifest ops_cli_schema_version mismatch")
    require(manifest.get("sample_schema_version") == SAMPLE_SCHEMA_VERSION, "manifest sample_schema_version mismatch")
    require(manifest.get("sample_importer_version") == SAMPLE_IMPORTER_VERSION, "manifest sample_importer_version mismatch")
    require(isinstance(manifest.get("code_signed"), bool), "manifest code_signed must be boolean")
    require(isinstance(manifest.get("notarized"), bool), "manifest notarized must be boolean")
    if args.mode == "internal":
        require(manifest.get("code_signed") is False, "internal dry-run must be unsigned")
        require(manifest.get("notarized") is False, "internal dry-run must not be notarized")
    targets = manifest.get("targets")
    require(isinstance(targets, list) and targets, "manifest targets missing")

    sha_entries = read_sha256sums(sha_path)
    expected_sha_files = {path.name for path in dist.iterdir() if path.is_file() and path.name != "SHA256SUMS.txt"}
    require(set(sha_entries) == expected_sha_files, "SHA256SUMS.txt file set mismatch")
    for name in sorted(expected_sha_files):
        require(sha_entries[name] == sha256_file(dist / name), f"SHA256SUMS mismatch for {name}")

    seen_files = {"release-manifest.json"}
    readiness_path = validate_standalone_file_meta(dist, manifest.get("release_readiness"), "release_readiness")
    seen_files.add(readiness_path.name)
    readiness = validate_readiness(readiness_path, args.version, args.contract_bundle)
    for target in targets:
        goos = expect_string(target, "goos")
        goarch = expect_string(target, "goarch")
        binary_name = expect_string(target, "binary_name")
        archive = validate_file_meta(dist, target, "archive")
        sbom = validate_file_meta(dist, target, "sbom")
        provenance = validate_file_meta(dist, target, "provenance")
        seen_files.update({archive.name, sbom.name, provenance.name})
        validate_archive(archive, binary_name, args.version, args.contract_bundle, manifest.get("release_channel"), goos, goarch, args.mode)
        validate_sbom(sbom)
        validate_provenance(provenance, args.version, args.contract_bundle, goos, goarch, archive.name, args.mode)

    require(seen_files.issubset(expected_sha_files), "manifest references files not present in SHA256SUMS")
    for file_path in dist.iterdir():
        if file_path.is_file():
            scan_file_for_secrets(file_path)

    if args.mode == "public":
        validate_public_gate(dist, evidence_dir, manifest, readiness)

    print(json.dumps({"ok": True, "mode": args.mode, "dist": str(dist), "evidence_dir": str(evidence_dir), "targets": len(targets)}, ensure_ascii=False))
    return 0


def validate_standalone_file_meta(dist: Path, meta: object, label: str) -> Path:
    require(isinstance(meta, dict), f"{label} metadata missing")
    name = expect_string(meta, "name")
    path = dist / name
    require(path.is_file(), f"{name} is missing")
    require(meta.get("sha256") == sha256_file(path), f"{name} sha256 mismatch")
    require(meta.get("size_bytes") == path.stat().st_size, f"{name} size mismatch")
    require(path.stat().st_size > 0, f"{name} is empty")
    return path


def validate_file_meta(dist: Path, target: dict[str, object], key: str) -> Path:
    meta = target.get(key)
    require(isinstance(meta, dict), f"{key} metadata missing")
    name = expect_string(meta, "name")
    path = dist / name
    require(path.is_file(), f"{name} is missing")
    require(meta.get("sha256") == sha256_file(path), f"{name} sha256 mismatch")
    require(meta.get("size_bytes") == path.stat().st_size, f"{name} size mismatch")
    require(path.stat().st_size > 0, f"{name} is empty")
    return path


def validate_archive(path: Path, binary_name: str, version: str, contract_bundle: str, release_channel: object, goos: str, goarch: str, mode: str) -> None:
    members = read_archive_members(path)
    names = set(members)
    allowed = set(TEXT_ALLOWED)
    allowed.add(binary_name)
    launcher_names = LAUNCHERS_BY_GOOS.get(goos, set())
    allowed.update(launcher_names)
    require(names == allowed, f"{path.name} archive members mismatch: {sorted(names)}")
    require("release-manifest.json" not in names, f"{path.name} must not contain release-manifest.json")
    for name in names:
        require("/" not in name and "\\" not in name, f"{path.name} contains nested member {name}")
        require(not name.startswith("."), f"{path.name} contains hidden member {name}")

    build_info = json.loads(members["build-info.json"].decode("utf-8"))
    require(build_info.get("name") == APP_NAME, f"{path.name} build-info name mismatch")
    require(build_info.get("version") == version, f"{path.name} build-info version mismatch")
    require(build_info.get("contract_bundle") == contract_bundle, f"{path.name} build-info contract mismatch")
    require(build_info.get("signing_profile") == SIGNING_PROFILE, f"{path.name} build-info signing_profile mismatch")
    require(build_info.get("golden_vector_version") == GOLDEN_VECTOR_VERSION, f"{path.name} build-info golden_vector_version mismatch")
    require(build_info.get("release_evidence_schema_version") == RELEASE_EVIDENCE_SCHEMA_VERSION, f"{path.name} build-info release_evidence_schema_version mismatch")
    require(build_info.get("source_archive_schema_version") == SOURCE_ARCHIVE_SCHEMA_VERSION, f"{path.name} build-info source_archive_schema_version mismatch")
    require(build_info.get("coverage_runner_version") == COVERAGE_RUNNER_VERSION, f"{path.name} build-info coverage_runner_version mismatch")
    require(build_info.get("reference_digest_schema_version") == REFERENCE_DIGEST_SCHEMA_VERSION, f"{path.name} build-info reference_digest_schema_version mismatch")
    require(build_info.get("fixture_runner_version") == FIXTURE_RUNNER_VERSION, f"{path.name} build-info fixture_runner_version mismatch")
    require(build_info.get("ops_cli_schema_version") == OPS_CLI_SCHEMA_VERSION, f"{path.name} build-info ops_cli_schema_version mismatch")
    require(build_info.get("sample_schema_version") == SAMPLE_SCHEMA_VERSION, f"{path.name} build-info sample_schema_version mismatch")
    require(build_info.get("sample_importer_version") == SAMPLE_IMPORTER_VERSION, f"{path.name} build-info sample_importer_version mismatch")
    require(build_info.get("release_channel") == release_channel, f"{path.name} build-info release_channel mismatch")
    require(build_info.get("goos") == goos and build_info.get("goarch") == goarch, f"{path.name} build-info target mismatch")
    require(build_info.get("build_commit"), f"{path.name} build-info missing build_commit")
    require(build_info.get("build_time"), f"{path.name} build-info missing build_time")
    require(isinstance(build_info.get("build_dirty"), bool), f"{path.name} build-info build_dirty must be boolean")
    require(isinstance(build_info.get("code_signed"), bool), f"{path.name} build-info code_signed must be boolean")
    require(isinstance(build_info.get("notarized"), bool), f"{path.name} build-info notarized must be boolean")
    if mode == "internal":
        require(build_info.get("code_signed") is False, f"{path.name} build-info code_signed must be false")
        require(build_info.get("notarized") is False, f"{path.name} build-info notarized must be false")
    require(len(members[binary_name]) > 0, f"{path.name} binary is empty")
    for text_name in TEXT_ALLOWED | launcher_names:
        scan_bytes_for_secrets(path.name + ":" + text_name, members[text_name])


def validate_sbom(path: Path) -> None:
    data = read_json(path)
    require(data.get("spdxVersion") == "SPDX-2.3", f"{path.name} SPDX version mismatch")
    require(isinstance(data.get("packages"), list) and data["packages"], f"{path.name} packages missing")


def validate_provenance(path: Path, version: str, contract_bundle: str, goos: str, goarch: str, archive_name: str, mode: str) -> None:
    data = read_json(path)
    require(data.get("version") == version, f"{path.name} version mismatch")
    require(data.get("contract_bundle") == contract_bundle, f"{path.name} contract_bundle mismatch")
    require(data.get("signing_profile") == SIGNING_PROFILE, f"{path.name} signing_profile mismatch")
    require(data.get("golden_vector_version") == GOLDEN_VECTOR_VERSION, f"{path.name} golden_vector_version mismatch")
    require(data.get("release_evidence_schema_version") == RELEASE_EVIDENCE_SCHEMA_VERSION, f"{path.name} release_evidence_schema_version mismatch")
    require(data.get("source_archive_schema_version") == SOURCE_ARCHIVE_SCHEMA_VERSION, f"{path.name} source_archive_schema_version mismatch")
    require(data.get("coverage_runner_version") == COVERAGE_RUNNER_VERSION, f"{path.name} coverage_runner_version mismatch")
    require(data.get("reference_digest_schema_version") == REFERENCE_DIGEST_SCHEMA_VERSION, f"{path.name} reference_digest_schema_version mismatch")
    require(data.get("fixture_runner_version") == FIXTURE_RUNNER_VERSION, f"{path.name} fixture_runner_version mismatch")
    require(data.get("ops_cli_schema_version") == OPS_CLI_SCHEMA_VERSION, f"{path.name} ops_cli_schema_version mismatch")
    require(data.get("sample_schema_version") == SAMPLE_SCHEMA_VERSION, f"{path.name} sample_schema_version mismatch")
    require(data.get("sample_importer_version") == SAMPLE_IMPORTER_VERSION, f"{path.name} sample_importer_version mismatch")
    require(data.get("goos") == goos and data.get("goarch") == goarch, f"{path.name} target mismatch")
    require(data.get("archive_name") == archive_name, f"{path.name} archive_name mismatch")
    require(isinstance(data.get("code_signed"), bool), f"{path.name} code_signed must be boolean")
    if mode == "internal":
        require(data.get("code_signed") is False, f"{path.name} code_signed must be false")


def validate_readiness(path: Path, version: str, contract_bundle: str) -> dict[str, object]:
    data = read_json(path)
    require(data.get("name") == APP_NAME, "release-readiness name mismatch")
    require(data.get("version") == version, "release-readiness version mismatch")
    require(data.get("contract_bundle") == contract_bundle, "release-readiness contract_bundle mismatch")
    require(data.get("signing_profile") == SIGNING_PROFILE, "release-readiness signing_profile mismatch")
    require(data.get("golden_vector_version") == GOLDEN_VECTOR_VERSION, "release-readiness golden_vector_version mismatch")
    require(data.get("release_evidence_schema_version") == RELEASE_EVIDENCE_SCHEMA_VERSION, "release-readiness release_evidence_schema_version mismatch")
    require(data.get("source_archive_schema_version") == SOURCE_ARCHIVE_SCHEMA_VERSION, "release-readiness source_archive_schema_version mismatch")
    require(data.get("coverage_runner_version") == COVERAGE_RUNNER_VERSION, "release-readiness coverage_runner_version mismatch")
    require(data.get("reference_digest_schema_version") == REFERENCE_DIGEST_SCHEMA_VERSION, "release-readiness reference_digest_schema_version mismatch")
    require(data.get("fixture_runner_version") == FIXTURE_RUNNER_VERSION, "release-readiness fixture_runner_version mismatch")
    require(data.get("ops_cli_schema_version") == OPS_CLI_SCHEMA_VERSION, "release-readiness ops_cli_schema_version mismatch")
    require(data.get("sample_schema_version") == SAMPLE_SCHEMA_VERSION, "release-readiness sample_schema_version mismatch")
    require(data.get("sample_importer_version") == SAMPLE_IMPORTER_VERSION, "release-readiness sample_importer_version mismatch")
    require(data.get("golden_vectors_required") is True, "release-readiness must require golden vectors")
    require(set(data.get("required_evidence_files", [])) == set(REQUIRED_RELEASE_EVIDENCE.values()), "release-readiness required_evidence_files mismatch")
    require(data.get("public_release_allowed") is False, "internal release-readiness must block public release")
    blockers = data.get("blockers")
    require(isinstance(blockers, list) and blockers, "release-readiness blockers missing")
    return data


def validate_public_gate(dist: Path, evidence_dir: Path, manifest: dict[str, object], readiness: dict[str, object]) -> None:
    blockers = [blocker for blocker in readiness.get("blockers", []) if not required_evidence_present(evidence_dir, blocker)]
    blockers.extend(validate_release_evidence(evidence_dir, manifest))
    if manifest.get("code_signed") is not True:
        blockers.append({"id": "MANIFEST_CODE_SIGNED_FALSE", "severity": "P0", "category": "signing", "message": "Manifest code_signed is not true."})
    if manifest.get("notarized") is not True:
        blockers.append({"id": "MANIFEST_NOTARIZED_FALSE", "severity": "P0", "category": "signing", "message": "Manifest notarized is not true."})
    if readiness.get("public_release_allowed") is not True:
        blockers.append({"id": "READINESS_PUBLIC_RELEASE_BLOCKED", "severity": "P0", "category": "readiness", "message": "release-readiness.json does not allow public release."})
    for target in manifest.get("targets", []):
        if not isinstance(target, dict):
            continue
        target_name = f"{target.get('goos', 'unknown')}/{target.get('goarch', 'unknown')}"
        if target.get("code_signed") is not True:
            blockers.append({"id": "TARGET_CODE_SIGNED_FALSE", "severity": "P0", "category": "signing", "message": f"{target_name} code_signed is not true."})
        if target.get("goos") == "darwin" and target.get("notarized") is not True:
            blockers.append({"id": "TARGET_NOTARIZED_FALSE", "severity": "P0", "category": "signing", "message": f"{target_name} notarized is not true."})

    if blockers:
        print(json.dumps({"ok": False, "mode": "public", "evidence_dir": str(evidence_dir), "blockers": blockers}, ensure_ascii=False, indent=2))
        raise SystemExit(8)


def required_evidence_present(evidence_dir: Path, blocker: object) -> bool:
    if not isinstance(blocker, dict):
        return False
    required = blocker.get("required_evidence")
    if not isinstance(required, str) or not required.startswith("release-evidence/"):
        return False
    return (evidence_dir / Path(required).name).is_file()


def validate_release_evidence(evidence_dir: Path, manifest: dict[str, object]) -> list[dict[str, object]]:
    blockers: list[dict[str, object]] = []
    missing_ids = {
        "golden-vectors": "GOLDEN_VECTOR_EVIDENCE_MISSING",
        "internal-validation": "INTERNAL_VALIDATION_EVIDENCE_MISSING",
        "artifact-smoke": "ARTIFACT_SMOKE_EVIDENCE_MISSING",
        "source-archive": "SOURCE_ARCHIVE_EVIDENCE_MISSING",
        "license-approval": "PUBLIC_LICENSE_APPROVAL_MISSING",
        "trademark-approval": "PUBLIC_TRADEMARK_APPROVAL_MISSING",
        "content-authorization": "PUBLIC_CONTENT_AUTHORIZATION_MISSING",
        "windows-authenticode": "WINDOWS_AUTHENTICODE_MISSING",
        "macos-notarization": "MACOS_DEVELOPER_ID_NOTARIZATION_MISSING",
        "linux-archive-signature": "LINUX_ARCHIVE_SIGNATURE_MISSING",
        "public-download": "PUBLIC_DOWNLOAD_URL_NOT_ASSIGNED",
    }
    if not evidence_dir.is_dir():
        blockers.append({"id": "RELEASE_EVIDENCE_DIR_MISSING", "severity": "P0", "category": "public-release", "message": f"release evidence directory is missing: {evidence_dir}"})
        return blockers

    for file_path in evidence_dir.rglob("*"):
        if file_path.is_file():
            blockers.extend(secret_blockers(file_path))

    evidence: dict[str, dict[str, object]] = {}
    for evidence_type, filename in REQUIRED_RELEASE_EVIDENCE.items():
        path = evidence_dir / filename
        if not path.is_file():
            blockers.append({"id": missing_ids[evidence_type], "severity": "P0", "category": "public-release", "message": f"required evidence is missing: {path}"})
            continue
        try:
            data = read_json(path)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            blockers.append({"id": "RELEASE_EVIDENCE_JSON_INVALID", "severity": "P0", "category": "public-release", "message": f"{path.name} is not valid JSON: {exc}"})
            continue
        evidence[evidence_type] = data
        blockers.extend(validate_base_evidence(path, data, evidence_type, manifest))

    if "golden-vectors" in evidence:
        blockers.extend(validate_golden_vector_evidence(evidence["golden-vectors"]))
    if "internal-validation" in evidence:
        blockers.extend(validate_simple_passed_evidence(evidence["internal-validation"], "INTERNAL_VALIDATION_NOT_PASSED", "internal validation evidence is not passed"))
    if "artifact-smoke" in evidence:
        blockers.extend(validate_artifact_smoke_evidence(evidence["artifact-smoke"], manifest))
    if "source-archive" in evidence:
        blockers.extend(validate_source_archive_evidence(evidence["source-archive"]))
    for evidence_type, blocker_id in (
        ("license-approval", "PUBLIC_LICENSE_APPROVAL_NOT_APPROVED"),
        ("trademark-approval", "PUBLIC_TRADEMARK_APPROVAL_NOT_APPROVED"),
        ("content-authorization", "PUBLIC_CONTENT_AUTHORIZATION_NOT_APPROVED"),
    ):
        if evidence_type in evidence:
            blockers.extend(validate_approval_evidence(evidence[evidence_type], blocker_id))
    if "windows-authenticode" in evidence:
        blockers.extend(validate_signing_evidence(evidence["windows-authenticode"], "WINDOWS_AUTHENTICODE_NOT_PASSED", notarization=False))
    if "macos-notarization" in evidence:
        blockers.extend(validate_signing_evidence(evidence["macos-notarization"], "MACOS_NOTARIZATION_NOT_PASSED", notarization=True))
    if "linux-archive-signature" in evidence:
        blockers.extend(validate_signing_evidence(evidence["linux-archive-signature"], "LINUX_ARCHIVE_SIGNATURE_NOT_PASSED", notarization=False, require_signature_format=True))
    if "public-download" in evidence:
        blockers.extend(validate_public_download_evidence(evidence["public-download"], str(manifest.get("release", ""))))
    return blockers


def validate_source_archive_evidence(data: dict[str, object]) -> list[dict[str, object]]:
    blockers = validate_simple_passed_evidence(data, "SOURCE_ARCHIVE_NOT_PASSED", "source archive evidence is not passed")
    if data.get("source_archive_schema_version") != SOURCE_ARCHIVE_SCHEMA_VERSION:
        blockers.append({"id": "SOURCE_ARCHIVE_SCHEMA_VERSION_MISMATCH", "severity": "P0", "category": "source-release", "message": "source archive schema version mismatch"})
    if not isinstance(data.get("source_archive"), dict):
        blockers.append({"id": "SOURCE_ARCHIVE_METADATA_MISSING", "severity": "P0", "category": "source-release", "message": "source archive metadata missing"})
    else:
        archive = data["source_archive"]
        if not archive.get("name"):
            blockers.append({"id": "SOURCE_ARCHIVE_NAME_MISSING", "severity": "P0", "category": "source-release", "message": "source archive name missing"})
        if not is_hex_sha256(archive.get("sha256")):
            blockers.append({"id": "SOURCE_ARCHIVE_HASH_MISSING", "severity": "P0", "category": "source-release", "message": "source archive sha256 missing"})
        if not isinstance(archive.get("size_bytes"), int) or archive.get("size_bytes") <= 0:
            blockers.append({"id": "SOURCE_ARCHIVE_SIZE_MISSING", "severity": "P0", "category": "source-release", "message": "source archive size missing"})
    if data.get("forbidden_path_count") != 0:
        blockers.append({"id": "SOURCE_ARCHIVE_FORBIDDEN_PATHS", "severity": "P0", "category": "source-release", "message": f"source archive forbidden_path_count={data.get('forbidden_path_count')}"})
    if data.get("secret_scan_status") != "passed":
        blockers.append({"id": "SOURCE_ARCHIVE_SECRET_SCAN_NOT_PASSED", "severity": "P0", "category": "source-release", "message": f"source archive secret_scan_status={data.get('secret_scan_status')}"})
    if data.get("manifest_status") != "passed":
        blockers.append({"id": "SOURCE_ARCHIVE_MANIFEST_NOT_PASSED", "severity": "P0", "category": "source-release", "message": f"source archive manifest_status={data.get('manifest_status')}"})
    return blockers


def validate_base_evidence(path: Path, data: dict[str, object], evidence_type: str, manifest: dict[str, object]) -> list[dict[str, object]]:
    blockers: list[dict[str, object]] = []
    checks = {
        "schema_version": RELEASE_EVIDENCE_SCHEMA_VERSION,
        "evidence_type": evidence_type,
        "name": APP_NAME,
        "version": manifest.get("release"),
        "contract_bundle": manifest.get("contract_bundle"),
    }
    for key, expected in checks.items():
        if data.get(key) != expected:
            blockers.append({"id": "RELEASE_EVIDENCE_SCHEMA_MISMATCH", "severity": "P0", "category": "public-release", "message": f"{path.name} {key} mismatch"})
    if not isinstance(data.get("generated_at"), str) or not data.get("generated_at"):
        blockers.append({"id": "RELEASE_EVIDENCE_TIMESTAMP_MISSING", "severity": "P0", "category": "public-release", "message": f"{path.name} missing generated_at"})
    if not isinstance(data.get("status"), str) or not data.get("status"):
        blockers.append({"id": "RELEASE_EVIDENCE_STATUS_MISSING", "severity": "P0", "category": "public-release", "message": f"{path.name} missing status"})
    return blockers


def validate_golden_vector_evidence(data: dict[str, object]) -> list[dict[str, object]]:
    blockers = validate_simple_passed_evidence(data, "GOLDEN_VECTOR_EVIDENCE_NOT_PASSED", "golden vector evidence is not passed")
    if data.get("signing_profile") != SIGNING_PROFILE:
        blockers.append({"id": "GOLDEN_VECTOR_SIGNING_PROFILE_MISMATCH", "severity": "P0", "category": "public-release", "message": "golden vector signing_profile mismatch"})
    if data.get("golden_vector_version") != GOLDEN_VECTOR_VERSION:
        blockers.append({"id": "GOLDEN_VECTOR_VERSION_MISMATCH", "severity": "P0", "category": "public-release", "message": "golden vector version mismatch"})
    if not isinstance(data.get("vectors"), list) or not data["vectors"]:
        blockers.append({"id": "GOLDEN_VECTOR_LIST_MISSING", "severity": "P0", "category": "public-release", "message": "golden vector evidence has no vectors"})
    if not is_hex_sha256(data.get("synthetic_public_key_sha256")):
        blockers.append({"id": "GOLDEN_VECTOR_PUBLIC_KEY_DIGEST_MISSING", "severity": "P0", "category": "public-release", "message": "golden vector public key digest is missing"})
    return blockers


def validate_simple_passed_evidence(data: dict[str, object], blocker_id: str, message: str) -> list[dict[str, object]]:
    if data.get("status") == "passed":
        return []
    return [{"id": blocker_id, "severity": "P0", "category": "public-release", "message": f"{message}: status={data.get('status')}"}]


def validate_artifact_smoke_evidence(data: dict[str, object], manifest: dict[str, object]) -> list[dict[str, object]]:
    blockers = validate_simple_passed_evidence(data, "ARTIFACT_SMOKE_NOT_PASSED", "artifact smoke evidence is not passed")
    results = data.get("smoke_results")
    if not isinstance(results, list) or not results:
        blockers.append({"id": "ARTIFACT_SMOKE_RESULTS_MISSING", "severity": "P0", "category": "public-release", "message": "artifact smoke evidence has no smoke_results"})
        return blockers
    release = manifest.get("release")
    for item in results:
        if not isinstance(item, dict):
            blockers.append({"id": "ARTIFACT_SMOKE_RESULT_INVALID", "severity": "P0", "category": "public-release", "message": "artifact smoke result is not an object"})
            continue
        if item.get("status") != "passed":
            blockers.append({"id": "ARTIFACT_SMOKE_TARGET_NOT_PASSED", "severity": "P0", "category": "public-release", "message": f"artifact smoke target did not pass: {item.get('target')}"})
        if item.get("version") != release:
            blockers.append({"id": "ARTIFACT_SMOKE_VERSION_MISMATCH", "severity": "P0", "category": "public-release", "message": f"artifact smoke version mismatch: {item.get('target')}"})
    return blockers


def validate_approval_evidence(data: dict[str, object], blocker_id: str) -> list[dict[str, object]]:
    blockers: list[dict[str, object]] = []
    if data.get("status") != "approved":
        blockers.append({"id": blocker_id, "severity": "P0", "category": "legal", "message": f"{data.get('evidence_type')} status is not approved: {data.get('status')}"})
    for key in ("issuer", "approved_at", "subject", "scope", "evidence_reference"):
        if not data.get(key):
            blockers.append({"id": "APPROVAL_EVIDENCE_FIELD_MISSING", "severity": "P0", "category": "legal", "message": f"{data.get('evidence_type')} missing {key}"})
    return blockers


def validate_signing_evidence(data: dict[str, object], blocker_id: str, *, notarization: bool, require_signature_format: bool = False) -> list[dict[str, object]]:
    blockers: list[dict[str, object]] = []
    if data.get("status") != "passed":
        blockers.append({"id": blocker_id, "severity": "P0", "category": "signing", "message": f"{data.get('evidence_type')} status is not passed: {data.get('status')}"})
    for key in ("issuer", "signed_at", "verification_command"):
        if not data.get(key):
            blockers.append({"id": "SIGNING_EVIDENCE_FIELD_MISSING", "severity": "P0", "category": "signing", "message": f"{data.get('evidence_type')} missing {key}"})
    if not is_hex_sha256(data.get("subject_sha256")):
        blockers.append({"id": "SIGNING_EVIDENCE_SUBJECT_HASH_MISSING", "severity": "P0", "category": "signing", "message": f"{data.get('evidence_type')} missing subject_sha256"})
    if data.get("evidence_type") == "windows-authenticode" and data.get("timestamped") is not True:
        blockers.append({"id": "WINDOWS_TIMESTAMP_MISSING", "severity": "P0", "category": "signing", "message": "windows Authenticode evidence must be timestamped"})
    if notarization and not data.get("notarized_at"):
        blockers.append({"id": "MACOS_NOTARIZATION_TIMESTAMP_MISSING", "severity": "P0", "category": "signing", "message": "macOS notarization evidence missing notarized_at"})
    if require_signature_format and not data.get("signature_format"):
        blockers.append({"id": "LINUX_SIGNATURE_FORMAT_MISSING", "severity": "P0", "category": "signing", "message": "Linux archive signature evidence missing signature_format"})
    return blockers


def validate_public_download_evidence(data: dict[str, object], version: str) -> list[dict[str, object]]:
    blockers: list[dict[str, object]] = []
    if data.get("status") != "approved":
        blockers.append({"id": "PUBLIC_DOWNLOAD_NOT_APPROVED", "severity": "P0", "category": "distribution", "message": f"public download evidence status is not approved: {data.get('status')}"})
    for key in ("issuer", "approved_at"):
        if not data.get(key):
            blockers.append({"id": "PUBLIC_DOWNLOAD_FIELD_MISSING", "severity": "P0", "category": "distribution", "message": f"public download evidence missing {key}"})
    urls = data.get("immutable_urls")
    if not isinstance(urls, list) or not urls:
        blockers.append({"id": "PUBLIC_DOWNLOAD_URLS_MISSING", "severity": "P0", "category": "distribution", "message": "public download evidence has no immutable_urls"})
        return blockers
    for item in urls:
        if not isinstance(item, dict) or not isinstance(item.get("url"), str):
            blockers.append({"id": "PUBLIC_DOWNLOAD_URL_INVALID", "severity": "P0", "category": "distribution", "message": "public download URL entry is invalid"})
            continue
        url = item["url"]
        if not url.startswith("https://"):
            blockers.append({"id": "PUBLIC_DOWNLOAD_URL_NOT_HTTPS", "severity": "P0", "category": "distribution", "message": f"public download URL is not HTTPS: {url}"})
        if "latest" in url.lower():
            blockers.append({"id": "PUBLIC_DOWNLOAD_URL_MUTABLE", "severity": "P0", "category": "distribution", "message": f"public download URL must not be mutable/latest: {url}"})
        if version and version not in url:
            blockers.append({"id": "PUBLIC_DOWNLOAD_URL_VERSION_MISSING", "severity": "P0", "category": "distribution", "message": f"public download URL does not contain release version: {url}"})
    return blockers


def secret_blockers(path: Path) -> list[dict[str, object]]:
    content = path.read_bytes()
    blockers = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(content):
            blockers.append({"id": "RELEASE_EVIDENCE_SECRET_PATTERN", "severity": "P0", "category": "security", "message": f"{path} contains blocked secret/query pattern"})
    return blockers


def is_hex_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdefABCDEF" for ch in value)


def read_archive_members(path: Path) -> dict[str, bytes]:
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as zf:
            return {info.filename: zf.read(info.filename) for info in zf.infolist() if not info.is_dir()}
    if path.name.endswith(".tar.gz"):
        with tarfile.open(path, "r:gz") as tf:
            out = {}
            for member in tf.getmembers():
                if not member.isfile():
                    continue
                extracted = tf.extractfile(member)
                require(extracted is not None, f"{path.name} cannot read {member.name}")
                out[member.name] = extracted.read()
            return out
    fail(f"unsupported archive type: {path.name}")


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


def read_sha256sums(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        out[name.strip()] = digest
    return out


def scan_file_for_secrets(path: Path) -> None:
    if path.suffix.lower() in {".zip", ".gz", ".exe"}:
        return
    scan_bytes_for_secrets(path.name, path.read_bytes())


def scan_bytes_for_secrets(label: str, content: bytes) -> None:
    for pattern in SECRET_PATTERNS:
        require(pattern.search(content) is None, f"{label} contains blocked secret/query pattern")


def expect_string(data: dict[str, object], key: str) -> str:
    value = data.get(key)
    require(isinstance(value, str) and value, f"{key} missing")
    return value


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def fail(message: str) -> None:
    raise SystemExit(f"[ERROR] {message}")


if __name__ == "__main__":
    raise SystemExit(main())
