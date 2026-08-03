#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${PYTHONOPTIMIZE:-}" && "${PYTHONOPTIMIZE}" != "0" ]]; then
  echo "PYTHONOPTIMIZE must be unset or 0 for release validation." >&2
  exit 2
fi
export PYTHONOPTIMIZE=0

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

: "${HUIFU_SDK_ROOT:?HUIFU_SDK_ROOT is required for release validation}"
: "${REAL_MODEL_EVIDENCE_ROOT:?REAL_MODEL_EVIDENCE_ROOT is required for the 115-case release evidence}"
: "${RELEASE_OUTPUT_DIR:?RELEASE_OUTPUT_DIR is required for durable release packages}"

if [[ -e "$RELEASE_OUTPUT_DIR" ]]; then
  echo "Release output directory must not already exist: $RELEASE_OUTPUT_DIR" >&2
  exit 2
fi
if [[ -e "$REAL_MODEL_EVIDENCE_ROOT" ]]; then
  echo "Real-model evidence root must not already exist: $REAL_MODEL_EVIDENCE_ROOT" >&2
  exit 2
fi
mkdir "$REAL_MODEL_EVIDENCE_ROOT"

REQUIRE_SDK_EVIDENCE=1 RUN_REAL_MODEL_REGRESSION=0 scripts/validate-skills.sh
python3 -B scripts/run_real_model_regression.py --validate-rules-only

regression_common_args=(
  scripts/run_real_model_regression.py
  --timeout "${REAL_MODEL_TIMEOUT:-300}"
  --jobs "${REAL_MODEL_JOBS:-2}"
)
if [[ -n "${CODEX_EXECUTABLE:-}" ]]; then
  regression_common_args+=(--codex-executable "$CODEX_EXECUTABLE")
fi
if [[ -n "${REAL_MODEL_MODEL:-}" ]]; then
  regression_common_args+=(--model "$REAL_MODEL_MODEL")
fi

run_release_suite() {
  local suite="$1"
  local load_mode="$2"
  local output_dir="$REAL_MODEL_EVIDENCE_ROOT/$suite"
  if [[ -e "$output_dir" ]]; then
    echo "Real-model evidence directory already exists: $output_dir" >&2
    return 2
  fi
  python3 -B "${regression_common_args[@]}" \
    --suite "$suite" \
    --load-mode "$load_mode" \
    --output-dir "$output_dir"
}

run_release_suite payment payment-only
run_release_suite onboarding onboarding-only
run_release_suite cross-route both

# Re-evaluate the exact persisted outputs and validate source commit, clean
# state, suite/load-mode case sets, per-case digests and final pass counts.
python3 -B "${regression_common_args[@]}" --suite payment --load-mode payment-only \
  --output-dir "$REAL_MODEL_EVIDENCE_ROOT/payment" --skip-run
python3 -B "${regression_common_args[@]}" --suite onboarding --load-mode onboarding-only \
  --output-dir "$REAL_MODEL_EVIDENCE_ROOT/onboarding" --skip-run
python3 -B "${regression_common_args[@]}" --suite cross-route --load-mode both \
  --output-dir "$REAL_MODEL_EVIDENCE_ROOT/cross-route" --skip-run

release_evidence=(
  --evidence "real-model/payment/run-manifest.json=$REAL_MODEL_EVIDENCE_ROOT/payment/run-manifest.json"
  --evidence "real-model/payment/summary.json=$REAL_MODEL_EVIDENCE_ROOT/payment/summary.json"
  --evidence "real-model/onboarding/run-manifest.json=$REAL_MODEL_EVIDENCE_ROOT/onboarding/run-manifest.json"
  --evidence "real-model/onboarding/summary.json=$REAL_MODEL_EVIDENCE_ROOT/onboarding/summary.json"
  --evidence "real-model/cross-route/run-manifest.json=$REAL_MODEL_EVIDENCE_ROOT/cross-route/run-manifest.json"
  --evidence "real-model/cross-route/summary.json=$REAL_MODEL_EVIDENCE_ROOT/cross-route/summary.json"
)
python3 -B scripts/validate_skill_packages.py \
  --output-dir "$RELEASE_OUTPUT_DIR" \
  "${release_evidence[@]}"
