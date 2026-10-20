#!/usr/bin/env python3
"""Independently verify the complete before/after audit and immutable assets."""
from __future__ import annotations

import json
import hashlib
import re
import subprocess
from pathlib import Path

from skill_validation_config import PAYMENT_SOURCE_LOCK, ONBOARDING_SOURCE_LOCK, USER_ONBOARDING_SOURCE_LOCK, ONBOARDING_EXTENSION_SOURCE_LOCK
from validation_runtime import require_assertions_enabled

require_assertions_enabled()
ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / 'maintainer-contracts/api-review-2026-10-08.json'
CATALOGS = {
    'payment': 'huifu-pay-integration/references/payment-complete-field-catalog.md',
    'merchant': 'huifu-merchant-onboarding/references/merchant-onboarding-complete-field-catalog.md',
    'user': 'huifu-merchant-onboarding/references/user-onboarding-complete-field-catalog.md',
    'extension': 'huifu-merchant-onboarding/references/onboarding-extension-complete-field-catalog.md',
}


def records(text: str) -> dict:
    result = {}
    title = ''
    for line in text.splitlines():
        if line.startswith('## '):
            title = line[3:]
        if not line.startswith('| `'):
            continue
        cells = [cell.strip().replace('\\|', '|') for cell in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
        assert len(cells) in (6, 9)
        key = title, cells[0].strip('`')
        assert key not in result
        columns = ['wire','decoded','name','type','length','required','status','description'] if len(cells) == 9 else ['name','type','length','required','description']
        result[key] = dict(zip(columns, cells[1:]))
    return result


def comparison(before: dict, after: dict) -> dict:
    return {
        'before': len(before), 'after': len(after),
        'added': [{'interface': k[0], 'path': k[1], 'after': after[k]} for k in sorted(after.keys()-before.keys())],
        'removed': [{'interface': k[0], 'path': k[1], 'before': before[k]} for k in sorted(before.keys()-after.keys())],
        'changed': [{'interface': k[0], 'path': k[1], 'before': before[k], 'after': after[k]} for k in sorted(after.keys() & before.keys()) if after[k] != before[k]],
    }


def checked_path(item: dict) -> Path:
    path = ROOT / item['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], item['path']
    return path


def validate_first_review(after_paths: dict[str, Path]) -> int:
    report = json.loads(REPORT.read_text())
    commit = report['baseline_commit']
    assert re.fullmatch(r'[0-9a-f]{40}', commit)
    for name, path in CATALOGS.items():
        before = records(subprocess.check_output(['git','show',f'{commit}:{path}'], cwd=ROOT, text=True))
        after = records(after_paths[name].read_text())
        delta = comparison(before, after)
        assert report['field_comparison'][name] == delta, f'incomplete field audit: {name}'
    sources = []
    # This is a historical audit: use its own date, not the active manifest.
    for domain, prefix in [('payment','payment'),('merchant','merchant-onboarding'),('user','user-onboarding'),('extension','onboarding-extension')]:
        path = ROOT / f'maintainer-contracts/{prefix}-source-lock-2026-10-08.json'
        lock = json.loads(path.read_text())
        previous = json.loads((ROOT / lock['previous_source_lock']['path']).read_text())
        old = {item['key']:item for item in previous['sources']}
        for item in lock['sources']:
            old_sha = old.get(item['key'], {}).get('sha256')
            sources.append({'domain':domain,'key':item['key'],'url':item['url'],'before_sha256':old_sha,'after_sha256':item['sha256'],'result':'added' if old_sha is None else 'unchanged' if old_sha==item['sha256'] else 'changed'})
    assert report['source_comparison'] == sources
    assert len(sources) == 78
    assert sum(item['result']=='added' for item in sources) == 7
    assert sum(item['result']=='changed' for item in sources) == 6
    assert sum(item['result']=='unchanged' for item in sources) == 65
    assert sum(item['after'] for item in report['field_comparison'].values()) == 6296
    # Protect all prior source bytes/locks and sandbox assets, including files
    # omitted by a current catalog. Comparing bytes avoids newline exceptions.
    paths = subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'maintainer-contracts','local-sandbox'], cwd=ROOT, text=True).splitlines()
    protected = [path for path in paths if path.startswith('maintainer-contracts/official-sources/') or '/contracts/' in path or '/sample-packs/' in path or ('source-lock' in path and path.endswith('.json')) or path.startswith('maintainer-contracts/api-refresh')]
    for path in protected:
        original = subprocess.check_output(['git','show',f'{commit}:{path}'], cwd=ROOT)
        assert (ROOT / path).read_bytes() == original, f'historical evidence changed: {path}'
    return len(protected)


