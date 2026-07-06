#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path


CONTRACT_BUNDLE = "huifu-pay-integration-1.3.0-r4"
SAMPLE_SCHEMA_VERSION = "1.0"
SAMPLE_IMPORTER_VERSION = "1.0"
SOURCE_TYPES = {"deidentified_production", "deidentified_joint_debug"}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(access[_-]?token|api[_-]?key|secret|password)\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"[?&](token|secret|key|password)=", re.I),
)
PHONE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
ID_CARD_PATTERN = re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)")
URL_PATTERN = re.compile(r"https?://([^/\s\"']+)", re.I)
ALLOWED_SAMPLE_HOSTS = {"localhost", "127.0.0.1", "::1", "example.invalid", "sandbox.local"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deidentified local-sandbox sample packs.")
    parser.add_argument("--sample-pack", default="local-sandbox/sample-packs/huifu-pay-integration-1.3.0-r4")
    parser.add_argument("--contract-dir", default="local-sandbox/contracts/huifu-pay-integration-1.3.0-r4")
    parser.add_argument("--require-samples", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sample_pack = resolve(repo_root, args.sample_pack)
    contract_dir = resolve(repo_root, args.contract_dir)
    result = validate_sample_pack(sample_pack, contract_dir, require_samples=args.require_samples)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


def validate_sample_pack(sample_pack: Path, contract_dir: Path, *, require_samples: bool = False) -> dict[str, object]:
    problems: list[str] = []
    warnings: list[str] = []
    manifest_path = sample_pack / "manifest.json"
    if not manifest_path.is_file():
        return failure([f"sample pack manifest missing: {manifest_path}"])
    manifest = read_json(manifest_path, problems)
    if manifest.get("contract_bundle") != CONTRACT_BUNDLE:
        problems.append("sample manifest contract_bundle mismatch")
    if manifest.get("sample_schema_version") != SAMPLE_SCHEMA_VERSION:
        problems.append("sample manifest sample_schema_version mismatch")
    if manifest.get("sample_importer_version") != SAMPLE_IMPORTER_VERSION:
        problems.append("sample manifest sample_importer_version mismatch")
    if not (sample_pack / "sample.schema.json").is_file():
        problems.append("sample.schema.json missing")
    endpoints = load_endpoints(contract_dir, problems)
    scenario_ids = load_scenario_ids(contract_dir, problems)

    samples_dir = sample_pack / "samples"
    sample_files = sorted(path for path in samples_dir.glob("*.json") if path.is_file()) if samples_dir.is_dir() else []
    manifest_samples = manifest.get("samples", [])
    if manifest_samples and len(manifest_samples) != len(sample_files):
        warnings.append("manifest samples list does not match samples/*.json count")
    if require_samples and not sample_files:
        problems.append("sample pack has no samples")

    samples: list[dict[str, object]] = []
    sample_manifest_items: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for path in sample_files:
        raw = path.read_text(encoding="utf-8")
        scan_text_for_sensitive_values(path.as_posix(), raw, problems)
        sample = read_json(path, problems)
        validate_sample(path, sample, endpoints, scenario_ids, seen_ids, problems)
        item = {
            "file": f"samples/{path.name}",
            "sample_id": sample.get("sample_id", ""),
            "source_type": sample.get("source_type", ""),
            "endpoint_id": nested(sample, "endpoint", "id"),
            "scenario_id": sample.get("scenario_id", ""),
            "digest": "sha256:" + sample_digest(sample),
        }
        sample_manifest_items.append(item)
        samples.append({**item, "file": str(path)})

    validate_manifest_samples(manifest_samples, sample_manifest_items, problems)

    status = "passed"
    if problems:
        status = "failed"
    elif not sample_files:
        status = "awaiting_samples"
    return {
        "ok": not problems,
        "status": status,
        "contract_bundle": CONTRACT_BUNDLE,
        "sample_schema_version": SAMPLE_SCHEMA_VERSION,
        "sample_importer_version": SAMPLE_IMPORTER_VERSION,
        "sample_pack": str(sample_pack),
        "sample_count": len(sample_files),
        "samples": samples,
        "warnings": warnings,
        "problems": problems,
    }


def validate_sample(path: Path, sample: dict[str, object], endpoints: dict[str, dict[str, object]], scenario_ids: set[str], seen_ids: set[str], problems: list[str]) -> None:
    sample_id = expect_string(sample, "sample_id", problems, path)
    if sample_id in seen_ids:
        problems.append(f"{path}: duplicate sample_id {sample_id}")
    seen_ids.add(sample_id)
    if sample.get("schema_version") != SAMPLE_SCHEMA_VERSION:
        problems.append(f"{path}: schema_version mismatch")
    if sample.get("contract_bundle") != CONTRACT_BUNDLE:
        problems.append(f"{path}: contract_bundle mismatch")
    source_type = expect_string(sample, "source_type", problems, path)
    if source_type not in SOURCE_TYPES:
        problems.append(f"{path}: invalid source_type {source_type}")
    if sample.get("sample_sha256") != sample_digest(sample):
        problems.append(f"{path}: sample_sha256 mismatch")

    authorization = sample.get("authorization")
    if not isinstance(authorization, dict) or authorization.get("status") != "approved":
        problems.append(f"{path}: authorization.status must be approved")
    else:
        for key in ("approved_by", "approved_at"):
            if not string_value(authorization.get(key)):
                problems.append(f"{path}: authorization.{key} missing")

    deidentification = sample.get("deidentification")
    if not isinstance(deidentification, dict) or deidentification.get("status") != "passed":
        problems.append(f"{path}: deidentification.status must be passed")
    else:
        for key in ("method", "checked_at"):
            if not string_value(deidentification.get(key)):
                problems.append(f"{path}: deidentification.{key} missing")

    endpoint = sample.get("endpoint")
    if not isinstance(endpoint, dict):
        problems.append(f"{path}: endpoint missing")
        return
    endpoint_id = string_value(endpoint.get("id"))
    contract = endpoints.get(endpoint_id)
    if not contract:
        problems.append(f"{path}: unknown endpoint id {endpoint_id}")
    else:
        if endpoint.get("method") != contract.get("method") or endpoint.get("path") != contract.get("path"):
            problems.append(f"{path}: endpoint method/path mismatch")
    scenario_id = string_value(sample.get("scenario_id"))
    if scenario_id not in scenario_ids:
        problems.append(f"{path}: unknown scenario_id {scenario_id}")
    request = sample.get("request")
    if not isinstance(request, dict) or not isinstance(request.get("data"), dict) or not request["data"]:
        problems.append(f"{path}: request.data missing")
    responses = sample.get("responses")
    if not isinstance(responses, dict) or not isinstance(responses.get("sync"), dict):
        problems.append(f"{path}: responses.sync missing")
    assertions = sample.get("assertions")
    if not isinstance(assertions, dict):
        problems.append(f"{path}: assertions missing")


def validate_manifest_samples(manifest_samples: object, samples: list[dict[str, object]], problems: list[str]) -> None:
    if not isinstance(manifest_samples, list):
        problems.append("sample manifest samples must be a list")
        return
    manifest_by_id: dict[str, dict[str, object]] = {}
    for item in manifest_samples:
        if not isinstance(item, dict):
            problems.append("sample manifest contains a non-object sample item")
            continue
        sample_id = string_value(item.get("sample_id"))
        if not sample_id:
            problems.append("sample manifest contains an item without sample_id")
            continue
        if sample_id in manifest_by_id:
            problems.append(f"sample manifest duplicate sample_id {sample_id}")
        manifest_by_id[sample_id] = item
    actual_by_id = {string_value(item.get("sample_id")): item for item in samples}
    for sample_id in sorted(set(manifest_by_id) - set(actual_by_id)):
        problems.append(f"sample manifest references missing sample file for {sample_id}")
    for sample_id in sorted(set(actual_by_id) - set(manifest_by_id)):
        problems.append(f"sample manifest missing sample item for {sample_id}")
    for sample_id in sorted(set(manifest_by_id) & set(actual_by_id)):
        manifest_item = manifest_by_id[sample_id]
        actual_item = actual_by_id[sample_id]
        for key in ("file", "digest", "endpoint_id", "scenario_id", "source_type"):
            if manifest_item.get(key) != actual_item.get(key):
                problems.append(
                    f"sample manifest {sample_id}.{key} mismatch: "
                    f"manifest={manifest_item.get(key)!r} actual={actual_item.get(key)!r}"
                )


def load_endpoints(contract_dir: Path, problems: list[str]) -> dict[str, dict[str, object]]:
    data = read_json(contract_dir / "endpoint-contracts.json", problems)
    endpoints = {}
    for item in data.get("endpoints", []):
        if isinstance(item, dict):
            endpoints[string_value(item.get("id"))] = item
    return endpoints


def load_scenario_ids(contract_dir: Path, problems: list[str]) -> set[str]:
    data = read_json(contract_dir / "scenario-catalog.json", problems)
    return {string_value(item.get("id")) for item in data.get("scenarios", []) if isinstance(item, dict)}


def scan_text_for_sensitive_values(label: str, text: str, problems: list[str]) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            problems.append(f"{label}: contains blocked secret pattern")
    if PHONE_PATTERN.search(text):
        problems.append(f"{label}: contains unmasked mainland China mobile number")
    if ID_CARD_PATTERN.search(text):
        problems.append(f"{label}: contains unmasked PRC ID card number")
    for host in URL_PATTERN.findall(text):
        normalized = host.lower().strip("[]")
        if normalized not in ALLOWED_SAMPLE_HOSTS and not normalized.endswith(".example.invalid"):
            problems.append(f"{label}: contains non-placeholder URL host {host}")
    for number in re.findall(r"(?<!\d)\d{13,19}(?!\d)", text):
        if is_placeholder_number(number):
            continue
        if luhn(number):
            problems.append(f"{label}: contains possible unmasked bank card number")
        else:
            problems.append(f"{label}: contains long unmasked numeric identifier")


def sample_digest(sample: dict[str, object]) -> str:
    clone = copy.deepcopy(sample)
    clone.pop("sample_sha256", None)
    canonical = json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def luhn(value: str) -> bool:
    total = 0
    reverse = value[::-1]
    for index, char in enumerate(reverse):
        digit = ord(char) - 48
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def is_placeholder_number(value: str) -> bool:
    return len(set(value)) <= 2 or value.startswith(("0000", "9999", "1234"))


def read_json(path: Path, problems: list[str]) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        problems.append(f"{path}: invalid JSON: {exc}")
        return {}


def expect_string(data: dict[str, object], key: str, problems: list[str], path: Path) -> str:
    value = string_value(data.get(key))
    if not value:
        problems.append(f"{path}: {key} missing")
    return value


def string_value(value: object) -> str:
    return value if isinstance(value, str) else ""


def nested(data: dict[str, object], *keys: str) -> str:
    value: object = data
    for key in keys:
        if not isinstance(value, dict):
            return ""
        value = value.get(key)
    return string_value(value)


def resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def failure(problems: list[str]) -> dict[str, object]:
    return {"ok": False, "status": "failed", "problems": problems, "warnings": [], "samples": [], "sample_count": 0}


if __name__ == "__main__":
    raise SystemExit(main())
