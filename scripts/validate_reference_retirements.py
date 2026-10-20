#!/usr/bin/env python3
"""Check retired resources, preserved archives and current package callers."""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

from reference_retirements import CONTRACT, ROOT, retirement_entries
from validation_runtime import require_assertions_enabled

require_assertions_enabled()
ARCHIVE = "maintainer-contracts/skill-review-2026-10-10-archive/"
PAY = "huifu-pay-integration/references/"
ONB = "huifu-merchant-onboarding/references/"
EXPECTED_MOVES = {
    PAY + "canonical-regression-prompts.md": None,
    ONB + "canonical-regression-prompts.md": None,
    ONB + "user-onboarding-canonical-regression-prompts.md": None,
    ONB + "onboarding-extension-canonical-regression-prompts.md": None,
    PAY + "aggregation-order-quickstart.md": PAY + "aggregation-order.md",
    PAY + "aggregation-query-quickstart.md": PAY + "aggregation-query.md",
    PAY + "aggregation-refund-quickstart.md": PAY + "aggregation-refund.md",
    PAY + "checkout-js-readme.md": PAY + "checkout-js.md",
}


def retirement_errors(entries: list[dict], root: Path) -> list[str]:
    errors: list[str] = []
    sources = [item.get("source") for item in entries]
    if len(sources) != len(set(sources)) or set(sources) != set(EXPECTED_MOVES):
        errors.append("retirement source set must contain exactly the eight reviewed resources")
    for item in entries:
        source = item.get("source")
        if source not in EXPECTED_MOVES:
            errors.append("unreviewed source path")
            continue
        archive = ARCHIVE + source
        if item.get("archive") != archive:
            errors.append(f"{source}: invalid archive path")
            continue
        archived = root / archive
        if not archived.is_file():
            errors.append(f"{source}: archive missing")
        elif hashlib.sha256(archived.read_bytes()).hexdigest() != item.get("sha256"):
            errors.append(f"{source}: archive bytes changed")
        if (root / source).exists():
            errors.append(f"{source}: retired document re-entered the package")
        replacement = EXPECTED_MOVES[source]
        if item.get("replacement") != replacement:
            errors.append(f"{source}: unreviewed replacement")
        elif replacement and not (root / replacement).is_file():
            errors.append(f"{source}: current replacement missing")
    # A retained file may not refer to any retired basename, even through inline code.
    for skill in ("huifu-pay-integration", "huifu-merchant-onboarding"):
        names = [Path(source).name for source in EXPECTED_MOVES if source.startswith(skill + "/")]
        for path in (root / skill).rglob("*.md"):
            for name in names:
                if name in path.read_text(encoding="utf-8"):
                    errors.append(f"{path.relative_to(root)}: dangling reference to {name}")
    return errors


def validate_negative_fixtures(entries: list[dict]) -> int:
    """Exercise missing evidence, reintroduced content, invalid routes and callers."""
    with tempfile.TemporaryDirectory(prefix="huifu-retirements-") as tmp:
        root = Path(tmp)
        for entry in entries:
            dest = root / entry["archive"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / entry["archive"], dest)
            if entry["replacement"]:
                dest = root / entry["replacement"]
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / entry["replacement"], dest)
        assert not retirement_errors(entries, root), "baseline retirement fixture must pass"
        mutated = copy.deepcopy(entries)
        mutated[0]["sha256"] = "0" * 64
        assert any("bytes changed" in e for e in retirement_errors(mutated, root))
        mutated = copy.deepcopy(entries)
        mutated[0]["archive"] = "../outside.md"
        assert any("invalid archive" in e for e in retirement_errors(mutated, root))
        assert retirement_errors(entries + [entries[0]], root)
        archived = root / entries[0]["archive"]
        data = archived.read_bytes()
        archived.unlink()
        assert any("archive missing" in e for e in retirement_errors(entries, root))
        archived.write_bytes(data)
        retired = root / entries[0]["source"]
        retired.parent.mkdir(parents=True, exist_ok=True)
        retired.write_bytes(data)
        assert any("re-entered" in e for e in retirement_errors(entries, root))
        retired.unlink()
        replacement = root / next(item["replacement"] for item in entries if item["replacement"])
        data = replacement.read_bytes()
        replacement.unlink()
        assert any("replacement missing" in e for e in retirement_errors(entries, root))
        replacement.write_bytes(data)
        replacement.write_text(replacement.read_text() + "\n`canonical-regression-prompts.md`\n")
        assert any("dangling reference" in e for e in retirement_errors(entries, root))
    return 7


def main() -> int:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert (ROOT / payload["review_plan"]).is_file()
    entries = retirement_entries()
    errors = retirement_errors(entries, ROOT)
    assert not errors, "\n".join(errors)
    # Critical field preservation is independently checked from the frozen catalog.
    contract = (ROOT / ONB / "merchant-onboarding-field-contracts.md").read_text()
    catalog = (ROOT / ONB / "merchant-onboarding-complete-field-catalog.md").read_text()
    image = catalog.split("## 图片上传", 1)[1].split("\n## ", 1)[0]
    row = next(line for line in image.splitlines() if line.startswith("| `request.data.file_url` |"))
    cells = [x.strip().strip("`") for x in row.strip("|").split("|")]
    assert cells[2:5] == ["String", "512", "C"], cells
    assert "file_url String(512) C" in contract and "file_url String(512) N" not in contract
    fixtures = validate_negative_fixtures(entries)
    print(f"Reference retirements validated: {len(entries)} archives, four current replacement routes, {fixtures} negative fixtures; image C contract preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
