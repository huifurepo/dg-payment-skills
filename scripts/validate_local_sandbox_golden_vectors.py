#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


SIGNING_PROFILE = "sdk-v2-sorted-json"
GOLDEN_VECTOR_VERSION = "1.0"
JAVA_SDK = Path("docs/sdk/bspay-java-sdk-parent-generator-sdk/opps-bspay-java-sdk")
PHP_TOOL = Path("docs/sdk/bspay-php-sdk-feature_generator_sdk/BsPaySdk/core/BsPayTools.php")

REQUEST_VECTORS = [
    {
        "id": "aggregation-payment-create",
        "data": {
            "req_seq_id": "REQ-SDK-001",
            "req_date": "20260624",
            "huifu_id": "6666000100000001",
            "trade_type": "A_NATIVE",
            "trans_amt": "0.01",
            "goods_desc": "SDK一致性/聚合下单",
            "notify_url": "http://127.0.0.1:18080/notify?case=create",
        },
    },
    {
        "id": "aggregation-payment-query",
        "data": {
            "hf_seq_id": "HFSDKQUERY001",
            "req_seq_id": "REQ-SDK-001",
            "huifu_id": "6666000100000001",
        },
    },
    {
        "id": "html-and-query-escape-boundary",
        "data": {
            "req_seq_id": "REQ-SDK-HTML-001",
            "req_date": "20260630",
            "huifu_id": "6666000100000001",
            "trade_type": "A_NATIVE",
            "trans_amt": "0.01",
            "goods_desc": "SDK一致性 <tag>&value / 中文",
            "notify_url": "http://127.0.0.1:18080/notify?a=1&b=2",
            "method_expand": "{\"html\":\"<b>&value</b>\",\"path\":\"/pay/中文\"}",
        },
    },
    {
        "id": "hosting-preorder-string-json",
        "data": {
            "req_seq_id": "HREQ-SDK-001",
            "req_date": "20260624",
            "huifu_id": "6666000100000001",
            "trans_amt": "0.01",
            "goods_desc": "托管预下单",
            "project_info": "{\"project_id\":\"P002\",\"project_title\":\"Sandbox Project\",\"request_type\":\"P\"}",
        },
    },
    {
        "id": "reconciliation-filequery",
        "data": {
            "req_seq_id": "BILL-SDK-001",
            "req_date": "20260624",
            "huifu_id": "6666000100000001",
            "file_date": "20260623",
            "bill_type": "TRADE_BILL",
        },
    },
]

