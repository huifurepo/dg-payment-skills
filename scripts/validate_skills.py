#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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
    SKILL_SPECS,
    SKILL_FILES,
    ValidationState,
)
from validate_python_contract import validate_python_prod_contract
from skill_validation_utils import (
    looks_like_local_path,
    should_skip,
    strip_quotes,
    validate_repo_files,
    validate_skill_top_level,
)

DESCRIPTION_REQUIRED_TERMS = {
    "huifu-pay-integration": (
        "聚合支付",
        "托管支付",
        "checkout-js",
        "签名",
        "幂等",
        "商户进件",
        "业务开通",
        "huifu-merchant-onboarding",
    ),
    "huifu-merchant-onboarding": (
        "企业",
        "个人",
        "开户",
        "图片",
        "业务开通",
        "业务开通修改",
        "基本信息修改",
        "费率查询",
        "状态变更",
        "短信",
        "商户详情",
        "申请状态",
        "企业用户",
        "个人用户",
        "用户业务入驻",
        "用户申请单",
        "用户信息查询",
        "支付下单",
        "支付终态",
        "huifu-pay-integration",
    ),
}


def main() -> int:
    state = ValidationState()
    print("=== Skill 仓库校验 ===\n")
    validate_repo_layout(state)
    validate_skill_top_level(state)
    validate_skill_files(state)
    validate_agents_files(state)
    validate_entry_docs(state)
    validate_regression_metadata(state)
    validate_user_onboarding_reference_contract(state)
    validate_python_prod_contract(state)
    validate_reference_navigation(state)
    validate_reference_reachability(state)
    validate_markdown_links(state)
    validate_repo_files(state)
    print(f"\n=== 结果: {state.errors} errors, {state.warnings} warnings ===")
    if state.errors == 0:
        print("[OK] All checks passed")
    else:
        print("[ERROR] Fix errors before release")
    return state.errors


def validate_repo_layout(state: ValidationState) -> None:
    print("--- 仓库发布结构检查（自定义约束） ---")
    expected_files = sorted(spec.skill_file for spec in SKILL_SPECS)
    actual_files = sorted(REPO_ROOT.glob("*/SKILL.md"))
    if actual_files != expected_files:
        found = ", ".join(str(path.relative_to(REPO_ROOT)) for path in actual_files) or "none"
        state.error(f"skill layout differs from skills-manifest.json: {found}")
    else:
        state.ok(f"skill layout matches manifest: {len(expected_files)} skills")

    for spec in SKILL_SPECS:
        references_dir = spec.references_dir
        if not references_dir.is_dir():
            state.error(f"{spec.skill_id}/references missing")
            continue
        nested_dirs = sorted(
            path.relative_to(references_dir) for path in references_dir.iterdir() if path.is_dir()
        )
        if nested_dirs:
            state.error(
                f"{spec.skill_id}: references must stay flat, found: "
                f"{', '.join(map(str, nested_dirs))}"
            )
        expected_refs = spec.expected_references
        actual_refs = {path.name for path in references_dir.glob("*.md")}
        missing_refs = sorted(expected_refs - actual_refs)
        extra_refs = sorted(actual_refs - expected_refs)
        if missing_refs:
            state.error(f"{spec.skill_id}: missing references: {', '.join(missing_refs)}")
        if extra_refs:
            state.error(f"{spec.skill_id}: unexpected references: {', '.join(extra_refs)}")
        if not missing_refs and not extra_refs:
            state.ok(f"{spec.skill_id}: reference set matches manifest ({len(actual_refs)})")


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
    missing_terms = [
        term
        for term in DESCRIPTION_REQUIRED_TERMS.get(skill_file.parent.name, ())
        if term not in description
    ]
    if missing_terms:
        state.error(
            f"{skill_file} description is missing routing terms: "
            + ", ".join(missing_terms)
        )
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
    for spec in SKILL_SPECS:
        openai_file = spec.agents_file
        if not openai_file.is_file():
            state.error(f"{openai_file.relative_to(REPO_ROOT)} missing")
            continue
        interface, quoted = parse_openai_interface(openai_file, state)
        if interface is None:
            continue
        validate_interface_string(openai_file, interface, quoted, "display_name", 1, 80, state)
        validate_interface_string(
            openai_file,
            interface,
            quoted,
            "short_description",
            MIN_SHORT_DESCRIPTION_LENGTH,
            MAX_SHORT_DESCRIPTION_LENGTH,
            state,
        )
        validate_default_prompt(interface, quoted, openai_file, spec.skill_id, state)
        validate_interface_consistency(interface, spec.skill_file, openai_file, state)
        validate_openai_policy(openai_file, state)


