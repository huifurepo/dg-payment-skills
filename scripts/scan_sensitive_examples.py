#!/usr/bin/env python3
"""Fail if merchant-onboarding guidance contains credential or real-looking PII material."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERAL_TARGETS = [
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "huifu-pay-integration" / "SKILL.md",
    ROOT / "scripts" / "huifu-payment-test-prompts.json",
    ROOT / "scripts" / "run_real_model_regression.py",
    *sorted((ROOT / "huifu-pay-integration" / "references").glob("*.md")),
]
ONBOARDING_TARGETS = [
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "huifu-pay-integration" / "SKILL.md",
    ROOT / "scripts" / "huifu-payment-test-prompts.json",
    ROOT / "scripts" / "run_real_model_regression.py",
    *sorted((ROOT / "huifu-pay-integration" / "references").glob("merchant-onboarding-*.md")),
]
GENERAL_PATTERNS = (
    (re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----"), "PEM private key marker"),
    (re.compile(r"MIIE(?:vg|ow)[A-Za-z0-9+/=]{80,}"), "PKCS8 private-key-like blob"),
    (re.compile(r"(?i)(?:rsa_)?private[_-]?key\s*[:=]\s*[\"'][^\"']{32,}"), "inline private key assignment"),
)
ONBOARDING_PATTERNS = (
    (re.compile(r"https?://[^\s`\"')]+(?:idcard|bankcard|identity|license|身份证|银行卡)[^\s`\"')]*", re.I), "sensitive material URL"),
    (re.compile(r"https?://[^\s`\"')]+\.(?:jpe?g|png|bmp)(?:[?#][^\s`\"')]*)?", re.I), "image URL"),
    (re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "mainland mobile number"),
    (re.compile(r"(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[0-9Xx](?![0-9Xx])"), "mainland identity number"),
    (re.compile(r"(?<!\d)\d{16,32}(?!\d)"), "long merchant/card/production identifier"),
)


def matching_label(line: str, patterns: tuple[tuple[re.Pattern[str], str], ...]) -> str | None:
    for pattern, label in patterns:
        if pattern.search(line):
            return label
    return None


def validate_patterns() -> list[str]:
    detection_samples = {
        "merchant number": "huifu_id=" + "66660001" + "04778898",
        "phone": "mobile=" + "138" + "00138000",
        "identity": "cert_no=" + "310101" + "19900101" + "1234",
        "bank card": "card_no=" + "622202" + "1234567890123",
        "production sequence": "req_seq_id=" + "20260713" + "12345678901234567890",
        "image URL": "https://merchant.invalid/material/license." + "png",
    }
    safe_samples = (
        "huifu_id String(18) Y",
        "req_date String(8) yyyyMMdd",
        "https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json",
        "file_url 与 file 互斥",
    )
    errors = [
        f"self-test did not detect {name}"
        for name, sample in detection_samples.items()
        if matching_label(sample, ONBOARDING_PATTERNS) is None
    ]
    errors.extend(
        f"self-test false positive: {sample}"
        for sample in safe_samples
        if matching_label(sample, ONBOARDING_PATTERNS) is not None
    )
    return errors


def main() -> int:
    findings = validate_patterns()
    for path in GENERAL_TARGETS:
        if not path.exists():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            label = matching_label(line, GENERAL_PATTERNS)
            if label:
                findings.append(f"{path.relative_to(ROOT)}:{number}: {label}")
    for path in ONBOARDING_TARGETS:
        if not path.exists():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            label = matching_label(line, ONBOARDING_PATTERNS)
            if label:
                findings.append(f"{path.relative_to(ROOT)}:{number}: {label}")
    if findings:
        print("Sensitive example scan failed; rotate/remove the source material before release.")
        print("\n".join(findings))
        return 1
    checked = len(set(GENERAL_TARGETS + ONBOARDING_TARGETS))
    print(f"Sensitive example scan passed: {checked} files checked; detector self-test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
