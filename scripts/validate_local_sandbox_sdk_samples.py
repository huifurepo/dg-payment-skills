#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

OFFICIAL_PROFILE = "official-demo"
ACTIVE_SYS_ID = "6666000108840829"
ACTIVE_PRODUCT_ID = "YYZY"
SUCCESS_RESP_CODES = {"00000000", "00000100"}


def main() -> int:
    global ACTIVE_PRODUCT_ID, ACTIVE_SYS_ID
    parser = argparse.ArgumentParser(description="Run Java/PHP/Python samples against local-sandbox.")
    parser.add_argument("--version", default="1.0.1")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sandbox_dir = repo_root / "local-sandbox"
    temp_ctx = tempfile.TemporaryDirectory(prefix="hf-sandbox-sdk-samples-")
    tmp = Path(temp_ctx.name)
    server = None
    try:
        ready, server = start_sandbox(sandbox_dir, tmp)
        credentials = export_credentials(sandbox_dir, tmp / "data")
        ACTIVE_SYS_ID = credentials.get("sys_id") or ACTIVE_SYS_ID
        ACTIVE_PRODUCT_ID = credentials.get("product_id") or ACTIVE_PRODUCT_ID
        private_key = credentials["merchant_private_key"]
        public_key = credentials["merchant_public_key"]
        if credentials.get("huifu_id") != "6666000100000001":
            raise SystemExit("[ERROR] exported huifu_id sample value is missing")
        private_pem = wrap_pem("PRIVATE KEY", private_key)
        public_pem = wrap_pem("PUBLIC KEY", public_key)
        private_path = tmp / "merchant-private.pem"
        public_path = tmp / "gateway-public.pem"
        private_path.write_text(private_pem, encoding="utf-8")
        public_path.write_text(public_pem, encoding="utf-8")

        results = []
        results.append(run_python_sample(ready["gateway_url"], ready["control_url"], ready["csrf_token"], private_key, public_key))
        results.append(run_java_sample(tmp, ready["gateway_url"], ready["control_url"], ready["csrf_token"], private_path, public_path))
        results.append(run_php_sample(tmp, ready["gateway_url"], ready["control_url"], ready["csrf_token"], private_path, public_path))
        shutdown_sandbox(ready)
        server.wait(timeout=20)
        server = None

        ok = all(item["ok"] for item in results) and ready.get("version") == args.version
        print(json.dumps({"ok": ok, "version": ready.get("version"), "samples": results, "report_dir": ready.get("report_dir")}, ensure_ascii=False))
        return 0 if ok else 1
    finally:
        if server is not None and server.poll() is None:
            try:
                server.terminate()
                server.wait(timeout=5)
            except Exception:
                server.kill()
        if args.keep_temp:
            print(json.dumps({"temp_dir": str(tmp)}, ensure_ascii=False), file=sys.stderr)
        else:
            temp_ctx.cleanup()


def start_sandbox(sandbox_dir: Path, tmp: Path) -> tuple[dict[str, object], subprocess.Popen[str]]:
    cmd = [
        "go",
        "run",
        ".",
        "serve",
        "--control-port",
        "0",
        "--gateway-port",
        "0",
        "--print-json",
        "--credential-profile",
        OFFICIAL_PROFILE,
        "--data-dir",
        str(tmp / "data"),
        "--report-dir",
        str(tmp / "report"),
    ]
    proc = subprocess.Popen(cmd, cwd=sandbox_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    assert proc.stdout is not None
    deadline = time.time() + 60
    while time.time() < deadline:
        line = proc.stdout.readline()
        if line:
            ready = json.loads(line)
            if ready.get("event") == "ready":
                return ready, proc
        if proc.poll() is not None:
            stderr = proc.stderr.read() if proc.stderr else ""
            raise SystemExit(f"[ERROR] sandbox exited before ready: {stderr}")
    raise SystemExit("[ERROR] sandbox did not become ready")


def export_credentials(sandbox_dir: Path, data_dir: Path) -> dict[str, str]:
    raw = subprocess.check_output(
        [
            "go",
            "run",
            ".",
            "credentials",
            "export",
            "--credential-profile",
            OFFICIAL_PROFILE,
            "--data-dir",
            str(data_dir),
            "--format",
            "json",
            "--allow-private-export",
        ],
        cwd=sandbox_dir,
        text=True,
        encoding="utf-8",
    )
    return json.loads(raw)


def shutdown_sandbox(ready: dict[str, object]) -> None:
    req = urllib.request.Request(
        str(ready["control_url"]).rstrip("/") + "/__admin/shutdown",
        data=b"{}",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(ready["admin_token"]),
            "X-Huifu-Sandbox-CSRF": str(ready["csrf_token"]),
        },
    )
    urllib.request.urlopen(req, timeout=10).read()


