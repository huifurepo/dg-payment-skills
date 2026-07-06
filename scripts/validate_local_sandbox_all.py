#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path


CONTRACT_BUNDLE = "huifu-pay-integration-1.3.0-r4"
DEFAULT_TARGETS = "windows/amd64,linux/amd64,darwin/amd64,darwin/arm64"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full local-sandbox validation suite.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--targets", default=DEFAULT_TARGETS)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sandbox_dir = repo_root / "local-sandbox"
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    build_dir = output_dir / "build"
    dist_dir = output_dir / "dist"
    preview_release_dir = output_dir / "preview-release"
    preview_dist_dir = preview_release_dir / "dist"
    source_dir = output_dir / "source"
    scenario_report_dir = output_dir / "scenario-report"
    build_dir.mkdir(exist_ok=True)

    binary = build_dir / ("hf-payment-local-sandbox.exe" if os.name == "nt" else "hf-payment-local-sandbox")
    steps: list[dict[str, object]] = []
    steps.append(run_step("contract-fixtures", [sys.executable, "scripts/validate_contract_fixtures.py"], repo_root))
    steps.append(run_step("go-test", ["go", "test", "./...", "-count=1"], sandbox_dir))
    steps.append(run_step("go-vet", ["go", "vet", "./..."], sandbox_dir))
    steps.append(run_step("go-build", ["go", "build", "-o", str(binary), "."], sandbox_dir))
    steps.append(run_step("validate-contract", ["go", "run", ".", "validate", "contract"], sandbox_dir))
    steps.append(run_step("validate-samples", [sys.executable, "scripts/validate_local_sandbox_samples.py", "--require-samples"], repo_root))
    steps.append(run_step("import-samples-dry-run", [sys.executable, "scripts/import_local_sandbox_samples.py"], repo_root))
    steps.append(run_step("validate-scenarios", ["go", "run", ".", "validate", "scenarios", "--report-dir", str(scenario_report_dir), "--print-json"], sandbox_dir))
    steps.append(
        run_step(
            "sample-replay-contracts",
            [
                sys.executable,
                "scripts/validate_local_sandbox_sample_replay_contracts.py",
                "--scenario-report-dir",
                str(scenario_report_dir),
                "--output",
                str(scenario_report_dir / "sample-replay-contracts.json"),
            ],
            repo_root,
        )
    )
    steps.append(run_step("golden-vectors", [sys.executable, "scripts/validate_local_sandbox_golden_vectors.py", "--strict"], repo_root))
    steps.append(run_step("sdk-samples", [sys.executable, "scripts/validate_local_sandbox_sdk_samples.py", "--version", args.version], repo_root))
    steps.append(run_step("validate-skills", [sys.executable, "scripts/validate_skills.py"], repo_root))
    steps.append(
        run_step(
            "package-release",
            [
                sys.executable,
                "scripts/package_local_sandbox_release.py",
                "--version",
                args.version,
                "--release-channel",
                "internal-rc",
                "--output-dir",
                str(dist_dir),
                "--targets",
                args.targets,
            ],
            repo_root,
        )
    )
    steps.append(
        run_step(
            "validate-release-internal",
            [
                sys.executable,
                "scripts/validate_local_sandbox_release.py",
                "--dist",
                str(dist_dir),
                "--version",
                args.version,
                "--contract-bundle",
                CONTRACT_BUNDLE,
                "--mode",
                "internal",
            ],
            repo_root,
        )
    )
    steps.append(
        run_step(
            "package-preview-release",
            [
                sys.executable,
                "scripts/package_local_sandbox_release.py",
                "--version",
                args.version,
                "--release-channel",
                "preview",
                "--output-dir",
                str(preview_dist_dir),
                "--targets",
                args.targets,
            ],
            repo_root,
        )
    )
    steps.append(create_preview_bundle_step("package-preview-wrapper", preview_release_dir, args.version))
    steps.append(
        run_step(
            "generate-preview-update-index",
            [
                sys.executable,
                "scripts/generate_local_sandbox_update_index.py",
                "--manifest",
                str(preview_dist_dir / "release-manifest.json"),
                "--preview-package",
                str(preview_release_dir / "hf-payment-local-sandbox-latest-preview.zip"),
                "--output",
                str(preview_release_dir / "hf-payment-local-sandbox-latest.json"),
            ],
            repo_root,
        )
    )
    steps.append(
        run_step(
            "validate-preview-bundle",
            [
                sys.executable,
                "scripts/validate_local_sandbox_preview_bundle.py",
                "--release-dir",
                str(preview_release_dir),
                "--version",
                args.version,
            ],
            repo_root,
        )
    )
    source_package = run_step(
        "package-source",
        [sys.executable, "scripts/package_local_sandbox_source_release.py", "--version", args.version, "--output-dir", str(source_dir)],
        repo_root,
    )
    steps.append(source_package)
    source_archive = source_dir / f"hf-payment-local-sandbox-source_{args.version}.tar.gz"
    source_manifest = source_dir / "source-manifest.json"
    steps.append(
        run_step(
            "validate-source-release",
            [
                sys.executable,
                "scripts/validate_local_sandbox_source_release.py",
                "--archive",
                str(source_archive),
                "--manifest",
                str(source_manifest),
                "--version",
                args.version,
            ],
            repo_root,
        )
    )

    ok = all(step["returncode"] == 0 for step in steps)
    print(
        json.dumps(
            {
                "ok": ok,
                "version": args.version,
                "contract_bundle": CONTRACT_BUNDLE,
                "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "output_dir": str(output_dir),
                "steps": steps,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if ok else 1


def create_preview_bundle_step(name: str, release_dir: Path, version: str) -> dict[str, object]:
    started = time.time()
    try:
        versioned_zip, latest_zip = create_preview_bundle(release_dir, version)
        return {
            "name": name,
            "command": ["create-preview-bundle", str(release_dir), version],
            "cwd": str(release_dir.parent),
            "returncode": 0,
            "duration_seconds": round(time.time() - started, 3),
            "output_tail": json.dumps(
                {
                    "ok": True,
                    "versioned_zip": str(versioned_zip),
                    "latest_zip": str(latest_zip),
                    "sha256": sha256_file(versioned_zip),
                },
                ensure_ascii=False,
            ),
        }
    except Exception as exc:
        return {
            "name": name,
            "command": ["create-preview-bundle", str(release_dir), version],
            "cwd": str(release_dir.parent),
            "returncode": 1,
            "duration_seconds": round(time.time() - started, 3),
            "output_tail": str(exc),
        }


def create_preview_bundle(release_dir: Path, version: str) -> tuple[Path, Path]:
    dist_dir = release_dir / "dist"
    if not dist_dir.is_dir():
        raise FileNotFoundError(f"{dist_dir} is missing")
    prepare_preview_root_docs(release_dir, version)
    versioned_zip = release_dir / f"hf-payment-local-sandbox-{version}-preview.zip"
    latest_zip = release_dir / "hf-payment-local-sandbox-latest-preview.zip"
    for path in (versioned_zip, latest_zip):
        path.unlink(missing_ok=True)
        path.with_suffix(path.suffix + ".sha256").unlink(missing_ok=True)
    with zipfile.ZipFile(versioned_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root_name in ("README.md", "USAGE.md"):
            root_file = release_dir / root_name
            zf.write(root_file, root_name)
        for item in sorted(dist_dir.iterdir(), key=lambda p: p.name):
            if item.is_file():
                zf.write(item, f"dist/{item.name}")
    latest_zip.write_bytes(versioned_zip.read_bytes())
    write_sha256_file(versioned_zip)
    write_sha256_file(latest_zip)
    return versioned_zip, latest_zip


def prepare_preview_root_docs(release_dir: Path, version: str) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    usage_source = repo_root / "local-sandbox" / "USAGE.md"
    if not usage_source.is_file():
        raise FileNotFoundError(f"{usage_source} is missing")
    (release_dir / "README.md").write_text(preview_readme_text(version), encoding="utf-8")
    (release_dir / "USAGE.md").write_text(usage_source.read_text(encoding="utf-8"), encoding="utf-8")


def preview_readme_text(version: str) -> str:
    return f"""# hf-payment-local-sandbox {version} Preview

This zip is the preview download bundle for the Huifu Payment local sandbox service.

## Start Here

1. Open the `dist/` directory.
2. Choose the archive for your operating system:
   - Windows: `hf-payment-local-sandbox_{version}_windows_amd64.zip`
   - macOS Intel: `hf-payment-local-sandbox_{version}_darwin_amd64.tar.gz`
   - macOS Apple Silicon: `hf-payment-local-sandbox_{version}_darwin_arm64.tar.gz`
   - Linux: `hf-payment-local-sandbox_{version}_linux_amd64.tar.gz`
3. Extract that platform archive.
4. Use the platform launcher or run `hf-payment-local-sandbox version --json` to confirm the binary.
5. Read `USAGE.md` for startup, credential export, SDK configuration, webhook/notify testing, and reports.

This preview is unsigned and not notarized. It is intended for local protocol simulation and integration rehearsal, not as a formal production acceptance result.
"""


def write_sha256_file(path: Path) -> None:
    path.with_suffix(path.suffix + ".sha256").write_text(f"{sha256_file(path)}  {path.name}\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_step(name: str, command: list[str], cwd: Path) -> dict[str, object]:
    started = time.time()
    try:
        completed = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        output = completed.stdout or ""
        return {
            "name": name,
            "command": command,
            "cwd": str(cwd),
            "returncode": completed.returncode,
            "duration_seconds": round(time.time() - started, 3),
            "output_tail": redact_output(output[-4000:]),
        }
    except FileNotFoundError as exc:
        return {
            "name": name,
            "command": command,
            "cwd": str(cwd),
            "returncode": 127,
            "duration_seconds": round(time.time() - started, 3),
            "output_tail": str(exc),
        }


def redact_output(value: str) -> str:
    redacted = re.sub(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "[REDACTED_PRIVATE_KEY_BLOCK]",
        value,
        flags=re.S,
    )
    redacted = re.sub(
        r'(?i)("?(?:access[_-]?token|api[_-]?key|secret|password|private[_-]?key|sign)"?\s*[:=]\s*)("[^"]+"|[^,\s}]+)',
        r'\1"REDACTED"',
        redacted,
    )
    return redacted


if __name__ == "__main__":
    raise SystemExit(main())
