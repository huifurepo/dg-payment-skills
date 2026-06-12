param(
    [switch]$RunRealModelRegression,
    [switch]$Smoke,
    [string]$CodexExecutable,
    [string]$Model,
    [int]$Timeout = 300
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

function Invoke-Validation {
    param([string[]]$Arguments)
    & python -B @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Invoke-Validation @("scripts\validate_skills.py")
Invoke-Validation @("scripts\validate_aggregation_payload_contract.py")
Invoke-Validation @("scripts\validate_request_field_preservation.py")
Invoke-Validation @("scripts\validate_code_examples.py")

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
