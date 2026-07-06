package main

import (
	"bytes"
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/json"
	"encoding/pem"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

type CredentialSet struct {
	MerchantPrivate   *rsa.PrivateKey
	MerchantPublic    *rsa.PublicKey
	GatewayPrivate    *rsa.PrivateKey
	GatewayPublic     *rsa.PublicKey
	HuifuPublic       *rsa.PublicKey
	Directory         string
	Ephemeral         bool
	ProfileName       string
	SysID             string
	ProductID         string
	SignatureModel    string
	MerchantKeySource string
}

func loadOrCreateCredentials(dataDir string, ephemeral bool) (*CredentialSet, error) {
	return loadOrCreateCredentialsProfile(dataDir, ephemeral, "")
}

func loadOrCreateCredentialsProfile(dataDir string, ephemeral bool, profileName string) (*CredentialSet, error) {
	profileName = strings.TrimSpace(profileName)
	if profileName == "synthetic" {
		profileName = ""
	}
	if profileName != "" {
		return loadCredentialProfile(profileName, dataDir, ephemeral)
	}
	creds := &CredentialSet{Directory: filepath.Join(dataDir, "credentials"), Ephemeral: ephemeral}
	if ephemeral {
		return generateCredentialSet(creds, "synthetic-dual-key")
	}
	if err := os.MkdirAll(creds.Directory, 0o700); err != nil {
		return nil, err
	}
	merchantPath := filepath.Join(creds.Directory, "merchant-sandbox-private.pem")
	gatewayPath := filepath.Join(creds.Directory, "gateway-sandbox-private.pem")
	if fileExists(merchantPath) && fileExists(gatewayPath) {
		merchant, err := readPrivateKey(merchantPath)
		if err != nil {
			return nil, err
		}
		gateway, err := readPrivateKey(gatewayPath)
		if err != nil {
			return nil, err
		}
		creds.MerchantPrivate = merchant
		creds.MerchantPublic = &merchant.PublicKey
		creds.GatewayPrivate = gateway
		creds.GatewayPublic = &gateway.PublicKey
		creds.ProfileName = "synthetic"
		creds.SignatureModel = "synthetic-dual-key"
		creds.MerchantKeySource = "local-file"
		return creds, nil
	}
	if _, err := generateCredentialSet(creds, "synthetic-dual-key"); err != nil {
		return nil, err
	}
	if err := writePrivateKey(merchantPath, creds.MerchantPrivate); err != nil {
		return nil, err
	}
	if err := writePrivateKey(gatewayPath, creds.GatewayPrivate); err != nil {
		return nil, err
	}
	return creds, nil
}

func generateCredentialSet(creds *CredentialSet, signatureModel string) (*CredentialSet, error) {
	merchant, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return nil, err
	}
	gateway, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return nil, err
	}
	creds.MerchantPrivate = merchant
	creds.MerchantPublic = &merchant.PublicKey
	creds.GatewayPrivate = gateway
	creds.GatewayPublic = &gateway.PublicKey
	creds.ProfileName = "synthetic"
	creds.SignatureModel = signatureModel
	creds.MerchantKeySource = "generated-synthetic"
	return creds, nil
}

func writePrivateKey(path string, key *rsa.PrivateKey) error {
	der := x509.MarshalPKCS1PrivateKey(key)
	block := &pem.Block{Type: "RSA PRIVATE KEY", Bytes: der}
	return os.WriteFile(path, pem.EncodeToMemory(block), 0o600)
}

func readPrivateKey(path string) (*rsa.PrivateKey, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	return parsePrivateKeyMaterial(string(b))
}

func parsePrivateKeyMaterial(value string) (*rsa.PrivateKey, error) {
	der, err := decodeKeyMaterial(value)
	if err != nil {
		return nil, err
	}
	if key, err := x509.ParsePKCS1PrivateKey(der); err == nil {
		return key, nil
	}
	parsed, err := x509.ParsePKCS8PrivateKey(der)
	if err != nil {
		return nil, err
	}
	key, ok := parsed.(*rsa.PrivateKey)
	if !ok {
		return nil, errors.New("private key is not RSA")
	}
	return key, nil
}

