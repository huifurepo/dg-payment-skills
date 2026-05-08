from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_SKILL_DIR = REPO_ROOT / "huifu-pay-integration"
EXPECTED_SKILL_FILE = EXPECTED_SKILL_DIR / "SKILL.md"
SKILL_FILES = sorted(REPO_ROOT.glob("*/SKILL.md"))
EXPECTED_OPENAI_YAML = EXPECTED_SKILL_DIR / "agents" / "openai.yaml"
EXPECTED_SKILL_TOP_LEVEL = {"SKILL.md", "agents", "references"}
EXPECTED_REFERENCES = {
    "aggregation-async-webhook.md",
    "shared-overview.md",
    "shared-signing-v2.md",
    "shared-async-notify.md",
    "shared-credential-boundary.md",
    "shared-copyright-notice.md",
    "shared-request-header-policy.md",
    "shared-server-sdk-matrix.md",
    "shared-frontend-sdk-matrix.md",
    "shared-versioning-policy.md",
    "shared-release-checklist.md",
    "aggregation-base.md",
    "aggregation-quickstart.md",
    "aggregation-common-params.md",
    "aggregation-customer-preparation.md",
    "aggregation-error-codes.md",
    "aggregation-faq.md",
    "aggregation-payload-construction.md",
    "aggregation-java-adapter.md",
    "aggregation-java-sdk-quickstart.md",
    "aggregation-java-tech-spec.md",
    "aggregation-php-adapter.md",
    "aggregation-order.md",
    "aggregation-order-quickstart.md",
    "aggregation-order-request.md",
    "aggregation-order-response.md",
    "aggregation-order-errors.md",
    "aggregation-order-tx-metadata.md",
    "aggregation-order-method-wechat.md",
    "aggregation-order-method-alipay.md",
    "aggregation-order-method-unionpay.md",
    "aggregation-query.md",
    "aggregation-query-quickstart.md",
    "aggregation-query-payment-query.md",
    "aggregation-query-trade-close.md",
    "aggregation-query-close-query.md",
    "aggregation-query-reconciliation.md",
    "aggregation-query-php-scenarios.md",
    "aggregation-refund.md",
    "aggregation-refund-quickstart.md",
    "aggregation-refund-query.md",
    "hostingpay-base.md",
    "hostingpay-quickstart.md",
    "hostingpay-async-webhook.md",
    "hostingpay-common-params.md",
    "hostingpay-customer-preparation.md",
    "hostingpay-error-codes.md",
    "hostingpay-faq.md",
    "hostingpay-payload-construction.md",
    "hostingpay-java-adapter.md",
    "hostingpay-java-sdk-quickstart.md",
    "hostingpay-java-tech-spec.md",
    "hostingpay-php-adapter.md",
    "hostingpay-preorder.md",
    "hostingpay-preorder-quickstart.md",
    "hostingpay-preorder-h5-pc.md",
    "hostingpay-preorder-h5-pc-request.md",
    "hostingpay-preorder-h5-pc-response.md",
    "hostingpay-preorder-h5-pc-response-channel.md",
    "hostingpay-preorder-h5-pc-channel.md",
    "hostingpay-preorder-h5-pc-errors.md",
    "hostingpay-preorder-alipay-mini.md",
    "hostingpay-preorder-wechat-mini.md",
    "hostingpay-preorder-php-scenarios.md",
    "hostingpay-query.md",
    "hostingpay-query-quickstart.md",
    "hostingpay-query-payment-status-query.md",
    "hostingpay-query-trade-close.md",
    "hostingpay-query-reconciliation.md",
    "hostingpay-query-php-scenarios.md",
    "hostingpay-refund.md",
    "hostingpay-refund-quickstart.md",
    "hostingpay-refund-query.md",
    "hostingpay-refund-php-scenarios.md",
    "checkout-js.md",
    "checkout-js-readme.md",
    "checkout-js-integration-flow.md",
    "checkout-js-create-preorder-contract.md",
    "checkout-js-component-modes.md",
    "checkout-js-callback-and-confirmation.md",
    "checkout-js-framework-integration-notes.md",
}
ALLOWED_TOP_LEVEL_KEYS = {
    "name",
    "description",
}
NAME_PATTERN = re.compile(r"^(?!-)(?!.*--)[a-z0-9-]{1,64}(?<!-)$")
MD_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?!https?://)(?!#)([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`\n]+)`")
SKIP_PARTS = {".git", ".tmp", ".worktrees", ".codex-tasks", "node_modules", "docs"}
MIN_SHORT_DESCRIPTION_LENGTH = 25
MAX_SHORT_DESCRIPTION_LENGTH = 64
MAX_SKILL_REFERENCE_MENTIONS = 40
LONG_REFERENCE_TOC_LINE_LIMIT = 100
LOCAL_PATH_PREFIXES = ("references/", "agents/", "scripts/")


@dataclass
class ValidationState:
    errors: int = 0
    warnings: int = 0

    def ok(self, message: str) -> None:
        print(f"✅ OK:    {message}")

    def warning(self, message: str) -> None:
        print(f"⚠️ WARN:  {message}")
        self.warnings += 1

    def error(self, message: str) -> None:
        print(f"❌ ERROR: {message}")
        self.errors += 1
