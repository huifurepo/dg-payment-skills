#!/usr/bin/env bash
# validate-skills.sh - 自动校验 skill 仓库结构和内容
# 用法: bash scripts/validate-skills.sh

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

ERRORS=0
WARNINGS=0
SKILL_FILES=(*/SKILL.md)

error() { echo "❌ ERROR: $1"; ((ERRORS++)) || true; }
warn()  { echo "⚠️  WARN:  $1"; ((WARNINGS++)) || true; }
ok()    { echo "✅ OK:    $1"; }

echo "=== Skill 仓库校验 ==="
echo ""

# 1. Check all SKILL.md have frontmatter
echo "--- Frontmatter 检查 ---"
for f in "${SKILL_FILES[@]}"; do
  if head -1 "$f" | grep -q '^---$'; then
    ok "$f has frontmatter"
  else
    error "$f missing frontmatter"
  fi
done

# 2. Check license is exact expected value
echo ""
echo "--- License 检查 ---"
for f in "${SKILL_FILES[@]}"; do
  if grep -q '^license: CC-BY-NC-4.0$' "$f"; then
    ok "$f license OK"
  else
    error "$f license is not CC-BY-NC-4.0"
  fi
done

# 3. Check frontmatter/body version consistency
echo ""
echo "--- 版本一致性 ---"
for f in "${SKILL_FILES[@]}"; do
  front_version=$(grep '^version:' "$f" | head -1 | awk '{print $2}')
  body_version=$(grep '^| Skill 版本 |' "$f" | head -1 | sed -n 's/.*`\([^`]*\)`.*/\1/p')

  if [ -z "$body_version" ]; then
    error "$f missing body version row"
  elif [ "$front_version" = "$body_version" ]; then
    ok "$f version consistent ($front_version)"
  else
    error "$f version mismatch: frontmatter=$front_version body=$body_version"
  fi
done

# 4. Check broken relative links in markdown files
echo ""
echo "--- 链接检查 ---"
while IFS= read -r f; do
  dir=$(dirname "$f")
  while IFS= read -r link; do
    target="${link%%#*}"
    if [ -n "$target" ] && [ ! -e "$dir/$target" ]; then
      error "$f -> broken link: $link"
    fi
  done < <(grep -oP '\]\((?!http)(?!#)([^)]+)\)' "$f" 2>/dev/null | sed 's/^](//' | sed 's/)$//')
done < <(find . -name "*.md" -not -path "./.tmp/*" -not -path "./.worktrees/*" -not -path "./.codex-tasks/*" -not -path "./docs/superpowers/plans/*" | sort)

# 5. Check all skill dirs are listed in README
echo ""
echo "--- README 覆盖检查 ---"
for f in "${SKILL_FILES[@]}"; do
  name="${f%/SKILL.md}"
  if grep -q "$name" README.md 2>/dev/null; then
    ok "$name in README"
  else
    error "$name missing from README"
  fi
done

# 6. Check LICENSE exists
echo ""
echo "--- 顶层文件检查 ---"
[ -f LICENSE ] && ok "LICENSE exists" || error "LICENSE missing"
[ -f CHANGELOG.md ] && ok "CHANGELOG.md exists" || error "CHANGELOG.md missing"
[ -f README.md ] && ok "README.md exists" || error "README.md missing"

echo ""
echo "=== 结果: $ERRORS errors, $WARNINGS warnings ==="
[ "$ERRORS" -eq 0 ] && echo "✅ All checks passed" || echo "❌ Fix errors before release"
exit "$ERRORS"