def validate_openai_policy(openai_file: Path, state: ValidationState) -> None:
    text = openai_file.read_text(encoding="utf-8")
    if not re.search(
        r"(?m)^policy:\s*$\n^[ ]{2}allow_implicit_invocation:\s*(?:true|false)\s*$",
        text,
    ):
        state.error(
            f"{openai_file} must explicitly set policy.allow_implicit_invocation"
        )
        return
    state.ok(f"{openai_file} invocation policy is explicit")


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
    skill_id: str,
    state: ValidationState,
) -> None:
    validate_interface_string(openai_file, interface, quoted, "default_prompt", 1, 200, state)
    prompt = interface.get("default_prompt", "")
    if f"${skill_id}" not in prompt:
        state.error(f"{openai_file} interface.default_prompt must mention ${skill_id}")
        return
    state.ok(f"{openai_file} interface.default_prompt skill reference OK")


def validate_interface_consistency(
    interface: dict[str, str],
    skill_file: Path,
    openai_file: Path,
    state: ValidationState,
) -> None:
    text = skill_file.read_text(encoding="utf-8")
    heading = extract_skill_heading(text)
    if heading is None:
        state.error(f"{skill_file} missing H1 heading for interface consistency check")
        return
    display_name = interface.get("display_name", "")
    if display_name != heading:
        state.error(f"{openai_file} interface.display_name must match SKILL.md H1 heading")
    else:
        state.ok(f"{openai_file} interface.display_name matches SKILL.md heading")
    validate_keyword_groups(
        interface.get("short_description", ""),
        build_short_description_groups(text),
        "interface.short_description",
        state,
        openai_file,
    )
    validate_keyword_groups(
        interface.get("default_prompt", ""),
        build_default_prompt_groups(text),
        "interface.default_prompt",
        state,
        openai_file,
    )


def extract_skill_heading(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def build_short_description_groups(text: str) -> list[tuple[str, tuple[str, ...]]]:
    groups: list[tuple[str, tuple[str, ...]]] = []
    if "# 汇付商户进件" in text:
        return [("商户进件", ("商户进件", "进件"))]
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
    openai_file: Path,
) -> None:
    for label, options in groups:
        if any(option in value for option in options):
            state.ok(f"{openai_file} {field_name} covers {label}")
            continue
        state.error(f"{openai_file} {field_name} missing keyword group: {label}")


def validate_entry_docs(state: ValidationState) -> None:
    print("\n--- 入口文档检查（自定义约束） ---")
    for spec in SKILL_SPECS:
        skill_text = spec.skill_file.read_text(encoding="utf-8")
        check_required_snippet(
            spec.skill_file, skill_text, "references/shared-copyright-notice.md", state
        )
        check_required_snippet(spec.skill_file, skill_text, "references/shared-overview.md", state)
        references_count = skill_text.count("references/")
        if references_count > spec.max_reference_mentions:
            state.error(
                f"{spec.skill_file} should stay route-focused, found "
                f"{references_count} references/ mentions"
            )
            continue
        state.ok(
            f"{spec.skill_file} reference mentions stay within "
            f"{spec.max_reference_mentions}"
        )


