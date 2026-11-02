#!/usr/bin/env python3
"""Generate the packaged payment source-lock index from the maintainer lock."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validation_runtime import require_assertions_enabled
from skill_validation_config import PAYMENT_SOURCE_LOCK


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
LOCK = PAYMENT_SOURCE_LOCK
OUTPUT = ROOT / "huifu-pay-integration/references/official-payment-page-lock.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when the packaged index differs from the source lock.",
    )
    args = parser.parse_args()
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "skills-manifest.json").read_text())
    additions_name = manifest["skills"]["huifu-pay-integration"].get("additional_source_lock")
    sources = list(lock["sources"])
    if additions_name:
        additions = json.loads((ROOT / additions_name).read_text())
        sources += [{**source, "local_reference": source["reference"]} for source in additions["sources"]]
    lines = [
        "# 支付官方接口页来源锁",
        "",
        f"- 来源快照日期：`{lock['source_date']}`",
        f"- 页面数：`{len(sources)}`（基础{lock['source_count']}页；本轮新增{len(sources)-lock['source_count']}页）",
        "- 用途：复核字段、类型、长度、必填条件和接口边界；普通接入回答仍使用对应原子 reference。",
        "",
        "| 页面 | 官方 URL | 本地原子 reference | SHA-256 |",
        "| --- | --- | --- | --- |",
    ]
    for item in sources:
        lines.append(
            f"| {item['title']} | {item['url']} | "
            f"`{item['local_reference']}` | `{item['sha256']}` |"
        )
    lines.extend(
        [
            "",
            "## 使用规则",
            "",
            "1. 本表只证明指定快照与本地原子 reference 的映射，不代表运行时实时访问官网。",
            "2. 字段口径冲突时，保留官方原文事实并在对应原子 reference 说明疑义和待确认适配点，继续已明确部分；不得静默猜测。",
            "3. 刷新必须重新生成维护者来源锁与本文件，并通过独立来源契约校验。",
            "4. 下载链接、密钥、签名和真实商户数据不得写入来源锁。",
            "",
        ]
    )
    rendered = "\n".join(lines)
    if args.check:
        assert OUTPUT.read_text(encoding="utf-8") == rendered, (
            "official payment page index is stale; regenerate it"
        )
        print(f"payment source index is current: {OUTPUT.relative_to(ROOT)}")
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"generated {OUTPUT.relative_to(ROOT)} from {len(sources)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