def run_python_sample(gateway_url: str, control_url: str, csrf_token: str, private_pem: str, public_pem: str) -> dict[str, object]:
    private_values = parse_rsa_private_pem(private_pem)
    public_values = parse_rsa_public_pem(public_pem)
    checks = []

    agg = create_paid_aggregation(gateway_url, private_values, public_values, "PY-AGG", "0.01")
    checks.append(agg["trans_stat"] == "S")

    refund_payment = create_paid_aggregation(gateway_url, private_values, public_values, "PY-RF-ORIG", "0.10")
    refund_data = {
        "req_date": "20260624",
        "req_seq_id": "SDK-PY-RF-001",
        "huifu_id": refund_payment["huifu_id"],
        "ord_amt": "0.04",
        "org_req_date": refund_payment["req_date"],
        "org_req_seq_id": refund_payment["req_seq_id"],
    }
    post_gateway(gateway_url, "/v4/trade/payment/scanpay/refund", refund_data, private_values, public_values)
    refund_query = {"huifu_id": refund_payment["huifu_id"], "org_req_date": "20260624", "org_req_seq_id": "SDK-PY-RF-001"}
    post_gateway(gateway_url, "/v4/trade/payment/scanpay/refundquery", refund_query, private_values, public_values)
    refund_second = post_gateway(gateway_url, "/v4/trade/payment/scanpay/refundquery", refund_query, private_values, public_values)
    checks.append(refund_second["data"].get("trans_stat") == "S")

    close_create = sample_create_data("PY", "CL-ORIG", "0.03")
    post_gateway(gateway_url, "/v4/trade/payment/create", close_create, private_values, public_values)
    close_data = {
        "req_date": "20260624",
        "req_seq_id": "SDK-PY-CL-001",
        "huifu_id": close_create["huifu_id"],
        "org_req_date": close_create["req_date"],
        "org_req_seq_id": close_create["req_seq_id"],
    }
    post_gateway(gateway_url, "/v2/trade/payment/scanpay/close", close_data, private_values, public_values)
    close_query = {"huifu_id": close_create["huifu_id"], "org_req_date": close_create["req_date"], "org_req_seq_id": close_create["req_seq_id"]}
    post_gateway(gateway_url, "/v2/trade/payment/scanpay/closequery", close_query, private_values, public_values)
    close_second = post_gateway(gateway_url, "/v2/trade/payment/scanpay/closequery", close_query, private_values, public_values)
    checks.append(close_second["data"].get("trans_stat") == "S")

    hosting = sample_hosting_data("PY-HOST")
    preorder = post_gateway(gateway_url, "/v2/trade/hosting/payment/preorder", hosting, private_values, public_values)
    pre_order_id = preorder["data"]["pre_order_id"]
    get_control(control_url, "/__merchant/hosting/callback?pre_order_id=" + urllib.parse.quote(str(pre_order_id)))
    post_control(control_url, "/__merchant/hosting/confirm", {"pre_order_id": pre_order_id}, csrf_token)
    hosting_query = post_gateway(
        gateway_url,
        "/v2/trade/hosting/payment/queryorderinfo",
        {
            "req_date": hosting["req_date"],
            "req_seq_id": "SDK-PY-HOST-QRY-001",
            "huifu_id": hosting["huifu_id"],
            "org_req_date": hosting["req_date"],
            "org_req_seq_id": hosting["req_seq_id"],
        },
        private_values,
        public_values,
    )
    checks.append(hosting_query["data"].get("trans_stat") == "S")

    recon = {"req_date": "20260624", "req_seq_id": "SDK-PY-RECON", "huifu_id": "6666000100000001", "file_date": "20260623"}
    post_gateway(gateway_url, "/v2/trade/check/filequery", recon, private_values, public_values)
    recon_second = post_gateway(gateway_url, "/v2/trade/check/filequery", recon, private_values, public_values)
    checks.append("file_details" in recon_second["data"])

    return {
        "language": "python",
        "ok": all(checks),
        "chains": ["aggregation", "hosting", "refund", "close", "reconciliation"],
        "req_seq_id": agg["req_seq_id"],
    }


