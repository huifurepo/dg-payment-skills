package main

import (
	"crypto/rand"
	"crypto/rsa"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

const (
	officialDemoProfileName        = "official-demo"
	officialDemoProductID          = "YYZY"
	officialDemoSysID              = "6666000108840829"
	officialDemoMerchantKeyFile    = "official-demo-merchant-private.pem"
	officialDemoSandboxKeyFile     = "official-demo-sandbox-private.pem"
	officialDemoMerchantKeyWarning = "official-demo private export requires --allow-private-export and must stay local"
)

func loadCredentialProfile(name, dataDir string, ephemeral bool) (*CredentialSet, error) {
	name = strings.TrimSpace(name)
	switch name {
	case "", "synthetic":
		return nil, errors.New("synthetic profile is loaded through generated credentials")
	case officialDemoProfileName:
		merchant, merchantSource, err := loadOrCreateOfficialDemoKey(dataDir, ephemeral, officialDemoMerchantKeyFile)
		if err != nil {
			return nil, fmt.Errorf("load %s merchant key: %w", officialDemoProfileName, err)
		}
		sandbox, sandboxSource, err := loadOrCreateOfficialDemoKey(dataDir, ephemeral, officialDemoSandboxKeyFile)
		if err != nil {
			return nil, fmt.Errorf("load %s sandbox key: %w", officialDemoProfileName, err)
		}
		return &CredentialSet{
			MerchantPrivate:   merchant,
			MerchantPublic:    &merchant.PublicKey,
			GatewayPrivate:    sandbox,
			GatewayPublic:     &sandbox.PublicKey,
			HuifuPublic:       &sandbox.PublicKey,
			Directory:         filepath.Join(dataDir, "credentials"),
			Ephemeral:         ephemeral,
			ProfileName:       officialDemoProfileName,
			SysID:             officialDemoSysID,
			ProductID:         officialDemoProductID,
			SignatureModel:    "dual_key_local_sandbox",
			MerchantKeySource: merchantSource + ";sandbox=" + sandboxSource,
		}, nil
	default:
		return nil, fmt.Errorf("unknown credential profile %q", name)
	}
}

func loadOrCreateOfficialDemoKey(dataDir string, ephemeral bool, fileName string) (*rsa.PrivateKey, string, error) {
	if dataDir == "" {
		dataDir = defaultDataDir()
	}
	if ephemeral {
		key, err := rsa.GenerateKey(rand.Reader, 2048)
		return key, "generated-ephemeral", err
	}
	dir := filepath.Join(dataDir, "credentials")
	path := filepath.Join(dir, fileName)
	if fileExists(path) {
		key, err := readPrivateKey(path)
		return key, "local-file", err
	}
	if err := os.MkdirAll(dir, 0o700); err != nil {
		return nil, "", err
	}
	key, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return nil, "", err
	}
	if err := writePrivateKey(path, key); err != nil {
		return nil, "", err
	}
	return key, "generated-local-file", nil
}

func credentialProfileSummary(creds *CredentialSet) map[string]any {
	if creds == nil {
		return map[string]any{"profile": "unknown"}
	}
	out := map[string]any{
		"profile":                     firstNonEmpty(creds.ProfileName, "synthetic"),
		"signature_model":             firstNonEmpty(creds.SignatureModel, "synthetic-dual-key"),
		"merchant_public_fingerprint": publicKeyFingerprint(creds.MerchantPublic),
		"sandbox_public_fingerprint":  publicKeyFingerprint(creds.GatewayPublic),
	}
	if creds.MerchantKeySource != "" {
		out["merchant_key_source"] = creds.MerchantKeySource
	}
	if creds.SysID != "" {
		out["sys_id"] = creds.SysID
	}
	if creds.ProductID != "" {
		out["product_id"] = creds.ProductID
	}
	if creds.HuifuPublic != nil {
		out["huifu_public_fingerprint"] = publicKeyFingerprint(creds.HuifuPublic)
	}
	return out
}

func credentialExportPayload(creds *CredentialSet, gatewayURL, webhookEndpointKey string) map[string]string {
	signatureModel := firstNonEmpty(creds.SignatureModel, "synthetic-dual-key")
	merchantPrivateKey := privateKeyPKCS8Base64(creds.MerchantPrivate)
	merchantPublicKey := publicKeyPKIXBase64(creds.GatewayPublic)
	payload := map[string]string{
		"gateway_url":          gatewayURL,
		"sys_id":               creds.SysID,
		"product_id":           creds.ProductID,
		"huifu_id":             "6666000100000001",
		"skill_source":         sandboxSkillSource,
		"merchant_private_key": merchantPrivateKey,
		"merchant_public_key":  merchantPublicKey,
		"signature_model":      signatureModel,
		"usage":                "本地沙箱模式下 skill_source 使用 " + sandboxSkillSource + "；merchant_private_key 用于客户项目请求加签；merchant_public_key 用于客户项目验证本地沙箱响应和通知签名；webhook_endpoint_key 用于客户项目验证本地沙箱 Webhook 签名。RSA 密钥值均为无 PEM 头尾、无换行的 Base64。",
	}
	if strings.TrimSpace(webhookEndpointKey) != "" {
		payload["webhook_endpoint_key"] = webhookEndpointKey
	}
	return payload
}

func credentialWatermark(creds *CredentialSet) string {
	if creds != nil && creds.ProfileName == officialDemoProfileName {
		return "official-demo local sandbox preview only; do not use for official joint debugging, production, or unauthorized environments"
	}
	return "local sandbox only; do not use for official joint debugging or production"
}
