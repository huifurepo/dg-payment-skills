#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from skill_validation_config import (
    ALLOWED_TOP_LEVEL_KEYS,
    EXPECTED_OPENAI_YAML,
    EXPECTED_REFERENCES,
    EXPECTED_SKILL_DIR,
    EXPECTED_SKILL_FILE,
    INLINE_CODE_PATTERN,
    LONG_REFERENCE_TOC_LINE_LIMIT,
    MAX_SHORT_DESCRIPTION_LENGTH,
    MAX_SKILL_REFERENCE_MENTIONS,
    MD_LINK_PATTERN,
    MIN_SHORT_DESCRIPTION_LENGTH,
    NAME_PATTERN,
    REPO_ROOT,
    SKILL_FILES,
    ValidationState,
)
from skill_validation_utils import (
    looks_like_local_path,
    should_skip,
    strip_quotes,
    validate_repo_files,
    validate_skill_top_level,
)


def main() -> int:
    state = ValidationState()
    print("=== Skill 仓库校验 ===\n")
    validate_repo_layout(state)
    validate_skill_top_level(state)
    validate_skill_files(state)
    validate_agents_files(state)
    validate_entry_docs(state)
    validate_reference_navigation(state)
    validate_markdown_links(state)
    validate_repo_files(state)
    print(f"\n=== 结果: {state.errors} errors, {state.warnings} warnings ===")
    if state.errors == 0:
        print("✅ All checks passed")
    else:
        print("❌ Fix errors before release")
    return state.errors


def validate_repo_layout(state: ValidationState) -> None:
    print("--- 仓库发布结构检查（自定义约束） ---")
    if SKILL_FILES != [EXPECTED_SKILL_FILE]:
        found = ", ".join(str(path.relative_to(REPO_ROOT)) for path in SKILL_FILES) or "none"
        state.error(f"expected only {EXPECTED_SKILL_FILE.relative_to(REPO_ROOT)}, found: {found}")
    else:
        state.ok(f"single skill layout OK: {EXPECTED_SKILL_FILE.relative_to(REPO_ROOT)}")

    references_dir = EXPECTED_SKILL_DIR / "references"
    if not references_dir.is_dir():
        state.error("huifu-pay-integration/references missing")
        return
    nested_dirs = sorted(path.relative_to(references_dir) for path in references_dir.iterdir() if path.is_dir())
    if nested_dirs:
        state.error(f"references must stay flat, found subdirectories: {', '.join(map(str, nested_dirs))}")
    missing_refs = sorted(name for name in EXPECTED_REFERENCES if not (references_dir / name).exists())
    if missing_refs:
        state.error(f"missing references: {', '.join(missing_refs)}")
    else:
        state.ok("all expected reference files exist")
    actual_refs = {path.name for path in references_dir.glob("*.md")}
    extra_refs = sorted(actual_refs - EXPECTED_REFERENCES)
    if extra_refs:
        state.error(f"unexpected references: {', '.join(extra_refs)}")
    else:
        state.ok("reference file set matches expected single-skill manifest")


def validate_skill_files(state: ValidationState) -> None:
    print("\n--- Agent Skills 规范检查 ---")
    for skill_file in SKILL_FILES:
        validate_single_skill(skill_file, state)


def validate_single_skill(skill_file: Path, state: ValidationState) -> None:
    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text, skill_file, state)
    if frontmatter is None:
        return

    fields = parse_frontmatter(frontmatter, skill_file, state)
    if fields is None:
        return

    validate_top_level_keys(fields, skill_file, state)
    validate_name(fields.get("name"), skill_file, state)
    validate_description(fields.get("description"), skill_file, state)
    validate_body(body, skill_file, state)


