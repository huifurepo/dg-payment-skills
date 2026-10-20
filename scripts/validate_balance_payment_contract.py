#!/usr/bin/env python3
"""Protect balance API roles, conditional fields, transport and SDK routes offline."""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

from skill_validation_config import PAYMENT_SOURCE_LOCK
from validate_payment_field_catalog import actual_records
from validate_merchant_onboarding_sdk_evidence import resolve_sdk_layout
from validation_runtime import require_assertions_enabled

require_assertions_enabled()
ROOT = Path(__file__).resolve().parent.parent
# Explicit expectations are independent of the generator and SDK reflection.
APIS = (
    ('余额支付', 'V2TradeAcctpaymentPayRequest', 'v2_trade_acctpayment_pay', '/v2/trade/acctpayment/pay', ('req_seq_id','req_date','out_huifu_id','ord_amt','acct_split_bunch','risk_check_data','fund_type','trans_fee_take_flag','verify_value')),
    ('余额支付查询', 'V2TradeAcctpaymentPayQueryRequest', 'v2_trade_acctpayment_pay_query', '/v2/trade/acctpayment/pay/query', ('huifu_id','org_req_date')),
    ('余额支付退款', 'V2TradeAcctpaymentRefundRequest', 'v2_trade_acctpayment_refund', '/v2/trade/acctpayment/refund', ('req_seq_id','req_date','huifu_id','org_req_date','org_req_seq_id','org_hf_seq_id','ord_amt')),
    ('余额支付退款查询', 'V2TradeAcctpaymentRefundQueryRequest', 'v2_trade_acctpayment_refund_query', '/v2/trade/acctpayment/refund/query', ('org_req_seq_id','org_req_date','huifu_id')),
    ('手续费试算', 'V2TradeFeecalcRequest', 'v2_trade_feecalc', '/v2/trade/feecalc', ('huifu_id','req_date','req_seq_id','trade_type','trans_amt')),
    ('付款关系提交', 'V2TradePayrelationApplyRequest', 'v2_trade_payrelation_apply', '/v2/trade/payrelation/apply', ('out_huifu_id','req_date','req_seq_id','pay_relations')),
)


def validate_fields() -> None:
    lock = json.loads(PAYMENT_SOURCE_LOCK.read_text())
    rows = actual_records()
    fields = {(title, path): value for (title, _surface, path), value in rows.items()}
    def field(title: str, path: str) -> tuple:
        return fields[title, path]
    # The nine catalog attributes: wire, decoded, name, type, length, Y/N/C, status, description.
    assert field('余额支付', 'request.data.out_huifu_id')[2:5] == ('String', '32', 'Y')
    assert field('余额支付', 'request.data.huifu_id')[4] == 'N'
    assert field('余额支付', 'request.data.verify_value')[4] == 'C'
    assert field('余额支付', 'request.data.fund_type')[4] == 'C'
    assert field('余额支付', 'request.data.trans_fee_take_flag')[4] == 'C'
    assert field('余额支付', 'request.data.acct_split_bunch')[2] == 'String'
    assert field('余额支付', 'async.resp_data.acct_split_bunch')[2] == 'Object'
    assert '需要官方确认' in field('余额支付', 'async.resp_data.trans_stat')[1]
    assert 'C：完成' in field('余额支付查询', 'response.data.trans_stat')[-1]
    assert '06' in field('余额支付', 'request.data.risk_check_data.transfer_type')[-1]
    assert '06' not in field('余额支付退款', 'request.data.risk_check_data.transfer_type')[-1]
    request_paths = {path for (title, path) in fields if title == '余额支付退款查询' and path.startswith('request.data.')}
    assert request_paths == {'request.data.huifu_id','request.data.org_req_seq_id','request.data.org_req_date'}
    assert all(field('余额支付退款查询', path)[4] == 'Y' for path in request_paths)
    assert 'request.data.org_hf_seq_id' not in request_paths
    assert field('手续费试算', 'request.data.trans_amt')[4] == 'Y'
    assert ('手续费试算', 'request.data.ord_amt') not in fields
    assert field('付款关系提交', 'request.data.pay_relations[]')[2] == 'String'
    assert '需要官方确认' in field('付款关系提交', 'response.data.pay_relations')[1]
    sms_paths = {path for title, path in fields if title == '余额支付发送短信验证码' and path.startswith('request.data.')}
    assert sms_paths == {'request.data.req_date','request.data.req_seq_id','request.data.out_huifu_id','request.data.mobile_no','request.data.trans_type'}
    assert all(field('余额支付发送短信验证码', path)[4] == 'Y' for path in sms_paths)


