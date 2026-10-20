#!/usr/bin/env python3
"""Download and lock official payment documents without overwriting snapshots."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Source:
    key: str
    title: str
    filename: str
    url: str
    local_reference: str


def source(
    key: str, title: str, url: str, local_reference: str, suffix: str = ".md"
) -> Source:
    return Source(key, title, f"{key}{suffix}", url, local_reference)


SOURCES = (
    source("lightning-intro", "极速版介绍", "https://paas.huifu.com/partners/lightning/jsb/jsbjs.md", "aggregation-base.md"),
    source("lightning-quickstart", "极速版快速开始", "https://paas.huifu.com/partners/lightning/jsb/ksks.md", "aggregation-quickstart.md"),
    source("wx-jsapi-intro", "微信公众号支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/wx_gzh_intro.md", "aggregation-order-method-wechat.md"),
    source("wx-jsapi-guide", "微信公众号支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/wx_gzh_kfzy.md", "aggregation-order-method-wechat.md"),
    source("wx-mini-intro", "微信小程序支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/wx_xcx_intro.md", "aggregation-order-method-wechat.md"),
    source("wx-mini-guide", "微信小程序支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/wx_xcx_kfzy.md", "aggregation-order-method-wechat.md"),
    source("wx-micropay-intro", "微信付款码支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/wx_fkm_intro.md", "aggregation-order-method-wechat.md"),
    source("wx-micropay-guide", "微信付款码支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/wx_fkm_kfzy.md", "aggregation-order-method-wechat.md"),
    source("alipay-js-intro", "支付宝JS支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/zfb_js_intro.md", "aggregation-order-method-alipay.md"),
    source("alipay-js-guide", "支付宝JS支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/zfb_js_kfzy.md", "aggregation-order-method-alipay.md"),
    source("alipay-native-intro", "支付宝正扫支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/zfb_zs_intro.md", "aggregation-order-method-alipay.md"),
    source("alipay-native-guide", "支付宝正扫支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/zfb_zs_kfzy.md", "aggregation-order-method-alipay.md"),
    source("alipay-micropay-intro", "支付宝付款码支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/zfb_fkm_intro.md", "aggregation-order-method-alipay.md"),
    source("alipay-micropay-guide", "支付宝付款码支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/zfb_fkm_kfzy.md", "aggregation-order-method-alipay.md"),
    source("unionpay-js-intro", "银联JS支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/yl_js_intro.md", "aggregation-order-method-unionpay.md"),
    source("unionpay-js-guide", "银联JS支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/yl_js_kfzy.md", "aggregation-order-method-unionpay.md"),
    source("unionpay-native-intro", "银联正扫支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/yl_zs_intro.md", "aggregation-order-method-unionpay.md"),
    source("unionpay-native-guide", "银联正扫支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/yl_zs_kfzy.md", "aggregation-order-method-unionpay.md"),
    source("unionpay-micropay-intro", "银联付款码支付-产品介绍", "https://paas.huifu.com/partners/lightning/jsb/zf/yl_fkm_intro.md", "aggregation-order-method-unionpay.md"),
    source("unionpay-micropay-guide", "银联付款码支付-开发指引", "https://paas.huifu.com/partners/lightning/jsb/zf/yl_fkm_kfzy.md", "aggregation-order-method-unionpay.md"),
    source("aggregation-create", "聚合支付下单", "https://paas.huifu.com/partners/lightning/api/jhzfxd.md", "aggregation-order-request.md"),
    source("aggregation-query", "聚合交易查询", "https://paas.huifu.com/partners/lightning/api/jyddcx.md", "aggregation-query-payment-query.md"),
    source("aggregation-close", "聚合交易关单", "https://paas.huifu.com/partners/lightning/api/jygd.md", "aggregation-query-trade-close.md"),
    source("aggregation-close-query", "聚合交易关单查询", "https://paas.huifu.com/partners/lightning/api/jygdcx.md", "aggregation-query-close-query.md"),
    source("aggregation-refund", "聚合交易退款", "https://paas.huifu.com/partners/lightning/api/jytk.md", "aggregation-refund.md"),
    source("aggregation-refund-query", "聚合交易退款查询", "https://paas.huifu.com/partners/lightning/api/jytkcx.md", "aggregation-refund-query.md"),
    source("reconciliation-v2", "对账单-v2详细API", "https://paas.huifu.com/partners/api/doc/jyjs/api_jyjs_wjcx.md", "aggregation-query-reconciliation.md"),
    source("hosting-h5", "H5/PC预下单", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hosting.md", "hostingpay-preorder-h5-pc.md"),
    source("hosting-alipay-mini", "支付宝小程序预下单", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_zfbpreorder.md", "hostingpay-preorder-alipay-mini.md"),
    source("hosting-wechat-mini", "微信小程序预下单", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_wxpreorder.md", "hostingpay-preorder-wechat-mini.md"),
    source("hosting-douyin", "抖音直连下单", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_dypreorder.md", "hostingpay-preorder-douyin-direct.md"),
    source("hosting-query", "托管交易查询", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingcx.md", "hostingpay-query-payment-status-query.md"),
    source("hosting-refund", "托管交易退款", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingtk.md", "hostingpay-refund.md"),
    source("hosting-refund-query", "托管交易退款查询", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingtkcx.md", "hostingpay-refund-query.md"),
    source("hosting-close", "托管交易关单", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostinggd.md", "hostingpay-query-trade-close.md"),
    source("hosting-splitpay-query", "拆单支付订单查询", "https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingcdzf.md", "hostingpay-query-splitpay.md"),
    source("split-detail-query", "交易分账明细查询", "https://paas.huifu.com/partners/api/doc/smzf/api_fzmxcx.md", "trade-split-detail-query.md"),
    source("balance-pay", "余额支付", "https://paas.huifu.com/partners/api/doc/yuer/api_acctpayzf.md", "balancepay-pay.md"),
    source("balance-pay-query", "余额支付查询", "https://paas.huifu.com/partners/api/doc/yuer/api_acctpaycx.md", "balancepay-query.md"),
    source("balance-refund", "余额支付退款", "https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytk.md", "balancepay-refund.md"),
    source("balance-refund-query", "余额支付退款查询", "https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytkcx.md", "balancepay-refund-query.md"),
    source("fee-calc", "手续费试算", "https://paas.huifu.com/partners/api/doc/sxf/api_sxf_sxfss.md", "balancepay-fee-calc.md"),
    source("pay-relation", "付款关系提交", "https://paas.huifu.com/partners/api/doc/yuer/api_acct_fkgxtj.md", "balancepay-pay-relation.md"),
    source("balance-sms", "余额支付发送短信验证码", "https://paas.huifu.com/partners/api/doc/yuer/api_smscode.md", "balancepay-sms.md"),
)


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": "huifu-payment-skill-source-refresh/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def semantic_digest(raw: bytes) -> str:
    text = raw.decode("utf-8-sig")
    text = text.replace("\r\n", "\n")
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def page_update(raw: bytes) -> str | None:
    text = raw.decode("utf-8-sig")
    match = re.search(r"最近更新时间[：:]\s*(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})", text)
    if match is None:
        return None
    year, month, day = match.groups()
    return f"{year}-{int(month):02d}-{int(day):02d}"


def default_lock_path(source_date: str) -> Path:
    return ROOT / f"maintainer-contracts/payment-source-lock-{source_date}.json"


def ensure_mutable_lock(path: Path) -> None:
    historical_lock = ROOT / "maintainer-contracts/payment-source-lock.json"
    if path.resolve() == historical_lock.resolve() or path.exists():
        raise ValueError("existing payment source locks are immutable; choose a new snapshot date")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--lock",
        type=Path,
        help="Versioned lock output; defaults to payment-source-lock-<source-date>.json.",
    )
    parser.add_argument("--previous-lock", type=Path, help="Predecessor lock; defaults to the active manifest lock.")
    args = parser.parse_args()
    lock_path = args.lock or default_lock_path(args.source_date)
    try:
        ensure_mutable_lock(lock_path)
    except ValueError as exc:
        parser.error(str(exc))

    output_dir = args.output_dir or (
        ROOT / "maintainer-contracts/official-sources/payment" / args.source_date
    )
    if output_dir.exists() and any(output_dir.iterdir()):
        parser.error("existing payment source snapshot is immutable")
    output_dir.mkdir(parents=True, exist_ok=True)

    locked: list[dict[str, object]] = []
    for item in SOURCES:
        raw = fetch(item.url)
        (output_dir / item.filename).write_bytes(raw)
        locked.append(
            {
                "key": item.key,
                "title": item.title,
                "filename": item.filename,
                "url": item.url,
                "local_reference": item.local_reference,
                "page_updated_at": page_update(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "semantic_sha256": semantic_digest(raw),
            }
        )

    manifest = json.loads((ROOT / "skills-manifest.json").read_text())
    previous_lock = args.previous_lock or ROOT / manifest["skills"]["huifu-pay-integration"]["source_lock"]
    previous = {item["key"]: item for item in json.loads(previous_lock.read_text())["sources"]}
    payload = {
        "schema_version": 1,
        "source_date": args.source_date,
        "source_snapshot_id": args.source_date,
        "verified_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
        "source_count": len(locked),
        "previous_source_lock": {
            "path": str(previous_lock.relative_to(ROOT)),
            "sha256": hashlib.sha256(previous_lock.read_bytes()).hexdigest(),
        },
        "sources": locked,
        "current_extension": {
            "refresh_id": f"api-refresh-payment-online-review-{args.source_date}",
            "changed_source_keys": [item["key"] for item in locked if item["key"] in previous and item["sha256"] != previous[item["key"]]["sha256"]],
            "added_source_keys": [item["key"] for item in locked if item["key"] not in previous],
            "review_status": "pending-independent-field-and-semantic-review",
            "document_conflicts": [],
        },
    }
    lock_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"locked {len(locked)} payment sources in {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