def split_frontmatter(
    text: str,
    skill_file: Path,
    state: ValidationState,
) -> tuple[list[str] | None, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        state.error(f"{skill_file} missing frontmatter start")
        return None, ""
    try:
        end_index = lines[1:].index("---") + 1
    except ValueError:
        state.error(f"{skill_file} missing frontmatter end")
        return None, ""
    frontmatter = lines[1:end_index]
    body = "\n".join(lines[end_index + 1 :]).strip()
    return frontmatter, body


def parse_frontmatter(
    lines: list[str],
    skill_file: Path,
    state: ValidationState,
) -> dict[str, object] | None:
    fields: dict[str, object] = {}
    current_key: str | None = None
    current_block: list[str] = []

    for raw_line in lines + ["__END__: __END__"]:
        if not raw_line.strip():
            if current_key == "metadata":
                current_block.append(raw_line)
            continue
        if raw_line.startswith(" ") or raw_line.startswith("\t"):
            if current_key is None:
                state.error(f"{skill_file} has unexpected indentation in frontmatter")
                return None
            current_block.append(raw_line)
            continue
        finalize_field(current_key, current_block, fields, skill_file, state)
        current_key, value = parse_top_level_line(raw_line, skill_file, state)
        if current_key is None:
            return None
        current_block = [value]

    fields.pop("__END__", None)
    return fields


def finalize_field(
    key: str | None,
    block: list[str],
    fields: dict[str, object],
    skill_file: Path,
    state: ValidationState,
) -> None:
    if key is None:
        return
    value = block[0]
    if key == "metadata":
        fields[key] = parse_metadata_block(block[1:], skill_file, state)
        return
    if len(block) > 1:
        state.error(f"{skill_file} field '{key}' must be a single-line scalar")
        return
    fields[key] = strip_quotes(value.strip())


def parse_top_level_line(
    line: str,
    skill_file: Path,
    state: ValidationState,
) -> tuple[str | None, str]:
    if ":" not in line:
        state.error(f"{skill_file} invalid frontmatter line: {line}")
        return None, ""
    key, value = line.split(":", 1)
    key = key.strip()
    if not key:
        state.error(f"{skill_file} has empty frontmatter key")
        return None, ""
    return key, value


def parse_metadata_block(
    lines: list[str],
    skill_file: Path,
    state: ValidationState,
) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        if not line.startswith("  ") or line.startswith("    "):
            state.error(f"{skill_file} metadata must be a flat map of string values")
            return metadata
        if ":" not in line:
            state.error(f"{skill_file} metadata entry missing ':' -> {line.strip()}")
            return metadata
        key, value = line.strip().split(":", 1)
        if not key or not value.strip():
            state.error(f"{skill_file} metadata entry must be key: value -> {line.strip()}")
            return metadata
        metadata[key.strip()] = strip_quotes(value.strip())
    return metadata


def validate_top_level_keys(fields: dict[str, object], skill_file: Path, state: ValidationState) -> None:
    extra_keys = sorted(set(fields) - ALLOWED_TOP_LEVEL_KEYS)
    for key in extra_keys:
        state.error(f"{skill_file} uses unsupported frontmatter key '{key}'")


def validate_name(name: object, skill_file: Path, state: ValidationState) -> None:
    if not isinstance(name, str) or not name:
        state.error(f"{skill_file} missing required name")
        return
    if not NAME_PATTERN.match(name):
        state.error(f"{skill_file} invalid name '{name}'")
        return
    if name != skill_file.parent.name:
        state.error(f"{skill_file} name '{name}' does not match parent directory")
        return
    state.ok(f"{skill_file} name OK")


def validate_description(description: object, skill_file: Path, state: ValidationState) -> None:
    if not isinstance(description, str) or not description.strip():
        state.error(f"{skill_file} missing required description")
        return
    if len(description) > 1024:
        state.error(f"{skill_file} description exceeds 1024 chars")
        return
    state.ok(f"{skill_file} description OK")


def validate_body(body: str, skill_file: Path, state: ValidationState) -> None:
    if not body:
        state.error(f"{skill_file} missing Markdown body")
        return
    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count > 500:
        state.error(f"{skill_file} exceeds 500 lines ({line_count})")
        return
    state.ok(f"{skill_file} body OK")


def validate_agents_files(state: ValidationState) -> None:
    print("\n--- Agents 元数据检查（自定义约束） ---")
    if not EXPECTED_OPENAI_YAML.is_file():
        state.error("huifu-pay-integration/agents/openai.yaml missing")
        return
    interface, quoted = parse_openai_interface(EXPECTED_OPENAI_YAML, state)
    if interface is None:
        return
    validate_interface_string(EXPECTED_OPENAI_YAML, interface, quoted, "display_name", 1, 80, state)
    validate_interface_string(
        EXPECTED_OPENAI_YAML,
        interface,
        quoted,
        "short_description",
        MIN_SHORT_DESCRIPTION_LENGTH,
        MAX_SHORT_DESCRIPTION_LENGTH,
        state,
    )
    validate_default_prompt(interface, quoted, EXPECTED_OPENAI_YAML, state)
    validate_interface_consistency(interface, EXPECTED_SKILL_FILE, state)


def parse_openai_interface(
    openai_file: Path,
    state: ValidationState,
) -> tuple[dict[str, str] | None, set[str]]:
    interface: dict[str, str] = {}
    quoted: set[str] = set()
    inside_interface = False
    for raw_line in openai_file.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not raw_line.startswith(" "):
            inside_interface = stripped == "interface:"
            continue
        if not inside_interface:
            continue
        if not raw_line.startswith("  ") or raw_line.startswith("    "):
            state.error(f"{openai_file} interface must be a flat map")
            return None, set()
        key, separator, value = stripped.partition(":")
        if not separator:
            state.error(f"{openai_file} invalid interface line: {stripped}")
            return None, set()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            quoted.add(key)
        interface[key] = strip_quotes(value)
    if not interface:
        state.error(f"{openai_file} missing interface block")
        return None, set()
    state.ok(f"{openai_file} interface block OK")
    return interface, quoted


def validate_interface_string(
    openai_file: Path,
    interface: dict[str, str],
    quoted: set[str],
    key: str,
    min_len: int,
    max_len: int,
    state: ValidationState,
) -> None:
    value = interface.get(key, "").strip()
    if not value:
        state.error(f"{openai_file} missing interface.{key}")
        return
    if key not in quoted:
        state.error(f"{openai_file} interface.{key} must be quoted")
        return
    if len(value) < min_len or len(value) > max_len:
        state.error(f"{openai_file} interface.{key} length must be {min_len}-{max_len}")
        return
    state.ok(f"{openai_file} interface.{key} OK")


def validate_default_prompt(
    interface: dict[str, str],
    quoted: set[str],
    openai_file: Path,
    state: ValidationState,
) -> None:
    validate_interface_string(openai_file, interface, quoted, "default_prompt", 1, 200, state)
    prompt = interface.get("default_prompt", "")
    if f"${EXPECTED_SKILL_DIR.name}" not in prompt:
        state.error(f"{openai_file} interface.default_prompt must mention ${EXPECTED_SKILL_DIR.name}")
        return
    state.ok(f"{openai_file} interface.default_prompt skill reference OK")


def validate_interface_consistency(
    interface: dict[str, str],
    skill_file: Path,
    state: ValidationState,
) -> None:
    text = skill_file.read_text(encoding="utf-8")
    heading = extract_skill_heading(text)
    if heading is None:
        state.error(f"{skill_file} missing H1 heading for interface consistency check")
        return
    display_name = interface.get("display_name", "")
    if display_name != heading:
        state.error(f"{EXPECTED_OPENAI_YAML} interface.display_name must match SKILL.md H1 heading")
    else:
        state.ok(f"{EXPECTED_OPENAI_YAML} interface.display_name matches SKILL.md heading")
    validate_keyword_groups(
        interface.get("short_description", ""),
        build_short_description_groups(text),
        "interface.short_description",
        state,
    )
    validate_keyword_groups(
        interface.get("default_prompt", ""),
        build_default_prompt_groups(text),
        "interface.default_prompt",
        state,
    )


def extract_skill_heading(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def build_short_description_groups(text: str) -> list[tuple[str, tuple[str, ...]]]:
    groups: list[tuple[str, tuple[str, ...]]] = []
    if "聚合支付" in text:
        groups.append(("聚合支付", ("聚合支付",)))
    if "托管支付" in text:
        groups.append(("托管支付", ("托管支付",)))
    if "前端收银台" in text or "checkout" in text:
        groups.append(("前端收银台", ("前端收银台", "checkout")))
    return groups


def build_default_prompt_groups(text: str) -> list[tuple[str, tuple[str, ...]]]:
    groups: list[tuple[str, tuple[str, ...]]] = []
    if "产品线" in text:
        groups.append(("产品线", ("产品线",)))
    if "references/" in text:
        groups.append(("references", ("references",)))
    return groups


def validate_keyword_groups(
    value: str,
    groups: list[tuple[str, tuple[str, ...]]],
    field_name: str,
    state: ValidationState,
) -> None:
    for label, options in groups:
        if any(option in value for option in options):
            state.ok(f"{EXPECTED_OPENAI_YAML} {field_name} covers {label}")
            continue
        state.error(f"{EXPECTED_OPENAI_YAML} {field_name} missing keyword group: {label}")


def validate_entry_docs(state: ValidationState) -> None:
    print("\n--- 入口文档检查（自定义约束） ---")
    skill_text = EXPECTED_SKILL_FILE.read_text(encoding="utf-8")
    overview_file = EXPECTED_SKILL_DIR / "references" / "shared-overview.md"
    overview_text = overview_file.read_text(encoding="utf-8")
    check_required_snippet(EXPECTED_SKILL_FILE, skill_text, "references/shared-copyright-notice.md", state)
    check_required_snippet(EXPECTED_SKILL_FILE, skill_text, "references/shared-overview.md", state)
    references_count = skill_text.count("references/")
    if references_count > MAX_SKILL_REFERENCE_MENTIONS:
        state.error(
            f"{EXPECTED_SKILL_FILE} should stay route-focused, found {references_count} references/ mentions"
        )
        return
    state.ok(f"{EXPECTED_SKILL_FILE} reference mentions stay within route-only threshold")


def check_required_snippet(path: Path, text: str, snippet: str, state: ValidationState) -> None:
    if snippet not in text:
        state.error(f"{path} missing required route snippet: {snippet}")
        return
    state.ok(f"{path} route snippet OK: {snippet}")


def validate_reference_navigation(state: ValidationState) -> None:
    print("\n--- Reference 导航检查（自定义约束） ---")
    references_dir = EXPECTED_SKILL_DIR / "references"
    missing_toc = []
    for path in sorted(references_dir.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) <= LONG_REFERENCE_TOC_LINE_LIMIT:
            continue
        if has_reference_toc(lines):
            continue
        missing_toc.append(path.name)
    if missing_toc:
        state.error(f"long references missing TOC: {', '.join(missing_toc)}")
        return
    state.ok("long references include TOC blocks")


def has_reference_toc(lines: list[str]) -> bool:
    preview = "\n".join(lines[:20])
    return "## 目录" in preview or "# 目录" in preview


def validate_markdown_links(state: ValidationState) -> None:
    print("\n--- Markdown 链接检查 ---")
    markdown_files = sorted(REPO_ROOT.rglob("*.md"))
    for markdown_file in markdown_files:
        if should_skip(markdown_file):
            continue
        check_links(markdown_file, state)
        if markdown_file.is_relative_to(EXPECTED_SKILL_DIR):
            check_inline_paths(markdown_file, state)


def check_links(markdown_file: Path, state: ValidationState) -> None:
    text = markdown_file.read_text(encoding="utf-8")
    for match in MD_LINK_PATTERN.finditer(text):
        target = match.group(1).split("#", 1)[0]
        if not target:
            continue
        resolved = (markdown_file.parent / target).resolve()
        if not resolved.exists():
            state.error(f"{markdown_file.relative_to(REPO_ROOT)} -> broken link: {target}")


def check_inline_paths(markdown_file: Path, state: ValidationState) -> None:
    in_fence = False
    for line_no, line in enumerate(markdown_file.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in INLINE_CODE_PATTERN.finditer(line):
            candidate = match.group(1).strip()
            if not looks_like_local_path(candidate):
                continue
            resolved = (EXPECTED_SKILL_DIR / candidate.rstrip("/")).resolve()
            if resolved.exists():
                continue
            state.error(
                f"{markdown_file.relative_to(REPO_ROOT)}:{line_no} -> broken inline path: {candidate}"
            )


if __name__ == "__main__":
    sys.exit(main())
