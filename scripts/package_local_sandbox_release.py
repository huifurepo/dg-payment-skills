#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


APP_NAME = "hf-payment-local-sandbox"
CONTRACT_BUNDLE = "huifu-pay-integration-1.3.0-r4"
SOURCE_SKILL_VERSION = "1.3.1"
REPORT_SCHEMA_VERSION = "1.7"
SCENARIO_SCHEMA_VERSION = "1.0"
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
DEFAULT_TARGETS = ("windows/amd64", "linux/amd64", "darwin/amd64", "darwin/arm64")
REQUIRED_RELEASE_EVIDENCE = (
    "golden-vectors.json",
    "internal-validation.json",
    "artifact-smoke.json",
    "source-archive.json",
    "license-approval.json",
    "trademark-approval.json",
    "content-authorization.json",
    "windows-authenticode.json",
    "macos-notarization.json",
    "linux-archive-signature.json",
    "public-download.json",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Package local-sandbox release candidate artifacts.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--release-channel", default="internal-rc")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--targets", default=",".join(DEFAULT_TARGETS))
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sandbox_dir = repo_root / "local-sandbox"
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    targets = parse_targets(args.targets)
    commit = git_output(repo_root, "rev-parse", "HEAD") or "unknown"
    dirty = bool(git_output(repo_root, "status", "--porcelain"))
    build_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    go_version = subprocess.check_output(["go", "version"], text=True).strip()
    modules = go_modules(sandbox_dir)

    target_entries = []
    produced_files = []
    for goos, goarch in targets:
        entry, files = package_target(
            repo_root=repo_root,
            sandbox_dir=sandbox_dir,
            output_dir=output_dir,
            version=args.version,
            release_channel=args.release_channel,
            build_commit=commit,
            build_dirty=dirty,
            build_time=build_time,
            go_version=go_version,
            goos=goos,
            goarch=goarch,
            modules=modules,
        )
        target_entries.append(entry)
        produced_files.extend(files)

    manifest = {
        "schema_version": "1.0",
        "name": APP_NAME,
        "release": args.version,
        "release_channel": args.release_channel,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "contract_bundle": CONTRACT_BUNDLE,
        "source_skill_version": SOURCE_SKILL_VERSION,
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "scenario_schema_version": SCENARIO_SCHEMA_VERSION,
        "signing_profile": SIGNING_PROFILE,
        "golden_vector_version": GOLDEN_VECTOR_VERSION,
        "release_evidence_schema_version": RELEASE_EVIDENCE_SCHEMA_VERSION,
        "source_archive_schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
        "coverage_runner_version": COVERAGE_RUNNER_VERSION,
        "reference_digest_schema_version": REFERENCE_DIGEST_SCHEMA_VERSION,
        "fixture_runner_version": FIXTURE_RUNNER_VERSION,
        "ops_cli_schema_version": OPS_CLI_SCHEMA_VERSION,
        "sample_schema_version": SAMPLE_SCHEMA_VERSION,
        "sample_importer_version": SAMPLE_IMPORTER_VERSION,
        "compatible_contract_bundles": [CONTRACT_BUNDLE],
        "build_commit": commit,
        "build_dirty": dirty,
        "code_signed": False,
        "notarized": False,
        "targets": target_entries,
    }
    readiness_path = output_dir / "release-readiness.json"
    write_json(
        readiness_path,
        release_readiness_payload(
            version=args.version,
            release_channel=args.release_channel,
            build_commit=commit,
            build_dirty=dirty,
            target_count=len(target_entries),
        ),
    )
    manifest["release_readiness"] = file_meta(readiness_path)
    produced_files.append(readiness_path)

    manifest_path = output_dir / "release-manifest.json"
    write_json(manifest_path, manifest)
    produced_files.append(manifest_path)

    write_sha256sums(output_dir / "SHA256SUMS.txt", produced_files, output_dir)
    print(json.dumps({"ok": True, "output_dir": str(output_dir), "targets": len(target_entries)}, ensure_ascii=False))
    return 0


