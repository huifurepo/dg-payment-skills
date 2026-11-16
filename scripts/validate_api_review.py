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


def validate_second_review(latest_path: Path, after_paths: dict | None = None, locks: dict | None = None) -> int:
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
        current = after_paths[key] if after_paths is not None else ROOT / relative
        assert report['current_catalogs'][key]['path'] == relative
        assert hashlib.sha256(current.read_bytes()).hexdigest() == report['current_catalogs'][key]['sha256']
        delta = comparison(records(before_paths[key].read_text()), records(current.read_text()))
        assert delta == report['field_comparison'][key], f'incomplete second review: {key}'
    locks = locks or {
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
    lock = json.loads(locks['payment'].read_text())
    for name in ('added', 'removed', 'changed'):
        assert lock['current_extension'][f'field_paths_{name}'] == len(delta[name])
    print(f'Second API review validated: 78 documents, 8 changed, 6296 paths; 100 migrations, {len(delta["changed"])} same-path changes; {len(report["immutable_evidence"])} immutable files')
    return 0


def validate_current_review(path: Path, after_paths: dict[str, Path] | None = None, locks: dict[str, Path] | None = None) -> int:
    report = json.loads(path.read_text())
    assert report['schema_version'] == 3
    previous = checked_path(report['previous_api_review'])
    assert previous == ROOT / 'maintainer-contracts/api-review-2026-10-10.json'
    baseline = {key: checked_path(item) for key, item in report['baseline_catalogs'].items()}
    prior_locks = {key: checked_path(item) for key, item in report['baseline_source_locks'].items()}
    validate_second_review(previous, baseline, prior_locks)
    for key, name in CATALOGS.items():
        current = after_paths[key] if after_paths is not None else ROOT / name
        assert report['current_catalogs'][key]['path'] == name
        assert hashlib.sha256(current.read_bytes()).hexdigest() == report['current_catalogs'][key]['sha256']
        actual = comparison(records(baseline[key].read_text()), records(current.read_text()))
        assert actual == report['field_comparison'][key], ('incomplete current field audit', key)
    expected_locks = locks or {'payment': PAYMENT_SOURCE_LOCK, 'merchant-onboarding': ONBOARDING_SOURCE_LOCK,
                      'user-onboarding': USER_ONBOARDING_SOURCE_LOCK, 'onboarding-extension': ONBOARDING_EXTENSION_SOURCE_LOCK}
    active = {key: json.loads(checked_path(item).read_text()) for key, item in report['current_source_locks'].items()}
    for key, item in report['current_source_locks'].items():
        assert checked_path(item) == expected_locks[key]
    audit = json.loads(checked_path(report['source_audit']).read_text())
    assert audit['source_count'] == 78
    domains = {'payment': 'payment', 'merchant_onboarding': 'merchant-onboarding', 'user_onboarding': 'user-onboarding', 'onboarding_extension': 'onboarding-extension'}
    seen = set()
    for row in audit['sources']:
        domain = domains[row['domain']]
        identity = domain, row['key']
        assert identity not in seen; seen.add(identity)
        old = next(s for s in json.loads(prior_locks[domain].read_text())['sources'] if s['key'] == row['key'])
        new = next(s for s in active[domain]['sources'] if s['key'] == row['key'])
        assert row['before_sha256'] == old['sha256'] and row['after_sha256'] == new['sha256']
        assert row['url'] == old['url'] == new['url']
        assert row['http_status'] == 200
        assert hashlib.sha256((ROOT / row['after_file']).read_bytes()).hexdigest() == new['sha256']
        assert row['byte_changed'] == (old['sha256'] != new['sha256'])
        assert 'field_review_error' not in row
    assert len(seen) == 78
    assert sum(row['byte_changed'] for row in audit['sources']) == 13
    assert sum(row['result'] == 'unchanged' for row in audit['sources']) == 65
    assert sum(item['after'] for item in report['field_comparison'].values()) == 6500
    for name, expected in report['immutable_evidence'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    additions = [json.loads((ROOT / name).read_text()) for name in report['new_interface_locks']]
    assert sum(lock['totals']['interfaces'] for lock in additions) == 9
    assert sum(lock['totals']['field_paths'] for lock in additions) == 368
    assert report['scope']['total_apis'] == 67 and report['scope']['total_field_paths'] == 6868
    print('Current API review validated: 78 existing sources, 13 updates, 6500 base paths + 368 additional paths; all historical audit chains preserved')
    return 0


def validate_payout_review(path: Path, after_paths: dict[str, Path] | None = None,
                           locks: dict[str, Path] | None = None,
                           additional_locks: dict[str, Path] | None = None) -> int:
    from datetime import datetime
    from zoneinfo import ZoneInfo
    import difflib
    report = json.loads(path.read_text())
    assert report['schema_version'] == 4
    assert report['review_date'] == '2026-11-04'
    previous = checked_path(report['previous_api_review'])
    baseline = {key: checked_path(item) for key, item in report['baseline_catalogs'].items()}
    prior = {key: checked_path(item) for key, item in report['baseline_source_locks'].items()}
    validate_current_review(previous, {key: baseline[key] for key in CATALOGS}, prior)
    all_catalogs = {**CATALOGS,
        'payment-additions': 'huifu-pay-integration/references/payment-extension-complete-field-catalog.md',
        'merchant-account': 'huifu-merchant-onboarding/references/merchant-account-complete-field-catalog.md'}
    assert set(baseline) == set(report['current_catalogs']) == set(all_catalogs)
    for key, name in all_catalogs.items():
        original = subprocess.check_output(['git', 'show', report['baseline_commit'] + ':' + name], cwd=ROOT)
        assert baseline[key].read_bytes() == original, ('baseline must be original Git blob', key)
        current_catalog = after_paths[key] if after_paths is not None else ROOT / name
        assert report['current_catalogs'][key]['path'] == name
        assert hashlib.sha256(current_catalog.read_bytes()).hexdigest() == report['current_catalogs'][key]['sha256']
        assert comparison(records(original.decode()), records(current_catalog.read_text())) == report['field_comparison'][key]
    current = {key: checked_path(item) for key, item in report['current_source_locks'].items()}
    assert current == (locks or {'payment': PAYMENT_SOURCE_LOCK, 'merchant-onboarding': ONBOARDING_SOURCE_LOCK,
                                'user-onboarding': USER_ONBOARDING_SOURCE_LOCK, 'onboarding-extension': ONBOARDING_EXTENSION_SOURCE_LOCK})
    plan = json.loads(checked_path(report['plan_review']).read_text())
    checked_path(plan['plan'])
    assert plan['status'] == 'approved-for-implementation' and len(plan['reviews']) == 3
    assert all(row['status'] == 'no-unresolved-blockers' for row in plan['reviews'])
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    old_sources, new_sources = {}, {}
    def add_sources(target, lock, domain, additional=False):
        for source in lock['sources']:
            key = source['key']
            assert key not in target
            raw = source['path'] if additional else f"maintainer-contracts/official-sources/{domain}/{lock['source_snapshot_id']}/{source['filename']}"
            assert hashlib.sha256((ROOT / raw).read_bytes()).hexdigest() == source['sha256']
            target[key] = {**source, 'raw_path': raw}
    for domain in prior:
        add_sources(old_sources, json.loads(prior[domain].read_text()), domain)
        add_sources(new_sources, json.loads(current[domain].read_text()), domain)
    assert len(report['current_additional_sources']) == 2
    for row in report['current_additional_sources']:
        skill = row['skill']
        old = json.loads(checked_path(report['prior_additional_locks'][skill]).read_text())
        additive_path = additional_locks[skill] if additional_locks is not None else ROOT / manifest['skills'][skill]['additional_source_lock']
        lock = json.loads(additive_path.read_text())
        assert row['sources'] == lock['sources'] and row['totals'] == lock['totals'] and row['catalog'] == lock['catalog']
        add_sources(old_sources, old, '', True); add_sources(new_sources, lock, '', True)
    audit = json.loads(checked_path(report['source_audit']).read_text())
    assert len(old_sources) == 87 and len(new_sources) == 93
    assert len(audit['sources']) == 93
    seen = set()
    resolved = []
    for row in audit['sources']:
        key = row['key']; assert key not in seen; seen.add(key)
        new = new_sources[key]; old = old_sources.get(key)
        assert row['url'] == new['url'] and row['after_sha256'] == new['sha256']
        assert row['after_file'] == new['raw_path']
        assert row['http_status'] == 200
        assert datetime.fromisoformat(row['retrieved_at']).astimezone(ZoneInfo(report['snapshot_timezone'])).date().isoformat() == report['review_date']
        assert 'field_review_error' not in row
        if 'generic_parser_diagnostic' in row:
            assert row['semantic_resolution']['status'] == 'resolved-by-specialized-parsers'
            assert key in {'wechat_config', 'alipay_realname_query'}
            resolved.append(key)
        if old:
            assert row['before_sha256'] == old['sha256']
            assert row['baseline_file'] == old['raw_path'] and row['url'] == old['url']
            assert row['byte_changed'] == (old['sha256'] != new['sha256'])
            diff = ''.join(difflib.unified_diff((ROOT / old['raw_path']).read_text(encoding='utf-8-sig').splitlines(keepends=True),
                                              (ROOT / new['raw_path']).read_text(encoding='utf-8-sig').splitlines(keepends=True),
                                              fromfile=old['raw_path'], tofile=new['raw_path']))
            assert row['unified_diff'] == diff
        else:
            assert row['result'] == 'new' and row['unified_diff'] is None
    assert seen == new_sources.keys() and sorted(resolved) == ['alipay_realname_query', 'wechat_config']
    assert sum(row.get('byte_changed', False) for row in audit['sources'] if row['key'] in old_sources) == 8
    assert sum(row['result'] == 'unchanged' for row in audit['sources']) == 79
    assert sum(row['result'] == 'new' for row in audit['sources']) == 6
    assert audit['fetch_summary'] == {'success': 93, 'http_failures': 0, 'format_failures': 0}
    assert audit['semantic_parse_summary']['unresolved'] == 0
    # Specialized generator and independent raw parser resolve two generic-parser diagnostics.
    import generate_onboarding_extension_field_catalog as gen
    import validate_onboarding_extension_source_contract as independent
    extension_lock = json.loads(current['onboarding-extension'].read_text())
    extension_source_dir = ROOT / 'maintainer-contracts/official-sources/onboarding-extension' / extension_lock['source_snapshot_id']
    generated, _ = gen.build_catalog(extension_source_dir)
    extension_catalog = after_paths['extension'] if after_paths is not None else ROOT / CATALOGS['extension']
    assert generated == extension_catalog.read_text()
    if after_paths is None:
        independent.main()
    delta = report['field_comparison']['merchant']
    assert (len(delta['added']),len(delta['removed']),len(delta['changed'])) == (106,62,7)
    assert report['field_comparison']['payment-additions']['after'] - report['field_comparison']['payment-additions']['before'] == 198
    assert sum(v['after'] for v in report['field_comparison'].values()) == report['scope']['total_field_paths'] == 7110
    assert report['scope']['total_apis'] == 73
    checked_path(report['sdk_evidence'])
    for name, expected in report['immutable_evidence'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    print('Payout API audit passed: all 93 sources, 87 comparisons, eight updates, six additions; six Git-anchored baselines, 7110 paths, full immutable history')
    return 0


def validate_onboarding_maintenance_review(path: Path) -> int:
    """Verify an independently dated onboarding refresh without advancing payment."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    import difflib
    report = json.loads(path.read_text())
    assert report['schema_version'] == 5 and report['review_kind'] == 'onboarding-only-refresh'
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    skill = 'huifu-merchant-onboarding'
    spec = manifest['skills'][skill]
    assert path == ROOT / spec['api_review']
    assert report['skill'] == skill and report['version_before'] == report['version_after'] == spec['version'] == '1.2.0'
    # These are historical review context, not permanent version locks on
    # unrelated Skills: they must remain independently upgradeable.
    for name, previous_spec in report['preserved_skills'].items():
        assert name != skill and previous_spec['root'] == name
    assert report['preserved_skills']['huifu-pay-integration']['api_review'] == report['previous_api_review']['path']
    previous_path = checked_path(report['previous_api_review'])
    previous = json.loads(previous_path.read_text())
    baseline = {name: checked_path(row) for name, row in report['baseline_catalogs'].items()}
    assert set(baseline) == set(previous['current_catalogs'])
    for name, item in previous['current_catalogs'].items():
        assert hashlib.sha256(baseline[name].read_bytes()).hexdigest() == item['sha256'], name
    old_locks = {name: checked_path(row) for name, row in report['baseline_source_locks'].items()}
    assert report['baseline_source_locks'] == previous['current_source_locks']
    old_additions = {name: checked_path(row) for name, row in report['prior_additional_locks'].items()}
    validate_payout_review(previous_path, baseline, old_locks, old_additions)
    prior_refresh_path = checked_path(report['previous_refresh'])
    prior_refresh = json.loads(prior_refresh_path.read_text())
    assert prior_refresh['api_source_date'] == previous['review_date']
    # Frozen files must also equal the predecessor's own package-source contracts.
    for name, row in prior_refresh['catalogs'].items():
        assert hashlib.sha256(baseline[name].read_bytes()).hexdigest() == row['sha256']
    old_add = json.loads(old_additions[skill].read_text())
    assert hashlib.sha256(baseline['merchant-account'].read_bytes()).hexdigest() == old_add['catalog']['sha256']
    paths = {name: checked_path(row) for name, row in report['current_catalogs'].items()}
    assert set(paths) == {'merchant', 'user', 'extension', 'merchant-account'}
    for name, current in paths.items():
        assert current == ROOT / ({**CATALOGS, 'merchant-account': 'huifu-merchant-onboarding/references/merchant-account-complete-field-catalog.md'}[name])
        actual = comparison(records(baseline[name].read_text()), records(current.read_text()))
        assert actual == report['field_comparison'][name], ('incomplete refresh delta', name)
    current_locks = {name: checked_path(row) for name, row in report['current_source_locks'].items()}
    assert current_locks == {'merchant-onboarding': ONBOARDING_SOURCE_LOCK,
                             'user-onboarding': USER_ONBOARDING_SOURCE_LOCK,
                             'onboarding-extension': ONBOARDING_EXTENSION_SOURCE_LOCK}
    current_add = json.loads((ROOT / spec['additional_source_lock']).read_text())
    for key in ('skill', 'catalog', 'sources', 'totals'):
        assert report['current_additional_sources'][key] == current_add[key]
    before, after = {}, {}
    def collect(target, lock, group=None):
        for entry in lock['sources']:
            identity = group or 'merchant-account', entry['key']
            assert identity not in target
            source = entry['path'] if group is None else f"maintainer-contracts/official-sources/{group}/{lock['source_snapshot_id']}/{entry['filename']}"
            assert hashlib.sha256((ROOT / source).read_bytes()).hexdigest() == entry['sha256']
            target[identity] = {**entry, 'raw_path': source}
    for group, lock_path in current_locks.items():
        collect(before, json.loads(old_locks[group].read_text()), group)
        collect(after, json.loads(lock_path.read_text()), group)
    collect(before, old_add); collect(after, current_add)
    assert before.keys() == after.keys() and len(after) == 36
    audit = json.loads(checked_path(report['source_audit']).read_text())
    assert len(audit['sources']) == audit['source_count'] == 36
    seen = set()
    changed = []
    for row in audit['sources']:
        identity = row['directory'], row['key']
        assert identity not in seen; seen.add(identity)
        old, new = before[identity], after[identity]
        assert row['http_status'] == 200 and 'error' not in row
        assert row['url'] == old['url'] == new['url']
        assert row['baseline_file'] == old['raw_path'] and row['after_file'] == new['raw_path']
        assert row['before_sha256'] == old['sha256'] and row['after_sha256'] == new['sha256']
        assert datetime.fromisoformat(row['retrieved_at']).astimezone(ZoneInfo(report['snapshot_timezone'])).date().isoformat() == report['review_date']
        assert row['byte_changed'] == (old['sha256'] != new['sha256'])
        actual_diff = ''.join(difflib.unified_diff((ROOT / old['raw_path']).read_text(encoding='utf-8-sig').splitlines(keepends=True),
                                                (ROOT / new['raw_path']).read_text(encoding='utf-8-sig').splitlines(keepends=True),
                                                fromfile=old['raw_path'], tofile=new['raw_path']))
        assert row['unified_diff'] == actual_diff
        if row['byte_changed']: changed.append(identity)
    assert seen == after.keys() and changed == [('merchant-onboarding', 'business_open_modify')]
    assert audit['counts'] == {'changed': 1, 'unchanged': 35, 'failed': 0}
    deltas = report['field_comparison']
    assert all(not row[attribute] for row in deltas.values() for attribute in ('added', 'removed'))
    assert sum(len(row['changed']) for row in deltas.values()) == 1
    change = deltas['merchant']['changed'][0]
    assert change['interface'] == '商户业务开通修改'
    assert change['path'] == 'request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.sign_start_date'
    assert change['before']['length'] == '`7`' and change['after']['length'] == '`8`'
    assert {k:v for k,v in change['before'].items() if k != 'length'} == {k:v for k,v in change['after'].items() if k != 'length'}
    assert sum(row['after'] for row in deltas.values()) == report['scope']['field_paths'] == 3578
    assert report['scope'] == {'official_documents': 36, 'changed_documents': 1, 'unchanged_documents': 35,
                               'interfaces': 36, 'field_paths': 3578, 'added': 0, 'removed': 0, 'changed': 1}
    # Final locks and refreshes are checked after report -> online -> refresh construction.
    from additional_source_bindings import additional_bindings
    additional_bindings(ROOT, spec)
    formal = json.loads((ROOT / spec['refresh_contract']).read_text())
    assert checked_path(formal['field_review']) == path
    source_review = json.loads(checked_path(formal['source_review']).read_text())
    assert source_review['field_review'] == formal['field_review']
    assert checked_path(source_review['source_audit']) == checked_path(report['source_audit'])
    print(f"Onboarding-only review passed: 36 official sources, one update / 35 unchanged; sign_start_date 7 -> 8; package version {spec['version']}, API snapshot {report['review_date']}; historical evidence preserved")
    return 0



def main() -> int:
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    onboarding_review = manifest['skills']['huifu-merchant-onboarding'].get('api_review')
    if onboarding_review and json.loads((ROOT / onboarding_review).read_text())['schema_version'] == 5:
        validate_onboarding_maintenance_review(ROOT / onboarding_review)
        previous_payment_review = json.loads((ROOT / onboarding_review).read_text())['previous_api_review']['path']
        if manifest['skills']['huifu-pay-integration'].get('api_review') == previous_payment_review:
            return 0
    latest = ROOT / manifest['skills']['huifu-pay-integration'].get('api_review', str(REPORT.relative_to(ROOT)))
    if latest == REPORT:
        protected = validate_first_review({key: ROOT / path for key, path in CATALOGS.items()})
        print(f'API review validated: 78 documents, 6296 paths; {protected} immutable historical files')
        return 0
    if json.loads(latest.read_text())['schema_version'] == 4:
        return validate_payout_review(latest)
    if json.loads(latest.read_text())['schema_version'] == 3:
        return validate_current_review(latest)
    return validate_second_review(latest)


if __name__ == '__main__':
    raise SystemExit(main())
