#!/usr/bin/env python3
"""Generate the packaged payment source-lock index from the maintainer lock."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validation_runtime import require_assertions_enabled


require_assertions_enabled()


ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "maintainer-contracts/payment-source-lock.json"
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
    lines = [
        "# 支付官方接口页来源锁",
        "",
        f"- 来源快照日期：`{lock['source_date']}`",
        f"- 页面数：`{lock['source_count']}`",
        "- 用途：复核字段、类型、长度、必填条件和接口边界；普通接入回答仍使用对应原子 reference。",
        "",
        "| 页面 | 官方 URL | 本地原子 reference | SHA-256 |",
        "| --- | --- | --- | --- |",
    ]
    for item in lock["sources"]:
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
            "2. 字段口径冲突时，先保留官方原文事实，再把冲突和生产硬停写入对应原子 reference；不得静默猜测。",
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
    print(f"generated {OUTPUT.relative_to(ROOT)} from {lock['source_count']} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