def validate_regression_metadata(state: ValidationState) -> None:
    print("\n--- 回归 Prompt 元数据检查 ---")
    prompts_file = REPO_ROOT / "scripts" / "huifu-payment-test-prompts.json"
    runner_file = REPO_ROOT / "scripts" / "run_real_model_regression.py"
    readme_file = REPO_ROOT / "README.md"

    prompts = json.loads(prompts_file.read_text(encoding="utf-8"))
    prompt_ids = {int(item["id"]) for item in prompts}
    runner_text = runner_file.read_text(encoding="utf-8")
    rule_ids = {int(match.group(1)) for match in re.finditer(r"^\s+(\d+):\s+CaseRule", runner_text, flags=re.M)}
    missing_rules = sorted(prompt_ids - rule_ids)
    if missing_rules:
        state.error(f"missing regression rule ids: {', '.join(map(str, missing_rules))}")
    else:
        state.ok(f"all {len(prompt_ids)} regression prompts have runner rules")
    suite_counts = {
        suite: sum(1 for item in prompts if item.get("suite") == suite)
        for suite in ("payment", "onboarding")
    }
    if suite_counts != {"payment": 58, "onboarding": 32}:
        state.error(f"regression ownership/count changed unexpectedly: {suite_counts}")
    else:
        state.ok("90 cases have unique payment=58/onboarding=32 ownership")
    expected_suite_files = {
        "payment": [item for item in prompts if item.get("suite") == "payment"],
        "onboarding": [item for item in prompts if item.get("suite") == "onboarding"],
    }
    for suite, expected_items in expected_suite_files.items():
        suite_file = REPO_ROOT / f"tests/regression/{suite}.json"
        actual_items = json.loads(suite_file.read_text(encoding="utf-8"))
        if actual_items != expected_items:
            state.error(f"{suite_file.relative_to(REPO_ROOT)} drifted from canonical prompts")
        else:
            state.ok(f"{suite}: generated regression suite matches canonical prompts")
    cross_file = REPO_ROOT / "tests/regression/cross-route.json"
    cross_cases = json.loads(cross_file.read_text(encoding="utf-8"))
    if len(cross_cases) != 35 or any(item.get("suite") != "cross-route" for item in cross_cases):
        state.error("cross-route regression suite must contain 35 tagged cases")
    else:
        state.ok("cross-route regression suite count OK: 35")

    user_file = REPO_ROOT / "tests/regression/user-onboarding.json"
    user_cases = json.loads(user_file.read_text(encoding="utf-8"))
    user_ids = {int(item["id"]) for item in user_cases}
    missing_user_rules = sorted(user_ids - rule_ids)
    if (
        len(user_cases) != 15
        or any(item.get("suite") != "user-onboarding" for item in user_cases)
        or missing_user_rules
    ):
        state.error(
            "user-onboarding regression suite must contain 15 tagged cases "
            f"with rules; missing={missing_user_rules}"
        )
    else:
        state.ok("user-onboarding regression suite count/rules OK: 15")

    smoke_match = re.search(r"SMOKE_CASE_IDS\s*=\s*\(([^)]*)\)", runner_text)
    smoke_ids = set()
    if smoke_match:
        smoke_ids = {int(value) for value in re.findall(r"\d+", smoke_match.group(1))}
    required_smoke_ids = {34, 35, 36, 37, 38, 89, 90, 201, 205, 207, 208, 212, 213, 214, 1001, 1002, 1019, 1032}
    missing_smoke = sorted(required_smoke_ids - smoke_ids)
    if missing_smoke:
        state.error(f"smoke regression missing required 1.3.0 cases: {', '.join(map(str, missing_smoke))}")
    else:
        state.ok("smoke regression covers 1.3.0 field/API refresh cases")

    for spec in SKILL_SPECS:
        canonical_files = [spec.references_dir / "canonical-regression-prompts.md"]
        user_canonical = spec.references_dir / "user-onboarding-canonical-regression-prompts.md"
        if user_canonical.is_file():
            canonical_files.append(user_canonical)
        canonical_count = sum(
            len(re.findall(r"^### [COU]\d+", path.read_text(encoding="utf-8"), flags=re.M))
            for path in canonical_files
        )
        expected_count = spec.canonical_regression_count
        if canonical_count != expected_count:
            state.error(
                f"{spec.skill_id}: canonical prompt count must be "
                f"{expected_count}, found {canonical_count}"
            )
        else:
            state.ok(f"{spec.skill_id}: canonical regression prompt count OK")

    readme_text = readme_file.read_text(encoding="utf-8")
    stale_claims = [claim for claim in ("5/5 passed", "34/34 passed", "5 条随 Skill 分发") if claim in readme_text]
    if stale_claims:
        state.error(f"README.md has stale regression claims: {', '.join(stale_claims)}")
    else:
        state.ok("README.md regression claims avoid stale fixed totals")

    regression_counts = {
        "payment": suite_counts["payment"],
        "onboarding": suite_counts["onboarding"],
        "user-onboarding": len(user_cases),
        "cross-route": len(cross_cases),
    }
    expected_release_counts = (
        f"执行{regression_counts['payment']}、{regression_counts['onboarding']}、"
        f"{regression_counts['user-onboarding']}、{regression_counts['cross-route']}个真实模型案例"
    )
    expected_regression_summary = (
        f"当前共{sum(regression_counts.values())}个真实模型案例："
        f"支付{regression_counts['payment']}、商户进件{regression_counts['onboarding']}、"
        f"用户开户{regression_counts['user-onboarding']}、跨域路由{regression_counts['cross-route']}。"
    )
    missing_readme_counts = [
        claim
        for claim in (expected_release_counts, expected_regression_summary)
        if claim not in readme_text
    ]
    if missing_readme_counts:
        state.error(
            "README.md regression suite counts differ from suite files: "
            + " | ".join(missing_readme_counts)
        )
    else:
        state.ok(f"README.md regression suite counts match suite files: {regression_counts}")


