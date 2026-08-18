#!/usr/bin/env python3
"""Fail if any published Skill file contains credentials or real-looking PII."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOTS = tuple(
    ROOT / spec["root"]
    for spec in json.loads((ROOT / "skills-manifest.json").read_text(encoding="utf-8"))[
        "skills"
    ].values()
)
PUBLISHED_TARGETS = [
    path
    for skill_root in SKILL_ROOTS
    for path in sorted(skill_root.rglob("*"))
    if path.is_file()
]
REPOSITORY_SUPPORT_TARGETS = [
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "scripts" / "huifu-payment-test-prompts.json",
    ROOT / "scripts" / "run_real_model_regression.py",
]
SCAN_TARGETS = sorted(set(PUBLISHED_TARGETS + REPOSITORY_SUPPORT_TARGETS))

SENSITIVE_PATTERNS = (
    (re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----"), "PEM private key marker"),
    (re.compile(r"MIIE(?:vg|ow)[A-Za-z0-9+/=]{80,}"), "PKCS8 private-key-like blob"),
    (re.compile(r"(?i)(?:rsa_)?private[_-]?key\s*[:=]\s*[\"'][^\"']{32,}"), "inline private key assignment"),
    (
        re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret)"
            r"\s*[:=]\s*[\"'](?![<{][$A-Z_]*[}>])[^\"']{16,}"
        ),
        "inline API credential assignment",
    ),
    (re.compile(r"https?://[^\s`\"')]+(?:idcard|bankcard|identity|license|身份证|银行卡)[^\s`\"')]*", re.I), "sensitive material URL"),
    (re.compile(r"https?://[^\s`\"')]+\.(?:jpe?g|png|bmp)(?:[?#][^\s`\"')]*)?", re.I), "image URL"),
    (re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "mainland mobile number"),
    (re.compile(r"(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[0-9Xx](?![0-9Xx])"), "mainland identity number"),
    (
        re.compile(
            r"(?i)(?:card_no|bank_card_no|bankcard)\s*[\"']?\s*[:=]\s*[\"']?"
            r"(?<!\d)\d{12,32}(?!\d)"
        ),
        "bank-card-like value",
    ),
)
REVIEWED_NORMATIVE_IMAGE_URLS = frozenset(
    {
        "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/"
        "%E6%B5%8F%E8%A7%88%E5%99%A8%E5%85%81%E8%AE%B8%E5%BC%B9%E7%AA%97"
        "%E9%85%8D%E7%BD%AE.png",
        "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/"
        "%E6%94%AF%E4%BB%98%E6%89%98%E7%AE%A1%E5%BA%94%E7%94%A8ID.png",
    }
)
MERCHANT_IDENTIFIER_PATTERNS = (
    re.compile(
        r"(?i)(?<![A-Za-z0-9_])"
        r"(?:huifu_id|merchant_id|mer_id|atu_sub_mer_id)"
        r"[\"']?\s*(?:[:=]|=>)\s*[\"']?([0-9]{16,32})(?!\d)"
    ),
    re.compile(
        r"(?i)(?<![A-Za-z0-9_])sys_id(?![A-Za-z0-9_])"
        r"[^\n]{0,160}(?:示例值|example)[^\n0-9]{0,40}([0-9]{16,32})(?!\d)"
    ),
)
# SHA-256 only: reviewed official/demo identifiers stay auditable without
# duplicating the identifier values in validation source or failure output.
REVIEWED_MERCHANT_IDENTIFIER_SHA256 = frozenset(
    {
        "0658d01f14cffd4b20de655eb084266ec0e90602761c0747ee5a5a370fe2ac2b",
        "1e0aa5ebc7b248b2742d94f2d25d30bbd8f0db02fe433e1f23970738b8825d34",
        "6fd6174ee4ac2445c1b1faaeceaf869fbf62986a73774503f780aac723778f88",
        "7c171e9a0f5718177a7a1f8b61c6f2f217faf9778186719ab130ffaff7422e2b",
        "a692677d34f77fe40bc675f500cf46b892de2b2dc420ba7254517857cab88ead",
        "a7b28b86e60762ff977f19e5ce3f44ce24a568845c1b0c6aaee922ecee332188",
        "b27d8f337762f11a4e026e3c884e288d1713c0ad5ce12dd16b1b02a05b60b550",
        "fa71bcb3e40e94bee0258ea84909b9dfd81cd849e8658b0da597f9a718017177",
    }
)


def matching_label(line: str, patterns: tuple[tuple[re.Pattern[str], str], ...]) -> str | None:
    for pattern, label in patterns:
        if pattern.search(line):
            return label
    return None


def merchant_identifier_digests(text: str) -> set[str]:
    normalized = text.replace(r"\"", '"')
    return {
        hashlib.sha256(match.group(1).encode("ascii")).hexdigest()
        for pattern in MERCHANT_IDENTIFIER_PATTERNS
        for match in pattern.finditer(normalized)
    }


def scan_text(text: str) -> list[str]:
    """Return all sensitive-pattern labels found in a text fragment."""
    labels: list[str] = []
    for pattern, label in SENSITIVE_PATTERNS:
        matches = tuple(pattern.finditer(text))
        if not matches:
            continue
        if label == "image URL" and all(
            match.group(0) in REVIEWED_NORMATIVE_IMAGE_URLS
            for match in matches
        ):
            continue
        labels.append(label)
    unknown_identifiers = (
        merchant_identifier_digests(text) - REVIEWED_MERCHANT_IDENTIFIER_SHA256
    )
    if unknown_identifiers:
        labels.append("unreviewed merchant identifier")
    return labels


def validate_patterns() -> list[str]:
    detection_samples = {
        "phone": "mobile=" + "138" + "00138000",
        "identity": "cert_no=" + "310101" + "19900101" + "1234",
        "bank card": "card_no=" + "622202" + "1234567890123",
        "image URL": "https://merchant.invalid/material/license." + "png",
        "signed normative image": sorted(REVIEWED_NORMATIVE_IMAGE_URLS)[0]
        + "?Signature=temporary",
        "API token": 'access_token="' + "tok_live_" + "A" * 32 + '"',
        "private key": "-----BEGIN PRIVATE KEY-----",
        "unknown merchant identifier": 'huifu_id="' + "69990000" + "12345678" + '"',
    }
    safe_samples = (
        "huifu_id String(18) Y",
        "req_date String(8) yyyyMMdd",
        "https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json",
        *REVIEWED_NORMATIVE_IMAGE_URLS,
        "file_url 与 file 互斥",
        'access_token="<ACCESS_TOKEN>"',
        'card_no="<ENCRYPTED_CARD_NO_FROM_CLIENT>"',
    )
    errors = [
        f"self-test did not detect {name}"
        for name, sample in detection_samples.items()
        if not scan_text(sample)
    ]
    errors.extend(
        f"self-test false positive: {sample}"
        for sample in safe_samples
        if scan_text(sample)
    )
    return errors


def main() -> int:
    findings = validate_patterns()
    observed_reviewed_identifiers: set[str] = set()
    for path in SCAN_TARGETS:
        if not path.exists():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            observed_reviewed_identifiers.update(
                merchant_identifier_digests(line)
                & REVIEWED_MERCHANT_IDENTIFIER_SHA256
            )
            for label in scan_text(line):
                findings.append(f"{path.relative_to(ROOT)}:{number}: {label}")
    stale_allowlist = (
        REVIEWED_MERCHANT_IDENTIFIER_SHA256 - observed_reviewed_identifiers
    )
    if stale_allowlist:
        findings.append(
            "reviewed merchant identifier allowlist has "
            f"{len(stale_allowlist)} stale digest(s); re-review the published examples"
        )
    if findings:
        print("Sensitive example scan failed; rotate/remove the source material before release.")
        print("\n".join(findings))
        return 1
    print(
        "Sensitive example scan passed: "
        f"{len(SCAN_TARGETS)} files checked "
        f"({len(PUBLISHED_TARGETS)} published Skill files); detector self-test passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
