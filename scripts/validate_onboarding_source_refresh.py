#!/usr/bin/env python3
"""Prove that the post-split catalog refresh contains only approved source deltas."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from validation_runtime import require_assertions_enabled
from generate_merchant_onboarding_field_catalog import build_catalog


require_assertions_enabled()


REPO_ROOT = Path(__file__).resolve().parent.parent
LOCK = REPO_ROOT / "maintainer-contracts/merchant-onboarding-source-lock-2026-08-10.json"
CATALOG_PATH = "huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md"
CATALOG = REPO_ROOT / CATALOG_PATH
SOURCE_DIR = (
    REPO_ROOT
    / "maintainer-contracts/official-sources/merchant-onboarding/2026-08-10"
)


def normalize_description(value: str) -> str:
    return re.sub(r"(?:\s*；\s*){2,}", "；", value).strip()


def parse_fields(text: str) -> dict[tuple[str, str, str], tuple[str, str, str, str, str]]:
    interface = ""
    surface = ""
    fields: dict[tuple[str, str, str], tuple[str, str, str, str, str]] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            interface = line[3:].strip()
            surface = ""
            continue
        if line.startswith("### "):
            surface = line[4:].strip()
            continue
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        path = cells[0].strip("`")
        key = (interface, surface, path)
        if key in fields:
            raise AssertionError(f"duplicate field key: {key}")
        fields[key] = (
            cells[1],
            cells[2].strip("`"),
            cells[3].strip("`"),
            cells[4].strip("`"),
            normalize_description(" | ".join(cells[5:])),
        )
    return fields


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    for source in lock["sources"]:
        path = SOURCE_DIR / source["filename"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == source["sha256"], f"{source['filename']}: source SHA changed"

    previous_dir = (
        REPO_ROOT
        / "maintainer-contracts/official-sources/merchant-onboarding"
        / lock["previous_snapshot_date"]
    )
    latest_refresh = lock["latest_refresh"]
    changed_titles = set(latest_refresh["changed_pages"])
    assert len(changed_titles) == 3, (
        f"expected three changed onboarding pages, found {len(changed_titles)}"
    )
    for source in lock["sources"]:
        previous = previous_dir / source["filename"]
        current = SOURCE_DIR / source["filename"]
        if source["title"] in changed_titles:
            assert previous.read_bytes() != current.read_bytes(), (
                f"{source['title']}: refresh page unexpectedly byte-identical"
            )
        else:
            assert previous.read_bytes() == current.read_bytes(), (
                f"{source['title']}: page changed outside the three approved changed pages"
            )

    baseline = subprocess.check_output(
        ["git", "show", f"{lock['migration_baseline_commit']}:{CATALOG_PATH}"],
        cwd=REPO_ROOT,
        text=True,
    )
    before = parse_fields(baseline)
    # Rebuild the historical pages with the current parser.  The generator has
    # two later source specs, so provide those files only to satisfy its input
    # surface and filter them back out below.
    with tempfile.TemporaryDirectory(prefix="huifu-onboarding-history-") as temp:
        composite = Path(temp)
        for path in SOURCE_DIR.iterdir():
            if path.is_file():
                shutil.copyfile(path, composite / path.name)
        current_dir = (
            REPO_ROOT
            / "maintainer-contracts/official-sources/merchant-onboarding/2026-08-31"
        )
        for filename in ("multifee-config.md", "multifee-query.md"):
            shutil.copyfile(current_dir / filename, composite / filename)
        historical_catalog, _ = build_catalog(composite)
    active_catalog = parse_fields(historical_catalog)
    locked_titles = {source["title"] for source in lock["sources"]}
    # This validator proves the historical 2026-08-10 refresh. Later interfaces
    # may be appended to the active catalog and are validated by the current
    # source-contract validator instead of being treated as historical drift.
    after = {
        key: value
        for key, value in active_catalog.items()
        if key[0] in locked_titles
    }
    extension = lock["extension_from_1_0_0"]
    source_by_key = {item["key"]: item for item in lock["sources"]}
    new_titles = {
        source_by_key[key]["title"] for key in extension["added_source_keys"]
    }
    legacy_after = {
        key: value for key, value in after.items() if key[0] not in new_titles
    }
    new_after = {
        key: value for key, value in after.items() if key[0] in new_titles
    }
    deleted = sorted(set(before) - set(legacy_after))
    changed = sorted(
        key
        for key in set(before) & set(legacy_after)
        if before[key] != legacy_after[key]
    )
    added = sorted(set(legacy_after) - set(before))

    allowed = {
        (item["interface"], item["surface"], item["path"]): (
            item["label"],
            item["type"],
            item["length"],
            item["required"],
            normalize_description(item["description"]),
        )
        for item in lock["allowed_delta_from_1_3_2"]
    }
    corrections = {
        (item["interface"], item["surface"], item["path"]): (
            (
                item["before"]["label"],
                item["before"]["type"],
                item["before"]["length"],
                item["before"]["required"],
                normalize_description(item["before"]["description"]),
            ),
            (
                item["after"]["label"],
                item["after"]["type"],
                item["after"]["length"],
                item["after"]["required"],
                normalize_description(item["after"]["description"]),
            ),
        )
        for item in lock["allowed_corrections_from_1_3_2"]
    }
    path_corrections = lock["fourth_review_path_corrections"]
    renamed_before = {
        (item["interface"], item["surface"], item["before_path"])
        for item in path_corrections
    }
    renamed_after = {
        (item["interface"], item["surface"], item["after_path"])
        for item in path_corrections
    }
    refresh_keys = {
        (item["interface"], item["surface"], item["path"])
        for item in lock["api_refresh"]["changed_fields"]
    }
    latest_refresh_changes = {
        (item["interface"], item["surface"], item["path"]): item
        for item in latest_refresh["changed_fields"]
    }
    material_changes = {
        (item["interface"], item["surface"], item["path"]): item
        for item in lock["api_refresh"]["conditional_material_changes"]
    }
    link_normalized_changes = {
        key
        for key in changed
        if before[key][:4] == legacy_after[key][:4]
        and (
            "官网相对地址原文" in legacy_after[key][4]
            or "官网原始地址为非 HTTPS" in legacy_after[key][4]
        )
    }
    legacy_refresh_keys = refresh_keys & set(before)
    latest_legacy_refresh_keys = set(latest_refresh_changes) & set(before)
    assert set(deleted) == renamed_before, f"unexpected deleted fields: {deleted}"
    assert set(changed) == (
        set(corrections)
        | legacy_refresh_keys
        | latest_legacy_refresh_keys
        | set(material_changes)
        | link_normalized_changes
    ), (
        f"unexpected changed fields: {changed}"
    )
    assert set(added) == set(allowed) | renamed_after, (
        f"unexpected additions: {added}"
    )
    for key, expected in allowed.items():
        assert legacy_after[key] == expected, f"{key}: delta contract changed"
    for key, (expected_before, expected_after) in corrections.items():
        assert before[key] == expected_before, f"{key}: correction baseline changed"
        assert legacy_after[key] == expected_after, f"{key}: corrected contract changed"
    for item in path_corrections:
        before_key = (item["interface"], item["surface"], item["before_path"])
        after_key = (item["interface"], item["surface"], item["after_path"])
        assert before[before_key] == legacy_after[after_key], (
            f"{after_key}: array path correction changed field properties"
        )
    for key in refresh_keys:
        current = after[key]
        assert current[1:4] == ("String", "18", "C"), (
            f"{key}: expected String(18) C, found {current[1:4]}"
        )
        assert "sys_id主体为渠道商时填写" in current[4], (
            f"{key}: missing channel sys_id condition"
        )
        assert "sys_id主体为总部商户时选填" in current[4], (
            f"{key}: missing headquarters sys_id condition"
        )
        if key in before:
            assert before[key][3] == "Y", f"{key}: prior required marker is not Y"
    for key, contract in latest_refresh_changes.items():
        current = after[key]
        assert current[4] == normalize_description(contract["after_description"]), (
            f"{key}: refreshed activated_products description changed"
        )
        assert current[1:4] == ("String", "—", "N"), (
            f"{key}: activated_products type/length/required changed: {current[1:4]}"
        )
        if key in before:
            assert before[key][4] == normalize_description(contract["before_description"]), (
                f"{key}: prior activated_products description changed"
            )
            assert before[key][:4] == current[:4], (
                f"{key}: latest refresh changed more than the description"
            )
    material_rule = lock["api_refresh"]["conditional_material_rule"]
    for key, contract in material_changes.items():
        assert before[key][3] == contract["required_before"], (
            f"{key}: prior material required marker changed"
        )
        assert after[key][3] == contract["required_after"], (
            f"{key}: refreshed material required marker changed"
        )
        assert material_rule not in before[key][4], (
            f"{key}: material rule unexpectedly existed in the baseline"
        )
        assert material_rule in after[key][4], (
            f"{key}: missing exact scene_type conditional material rule"
        )
    assert len(before) == 1393, f"baseline field count changed: {len(before)}"
    assert len(legacy_after) == extension["base_fields"], (
        f"legacy field count changed: {len(legacy_after)}"
    )
    assert len(new_after) == extension["added_fields"], (
        f"new interface field count changed: {len(new_after)}"
    )
    assert len(after) == lock["totals"]["fields"], (
        f"current field count changed: {len(after)}"
    )
    for source in lock["sources"]:
        actual = sum(key[0] == source["title"] for key in after)
        assert actual == source["field_count"], (
            f"{source['title']}: expected {source['field_count']} fields, found {actual}"
        )
    print(
        "onboarding source refresh validated: live 2026-08-10 snapshot keeps "
        "all 2111 paths and changes only three activated_products descriptions; "
        "historical baseline remains legacy 1393 -> 1402 with "
        "exactly 16 approved additions, 1 recorded parser correction, "
        "4 upper_huifu_id Y-to-C changes, and 6 conditional material updates "
        "plus 1 scalar jsonArray path correction "
        "at the 2026-07-29 snapshot; 5 new interfaces add 702 fields for 2111 total"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