func parsePublicKeyMaterial(value string) (*rsa.PublicKey, error) {
	der, err := decodeKeyMaterial(value)
	if err != nil {
		return nil, err
	}
	if key, err := x509.ParsePKCS1PublicKey(der); err == nil {
		return key, nil
	}
	parsed, err := x509.ParsePKIXPublicKey(der)
	if err != nil {
		return nil, err
	}
	key, ok := parsed.(*rsa.PublicKey)
	if !ok {
		return nil, errors.New("public key is not RSA")
	}
	return key, nil
}

func decodeKeyMaterial(value string) ([]byte, error) {
	value = strings.TrimSpace(value)
	if value == "" {
		return nil, errors.New("empty key material")
	}
	if block, _ := pem.Decode([]byte(value)); block != nil {
		return block.Bytes, nil
	}
	compact := strings.Map(func(r rune) rune {
		if r == '\r' || r == '\n' || r == '\t' || r == ' ' {
			return -1
		}
		return r
	}, value)
	return base64.StdEncoding.DecodeString(compact)
}

func publicKeyPEM(key *rsa.PublicKey) string {
	der := x509.MarshalPKCS1PublicKey(key)
	return string(pem.EncodeToMemory(&pem.Block{Type: "RSA PUBLIC KEY", Bytes: der}))
}

func privateKeyPEM(key *rsa.PrivateKey) string {
	der := x509.MarshalPKCS1PrivateKey(key)
	return string(pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: der}))
}

func publicKeyPKIXBase64(key *rsa.PublicKey) string {
	der, err := x509.MarshalPKIXPublicKey(key)
	if err != nil {
		return ""
	}
	return base64.StdEncoding.EncodeToString(der)
}

func privateKeyPKCS8Base64(key *rsa.PrivateKey) string {
	der, err := x509.MarshalPKCS8PrivateKey(key)
	if err != nil {
		return ""
	}
	return base64.StdEncoding.EncodeToString(der)
}

func publicKeyFingerprint(key *rsa.PublicKey) string {
	der := x509.MarshalPKCS1PublicKey(key)
	sum := sha256.Sum256(der)
	return base64.RawURLEncoding.EncodeToString(sum[:])[:24]
}

func signData(data map[string]any, key *rsa.PrivateKey) (string, error) {
	canonical, err := canonicalData(data)
	if err != nil {
		return "", err
	}
	return signRaw(canonical, key)
}

func signRaw(raw string, key *rsa.PrivateKey) (string, error) {
	sum := sha256.Sum256([]byte(raw))
	sig, err := rsa.SignPKCS1v15(rand.Reader, key, crypto.SHA256, sum[:])
	if err != nil {
		return "", err
	}
	return base64.StdEncoding.EncodeToString(sig), nil
}

func verifyRaw(raw, signature string, key *rsa.PublicKey) error {
	sig, err := base64.StdEncoding.DecodeString(signature)
	if err != nil {
		return err
	}
	sum := sha256.Sum256([]byte(raw))
	return rsa.VerifyPKCS1v15(key, crypto.SHA256, sum[:], sig)
}

func verifyData(data map[string]any, signature string, key *rsa.PublicKey) error {
	canonical, err := canonicalData(data)
	if err != nil {
		return err
	}
	return verifyRaw(canonical, signature, key)
}

func dataDigest(data map[string]any) (string, error) {
	canonical, err := canonicalData(data)
	if err != nil {
		return "", err
	}
	sum := sha256.Sum256([]byte(canonical))
	return "sha256:" + base64.RawURLEncoding.EncodeToString(sum[:]), nil
}

func canonicalData(data map[string]any) (string, error) {
	if data == nil {
		data = map[string]any{}
	}
	var buf bytes.Buffer
	enc := json.NewEncoder(&buf)
	enc.SetEscapeHTML(false)
	if err := enc.Encode(data); err != nil {
		return "", fmt.Errorf("canonicalize sdk sorted json: %w", err)
	}
	return string(bytes.TrimSuffix(buf.Bytes(), []byte("\n"))), nil
}

func fileExists(path string) bool {
	_, err := os.Stat(path)
	return err == nil
}
