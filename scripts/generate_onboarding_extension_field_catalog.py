#!/usr/bin/env python3
"""Generate the complete field catalog for the twelve onboarding extensions."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path

import generate_user_onboarding_field_catalog as base
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
from skill_validation_config import ONBOARDING_EXTENSION_SOURCE_LOCK
LOCK = ONBOARDING_EXTENSION_SOURCE_LOCK
DEFAULT_OUTPUT = (
    ROOT
    / "huifu-merchant-onboarding/references/onboarding-extension-complete-field-catalog.md"
)


def spec(
    key: str,
    title: str,
    filename: str,
    url: str,
    surfaces: tuple[tuple[str, str], ...],
) -> base.SourceSpec:
    return base.SourceSpec(key, title, filename, url, surfaces)


SOURCES = (
    spec(
        "contract_resend",
        "电子合同重发",
        "contract-resend.md",
        "https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtcf.md",
        (
            ("请求信封", "request"),
            ("请求 data", "request.data"),
            ("响应信封", "response"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "contract_list_query",
        "电子合同列表查询",
        "contract-list-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtsqlbcx.md",
        (
            ("请求信封", "request"),
            ("请求 data", "request.data"),
            ("响应信封", "response"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "contract_reject",
        "电子合同拒签",
        "contract-reject.md",
        "https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtjq.md",
        (
            ("请求信封", "request"),
            ("请求 data", "request.data"),
            ("响应信封", "response"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "lower_merchant_permission",
        "开通下级商户权限配置",
        "lower-merchant-permission.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_xjshpz.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "unified_web_onboarding",
        "商户统一进件（页面版）",
        "unified-web-onboarding.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shtyjjweb.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("异步通知信封", "async"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
            ("审核异步 data", "async.audit.data"),
            ("业务异步 data", "async.business.data"),
        ),
    ),
    spec(
        "unified_web_query",
        "统一进件页面版查询",
        "unified-web-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shtyjjwebcx.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "wechat_config",
        "微信商户配置",
        "wechat-config.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxshpz.md",
        (
            ("请求信封", "request"),
            ("请求 data", "request.data"),
            ("同步响应信封", "response"),
            ("同步响应 data", "response.data"),
            ("异步通知信封", "async"),
            ("异步通知 data", "async.data"),
        ),
    ),
    spec(
        "wechat_config_query",
        "微信商户配置查询",
        "wechat-config-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxshpzcx.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "wechat_realname",
        "微信实名认证",
        "wechat-realname.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrz.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "wechat_realname_query",
        "微信实名认证状态查询",
        "wechat-realname-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrzztcx.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "alipay_realname",
        "支付宝实名申请提交",
        "alipay-realname.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmrz.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
    spec(
        "alipay_realname_query",
        "支付宝实名申请单查询",
        "alipay-realname-query.md",
        "https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmcx.md",
        (
            ("请求信封", "request"),
            ("响应信封", "response"),
            ("请求 data", "request.data"),
            ("同步响应 data", "response.data"),
        ),
    ),
)


def fetch(url: str) -> bytes:
    return base.fetch(url)


def locked_source_dir() -> Path:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    snapshot_id = lock.get("source_snapshot_id", lock["source_date"])
    return ROOT / "maintainer-contracts/official-sources/onboarding-extension" / snapshot_id


def refresh_sources(target: Path, source_key: str | None = None) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        if source_key is not None and source.key != source_key:
            continue
        (target / source.filename).write_bytes(fetch(source.url))


def render_source(source: base.SourceSpec, content: bytes) -> tuple[str, dict[str, object]]:
    """Support the two evidenced WeChat layouts without guessing directions."""
    if source.key == "wechat_config":
        roots, _ = base.parse_tables(content.decode("utf-8-sig"), source.url)
        if len(roots) == 4:
            source = replace(source, surfaces=(
                ("请求信封", "request"), ("请求 data", "request.data"),
                ("同步响应 data", "response.data"), ("异步通知 data", "async.data"),
            ))
        elif len(roots) != 6:
            raise ValueError(f"unrecognized WeChat configuration layout: {len(roots)} roots")
    return base.render_source(source, content)


def build_catalog(source_dir: Path) -> tuple[str, dict[str, dict[str, object]]]:
    sections: list[str] = []
    summaries: dict[str, dict[str, object]] = {}
    for source in SOURCES:
        content = (source_dir / source.filename).read_bytes()
        section, summary = render_source(source, content)
        sections.append(section)
        summaries[source.key] = summary

    summary_rows = [
        f"| {source.title} | {summaries[source.key]['total_fields']} | "
        f"{summaries[source.key]['extend_tables']} | {summaries[source.key]['max_depth']} |"
        for source in SOURCES
    ]
    header = """# 进件扩展十二接口完整字段目录

