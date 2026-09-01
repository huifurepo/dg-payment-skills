#!/usr/bin/env python3
"""Validate self-contained Skill packages and migration conservation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from skill_validation_config import ONBOARDING_SOURCE_LOCK
from validation_runtime import require_assertions_enabled


require_assertions_enabled()


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "skills-manifest.json"
LEDGER = REPO_ROOT / "maintainer-contracts/reference-migration-ledger.json"
TRANSFORMATION_REVIEW = (
    REPO_ROOT / "maintainer-contracts/reference-transformation-review.json"
)
DOMAIN_BOUNDARIES = REPO_ROOT / "maintainer-contracts/skill-domain-boundaries.json"
SEMANTIC_ANCHORS = REPO_ROOT / "maintainer-contracts/reference-semantic-anchors.json"
TRANSFORMATION_TARGET_LOCK = (
    REPO_ROOT / "maintainer-contracts/reference-transformation-target-lock.json"
)
EXPECTED_SKILLS = {
    "huifu-pay-integration",
    "huifu-merchant-onboarding",
}
EXPECTED_CATEGORY_COUNTS = {
    "KEEP": 78,
    "MOVE": 7,
    "SPLIT": 13,
    "REWRITE_PAYMENT": 8,
    "REWRITE_ONBOARDING": 2,
    "REPO_ONLY": 2,
}
LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://)(?!#)([^)]+)\)")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def commit_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO_ROOT,
    )


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_manifest(errors: list[str]) -> dict[str, object]:
    if not MANIFEST.is_file():
        error(errors, "skills-manifest.json missing")
        return {}
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    skills = payload.get("skills", {})
    missing_skills = EXPECTED_SKILLS - set(skills)
    if missing_skills:
        error(errors, f"manifest is missing split baseline skills: {sorted(missing_skills)}")
    for skill_id, spec in skills.items():
        root = REPO_ROOT / str(spec["root"])
        if root.name != skill_id:
            error(errors, f"{skill_id}: root must match skill id")
        if set(path.name for path in root.iterdir()) != {"SKILL.md", "agents", "references"}:
            error(errors, f"{skill_id}: package top-level must contain only SKILL.md, agents, references")
        reference_manifest = REPO_ROOT / str(spec["reference_manifest"])
        expected_refs = set(json.loads(reference_manifest.read_text(encoding="utf-8"))["references"])
        actual_refs = {path.name for path in (root / "references").glob("*.md")}
        if actual_refs != expected_refs:
            error(
                errors,
                f"{skill_id}: reference manifest mismatch; missing={sorted(expected_refs - actual_refs)}, "
                f"extra={sorted(actual_refs - expected_refs)}",
            )
    return payload


def validate_ledger(errors: list[str]) -> None:
    if not LEDGER.is_file():
        error(errors, "reference migration ledger missing")
        return
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    entries = ledger.get("entries", [])
    baseline_commit = ledger.get("baseline_commit")
    migration_commit = ledger.get("migration_commit")
    if not isinstance(baseline_commit, str) or not isinstance(migration_commit, str):
        error(errors, "migration ledger must declare baseline_commit and migration_commit")
        return
    if len(entries) != 110:
        error(errors, f"migration ledger must contain 110 entries, found {len(entries)}")
    paths = [entry["source_path"] for entry in entries]
    if len(paths) != len(set(paths)):
        error(errors, "migration ledger contains duplicate source paths")
    if ledger.get("category_counts") != EXPECTED_CATEGORY_COUNTS:
        error(errors, f"migration category counts changed: {ledger.get('category_counts')}")
    for entry in entries:
        try:
            source_bytes = commit_bytes(baseline_commit, entry["source_path"])
        except subprocess.CalledProcessError:
            error(errors, f"{entry['source_path']}: missing from baseline commit")
            continue
        source_digest = hashlib.sha256(source_bytes).hexdigest()
        if source_digest != entry.get("source_sha256"):
            error(errors, f"{entry['source_path']}: baseline blob does not match ledger SHA")
        if entry.get("status") != "completed":
            error(errors, f"{entry['source_path']}: migration status is not completed")
        destinations = entry.get("destinations", [])
        if not destinations:
            error(errors, f"{entry['source_path']}: no destination")
            continue
        for destination in destinations:
            target = REPO_ROOT / destination["path"]
            if not target.is_file():
                error(errors, f"{entry['source_path']}: missing destination {destination['path']}")
                continue
            destination_commit = destination.get("migration_commit")
            if destination_commit != migration_commit:
                error(errors, f"{entry['source_path']}: destination migration commit changed")
                continue
            try:
                migrated_bytes = commit_bytes(migration_commit, destination["path"])
            except subprocess.CalledProcessError:
                error(errors, f"{destination['path']}: missing from migration commit")
                continue
            migrated_digest = hashlib.sha256(migrated_bytes).hexdigest()
            if migrated_digest != destination.get("migration_sha256"):
                error(errors, f"{destination['path']}: sealed migration SHA changed")
            if destination.get("expect_byte_identical") and migrated_digest != source_digest:
                error(errors, f"{entry['source_path']}: byte-preserving migration differs")
    validate_transformation_review(errors, ledger)


def validate_transformation_review(
    errors: list[str],
    ledger: dict[str, object],
) -> None:
    if not TRANSFORMATION_REVIEW.is_file():
        error(errors, "independent reference transformation review is missing")
        return
    review = json.loads(TRANSFORMATION_REVIEW.read_text(encoding="utf-8"))
    for key in ("baseline_commit", "migration_commit"):
        if review.get(key) != ledger.get(key):
            error(errors, f"transformation review {key} differs from migration ledger")
    reviewers = {
        (item.get("role"), item.get("identity"))
        for item in review.get("reviewers", [])
        if item.get("role") and item.get("identity")
    }
    if len(reviewers) < 2:
        error(errors, "transformation review requires at least two named reviewer roles")

    transformed = {
        entry["source_path"]: entry
        for entry in ledger["entries"]
        if entry["category"] in {"SPLIT", "REWRITE_PAYMENT", "REWRITE_ONBOARDING"}
    }
    reviewed_entries = review.get("entries", [])
    reviewed = {entry["source_path"]: entry for entry in reviewed_entries}
    if len(reviewed) != len(reviewed_entries):
        error(errors, "transformation review contains duplicate source paths")
    if set(reviewed) != set(transformed):
        error(
            errors,
            "transformation review source set differs; "
            f"missing={sorted(set(transformed) - set(reviewed))}, "
            f"extra={sorted(set(reviewed) - set(transformed))}",
        )
        return

    allowed_decisions = {
        "whole-document-retained-after-rewrite",
        "retained-or-verbatim-routed",
        "restructured-within-domain",
        "domain-split-and-restructured",
    }
    for source_path, source in transformed.items():
        item = reviewed[source_path]
        if item.get("status") != "approved":
            error(errors, f"{source_path}: transformation review is not approved")
        if item.get("category") != source["category"]:
            error(errors, f"{source_path}: transformation review category differs")
        expected_destinations = [entry["path"] for entry in source["destinations"]]
        if item.get("destination_paths") != expected_destinations:
            error(errors, f"{source_path}: transformation destinations differ")
        expected_sections = [
            f"L{heading['level']}@{heading['source_line']}:{heading['heading']}"
            for heading in source["source_headings"]
        ] or ["__whole_document__"]
        routes = item.get("section_routes", [])
        actual_sections = [route.get("source_section") for route in routes]
        if actual_sections != expected_sections:
            error(errors, f"{source_path}: source section coverage differs")
        inventory_digest = hashlib.sha256(
            json.dumps(
                actual_sections,
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        if item.get("source_section_inventory_sha256") != inventory_digest:
            error(errors, f"{source_path}: section inventory SHA differs")
        for route in routes:
            targets = route.get("destination_paths", [])
            if not targets or not set(targets).issubset(expected_destinations):
                error(errors, f"{source_path}: invalid section destination route {targets}")
            if route.get("decision") not in allowed_decisions:
                error(errors, f"{source_path}: unapproved section decision")
            if not route.get("review_note"):
                error(errors, f"{source_path}: section review note is missing")
    validate_transformation_target_lock(
        errors,
        review,
        transformed,
        str(ledger.get("baseline_commit", "")),
        str(ledger.get("migration_commit", "")),
    )
    validate_semantic_anchors(errors, transformed, str(ledger.get("baseline_commit", "")))


def validate_transformation_target_lock(
    errors: list[str],
    review: dict[str, object],
    transformed: dict[str, object],
    expected_baseline_commit: str,
    expected_migration_commit: str,
) -> None:
    """Seal every destination byte covered by the independent transformation review."""
    if not TRANSFORMATION_TARGET_LOCK.is_file():
        error(errors, "reference transformation target lock is missing")
        return
    payload = json.loads(TRANSFORMATION_TARGET_LOCK.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        error(errors, "reference transformation target lock schema_version must be 1")
    if payload.get("baseline_commit") != expected_baseline_commit:
        error(errors, "reference transformation target lock baseline differs")
    if payload.get("migration_commit") != expected_migration_commit:
        error(errors, "reference transformation target lock migration commit differs")
    reviewed_entries = review.get("entries", [])
    section_count = sum(
        len(item.get("section_routes", []))
        for item in reviewed_entries
        if isinstance(item, dict)
    )
    if payload.get("reviewed_source_documents") != len(transformed):
        error(errors, "reference transformation target lock source count differs")
    if payload.get("reviewed_section_routes") != section_count:
        error(errors, "reference transformation target lock section count differs")
    current_review = payload.get("current_snapshot_review")
    if not isinstance(current_review, dict):
        error(errors, "reference transformation target lock current review is missing")
    else:
        reviewed_head = current_review.get("reviewed_head")
        reviewers = current_review.get("reviewers", [])
        if (
            not isinstance(reviewed_head, str)
            or not re.fullmatch(r"[0-9a-f]{40}", reviewed_head)
            or subprocess.run(
                ["git", "merge-base", "--is-ancestor", reviewed_head, "HEAD"],
                cwd=REPO_ROOT,
                check=False,
            ).returncode
            != 0
        ):
            error(errors, "reference transformation target lock reviewed HEAD is invalid")
        reviewer_roles = {
            (item.get("role"), item.get("identity"))
            for item in reviewers
            if isinstance(item, dict) and item.get("role") and item.get("identity")
        }
        if len(reviewer_roles) < 2:
            error(errors, "reference transformation target lock requires two reviewers")
        if current_review.get("result") != "approved-after-corrections":
            error(errors, "reference transformation target lock review is not approved")
    expected_targets = {
        destination["path"]
        for source in transformed.values()
        for destination in source.get("destinations", [])
    }
    locked = payload.get("destination_sha256")
    if not isinstance(locked, dict) or set(locked) != expected_targets:
        error(errors, "reference transformation target lock destination set differs")
        return
    for relative_path, expected_digest in locked.items():
        target = REPO_ROOT / relative_path
        if not target.is_file():
            error(errors, f"{relative_path}: reviewed transformation target is missing")
            continue
        try:
            head_digest = hashlib.sha256(commit_bytes("HEAD", relative_path)).hexdigest()
        except subprocess.CalledProcessError:
            error(errors, f"{relative_path}: reviewed transformation target is absent from HEAD")
            continue
        if head_digest != expected_digest:
            error(errors, f"{relative_path}: reviewed transformation target HEAD blob changed")
        dirty = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", relative_path],
            cwd=REPO_ROOT,
            check=False,
        )
        if dirty.returncode != 0:
            error(errors, f"{relative_path}: reviewed transformation target has uncommitted changes")


def validate_semantic_anchors(
    errors: list[str],
    transformed: dict[str, object],
    expected_baseline_commit: str,
) -> None:
    """Protect a small, explicit set of high-risk clauses across rewrites."""
    if not SEMANTIC_ANCHORS.is_file():
        error(errors, "reference semantic anchor contract is missing")
        return
    payload = json.loads(SEMANTIC_ANCHORS.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        error(errors, "reference semantic anchor schema_version must be 1")
    if payload.get("coverage") != "selected-high-risk-clauses":
        error(errors, "reference semantic anchors must declare selected high-risk coverage")
    if payload.get("full_review_lock") != TRANSFORMATION_TARGET_LOCK.relative_to(
        REPO_ROOT
    ).as_posix():
        error(errors, "reference semantic anchors must link the full reviewed target lock")
    baseline_commit = payload.get("baseline_commit")
    if not isinstance(baseline_commit, str):
        error(errors, "reference semantic anchors must declare baseline_commit")
        return
    if baseline_commit != expected_baseline_commit:
        error(errors, "reference semantic anchor baseline differs from migration ledger")
        return
    anchors = payload.get("anchors", [])
    if not isinstance(anchors, list) or not anchors:
        error(errors, "reference semantic anchors must not be empty")
        return
    identifiers = [item.get("id") for item in anchors if isinstance(item, dict)]
    if len(identifiers) != len(anchors) or len(identifiers) != len(set(identifiers)):
        error(errors, "reference semantic anchor ids must be present and unique")
        return
    anchored_domains: set[str] = set()
    for item in anchors:
        source_path = item.get("source_path")
        target_path = item.get("target_path")
        source_clause = item.get("source_clause")
        target_clause = item.get("target_clause")
        if source_path not in transformed:
            error(errors, f"{item['id']}: semantic anchor source is not transformed")
            continue
        if not all(
            isinstance(value, str) and value
            for value in (target_path, source_clause, target_clause)
        ):
            error(errors, f"{item['id']}: semantic anchor fields must be non-empty strings")
            continue
        transformed_entry = transformed[source_path]
        assert isinstance(transformed_entry, dict)
        allowed_targets = {
            destination["path"]
            for destination in transformed_entry.get("destinations", [])
        }
        if target_path not in allowed_targets:
            error(errors, f"{item['id']}: semantic anchor target is not a migration destination")
            continue
        try:
            baseline_text = commit_bytes(baseline_commit, source_path).decode("utf-8")
        except (subprocess.CalledProcessError, UnicodeDecodeError):
            error(errors, f"{item['id']}: cannot read baseline source clause")
            continue
        if source_clause not in baseline_text:
            error(errors, f"{item['id']}: source clause is absent from the locked baseline")
        target = REPO_ROOT / target_path
        if not target.is_file():
            error(errors, f"{item['id']}: semantic anchor target is missing")
            continue
        if target_clause not in target.read_text(encoding="utf-8"):
            error(errors, f"{item['id']}: protected target clause is missing")
        if target_path.startswith("huifu-pay-integration/"):
            anchored_domains.add("payment")
        elif target_path.startswith("huifu-merchant-onboarding/"):
            anchored_domains.add("onboarding")
    if anchored_domains != {"payment", "onboarding"}:
        error(errors, "semantic anchors must protect both payment and onboarding domains")


def validate_isolation(errors: list[str], manifest: dict[str, object]) -> None:
    skills = manifest.get("skills", {})
    all_skill_ids = set(skills)
    for skill_id, spec in skills.items():
        root = REPO_ROOT / str(spec["root"])
        other_ids = all_skill_ids - {skill_id}
        for path in [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]:
            text = path.read_text(encoding="utf-8")
            for repo_only_prefix in ("maintainer-contracts/", "tests/regression/", "scripts/"):
                if repo_only_prefix in text:
                    error(
                        errors,
                        f"{path.relative_to(REPO_ROOT)}: package depends on repo-only "
                        f"path {repo_only_prefix}",
                    )
            for other_id in other_ids:
                forbidden = f"../{other_id}"
                if forbidden in text:
                    error(errors, f"{path.relative_to(REPO_ROOT)}: cross-skill path {forbidden}")
            for match in LOCAL_LINK.finditer(text):
                target = match.group(1).split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    error(errors, f"{path.relative_to(REPO_ROOT)}: broken link {target}")


def validate_frozen_assets(
    errors: list[str],
    manifest: dict[str, object],
    baseline_commit: str,
) -> None:
    frozen_assets = manifest.get("frozen_assets", [])
    if not frozen_assets:
        error(errors, "manifest must declare frozen_assets")
        return
    missing = [path for path in frozen_assets if not (REPO_ROOT / path).exists()]
    if missing:
        error(errors, f"frozen assets are missing: {missing}")
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", baseline_commit, "--", *frozen_assets],
        cwd=REPO_ROOT,
        text=True,
    ).splitlines()
    if changed:
        error(errors, f"frozen assets changed since split baseline: {changed}")
    optional_assets = manifest.get("local_optional_frozen_assets", [])
    present_optional = [path for path in optional_assets if (REPO_ROOT / path).exists()]
    if present_optional:
        changed_optional = subprocess.check_output(
            ["git", "diff", "--name-only", baseline_commit, "--", *present_optional],
            cwd=REPO_ROOT,
            text=True,
        ).splitlines()
        if changed_optional:
            error(errors, f"optional frozen assets changed since baseline: {changed_optional}")


def validate_maintainer_contracts(errors: list[str]) -> None:
    release = (REPO_ROOT / "maintainer-contracts/shared-release-checklist.md").read_text(
        encoding="utf-8"
    )
    versioning = (REPO_ROOT / "maintainer-contracts/shared-versioning-policy.md").read_text(
        encoding="utf-8"
    )
    architecture = (
        REPO_ROOT / "maintainer-contracts/SKILL_FAMILY_ARCHITECTURE.md"
    ).read_text(encoding="utf-8")
    stale = ("当前单 Skill", "169/129/442/9/551/93")
    for phrase in stale:
        if phrase in release:
            error(errors, f"release checklist contains stale phrase: {phrase}")
    for required in (
        "huifu-pay-integration` | `1.3.5",
        "huifu-merchant-onboarding` | `1.0.2",
        "企业/个人用户开户、企业/个人用户基本信息修改、用户业务入驻及修改",
    ):
        if required not in versioning:
            error(errors, f"versioning policy missing current fact: {required}")
    for required in ("manifest", "新增模块流程", "2,737"):
        if required not in architecture:
            error(errors, f"Skill family architecture missing: {required}")


def load_domain_boundaries() -> dict[str, dict[str, tuple[str, ...]]]:
    if not DOMAIN_BOUNDARIES.is_file():
        raise ValueError("skill domain boundary contract is missing")
    payload = json.loads(DOMAIN_BOUNDARIES.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 2:
        raise ValueError("skill domain boundary schema_version must be 2")
    merchant_catalog = payload.get("merchant_field_catalog")
    if not isinstance(merchant_catalog, str) or not merchant_catalog:
        raise ValueError("skill domain boundary merchant field catalog is missing")
    catalog_path = REPO_ROOT / merchant_catalog
    if not catalog_path.is_file():
        raise ValueError("skill domain boundary merchant field catalog does not exist")
    field_paths = re.findall(
        r"^\| `([^`]+)` \|",
        catalog_path.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    source_lock = json.loads(
        (
            ONBOARDING_SOURCE_LOCK
        ).read_text(encoding="utf-8")
    )
    expected_field_count = source_lock["totals"]["fields"]
    if len(field_paths) != expected_field_count:
        raise ValueError(
            "skill domain boundary merchant catalog must contain "
            f"{expected_field_count} paths, found {len(field_paths)}"
        )
    user_catalog = payload.get("user_field_catalog")
    if not isinstance(user_catalog, str) or not user_catalog:
        raise ValueError("skill domain boundary user field catalog is missing")
    user_catalog_path = REPO_ROOT / user_catalog
    if not user_catalog_path.is_file():
        raise ValueError("skill domain boundary user field catalog does not exist")
    user_field_paths = re.findall(
        r"^\| `([^`]+)` \|",
        user_catalog_path.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    user_source_lock = json.loads(
        (REPO_ROOT / "maintainer-contracts/user-onboarding-source-lock-2026-08-24-r4.json").read_text(
            encoding="utf-8"
        )
    )
    expected_user_field_count = user_source_lock["totals"]["fields"]
    if len(user_field_paths) != expected_user_field_count:
        raise ValueError(
            "skill domain boundary user catalog must contain "
            f"{expected_user_field_count} paths, found {len(user_field_paths)}"
        )
    merchant_identifiers = {
        part.removesuffix("[]")
        for path in field_paths
        for part in path.split(".")
        if part not in {"request", "response", "async", "data"}
    }
    skills = payload.get("skills")
    if not isinstance(skills, dict) or set(skills) != EXPECTED_SKILLS:
        raise ValueError("skill domain boundary contract must cover all manifest skills")
    result: dict[str, dict[str, tuple[str, ...]]] = {}
    for skill_id, spec in skills.items():
        literals = spec.get("forbidden_implementation_literals")
        if (
            not isinstance(literals, list)
            or not literals
            or not all(isinstance(item, str) and item for item in literals)
            or len(literals) != len(set(literals))
        ):
            raise ValueError(f"{skill_id}: forbidden implementation literals are invalid")
        allowed_identifiers = spec.get("allowed_merchant_field_identifiers")
        if (
            not isinstance(allowed_identifiers, list)
            or not all(isinstance(item, str) and item for item in allowed_identifiers)
            or len(allowed_identifiers) != len(set(allowed_identifiers))
            or not set(allowed_identifiers).issubset(merchant_identifiers)
        ):
            raise ValueError(f"{skill_id}: allowed merchant field identifiers are invalid")
        result[skill_id] = {
            "forbidden_literals": tuple(literals),
            "merchant_identifiers": tuple(
                sorted(merchant_identifiers - set(allowed_identifiers))
                if skill_id == "huifu-pay-integration"
                else ()
            ),
        }
    return result


def domain_boundary_findings(
    skill_id: str,
    text: str,
    relative_path: str,
) -> list[str]:
    """Return high-confidence cross-domain implementation markers."""
    boundaries = load_domain_boundaries()
    findings = [
        f"{skill_id}/{relative_path}: cross-domain implementation marker {literal!r}"
        for literal in boundaries[skill_id]["forbidden_literals"]
        if literal.casefold() in text.casefold()
    ]
    implementation_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or stripped.startswith("|"):
            implementation_lines.append(line)
    implementation_text = "\n".join(implementation_lines)
    for identifier in boundaries[skill_id]["merchant_identifiers"]:
        if re.search(
            rf"(?<![A-Za-z0-9_]){re.escape(identifier)}(?![A-Za-z0-9_])",
            implementation_text,
            flags=re.IGNORECASE,
        ):
            findings.append(
                f"{skill_id}/{relative_path}: cross-domain merchant field identifier "
                f"{identifier!r}"
            )
    return findings


def validate_domain_separation(errors: list[str]) -> None:
    payment_refs = REPO_ROOT / "huifu-pay-integration/references"
    onboarding_refs = REPO_ROOT / "huifu-merchant-onboarding/references"
    merchant_named = sorted(path.name for path in payment_refs.glob("merchant-onboarding-*.md"))
    if merchant_named:
        error(errors, f"payment package still contains merchant-onboarding references: {merchant_named}")
    forbidden_onboarding = sorted(
        path.name
        for path in onboarding_refs.glob("*.md")
        if path.name.startswith(("aggregation-", "hostingpay-", "checkout-js"))
    )
    if forbidden_onboarding:
        error(errors, f"onboarding package contains payment implementation references: {forbidden_onboarding}")
    try:
        boundaries = load_domain_boundaries()
    except (ValueError, json.JSONDecodeError) as exc:
        error(errors, str(exc))
        return
    for skill_id in boundaries:
        root = REPO_ROOT / skill_id
        for path in [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]:
            errors.extend(
                domain_boundary_findings(
                    skill_id,
                    path.read_text(encoding="utf-8"),
                    path.relative_to(root).as_posix(),
                )
            )


def main() -> int:
    errors: list[str] = []
    manifest = validate_manifest(errors)
    validate_ledger(errors)
    if manifest:
        validate_isolation(errors, manifest)
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        validate_frozen_assets(errors, manifest, ledger["baseline_commit"])
        validate_maintainer_contracts(errors)
    if all((REPO_ROOT / skill_id).is_dir() for skill_id in EXPECTED_SKILLS):
        validate_domain_separation(errors)
    if errors:
        print("Skill split validation failed:")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print("Skill split validation passed: 2 isolated skills, 110 source references conserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
