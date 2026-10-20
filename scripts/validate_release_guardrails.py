#!/usr/bin/env python3
"""Regression checks for release, security, and domain-boundary guardrails."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import warnings
import zipfile
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import package_skill  # noqa: E402
import run_real_model_regression  # noqa: E402
import scan_sensitive_examples  # noqa: E402
import generate_merchant_onboarding_field_catalog  # noqa: E402
import refresh_onboarding_sources  # noqa: E402
import validate_merchant_onboarding_source_contract  # noqa: E402
import validate_skill_package  # noqa: E402
import validate_skill_packages  # noqa: E402
import validate_skill_split  # noqa: E402
from skill_validation_config import onboarding_source_dir  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expect_value_error(callable_, expected_text: str) -> None:
    try:
        callable_()
    except ValueError as exc:
        require(expected_text in str(exc), f"unexpected error: {exc}")
    else:
        raise AssertionError(f"expected ValueError containing {expected_text!r}")


def expect_system_exit(callable_, expected_text: str) -> None:
    try:
        callable_()
    except SystemExit as exc:
        require(expected_text in str(exc), f"unexpected exit: {exc}")
    else:
        raise AssertionError(f"expected SystemExit containing {expected_text!r}")


def validate_markdown_table_parsers() -> None:
    fixture = r"| sys_id | 系统\|编号 | String | 32 | Y | 保留\|说明 |"
    expected = ["sys_id", "系统|编号", "String", "32", "Y", "保留|说明"]
    require(
        generate_merchant_onboarding_field_catalog.split_markdown_row(fixture)
        == expected,
        "catalog generator corrupts Markdown-escaped pipes",
    )
    require(
        validate_merchant_onboarding_source_contract.split_source_row(fixture)
        == expected,
        "independent source parser corrupts Markdown-escaped pipes",
    )


def validate_onboarding_route_contract() -> None:
    skill_text = (
        REPO_ROOT / "huifu-merchant-onboarding/SKILL.md"
    ).read_text(encoding="utf-8")
    open_path = (
        REPO_ROOT
        / "huifu-merchant-onboarding/references/merchant-onboarding-business-open.md"
    )
    modify_path = (
        REPO_ROOT
        / "huifu-merchant-onboarding/references/merchant-onboarding-business-open-modify.md"
    )
    official_root = onboarding_source_dir()
    cases = json.loads(
        (REPO_ROOT / "tests/regression/onboarding.json").read_text(encoding="utf-8")
    )
    arguments = (
        skill_text,
        open_path.read_text(encoding="utf-8"),
        modify_path.read_text(encoding="utf-8"),
        (official_root / "business-open.md").read_text(encoding="utf-8"),
        (official_root / "business-open-modify.md").read_text(encoding="utf-8"),
        cases,
    )
    require(
        not validate_merchant_onboarding_source_contract.onboarding_route_contract_errors(
            *arguments
        ),
        "current onboarding supplementary-business route contract is inconsistent",
    )
    broken_open = arguments[1].replace(
        "银联、银行卡业务开通仍使用本接口",
        "银联、银行卡业务开通改走其他接口",
    )
    require(
        validate_merchant_onboarding_source_contract.onboarding_route_contract_errors(
            arguments[0],
            broken_open,
            *arguments[2:],
        ),
        "route contract did not reject a changed UnionPay/card endpoint rule",
    )


def validate_release_evidence_profile() -> None:
    with tempfile.TemporaryDirectory(prefix="huifu-fake-model-evidence-") as directory:
        root = Path(directory)
        evidence: list[str] = []
        for suite in validate_skill_packages.RELEASE_EVIDENCE_SUITES:
            suite_dir = root / suite
            suite_dir.mkdir()
            manifest = suite_dir / "run-manifest.json"
            summary = suite_dir / "summary.json"
            manifest.write_text('{"suite":"fake","jobs":999}\n', encoding="utf-8")
            summary.write_text('{"passed":999}\n', encoding="utf-8")
            evidence.extend(
                [
                    f"real-model/{suite}/run-manifest.json={manifest}",
                    f"real-model/{suite}/summary.json={summary}",
                ]
            )
        expect_system_exit(
            lambda: validate_skill_packages.validate_release_evidence(evidence),
            "release evidence semantic replay failed",
        )


def validate_replay_manifest_metadata() -> None:
    with tempfile.TemporaryDirectory(prefix="huifu-replay-metadata-") as directory:
        output_dir = Path(directory)
        output = output_dir / "case-01.txt"
        output.write_text("fixture\n", encoding="utf-8")
        args = SimpleNamespace(
            suite="payment",
            load_mode="payment-only",
            model=run_real_model_regression.DEFAULT_MODEL,
            jobs=1,
            timeout=300,
            codex_executable=None,
        )
        previous_workspace_entries = run_real_model_regression.REGRESSION_WORKSPACE_ENTRIES
        previous_source_entries = run_real_model_regression.REGRESSION_SOURCE_ENTRIES
        previous_collector = run_real_model_regression.collect_source_provenance
        workspace_entries = run_real_model_regression.workspace_entries_for(args.load_mode)
        source_entries = workspace_entries + (
            "scripts/run_real_model_regression.py",
            "scripts/huifu-payment-test-prompts.json",
            "tests/regression/cross-route.json",
        )
        current = {
            "head": "a" * 40,
            "git_status": "",
            "source_sha256": "b" * 64,
            "workspace_source_sha256": "c" * 64,
        }
        try:
            run_real_model_regression.REGRESSION_WORKSPACE_ENTRIES = workspace_entries
            run_real_model_regression.REGRESSION_SOURCE_ENTRIES = source_entries
            run_real_model_regression.collect_source_provenance = lambda: current
            payload = {
                "schema_version": run_real_model_regression.RUN_MANIFEST_SCHEMA_VERSION,
                "started_at": "2026-07-24T00:00:00+08:00",
                "finished_at": "2026-07-24T00:01:00+08:00",
                "head": current["head"],
                "source_clean": True,
                "git_status": "",
                "source_sha256": current["source_sha256"],
                "source_entries": list(source_entries),
                "workspace_source_sha256": current["workspace_source_sha256"],
                "workspace_copy_sha256": current["workspace_source_sha256"],
                "workspace_entries": list(workspace_entries),
                "case_ids": [1],
                "suite": "onboarding",
                "load_mode": "onboarding-only",
                "model": args.model,
                "reasoning_effort": run_real_model_regression.DEFAULT_REASONING_EFFORT,
                "sandbox": "read-only",
                "jobs": args.jobs,
                "timeout_seconds": args.timeout,
                "codex_executable": run_real_model_regression.resolve_codex_executable(None),
                "passed": 1,
                "total": 1,
                "all_passed": True,
                "output_sha256": {
                    output.name: run_real_model_regression.sha256_file(output)
                },
            }
            (output_dir / "run-manifest.json").write_text(
                json.dumps(payload),
                encoding="utf-8",
            )
            errors = run_real_model_regression.validate_existing_run_manifest(
                output_dir,
                [run_real_model_regression.PromptCase(1, "fixture", "")],
                args,
            )
            require(
                any("manifest suite differs" in error for error in errors),
                "replay accepted a false suite declaration",
            )
            require(
                any("manifest load_mode differs" in error for error in errors),
                "replay accepted a false load_mode declaration",
            )
        finally:
            run_real_model_regression.REGRESSION_WORKSPACE_ENTRIES = (
                previous_workspace_entries
            )
            run_real_model_regression.REGRESSION_SOURCE_ENTRIES = previous_source_entries
            run_real_model_regression.collect_source_provenance = previous_collector


def validate_sensitive_patterns() -> None:
    sensitive_samples = (
        "mobile=" + "138" + "00138000",
        "cert_no=" + "310101" + "19900101" + "1234",
        "card_no=" + "622202" + "1234567890123",
        'access_token="' + "tok_live_" + "A" * 32 + '"',
        'api_key="' + "sk_live_" + "B" * 32 + '"',
        "-----BEGIN PRIVATE KEY-----",
        'huifu_id="' + "69990000" + "12345678" + '"',
    )
    for sample in sensitive_samples:
        require(
            scan_sensitive_examples.scan_text(sample),
            f"sensitive sample was not detected: {sample.split('=')[0]}",
        )
    safe_samples = (
        'access_token="<ACCESS_TOKEN>"',
        'card_no="<ENCRYPTED_CARD_NO_FROM_CLIENT>"',
        'mobile="<ENCRYPTED_MOBILE_FROM_CLIENT>"',
    )
    for sample in safe_samples:
        require(
            not scan_sensitive_examples.scan_text(sample),
            f"placeholder was incorrectly detected: {sample}",
        )


def validate_archive_name_guards() -> None:
    expect_value_error(
        lambda: validate_skill_package.validate_zip_names(
            ["skill/SKILL.md", "skill/SKILL.md"]
        ),
        "duplicate ZIP entry",
    )
    expect_value_error(
        lambda: validate_skill_package.validate_zip_names(
            ["skill/references/Guide.md", "skill/references/guide.md"]
        ),
        "case-insensitive ZIP path collision",
    )


def validate_package_manifest_allowlist() -> None:
    manifest = json.loads(
        (REPO_ROOT / "skills-manifest.json").read_text(encoding="utf-8")
    )
    for skill, spec in manifest["skills"].items():
        allowed = package_skill.package_paths(spec)
        require(f"{skill}/SKILL.md" in allowed, f"{skill}: SKILL.md absent")
        require(f"{skill}/agents/openai.yaml" in allowed, f"{skill}: agents file absent")
        for forbidden in (
            f"{skill}/references/tests/forbidden.py",
            f"{skill}/references/scripts/check.py",
            f"{skill}/references/forbidden.py",
            f"{skill}/references/nested/extra.md",
        ):
            require(forbidden not in allowed, f"package allowlist admits {forbidden}")
        require(
            allowed == validate_skill_package.package_paths(spec),
            f"{skill}: builder and validator allowlists differ",
        )


def validate_provenance_schema_guard() -> None:
    expect_value_error(
        lambda: validate_skill_package.validate_provenance_schema({}),
        "missing required provenance fields",
    )
    for lock_name in (
        "merchant-onboarding-source-lock-2026-08-31.json",
        "user-onboarding-source-lock-2026-08-31.json",
    ):
        expect_value_error(
            lambda name=lock_name: refresh_onboarding_sources.ensure_new_lock_paths(
                REPO_ROOT / "maintainer-contracts" / name
            ),
            "refusing to overwrite versioned onboarding source lock",
        )


def validate_published_version_guard() -> None:
    validate_skill_package.validate_published_version_facts(
        "| Skill 版本 | `1.3.5` |",
        "| Skill | `huifu-pay-integration 1.3.5` |",
        "huifu-pay-integration",
        "1.3.5",
    )
    expect_value_error(
        lambda: validate_skill_package.validate_published_version_facts(
            "| Skill 版本 | `9.9.9` |",
            "| Skill | `huifu-pay-integration 1.3.5` |",
            "huifu-pay-integration",
            "1.3.5",
        ),
        "SKILL.md version differs",
    )


def validate_domain_boundary_guard() -> None:
    payment_findings = validate_skill_split.domain_boundary_findings(
        "huifu-pay-integration",
        "POST /v2/merchant/basicdata/ent",
        "SKILL.md",
    )
    require(payment_findings, "payment Skill accepted an onboarding implementation endpoint")
    onboarding_findings = validate_skill_split.domain_boundary_findings(
        "huifu-merchant-onboarding",
        "POST /v2/trade/hosting/payment/preorder",
        "SKILL.md",
    )
    require(onboarding_findings, "onboarding Skill accepted a payment implementation endpoint")
    require(
        not validate_skill_split.domain_boundary_findings(
            "huifu-pay-integration",
            "商户进件完成后交接 $huifu-pay-integration。",
            "SKILL.md",
        ),
        "handoff prose must remain allowed",
    )
    require(
        validate_skill_split.domain_boundary_findings(
            "huifu-pay-integration",
            "| request.data.share_holder_info_list[].mobile_no | String | 32 | Y |",
            "references/injected.md",
        ),
        "payment Skill accepted an onboarding field-contract identifier",
    )
    require(
        validate_skill_split.domain_boundary_findings(
            "huifu-merchant-onboarding",
            "TradePaymentCreateRequest",
            "SKILL.md",
        ),
        "onboarding Skill accepted a Lightning payment implementation class",
    )
    require(
        validate_skill_split.domain_boundary_findings(
            "huifu-pay-integration",
            "V2SupplementaryPictureRequest",
            "SKILL.md",
        ),
        "payment Skill accepted an onboarding picture implementation class",
    )
    require(
        not validate_skill_split.domain_boundary_findings(
            "huifu-pay-integration",
            "不要在支付 Skill 中实现 `request.data.contact_name`；交给 $huifu-merchant-onboarding。",
            "SKILL.md",
        ),
        "explicit cross-Skill handoff prose must remain allowed",
    )


def validate_release_evidence_contract() -> None:
    release_script = (REPO_ROOT / "scripts/validate-release.sh").read_text(encoding="utf-8")
    validate_skills_sh = (REPO_ROOT / "scripts/validate-skills.sh").read_text(
        encoding="utf-8"
    )
    validate_skills_ps1 = (REPO_ROOT / "scripts/validate-skills.ps1").read_text(
        encoding="utf-8-sig"
    )
    payment_sdk_command = "scripts/validate_payment_sdk_evidence.py"
    require(
        payment_sdk_command in validate_skills_sh,
        "bash validation chain omits payment SDK evidence",
    )
    require(
        payment_sdk_command.replace("/", "\\") in validate_skills_ps1,
        "PowerShell validation chain omits payment SDK evidence",
    )
    require(
        "REQUIRE_SDK_EVIDENCE=1" in release_script
        and "scripts/validate-skills.sh" in release_script,
        "release gate does not require the SDK evidence chain",
    )
    root_guard = 'if [[ -e "$REAL_MODEL_EVIDENCE_ROOT" ]]'
    root_create = 'mkdir "$REAL_MODEL_EVIDENCE_ROOT"'
    require(root_guard in release_script, "release gate does not reject an existing evidence root")
    require(root_create in release_script, "release gate does not create evidence root atomically")
    require(
        release_script.index(root_guard) < release_script.index(root_create),
        "release evidence root is checked after creation",
    )
    for suite in validate_skill_packages.RELEASE_EVIDENCE_SUITES:
        for artifact in ("run-manifest.json", "summary.json"):
            label = f"real-model/{suite}/{artifact}"
            require(label in release_script, f"release provenance omits {label}")
    require(
        release_script.count("--skip-run") >= 4,
        "release gate does not semantically replay all four persisted model suites",
    )
    require(
        ': "${RELEASE_OUTPUT_DIR:?RELEASE_OUTPUT_DIR is required' in release_script,
        "release gate does not require a durable package output directory",
    )
    require(
        '--output-dir "$RELEASE_OUTPUT_DIR"' in release_script,
        "release gate does not preserve the evidence-bound packages",
    )
    output_guard = 'if [[ -e "$RELEASE_OUTPUT_DIR" ]]'
    require(output_guard in release_script, "release gate does not reject an existing output root")
    require(
        release_script.index(output_guard) < release_script.index(root_create),
        "release output directory is checked after long-running validation begins",
    )

    label, path = package_skill.parse_evidence_argument(
        "real-model/payment/summary.json=/tmp/evidence/payment/summary.json"
    )
    require(label == "real-model/payment/summary.json", "evidence label was rewritten")
    require(
        path == Path("/tmp/evidence/payment/summary.json"),
        "evidence path was rewritten",
    )
    expect_value_error(
        lambda: package_skill.parse_evidence_argument("../escape=/tmp/evidence.json"),
        "unsafe evidence label",
    )


def validate_python_optimization_guard() -> None:
    target = REPO_ROOT / "scripts/validate_payment_field_catalog.py"
    result = subprocess.run(
        [sys.executable, "-O", str(target)],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    require(result.returncode != 0, "optimized Python bypassed a critical validator")
    require(
        "Validation requires assertions" in result.stdout,
        f"optimized validator failed for the wrong reason: {result.stdout}",
    )
    for script_name in ("validate-skills.sh", "validate-release.sh"):
        script = (REPO_ROOT / "scripts" / script_name).read_text(encoding="utf-8")
        require(
            "PYTHONOPTIMIZE must be unset or 0" in script,
            f"{script_name} does not reject Python optimization",
        )


def validate_reproducible_provenance() -> None:
    with tempfile.TemporaryDirectory(prefix="huifu-release-guardrails-") as temp_dir:
        temp = Path(temp_dir)
        evidence_path = temp / "summary.json"
        evidence_path.write_text('{"passed": 99}\n', encoding="utf-8")

        def source_snapshot() -> str:
            digest = hashlib.sha256()
            for path in sorted((REPO_ROOT / "huifu-pay-integration").rglob("*")):
                if path.is_file():
                    digest.update(path.relative_to(REPO_ROOT).as_posix().encode())
                    digest.update(path.read_bytes())
            digest.update(
                subprocess.check_output(
                    ["git", "status", "--porcelain=v1"],
                    cwd=REPO_ROOT,
                )
            )
            return digest.hexdigest()

        outputs: list[Path] = []
        for attempt in range(3):
            outputs = []
            before = source_snapshot()
            for label in ("a", "b"):
                output = temp / f"{attempt}-{label}"
                subprocess.run(
                    [
                        sys.executable,
                        str(REPO_ROOT / "scripts/package_skill.py"),
                        "--skill",
                        "huifu-pay-integration",
                        "--output-dir",
                        str(output),
                        "--allow-dirty",
                        "--evidence",
                        f"real-model/all/summary.json={evidence_path}",
                    ],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
                outputs.append(
                    output / f"huifu-pay-integration-{run_real_model_regression.PAYMENT_SKILL_VERSION}.provenance.json"
                )
            if before == source_snapshot():
                break
        else:
            raise AssertionError("repository changed during three reproducibility attempts")
        require(
            outputs[0].read_bytes() == outputs[1].read_bytes(),
            "identical inputs produced different provenance sidecars",
        )
        payload = json.loads(outputs[0].read_text(encoding="utf-8"))
        validate_skill_package.validate_provenance_schema(payload)
        manifest = json.loads(
            (REPO_ROOT / "skills-manifest.json").read_text(encoding="utf-8")
        )
        payment_spec = manifest["skills"]["huifu-pay-integration"]
        validate_skill_package.validate_refresh_source_bindings(payload, payment_spec)
        require(payload["schema_version"] == 3, "provenance schema 3 missing")
        require(
            payload["refresh_id"] == json.loads((REPO_ROOT / payment_spec["refresh_contract"]).read_text())["refresh_id"],
            "refresh ID was not bound to provenance",
        )
        require(
            payload["refresh_contract"]
            == payment_spec["refresh_contract"],
            "refresh contract path was not bound to provenance",
        )
        require(
            set(payload["source_locks"])
            == {payment_spec["source_lock"], payment_spec["sdk_source_lock"]},
            "payment source lock was not bound to provenance",
        )
        tampered_refresh = json.loads(json.dumps(payload))
        tampered_refresh["refresh_id"] = "api-refresh-tampered"
        expect_value_error(
            lambda: validate_skill_package.validate_refresh_source_bindings(
                tampered_refresh, payment_spec
            ),
            "refresh ID differs",
        )
        tampered_lock = json.loads(json.dumps(payload))
        tampered_lock["source_locks"][
            "maintainer-contracts/payment-source-lock-2026-08-31.json"
        ] = "0" * 64
        expect_value_error(
            lambda: validate_skill_package.validate_refresh_source_bindings(
                tampered_lock, payment_spec
            ),
            "source-lock map differs",
        )
        require(payload["build"]["builder"] == "scripts/package_skill.py", "builder missing")
        require(payload["build"]["timestamp_source"] == "git-commit", "timestamp source missing")
        require(
            payload["test_evidence"]
            == {"real-model/all/summary.json": hashlib.sha256(evidence_path.read_bytes()).hexdigest()},
            "labeled external evidence was not bound to provenance",
        )
        archive = outputs[0].parent / f"huifu-pay-integration-{run_real_model_regression.PAYMENT_SKILL_VERSION}.zip"
        validate_command = [
            sys.executable,
            str(REPO_ROOT / "scripts/validate_skill_package.py"),
            "--skill",
            "huifu-pay-integration",
            "--archive",
            str(archive),
            "--allow-dirty-provenance",
        ]
        subprocess.run(
            validate_command,
            cwd=REPO_ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(archive, "a") as package:
                original = package.read("huifu-pay-integration/SKILL.md")
                package.writestr("huifu-pay-integration/SKILL.md", original)
        duplicate_result = subprocess.run(
            validate_command,
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        require(duplicate_result.returncode != 0, "duplicate ZIP entry passed CLI validation")
        require(
            "duplicate ZIP entry" in duplicate_result.stdout,
            f"duplicate ZIP failed for the wrong reason: {duplicate_result.stdout}",
        )


def validate_external_model_evidence_path() -> None:
    workspace = Path("/isolated/workspace")
    external_output = Path("/external/evidence/payment/case-01.txt")
    actual = run_real_model_regression.workspace_model_output_path(
        workspace,
        external_output,
    )
    require(
        actual == workspace / ".real-model-output/case-01.txt",
        f"external evidence path was not mapped into workspace: {actual}",
    )
    require(
        run_real_model_regression.display_evidence_path(external_output)
        == str(external_output),
        "external evidence display path was rejected or rewritten",
    )
    case = run_real_model_regression.PromptCase(
        case_id=1,
        prompt="infrastructure fixture",
        expected="",
    )
    blocked = run_real_model_regression.evaluate_case(
        case,
        "[returncode] 1\n[stderr]\nERROR: You've hit your usage limit.",
        external_output,
        1,
        "payment-only",
    )
    require(
        run_real_model_regression.is_infrastructure_blocked(blocked),
        "usage-limit output was misclassified as a content failure",
    )
    require(
        not blocked.missing and not blocked.forbidden_hits,
        "infrastructure failure generated content-evaluation noise",
    )
    for message in (
        "authorize_stat 支持 AUTHORIZED、UNAUTHORIZED。",
        "接口返回 authentication failed；请核对网关凭据。",
        "遇到 rate limit 时按接口规则处理。",
    ):
        require(
            run_real_model_regression.detect_infrastructure_failure(message, 0) is None,
            "successful business answer was misclassified as model infrastructure failure",
        )
    for message, label in (
        ("ERROR: authentication failed", "authentication"),
        ("ERROR: rate limit exceeded", "rate-limit"),
    ):
        require(
            run_real_model_regression.detect_infrastructure_failure(message, 1) == label,
            "real model CLI failure was not detected",
        )


def main() -> int:
    checks = (
        validate_sensitive_patterns,
        validate_markdown_table_parsers,
        validate_onboarding_route_contract,
        validate_archive_name_guards,
        validate_package_manifest_allowlist,
        validate_provenance_schema_guard,
        validate_published_version_guard,
        validate_domain_boundary_guard,
        validate_release_evidence_contract,
        validate_python_optimization_guard,
        validate_release_evidence_profile,
        validate_replay_manifest_metadata,
        validate_reproducible_provenance,
        validate_external_model_evidence_path,
    )
    for check in checks:
        check()
        print(f"PASS {check.__name__}")
    print(f"release guardrail regression passed: {len(checks)} checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