NOTIFY_RESP_DATA = '{"resp_code":"00000000","resp_desc":"成功","huifu_id":"6666000100000001","req_seq_id":"REQ-SDK-001","trans_stat":"S"}'
WEBHOOK_RAW_BODY = '{"event_type":"trans.pay","huifu_id":"6666000100000001","req_seq_id":"REQ-SDK-001","trans_stat":"S"}'
WEBHOOK_ENDPOINT_KEY = "0123456789abcdef0123456789abcdef"
SYNTHETIC_PRIVATE_KEY_PKCS8_B64 = (
    "MIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQCkk2Wy65+oeB11t6DII3qN04HckrlkamuDPjHxSXrG9dU0HLvpmckC0xzy0o2Dc3xIrGlMtP6oFoCAiTihxV/joWCOIlsmFUN1pya22TThf3vI1KWiYgeMm2czgteZgv8qMcWu5ockb7WHZB9ipk3IeIjAxsNn7hXK0AVxc2GCFjk8bMNWALaWTHl03l52zZxoCpRN4DdWjABDYxovstSrDOFNp7zS+IiA3NYCJ6Cfhirapa/af+/bMcY0gw4ZZfDeyL7ksik+IHSKI+tTb9UYvDW1A+q9x2JDomKfb9by/6Nwsgqp1exPDmaZHA3QZO+DY65Ggc10ntHOTb6wqdExAgMBAAECggEAA/3t4bov5PiTsSfui5qhGodGsNvS1eHz8I35AAyJ4LR66UW7wOwoEUkfVfxJjozytvOOcui3/Zbc8C4D57HSxEHexovRFxPwdZsQlOJULON4YSDXt+APWISDeBJXwInW8eydPV0RNzVjdPpQSmA7MxF8/0oPvtNdh9rl97OQA6vHqzUU4QnqtlWWbRtOrBd+lgRPTRSJgOL2S55nomk2Zzk9wno4sVBRX0+PHaXcw/MnWZR5VuI87DJbko1dTQ28aQqtw75qNFBB5imXkgRcsD3Eh4m+nI/fGq+fr96dyo9GWbbb6vb9iBaj/lq+dQLwdiJiRBp9NR1OfANnTgLnjQKBgQDQ1KYWzq5qe0Rm9J0UNq+3Js9kgG9CnipBKNNzfIAwY56/LSGyMQFc/4F7CYPgbD5mPo6XmzxJ4D7eAKzalQcTtvlZHE8pNI6oI646LxqU6yLJB6pGliMkGIsEAJPVtRNGotdEkUjxr+xaeNDVoU++KPWqmT9kcqLphA/tGake5QKBgQDJv8Trt9YBTz/UzoxSogDY4H59waF23s/aiEEy/Sw+/nqsUF9EezN5aaV+pBBlO+KLlmS+9M9saxn7ESJjuuSyBBnUfs1P6NX9Uk6JlJ9H2/ltHGzBxwTuACMOupL6jfE9jkQGiGzRzQrcOZ6hEcxE9t3POkApcaoIsDssuqG4XQJ/DQ09VC+WtxD9NXIUXy8LzGagj6d3TLKV8XybupwNZvjS8x/e+0QU0bsmXIo7s8sQG1PNlaweGH/rbfSc2Qx3ZMQK0Ybza5/dSqTwPrKy9pu7kNTpz3+Ssq7WAWoH01N94OxMh/yMko5sNztV0gRC95+XuxHY5G5FwFKArFDuQQKBgB6WRHS4Wmm4aiUJa5zbkuVOo97NDH3JKhonrjrcx2iFjHOze74WL6eorL6WgSXX/nDLTFrnIst9MWMvJdeY7jNPC9t7ngUPd+IAKIgTUFLEtvwj4xk94zFyM953yvDRtFFw0D9tT5I/U/Yvhi1FVYLfKqHQYwnlgbHvhgkyAnLBAoGAI8yiqezJtTvTCtSumFqXYOqMiLqFU+WHPw0GtuwcKZiA4Jd2fEoXT/kpntjMNoEWmPYJwsQt4Ejr/Sy48yCh+sI7Eo0xcGSJubhzWbV58bZhoug/0hZkD/9lM01xYxGJw4vEwzHZDyPZ9vdU7eg2OuFngaznMvMRwjZ41Z9JWRs="
)
SYNTHETIC_PUBLIC_KEY_X509_B64 = (
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApJNlsuufqHgddbegyCN6jdOB3JK5ZGprgz4x8Ul6xvXVNBy76ZnJAtMc8tKNg3N8SKxpTLT+qBaAgIk4ocVf46FgjiJbJhVDdacmttk04X97yNSlomIHjJtnM4LXmYL/KjHFruaHJG+1h2QfYqZNyHiIwMbDZ+4VytAFcXNhghY5PGzDVgC2lkx5dN5eds2caAqUTeA3VowAQ2MaL7LUqwzhTae80viIgNzWAiegn4Yq2qWv2n/v2zHGNIMOGWXw3si+5LIpPiB0iiPrU2/VGLw1tQPqvcdiQ6Jin2/W8v+jcLIKqdXsTw5mmRwN0GTvg2OuRoHNdJ7Rzk2+sKnRMQIDAQAB"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local-sandbox SDK signing golden vectors.")
    parser.add_argument("--strict", action="store_true", help="fail if Java, Maven, PHP, or Go harnesses cannot run")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    java_sdk_dir = repo_root / JAVA_SDK
    php_tool = repo_root / PHP_TOOL
    require(java_sdk_dir.is_dir(), f"Java SDK directory not found: {java_sdk_dir}", args.strict)
    require(php_tool.is_file(), f"PHP BsPayTools not found: {php_tool}", args.strict)

    with tempfile.TemporaryDirectory(prefix="hf-sandbox-golden-") as tmp_raw:
        tmp = Path(tmp_raw)
        java_cp = build_java_harness(tmp, java_sdk_dir, args.strict)
        php_harness = write_php_harness(tmp, php_tool)
        go_harness = write_go_harness(tmp)

        private_key = SYNTHETIC_PRIVATE_KEY_PKCS8_B64
        public_key = SYNTHETIC_PUBLIC_KEY_X509_B64
        private_path = tmp / "private.pkcs8.b64"
        public_path = tmp / "public.x509.b64"
        private_path.write_text(private_key, encoding="utf-8")
        public_path.write_text(public_key, encoding="utf-8")

        results = []
        for vector in REQUEST_VECTORS:
            source_json = json.dumps(vector["data"], ensure_ascii=False, separators=(",", ":"))
            expected = json.dumps(vector["data"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            source_path = tmp / f"{vector['id']}.json"
            source_path.write_text(source_json, encoding="utf-8")

            go_result = go_run(go_harness, ["canonical-sign", source_path, private_path, public_path], args.strict)
            java_result = parse_output(
                run(["java", "-cp", java_cp, "GoldenVectorHarness", "canonical-sign", str(source_path), str(private_path), str(public_path)], strict=args.strict)
            )
            php_result = parse_output(
                run(["php", str(php_harness), "canonical-sign", str(source_path), str(private_path), str(public_path)], strict=args.strict)
            )

            assert_equal(vector["id"], "go canonical", go_result["CANONICAL"], expected)
            assert_equal(vector["id"], "java canonical", java_result["CANONICAL"], expected)
            assert_equal(vector["id"], "php canonical", php_result["CANONICAL"], expected)
            assert_equal(vector["id"], "go signature", go_result["SIGNATURE"], java_result["SIGNATURE"])
            assert_equal(vector["id"], "php signature", php_result["SIGNATURE"], java_result["SIGNATURE"])
            assert_equal(vector["id"], "go verify", go_result["VERIFY"], "true")
            assert_equal(vector["id"], "java verify", java_result["VERIFY"], "true")
            assert_equal(vector["id"], "php verify", php_result["VERIFY"], "true")
            results.append({"id": vector["id"], "canonical_sha256": sha256_text(expected)})

        notify_path = tmp / "notify-resp-data.json"
        notify_path.write_text(NOTIFY_RESP_DATA, encoding="utf-8")
        go_notify = go_run(go_harness, ["raw-sign", notify_path, private_path, public_path], args.strict)
        java_notify = parse_output(run(["java", "-cp", java_cp, "GoldenVectorHarness", "raw-sign", str(notify_path), str(private_path), str(public_path)], strict=args.strict))
        php_notify = parse_output(run(["php", str(php_harness), "raw-sign", str(notify_path), str(private_path), str(public_path)], strict=args.strict))
        assert_equal("notify-raw-resp-data", "go raw", go_notify["RAW"], NOTIFY_RESP_DATA)
        assert_equal("notify-raw-resp-data", "java signature", java_notify["SIGNATURE"], go_notify["SIGNATURE"])
        assert_equal("notify-raw-resp-data", "php signature", php_notify["SIGNATURE"], go_notify["SIGNATURE"])
        assert_equal("notify-raw-resp-data", "go verify", go_notify["VERIFY"], "true")
        assert_equal("notify-raw-resp-data", "java verify", java_notify["VERIFY"], "true")
        assert_equal("notify-raw-resp-data", "php verify", php_notify["VERIFY"], "true")
        results.append({"id": "notify-raw-resp-data", "raw_sha256": sha256_text(NOTIFY_RESP_DATA)})

        webhook_path = tmp / "webhook-body.json"
        webhook_path.write_text(WEBHOOK_RAW_BODY, encoding="utf-8")
        expected_webhook_sign = hashlib.md5((WEBHOOK_RAW_BODY + WEBHOOK_ENDPOINT_KEY).encode("utf-8")).hexdigest().upper()
        go_webhook = go_run(go_harness, ["webhook-md5", webhook_path, WEBHOOK_ENDPOINT_KEY], args.strict)
        java_webhook = parse_output(run(["java", "-cp", java_cp, "GoldenVectorHarness", "webhook-md5", str(webhook_path), WEBHOOK_ENDPOINT_KEY], strict=args.strict))
        php_webhook = parse_output(run(["php", str(php_harness), "webhook-md5", str(webhook_path), WEBHOOK_ENDPOINT_KEY], strict=args.strict))
        assert_equal("webhook-raw-body-md5", "go signature", go_webhook["WEBHOOK_SIGNATURE"], expected_webhook_sign)
        assert_equal("webhook-raw-body-md5", "java signature", java_webhook["WEBHOOK_SIGNATURE"], expected_webhook_sign)
        assert_equal("webhook-raw-body-md5", "php signature", php_webhook["WEBHOOK_SIGNATURE"], expected_webhook_sign)
        assert_equal("webhook-raw-body-md5", "php sdk verify", php_webhook["SDK_VERIFY"], "true")
        results.append({"id": "webhook-raw-body-md5", "raw_sha256": sha256_text(WEBHOOK_RAW_BODY)})

    print(
        json.dumps(
            {
                "ok": True,
                "golden_vector_version": GOLDEN_VECTOR_VERSION,
                "signing_profile": SIGNING_PROFILE,
                "synthetic_public_key_sha256": sha256_text(SYNTHETIC_PUBLIC_KEY_X509_B64),
                "vectors": results,
            },
            ensure_ascii=False,
        )
    )
    return 0


def build_java_harness(tmp: Path, java_sdk_dir: Path, strict: bool) -> str:
    cp_file = tmp / "java-sdk.classpath"
    run(["mvn", "-q", "dependency:build-classpath", f"-Dmdep.outputFile={cp_file}"], cwd=java_sdk_dir, strict=strict)
    dependency_cp = cp_file.read_text(encoding="utf-8").strip() if cp_file.is_file() else ""
    classes_dir = tmp / "java-classes"
    classes_dir.mkdir()
    harness = tmp / "GoldenVectorHarness.java"
    harness.write_text(JAVA_HARNESS, encoding="utf-8")
    compile_cp = dependency_cp
    run(
        [
            "javac",
            "-encoding",
            "UTF-8",
            "-d",
            str(classes_dir),
            "-cp",
            compile_cp,
            "-sourcepath",
            str(java_sdk_dir / "src/main/java"),
            str(harness),
        ],
        strict=strict,
    )
    return os.pathsep.join([str(classes_dir), dependency_cp]) if dependency_cp else str(classes_dir)


def write_php_harness(tmp: Path, php_tool: Path) -> Path:
    path = tmp / "golden_vectors.php"
    path.write_text(PHP_HARNESS.replace("__BSPAY_TOOLS__", str(php_tool).replace("\\", "\\\\")), encoding="utf-8")
    return path


def write_go_harness(tmp: Path) -> Path:
    path = tmp / "golden_vectors.go"
    path.write_text(GO_HARNESS, encoding="utf-8")
    return path


def go_run(go_harness: Path, args: list[object], strict: bool) -> dict[str, str]:
    return parse_output(run(["go", "run", str(go_harness), *[str(item) for item in args]], strict=strict))


def run(cmd: list[str], *, cwd: Path | None = None, strict: bool = True) -> str:
    cmd = [resolve_executable(cmd[0]), *cmd[1:]]
    try:
        return subprocess.check_output(cmd, cwd=cwd, text=True, stderr=subprocess.STDOUT, encoding="utf-8")
    except FileNotFoundError as exc:
        if strict:
            raise SystemExit(f"[ERROR] missing executable {cmd[0]!r}: {exc}") from exc
        raise
    except subprocess.CalledProcessError as exc:
        if strict:
            raise SystemExit(f"[ERROR] command failed: {' '.join(cmd)}\n{exc.output}") from exc
        raise


def resolve_executable(name: str) -> str:
    if os.path.isabs(name) or any(sep in name for sep in ("/", "\\")):
        return name
    candidates = [name]
    if os.name == "nt":
        candidates = [name + suffix for suffix in (".exe", ".cmd", ".bat", "")]
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return name


def parse_output(raw: str) -> dict[str, str]:
    out = {}
    for line in raw.splitlines():
        if "=" not in line:
            continue
        key, encoded = line.split("=", 1)
        out[key] = base64.b64decode(encoded).decode("utf-8")
    return out


def require(condition: bool, message: str, strict: bool) -> None:
    if condition:
        return
    if strict:
        raise SystemExit(f"[ERROR] {message}")
    print(json.dumps({"ok": False, "warning": message}, ensure_ascii=False))


def assert_equal(vector_id: str, label: str, got: str, want: str) -> None:
    if got != want:
        raise SystemExit(f"[ERROR] {vector_id} {label} mismatch\ngot:  {got}\nwant: {want}")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


JAVA_HARNESS = r'''
import com.huifu.bspay.sdk.opps.core.sign.JsonUtils;
import com.huifu.bspay.sdk.opps.core.utils.RsaUtils;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.Base64;
import java.util.Locale;
import java.util.Map;

public class GoldenVectorHarness {
    public static void main(String[] args) throws Exception {
        switch (args[0]) {
            case "keys":
                Map<String, String> keys = RsaUtils.generateKeyPair(2048);
                out("PRIVATE_KEY", keys.get(RsaUtils.RSA_PRIVATE_KEY));
                out("PUBLIC_KEY", keys.get(RsaUtils.RSA_PUBLIC_KEY));
                return;
            case "canonical-sign": {
                String source = Files.readString(Path.of(args[1]), StandardCharsets.UTF_8);
                String privateKey = Files.readString(Path.of(args[2]), StandardCharsets.UTF_8).trim();
                String publicKey = Files.readString(Path.of(args[3]), StandardCharsets.UTF_8).trim();
                String canonical = JsonUtils.sort4JsonString(source, 0);
                signAndPrint(canonical, privateKey, publicKey, true);
                return;
            }
            case "raw-sign": {
                String raw = Files.readString(Path.of(args[1]), StandardCharsets.UTF_8);
                String privateKey = Files.readString(Path.of(args[2]), StandardCharsets.UTF_8).trim();
                String publicKey = Files.readString(Path.of(args[3]), StandardCharsets.UTF_8).trim();
                signAndPrint(raw, privateKey, publicKey, false);
                return;
            }
            case "webhook-md5": {
                String raw = Files.readString(Path.of(args[1]), StandardCharsets.UTF_8);
                out("WEBHOOK_SIGNATURE", md5(raw + args[2]).toUpperCase(Locale.ROOT));
                return;
            }
            default:
                throw new IllegalArgumentException("unknown mode " + args[0]);
        }
    }

    private static void signAndPrint(String raw, String privateKey, String publicKey, boolean canonical) {
        String sign = RsaUtils.sign(raw, privateKey);
        if (canonical) {
            out("CANONICAL", raw);
        } else {
            out("RAW", raw);
        }
        out("SIGNATURE", sign);
        out("VERIFY", String.valueOf(RsaUtils.verify(raw, publicKey, sign)));
    }

    private static String md5(String value) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] digest = md.digest(value.getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(String.format("%02x", b & 0xff));
        }
        return sb.toString();
    }

    private static void out(String key, String value) {
        System.out.println(key + "=" + Base64.getEncoder().encodeToString(value.getBytes(StandardCharsets.UTF_8)));
    }
}
'''


PHP_HARNESS = r'''<?php
require_once "__BSPAY_TOOLS__";
use BsPaySdk\core\BsPayTools;

function outv($key, $value) {
    echo $key . "=" . base64_encode($value) . PHP_EOL;
}

$mode = $argv[1];
if ($mode === "canonical-sign") {
    $data = json_decode(file_get_contents($argv[2]), true);
    ksort($data);
    $canonical = json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    $canonical = str_replace("\n", "\\n", $canonical);
    $privateKey = trim(file_get_contents($argv[3]));
    $publicKey = trim(file_get_contents($argv[4]));
    $signature = BsPayTools::sha_with_rsa_sign($canonical, $privateKey);
    outv("CANONICAL", $canonical);
    outv("SIGNATURE", $signature);
    outv("VERIFY", BsPayTools::verifySign($signature, $canonical, $publicKey) === 1 ? "true" : "false");
    exit(0);
}
if ($mode === "raw-sign") {
    $raw = file_get_contents($argv[2]);
    $privateKey = trim(file_get_contents($argv[3]));
    $publicKey = trim(file_get_contents($argv[4]));
    $signature = BsPayTools::sha_with_rsa_sign($raw, $privateKey);
    outv("RAW", $raw);
    outv("SIGNATURE", $signature);
    outv("VERIFY", BsPayTools::verifySign($signature, $raw, $publicKey) === 1 ? "true" : "false");
    exit(0);
}
if ($mode === "webhook-md5") {
    $raw = file_get_contents($argv[2]);
    $key = $argv[3];
    $signature = strtoupper(md5($raw . $key));
    $data = json_decode($raw, true);
    outv("WEBHOOK_SIGNATURE", $signature);
    outv("SDK_VERIFY", BsPayTools::verify_webhook_sign($signature, $data, $key) ? "true" : "false");
    exit(0);
}
fwrite(STDERR, "unknown mode " . $mode . PHP_EOL);
exit(2);
'''


GO_HARNESS = r'''
package main

import (
	"bytes"
	"crypto"
	"crypto/md5"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

func main() {
	if len(os.Args) < 2 {
		panic("missing mode")
	}
	switch os.Args[1] {
	case "canonical-sign":
		raw, err := os.ReadFile(os.Args[2])
		must(err)
		var data map[string]any
		must(json.Unmarshal(raw, &data))
		canonical, err := canonicalJSON(data)
		must(err)
		signAndPrint(canonical, os.Args[3], os.Args[4], true)
	case "raw-sign":
		raw, err := os.ReadFile(os.Args[2])
		must(err)
		signAndPrint(string(raw), os.Args[3], os.Args[4], false)
	case "webhook-md5":
		raw, err := os.ReadFile(os.Args[2])
		must(err)
		sum := md5.Sum([]byte(string(raw) + os.Args[3]))
		out("WEBHOOK_SIGNATURE", strings.ToUpper(hex.EncodeToString(sum[:])))
	default:
		panic("unknown mode " + os.Args[1])
	}
}

func canonicalJSON(value any) (string, error) {
	var buf bytes.Buffer
	enc := json.NewEncoder(&buf)
	enc.SetEscapeHTML(false)
	if err := enc.Encode(value); err != nil {
		return "", err
	}
	return string(bytes.TrimSuffix(buf.Bytes(), []byte("\n"))), nil
}

func signAndPrint(raw, privatePath, publicPath string, canonical bool) {
	privateKey := readPrivate(privatePath)
	publicKey := readPublic(publicPath)
	sum := sha256.Sum256([]byte(raw))
	signature, err := rsa.SignPKCS1v15(rand.Reader, privateKey, crypto.SHA256, sum[:])
	must(err)
	signatureText := base64.StdEncoding.EncodeToString(signature)
	if canonical {
		out("CANONICAL", raw)
	} else {
		out("RAW", raw)
	}
	out("SIGNATURE", signatureText)
	sigBytes, err := base64.StdEncoding.DecodeString(signatureText)
	must(err)
	err = rsa.VerifyPKCS1v15(publicKey, crypto.SHA256, sum[:], sigBytes)
	if err == nil {
		out("VERIFY", "true")
	} else {
		out("VERIFY", "false")
	}
}

func readPrivate(path string) *rsa.PrivateKey {
	content, err := os.ReadFile(path)
	must(err)
	der, err := base64.StdEncoding.DecodeString(strings.TrimSpace(string(content)))
	must(err)
	key, err := x509.ParsePKCS8PrivateKey(der)
	must(err)
	privateKey, ok := key.(*rsa.PrivateKey)
	if !ok {
		panic("private key is not RSA")
	}
	return privateKey
}

func readPublic(path string) *rsa.PublicKey {
	content, err := os.ReadFile(path)
	must(err)
	der, err := base64.StdEncoding.DecodeString(strings.TrimSpace(string(content)))
	must(err)
	key, err := x509.ParsePKIXPublicKey(der)
	must(err)
	publicKey, ok := key.(*rsa.PublicKey)
	if !ok {
		panic("public key is not RSA")
	}
	return publicKey
}

func out(key, value string) {
	fmt.Println(key + "=" + base64.StdEncoding.EncodeToString([]byte(value)))
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
'''


if __name__ == "__main__":
    raise SystemExit(main())