def parse_targets(raw: str) -> list[tuple[str, str]]:
    targets = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split("/")
        if len(parts) != 2 or not all(parts):
            raise SystemExit(f"invalid target {item!r}; expected goos/goarch")
        targets.append((parts[0], parts[1]))
    if not targets:
        raise SystemExit("at least one target is required")
    return targets


def package_target(
    *,
    repo_root: Path,
    sandbox_dir: Path,
    output_dir: Path,
    version: str,
    release_channel: str,
    build_commit: str,
    build_dirty: bool,
    build_time: str,
    go_version: str,
    goos: str,
    goarch: str,
    modules: list[dict[str, object]],
) -> tuple[dict[str, object], list[Path]]:
    base_name = f"{APP_NAME}_{version}_{goos}_{goarch}"
    archive_name = base_name + (".zip" if goos == "windows" else ".tar.gz")
    binary_name = APP_NAME + (".exe" if goos == "windows" else "")
    archive_path = output_dir / archive_name
    sbom_path = output_dir / f"{base_name}.spdx.json"
    provenance_path = output_dir / f"{base_name}.provenance.json"

    with tempfile.TemporaryDirectory(prefix="local-sandbox-release-") as tmp_raw:
        stage = Path(tmp_raw)
        binary_path = stage / binary_name
        ldflags = " ".join(
            [
                "-s",
                "-w",
                f"-X main.buildCommit={build_commit}",
                f"-X main.buildTime={build_time}",
                f"-X main.buildDirty={str(build_dirty).lower()}",
                f"-X main.releaseChannel={release_channel}",
            ]
        )
        env = os.environ.copy()
        env.update({"GOOS": goos, "GOARCH": goarch, "CGO_ENABLED": "0"})
        subprocess.check_call(["go", "build", "-trimpath", "-ldflags", ldflags, "-o", str(binary_path), "."], cwd=sandbox_dir, env=env)

        build_info = build_info_payload(
            version=version,
            release_channel=release_channel,
            build_commit=build_commit,
            build_dirty=build_dirty,
            build_time=build_time,
            go_version=go_version,
            goos=goos,
            goarch=goarch,
            binary_name=binary_name,
        )
        write_json(stage / "build-info.json", build_info)
        (stage / "README.txt").write_text(readme_text(version, release_channel), encoding="utf-8")
        shutil.copyfile(sandbox_dir / "USAGE.md", stage / "USAGE.md")
        shutil.copyfile(repo_root / "LICENSE", stage / "LICENSE")
        (stage / "THIRD_PARTY_NOTICES.txt").write_text(third_party_notice(modules), encoding="utf-8")
        launcher_names = write_launcher_files(stage=stage, goos=goos, binary_name=binary_name)

        if goos == "windows":
            write_zip(archive_path, stage, binary_name, launcher_names)
        else:
            write_targz(archive_path, stage, binary_name, launcher_names)

    write_json(sbom_path, sbom_payload(version, goos, goarch, modules))
    write_json(
        provenance_path,
        provenance_payload(
            version=version,
            release_channel=release_channel,
            build_commit=build_commit,
            build_dirty=build_dirty,
            build_time=build_time,
            go_version=go_version,
            goos=goos,
            goarch=goarch,
            binary_name=binary_name,
            archive_name=archive_name,
        ),
    )

    archive_meta = file_meta(archive_path)
    sbom_meta = file_meta(sbom_path)
    provenance_meta = file_meta(provenance_path)
    entry = {
        "goos": goos,
        "goarch": goarch,
        "binary_name": binary_name,
        "archive": archive_meta,
        "sbom": sbom_meta,
        "provenance": provenance_meta,
        "code_signed": False,
        "notarized": False,
    }
    return entry, [archive_path, sbom_path, provenance_path]


