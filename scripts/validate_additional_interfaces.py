#!/usr/bin/env python3
"""Independently verify additions against raw tables and real SDK serializers."""
import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import re

from validate_merchant_onboarding_source_contract import RawField, source_tables, flatten, normalize, split_catalog_row
from validate_payment_field_catalog import expected_description, expected_transport, expected_status
from validation_runtime import require_assertions_enabled

require_assertions_enabled()
ROOT = Path(__file__).resolve().parent.parent
# Kept independent of generator configuration: route version and root order are
# semantic decisions, not something inferred from whatever the generator emits.
SCOPES = {
    "delay-confirm": ("payment", "/v2/trade/payment/delaytrans/confirm", ("request", "response", "request.data", "response.data", "async", "async.resp_data")),
    "delay-confirm-query": ("payment", "/v3/trade/payment/delaytrans/confirmquery", ("request", "response", "request.data", "response.data")),
    "delay-confirm-refund": ("payment", "/v2/trade/payment/delaytrans/confirmrefund", ("request", "response", "request.data", "response.data")),
    "delay-confirm-refund-query": ("payment", "/v2/trade/payment/delaytrans/confirmrefundquery", ("request.data",)),
    "account-balance-query": ("payment", "/v2/trade/acctpayment/balance/query", ("request", "request.data", "response")),
    "account-ledger-query": ("payment", "/v2/trade/acctpayment/acctlog/query", ("request", "request.data", "response")),
    "account-ledger-summary-query": ("payment", "/v2/trade/acctpayment/acctlog/summary", ("request", "request.data", "response")),
    "account-subaccount-open": ("onboarding", "/v2/merchant/settle/config", ("request", "request.data", "response", "async")),
    "account-subaccount-modify": ("onboarding", "/v2/merchant/settle/modify", ("request", "request.data", "response", "async")),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def catalog_records(path):
    result, title = {}, None
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            title = line[3:]
        if line.startswith("| `"):
            cells = [cell.strip('`') for cell in split_catalog_row(line)]
            assert len(cells) == 9, (path, title)
            key = title, cells[0]
            assert key not in result, key
            result[key] = tuple(cells[1:])
    return result


def raw_records(entry):
    path = ROOT / entry["path"]
    assert sha(path) == entry["sha256"], entry["key"]
    _, route, prefixes = SCOPES[entry["key"]]
    assert route == entry["endpoint"], (entry["key"], "wrong API version or route")
    text = path.read_text(encoding="utf-8-sig")
    expected, declared = {}, []
    if path.suffix == ".json":
        doc = json.loads(text)
        assert "/" + doc["uri"].lstrip("/") == route
        assert set(doc) == {"desc", "requestBody", "requestDemo", "sign", "uri"}
        fields = [RawField(p["name"], normalize(p.get("desc", "")) or "—", p["fieldType"], p.get("maxLength") or "—", p["isRequired"], normalize(p.get("remark", "")) or "—", None, False) for p in doc["requestBody"]["params"]]
        flat = [("request.data." + field.name, field) for field in fields]
        for name, field in flat:
            p = next(p for p in doc["requestBody"]["params"] if p["name"] == field.name)
            key = entry["title"], "request.data." + p["name"]
            assert key not in expected
            expected[key] = (*expected_transport(name, flat, set(), entry["key"], "request.data"), field.label, field.kind, field.length, field.required, expected_status(field), field.description)
            declared.append(p["name"])
        assert len(expected) == 4
        assert entry["http_method"] is None
        return expected, declared
    assert "https://api.huifu.com" + route in text
    assert entry["http_method"] == "POST"
    roots, nested = source_tables(text, entry["url"])
    assert len(roots) == len(prefixes), (entry["key"], "root-table mismatch")
    used = set()
    for prefix, fields in zip(prefixes, roots, strict=True):
        if prefix == "request.data":
            declared = [field.name for field in fields]
        flat = flatten(fields, nested, prefix, used)
        for name, field in flat:
            key = entry["title"], name
            assert key not in expected, key
            expected[key] = (*expected_transport(name, flat, set(), entry["key"], prefix), field.label, field.kind, field.length, field.required, expected_status(field), expected_description(field.description, entry["url"], entry["key"], name))
    assert set(nested) == used, entry["key"]
    return expected, declared


def check_equal(expected, actual):
    assert expected.keys() == actual.keys(), {"missing": sorted(expected.keys()-actual.keys()), "extra": sorted(actual.keys()-expected.keys())}
    mismatches = [key for key in expected if expected[key] != actual[key]]
    assert not mismatches, [(key, expected[key], actual[key]) for key in mismatches[:3]]


def sdk_validate(root, entries, expected_request_fields):
    java = root / "bspay-java-sdk/opps-bspay-java-sdk/src/main/java/com/huifu/bspay/sdk/opps"
    php = root / "bspay-php-sdk/BsPaySdk"
    python = root / "dg_sdk-2.0.28/dg_sdk"
    je = (java / "core/enums/FunctionCodeEnum.java").read_text()
    pe = (php / "enums/FunctionCodeEnum.php").read_text()
    py = (python / "request/request_api_urls.py").read_text()
    urls = {}; exec(compile(py, "<official-sdk-routes>", "exec"), urls)
    evidence = json.loads((ROOT / "maintainer-contracts/interface-expansion-sdk-evidence-2026-10-25.json").read_text())
    typed = 0
    for entry in entries:
        route = SCOPES[entry["key"]][1]
        record = next(row for row in evidence["interfaces"] if row["key"] == entry["key"])
        assert record["route"] == route
        if entry["request_class"] is None:
            assert route not in py and route.lstrip("/") not in pe and route.lstrip("/").replace("/", ".") not in je
            assert "request(Map<String, Object> params, String funcCode, boolean isPage)" in (java / "client/BasePayClient.java").read_text()
            assert "is_object($request)" in (php / "core/BsPayClient.php").read_text()
            assert "def request_post(" in (python / "core/request_tools.py").read_text()
            continue
        cls, module = entry["request_class"], entry["python_module"]
        constant = module.upper()
        j = (java / "core/request" / (cls + ".java")).read_text()
        p = (php / "request" / (cls + ".php")).read_text()
        source = python / "request" / (module + "_request.py")
        keys = re.findall(r'@JSONField\(name = "([^"]+)"\)', j)
        properties = re.findall(r'private \$(\w+);', p)
        snake = lambda key: re.sub(r'[A-Z]', lambda m: '_' + m[0].lower(), key)
        assert set(map(snake, properties)) == set(keys), entry["key"]
        assert set(keys) <= set(expected_request_fields[entry["key"]])
        assert record["declared_fields"] == keys
        assert re.search(r'\b' + constant + r'\("' + re.escape(route.lstrip('/').replace('/', '.')) + r'"\s*,', je)
        assert re.search(r'\$' + constant + r'\s*=\s*[\'"]' + re.escape(route.lstrip('/')) + r'[\'"]', pe)
        assert urls[constant] == route
        for language, item in record["sources"].items():
            assert sha(root / item["path"]) == item["sha256"], (entry["key"], language)
        tree = ast.parse(source.read_text())
        tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
        calls = []
        namespace = {constant: route, "request_post": lambda *a, **kw: calls.append((a, kw))}
        exec(compile(tree, "<official-request-serializer>", "exec"), namespace)
        request = namespace[cls]()
        for key in keys:
            setattr(request, key, "offline_" + key)
        request.post({"offline_extra": "preserved"})
        assert calls == [((route, {**{key: "offline_" + key for key in keys}, "offline_extra": "preserved"}), {})]
        request.post({keys[0]: "collision"})
        assert calls[-1][0][1][keys[0]] == "collision", "SDK extension overwrite behavior changed"
        typed += 1
    assert typed == 8
    print("SDK additions verified: 8 × 3 exact typed routes; 8 actual Python serializers and collision probes; official generic summary entry; no network")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk-root", type=Path)
    args = parser.parse_args()
    all_expected, entries, request_fields = {}, [], {}
    for skill in ("huifu-pay-integration", "huifu-merchant-onboarding"):
        lock = json.loads((ROOT / f"maintainer-contracts/{skill}-additional-source-lock-2026-10-25.json").read_text())
        assert lock["skill"] == skill
        expected = {}
        for entry in lock["sources"]:
            owner = "payment" if skill == "huifu-pay-integration" else "onboarding"
            assert SCOPES[entry["key"]][0] == owner
            rows, top = raw_records(entry)
            expected.update(rows); request_fields[entry["key"]] = top
        actual = catalog_records(ROOT / lock["catalog"]["path"])
        check_equal(expected, actual)
        assert len(actual) == lock["totals"]["field_paths"]
        all_expected.update(expected); entries += lock["sources"]
    # Observable source-backed differences between interfaces and directions.
    assert all_expected['修改子账户配置', 'request.data.settle_config'][5] == 'Y'
    assert all_expected['子账户开通配置', 'request.data.settle_config'][5] == 'N'
    assert all_expected['账户余额信息查询', 'request.data.req_seq_id'][5] == 'N'
    assert 'req_date' not in request_fields['account-ledger-query']
    assert 'ord_amt' not in request_fields['delay-confirm-refund']
    assert all_expected['交易确认查询', 'response.data.trans_stat'][5] == 'N'
    assert set(request_fields['delay-confirm-refund-query']) == {'huifu_id','org_req_date','org_req_seq_id','org_hf_seq_id'}
    assert all_expected['账务流水汇总结果查询', 'response.data.summary_list[]'][3] == 'String'
    # Parsed String(JSON) containers stay strings on the wire, including descendants.
    for title, container in [('交易确认', 'response.data.acct_split_bunch'), ('修改子账户配置', 'request.data.settle_config')]:
        assert all_expected[title, container][3] == 'String'
        descendants = [value for (interface, path), value in all_expected.items() if interface == title and path.startswith(container + '.') ]
        assert descendants and all(value[0] == container for value in descendants)
    assert len(all_expected) == 368
    # Negative controls reject altered requiredness and invented response fields.
    bad = copy.deepcopy(all_expected)
    key = '修改子账户配置', 'request.data.settle_config'
    value = list(bad[key]); value[5] = 'N'; bad[key] = tuple(value)
    try: check_equal(all_expected, bad)
    except AssertionError: pass
    else: raise AssertionError('requiredness negative control accepted')
    bad = {**all_expected, ('交易确认退款查询','response.data.trans_stat'): ('状态','String','1','Y','invented')}
    try: check_equal(all_expected, bad)
    except AssertionError: pass
    else: raise AssertionError('invented response negative control accepted')
    print("Independent additions field check passed: 9 interfaces, 368 full paths, 2 negative controls")
    if args.sdk_root:
        sdk_validate(args.sdk_root, entries, request_fields)


if __name__ == "__main__":
    main()