def check_required_snippet(path: Path, text: str, snippet: str, state: ValidationState) -> None:
    if snippet not in text:
        state.error(f"{path} missing required route snippet: {snippet}")
        return
    state.ok(f"{path} route snippet OK: {snippet}")


def validate_user_onboarding_reference_contract(state: ValidationState) -> None:
    print("\n--- 用户开户冲突保真检查 ---")
    root = REPO_ROOT / "huifu-merchant-onboarding"
    required_terms = {
        root / "SKILL.md": (
            "条件必填",
            "只有业务入驻修改 `async.data` 的说明为空",
            "已没有长度为空的标量叶字段",
            "九页官网都把外层 `response.data`",
            "父节点整体缺失",
            "个人用户只允许 `card_type=1`",
            "RECV_ORD_ID_` + `req_seq_id",
            "user-onboarding-platform-contracts.md",
            "官方 SDK-first 与图片例外",
            "不存在本 Skill 曾推断的 TLS 硬停问题",
            "常规接口真实请求都使用官方 Request/Client 入口",
            "SDK 没有专属 Request/路由时",
            "唯一例外是 `/v2/supplementary/picture`",
            "PHP/Python 图片上传按上述唯一例外允许受控降级",
            "商户费率查询仍禁止手写 HTTP",
        ),
        root / "references/shared-server-sdk-matrix.md": (
            "只使用官方 Request/SDK 主链路",
            "不存在此前 Skill 推断的 TLS 问题",
            "按官方 Request/Client 生成真实调用",
            "常规接口不得用",
            "唯一例外是 `/v2/supplementary/picture`",
            "受控降级",
            "不得只让 Python 用 SDK",
        ),
        root / "references/user-onboarding-shared-server-sdk-matrix.md": (
            "官方 SDK-only 传输规则",
            "不存在此前 Skill 推断的 TLS 问题",
            "九接口均使用各自官方 Request/Client",
            "V2UserBasicdataIndvModifyRequest",
            "V2UserBusiModifyRequest",
            "V2UserListQueryRequest",
            "HttpClient",
            "OkHttp",
            "Guzzle",
            "自实现签名/验签客户端",
            "三语言交付分别使用官方 SDK",
        ),
        root / "references/user-onboarding-field-contracts.md": (
            "九页正式公共返回表都把外层 `response.data` 标为 `N`",
            "用户业务入驻修改仍为 `String`，其余为 `Json`",
            "成功码下缺少 `data` 按协议异常处理",
            "async.data.huifu_id:String(18) Y",
            "条件必填",
            "response.data.ent_base_info.file_list[]",
            "response.data.indv_base_info.file_list[]",
            "elec_acct_config.elec_card_list",
            "out_settle_acct_type",
            "weekday_fix_amt",
            "weekday_fee_rate",
            "response.data.elec_acct_config.elec_card_list[].mp",
            "response.data.qry_cash_card_info_list[].branch_code",
            "response.sign:String(512)",
            "request.data.legal_name",
            "request.data.legal_cert_no",
            "个人用户只允许 `1`",
            "RECV_ORD_ID_` + `req_seq_id",
        ),
        root / "references/user-onboarding-individual-modify.md": (
            "/v2/user/basicdata/indv/modify",
            "V2UserBasicdataIndvModifyRequest",
            "共26个字段路径",
            "请求21、同步响应5、异步0",
            "直属汇付客户 ID",
            "cert_validity_type:String(1) N",
            "正式枚举只有 1=长期有效、0=非长期有效",
            "String(JSON Array)",
            "file_id:String(64)",
            "file_name:String(64)",
            "dict.update",
        ),
        root / "references/user-onboarding-business-modify.md": (
            "/v2/user/busi/modify",
            "V2UserBusiModifyRequest",
            "共120个字段路径",
            "请求85、同步响应11、异步24",
            "只声明一次 `file_list`",
            "elec_receipt_config",
            "Object",
            "jsonObject字符串",
            "sign_user_info",
            "exact-key",
            "RECV_ORD_ID_` + `req_seq_id",
        ),
        root / "references/user-onboarding-list-query.md": (
            "/v2/user/list/query",
            "V2UserListQueryRequest",
            "共17个完整字段路径",
            "请求8、同步响应9",
            "user_list_info_list` 修正为 `Object N",
            "原生 JSON Array",
            "user_list_info_list[].huifu_id`",
            "user_list_info_list[].upper_huifu_id`",
            "`String(18) N`",
            "上限为18",
            "`sign:String(512) Y`",
            "legal_cert_no/req_date/req_seq_id",
            "upper_huifu_id",
            "exact-key",
        ),
        root / "references/user-onboarding-platform-contracts.md": (
            "异步消息简介",
            "SHA256WithRSA",
            "原始 `data` 字符串",
            "RECV_ORD_ID_` + `async.data.req_seq_id",
            "控台 Webhook",
            "个人用户只允许对私法人卡",
            "成功响应返回 `apply_no`",
            "wire 矩阵",
            "response.data.qry_cash_card_info_list",
        ),
        root / "references/user-onboarding-business-open.md": (
            "user-onboarding-complete-field-catalog.md",
            "汇付客户号",
            "userHuifuId",
            "两个角色不得交换",
            "constant_amt",
            "fixed_ratio",
            "card_info.card_name",
            "`response.data` 定义为 `Json N`",
            "个人用户只允许 `1`",
            "RECV_ORD_ID_` + `req_seq_id",
        ),
        root / "references/user-onboarding-detail-query.md": (
            "user-onboarding-complete-field-catalog.md",
            "同一商户号当天唯一",
            "response.data.ent_base_info.file_list[]",
            "response.data.indv_base_info.file_list[]",
            "elec_acct_config.elec_card_list",
            "out_settle_acct_type",
            "weekday_fix_amt",
            "weekday_fee_rate",
            "elec_card_list[].mp:String(11)",
            "qry_cash_card_info_list[].branch_code",
            "response.data:Json` 的官网必填列为 `N`",
            "String(JSON Object)",
            "card_type=1",
        ),
        root / "references/user-onboarding-individual.md": (
            "必填列为 `N`",
            "实名认证",
            "用户业务入驻修改且电子回单配置开通",
            "response.data:Json` 的官网必填列为 `N`",
        ),
        root / "references/user-onboarding-enterprise.md": (
            "用户业务入驻修改且电子回单配置开通",
            "姓名与证件实名认证",
            "response.data:Json` 的官网必填列为 `N`",
        ),
        root / "references/user-onboarding-application-status-query.md": (
            "user-onboarding-complete-field-catalog.md",
            "用户信息查询页面也独立声明相同规则",
            "不能外推成所有用户接口",
            "`apply_status` | 官网必填列为 `N`",
            "四种状态均返回",
            "response.data:Json` 的官网必填列为 `N`",
        ),
        root / "references/user-onboarding-external-resources.md": (
            "request.data.card_info.branch_code",
            "response.data.elec_acct_config.elec_card_list[].branch_code",
            "response.data.qry_cash_card_info_list[].branch_code",
            "基础参数汇总",
            "不是按同名叶字段猜测",
        ),
        root / "references/user-onboarding-shared-request-field-preservation.md": (
            "申请状态查询和用户信息查询页面",
            "同一商户号当天唯一",
            "不得外推成所有用户接口",
        ),
        root / "references/user-onboarding-shared-overview.md": (
            "条件选填",
            "async.data.huifu_id",
            "ent_base_info.file_list",
            "out_settle_acct_type",
            "weekday_fix_amt",
            "weekday_fee_rate",
            "只有业务入驻修改 `async.data` 的说明为空",
            "已没有长度为空的标量叶字段",
        ),
        REPO_ROOT / "maintainer-contracts/api-refresh-user-onboarding-2026-08-10.json": (
            "request.data.*[required=C]",
            "async.data.huifu_id",
            "response.data.ent_base_info.file_list[]",
            "response.data.indv_base_info.file_list[]",
            "response.data.elec_acct_config.elec_card_list[]",
            "response.data.settle_config_list[].out_settle_acct_type",
            "response.data.qry_cash_config_list[].weekday_fix_amt|weekday_fee_rate",
            "official_undefined_fields",
            "official_request_example_anomalies_guarded",
            "official_response_example_anomalies_guarded",
            "official_example_shape_contract",
            "page_field_notes_preserved",
            "official_incomplete_links",
            "official_ambiguous_semantics",
            "public_sources",
            "integration_decisions",
        ),
    }
    failures: list[str] = []
    for path, terms in required_terms.items():
        text = path.read_text(encoding="utf-8")
        missing = [term for term in terms if term not in text]
        if missing:
            failures.append(
                f"{path.relative_to(REPO_ROOT)} missing {', '.join(missing)}"
            )
    if failures:
        for failure in failures:
            state.error(failure)
        return
    external_text = (
        root / "references/user-onboarding-external-resources.md"
    ).read_text(encoding="utf-8")
    if "| 银行支行编码 | `branch_code` |" in external_text:
        state.error(
            "user-onboarding external resources must not map every branch_code leaf "
            "to one URL"
        )
        return
    state.ok("user-onboarding conflict, uniqueness and nested-path summaries are preserved")