def build_info_payload(**kwargs: object) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "name": APP_NAME,
        "version": kwargs["version"],
        "release_channel": kwargs["release_channel"],
        "contract_bundle": CONTRACT_BUNDLE,
        "source_skill_version": SOURCE_SKILL_VERSION,
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "scenario_schema_version": SCENARIO_SCHEMA_VERSION,
        "signing_profile": SIGNING_PROFILE,
        "golden_vector_version": GOLDEN_VECTOR_VERSION,
        "release_evidence_schema_version": RELEASE_EVIDENCE_SCHEMA_VERSION,
        "source_archive_schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
        "coverage_runner_version": COVERAGE_RUNNER_VERSION,
        "reference_digest_schema_version": REFERENCE_DIGEST_SCHEMA_VERSION,
        "fixture_runner_version": FIXTURE_RUNNER_VERSION,
        "ops_cli_schema_version": OPS_CLI_SCHEMA_VERSION,
        "sample_schema_version": SAMPLE_SCHEMA_VERSION,
        "sample_importer_version": SAMPLE_IMPORTER_VERSION,
        "build_commit": kwargs["build_commit"],
        "build_time": kwargs["build_time"],
        "build_dirty": kwargs["build_dirty"],
        "go_version": kwargs["go_version"],
        "goos": kwargs["goos"],
        "goarch": kwargs["goarch"],
        "binary_name": kwargs["binary_name"],
        "cgo_enabled": False,
        "code_signed": False,
        "notarized": False,
        "distribution": "internal release candidate; not for public download",
    }


def provenance_payload(**kwargs: object) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "subject": APP_NAME,
        "version": kwargs["version"],
        "release_channel": kwargs["release_channel"],
        "build_commit": kwargs["build_commit"],
        "build_dirty": kwargs["build_dirty"],
        "build_time": kwargs["build_time"],
        "go_version": kwargs["go_version"],
        "goos": kwargs["goos"],
        "goarch": kwargs["goarch"],
        "binary_name": kwargs["binary_name"],
        "archive_name": kwargs["archive_name"],
        "contract_bundle": CONTRACT_BUNDLE,
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "signing_profile": SIGNING_PROFILE,
        "golden_vector_version": GOLDEN_VECTOR_VERSION,
        "release_evidence_schema_version": RELEASE_EVIDENCE_SCHEMA_VERSION,
        "source_archive_schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
        "coverage_runner_version": COVERAGE_RUNNER_VERSION,
        "reference_digest_schema_version": REFERENCE_DIGEST_SCHEMA_VERSION,
        "fixture_runner_version": FIXTURE_RUNNER_VERSION,
        "ops_cli_schema_version": OPS_CLI_SCHEMA_VERSION,
        "sample_schema_version": SAMPLE_SCHEMA_VERSION,
        "sample_importer_version": SAMPLE_IMPORTER_VERSION,
        "build_command": "go build -trimpath -ldflags <metadata> -o <binary> .",
        "cgo_enabled": False,
        "code_signed": False,
        "notarized": False,
    }


