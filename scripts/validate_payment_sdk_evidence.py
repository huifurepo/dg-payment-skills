#!/usr/bin/env python3
"""Validate T7 transaction split-detail query evidence in the three SDK trees."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from validation_runtime import require_assertions_enabled


require_assertions_enabled()


def read(path: Path) -> str:
    assert path.is_file(), f"missing SDK evidence: {path}"
    return path.read_text(encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.sdk_root.resolve()

    java_root = root / "bspay-java-sdk-parent-generator-sdk/opps-bspay-java-sdk/src/main/java/com/huifu/bspay/sdk/opps"
    java_request = read(java_root / "core/request/V2TradeTransSplitQueryRequest.java")
    java_enum = read(java_root / "core/enums/FunctionCodeEnum.java")
    java_client = read(java_root / "client/BasePayClient.java")
    assert set(re.findall(r'@JSONField\(name = "([^"]+)"\)', java_request)) == {
        "hf_seq_id", "huifu_id", "ord_type"
    }
    assert 'V2_TRADE_TRANS_SPLIT_QUERY("v2.trade.trans.split.query"' in java_enum
    assert "params.putAll(request.getExtendInfos())" in java_client

    php_root = root / "bspay-php-sdk-feature_generator_sdk/BsPaySdk"
    php_request = read(php_root / "request/V2TradeTransSplitQueryRequest.php")
    php_enum = read(php_root / "enums/FunctionCodeEnum.php")
    php_client = read(php_root / "core/BsPayClient.php")
    assert set(re.findall(r"private \$(hfSeqId|huifuId|ordType);", php_request)) == {
        "hfSeqId", "huifuId", "ordType"
    }
    assert "V2_TRADE_TRANS_SPLIT_QUERY = 'v2/trade/trans/split/query'" in php_enum
    assert "array_merge($arrayData, $extendInfos)" in php_client

    python_root = root / "bspay-python-sdk-feature_generator_sdk/dg_sdk/request"
    python_request = read(python_root / "v2_trade_trans_split_query_request.py")
    python_urls = read(python_root / "request_api_urls.py")
    declared = set(re.findall(r"^    (hf_seq_id|huifu_id|ord_type) = \"\"$", python_request, re.M))
    assert declared == {"hf_seq_id", "huifu_id", "ord_type"}
    assert 'V2_TRADE_TRANS_SPLIT_QUERY = "/v2/trade/trans/split/query"' in python_urls
    assert "required_params.update(extend_infos)" in python_request

    reference = read(
        Path(__file__).resolve().parent.parent
        / "huifu-pay-integration/references/trade-split-detail-query.md"
    )
    for token in (
        "V2TradeTransSplitQueryRequest",
        "v2/trade/trans/split/query",
        "扩展映射必须为空",
        "split_trans_responses",
        "String(JSON Array)",
        "未知附加字段",
        "dcab5eb128a7987742ea339631add74ad771227d3ce557c1154d6d6a27266270",
    ):
        assert token in reference

    print("payment SDK evidence validated: split-detail query Java/PHP/Python")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