def validate_reference_navigation(state: ValidationState) -> None:
    print("\n--- Reference 导航检查（自定义约束） ---")
    missing_toc = []
    for spec in SKILL_SPECS:
        for path in sorted(spec.references_dir.glob("*.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            if len(lines) <= LONG_REFERENCE_TOC_LINE_LIMIT:
                continue
            if has_reference_toc(lines):
                continue
            missing_toc.append(f"{spec.skill_id}/{path.name}")
    if missing_toc:
        state.error(f"long references missing TOC: {', '.join(missing_toc)}")
        return
    state.ok("long references include TOC blocks")


def validate_reference_reachability(state: ValidationState) -> None:
    print("\n--- Reference 可达性检查 ---")
    reference_name_pattern = re.compile(
        r"(?<![A-Za-z0-9_.-])([A-Za-z0-9][A-Za-z0-9._-]*\.md)"
    )
    entry_reference_pattern = re.compile(r"references/([A-Za-z0-9][A-Za-z0-9._-]*\.md)")

    for spec in SKILL_SPECS:
        reference_paths = {
            path.name: path for path in sorted(spec.references_dir.glob("*.md"))
        }
        entry_text = spec.skill_file.read_text(encoding="utf-8")
        pending = [
            name
            for name in entry_reference_pattern.findall(entry_text)
            if name in reference_paths
        ]
        reachable: set[str] = set()

        while pending:
            name = pending.pop()
            if name in reachable:
                continue
            reachable.add(name)
            text = reference_paths[name].read_text(encoding="utf-8")
            pending.extend(
                candidate
                for candidate in reference_name_pattern.findall(text)
                if candidate in reference_paths and candidate not in reachable
            )

        missing = sorted(set(reference_paths) - reachable)
        if missing:
            state.error(
                f"{spec.skill_id}: orphan references not reachable from SKILL.md: "
                + ", ".join(missing)
            )
            continue
        state.ok(
            f"{spec.skill_id}: all {len(reference_paths)} references are reachable "
            "from SKILL.md"
        )


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
        for spec in SKILL_SPECS:
            if markdown_file.is_relative_to(spec.root):
                check_inline_paths(markdown_file, spec.root, state)
                break


def check_links(markdown_file: Path, state: ValidationState) -> None:
    text = markdown_file.read_text(encoding="utf-8")
    for match in MD_LINK_PATTERN.finditer(text):
        target = match.group(1).split("#", 1)[0]
        if not target:
            continue
        resolved = (markdown_file.parent / target).resolve()
        if not resolved.exists():
            state.error(f"{markdown_file.relative_to(REPO_ROOT)} -> broken link: {target}")


def check_inline_paths(markdown_file: Path, skill_root: Path, state: ValidationState) -> None:
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
            resolved = (skill_root / candidate.rstrip("/")).resolve()
            if resolved.exists():
                continue
            state.error(
                f"{markdown_file.relative_to(REPO_ROOT)}:{line_no} -> broken inline path: {candidate}"
            )


if __name__ == "__main__":
    sys.exit(main())