def create_paid_aggregation(gateway_url: str, private_values: dict[str, int], public_values: dict[str, int], suffix: str, amount: str) -> dict[str, str]:
    data = sample_create_data(suffix, "001", amount)
    create = post_gateway(gateway_url, "/v4/trade/payment/create", data, private_values, public_values)
    query_data = {"huifu_id": data["huifu_id"], "hf_seq_id": create["data"]["hf_seq_id"]}
    post_gateway(gateway_url, "/v4/trade/payment/scanpay/query", query_data, private_values, public_values)
    query = post_gateway(gateway_url, "/v4/trade/payment/scanpay/query", query_data, private_values, public_values)
    return {
        "huifu_id": data["huifu_id"],
        "req_date": data["req_date"],
        "req_seq_id": data["req_seq_id"],
        "hf_seq_id": create["data"]["hf_seq_id"],
        "trans_stat": query["data"].get("trans_stat"),
    }


def post_gateway(gateway_url: str, path: str, data: dict[str, object], private_values: dict[str, int], public_values: dict[str, int]) -> dict[str, object]:
    canonical = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    sign = rsa_sign(canonical.encode("utf-8"), private_values)
    envelope = {"sys_id": ACTIVE_SYS_ID, "product_id": ACTIVE_PRODUCT_ID, "sign": sign, "data": data}
    body = json.dumps(envelope, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        gateway_url.rstrip("/") + path,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json;charset=UTF-8",
            "jpt-x-skill-source": "hfps/1.3.1;sandbox/1.0.1",
            "jpt-x-skill-huifu_id": str(data["huifu_id"]),
        },
    )
    raw = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
    payload = json.loads(raw)
    response_canonical = json.dumps(payload["data"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if not rsa_verify(response_canonical.encode("utf-8"), payload["sign"], public_values):
        raise SystemExit("[ERROR] python sample response signature verification failed")
    if payload["data"].get("resp_code") not in SUCCESS_RESP_CODES:
        raise SystemExit(f"[ERROR] python sample gateway error: {payload}")
    return payload


def post_control(control_url: str, path: str, data: dict[str, object], csrf_token: str) -> dict[str, object]:
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        control_url.rstrip("/") + path,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "X-Huifu-Sandbox-CSRF": csrf_token},
    )
    raw = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
    return json.loads(raw)


def get_control(control_url: str, path: str) -> dict[str, object]:
    raw = urllib.request.urlopen(control_url.rstrip("/") + path, timeout=10).read().decode("utf-8")
    return json.loads(raw)


def run_java_sample(tmp: Path, gateway_url: str, control_url: str, csrf_token: str, private_path: Path, public_path: Path) -> dict[str, object]:
    javac = require_executable("javac")
    java = require_executable("java")
    source = tmp / "SandboxJavaSample.java"
    source.write_text(JAVA_SAMPLE, encoding="utf-8")
    subprocess.check_call([javac, "-encoding", "UTF-8", str(source)], cwd=tmp)
    raw = subprocess.check_output([java, "-cp", str(tmp), "SandboxJavaSample", gateway_url, str(private_path), str(public_path), control_url, csrf_token, ACTIVE_SYS_ID, ACTIVE_PRODUCT_ID], text=True, encoding="utf-8")
    return json.loads(raw)


def run_php_sample(tmp: Path, gateway_url: str, control_url: str, csrf_token: str, private_path: Path, public_path: Path) -> dict[str, object]:
    php = require_executable("php")
    source = tmp / "sandbox_php_sample.php"
    source.write_text(PHP_SAMPLE, encoding="utf-8")
    raw = subprocess.check_output([php, str(source), gateway_url, str(private_path), str(public_path), control_url, csrf_token, ACTIVE_SYS_ID, ACTIVE_PRODUCT_ID], text=True, encoding="utf-8")
    return json.loads(raw)


def require_executable(name: str) -> str:
    resolved = shutil.which(name)
    if not resolved:
        raise SystemExit(f"[ERROR] missing executable: {name}")
    return resolved


def sample_create_data(prefix: str, suffix: str = "001", amount: str = "0.01") -> dict[str, str]:
    return {
        "req_date": "20260624",
        "req_seq_id": f"SDK-{prefix}-{suffix}",
        "huifu_id": "6666000100000001",
        "trade_type": "A_NATIVE",
        "trans_amt": amount,
        "goods_desc": f"{prefix} sdk sample",
    }


def sample_hosting_data(prefix: str) -> dict[str, str]:
    return {
        "req_date": "20260624",
        "req_seq_id": f"SDK-{prefix}-001",
        "huifu_id": "6666000100000001",
        "pre_order_type": "1",
        "trans_type": "A_NATIVE",
        "trans_amt": "0.02",
        "goods_desc": f"{prefix} hosting sdk sample",
        "hosting_data": json.dumps({"project_title": "SDK Sample", "project_id": "P123", "request_type": "P"}, separators=(",", ":")),
    }


