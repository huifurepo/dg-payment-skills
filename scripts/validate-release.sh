#!/usr/bin/env bash
set -euo pipefail

: "${HUIFU_SDK_ROOT:?HUIFU_SDK_ROOT is required for release validation}"
REQUIRE_SDK_EVIDENCE=1 "$(dirname "$0")/validate-skills.sh"
python3 "$(dirname "$0")/run_real_model_regression.py" --validate-rules-only
