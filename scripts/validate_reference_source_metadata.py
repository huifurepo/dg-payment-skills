#!/usr/bin/env python3
"""Check published metadata against the active source and version locks."""
from __future__ import annotations

import json
import re
from pathlib import Path

from skill_validation_config import (
    PAYMENT_SOURCE_LOCK, ONBOARDING_SOURCE_LOCK,
    USER_ONBOARDING_SOURCE_LOCK, ONBOARDING_EXTENSION_SOURCE_LOCK,
)
from validation_runtime import require_assertions_enabled

require_assertions_enabled()
ROOT = Path(__file__).resolve().parent.parent


def source_metadata_errors(header: str, source: dict, lock: dict) -> list[str]:
    """Only explicit current metadata is checked; historical prose is excluded."""
    errors = []
    official = source.get('official_page_update', source.get('page_updated_at'))
    for date in re.findall(r'(?:官网更新时间|官网更新|官方接口更新时间|官网)[：: ]*`?(\d{4}[.-]\d{2}[.-]\d{2})', header):
        if date.replace('.', '-') != official:
            errors.append(f'official date {date} differs from {official}')
    for date in re.findall(r'(?:本地冻结|本地活动快照|快照)[：: ]*`?(\d{4}-\d{2}-\d{2})', header):
        if date != lock['source_date']:
            errors.append(f'freeze date {date} differs from {lock["source_date"]}')
    for digest in re.findall(r'(?:SHA-256|SHA256)(?:[：: 为]|`)*([a-f0-9]{64})', header):
        if digest != source['sha256']:
            errors.append('source SHA differs from the active lock')
    return errors


def main() -> int:
    errors = []
    checked = 0
    for name, locks in (
        ('huifu-pay-integration', (PAYMENT_SOURCE_LOCK,)),
        ('huifu-merchant-onboarding', (ONBOARDING_SOURCE_LOCK, USER_ONBOARDING_SOURCE_LOCK, ONBOARDING_EXTENSION_SOURCE_LOCK)),
    ):
        sources = [(source, lock) for path in locks for lock in [json.loads(path.read_text())] for source in lock['sources']]
        for path in (ROOT / name / 'references').glob('*.md'):
            header = '\n'.join(path.read_text().splitlines()[:20])
            matches = [(source, lock) for source, lock in sources if source['url'] in header]
            if len(matches) != 1:
                continue
            checked += 1
            for error in source_metadata_errors(header, *matches[0]):
                errors.append(f'{path.relative_to(ROOT)}: {error}')
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    payment = manifest['skills']['huifu-pay-integration']['version']
    onboarding = manifest['skills']['huifu-merchant-onboarding']['version']
    payrefs = ROOT / 'huifu-pay-integration/references'
    for filename in ('shared-overview.md', 'shared-request-header-policy.md', 'shared-local-sandbox.md'):
        text = (payrefs / filename).read_text()
        declared = re.findall(r'支付 Skill(?: 为)? `([^`]+)`', text)
        assert declared and set(declared) == {payment}, f'{filename}: current version mismatch'
    policy = (ROOT / 'huifu-merchant-onboarding/references/skill-version-policy.md').read_text().split('## 更新方式', 1)[1]
    defaults = re.findall(r'`((?:hfms|hfps)/[^`]+)`', policy)
    assert defaults == [f'hfms/{onboarding}', f'hfps/{payment};hfms/{onboarding}'], defaults
    # A fixed official update date must survive a different local freeze date.
    fixture = {'official_page_update': '2026-09-22', 'sha256': 'a'*64}
    lock = {'source_date': '2026-10-08'}
    assert not source_metadata_errors('官网更新时间：`2026-09-22`；本地冻结：`2026-10-08`', fixture, lock)
    assert source_metadata_errors('官网更新时间：`2026-10-08`；本地冻结：`2026-10-08`', fixture, lock)
    assert source_metadata_errors('官网更新时间：`2026-09-22`；本地冻结：`2026-09-22`', fixture, lock)
    assert not errors, '\n'.join(errors)
    print(f'Reference metadata validated: {checked} source-linked headers; current versions and default source headers')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