def wrap_pem(label: str, value: str) -> str:
    compact = re.sub(r"\s+", "", value)
    lines = [compact[i : i + 64] for i in range(0, len(compact), 64)]
    return f"-----BEGIN {label}-----\n" + "\n".join(lines) + f"\n-----END {label}-----\n"


def parse_rsa_private_pem(pem: str) -> dict[str, int]:
    der = key_to_der(pem)
    ints = parse_der_integers(der)
    if len(ints) < 4:
        inner = extract_pkcs8_private_key(der)
        ints = parse_der_integers(inner)
    if len(ints) < 4:
        raise SystemExit("[ERROR] invalid RSA private key")
    return {"n": ints[1], "e": ints[2], "d": ints[3]}


def parse_rsa_public_pem(pem: str) -> dict[str, int]:
    der = key_to_der(pem)
    ints = parse_der_integers(der)
    if len(ints) < 2:
        inner = extract_x509_public_key(der)
        ints = parse_der_integers(inner)
    if len(ints) < 2:
        raise SystemExit("[ERROR] invalid RSA public key")
    return {"n": ints[0], "e": ints[1]}


def key_to_der(value: str) -> bytes:
    lines = [line.strip() for line in value.splitlines() if line and not line.startswith("-----")]
    return base64.b64decode("".join(lines))


def extract_pkcs8_private_key(data: bytes) -> bytes:
    tag, outer, _ = read_tlv(data, 0)
    if tag != 0x30:
        raise SystemExit("[ERROR] PKCS8 sequence expected")
    pos = 0
    seen_version = False
    while pos < len(outer):
        tag, value, pos = read_tlv(outer, pos)
        if tag == 0x02:
            seen_version = True
            continue
        if seen_version and tag == 0x04:
            return value
    raise SystemExit("[ERROR] PKCS8 private key payload missing")


def extract_x509_public_key(data: bytes) -> bytes:
    tag, outer, _ = read_tlv(data, 0)
    if tag != 0x30:
        raise SystemExit("[ERROR] X509 public key sequence expected")
    pos = 0
    while pos < len(outer):
        tag, value, pos = read_tlv(outer, pos)
        if tag == 0x03:
            if not value or value[0] != 0:
                raise SystemExit("[ERROR] unsupported X509 public key bit string")
            return value[1:]
    raise SystemExit("[ERROR] X509 public key payload missing")


def parse_der_integers(data: bytes) -> list[int]:
    pos = 0
    if data[pos] != 0x30:
        raise SystemExit("[ERROR] DER sequence expected")
    pos += 1
    _, pos = der_length(data, pos)
    values = []
    while pos < len(data):
        if data[pos] != 0x02:
            break
        pos += 1
        length, pos = der_length(data, pos)
        raw = data[pos : pos + length]
        pos += length
        values.append(int.from_bytes(raw, "big", signed=False))
    return values


def read_tlv(data: bytes, pos: int) -> tuple[int, bytes, int]:
    if pos >= len(data):
        raise SystemExit("[ERROR] DER value truncated")
    tag = data[pos]
    pos += 1
    length, pos = der_length(data, pos)
    end = pos + length
    if end > len(data):
        raise SystemExit("[ERROR] DER length exceeds input")
    return tag, data[pos:end], end


def der_length(data: bytes, pos: int) -> tuple[int, int]:
    first = data[pos]
    pos += 1
    if first < 0x80:
        return first, pos
    count = first & 0x7F
    length = int.from_bytes(data[pos : pos + count], "big")
    return length, pos + count


def rsa_sign(message: bytes, values: dict[str, int]) -> str:
    digest = hashlib.sha256(message).digest()
    digest_info = bytes.fromhex("3031300d060960864801650304020105000420") + digest
    k = (values["n"].bit_length() + 7) // 8
    em = b"\x00\x01" + (b"\xff" * (k - len(digest_info) - 3)) + b"\x00" + digest_info
    sig = pow(int.from_bytes(em, "big"), values["d"], values["n"]).to_bytes(k, "big")
    return base64.b64encode(sig).decode("ascii")


def rsa_verify(message: bytes, signature: str, values: dict[str, int]) -> bool:
    digest = hashlib.sha256(message).digest()
    digest_info = bytes.fromhex("3031300d060960864801650304020105000420") + digest
    k = (values["n"].bit_length() + 7) // 8
    sig = int.from_bytes(base64.b64decode(signature), "big")
    em = pow(sig, values["e"], values["n"]).to_bytes(k, "big")
    return em.endswith(b"\x00" + digest_info)


