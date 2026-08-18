param(
    [switch]$RunRealModelRegression,
    [switch]$Smoke,
    [string]$CodexExecutable,
    [string]$Model,
    [int]$Timeout = 300
)

$ErrorActionPreference = "Stop"

if ($env:PYTHONOPTIMIZE -and $env:PYTHONOPTIMIZE -ne "0") {
    throw "PYTHONOPTIMIZE must be unset or 0 for validation."
}
$env:PYTHONOPTIMIZE = "0"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

function Invoke-Validation {
    param([string[]]$Arguments)
    & python -B @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Invoke-Validation @("scripts\validate_skill_split.py")
Invoke-Validation @("scripts\validate_skills.py")
Invoke-Validation @("scripts\validate_regression_reference_ownership.py")
Invoke-Validation @("scripts\validate_aggregation_payload_contract.py")
Invoke-Validation @("scripts\validate_request_field_preservation.py")
# Windows process startup and antivirus scanning can make the 60 PHP lint/run
# subprocesses exceed the cross-platform 300s aggregate budget. Keep the
# per-command 10s timeout unchanged, but give this Windows-only gate enough
# aggregate time to finish every example instead of reporting partial success.
Invoke-Validation @("scripts\validate_code_examples.py", "--timeout", "600")
Invoke-Validation @("scripts\scan_sensitive_examples.py")
Invoke-Validation @("scripts\validate_release_guardrails.py")
Invoke-Validation @("scripts\generate_payment_source_index.py", "--check")
Invoke-Validation @("scripts\validate_payment_source_contract.py")
Invoke-Validation @("scripts\validate_payment_review_contract.py")
Invoke-Validation @("scripts\generate_payment_field_catalog.py", "--check")
Invoke-Validation @("scripts\validate_payment_field_catalog.py")
Invoke-Validation @("scripts\validate_onboarding_source_refresh.py")
Invoke-Validation @(
    "scripts\generate_merchant_onboarding_field_catalog.py",
    "--locked-source-dir",
    "--output", "huifu-merchant-onboarding\references\merchant-onboarding-complete-field-catalog.md",
    "--check"
)
Invoke-Validation @("scripts\validate_merchant_onboarding_field_catalog_generation.py")
Invoke-Validation @("scripts\validate_merchant_onboarding_complete_catalog.py")
Invoke-Validation @("scripts\validate_merchant_onboarding_source_contract.py")
Invoke-Validation @("scripts\validate_merchant_onboarding_field_contract.py")
Invoke-Validation @(
    "scripts\generate_user_onboarding_field_catalog.py",
    "--locked-source-dir",
    "--output", "huifu-merchant-onboarding\references\user-onboarding-complete-field-catalog.md",
    "--check"
)
Invoke-Validation @("scripts\validate_user_onboarding_source_contract.py")
Invoke-Validation @("scripts\validate_skill_packages.py", "--allow-dirty")

Push-Location (Join-Path $RepoRoot "local-sandbox")
try {
    & go test ./... -count=1
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
}

if ($env:HUIFU_SDK_ROOT) {
    Invoke-Validation @("scripts\validate_merchant_onboarding_sdk_evidence.py", "--sdk-root", $env:HUIFU_SDK_ROOT)
    Invoke-Validation @("scripts\validate_user_onboarding_sdk_evidence.py", "--sdk-root", $env:HUIFU_SDK_ROOT)
    Invoke-Validation @("scripts\validate_local_sandbox_golden_vectors.py", "--strict", "--sdk-root", $env:HUIFU_SDK_ROOT)
} elseif ($env:REQUIRE_SDK_EVIDENCE -eq "1") {
    throw "HUIFU_SDK_ROOT is required when REQUIRE_SDK_EVIDENCE=1."
} else {
    Write-Host "Skipping SDK source and golden-vector evidence validation; set HUIFU_SDK_ROOT in CI/release validation."
}

if ($RunRealModelRegression) {
    $RegressionArgs = @("scripts\run_real_model_regression.py", "--timeout", "$Timeout")
    if ($Smoke) {
        $RegressionArgs += "--smoke"
    }
    if ($CodexExecutable) {
        $RegressionArgs += @("--codex-executable", $CodexExecutable)
    }
    if ($Model) {
        $RegressionArgs += @("--model", $Model)
    }
    Invoke-Validation $RegressionArgs
}