def release_readiness_payload(**kwargs: object) -> dict[str, object]:
    blockers = [
        {
            "id": "SOURCE_ARCHIVE_EVIDENCE_MISSING",
            "severity": "P0",
            "category": "source-release",
            "message": "Source archive whitelist validation evidence is not present.",
            "required_evidence": "release-evidence/source-archive.json",
        },
        {
            "id": "PUBLIC_LICENSE_APPROVAL_MISSING",
            "severity": "P0",
            "category": "legal",
            "message": "Public redistribution license, trademark, and documentation authorization evidence is not present.",
            "required_evidence": "release-evidence/license-approval.json",
        },
        {
            "id": "PUBLIC_TRADEMARK_APPROVAL_MISSING",
            "severity": "P0",
            "category": "legal",
            "message": "Trademark and product naming approval evidence is not present.",
            "required_evidence": "release-evidence/trademark-approval.json",
        },
        {
            "id": "PUBLIC_CONTENT_AUTHORIZATION_MISSING",
            "severity": "P0",
            "category": "legal",
            "message": "Protocol material, fixture, and documentation authorization evidence is not present.",
            "required_evidence": "release-evidence/content-authorization.json",
        },
        {
            "id": "WINDOWS_AUTHENTICODE_MISSING",
            "severity": "P0",
            "category": "signing",
            "message": "Windows Authenticode signing evidence is not present.",
            "required_evidence": "release-evidence/windows-authenticode.json",
        },
        {
            "id": "MACOS_DEVELOPER_ID_NOTARIZATION_MISSING",
            "severity": "P0",
            "category": "signing",
            "message": "macOS Developer ID signing and notarization evidence is not present.",
            "required_evidence": "release-evidence/macos-notarization.json",
        },
        {
            "id": "LINUX_ARCHIVE_SIGNATURE_MISSING",
            "severity": "P0",
            "category": "signing",
            "message": "Linux archive signature evidence is not present.",
            "required_evidence": "release-evidence/linux-archive-signature.json",
        },
        {
            "id": "PUBLIC_DOWNLOAD_URL_NOT_ASSIGNED",
            "severity": "P0",
            "category": "distribution",
            "message": "Official public download URL and publication approval are not assigned.",
            "required_evidence": "release-evidence/public-download.json",
        },
    ]
    return {
        "schema_version": "1.0",
        "name": APP_NAME,
        "version": kwargs["version"],
        "release_channel": kwargs["release_channel"],
        "status": "blocked",
        "public_release_allowed": False,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "build_commit": kwargs["build_commit"],
        "build_dirty": kwargs["build_dirty"],
        "contract_bundle": CONTRACT_BUNDLE,
        "signing_profile": SIGNING_PROFILE,
        "golden_vector_version": GOLDEN_VECTOR_VERSION,
        "release_evidence_schema_version": RELEASE_EVIDENCE_SCHEMA_VERSION,
        "source_archive_schema_version": SOURCE_ARCHIVE_SCHEMA_VERSION,
        "coverage_runner_version": COVERAGE_RUNNER_VERSION,
        "reference_digest_schema_version": REFERENCE_DIGEST_SCHEMA_VERSION,
        "fixture_runner_version": FIXTURE_RUNNER_VERSION,
        "ops_cli_schema_version": OPS_CLI_SCHEMA_VERSION,
        "sample_schema_version": SAMPLE_SCHEMA_VERSION,
        "sample_importer_version": SAMPLE_IMPORTER_VERSION,
        "required_evidence_files": list(REQUIRED_RELEASE_EVIDENCE),
        "golden_vectors_required": True,
        "golden_vectors_command": "python scripts/validate_local_sandbox_golden_vectors.py --strict",
        "target_count": kwargs["target_count"],
        "blockers": blockers,
    }


def sbom_payload(version: str, goos: str, goarch: str, modules: list[dict[str, object]]) -> dict[str, object]:
    packages = []
    for module in modules:
        name = str(module.get("Path", "unknown"))
        module_version = str(module.get("Version", ""))
        packages.append(
            {
                "SPDXID": "SPDXRef-Package-" + safe_spdx_id(name + "-" + module_version),
                "name": name,
                "versionInfo": module_version or "local",
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
            }
        )
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"{APP_NAME}-{version}-{goos}-{goarch}",
        "documentNamespace": f"https://local-sandbox.invalid/spdx/{version}/{goos}/{goarch}",
        "creationInfo": {
            "created": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "creators": ["Tool: package_local_sandbox_release.py"],
        },
        "packages": packages,
    }


def go_modules(sandbox_dir: Path) -> list[dict[str, object]]:
    raw = subprocess.check_output(["go", "list", "-m", "-json", "all"], cwd=sandbox_dir, text=True)
    decoder = json.JSONDecoder()
    index = 0
    modules = []
    while index < len(raw):
        while index < len(raw) and raw[index].isspace():
            index += 1
        if index >= len(raw):
            break
        obj, end = decoder.raw_decode(raw, index)
        modules.append(obj)
        index = end
    return modules


