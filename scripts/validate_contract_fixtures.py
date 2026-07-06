#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_BUNDLE = "huifu-pay-integration-1.3.0-r4"
CONTRACT_ROOT = REPO_ROOT / "local-sandbox" / "contracts" / CONTRACT_BUNDLE
ENDPOINT_CONTRACTS = CONTRACT_ROOT / "endpoint-contracts.json"
FIXTURES_ROOT = CONTRACT_ROOT / "fixtures"


class State:
    def __init__(self) -> None:
        self.errors = 0

    def ok(self, message: str) -> None:
        print(f"OK:    {message}")

    def error(self, message: str) -> None:
        print(f"ERROR: {message}")
        self.errors += 1


def endpoint_fixture_ids(endpoint: dict) -> list[str]:
    """对齐 contracts.go 的 endpointFixtureIDs：positive + negative + variant，去空去重、保序。"""
    ids = [endpoint.get("positive_fixture", ""), endpoint.get("negative_fixture", "")]
    ids.extend(endpoint.get("variant_fixtures", []) or [])
    out: list[str] = []
    seen: set[str] = set()
    for fixture_id in ids:
        if not fixture_id or fixture_id in seen:
            continue
        seen.add(fixture_id)
        out.append(fixture_id)
    return out


def main() -> int:
    state = State()
    print("=== 契约 fixture 引用完整性校验 ===\n")

    if not ENDPOINT_CONTRACTS.is_file():
        state.error(f"缺少 endpoint 契约文件: {relative(ENDPOINT_CONTRACTS)}")
        print(f"\n=== 结果: {state.errors} errors ===")
        return state.errors
    if not FIXTURES_ROOT.is_dir():
        state.error(f"缺少 fixtures 目录: {relative(FIXTURES_ROOT)}")
        print(f"\n=== 结果: {state.errors} errors ===")
        return state.errors

    contracts = json.loads(ENDPOINT_CONTRACTS.read_text(encoding="utf-8"))
    endpoints = contracts.get("endpoints", [])

    # 反查：每个 endpoint 引用的 fixture id 必须存在 fixtures/<id>.json
    referenced: dict[str, list[str]] = {}
    checked = 0
    for endpoint in endpoints:
        endpoint_id = endpoint.get("id", "<无 id>")
        for fixture_id in endpoint_fixture_ids(endpoint):
            checked += 1
            referenced.setdefault(fixture_id, []).append(endpoint_id)
            fixture_path = FIXTURES_ROOT / f"{fixture_id}.json"
            if not fixture_path.is_file():
                state.error(
                    f"{endpoint_id} 引用的 fixture 缺失文件: {relative(fixture_path)}"
                )

    # 反查孤儿：fixtures 目录里存在但无任何 endpoint 引用的文件。
    # 依据 contracts.go(validateContractBundle 第 350-354 行)：所有 fixture 均须被某个
    # endpoint 引用，Go 侧对未引用文件一律报错，故不存在合法的非 endpoint 关联 fixture。
    # 判定口径：以文件内部 id 字段为准(与 Go 一致，Go 按 fixture.ID 建索引)。
    orphans: list[str] = []
    fixture_files = sorted(FIXTURES_ROOT.glob("*.json"))
    for fixture_path in fixture_files:
        try:
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            state.error(f"fixture 文件解析失败 {relative(fixture_path)}: {exc}")
            continue
        fixture_id = fixture.get("id", "")
        if not fixture_id:
            state.error(f"fixture 文件缺少 id 字段: {relative(fixture_path)}")
            continue
        if fixture_id not in referenced:
            orphans.append(relative(fixture_path))

    for orphan in orphans:
        state.error(f"孤儿 fixture（无任何 endpoint 引用）: {orphan}")

    if state.errors == 0:
        state.ok(
            f"{len(endpoints)} 个 endpoint 共引用 {checked} 个 fixture、"
            f"{len(fixture_files)} 个 fixture 文件全部匹配，无缺失、无孤儿"
        )

    print(f"\n=== 结果: {state.errors} errors ===")
    return state.errors


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    sys.exit(main())