本文件由仓库维护脚本从锁定的十二份官方原文机械生成，覆盖电子合同、下级商户权限、统一页面进件及微信/支付宝 AT 管理。条件必填、官方冲突、路由和 SDK 边界仍须同时读取对应原子接口 reference 与 `onboarding-extension-field-contracts.md`。

安全说明：官网说明中的证件号、手机号、邮箱、密钥、二维码、合同链接和长流水已机械脱敏；字段名、枚举、条件、材料编号和资料链接保持原文。

## 目录

- [使用规则](#使用规则)
- [生成覆盖摘要](#生成覆盖摘要)
- [电子合同接口](#电子合同重发)
- [页面进件与下级权限](#开通下级商户权限配置)
- [微信与支付宝 AT 管理](#微信商户配置)

## 使用规则

1. 十二个接口都保留独立 DTO；不得因同属进件流程而复用商户详情、用户开户或支付交易模型。
2. 按完整路径区分同名字段；String(JSON) 仅按接口级合同编码，不能由 `*_list` 名称猜测。
3. 官网类型、长度、必填、字段名与示例冲突时，目录保留正式参数表原值并标记官方证据，不以示例覆盖。
4. 微信/支付宝实名、页面进件和配置异步通知分别建模；未声明的 ACK、重试、超时和验签原文保持 `[需要官方确认]`。

## 生成覆盖摘要

| 接口 | 字段路径总数 | 扩展表数量 | 最大路径深度 |
| --- | ---: | ---: | ---: |
"""
    catalog = header + "\n".join(summary_rows) + "\n\n" + "\n".join(sections)
    return catalog.rstrip() + "\n", summaries


def validate_summary(summary: dict[str, dict[str, object]]) -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    by_key = {source["key"]: source for source in lock["sources"]}
    assert set(summary) == set(by_key)
    for key, item in summary.items():
        expected = by_key[key]
        assert item["sha256"] == expected["sha256"], f"{key}: digest mismatch"
        assert item["total_fields"] == expected["field_count"], (
            f"{key}: field count mismatch"
        )
    assert sum(item["total_fields"] for item in summary.values()) == lock["totals"]["fields"]
    assert sum(item["root_tables"] for item in summary.values()) == lock["totals"]["root_tables"]
    assert sum(item["extend_tables"] for item in summary.values()) == lock["totals"]["extend_tables"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--locked-source-dir", action="store_true")
    parser.add_argument("--refresh-source-dir", type=Path)
    parser.add_argument("--refresh-source-key", choices=[source.key for source in SOURCES])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    selected = sum(
        value is not None and value is not False
        for value in (args.source_dir, args.locked_source_dir, args.refresh_source_dir)
    )
    if selected > 1:
        parser.error("source selection options are mutually exclusive")
    source_dir = args.source_dir or locked_source_dir()
    if args.refresh_source_dir is not None:
        refresh_sources(args.refresh_source_dir, args.refresh_source_key)
        source_dir = args.refresh_source_dir
    elif args.refresh_source_key is not None:
        parser.error("--refresh-source-key requires --refresh-source-dir")
    catalog, summary = build_catalog(source_dir)
    validate_summary(summary)
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != catalog:
            print(f"catalog is stale: {args.output}", file=sys.stderr)
            return 1
        print(f"catalog is current: {args.output}")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(catalog, encoding="utf-8")
        print(f"generated: {args.output}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
