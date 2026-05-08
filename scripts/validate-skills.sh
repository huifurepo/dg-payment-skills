#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

python3 -B scripts/validate_skills.py
python3 -B scripts/validate_code_examples.py

if [[ "${RUN_REAL_MODEL_REGRESSION:-0}" == "1" ]]; then
  python3 -B scripts/run_real_model_regression.py
fi
