#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTRACT_BUNDLE = "huifu-pay-integration-1.3.0-r4"
SAMPLE_SCHEMA_VERSION = "1.0"

EVENT_ALIASES = {
    "business.variant": ("business.variant",),
    "close.accepted": ("close.accepted",),
    "close.query": ("close.query",),
    "close.settled": ("close.settled",),
    "notify.delivery": ("notify.delivery",),
    "payment.accepted": ("payment.accepted",),
    "payment.notify": ("notify.delivery",),
    "payment.query": ("payment.query",),
    "refund.accepted": ("refund.accepted",),
    "refund.notify": ("notify.refund_delivery", "notify.delivery"),
    "refund.query": ("refund.query",),
    "refund.settled": ("refund.settled",),
    "splitpay.query": ("splitpay.query",),
    "webhook.delivery": ("webhook.delivery",),
    "webhook.hosting.accounted": ("webhook.delivery",),
    "webhook.hosting.pay": ("webhook.delivery",),
    "webhook.refund.standard": ("webhook.delivery",),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sample-backed multi-step replay coverage against scenario reports.")
    parser.add_argument("--sample-pack", default="local-sandbox/sample-packs/huifu-pay-integration-1.3.0-r4")
    parser.add_argument("--scenario-report-dir", required=True)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sample_pack = resolve(repo_root, args.sample_pack)
    scenario_report_dir = resolve(repo_root, args.scenario_report_dir)
    result = validate_sample_replay_contracts(sample_pack, scenario_report_dir)
    if args.output:
        output = resolve(repo_root, args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


def validate_sample_replay_contracts(sample_pack: Path, scenario_report_dir: Path) -> dict[str, Any]:
    problems: list[str] = []
    warnings: list[str] = []
    manifest = read_json(sample_pack / "manifest.json", problems)
    scenario_doc = read_json(scenario_report_dir / "scenario-results.json", problems)
    sample_coverage = read_json(scenario_report_dir / "sample-coverage.json", problems)

    if manifest.get("contract_bundle") != CONTRACT_BUNDLE:
        problems.append("sample manifest contract_bundle mismatch")
    if manifest.get("sample_schema_version") != SAMPLE_SCHEMA_VERSION:
        problems.append("sample manifest sample_schema_version mismatch")

    scenarios = scenario_doc.get("scenarios", [])
    if not isinstance(scenarios, list):
        problems.append("scenario-results.json scenarios must be a list")
        scenarios = []
    scenarios_by_id = {string_value(item.get("id")): item for item in scenarios if isinstance(item, dict)}
    fixture_by_sample = sample_fixture_index(sample_coverage, problems)
    manifest_by_id = manifest_sample_index(manifest, problems)

    sample_files = sorted((sample_pack / "samples").glob("*.json")) if (sample_pack / "samples").is_dir() else []
    if not sample_files:
        problems.append("sample pack has no samples")

    results = []
    for path in sample_files:
        sample = read_json(path, problems)
        sample_result = validate_sample(path, sample, manifest_by_id, fixture_by_sample, scenarios_by_id)
        results.append(sample_result)

    actual_sample_ids = {string_value(item.get("sample_id")) for item in results}
    for sample_id in sorted(set(manifest_by_id) - actual_sample_ids):
        problems.append(f"sample manifest references missing sample file for {sample_id}")
    for sample_id in sorted(set(fixture_by_sample) - actual_sample_ids):
        warnings.append(f"scenario report contains derived fixture for sample not present in sample pack: {sample_id}")

    for item in results:
        problems.extend(f"{item['sample_id']}: {problem}" for problem in item["problems"])

    passed = sum(1 for item in results if item["status"] == "passed")
    failed = len(results) - passed
    return {
        "ok": not problems,
        "status": "passed" if not problems else "failed",
        "schema_version": "1.0",
        "contract_bundle": CONTRACT_BUNDLE,
        "generated_at": now_utc(),
        "sample_pack": str(sample_pack),
        "scenario_report_dir": str(scenario_report_dir),
        "coverage_model": "sample_evidence_chain_coverage",
        "execution_model": "scenario_report_cross_check",
        "sample_fixture_execution_required": False,
        "sample_count": len(results),
        "passed": passed,
        "failed": failed,
        "samples": results,
        "warnings": warnings,
        "problems": problems,
    }


def validate_sample(
    path: Path,
    sample: dict[str, Any],
    manifest_by_id: dict[str, dict[str, Any]],
    fixture_by_sample: dict[str, dict[str, Any]],
    scenarios_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    problems: list[str] = []
    sample_id = string_value(sample.get("sample_id")) or path.stem
    scenario_id = string_value(sample.get("scenario_id"))
    scenario = scenarios_by_id.get(scenario_id, {})
    scenario_status = string_value(scenario.get("status")) or "missing"
    scenario_events = set(string_list(scenario.get("events")))
    scenario_endpoints = set(string_list(scenario.get("endpoint_ids")))

    if scenario_status == "missing":
        problems.append(f"scenario {scenario_id} missing from scenario-results.json")
    elif scenario_status != "passed":
        problems.append(f"scenario {scenario_id} status={scenario_status}")

    expected_digest = "sha256:" + sample_digest(sample)
    manifest_item = manifest_by_id.get(sample_id)
    if not manifest_item:
        problems.append("missing from sample manifest")
    else:
        if manifest_item.get("digest") != expected_digest:
            problems.append("sample manifest digest mismatch")
        if manifest_item.get("scenario_id") != scenario_id:
            problems.append("sample manifest scenario_id mismatch")
        if manifest_item.get("file") != f"samples/{path.name}":
            problems.append("sample manifest file mismatch")
        if manifest_item.get("endpoint_id") != sample_endpoint_id(sample):
            problems.append("sample manifest endpoint_id mismatch")
        if manifest_item.get("source_type") != sample.get("source_type"):
            problems.append("sample manifest source_type mismatch")
    if sample.get("sample_sha256") != sample_digest(sample):
        problems.append("sample_sha256 mismatch")

    fixture = fixture_by_sample.get(sample_id)
    fixture_result: dict[str, Any]
    if not fixture:
        fixture_result = {"status": "missing", "reason": "sample-backed fixture missing from sample-coverage.json"}
        problems.append("sample-backed fixture missing from sample-coverage.json")
    else:
        fixture_digest = string_value(fixture.get("sample_digest"))
        fixture_result = {
            "id": fixture.get("id"),
            "endpoint_id": fixture.get("endpoint_id"),
            "sample_coverage_level": fixture.get("sample_coverage_level"),
            "status": "present",
            "direct_fixture_execution_status": fixture.get("status"),
            "direct_fixture_execution_required": False,
        }
        if fixture_digest != expected_digest:
            problems.append("derived sample fixture digest mismatch")
            fixture_result["status"] = "digest_mismatch"

    required_endpoints = collect_required_endpoints(sample)
    endpoint_results = []
    for endpoint_id in required_endpoints:
        status = "covered" if endpoint_id in scenario_endpoints else "missing"
        endpoint_results.append({"id": endpoint_id, "status": status})
        if status != "covered":
            problems.append(f"required endpoint {endpoint_id} not covered by scenario {scenario_id}")

    assertions = sample.get("assertions", {})
    if not isinstance(assertions, dict):
        assertions = {}
    field_results = validate_field_assertions(
        assertions.get("field_assertions"),
        sample_response_payloads(sample),
        "responses.*.data",
    )
    for field_status in field_results:
        if field_status["status"] != "covered":
            problems.append(f"field assertion {field_status['path']} not satisfied in {field_status['scope']}")

    event_assertions = normalize_event_assertions(assertions.get("event_assertions"))
    event_results = []
    event_field_results = []
    for assertion in event_assertions:
        event_id = assertion["event"]
        aliases = EVENT_ALIASES.get(event_id, (event_id,))
        matched = sorted(set(aliases) & scenario_events)
        status = "covered" if matched else "missing"
        event_results.append({"event": event_id, "scenario_events": list(aliases), "matched": matched, "status": status})
        if status != "covered":
            problems.append(f"required event {event_id} not covered by scenario {scenario_id}")
        for field, expected in assertion["fields"].items():
            field_status = field_assertion_status(sample, field, expected)
            event_field_results.append(field_status)
            if field_status["status"] != "covered":
                problems.append(f"event field assertion {event_id}.{field}={expected!r} not found in sample evidence")

    response_steps = response_step_results(sample, scenario_endpoints, scenario_events)
    for step in response_steps:
        if step["status"] == "missing":
            problems.append(f"response step {step['name']} lacks scenario evidence")

    return {
        "sample_id": sample_id,
        "file": str(path),
        "source_type": sample.get("source_type"),
        "scenario_id": scenario_id,
        "scenario_status": scenario_status,
        "status": "passed" if not problems else "failed",
        "source_sample_fixture": fixture_result,
        "required_endpoints": endpoint_results,
        "required_events": event_results,
        "field_assertions": field_results,
        "event_field_assertions": event_field_results,
        "response_steps": response_steps,
        "problems": problems,
    }


def collect_required_endpoints(sample: dict[str, Any]) -> list[str]:
    endpoints: list[str] = []
    append_unique(endpoints, sample_endpoint_id(sample))
    responses = sample.get("responses")
    if isinstance(responses, dict):
        for step in responses.values():
            if not isinstance(step, dict):
                continue
            step_endpoint = step.get("endpoint")
            if isinstance(step_endpoint, dict):
                append_unique(endpoints, string_value(step_endpoint.get("id")))
    return endpoints


def sample_endpoint_id(sample: dict[str, Any]) -> str:
    endpoint = sample.get("endpoint")
    if not isinstance(endpoint, dict):
        return ""
    return string_value(endpoint.get("id"))


def response_step_results(sample: dict[str, Any], scenario_endpoints: set[str], scenario_events: set[str]) -> list[dict[str, Any]]:
    responses = sample.get("responses")
    if not isinstance(responses, dict):
        return []
    out: list[dict[str, Any]] = []
    for name, step in sorted(responses.items()):
        if not isinstance(step, dict):
            continue
        kind = response_step_kind(name, step)
        evidence: list[dict[str, Any]] = []
        endpoint = step.get("endpoint")
        if isinstance(endpoint, dict):
            endpoint_id = string_value(endpoint.get("id"))
            if endpoint_id:
                evidence.append({"type": "endpoint", "id": endpoint_id, "status": "covered" if endpoint_id in scenario_endpoints else "missing"})
        event_id = response_step_event_hint(name, sample)
        if event_id:
            aliases = EVENT_ALIASES.get(event_id, (event_id,))
            matched = sorted(set(aliases) & scenario_events)
            evidence.append({"type": "event", "id": event_id, "scenario_events": list(aliases), "matched": matched, "status": "covered" if matched else "missing"})
        required = bool(evidence)
        status = "covered"
        if required and any(item["status"] != "covered" for item in evidence):
            status = "missing"
        elif not required:
            status = "supporting_evidence"
        out.append({"name": name, "kind": kind, "required": required, "status": status, "evidence": evidence})
    return out


def response_step_kind(name: str, step: dict[str, Any]) -> str:
    lowered = name.lower()
    endpoint = step.get("endpoint")
    endpoint_id = string_value(endpoint.get("id")) if isinstance(endpoint, dict) else ""
    if lowered == "sync":
        return "sync_response"
    if "terminal" in lowered and "notification" in lowered:
        return "supporting_evidence"
    if "webhook" in lowered:
        return "webhook_evidence"
    if "notify" in lowered or "notification" in lowered:
        return "notify_evidence"
    if "query" in lowered or "query" in endpoint_id:
        return "query_response"
    if lowered.startswith(("downstream", "legacy", "original")):
        return "supporting_evidence"
    if endpoint_id:
        return "endpoint_response"
    return "supporting_evidence"


def response_step_event_hint(name: str, sample: dict[str, Any]) -> str:
    lowered = name.lower()
    endpoint_id = string_value(sample.get("endpoint", {}).get("id")) if isinstance(sample.get("endpoint"), dict) else ""
    if "terminal" in lowered and "notification" in lowered:
        return ""
    if "webhook" in lowered:
        if "refund" in lowered or "refund" in endpoint_id:
            return "webhook.refund.standard"
        return "webhook.delivery"
    if "notify" in lowered or "notification" in lowered:
        if "refund" in lowered or "refund" in endpoint_id:
            return "refund.notify"
        return "payment.notify"
    return ""


def normalize_event_assertions(raw: Any) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, str) and item:
            out.append({"event": item, "fields": {}})
        elif isinstance(item, dict):
            event = string_value(item.get("event"))
            if event:
                fields = item.get("fields")
                out.append({"event": event, "fields": fields if isinstance(fields, dict) else {}})
    return out


def field_assertion_status(sample: dict[str, Any], field: str, expected: Any) -> dict[str, Any]:
    values = find_values_by_key(sample.get("responses", {}), field)
    expected_text = comparable(expected)
    matched = [value for value in values if comparable(value) == expected_text]
    return {
        "field": field,
        "expected": expected,
        "status": "covered" if matched else "missing",
        "observed_count": len(values),
        "matched_count": len(matched),
    }


def validate_field_assertions(raw: Any, payloads: list[tuple[str, Any]], scope: str) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            out.append({"path": "", "scope": scope, "status": "invalid", "reason": "field assertion must be an object"})
            continue
        path = string_value(item.get("path"))
        if not path:
            out.append({"path": "", "scope": scope, "status": "invalid", "reason": "path missing"})
            continue
        matches = find_payload_path_matches(payloads, path)
        if item.get("exists") is True:
            status = "covered" if matches else "missing"
            out.append({"path": path, "scope": scope, "assertion": "exists", "matched_steps": [name for name, _ in matches], "status": status})
            continue
        if "equals" in item:
            expected = item.get("equals")
            matched = [(name, value) for name, value in matches if comparable(value) == comparable(expected)]
            status = "covered" if matched else "missing"
            out.append({
                "path": path,
                "scope": scope,
                "assertion": "equals",
                "expected": expected,
                "matched_steps": [name for name, _ in matched],
                "observed_count": len(matches),
                "status": status,
            })
            continue
        out.append({"path": path, "scope": scope, "status": "invalid", "reason": "unsupported assertion"})
    return out


def sample_response_payloads(sample: dict[str, Any]) -> list[tuple[str, Any]]:
    responses = sample.get("responses")
    request = nested_object(sample, "request", "data")
    out: list[tuple[str, Any]] = []
    if isinstance(request, dict):
        out.append(("request", request))
    if not isinstance(responses, dict):
        return out
    for name, step in responses.items():
        if not isinstance(step, dict):
            continue
        for key_path in (("data",), ("body", "data")):
            payload = nested_object(step, *key_path)
            if isinstance(payload, dict):
                out.append((name, payload))
    return out


def find_payload_path_matches(payloads: list[tuple[str, Any]], path: str) -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    for name, payload in payloads:
        exists, value = value_by_path(payload, path)
        if exists:
            out.append((name, value))
    return out


def value_by_path(root: Any, path: str) -> tuple[bool, Any]:
    value = root
    for part in path.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
            continue
        return False, None
    return True, value


def nested_object(data: dict[str, Any], *keys: str) -> Any:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict):
            return {}
        value = value.get(key)
    return value if value is not None else {}


def find_values_by_key(value: Any, key: str) -> list[Any]:
    out: list[Any] = []
    if isinstance(value, dict):
        for item_key, item_value in value.items():
            if item_key == key:
                out.append(item_value)
            out.extend(find_values_by_key(item_value, key))
    elif isinstance(value, list):
        for item in value:
            out.extend(find_values_by_key(item, key))
    return out


def sample_fixture_index(sample_coverage: dict[str, Any], problems: list[str]) -> dict[str, dict[str, Any]]:
    raw = sample_coverage.get("sample_backed_fixtures", [])
    if not isinstance(raw, list):
        problems.append("sample-coverage.json sample_backed_fixtures must be a list")
        return {}
    out: dict[str, dict[str, Any]] = {}
    for item in raw:
        if not isinstance(item, dict):
            continue
        sample_id = string_value(item.get("source_sample_id"))
        if not sample_id:
            continue
        if sample_id in out:
            problems.append(f"duplicate sample-backed fixture for {sample_id}")
        out[sample_id] = item
    return out


def manifest_sample_index(manifest: dict[str, Any], problems: list[str]) -> dict[str, dict[str, Any]]:
    raw = manifest.get("samples", [])
    if not isinstance(raw, list):
        problems.append("sample manifest samples must be a list")
        return {}
    out: dict[str, dict[str, Any]] = {}
    for item in raw:
        if not isinstance(item, dict):
            continue
        sample_id = string_value(item.get("sample_id"))
        if not sample_id:
            problems.append("sample manifest item missing sample_id")
            continue
        if sample_id in out:
            problems.append(f"sample manifest duplicate sample_id {sample_id}")
        out[sample_id] = item
    return out


def sample_digest(sample: dict[str, Any]) -> str:
    clone = copy.deepcopy(sample)
    clone.pop("sample_sha256", None)
    canonical = json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def append_unique(values: list[str], value: str) -> None:
    if value and value not in values:
        values.append(value)


def comparable(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def read_json(path: Path, problems: list[str]) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        problems.append(f"{path}: {exc}")
        return {}


def resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
