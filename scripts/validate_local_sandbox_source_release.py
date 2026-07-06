#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
from pathlib import Path
from urllib.parse import urlsplit


APP_NAME = "hf-payment-local-sandbox"
SOURCE_ARCHIVE_SCHEMA_VERSION = "1.0"
FORBIDDEN_PARTS = {".git", ".claude", ".tmp", ".worktrees", ".codex-tasks", "__pycache__", "node_modules", "target", "dist", "build", "release-evidence", "sample-packs", ".venv", "venv"}
FORBIDDEN_NAMES = {".DS_Store", "Thumbs.db", APP_NAME}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".exe", ".dll", ".so", ".dylib", ".zip", ".tar", ".gz", ".tgz", ".7z"}
FORBIDDEN_NAME_SUFFIXES = ("_test.go",)
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"SYNTHETIC_" + rb"PRIVATE_" + rb"KEY_PKCS8_B64"),
    re.compile(rb"PRIVATE_" + rb"KEY_PKCS8"),
    re.compile(rb"[?&](" + b"|".join([rb"secret", rb"token", rb"key", rb"password"]) + rb")="),
)
PHONE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
ID_CARD_PATTERN = re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)")
URL_PATTERN = re.compile(r"https?://([^/\s\"']+)", re.I)
ALLOWED_SAMPLE_HOSTS = {"localhost", "127.0.0.1", "::1", "example.invalid", "sandbox.local"}
SENSITIVE_FIELD_NAMES = {"access_token", "api_key", "apikey", "secret", "password", "passwd", "private_key", "token"}
SYNTHETIC_LONG_NUMBER_PATTERNS = (
    re.compile(r"12340001\d{8}$"),
    re.compile(r"0{13,19}$"),
    re.compile(r"9{13,19}$"),
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local-sandbox source release archive.")
    parser.add_argument("--archive", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    archive = Path(args.archive).resolve()
    manifest = Path(args.manifest).resolve()
    require(archive.is_file(), f"source archive is missing: {archive}")
    require(manifest.is_file(), f"source manifest is missing: {manifest}")

    outer = read_json(manifest)
    require(outer.get("name") == APP_NAME, "source manifest name mismatch")
    require(outer.get("version") == args.version, "source manifest version mismatch")
    require(outer.get("source_archive_schema_version") == SOURCE_ARCHIVE_SCHEMA_VERSION, "source manifest schema mismatch")
    require_forbidden_policy(outer.get("forbidden_path_policy"))
    meta = outer.get("source_archive")
    require(isinstance(meta, dict), "source manifest missing source_archive metadata")
    require(meta.get("name") == archive.name, "source archive name mismatch")
    require(meta.get("sha256") == sha256_file(archive), "source archive sha256 mismatch")
    require(meta.get("size_bytes") == archive.stat().st_size, "source archive size mismatch")

    members = read_archive(archive)
    require(members, "source archive is empty")
    prefixes = {name.split("/", 1)[0] for name in members}
    require(len(prefixes) == 1, "source archive must contain one root directory")
    prefix = next(iter(prefixes)) + "/"
    inner_manifest_name = prefix + "SOURCE_RELEASE_MANIFEST.json"
    require(inner_manifest_name in members, "SOURCE_RELEASE_MANIFEST.json missing")
    inner = json.loads(members[inner_manifest_name].decode("utf-8"))
    require(inner.get("name") == APP_NAME, "inner source manifest name mismatch")
    require(inner.get("version") == args.version, "inner source manifest version mismatch")
    require(inner.get("source_archive_schema_version") == SOURCE_ARCHIVE_SCHEMA_VERSION, "inner source manifest schema mismatch")
    listed = inner.get("files")
    require(isinstance(listed, list) and listed, "inner source manifest files missing")
    require(inner.get("file_count") == len(listed), "inner source manifest file_count mismatch")

    expected_names = {inner_manifest_name}
    forbidden_count = 0
    for entry in listed:
        require(isinstance(entry, dict), "inner source manifest file entry invalid")
        rel = expect_string(entry, "path")
        member_name = prefix + rel
        expected_names.add(member_name)
        require(member_name in members, f"listed source file missing from archive: {rel}")
        content = members[member_name]
        require(entry.get("sha256") == sha256_bytes(content), f"source file sha256 mismatch: {rel}")
        require(entry.get("size_bytes") == len(content), f"source file size mismatch: {rel}")
        if is_forbidden(Path(rel)):
            forbidden_count += 1
        scan_bytes_for_secrets(rel, content)
        if is_sample_derived_fixture(Path(rel), content):
            scan_sample_fixture_for_sensitive_values(rel, content)

    extra = set(members) - expected_names
    require(not extra, f"source archive contains unlisted files: {sorted(extra)[:5]}")
    require(outer.get("file_count") == len(listed), "source manifest file_count mismatch")
    require(forbidden_count == 0, f"source archive contains {forbidden_count} forbidden paths")
    scan_bytes_for_secrets(manifest.name, manifest.read_bytes())
    print(json.dumps({"ok": True, "archive": str(archive), "manifest": str(manifest), "files": len(listed), "forbidden_path_count": forbidden_count, "secret_scan_status": "passed", "manifest_status": "passed"}, ensure_ascii=False))
    return 0


def read_archive(path: Path) -> dict[str, bytes]:
    require(path.name.endswith(".tar.gz"), "source archive must be .tar.gz")
    out: dict[str, bytes] = {}
    with tarfile.open(path, "r:gz") as tf:
        for member in tf.getmembers():
            require(not member.name.startswith("/") and ".." not in Path(member.name).parts, f"unsafe archive member: {member.name}")
            require(member.isfile(), f"source archive member is not a file: {member.name}")
            require(not is_forbidden(Path(member.name)), f"source archive contains forbidden path: {member.name}")
            fh = tf.extractfile(member)
            require(fh is not None, f"cannot read source archive member: {member.name}")
            out[member.name] = fh.read()
    return out


def is_forbidden(path: Path) -> bool:
    parts = set(path.parts)
    if parts & FORBIDDEN_PARTS:
        return True
    if path.name in FORBIDDEN_NAMES:
        return True
    if path.name.endswith(FORBIDDEN_NAME_SUFFIXES):
        return True
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        return True
    return False


def require_forbidden_policy(policy: object) -> None:
    require(isinstance(policy, dict), "source manifest forbidden_path_policy missing")
    expected = {
        "forbidden_parts": sorted(FORBIDDEN_PARTS),
        "forbidden_names": sorted(FORBIDDEN_NAMES),
        "forbidden_name_suffixes": sorted(FORBIDDEN_NAME_SUFFIXES),
        "forbidden_suffixes": sorted(FORBIDDEN_SUFFIXES),
    }
    for key, value in expected.items():
        require(policy.get(key) == value, f"source manifest forbidden_path_policy.{key} mismatch")


def read_json(path: Path) -> dict[str, object]:
    return json.loads(read_text_auto(path))


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8")


def scan_bytes_for_secrets(label: str, content: bytes) -> None:
    for pattern in SECRET_PATTERNS:
        require(pattern.search(content) is None, f"{label} contains blocked secret/query pattern")


def scan_sample_fixture_for_sensitive_values(label: str, content: bytes) -> None:
    text = content.decode("utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[ERROR] {label} invalid sample fixture JSON: {exc}") from exc
    scan_json_for_sensitive_fields(label, data)
    require(PHONE_PATTERN.search(text) is None, f"{label} contains unmasked mainland China mobile number")
    require(ID_CARD_PATTERN.search(text) is None, f"{label} contains unmasked PRC ID card number")
    for url in re.findall(r"https?://[^\s\"']+", text, re.I):
        parsed = urlsplit(url)
        normalized = (parsed.hostname or "").lower()
        require(
            normalized in ALLOWED_SAMPLE_HOSTS or normalized.endswith(".example.invalid"),
            f"{label} contains non-placeholder URL host {parsed.netloc}",
        )
    for number in re.findall(r"(?<!\d)\d{13,19}(?!\d)", text):
        if is_placeholder_number(number):
            continue
        if luhn(number):
            raise SystemExit(f"[ERROR] {label} contains possible unmasked bank card number")
        raise SystemExit(f"[ERROR] {label} contains long unmasked numeric identifier")


def scan_json_for_sensitive_fields(label: str, value: object, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            normalized = re.sub(r"[^a-z0-9]", "_", key_text.lower()).strip("_")
            if normalized in SENSITIVE_FIELD_NAMES and sensitive_field_value(item):
                raise SystemExit(f"[ERROR] {label} contains sensitive field {path}.{key_text}")
            scan_json_for_sensitive_fields(label, item, f"{path}.{key_text}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_json_for_sensitive_fields(label, item, f"{path}[{index}]")


def sensitive_field_value(value: object) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped or stripped.upper() in {"REDACTED", "PLACEHOLDER", "SIGNATURE-PLACEHOLDER"}:
            return False
        if stripped.startswith(("sha256:", "SIGNATURE-", "{{")):
            return False
        return len(stripped) >= 8
    return True


def is_sample_derived_fixture(path: Path, content: bytes) -> bool:
    if path.suffix != ".json" or "fixtures" not in path.parts:
        return False
    try:
        data = json.loads(content.decode("utf-8"))
    except json.JSONDecodeError:
        return path.name.startswith("sample-")
    return data.get("kind") == "sample" or bool(data.get("source_sample_id"))


def is_placeholder_number(value: str) -> bool:
    return any(pattern.fullmatch(value) for pattern in SYNTHETIC_LONG_NUMBER_PATTERNS)


def luhn(value: str) -> bool:
    total = 0
    for index, char in enumerate(value[::-1]):
        digit = ord(char) - 48
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def expect_string(data: dict[str, object], key: str) -> str:
    value = data.get(key)
    require(isinstance(value, str) and value, f"{key} missing")
    return value


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"[ERROR] {message}")


if __name__ == "__main__":
    raise SystemExit(main())