def validate_sdk(root: Path) -> None:
    java, php, python = resolve_sdk_layout(root)
    java_base = java / 'opps-bspay-java-sdk/src/main/java/com/huifu/bspay/sdk/opps'
    java_enum = (java_base / 'core/enums/FunctionCodeEnum.java').read_text()
    php_enum = (php / 'enums/FunctionCodeEnum.php').read_text()
    python_urls = (python / 'request/request_api_urls.py').read_text()
    url_namespace = {}
    exec(compile(python_urls, '<official-route-constants>', 'exec'), url_namespace)
    for title, class_name, module, route, keys in APIS:
        java_text = (java_base / 'core/request' / (class_name + '.java')).read_text()
        php_text = (php / 'request' / (class_name + '.php')).read_text()
        constant = module.upper()
        assert set(re.findall(r'@JSONField\(name = "([^"]+)"\)', java_text)) == set(keys), title
        properties = re.findall(r'private \$(\w+);', php_text)
        snake = lambda word: re.sub(r'[A-Z]', lambda m: '_' + m[0].lower(), word)
        assert {snake(p) for p in properties} == set(keys), title
        assert constant in java_text and constant in php_text
        assert re.search(r'\b' + constant + r'\("' + re.escape(route.lstrip('/').replace('/', '.')) + r'"\s*,', java_enum), title
        assert re.search(r'\$' + constant + r'\s*=\s*[\'"]' + re.escape(route.lstrip('/')) + r'[\'"]', php_enum), title
        assert url_namespace[constant] == route
        # Execute the actual generated Python class without importing transport.
        tree = ast.parse((python / 'request' / (module + '_request.py')).read_text())
        tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
        calls = []
        namespace = {constant: route, 'request_post': lambda *a, **kw: calls.append((a,kw))}
        exec(compile(tree, '<official-balance-request>', 'exec'), namespace)
        request = namespace[class_name]()
        for key in keys:
            setattr(request, key, 'offline_' + key)
        request.post({'offline_extra': 'preserved'})
        assert calls == [((route, {**{key: 'offline_' + key for key in keys}, 'offline_extra':'preserved'}), {})]
        # Confirm overwrite behavior so the documented rejection must stay in adapters.
        request.post({keys[0]: 'collision'})
        assert calls[-1][0][1][keys[0]] == 'collision'
    sms_route = '/v2/trade/sms/verifycode/send'
    assert sms_route.replace('/', '.') .lstrip('.') not in java_enum
    assert sms_route.lstrip('/') not in php_enum
    assert sms_route not in python_urls
    for name in ('balancepay-java-adapter.md','balancepay-php-adapter.md','balancepay-python-adapter.md'):
        text = (ROOT / 'huifu-pay-integration/references' / name).read_text()
        assert sms_route.lstrip('/').replace('/', '.') in text or sms_route.lstrip('/') in text
        assert '官方' in text and '扩展' in text
    print('balance SDK evidence validated: 6 × 3 specialized routes, Python payload/collision probes, 3 generic SMS entries; no network')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk-root', type=Path)
    args = parser.parse_args()
    validate_fields()
    print('balance field contracts validated: roles, conditionality, original-refund identifiers, String(JSON), status and SMS boundaries')
    if args.sdk_root:
        validate_sdk(args.sdk_root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
