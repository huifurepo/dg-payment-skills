#!/usr/bin/env python3
"""Exercise official payout Request -> request_tools -> final signed body offline."""
import argparse
import base64
import importlib
import json
from pathlib import Path
import socket
import sys
from unittest.mock import patch

from validation_runtime import require_assertions_enabled
require_assertions_enabled()

ROUTES = {
    'v2_trade_settlement_encashment': '/v2/trade/settlement/encashment',
    'v2_trade_settlement_surrogate': '/v2/trade/settlement/surrogate',
    'v2_trade_settlement_query': '/v2/trade/settlement/query',
    'v2_trade_batchtranslog_query': '/v2/trade/batchtranslog/query',
    'v2_merchant_basicdata_settlement_query': '/v2/merchant/basicdata/settlement/query',
    'v2_trade_settlement_enchashment_dmamt_query': '/v2/trade/settlement/enchashment/dmamt/query',
}


def validate(root):
    sys.path.insert(0, str(root / 'dg_sdk-2.0.28'))
    from Crypto.PublicKey import RSA
    from dg_sdk.core.api_request import ApiRequest
    from dg_sdk.core.mer_config import MerConfig
    from dg_sdk.core.rsa_utils import rsa_design, rsa_long_encrypt
    from dg_sdk.dg_client import DGClient
    # Synthetic throwaway keys exist only in memory. No payment or HTTP call.
    pair = RSA.generate(2048)
    private = pair.export_key(pkcs=8).decode()
    public = pair.public_key().export_key().decode()
    DGClient.mer_config = MerConfig(private_key=private, public_key=public,
                                  sys_id='offline-system', product_id='offline-product',
                                  sign_type='RSA', jpt_x_skill_source='hfps/1.6.0')
    captured = []

    def final_body(files=None):
        assert files is None
        headers, body = ApiRequest._build_request_info(ApiRequest.request_url, ApiRequest.request_params, None)
        assert isinstance(body['data'], dict), 'SDK envelope data must remain an object'
        assert headers['jpt-x-skill-source'] == 'hfps/1.6.0'
        assert headers['jpt-x-skill-huifu_id'] == body['data'].get('huifu_id', '')
        assert headers['Content-Type'] == 'application/json;charset=utf-8'
        assert headers['signType'] == 'RSA' and headers['jpt-sdk_version'] == 'python_2.0.28'
        assert body['sys_id'] == 'offline-system' and body['product_id'] == 'offline-product'
        flag, _ = rsa_design(body['sign'], json.dumps(body['data'], ensure_ascii=False, separators=(',', ':')), public)
        assert flag, 'final body signature does not match retained caller fields'
        captured.append((ApiRequest.request_url, headers, body))
        return body

    with patch.object(socket.socket, 'connect', side_effect=AssertionError('network forbidden')), patch.object(ApiRequest, 'post', side_effect=final_body):
        for module, route in ROUTES.items():
            mod = importlib.import_module('dg_sdk.request.' + module + '_request')
            cls = next(value for name, value in vars(mod).items() if name.endswith('Request') and name != 'ApiRequest' and isinstance(value, type))
            obj = cls()
            obj.huifu_id = 'offline-actor'
            if hasattr(obj, 'req_date'): obj.req_date = '20261104'
            if hasattr(obj, 'req_seq_id'): obj.req_seq_id = 'offline-original-seq'
            extra = {'empty_string': '', 'empty_list': [], 'empty_dict': {}, 'empty_none': None, 'zero': 0, 'flag': False}
            obj.post(extra)
            url, headers, body = captured[-1]
            assert url.endswith(route)
            data = body['data']
            assert data['huifu_id'] == 'offline-actor' and data['zero'] == 0 and data['flag'] is False
            assert not set(extra).difference({'zero', 'flag'}) & data.keys()
            if hasattr(obj, 'req_date'): assert data['req_date'] == '20261104'
            else: assert 'req_date' not in data
            if hasattr(obj, 'req_seq_id'): assert data['req_seq_id'] == 'offline-original-seq'
            else: assert 'req_seq_id' not in data
            # Observe SDK's real overwrite behavior; public guidance requires a caller guard.
            obj.post({'huifu_id': 'offline-collision-actor'})
            assert captured[-1][2]['data']['huifu_id'] == 'offline-collision-actor'
        query_module = importlib.import_module('dg_sdk.request.v2_trade_settlement_query_request')
        for locator in ('org_hf_seq_id', 'org_req_seq_id'):
            query = query_module.V2TradeSettlementQueryRequest()
            query.huifu_id = 'offline-actor'
            query.org_req_date = '20261104'
            setattr(query, locator, 'offline-original-locator')
            query.post({})
            data = captured[-1][2]['data']
            assert data == {'huifu_id': 'offline-actor', 'org_req_date': '20261104', locator: 'offline-original-locator'}
        batch_module = importlib.import_module('dg_sdk.request.v2_trade_batchtranslog_query_request')
        regular = batch_module.V2TradeBatchtranslogQueryRequest()
        regular.huifu_id = 'offline-actor'
        regular.begin_date = '20261101'
        regular.end_date = '20261104'
        regular.post({})
        assert captured[-1][2]['data'] == {'huifu_id': 'offline-actor', 'begin_date': '20261101', 'end_date': '20261104'}
        batch = batch_module.V2TradeBatchtranslogQueryRequest()
        batch.post({'payment_hf_seq_id': 'offline-ts-payment'})
        assert captured[-1][2]['data'] == {'payment_hf_seq_id': 'offline-ts-payment'}
        # This proves SDK expression only. The formal Y/conditional exception remains unresolved.
    cipher = rsa_long_encrypt('synthetic-account', public)
    assert len(base64.b64decode(cipher, validate=True)) == pair.size_in_bytes()
    error = rsa_long_encrypt('synthetic-account', 'invalid-public-key')
    assert error, 'probe requires a nonempty SDK error string'
    try:
        decoded = base64.b64decode(error, validate=True)
        assert len(decoded) % pair.size_in_bytes() == 0 and decoded
    except (ValueError, AssertionError):
        pass
    else:
        raise AssertionError('encryption error string accepted as ciphertext')
    print('Payout SDK offline transport passed: six real Python chains, final object data, RSA signature/headers, empty pruning, preserved IDs, six declared-key collision probes, two original locators, TS batch omission, encryption error control; network calls=0')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk-root', required=True, type=Path)
    validate(parser.parse_args().sdk_root.resolve())


if __name__ == '__main__': main()
