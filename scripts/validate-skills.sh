#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${PYTHONOPTIMIZE:-}" && "${PYTHONOPTIMIZE}" != "0" ]]; then
  echo "PYTHONOPTIMIZE must be unset or 0 for validation." >&2
  exit 2
fi
export PYTHONOPTIMIZE=0

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

python3 -B scripts/validate_skill_split.py
python3 -B scripts/validate_skills.py
python3 -B scripts/validate_regression_reference_ownership.py
python3 -B scripts/validate_aggregation_payload_contract.py
python3 -B scripts/validate_request_field_preservation.py
python3 -B scripts/validate_code_examples.py
python3 -B scripts/scan_sensitive_examples.py
python3 -B scripts/validate_release_guardrails.py
python3 -B scripts/generate_payment_source_index.py --check
python3 -B scripts/validate_payment_source_contract.py
python3 -B scripts/validate_payment_review_contract.py
python3 -B scripts/generate_payment_field_catalog.py --check
python3 -B scripts/validate_payment_field_catalog.py
python3 -B scripts/validate_onboarding_source_refresh.py
python3 -B scripts/generate_merchant_onboarding_field_catalog.py \
  --locked-source-dir \
  --output huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md \
  --check
python3 -B scripts/validate_merchant_onboarding_field_catalog_generation.py
python3 -B scripts/validate_merchant_onboarding_complete_catalog.py
python3 -B scripts/validate_merchant_onboarding_source_contract.py
python3 -B scripts/validate_merchant_onboarding_field_contract.py
python3 -B scripts/validate_skill_packages.py --allow-dirty

(cd local-sandbox && go test ./... -count=1)

if [[ -n "${HUIFU_SDK_ROOT:-}" ]]; then
  python3 -B scripts/validate_merchant_onboarding_sdk_evidence.py --sdk-root "$HUIFU_SDK_ROOT"
  python3 -B scripts/validate_local_sandbox_golden_vectors.py --strict --sdk-root "$HUIFU_SDK_ROOT"
elif [[ "${REQUIRE_SDK_EVIDENCE:-0}" == "1" ]]; then
  echo "HUIFU_SDK_ROOT is required when REQUIRE_SDK_EVIDENCE=1." >&2
  exit 2
else
  echo "Skipping SDK source and golden-vector evidence validation; set HUIFU_SDK_ROOT in CI/release validation."
fi

if [[ "${RUN_REAL_MODEL_REGRESSION:-0}" == "1" ]]; then
  regression_args=(scripts/run_real_model_regression.py --timeout "${REAL_MODEL_TIMEOUT:-300}")
  if [[ "${REAL_MODEL_SMOKE:-0}" == "1" ]]; then
    regression_args+=(--smoke)
  fi
  if [[ -n "${CODEX_EXECUTABLE:-}" ]]; then
    regression_args+=(--codex-executable "$CODEX_EXECUTABLE")
  fi
  if [[ -n "${REAL_MODEL_MODEL:-}" ]]; then
    regression_args+=(--model "$REAL_MODEL_MODEL")
  fi
  python3 -B "${regression_args[@]}"
fi