def third_party_notice(modules: list[dict[str, object]]) -> str:
    lines = [
        "Third Party Notices",
        "",
        "This internal release candidate is generated from the Go module graph.",
        "License metadata is not asserted by this dry-run packager.",
        "",
    ]
    for module in modules:
        version = module.get("Version") or "local"
        lines.append(f"- {module.get('Path')} {version}")
    return "\n".join(lines) + "\n"


def readme_text(version: str, release_channel: str) -> str:
    return (
        f"{APP_NAME} {version}\n"
        f"Release channel: {release_channel}\n\n"
        "Internal release candidate for local simulation and official-gateway proxy validation.\n"
        "Do not use this binary for production, real funds, merchant onboarding approval, or public release evidence by itself.\n"
        "For first-time local use, double-click start-local-sandbox.cmd on Windows or start-local-sandbox.command on macOS.\n"
        "See USAGE.md for official-demo Profile startup, credential, scenario validation, report, and cleanup commands.\n"
    )


def write_launcher_files(*, stage: Path, goos: str, binary_name: str) -> list[str]:
    if goos == "windows":
        name = "start-local-sandbox.cmd"
        (stage / name).write_text(
            "\r\n".join(
                [
                    "@echo off",
                    "setlocal",
                    'cd /d "%~dp0"',
                    "echo Starting Huifu local sandbox...",
                    "echo The console page will open in your default browser.",
                    "echo Keep this window open while testing. Press Ctrl+C to stop.",
                    "echo.",
                    f'"%~dp0{binary_name}" serve --credential-profile official-demo --control-port 8765 --gateway-port 8766 --data-dir "%~dp0sandbox-data" --report-dir "%~dp0sandbox-report" --open',
                    "echo.",
                    "echo Sandbox stopped. Press any key to close.",
                    "pause >nul",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return [name]

    shell = "\n".join(
        [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            'cd "$(dirname "$0")"',
            "echo \"Starting Huifu local sandbox...\"",
            "echo \"The console page will open in your default browser.\"",
            "echo \"Keep this window open while testing. Press Ctrl+C to stop.\"",
            "echo",
            f'./{binary_name} serve --credential-profile official-demo --control-port 8765 --gateway-port 8766 --data-dir ./sandbox-data --report-dir ./sandbox-report --open',
            "",
        ]
    )
    names = ["start-local-sandbox.sh"]
    if goos == "darwin":
        names.insert(0, "start-local-sandbox.command")
    for name in names:
        path = stage / name
        path.write_text(shell, encoding="utf-8")
        path.chmod(0o755)
    return names


def write_zip(path: Path, stage: Path, binary_name: str, launcher_names: list[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in archive_names(binary_name, launcher_names):
            zf.write(stage / name, arcname=name)


def write_targz(path: Path, stage: Path, binary_name: str, launcher_names: list[str]) -> None:
    with tarfile.open(path, "w:gz") as tf:
        for name in archive_names(binary_name, launcher_names):
            file_path = stage / name
            info = tf.gettarinfo(str(file_path), arcname=name)
            with file_path.open("rb") as fh:
                tf.addfile(info, fh)


def archive_names(binary_name: str, launcher_names: list[str]) -> list[str]:
    return [binary_name, *launcher_names, "build-info.json", "README.txt", "USAGE.md", "LICENSE", "THIRD_PARTY_NOTICES.txt"]


def file_meta(path: Path) -> dict[str, object]:
    return {"name": path.name, "sha256": sha256_file(path), "size_bytes": path.stat().st_size}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_sha256sums(path: Path, files: list[Path], output_dir: Path) -> None:
    lines = []
    for file_path in sorted(files, key=lambda item: item.name):
        lines.append(f"{sha256_file(file_path)}  {file_path.relative_to(output_dir).as_posix()}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_output(repo_root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=repo_root, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def safe_spdx_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in value).strip("-") or "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
