#!/usr/bin/env python3
"""Build and validate both Skill packages in a temporary directory."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "skills-manifest.json"
RELEASE_EVIDENCE_SUITES = {
    "payment": "payment-only",
    "onboarding": "onboarding-only",
    "cross-route": "both",
}


def validate_release_evidence(evidence: list[str]) -> None:
    if not evidence:
        return
    mapped: dict[str, Path] = {}
    for item in evidence:
        if "=" not in item:
            raise SystemExit("release evidence requires an explicit safe label=path")
        label, raw_path = item.split("=", 1)
        if label in mapped:
            raise SystemExit(f"duplicate release evidence label: {label}")
        mapped[label] = Path(raw_path).resolve()
    expected = {
        f"real-model/{suite}/{filename}"
        for suite in RELEASE_EVIDENCE_SUITES
        for filename in ("run-manifest.json", "summary.json")
    }
    if set(mapped) != expected:
        raise SystemExit(
            "release evidence set mismatch; "
            f"missing={sorted(expected - set(mapped))}, "
            f"extra={sorted(set(mapped) - expected)}"
        )
    for suite, load_mode in RELEASE_EVIDENCE_SUITES.items():
        manifest_path = mapped[f"real-model/{suite}/run-manifest.json"]
        summary_path = mapped[f"real-model/{suite}/summary.json"]
        if (
            manifest_path.name != "run-manifest.json"
            or summary_path.name != "summary.json"
            or manifest_path.parent != summary_path.parent
        ):
            raise SystemExit(f"{suite}: evidence files must share one suite directory")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise SystemExit(f"{suite}: invalid run manifest: {exc}") from exc
        if not isinstance(manifest, dict):
            raise SystemExit(f"{suite}: run manifest root must be an object")
        command = [
            sys.executable,
            str(REPO_ROOT / "scripts/run_real_model_regression.py"),
            "--suite",
            suite,
            "--load-mode",
            load_mode,
            "--output-dir",
            str(manifest_path.parent),
            "--skip-run",
            "--model",
            str(manifest.get("model", "")),
            "--jobs",
            str(manifest.get("jobs", "")),
            "--timeout",
            str(manifest.get("timeout_seconds", "")),
        ]
        codex_executable = manifest.get("codex_executable")
        if isinstance(codex_executable, str) and codex_executable:
            command.extend(["--codex-executable", codex_executable])
        replay_env = os.environ.copy()
        reasoning_effort = manifest.get("reasoning_effort")
        if isinstance(reasoning_effort, str) and reasoning_effort:
            replay_env["CODEX_REGRESSION_REASONING_EFFORT"] = reasoning_effort
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            env=replay_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode != 0:
            raise SystemExit(
                f"{suite}: release evidence semantic replay failed:\n{result.stdout}"
            )


def build_and_validate(
    output: Path,
    manifest: dict[str, object],
    evidence: list[str],
    allow_dirty: bool,
) -> None:
    for skill, spec in manifest["skills"].items():
        package_command = [
            sys.executable,
            str(REPO_ROOT / "scripts/package_skill.py"),
            "--skill",
            skill,
            "--output-dir",
            str(output),
        ]
        if allow_dirty:
            package_command.append("--allow-dirty")
        for evidence_item in evidence:
            package_command.extend(["--evidence", evidence_item])
        subprocess.run(
            package_command,
            cwd=REPO_ROOT,
            check=True,
        )
        validate_command = [
            sys.executable,
            str(REPO_ROOT / "scripts/validate_skill_package.py"),
            "--skill",
            skill,
            "--archive",
            str(output / f"{skill}-{spec['version']}.zip"),
        ]
        if allow_dirty:
            validate_command.append("--allow-dirty-provenance")
        subprocess.run(
            validate_command,
            cwd=REPO_ROOT,
            check=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate_release_evidence(args.evidence)
    if args.output_dir is not None:
        if args.output_dir.exists():
            raise SystemExit(f"package output directory already exists: {args.output_dir}")
        args.output_dir.mkdir(parents=False)
        build_and_validate(args.output_dir, manifest, args.evidence, args.allow_dirty)
    else:
        with tempfile.TemporaryDirectory(prefix="huifu-skill-packages-") as directory:
            build_and_validate(Path(directory), manifest, args.evidence, args.allow_dirty)
    print(f"independent package validation passed: {len(manifest['skills'])} manifest skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
