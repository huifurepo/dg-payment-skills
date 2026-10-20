"""Shared provenance checks; field parsers remain independent of generators."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(item: dict) -> dict:
    path = ROOT / item['path']
    assert digest(path) == item['sha256'], f"stale evidence binding: {item['path']}"
    document = json.loads(path.read_text()) if path.suffix == '.json' else {}
    if 'refresh_id' in item:
        assert document['refresh_id'] == item['refresh_id']
    return document


def validate_source(lock: dict, domain: str, expected_keys: list[str]) -> Path:
    assert lock['schema_version'] == 1
    date = lock['source_date']
    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', date)
    assert lock['source_snapshot_id'] == date
    assert str(lock['verified_at']).startswith(date)
    directory = ROOT / 'maintainer-contracts/official-sources' / domain / date
    assert [s['key'] for s in lock['sources']] == expected_keys
    assert {p.name for p in directory.iterdir() if p.is_file()} == {s['filename'] for s in lock['sources']}
    for item in lock['sources']:
        path = directory / item['filename']
        assert digest(path) == item['sha256'], path
        if 'endpoint' in item and item['filename'].endswith('.md'):
            assert 'https://api.huifu.com' + item['endpoint'].removeprefix('POST ') in path.read_text(encoding='utf-8-sig'), item['key']
    previous = binding(lock['previous_source_lock'])
    old_directory = ROOT / 'maintainer-contracts/official-sources' / domain / previous['source_snapshot_id']
    for item in previous['sources']:
        assert digest(old_directory / item['filename']) == item['sha256']
    old = {s['key']: s for s in previous['sources']}
    current = {s['key']: s for s in lock['sources']}
    meta = lock.get('api_refresh', lock.get('current_extension'))
    changed = {key for key in old.keys() & current.keys() if old[key]['sha256'] != current[key]['sha256']}
    assert changed == set(meta['changed_source_keys']), f'{domain}: changed source set differs'
    assert set(current) - set(old) == set(meta.get('added_source_keys', []))
    assert not (set(old) - set(current)), f'{domain}: unexpected source deletion'
    return directory


def validate_release(skill: str) -> tuple[dict, dict]:
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    spec = manifest['skills'][skill]
    release = json.loads((ROOT / spec['refresh_contract']).read_text())
    assert release['schema_version'] == 1
    assert release['version_state'][skill] == spec['version']
    binding(release['previous_refresh'])
    review = binding(release['source_review'])
    assert release['source_review_id'] == review['refresh_id']
    for key in ('source_locks', 'catalogs', 'field_delta'):
        assert release[key] == review[key], f'{skill}: release changed reviewed {key}'
    for item in (*release['source_locks'].values(), *release['catalogs'].values()):
        binding(item)
    sdk = json.loads((ROOT / spec['sdk_source_lock']).read_text())
    assert any(item['path'] == spec['sdk_source_lock'] for item in release['source_locks'].values())
    assert any(item['path'] == spec['source_lock'] for item in release['source_locks'].values())
    assert release['sdk_versions'] == {name: item['version'] for name, item in sdk['components'].items()}
    assert release['sdk_reviewed_at'] == sdk['verified_at']
    assert release['python_sdk'] == {'target_version': sdk['components']['python']['version'], 'verified_source_version': sdk['components']['python']['version'], 'target_source_verified': True}
    return release, review


def validate_onboarding_combined() -> dict:
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    spec = manifest['skills']['huifu-merchant-onboarding']
    combined = json.loads((ROOT / spec['source_lock']).read_text())
    assert combined['skill'] == 'huifu-merchant-onboarding'
    assert combined['version'] == spec['version']
    binding(combined['previous_combined_lock'])
    count = total = 0
    for item in combined['source_locks'].values():
        lock = binding(item)
        assert item['field_paths'] == lock['totals']['fields']
        count += len(lock['sources'])
        total += item['field_paths']
    assert combined['totals'] == {'interfaces': count, 'field_paths': total}
    for item in combined['catalogs'].values():
        binding(item)
    validate_release('huifu-merchant-onboarding')
    return combined
