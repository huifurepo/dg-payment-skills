#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path


CONTRACT_BUNDLE = "huifu-pay-integration-1.3.0-r4"
SAMPLE_SCHEMA_VERSION = "1.0"
SAMPLE_IMPORTER_VERSION = "1.0"


def main() -> int:
    parser = argparse.ArgumentParser(description="Import validated deidentified samples into r4 derived fixtures.")
    parser.add_argument("--sample-pack", default="local-sandbox/sample-packs/huifu-pay-integration-1.3.0-r4")
    parser.add_argument("--contract-dir", default="local-sandbox/contracts/huifu-pay-integration-1.3.0-r4")
    parser.add_argument("--write", action="store_true", help="Write derived fixtures and endpoint-contracts.json updates.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sample_pack = resolve(repo_root, args.sample_pack)
    contract_dir = resolve(repo_root, args.contract_dir)
    validation = run_validation(repo_root, sample_pack, contract_dir)
    if not validation.get("ok"):
        print(json.dumps({"ok": False, "stage": "validate", "validation": validation}, ensure_ascii=False, indent=2))
        return 1
    sample_files = sorted((sample_pack / "samples").glob("*.json")) if (sample_pack / "samples").is_dir() else []
    endpoint_contracts_path = contract_dir / "endpoint-contracts.json"
    endpoint_contracts = read_json(endpoint_contracts_path)
    endpoint_by_id = {item["id"]: item for item in endpoint_contracts.get("endpoints", [])}
    generated: list[dict[str, object]] = []
    drift: list[dict[str, object]] = []

    for path in sample_files:
        sample = read_json(path)
        fixture = derived_fixture(sample)
        endpoint = endpoint_by_id.get(fixture["endpoint_id"])
        if endpoint is None:
            raise SystemExit(f"[ERROR] unknown endpoint for sample fixture: {fixture['endpoint_id']}")
        fixture_path = contract_dir / "fixtures" / f"{fixture['id']}.json"
        generated.append({"sample_id": sample["sample_id"], "fixture_id": fixture["id"], "fixture_path": str(fixture_path)})
        variants = endpoint.setdefault("variant_fixtures", [])
        if not args.write:
            drift.extend(check_existing_fixture(fixture_path, fixture, variants))
        if args.write:
            fixture_path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if fixture["id"] not in variants:
                variants.append(fixture["id"])

    if args.write:
        endpoint_contracts_path.write_text(json.dumps(endpoint_contracts, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ok = not drift
    print(
        json.dumps(
            {
                "ok": ok,
                "write": args.write,
                "contract_bundle": CONTRACT_BUNDLE,
                "sample_schema_version": SAMPLE_SCHEMA_VERSION,
                "sample_importer_version": SAMPLE_IMPORTER_VERSION,
                "sample_count": len(sample_files),
                "generated_fixture_count": len(generated),
                "generated": generated,
                "drift": drift,
                "status": "imported" if args.write and generated else ("drift" if drift else ("verified" if generated else "awaiting_samples")),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if ok else 1


def run_validation(repo_root: Path, sample_pack: Path, contract_dir: Path) -> dict[str, object]:
    raw = subprocess.check_output(
        [
            sys.executable,
            "scripts/validate_local_sandbox_samples.py",
            "--sample-pack",
            str(sample_pack),
            "--contract-dir",
            str(contract_dir),
        ],
        cwd=repo_root,
        text=True,
        encoding="utf-8",
    )
    return json.loads(raw)


def derived_fixture(sample: dict[str, object]) -> dict[str, object]:
    endpoint = sample["endpoint"]
    sync = sample["responses"]["sync"]
    sync_data = sync.get("data", sync)
    expected = sample.get("expected", {})
    assertions = sample.get("assertions", {})
    source_type = sample["source_type"]
    coverage = "deidentified_production_sample" if source_type == "deidentified_production" else "deidentified_joint_debug_sample"
    fixture_id = "sample-" + sample["sample_id"]
    return {
        "schema_version": "1.1",
        "contract_bundle": CONTRACT_BUNDLE,
        "id": fixture_id,
        "endpoint_id": endpoint["id"],
        "method": endpoint["method"],
        "path": endpoint["path"],
        "kind": "sample",
        "headers_profile": sample.get("headers_profile", "java-php-python-local-sandbox"),
        "request": {"data": sample["request"]["data"]},
        "expected": {
            "resp_code": expected.get("resp_code") or sync_data.get("resp_code", "00000000"),
            "fields": expected.get("fields", {}),
        },
        "expected_resp_code": expected.get("resp_code") or sync_data.get("resp_code", "00000000"),
        "assertions": assertions.get("assertions", ["envelope", "headers", "signature", "sample-backed"]),
        "field_assertions": assertions.get("field_assertions", []),
        "event_assertions": event_assertion_ids(assertions),
        "source_sample_id": sample["sample_id"],
        "sample_digest": "sha256:" + sample_digest(sample),
        "sample_coverage_level": coverage,
    }


def sample_digest(sample: dict[str, object]) -> str:
    clone = copy.deepcopy(sample)
    clone.pop("sample_sha256", None)
    canonical = json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def event_assertion_ids(assertions: dict[str, object]) -> list[str]:
    raw = assertions.get("event_assertions", [])
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, str) and item:
            out.append(item)
        elif isinstance(item, dict):
            event = item.get("event")
            if isinstance(event, str) and event:
                out.append(event)
    return out


def check_existing_fixture(fixture_path: Path, expected: dict[str, object], variants: list[object]) -> list[dict[str, object]]:
    problems: list[dict[str, object]] = []
    if not fixture_path.is_file():
        problems.append({"fixture": str(fixture_path), "reason": "missing_derived_fixture"})
    else:
        current = read_json(fixture_path)
        if canonical_json(current) != canonical_json(expected):
            problems.append({"fixture": str(fixture_path), "reason": "derived_fixture_drift"})
    if expected["id"] not in variants:
        problems.append({"fixture": expected["id"], "reason": "endpoint_variant_missing"})
    return problems


def canonical_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


if __name__ == "__main__":
    raise SystemExit(main())
