"""Check independent package provenance and immutable historical newline locks."""

import copy
import hashlib
import json
import unittest
from pathlib import Path

import package_skill
import validate_skill_package
import validate_skill_split


ROOT = Path(__file__).resolve().parent.parent


class IndependentReleaseTests(unittest.TestCase):
    def test_packages_keep_independent_evidence(self):
        manifest = json.loads((ROOT / "skills-manifest.json").read_text(encoding="utf-8"))
        for name, spec in manifest["skills"].items():
            with self.subTest(skill=name):
                path = ROOT / spec["refresh_contract"]
                refresh = json.loads(path.read_text(encoding="utf-8"))
                bindings = package_skill.source_bindings(manifest, spec, refresh)
                expected = {spec["source_lock"]}
                if spec["domain"] == "onboarding":
                    expected.add(spec["sdk_source_lock"])
                self.assertEqual(set(bindings), expected)
                provenance = {
                    "refresh_contract": spec["refresh_contract"],
                    "refresh_id": refresh["refresh_id"],
                    "refresh_contract_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "source_locks": bindings,
                }
                validate_skill_package.validate_refresh_source_bindings(provenance, spec)
                bad = copy.deepcopy(provenance)
                bad["source_locks"][spec["source_lock"]] = "0" * 64
                with self.assertRaises(ValueError):
                    validate_skill_package.validate_refresh_source_bindings(bad, spec)
                if spec["domain"] == "onboarding":
                    for mutation in ("missing", "wrong"):
                        bad = copy.deepcopy(provenance)
                        if mutation == "missing":
                            del bad["source_locks"][spec["sdk_source_lock"]]
                        else:
                            bad["source_locks"][spec["sdk_source_lock"]] = "0" * 64
                        with self.assertRaises(ValueError):
                            validate_skill_package.validate_refresh_source_bindings(bad, spec)

    def test_newline_compatibility_does_not_accept_content_changes(self):
        original = b"first\r\nsecond\r\n"
        digest = hashlib.sha256(original).hexdigest()
        check = validate_skill_split.reviewed_snapshot_matches
        self.assertTrue(check("example.md", b"first\nsecond\n", digest))
        self.assertFalse(check("example.md", b"first\nchanged\n", digest))


if __name__ == "__main__":
    unittest.main()