def main() -> int:
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    latest_path = ROOT / manifest['skills']['huifu-pay-integration'].get('api_review', str(REPORT.relative_to(ROOT)))
    if latest_path == REPORT:
        protected = validate_first_review({key: ROOT / path for key, path in CATALOGS.items()})
        print(f'API review validated: 78 documents, 6296 paths; {protected} immutable historical files')
        return 0
    report = json.loads(latest_path.read_text())
    assert report['schema_version'] == 2
    assert checked_path(report['previous_api_review']) == REPORT
    before_paths = {key: checked_path(item) for key, item in report['baseline_catalogs'].items()}
    assert set(before_paths) == set(CATALOGS)
    # Baseline hashes are anchored to the immutable first-round review records.
    payment_prior = json.loads((ROOT / 'maintainer-contracts/api-refresh-payment-online-review-2026-10-08.json').read_text())
    onboarding_prior = json.loads((ROOT / 'maintainer-contracts/api-refresh-onboarding-online-review-2026-10-08.json').read_text())
    prior_catalogs = {'payment': payment_prior['catalogs']['payment'], **onboarding_prior['catalogs']}
    prior_names = {'payment': 'payment', 'merchant': 'merchant', 'user': 'user', 'extension': 'extension'}
    for key, path in before_paths.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == prior_catalogs[prior_names[key]]['sha256'], key
    validate_first_review(before_paths)
    for key, relative in CATALOGS.items():
        assert checked_path(report['current_catalogs'][key]) == ROOT / relative
        delta = comparison(records(before_paths[key].read_text()), records((ROOT / relative).read_text()))
        assert delta == report['field_comparison'][key], f'incomplete second review: {key}'
    locks = {
        'payment': PAYMENT_SOURCE_LOCK,
        'merchant-onboarding': ONBOARDING_SOURCE_LOCK,
        'user-onboarding': USER_ONBOARDING_SOURCE_LOCK,
        'onboarding-extension': ONBOARDING_EXTENSION_SOURCE_LOCK,
    }
    source_count = changed = 0
    seen = set()
    for item in report['source_comparison']:
        domain, key = item['domain'], item['key']
        assert (domain, key) not in seen
        seen.add((domain, key))
        current_lock = json.loads(locks[domain].read_text())
        before_lock = json.loads((ROOT / f'maintainer-contracts/{domain}-source-lock-{report["baseline_date"]}.json').read_text())
        old = next(s for s in before_lock['sources'] if s['key'] == key)
        new = next(s for s in current_lock['sources'] if s['key'] == key)
        for attr in ('url', 'filename', 'title'):
            assert item[attr] == old[attr] == new[attr], (key, attr)
        assert item['before_sha256'] == old['sha256']
        assert item['after_sha256'] == new['sha256']
        expected_path = f'maintainer-contracts/official-sources/{domain}/{current_lock["source_snapshot_id"]}/{new["filename"]}'
        assert item['local_path'] == expected_path
        assert hashlib.sha256((ROOT / expected_path).read_bytes()).hexdigest() == new['sha256']
        is_changed = old['sha256'] != new['sha256']
        assert item['changed'] == is_changed
        assert item['result'] == ('changed' if is_changed else 'unchanged')
        assert item['http_status'] == 200 and item['retrieved_at'].startswith(report['review_date'])
        source_count += 1
        changed += is_changed
    assert seen == {(domain, s['key']) for domain, path in locks.items() for s in json.loads(path.read_text())['sources']}
    assert source_count == report['scope']['official_documents'] == 78
    assert changed == report['scope']['changed_existing_documents'] == 8
    assert source_count-changed == report['scope']['unchanged_documents'] == 70
    assert sum(d['after'] for d in report['field_comparison'].values()) == report['scope']['field_paths'] == 6296
    for path, digest in report['immutable_evidence'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, f'pre-existing evidence changed: {path}'
    migrations = report['path_migrations']
    added = report['field_comparison']['payment']['added']
    removed = report['field_comparison']['payment']['removed']
    migrated = set()
    for migration in migrations:
        replacements = [(r, migration['to_prefix'] + r['path'][len(migration['from_prefix']):]) for r in removed if r['interface'] == migration['interface'] and (r['path'] == migration['from_prefix'] or r['path'].startswith(migration['from_prefix']+'.'))]
        assert len(replacements) == migration['count']
        for old, new_path in replacements:
            assert any(r['interface'] == old['interface'] and r['path'] == new_path for r in added)
            migrated.add((old['interface'], old['path']))
    assert len(migrated) == len(added) == len(removed) == 100
    delta = report['field_comparison']['payment']
    lock = json.loads(PAYMENT_SOURCE_LOCK.read_text())
    for name in ('added', 'removed', 'changed'):
        assert lock['current_extension'][f'field_paths_{name}'] == len(delta[name])
    print(f'Second API review validated: 78 documents, 8 changed, 6296 paths; 100 migrations, {len(delta["changed"])} same-path changes; {len(report["immutable_evidence"])} immutable files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