JAVA_SAMPLE = r'''
import java.io.*;
import java.math.BigInteger;
import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.Signature;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.*;
import java.util.Base64;
import java.util.regex.*;

public class SandboxJavaSample {
  static String SYS_ID;
  static String PRODUCT_ID;
  public static void main(String[] args) throws Exception {
    String gateway = args[0];
    PrivateKey privateKey = privateKey(Files.readString(Path.of(args[1])));
    String control = args[3];
    String csrf = args[4];
    SYS_ID = args[5];
    PRODUCT_ID = args[6];
    List<Boolean> checks = new ArrayList<>();

    Map<String,String> agg = createPaid(gateway, privateKey, "JAVA-AGG", "0.01");
    checks.add("S".equals(agg.get("trans_stat")));

    Map<String,String> refundPayment = createPaid(gateway, privateKey, "JAVA-RF-ORIG", "0.10");
    Map<String,String> refund = new TreeMap<>();
    refund.put("huifu_id", refundPayment.get("huifu_id"));
    refund.put("ord_amt", "0.04");
    refund.put("org_req_date", refundPayment.get("req_date"));
    refund.put("org_req_seq_id", refundPayment.get("req_seq_id"));
    refund.put("req_date", "20260624");
    refund.put("req_seq_id", "SDK-JAVA-RF-001");
    post(gateway, "/v4/trade/payment/scanpay/refund", refund, privateKey);
    Map<String,String> refundQuery = new TreeMap<>();
    refundQuery.put("huifu_id", refundPayment.get("huifu_id"));
    refundQuery.put("org_req_date", "20260624");
    refundQuery.put("org_req_seq_id", "SDK-JAVA-RF-001");
    post(gateway, "/v4/trade/payment/scanpay/refundquery", refundQuery, privateKey);
    String refundSecond = post(gateway, "/v4/trade/payment/scanpay/refundquery", refundQuery, privateKey);
    checks.add(refundSecond.contains("\"trans_stat\":\"S\""));

    Map<String,String> closeOriginal = sample("JAVA-CL-ORIG", "001", "0.03");
    post(gateway, "/v4/trade/payment/create", closeOriginal, privateKey);
    Map<String,String> close = new TreeMap<>();
    close.put("huifu_id", closeOriginal.get("huifu_id"));
    close.put("org_req_date", closeOriginal.get("req_date"));
    close.put("org_req_seq_id", closeOriginal.get("req_seq_id"));
    close.put("req_date", "20260624");
    close.put("req_seq_id", "SDK-JAVA-CL-001");
    post(gateway, "/v2/trade/payment/scanpay/close", close, privateKey);
    Map<String,String> closeQuery = new TreeMap<>();
    closeQuery.put("huifu_id", closeOriginal.get("huifu_id"));
    closeQuery.put("org_req_date", closeOriginal.get("req_date"));
    closeQuery.put("org_req_seq_id", closeOriginal.get("req_seq_id"));
    post(gateway, "/v2/trade/payment/scanpay/closequery", closeQuery, privateKey);
    String closeSecond = post(gateway, "/v2/trade/payment/scanpay/closequery", closeQuery, privateKey);
    checks.add(closeSecond.contains("\"trans_stat\":\"S\""));

    Map<String,String> hosting = hostingSample("JAVA-HOST");
    String preorder = post(gateway, "/v2/trade/hosting/payment/preorder", hosting, privateKey);
    String preOrderId = match(preorder, "\\\"pre_order_id\\\"\\s*:\\s*\\\"([^\\\"]+)\\\"");
    controlGet(control, "/__merchant/hosting/callback?pre_order_id=" + preOrderId);
    controlPost(control, "/__merchant/hosting/confirm", "{\"pre_order_id\":\"" + esc(preOrderId) + "\"}", csrf);
    Map<String,String> hostingQuery = new TreeMap<>();
    hostingQuery.put("req_date", hosting.get("req_date"));
    hostingQuery.put("req_seq_id", "SDK-JAVA-HOST-QRY-001");
    hostingQuery.put("huifu_id", hosting.get("huifu_id"));
    hostingQuery.put("org_req_date", hosting.get("req_date"));
    hostingQuery.put("org_req_seq_id", hosting.get("req_seq_id"));
    String hostingResp = post(gateway, "/v2/trade/hosting/payment/queryorderinfo", hostingQuery, privateKey);
    checks.add(hostingResp.contains("\"trans_stat\":\"S\""));

    Map<String,String> recon = new TreeMap<>();
    recon.put("file_date", "20260623");
    recon.put("huifu_id", "6666000100000001");
    recon.put("req_date", "20260624");
    recon.put("req_seq_id", "SDK-JAVA-RECON");
    post(gateway, "/v2/trade/check/filequery", recon, privateKey);
    String reconSecond = post(gateway, "/v2/trade/check/filequery", recon, privateKey);
    checks.add(reconSecond.contains("\"file_details\""));

    boolean ok = true;
    for (Boolean check : checks) ok = ok && check.booleanValue();
    System.out.println("{\"language\":\"java\",\"ok\":" + ok + ",\"chains\":[\"aggregation\",\"hosting\",\"refund\",\"close\",\"reconciliation\"],\"req_seq_id\":\"" + agg.get("req_seq_id") + "\"}");
  }
  static Map<String,String> createPaid(String gateway, PrivateKey key, String prefix, String amount) throws Exception {
    Map<String,String> data = sample(prefix, "001", amount);
    String create = post(gateway, "/v4/trade/payment/create", data, key);
    String hfSeqId = match(create, "\\\"hf_seq_id\\\"\\s*:\\s*\\\"([^\\\"]+)\\\"");
    Map<String,String> query = new TreeMap<>();
    query.put("hf_seq_id", hfSeqId);
    query.put("huifu_id", data.get("huifu_id"));
    post(gateway, "/v4/trade/payment/scanpay/query", query, key);
    String second = post(gateway, "/v4/trade/payment/scanpay/query", query, key);
    data.put("hf_seq_id", hfSeqId);
    data.put("trans_stat", second.contains("\"trans_stat\":\"S\"") ? "S" : "P");
    return data;
  }
  static Map<String,String> sample(String prefix, String suffix, String amount) {
    Map<String,String> data = new TreeMap<>();
    data.put("goods_desc", prefix + " sdk sample");
    data.put("huifu_id", "6666000100000001");
    data.put("req_date", "20260624");
    data.put("req_seq_id", "SDK-" + prefix + "-" + suffix);
    data.put("trade_type", "A_NATIVE");
    data.put("trans_amt", amount);
    return data;
  }
  static Map<String,String> hostingSample(String prefix) {
    Map<String,String> data = new TreeMap<>();
    data.put("goods_desc", prefix + " hosting sdk sample");
    data.put("hosting_data", "{\"project_title\":\"SDK Sample\",\"project_id\":\"P123\",\"request_type\":\"P\"}");
    data.put("huifu_id", "6666000100000001");
    data.put("pre_order_type", "1");
    data.put("req_date", "20260624");
    data.put("req_seq_id", "SDK-" + prefix + "-001");
    data.put("trans_amt", "0.02");
    data.put("trans_type", "A_NATIVE");
    return data;
  }
  static String post(String gateway, String path, Map<String,String> data, PrivateKey key) throws Exception {
    String canonical = json(data);
    String sign = sign(canonical.getBytes(StandardCharsets.UTF_8), key);
    String body = "{\"sys_id\":\"" + esc(SYS_ID) + "\",\"product_id\":\"" + esc(PRODUCT_ID) + "\",\"sign\":\"" + esc(sign) + "\",\"data\":" + canonical + "}";
    HttpRequest req = HttpRequest.newBuilder(URI.create(gateway + path))
      .header("Content-Type", "application/json;charset=UTF-8")
      .header("jpt-x-skill-source", "hfps/1.3.1;sandbox/1.0.1")
      .header("jpt-x-skill-huifu_id", data.get("huifu_id"))
      .POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8)).build();
    String resp = HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString()).body();
    if (!resp.contains("\"resp_code\":\"00000000\"") && !resp.contains("\"resp_code\":\"00000100\"")) throw new RuntimeException(resp);
    return resp;
  }
  static String controlGet(String control, String path) throws Exception {
    HttpRequest req = HttpRequest.newBuilder(URI.create(control + path)).GET().build();
    String resp = HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString()).body();
    if (!resp.contains("\"ok\":true")) throw new RuntimeException(resp);
    return resp;
  }
  static String controlPost(String control, String path, String body, String csrf) throws Exception {
    HttpRequest req = HttpRequest.newBuilder(URI.create(control + path))
      .header("Content-Type", "application/json")
      .header("X-Huifu-Sandbox-CSRF", csrf)
      .POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8)).build();
    String resp = HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString()).body();
    if (!resp.contains("\"ok\":true")) throw new RuntimeException(resp);
    return resp;
  }
  static String json(Map<String,String> data) {
    StringBuilder out = new StringBuilder("{");
    boolean first = true;
    for (Map.Entry<String,String> e : new TreeMap<>(data).entrySet()) {
      if (!first) out.append(",");
      first = false;
      out.append("\"").append(esc(e.getKey())).append("\":\"").append(esc(e.getValue())).append("\"");
    }
    return out.append("}").toString();
  }
  static String esc(String value) { return value.replace("\\", "\\\\").replace("\"", "\\\""); }
  static String match(String value, String regex) {
    Matcher m = Pattern.compile(regex).matcher(value);
    if (!m.find()) throw new RuntimeException("missing match " + regex + " in " + value);
    return m.group(1);
  }
  static String sign(byte[] message, PrivateKey key) throws Exception {
    Signature signature = Signature.getInstance("SHA256withRSA");
    signature.initSign(key);
    signature.update(message);
    return Base64.getEncoder().encodeToString(signature.sign());
  }
  static PrivateKey privateKey(String pem) throws Exception {
    byte[] der = Base64.getDecoder().decode(pem.replaceAll("-----[^-]+-----", "").replaceAll("\\s+", ""));
    return KeyFactory.getInstance("RSA").generatePrivate(new PKCS8EncodedKeySpec(der));
  }
}
'''


