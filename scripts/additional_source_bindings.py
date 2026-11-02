"""Bind a versioned additive API bundle to its immutable base and SDK evidence."""
import hashlib
import json
from pathlib import Path, PurePosixPath


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def additional_bindings(root: Path, spec: dict) -> dict[str, str]:
    name = spec.get("additional_source_lock")
    if not name:
        return {}
    def checked(item):
        relative = PurePosixPath(item["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("unsafe additional evidence path")
        path = root / relative
        if not path.is_file() or digest(path) != item["sha256"]:
            raise ValueError("additional evidence digest mismatch: " + str(relative))
        return path
    lock_path = root / name
    lock = json.loads(lock_path.read_text())
    if lock["skill"] != spec["root"] or lock["version"] != spec["version"]:
        raise ValueError("additional API ownership/version mismatch")
    for label, expected in (("base_source_lock", spec["source_lock"]), ("base_refresh_contract", spec["refresh_contract"]), ("sdk_source_lock", spec["sdk_source_lock"])):
        if lock[label]["path"] != expected:
            raise ValueError("additional API base binding mismatch: " + label)
        checked(lock[label])
    catalog = checked(lock["catalog"])
    if not catalog.is_relative_to(root / spec["root"] / "references"):
        raise ValueError("additional catalog crosses Skill boundary")
    evidence = json.loads(checked(lock["sdk_evidence"]).read_text())
    if evidence["probe_status"] != "independent-offline-validation-passed" or evidence["network_calls"] != 0:
        raise ValueError("additional SDK proof is not a verified offline result")
    sources = lock["sources"]
    if len({source["key"] for source in sources}) != len(sources):
        raise ValueError("duplicate additional API")
    for source in sources:
        checked(source)
        if not (root / spec["root"] / "references" / source["reference"]).is_file():
            raise ValueError("missing additional interface reference")
    if lock["totals"] != {"interfaces": len(sources), "field_paths": sum(source["fields"] for source in sources)}:
        raise ValueError("additional API totals disagree")
    return {name: digest(lock_path)}