PHP_SAMPLE = r'''<?php
function sample($prefix, $suffix = "001", $amount = "0.01") {
    return [
        "goods_desc" => $prefix . " sdk sample",
        "huifu_id" => "6666000100000001",
        "req_date" => "20260624",
        "req_seq_id" => "SDK-" . $prefix . "-" . $suffix,
        "trade_type" => "A_NATIVE",
        "trans_amt" => $amount,
    ];
}
function hosting_sample($prefix) {
    return [
        "goods_desc" => $prefix . " hosting sdk sample",
        "hosting_data" => "{\"project_title\":\"SDK Sample\",\"project_id\":\"P123\",\"request_type\":\"P\"}",
        "huifu_id" => "6666000100000001",
        "pre_order_type" => "1",
        "req_date" => "20260624",
        "req_seq_id" => "SDK-" . $prefix . "-001",
        "trans_amt" => "0.02",
        "trans_type" => "A_NATIVE",
    ];
}
function canonical($data) {
    ksort($data);
    return json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
}
function sign_data($data, $privatePem) {
    openssl_sign(canonical($data), $signature, $privatePem, OPENSSL_ALGO_SHA256);
    return base64_encode($signature);
}
function post_gateway($gateway, $path, $data, $privatePem) {
    global $sysId, $productId;
    $body = json_encode([
        "sys_id" => $sysId,
        "product_id" => $productId,
        "sign" => sign_data($data, $privatePem),
        "data" => $data,
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    $context = stream_context_create([
        "http" => [
            "method" => "POST",
            "header" => "Content-Type: application/json;charset=UTF-8\r\njpt-x-skill-source: hfps/1.3.1;sandbox/1.0.1\r\njpt-x-skill-huifu_id: " . $data["huifu_id"] . "\r\n",
            "content" => $body,
            "ignore_errors" => true,
            "timeout" => 10,
        ],
    ]);
    $raw = file_get_contents($gateway . $path, false, $context);
    $decoded = json_decode($raw, true);
    if (!in_array(($decoded["data"]["resp_code"] ?? ""), ["00000000", "00000100"], true)) {
        fwrite(STDERR, $raw . PHP_EOL);
        exit(2);
    }
    return $decoded;
}
function control_get($control, $path) {
    $raw = file_get_contents($control . $path);
    $decoded = json_decode($raw, true);
    if (($decoded["ok"] ?? false) !== true) {
        fwrite(STDERR, $raw . PHP_EOL);
        exit(3);
    }
    return $decoded;
}
function control_post($control, $path, $data, $csrf) {
    $body = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    $context = stream_context_create([
        "http" => [
            "method" => "POST",
            "header" => "Content-Type: application/json\r\nX-Huifu-Sandbox-CSRF: " . $csrf . "\r\n",
            "content" => $body,
            "ignore_errors" => true,
            "timeout" => 10,
        ],
    ]);
    $raw = file_get_contents($control . $path, false, $context);
    $decoded = json_decode($raw, true);
    if (($decoded["ok"] ?? false) !== true) {
        fwrite(STDERR, $raw . PHP_EOL);
        exit(4);
    }
    return $decoded;
}
function create_paid($gateway, $privatePem, $prefix, $amount) {
    $data = sample($prefix, "001", $amount);
    $create = post_gateway($gateway, "/v4/trade/payment/create", $data, $privatePem);
    $query = ["huifu_id" => $data["huifu_id"], "hf_seq_id" => $create["data"]["hf_seq_id"]];
    post_gateway($gateway, "/v4/trade/payment/scanpay/query", $query, $privatePem);
    $second = post_gateway($gateway, "/v4/trade/payment/scanpay/query", $query, $privatePem);
    $data["hf_seq_id"] = $create["data"]["hf_seq_id"];
    $data["trans_stat"] = $second["data"]["trans_stat"] ?? "";
    return $data;
}
$gateway = $argv[1];
$privatePem = file_get_contents($argv[2]);
$control = $argv[4];
$csrf = $argv[5];
$sysId = $argv[6] ?? "6666000108840829";
$productId = $argv[7] ?? "YYZY";
$checks = [];

$agg = create_paid($gateway, $privatePem, "PHP-AGG", "0.01");
$checks[] = (($agg["trans_stat"] ?? "") === "S");

$refundPayment = create_paid($gateway, $privatePem, "PHP-RF-ORIG", "0.10");
$refund = [
    "huifu_id" => $refundPayment["huifu_id"],
    "ord_amt" => "0.04",
    "org_req_date" => $refundPayment["req_date"],
    "org_req_seq_id" => $refundPayment["req_seq_id"],
    "req_date" => "20260624",
    "req_seq_id" => "SDK-PHP-RF-001",
];
post_gateway($gateway, "/v4/trade/payment/scanpay/refund", $refund, $privatePem);
$refundQuery = ["huifu_id" => $refundPayment["huifu_id"], "org_req_date" => "20260624", "org_req_seq_id" => "SDK-PHP-RF-001"];
post_gateway($gateway, "/v4/trade/payment/scanpay/refundquery", $refundQuery, $privatePem);
$refundSecond = post_gateway($gateway, "/v4/trade/payment/scanpay/refundquery", $refundQuery, $privatePem);
$checks[] = (($refundSecond["data"]["trans_stat"] ?? "") === "S");

$closeOriginal = sample("PHP-CL-ORIG", "001", "0.03");
post_gateway($gateway, "/v4/trade/payment/create", $closeOriginal, $privatePem);
$close = [
    "huifu_id" => $closeOriginal["huifu_id"],
    "org_req_date" => $closeOriginal["req_date"],
    "org_req_seq_id" => $closeOriginal["req_seq_id"],
    "req_date" => "20260624",
    "req_seq_id" => "SDK-PHP-CL-001",
];
post_gateway($gateway, "/v2/trade/payment/scanpay/close", $close, $privatePem);
$closeQuery = ["huifu_id" => $closeOriginal["huifu_id"], "org_req_date" => $closeOriginal["req_date"], "org_req_seq_id" => $closeOriginal["req_seq_id"]];
post_gateway($gateway, "/v2/trade/payment/scanpay/closequery", $closeQuery, $privatePem);
$closeSecond = post_gateway($gateway, "/v2/trade/payment/scanpay/closequery", $closeQuery, $privatePem);
$checks[] = (($closeSecond["data"]["trans_stat"] ?? "") === "S");

$hosting = hosting_sample("PHP-HOST");
$preorder = post_gateway($gateway, "/v2/trade/hosting/payment/preorder", $hosting, $privatePem);
$preOrderId = $preorder["data"]["pre_order_id"];
control_get($control, "/__merchant/hosting/callback?pre_order_id=" . rawurlencode($preOrderId));
control_post($control, "/__merchant/hosting/confirm", ["pre_order_id" => $preOrderId], $csrf);
$hostingQuery = post_gateway($gateway, "/v2/trade/hosting/payment/queryorderinfo", [
    "req_date" => $hosting["req_date"],
    "req_seq_id" => "SDK-PHP-HOST-QRY-001",
    "huifu_id" => $hosting["huifu_id"],
    "org_req_date" => $hosting["req_date"],
    "org_req_seq_id" => $hosting["req_seq_id"],
], $privatePem);
$checks[] = (($hostingQuery["data"]["trans_stat"] ?? "") === "S");

$recon = ["file_date" => "20260623", "huifu_id" => "6666000100000001", "req_date" => "20260624", "req_seq_id" => "SDK-PHP-RECON"];
post_gateway($gateway, "/v2/trade/check/filequery", $recon, $privatePem);
$reconSecond = post_gateway($gateway, "/v2/trade/check/filequery", $recon, $privatePem);
$checks[] = isset($reconSecond["data"]["file_details"]);

$ok = !in_array(false, $checks, true);
echo json_encode([
    "language" => "php",
    "ok" => $ok,
    "chains" => ["aggregation", "hosting", "refund", "close", "reconciliation"],
    "req_seq_id" => $agg["req_seq_id"],
], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . PHP_EOL;
?>'''


if __name__ == "__main__":
    raise SystemExit(main())
