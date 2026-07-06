package main

import (
	"bytes"
	"context"
	"crypto/sha256"
	"crypto/subtle"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/url"
	"strings"
	"time"
)

type Envelope struct {
	SysID     string         `json:"sys_id"`
	ProductID string         `json:"product_id"`
	Sign      string         `json:"sign"`
	Data      map[string]any `json:"data"`
}

type SignedResponse struct {
	Sign string         `json:"sign"`
	Data map[string]any `json:"data"`
}

func (a *App) controlHandler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/", a.handleControlUI)
	mux.HandleFunc("/ui", a.handleControlUI)
	mux.HandleFunc("/__asset/", a.handleUIAsset)
	mux.HandleFunc("/__ui/state", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		writeJSON(w, http.StatusOK, a.uiSnapshotFor(a.authorized(r)))
	})
	mux.HandleFunc("/__ui/update/check", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		result, err := a.checkUpdate(r.Context())
		if err != nil {
			writeJSON(w, http.StatusBadGateway, map[string]any{
				"ok":              false,
				"current_version": appVersion,
				"source_url":      a.updateIndexURL,
				"error":           err.Error(),
			})
			return
		}
		writeJSON(w, http.StatusOK, result)
	})
	mux.HandleFunc("/__ui/declaration/decline", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		if !isSameOriginOrNoOrigin(r) {
			writeJSON(w, http.StatusForbidden, map[string]any{"error": "origin_not_allowed"})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"ok": true})
		if a.shutdown != nil {
			go a.shutdown()
		}
	})
	mux.HandleFunc("/__health/ready", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]any{
			"ok":                 true,
			"version":            appVersion,
			"contract_bundle":    contractBundle,
			"run_id":             a.runID,
			"mode":               a.mode,
			"credential_profile": firstNonEmpty(a.creds.ProfileName, "synthetic"),
			"signature_model":    firstNonEmpty(a.creds.SignatureModel, "synthetic-dual-key"),
			"control_url":        a.controlBaseURL,
			"gateway_url":        a.gatewayBaseURL,
		})
	})
	mux.HandleFunc("/__merchant/hosting/callback", a.handleHostingCallback)
	mux.HandleFunc("/__merchant/hosting/confirm", a.handleHostingConfirm)
	mux.HandleFunc("/__merchant/checkout/callback", a.handleHostingCallback)
	mux.HandleFunc("/__merchant/checkout/confirm", a.handleHostingConfirm)
	mux.HandleFunc("/__download/reconciliation/", a.handleReconciliationDownload)
	mux.HandleFunc("/__admin/state", func(w http.ResponseWriter, r *http.Request) {
		if !a.authorized(r) {
			writeJSON(w, http.StatusUnauthorized, map[string]any{"error": "unauthorized"})
			return
		}
		writeJSON(w, http.StatusOK, a.uiSnapshotFor(true))
	})
	mux.HandleFunc("/__admin/session", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		if !a.authorized(r) {
			writeJSON(w, http.StatusUnauthorized, map[string]any{"error": "unauthorized"})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"csrf_token": a.csrfToken,
			"report_dir": a.reportDir,
		})
	})
	mux.HandleFunc("/__admin/report", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		if !a.authorized(r) {
			writeJSON(w, http.StatusUnauthorized, map[string]any{"error": "unauthorized"})
			return
		}
		if !a.validCSRF(r) {
			writeJSON(w, http.StatusForbidden, map[string]any{"error": "csrf_required"})
			return
		}
		if err := a.WriteReport(); err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]any{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"report_dir": a.reportDir})
	})
	mux.HandleFunc("/__admin/credentials/export", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		if !a.authorized(r) {
			writeJSON(w, http.StatusUnauthorized, map[string]any{"error": "unauthorized"})
			return
		}
		if !a.validCSRF(r) {
			writeJSON(w, http.StatusForbidden, map[string]any{"error": "csrf_required"})
			return
		}
		payload := credentialExportPayload(a.creds, a.gatewayBaseURL, a.webhookEndpointKeySnapshot())
		raw, err := json.MarshalIndent(payload, "", "  ")
		if err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]any{"error": err.Error()})
			return
		}
		w.Header().Set("Content-Type", "application/json;charset=utf-8")
		w.Header().Set("Content-Disposition", `attachment; filename="sandbox-credentials.json"`)
		w.Header().Set("Cache-Control", "no-store")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		_, _ = w.Write(append(raw, '\n'))
	})
	mux.HandleFunc("/__admin/webhook-targets", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		if !a.authorized(r) {
			writeJSON(w, http.StatusUnauthorized, map[string]any{"error": "unauthorized"})
			return
		}
		if !a.validCSRF(r) {
			writeJSON(w, http.StatusForbidden, map[string]any{"error": "csrf_required"})
			return
		}
		var payload struct {
			Target string `json:"target"`
		}
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]any{"error": "invalid json"})
			return
		}
		target, err := a.setRuntimeWebhookTarget(payload.Target)
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]any{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"ok":                   true,
			"target":               redactTarget(target),
			"webhook_target_count": len(a.webhookTargetsSnapshot()),
		})
	})
	mux.HandleFunc("/__admin/deliver", a.handleAdminDeliver)
	mux.HandleFunc("/__admin/hosting/success", a.handleAdminHostingSuccess)
	mux.HandleFunc("/__admin/shutdown", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		if !a.validCSRF(r) {
			writeJSON(w, http.StatusForbidden, map[string]any{"error": "csrf_required"})
			return
		}
		if !a.authorized(r) {
			writeJSON(w, http.StatusUnauthorized, map[string]any{"error": "unauthorized"})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{"ok": true})
		if a.shutdown != nil {
			go a.shutdown()
		}
	})
	return withLocalSecurity(recoverPanic(mux))
}

func (a *App) gatewayHandler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/v4/trade/payment/create", a.handleAggregationCreate)
	mux.HandleFunc("/v4/trade/payment/scanpay/query", a.handleAggregationQuery)
	mux.HandleFunc("/v4/trade/payment/scanpay/refund", a.handleAggregationRefund)
	mux.HandleFunc("/v4/trade/payment/scanpay/refundquery", a.handleAggregationRefundQuery)
	mux.HandleFunc("/v2/trade/payment/scanpay/close", a.handleAggregationClose)
	mux.HandleFunc("/v2/trade/payment/scanpay/closequery", a.handleAggregationCloseQuery)
	mux.HandleFunc("/v2/trade/hosting/payment/preorder", a.handleHostingPreorder)
	mux.HandleFunc("/v2/trade/hosting/payment/queryorderinfo", a.handleHostingQuery)
	mux.HandleFunc("/v2/trade/hosting/payment/htRefund", a.handleHostingRefund)
	mux.HandleFunc("/v2/trade/hosting/payment/queryRefundInfo", a.handleHostingRefundQuery)
	mux.HandleFunc("/v2/trade/hosting/payment/close", a.handleHostingClose)
	mux.HandleFunc("/v2/trade/hosting/payment/splitpay/query", a.handleHostingSplitpayQuery)
	mux.HandleFunc("/v2/trade/check/filequery", a.handleReconciliationFileQuery)
	inner := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Huifu-Sandbox", "true")
		w.Header().Set("X-Huifu-Sandbox-Version", appVersion)
		w.Header().Set("X-Huifu-Contract-Bundle", contractBundle)
		w.Header().Set("X-Huifu-Sandbox-Mode", a.mode)
		w.Header().Set("X-Huifu-Sandbox-Credential-Profile", firstNonEmpty(a.creds.ProfileName, "synthetic"))
		w.Header().Set("X-Huifu-Sandbox-Signature-Model", firstNonEmpty(a.creds.SignatureModel, "synthetic-dual-key"))
		if a.mode == "official-proxy" {
			a.handleOfficialProxy(w, r)
			return
		}
		mux.ServeHTTP(w, r)
	})
	return a.gatewayLogMiddleware(recoverPanic(inner))
}

const (
	maxGatewayRequestLogs  = 200
	maxGatewayRequestBody  = 2 << 20
	maxCapturedResponseLog = 1 << 20
	maxPlainResponseLog    = 4096
	maxGatewayLogString    = 2048
	maxGatewayLogMapKeys   = 80
	maxGatewayLogArray     = 40
	maxGatewayLogDepth     = 6
)

type gatewaySignatureStatusContextKey struct{}

type gatewayCaptureWriter struct {
	http.ResponseWriter
	status      int
	wroteHeader bool
	body        bytes.Buffer
}

func (w *gatewayCaptureWriter) WriteHeader(status int) {
	if w.wroteHeader {
		return
	}
	w.status = status
	w.wroteHeader = true
	w.ResponseWriter.WriteHeader(status)
}

func (w *gatewayCaptureWriter) Write(b []byte) (int, error) {
	if !w.wroteHeader {
		w.status = http.StatusOK
		w.wroteHeader = true
	}
	if remaining := maxCapturedResponseLog - w.body.Len(); remaining > 0 {
		if len(b) > remaining {
			_, _ = w.body.Write(b[:remaining])
		} else {
			_, _ = w.body.Write(b)
		}
	}
	return w.ResponseWriter.Write(b)
}

func (w *gatewayCaptureWriter) statusCode() int {
	if w.status == 0 {
		return http.StatusOK
	}
	return w.status
}

func (a *App) gatewayLogMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			next.ServeHTTP(w, r)
			return
		}
		raw, err := io.ReadAll(http.MaxBytesReader(w, r.Body, maxGatewayRequestBody))
		if err != nil {
			http.Error(w, "request body too large or unreadable", http.StatusRequestEntityTooLarge)
			return
		}
		r.Body = io.NopCloser(bytes.NewReader(raw))
		capture := &gatewayCaptureWriter{ResponseWriter: w}
		next.ServeHTTP(capture, r)
		a.recordGatewayRequestLog(r, raw, capture.statusCode(), capture.body.Bytes())
	})
}

func (a *App) recordGatewayRequestLog(r *http.Request, rawRequest []byte, httpStatus int, rawResponse []byte) {
	path := ""
	if r.URL != nil {
		path = r.URL.Path
	}
	signatureStatus := gatewayLogSignatureStatus(r)
	requestVerified := signatureStatus == "verified"
	log := RequestLog{
		Time:              time.Now().UTC().Format(time.RFC3339Nano),
		Method:            r.Method,
		Path:              path,
		Kind:              gatewayLogKind(path),
		HTTPStatus:        httpStatus,
		SignatureStatus:   signatureStatus,
		RequestDataStatus: "unavailable",
	}

	var env Envelope
	if err := json.Unmarshal(rawRequest, &env); err == nil {
		log.SysID = env.SysID
		log.ProductID = env.ProductID
		log.RequestEnvelope = requestEnvelopeSummary(env, rawRequest)
		if env.Sign == "" || env.Data == nil {
			log.SignatureStatus = "invalid_envelope"
			log.RequestDataStatus = "omitted_invalid_envelope"
		} else if requestVerified {
			log.HuifuID = stringValue(env.Data["huifu_id"])
			log.ReqSeqID = firstNonEmpty(stringValue(env.Data["req_seq_id"]), stringValue(env.Data["org_req_seq_id"]))
			log.RequestData = sanitizeGatewayLogMap(env.Data)
			log.RequestDataStatus = "captured_verified"
		} else {
			log.RequestDataStatus = "omitted_unverified"
		}
	} else {
		log.SignatureStatus = "invalid_envelope"
		log.RequestDataStatus = "omitted_invalid_json"
		log.RequestEnvelope = invalidRequestEnvelopeSummary(rawRequest, err)
	}

	var signed SignedResponse
	if err := json.Unmarshal(rawResponse, &signed); err == nil && signed.Data != nil {
		log.ResponseData = sanitizeGatewayLogMap(signed.Data)
		log.ResponseEnvelope = responseEnvelopeSummary(signed, rawResponse)
		log.RespCode = stringValue(signed.Data["resp_code"])
		log.RespDesc = stringValue(signed.Data["resp_desc"])
		if requestVerified && log.ReqSeqID == "" {
			log.ReqSeqID = firstNonEmpty(stringValue(signed.Data["req_seq_id"]), stringValue(signed.Data["org_req_seq_id"]))
		}
		if requestVerified && log.HuifuID == "" {
			log.HuifuID = stringValue(signed.Data["huifu_id"])
		}
		if log.SignatureStatus == "" {
			log.SignatureStatus = gatewaySignatureStatus(log.RespCode)
		}
	} else if len(rawResponse) > 0 {
		log.ResponseBody = sanitizePlainLogText(string(rawResponse))
		log.ResponseEnvelope = plainResponseSummary(rawResponse)
		if log.SignatureStatus == "" {
			log.SignatureStatus = "not_verified"
		}
	} else {
		log.ResponseEnvelope = map[string]any{"status": "empty_response", "body_size_bytes": 0}
	}
	if log.SignatureStatus == "" {
		log.SignatureStatus = "unknown"
	}

	a.mu.Lock()
	a.requestLogSeq++
	log.ID = fmt.Sprintf("REQLOG-%06d", a.requestLogSeq)
	a.requestLogs = append(a.requestLogs, log)
	if len(a.requestLogs) > maxGatewayRequestLogs {
		a.requestLogs = append([]RequestLog(nil), a.requestLogs[len(a.requestLogs)-maxGatewayRequestLogs:]...)
	}
	a.mu.Unlock()
}

func requestEnvelopeSummary(env Envelope, raw []byte) map[string]any {
	summary := map[string]any{
		"status":          "parsed",
		"body_sha256":     bodyDigest(raw),
		"body_size_bytes": len(raw),
	}
	missing := make([]string, 0, 4)
	if env.SysID != "" {
		summary["sys_id"] = env.SysID
	} else {
		missing = append(missing, "sys_id")
	}
	if env.ProductID != "" {
		summary["product_id"] = env.ProductID
	} else {
		missing = append(missing, "product_id")
	}
	if env.Sign != "" {
		summary["sign_status"] = "present"
		summary["sign_sha256"] = signatureDigest(env.Sign)
		summary["sign_length"] = len(env.Sign)
	} else {
		summary["sign_status"] = "missing"
		missing = append(missing, "sign")
	}
	if env.Data != nil {
		summary["data_status"] = "present"
		summary["data_field_count"] = len(env.Data)
		summary["data_keys"] = limitedMapKeys(env.Data, maxGatewayLogMapKeys)
	} else {
		summary["data_status"] = "missing"
		missing = append(missing, "data")
	}
	if len(missing) > 0 {
		summary["status"] = "invalid_envelope"
		summary["missing_fields"] = missing
	}
	return summary
}

func invalidRequestEnvelopeSummary(raw []byte, err error) map[string]any {
	summary := map[string]any{
		"status":          "invalid_json",
		"body_sha256":     bodyDigest(raw),
		"body_size_bytes": len(raw),
	}
	if err != nil {
		summary["parse_error"] = sanitizePlainLogText(err.Error())
	}
	return summary
}

func responseEnvelopeSummary(signed SignedResponse, raw []byte) map[string]any {
	summary := map[string]any{
		"status":          "signed_response",
		"body_sha256":     bodyDigest(raw),
		"body_size_bytes": len(raw),
	}
	if signed.Sign != "" {
		summary["sign_status"] = "present"
		summary["sign_sha256"] = signatureDigest(signed.Sign)
		summary["sign_length"] = len(signed.Sign)
	} else {
		summary["sign_status"] = "missing"
	}
	if signed.Data != nil {
		summary["data_status"] = "present"
		summary["data_field_count"] = len(signed.Data)
		summary["data_keys"] = limitedMapKeys(signed.Data, maxGatewayLogMapKeys)
	} else {
		summary["data_status"] = "missing"
	}
	return summary
}

func plainResponseSummary(raw []byte) map[string]any {
	return map[string]any{
		"status":          "plain_or_invalid_json_response",
		"body_sha256":     bodyDigest(raw),
		"body_size_bytes": len(raw),
	}
}

func gatewaySignatureStatus(respCode string) string {
	switch respCode {
	case "LS000001", "LS000002", "LS000008":
		return "not_verified"
	case "LS000003":
		return "failed"
	default:
		return "verified"
	}
}

func markGatewaySignatureStatus(r *http.Request, status string) {
	if r == nil || status == "" {
		return
	}
	*r = *r.WithContext(context.WithValue(r.Context(), gatewaySignatureStatusContextKey{}, status))
}

func gatewayLogSignatureStatus(r *http.Request) string {
	if r == nil {
		return ""
	}
	if status, ok := r.Context().Value(gatewaySignatureStatusContextKey{}).(string); ok {
		return status
	}
	return ""
}

func gatewayLogKind(path string) string {
	switch {
	case strings.Contains(path, "splitpay/query"):
		return "拆单查询"
	case strings.Contains(path, "refundquery") || strings.Contains(path, "queryRefundInfo"):
		return "退款查询"
	case strings.Contains(path, "refund") || strings.Contains(path, "htRefund"):
		return "退款"
	case strings.Contains(path, "closequery"):
		return "关单查询"
	case strings.Contains(path, "close"):
		return "关单"
	case strings.Contains(path, "queryorderinfo"):
		return "托管查单"
	case strings.Contains(path, "scanpay/query"):
		return "聚合查单"
	case strings.Contains(path, "preorder"):
		return "托管预下单"
	case strings.Contains(path, "payment/create"):
		return "聚合支付下单"
	case strings.Contains(path, "filequery"):
		return "对账文件查询"
	default:
		return "网关请求"
	}
}

func sanitizeGatewayLogMap(in map[string]any) map[string]any {
	return sanitizeGatewayLogMapDepth(in, 0)
}

func sanitizeGatewayLogMapDepth(in map[string]any, depth int) map[string]any {
	if len(in) == 0 {
		return nil
	}
	if depth >= maxGatewayLogDepth {
		return map[string]any{"_omitted": "max_depth_exceeded"}
	}
	keys := limitedMapKeys(in, maxGatewayLogMapKeys)
	out := make(map[string]any, len(keys))
	for _, key := range keys {
		out[key] = sanitizeGatewayLogValue(key, in[key], depth)
	}
	if len(in) > len(keys) {
		out["_omitted_keys"] = len(in) - len(keys)
	}
	return out
}

func sanitizeGatewayLogValue(key string, value any, depth int) any {
	if sensitiveLogKey(key) {
		return "[REDACTED]"
	}
	switch typed := value.(type) {
	case string:
		typed = sanitizePlainLogText(typed)
		if strings.Contains(typed, "://") {
			return redactTarget(typed)
		}
		if len(typed) > maxGatewayLogString {
			return typed[:maxGatewayLogString] + "...[truncated]"
		}
		return typed
	case map[string]any:
		return sanitizeGatewayLogMapDepth(typed, depth+1)
	case []any:
		limit := len(typed)
		if limit > maxGatewayLogArray {
			limit = maxGatewayLogArray
		}
		out := make([]any, limit)
		for i := 0; i < limit; i++ {
			out[i] = sanitizeGatewayLogValue("", typed[i], depth+1)
		}
		if len(typed) > limit {
			out = append(out, fmt.Sprintf("...[%d items omitted]", len(typed)-limit))
		}
		return out
	default:
		return typed
	}
}

func sensitiveLogKey(key string) bool {
	lower := strings.ToLower(key)
	return lower == "sign" ||
		strings.Contains(lower, "private_key") ||
		strings.Contains(lower, "secret") ||
		strings.Contains(lower, "password") ||
		strings.Contains(lower, "access_token") ||
		strings.Contains(lower, "api_key") ||
		strings.Contains(lower, "openid") ||
		strings.Contains(lower, "user_id") ||
		strings.Contains(lower, "buyer_id") ||
		strings.Contains(lower, "payer_id") ||
		strings.Contains(lower, "mobile") ||
		strings.Contains(lower, "phone") ||
		strings.Contains(lower, "card_no") ||
		strings.Contains(lower, "bank_card") ||
		strings.Contains(lower, "cert") ||
		strings.Contains(lower, "id_card")
}

func limitedMapKeys(in map[string]any, limit int) []string {
	keys := mapKeys(in)
	if limit > 0 && len(keys) > limit {
		keys = keys[:limit]
	}
	return keys
}

func sanitizePlainLogText(value string) string {
	value = trimPlainResponseLog(value)
	value = sanitizeEmbeddedTargets(value)
	if plainLogTextSensitive(value) {
		return "[REDACTED]"
	}
	return value
}

func plainLogTextSensitive(value string) bool {
	lower := strings.ToLower(value)
	for _, marker := range []string{
		"private_key",
		"secret",
		"password",
		"access_token",
		"api_key",
		"token=",
		"token:",
		"sign=",
		"authorization:",
		"bearer ",
		"-----begin private key-----",
		"-----begin rsa private key-----",
		"-----begin ec private key-----",
		"-----begin encrypted private key-----",
		"-----begin openssh private key-----",
		"-----begin certificate-----",
		"-----begin public key-----",
		"-----begin rsa public key-----",
	} {
		if strings.Contains(lower, marker) {
			return true
		}
	}
	return false
}

func sanitizeEmbeddedTargets(value string) string {
	var out strings.Builder
	for {
		start := embeddedTargetStart(value)
		if start < 0 {
			out.WriteString(value)
			break
		}
		out.WriteString(value[:start])
		rest := value[start:]
		end := embeddedTargetEnd(rest)
		out.WriteString(redactTarget(rest[:end]))
		value = rest[end:]
	}
	return out.String()
}

func embeddedTargetStart(value string) int {
	httpIndex := strings.Index(value, "http://")
	httpsIndex := strings.Index(value, "https://")
	if httpIndex < 0 {
		return httpsIndex
	}
	if httpsIndex < 0 || httpIndex < httpsIndex {
		return httpIndex
	}
	return httpsIndex
}

func embeddedTargetEnd(value string) int {
	for index, r := range value {
		if index == 0 {
			continue
		}
		if r <= ' ' || strings.ContainsRune("\"'<>[]{}(),", r) {
			return index
		}
	}
	return len(value)
}

func bodyDigest(raw []byte) string {
	sum := sha256.Sum256(raw)
	return "sha256:" + base64.RawURLEncoding.EncodeToString(sum[:])[:24]
}

func signatureDigest(value string) string {
	if value == "" {
		return ""
	}
	sum := sha256.Sum256([]byte(value))
	return "sha256:" + base64.RawURLEncoding.EncodeToString(sum[:])[:24]
}

func trimPlainResponseLog(value string) string {
	value = strings.TrimSpace(value)
	if len(value) <= maxPlainResponseLog {
		return value
	}
	return value[:maxPlainResponseLog] + "...[truncated]"
}

func (a *App) authorized(r *http.Request) bool {
	if a.adminDisabled || a.adminToken == "" {
		return false
	}
	got := r.Header.Get("Authorization")
	want := "Bearer " + a.adminToken
	return subtle.ConstantTimeCompare([]byte(got), []byte(want)) == 1
}

func (a *App) validCSRF(r *http.Request) bool {
	return subtle.ConstantTimeCompare([]byte(r.Header.Get("X-Huifu-Sandbox-CSRF")), []byte(a.csrfToken)) == 1
}

func withLocalSecurity(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		host := r.Host
		if strings.Contains(host, ":") {
			h, _, err := net.SplitHostPort(host)
			if err == nil {
				host = h
			}
		}
		if host != "127.0.0.1" && host != "localhost" && host != "[::1]" && host != "::1" {
			writeJSON(w, http.StatusForbidden, map[string]any{"error": "host_not_allowed"})
			return
		}
		if origin := r.Header.Get("Origin"); origin != "" && !isAllowedLocalOrigin(origin) {
			writeJSON(w, http.StatusForbidden, map[string]any{"error": "origin_not_allowed"})
			return
		}
		next.ServeHTTP(w, r)
	})
}

// recoverPanic 捕获 handler panic，记录安全事件并返回签名错误封套，避免单个请求 panic 断开连接。
func recoverPanic(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if rec := recover(); rec != nil {
				writeJSON(w, http.StatusInternalServerError, map[string]any{"error": "internal_panic_recovered"})
			}
		}()
		next.ServeHTTP(w, r)
	})
}

func (a *App) handleAggregationCreate(w http.ResponseWriter, r *http.Request) {
	env, ok := a.readGatewayEnvelope(w, r, "/v4/trade/payment/create")
	if !ok {
		return
	}
	required := []string{"req_seq_id", "huifu_id", "trade_type", "trans_amt", "goods_desc"}
	if missing := missingFields(env.Data, required); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	reqDate := stringValue(env.Data["req_date"])
	if reqDate == "" {
		reqDate = nowDate()
	}
	reqSeqID := stringValue(env.Data["req_seq_id"])
	businessVariant, txMetadata, channelResponse, err := aggregationBusinessFields(env.Data)
	if err != nil {
		var bizErr businessValidationError
		if errors.As(err, &bizErr) {
			a.writeGatewayData(w, localError(bizErr.code, bizErr.msg))
			return
		}
		a.writeGatewayData(w, localError("LS000005", err.Error()))
		return
	}
	digest, err := dataDigest(env.Data)
	if err != nil {
		a.writeGatewayData(w, localError("LS000005", "request digest failed"))
		return
	}
	if a.handleAggregationIdempotency(w, r, reqSeqID, digest) {
		return
	}
	transAmtFen, err := parseAmountFen(stringValue(env.Data["trans_amt"]))
	if err != nil {
		a.writeGatewayData(w, localError("LS000005", "invalid trans_amt: "+err.Error()))
		return
	}
	hfSeqID := nextID("HF")
	initialState := aggregationInitialState(stringValue(env.Data["trade_type"]))
	payment := &Payment{
		Kind: "aggregation", HuifuID: stringValue(env.Data["huifu_id"]), ReqDate: reqDate,
		ReqSeqID: reqSeqID, HFSeqID: hfSeqID, TradeType: stringValue(env.Data["trade_type"]),
		TransAmt: stringValue(env.Data["trans_amt"]), TransAmtFen: transAmtFen, GoodsDesc: stringValue(env.Data["goods_desc"]),
		NotifyURL: stringValue(env.Data["notify_url"]), RequestDigest: digest, State: initialState,
		RefundedAmt: "0.00", RefundedFen: 0, RefundableAmt: formatFen(transAmtFen), RefundableFen: transAmtFen,
		BusinessVariant: businessVariant, TxMetadata: txMetadata, ChannelResponse: channelResponse,
	}
	a.mu.Lock()
	a.payments[reqSeqID] = payment
	a.hfIndex[hfSeqID] = reqSeqID
	pc := *payment
	a.mu.Unlock()
	a.record("payment.accepted", r.URL.Path, reqSeqID, map[string]any{"kind": "aggregation", "state": initialState, "business_variant": businessVariant})
	if businessVariant != "" && businessVariant != "aggregation.generic" {
		a.record("business.variant", r.URL.Path, reqSeqID, map[string]any{"variant": businessVariant})
	}
	respCode, respDesc := aggregationCreateResp(pc.TradeType)
	a.writeGatewayData(w, addPaymentCreateExtensions(map[string]any{
		"resp_code":      respCode,
		"resp_desc":      respDesc,
		"req_date":       reqDate,
		"req_seq_id":     reqSeqID,
		"huifu_id":       pc.HuifuID,
		"hf_seq_id":      hfSeqID,
		"out_ord_id":     aggregationOutOrdID(pc),
		"party_order_id": aggregationPartyOrderID(pc),
		"trade_type":     pc.TradeType,
		"trans_amt":      pc.TransAmt,
		"trans_stat":     initialState,
		"qr_code":        "https://local-sandbox.invalid/pay/" + reqSeqID,
	}, pc))
}

func (a *App) handleAggregationQuery(w http.ResponseWriter, r *http.Request) {
	env, ok := a.readGatewayEnvelope(w, r, "/v4/trade/payment/scanpay/query")
	if !ok {
		return
	}
	if missing := missingFields(env.Data, []string{"huifu_id"}); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	payment, err := a.findAggregationPayment(env.Data)
	if err != nil {
		a.writeGatewayData(w, localError("LS000004", err.Error()))
		return
	}
	a.mu.Lock()
	payment.QueryCount++
	if payment.QueryCount >= 2 {
		payment.State = "S"
	}
	pc := *payment
	a.mu.Unlock()
	state := pc.State
	count := pc.QueryCount
	a.record("payment.query", r.URL.Path, pc.ReqSeqID, map[string]any{"kind": "aggregation", "state": state, "query_count": count})
	if state == "S" {
		a.maybeNotifyPayment(pc.ReqSeqID)
		a.maybeWebhookPayment(pc.ReqSeqID)
	}
	a.writeGatewayData(w, addAggregationQueryExtensions(map[string]any{
		"resp_code":      "00000000",
		"resp_desc":      "查询成功",
		"huifu_id":       pc.HuifuID,
		"req_date":       pc.ReqDate,
		"req_seq_id":     pc.ReqSeqID,
		"hf_seq_id":      pc.HFSeqID,
		"out_ord_id":     aggregationOutOrdID(pc),
		"party_order_id": aggregationPartyOrderID(pc),
		"trade_type":     pc.TradeType,
		"trans_amt":      pc.TransAmt,
		"goods_desc":     pc.GoodsDesc,
		"trans_stat":     state,
	}, pc))
}

func (a *App) handleHostingPreorder(w http.ResponseWriter, r *http.Request) {
	env, ok := a.readGatewayEnvelope(w, r, "/v2/trade/hosting/payment/preorder")
	if !ok {
		return
	}
	required := []string{"req_date", "req_seq_id", "huifu_id", "trans_amt", "goods_desc", "pre_order_type"}
	if missing := missingFields(env.Data, required); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	preOrderType := stringValue(env.Data["pre_order_type"])
	hostingDataRaw := stringValue(env.Data["hosting_data"])
	if hostingDataRaw == "" {
		if preOrderType != "4" {
			a.writeGatewayData(w, localError("LS000002", "missing required data: hosting_data"))
			return
		}
	} else {
		hostingData, err := parseJSONStringObject(hostingDataRaw)
		if err != nil {
			a.writeGatewayData(w, localError("LS000005", "hosting_data must be a JSON object string"))
			return
		}
		if missing := missingFields(hostingData, []string{"project_title", "project_id"}); len(missing) > 0 {
			a.writeGatewayData(w, localError("LS000002", "missing hosting_data: "+strings.Join(missing, ",")))
			return
		}
		if stringValue(env.Data["trans_type"]) != "" && stringValue(hostingData["request_type"]) == "" {
			a.writeGatewayData(w, localError("LS000002", "missing hosting_data: request_type"))
			return
		}
	}
	businessVariant, channelResponse, err := hostingBusinessFields(env.Data)
	if err != nil {
		var bizErr businessValidationError
		if errors.As(err, &bizErr) {
			a.writeGatewayData(w, localError(bizErr.code, bizErr.msg))
			return
		}
		a.writeGatewayData(w, localError("LS000005", err.Error()))
		return
	}
	digest, err := dataDigest(env.Data)
	if err != nil {
		a.writeGatewayData(w, localError("LS000005", "request digest failed"))
		return
	}
	if a.handleHostingIdempotency(w, r, stringValue(env.Data["req_seq_id"]), digest, preOrderType) {
		return
	}
	transAmtFen, err := parseAmountFen(stringValue(env.Data["trans_amt"]))
	if err != nil {
		a.writeGatewayData(w, localError("LS000005", "invalid trans_amt: "+err.Error()))
		return
	}
	preOrderID := nextID("PO")
	payment := &Payment{
		Kind: "hosting", HuifuID: stringValue(env.Data["huifu_id"]), ReqDate: stringValue(env.Data["req_date"]),
		ReqSeqID: stringValue(env.Data["req_seq_id"]), HFSeqID: nextID("HF"), PreOrderID: preOrderID, TransAmt: stringValue(env.Data["trans_amt"]), TransAmtFen: transAmtFen,
		GoodsDesc: stringValue(env.Data["goods_desc"]), NotifyURL: stringValue(env.Data["notify_url"]), RequestDigest: digest, State: "P",
		RefundedAmt: "0.00", RefundedFen: 0, RefundableAmt: formatFen(transAmtFen), RefundableFen: transAmtFen,
		PreOrderType: preOrderType, BusinessVariant: businessVariant, ChannelResponse: channelResponse,
	}
	a.mu.Lock()
	a.payments[payment.ReqSeqID] = payment
	a.hfIndex[payment.HFSeqID] = payment.ReqSeqID
	a.preIndex[preOrderID] = payment.ReqSeqID
	pc := *payment
	a.mu.Unlock()
	a.record("payment.accepted", r.URL.Path, pc.ReqSeqID, map[string]any{"kind": "hosting", "state": "P", "pre_order_id": preOrderID, "business_variant": businessVariant})
	if businessVariant != "" && businessVariant != "hosting.h5pc" {
		a.record("business.variant", r.URL.Path, pc.ReqSeqID, map[string]any{"variant": businessVariant})
	}
	a.writeGatewayData(w, addPaymentExtensions(map[string]any{
		"resp_code":      "00000000",
		"resp_desc":      "操作成功",
		"product_id":     env.ProductID,
		"req_date":       pc.ReqDate,
		"req_seq_id":     pc.ReqSeqID,
		"huifu_id":       pc.HuifuID,
		"pre_order_type": preOrderType,
		"pre_order_id":   preOrderID,
		"trans_amt":      pc.TransAmt,
		"current_time":   nowDateTime(),
		"goods_desc":     pc.GoodsDesc,
		"jump_url":       a.hostingPreorderJumpURL(preOrderID, preOrderType, pc.ChannelResponse),
		"order_stat":     hostingOrderStat(pc),
		"trans_stat":     "P",
	}, pc))
}

func (a *App) handleHostingQuery(w http.ResponseWriter, r *http.Request) {
	env, ok := a.readGatewayEnvelope(w, r, "/v2/trade/hosting/payment/queryorderinfo")
	if !ok {
		return
	}
	if missing := missingFields(env.Data, []string{"req_date", "req_seq_id"}); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	payment, err := a.findHostingPayment(env.Data)
	if err != nil {
		a.writeGatewayData(w, localError("LS000004", err.Error()))
		return
	}
	a.mu.Lock()
	payment.QueryCount++
	closeStat := a.advanceHostingCloseLocked(payment.ReqSeqID)
	if closeStat == "S" {
		payment.State = "F"
	} else if payment.HostingConfirmed {
		payment.State = "S"
	}
	pc := *payment
	a.mu.Unlock()
	state := pc.State
	confirmed := pc.HostingConfirmed
	a.record("payment.query", r.URL.Path, pc.ReqSeqID, map[string]any{"kind": "hosting", "state": state, "hosting_confirmed": confirmed, "close_stat": closeStat})
	if state == "S" {
		a.record("hosting.final_state", r.URL.Path, pc.ReqSeqID, map[string]any{"state": state})
		a.maybeNotifyPayment(pc.ReqSeqID)
		a.maybeWebhookPayment(pc.ReqSeqID)
	}
	if closeStat == "S" {
		a.maybeWebhookCloseByPayment("hosting", pc.ReqSeqID)
	}
	resp := map[string]any{
		"resp_code":      "00000000",
		"resp_desc":      "操作成功",
		"product_id":     env.ProductID,
		"req_date":       stringValue(env.Data["req_date"]),
		"req_seq_id":     stringValue(env.Data["req_seq_id"]),
		"huifu_id":       pc.HuifuID,
		"org_req_date":   pc.ReqDate,
		"org_req_seq_id": pc.ReqSeqID,
		"pre_order_id":   pc.PreOrderID,
		"trans_date":     pc.ReqDate,
		"order_stat":     hostingOrderStat(pc),
		"org_hf_seq_id":  pc.HFSeqID,
		"out_trans_id":   "OUT-" + pc.ReqSeqID,
		"party_order_id": hostingPartyOrderID(pc),
		"trans_stat":     state,
		"close_stat":     closeStat,
		"pay_type":       hostingQueryPayType(pc),
		"trans_amt":      pc.TransAmt,
		"fee_flag":       2,
		"trans_time":     pc.ReqDate + "120000",
		"fee_amt":        hostingQueryFeeAmount(pc),
		"ref_amt":        "0.00",
		"bank_code":      hostingQueryBankCode(pc),
		"bank_desc":      hostingQueryBankDesc(pc),
		"is_div":         hostingQueryDivFlag(pc),
		"is_delay_acct":  "N",
		"large_pay_data": compactJSONString(map[string]any{"in_acct_flag": ""}),
		"goods_desc":     pc.GoodsDesc,
	}
	if closeStat != "" {
		resp["org_trans_stat"] = state
	}
	a.writeGatewayData(w, addPaymentExtensions(resp, pc))
}

func (a *App) handleHostingCallback(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet && r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	preOrderID := r.URL.Query().Get("pre_order_id")
	reqSeqID := r.URL.Query().Get("req_seq_id")
	payment, ok := a.findHostingCallbackPayment(preOrderID, reqSeqID)
	if !ok {
		writeJSON(w, http.StatusNotFound, map[string]any{"error": "unknown hosting order"})
		return
	}
	a.mu.Lock()
	if stored := a.payments[payment.ReqSeqID]; stored != nil {
		stored.HostingCallbackSeen = true
		payment = *stored
	}
	a.mu.Unlock()
	a.record("hosting.callback", r.URL.Path, payment.ReqSeqID, map[string]any{
		"pre_order_id":             payment.PreOrderID,
		"state":                    payment.State,
		"terminal_state_unchanged": true,
	})
	writeJSON(w, http.StatusOK, map[string]any{
		"ok":                       true,
		"req_seq_id":               payment.ReqSeqID,
		"pre_order_id":             payment.PreOrderID,
		"state":                    payment.State,
		"terminal_state_unchanged": true,
	})
}

func (a *App) handleHostingConfirm(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	if !a.validCSRF(r) {
		writeJSON(w, http.StatusForbidden, map[string]any{"error": "csrf_required"})
		return
	}
	preOrderID, reqSeqID, err := readHostingConfirmIDs(r)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]any{"error": err.Error()})
		return
	}
	payment, ok := a.findHostingCallbackPayment(preOrderID, reqSeqID)
	if !ok {
		writeJSON(w, http.StatusNotFound, map[string]any{"error": "unknown hosting order"})
		return
	}
	a.mu.Lock()
	if stored := a.payments[payment.ReqSeqID]; stored != nil {
		stored.HostingConfirmed = true
		stored.ConfirmCount++
		payment = *stored
	}
	a.mu.Unlock()
	a.record("hosting.confirm", r.URL.Path, payment.ReqSeqID, map[string]any{
		"pre_order_id": payment.PreOrderID,
		"state":        payment.State,
		"next":         "queryorderinfo",
	})
	writeJSON(w, http.StatusOK, map[string]any{
		"ok":           true,
		"req_seq_id":   payment.ReqSeqID,
		"pre_order_id": payment.PreOrderID,
		"state":        payment.State,
		"next":         "queryorderinfo",
	})
}

func (a *App) readGatewayEnvelope(w http.ResponseWriter, r *http.Request, endpoint string) (Envelope, bool) {
	env, _, ok := a.readGatewayEnvelopeBytes(w, r, endpoint)
	return env, ok
}

func (a *App) readGatewayEnvelopeBytes(w http.ResponseWriter, r *http.Request, endpoint string) (Envelope, []byte, bool) {
	var env Envelope
	if r.Method != http.MethodPost {
		markGatewaySignatureStatus(r, "not_verified")
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return env, nil, false
	}
	if !strings.Contains(strings.ToLower(r.Header.Get("Content-Type")), "application/json") {
		markGatewaySignatureStatus(r, "not_verified")
		http.Error(w, "Content-Type must be application/json", http.StatusUnsupportedMediaType)
		return env, nil, false
	}
	body, err := io.ReadAll(io.LimitReader(r.Body, 10<<20))
	if err != nil {
		markGatewaySignatureStatus(r, "invalid_envelope")
		http.Error(w, err.Error(), http.StatusBadRequest)
		return env, nil, false
	}
	if err := json.Unmarshal(body, &env); err != nil {
		markGatewaySignatureStatus(r, "invalid_envelope")
		http.Error(w, err.Error(), http.StatusBadRequest)
		return env, nil, false
	}
	if env.SysID == "" || env.ProductID == "" || env.Sign == "" || env.Data == nil {
		markGatewaySignatureStatus(r, "invalid_envelope")
		a.writeGatewayData(w, localError("LS000001", "invalid request envelope"))
		return env, nil, false
	}
	if a.creds.SysID != "" && env.SysID != a.creds.SysID {
		markGatewaySignatureStatus(r, "not_verified")
		a.writeGatewayData(w, localError("LS000008", "sys_id does not match credential profile"))
		return env, nil, false
	}
	if a.creds.ProductID != "" && env.ProductID != a.creds.ProductID {
		markGatewaySignatureStatus(r, "not_verified")
		a.writeGatewayData(w, localError("LS000008", "product_id does not match credential profile"))
		return env, nil, false
	}
	if r.Header.Get("jpt-x-skill-source") == "" {
		markGatewaySignatureStatus(r, "not_verified")
		a.writeGatewayData(w, localError("LS000002", "missing jpt-x-skill-source header"))
		return env, nil, false
	}
	if huifuID := stringValue(env.Data["huifu_id"]); huifuID != "" && r.Header.Get("jpt-x-skill-huifu_id") != huifuID {
		markGatewaySignatureStatus(r, "not_verified")
		a.writeGatewayData(w, localError("LS000002", "jpt-x-skill-huifu_id must equal data.huifu_id"))
		return env, nil, false
	}
	if err := verifyData(env.Data, env.Sign, a.creds.MerchantPublic); err != nil {
		markGatewaySignatureStatus(r, "failed")
		a.record("signature.invalid", endpoint, "", map[string]any{"error": err.Error()})
		a.writeGatewayData(w, localError("LS000003", "invalid request signature"))
		return env, nil, false
	}
	markGatewaySignatureStatus(r, "verified")
	if a.applyGatewayFault(w, r, env, endpoint) {
		return env, nil, false
	}
	return env, body, true
}

func (a *App) handleOfficialProxy(w http.ResponseWriter, r *http.Request) {
	env, body, ok := a.readGatewayEnvelopeBytes(w, r, r.URL.Path)
	if !ok {
		return
	}
	target := strings.TrimRight(a.officialGateway, "/") + r.URL.RequestURI()
	req, err := http.NewRequestWithContext(r.Context(), r.Method, target, bytes.NewReader(body))
	if err != nil {
		a.writeGatewayData(w, localError("LS900001", "official proxy request build failed"))
		return
	}
	copyProxyHeaders(req.Header, r.Header)
	resp, err := a.httpClient.Do(req)
	if err != nil {
		a.record("official_proxy.error", r.URL.Path, stringValue(env.Data["req_seq_id"]), map[string]any{"error": err.Error()})
		a.writeGatewayData(w, localError("LS900002", "official proxy request failed"))
		return
	}
	defer resp.Body.Close()
	raw, readErr := io.ReadAll(io.LimitReader(resp.Body, 10<<20))
	if readErr != nil {
		a.writeGatewayData(w, localError("LS900003", "official proxy response read failed"))
		return
	}
	a.record("official_proxy.response", r.URL.Path, stringValue(env.Data["req_seq_id"]), map[string]any{
		"http_status":     resp.StatusCode,
		"signature_model": "official_proxy_passthrough",
		"profile":         firstNonEmpty(a.creds.ProfileName, "synthetic"),
	})
	copyResponseHeaders(w.Header(), resp.Header)
	w.WriteHeader(resp.StatusCode)
	_, _ = w.Write(raw)
}

func copyProxyHeaders(dst, src http.Header) {
	for key, values := range src {
		if isHopByHopHeader(key) || strings.EqualFold(key, "Host") {
			continue
		}
		for _, value := range values {
			dst.Add(key, value)
		}
	}
}

func copyResponseHeaders(dst, src http.Header) {
	for key, values := range src {
		if isHopByHopHeader(key) {
			continue
		}
		for _, value := range values {
			dst.Add(key, value)
		}
	}
}

func isHopByHopHeader(key string) bool {
	switch strings.ToLower(key) {
	case "connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailer", "transfer-encoding", "upgrade":
		return true
	default:
		return false
	}
}

func (a *App) applyGatewayFault(w http.ResponseWriter, r *http.Request, env Envelope, endpoint string) bool {
	scenario := strings.ToUpper(strings.TrimSpace(r.Header.Get("jpt-x-sandbox-scenario")))
	if scenario == "" {
		scenario = strings.ToUpper(strings.TrimSpace(stringValue(env.Data["sandbox_scenario"])))
	}
	if scenario == "" {
		return false
	}
	details := map[string]any{"scenario": scenario}
	switch scenario {
	case "FAULT-500", "HTTP-500", "500":
		a.record("fault.injected", endpoint, stringValue(env.Data["req_seq_id"]), details)
		http.Error(w, "local sandbox injected HTTP 500", http.StatusInternalServerError)
		return true
	case "FAULT-TIMEOUT", "TIMEOUT":
		a.record("fault.injected", endpoint, stringValue(env.Data["req_seq_id"]), details)
		if a.faultTimeoutDelay > 0 {
			time.Sleep(a.faultTimeoutDelay)
		}
		http.Error(w, "local sandbox injected timeout", http.StatusGatewayTimeout)
		return true
	case "FAULT-BUSINESS-FAIL", "BUSINESS-FAIL", "BUSINESS_FAIL":
		a.record("fault.injected", endpoint, stringValue(env.Data["req_seq_id"]), details)
		a.writeGatewayData(w, localError("LS200001", "injected business failure"))
		return true
	default:
		if strings.HasPrefix(scenario, "RECON_") {
			return false
		}
		a.writeGatewayData(w, localError("LS000007", "unknown sandbox scenario "+scenario))
		return true
	}
}

func (a *App) writeGatewayData(w http.ResponseWriter, data map[string]any) {
	signature, err := signData(data, a.creds.GatewayPrivate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, SignedResponse{Sign: signature, Data: data})
}

func (a *App) handleAggregationIdempotency(w http.ResponseWriter, r *http.Request, reqSeqID, digest string) bool {
	a.mu.Lock()
	existing := a.payments[reqSeqID]
	if existing == nil {
		a.mu.Unlock()
		return false
	}
	copy := *existing
	a.mu.Unlock()
	if copy.RequestDigest != digest {
		a.record("idempotency.conflict", r.URL.Path, reqSeqID, map[string]any{
			"kind": "aggregation",
			"want": copy.RequestDigest,
			"got":  digest,
		})
		a.writeGatewayData(w, localError("LS000006", "idempotency conflict: same req_seq_id with different payload"))
		return true
	}
	a.record("payment.idempotent_replay", r.URL.Path, reqSeqID, map[string]any{"kind": "aggregation", "state": copy.State})
	a.writeGatewayData(w, addPaymentExtensions(map[string]any{
		"resp_code":  "00000000",
		"resp_desc":  "idempotent replay",
		"req_date":   copy.ReqDate,
		"req_seq_id": copy.ReqSeqID,
		"huifu_id":   copy.HuifuID,
		"hf_seq_id":  copy.HFSeqID,
		"trans_stat": copy.State,
		"qr_code":    "https://local-sandbox.invalid/pay/" + copy.ReqSeqID,
	}, copy))
	return true
}

func (a *App) handleHostingIdempotency(w http.ResponseWriter, r *http.Request, reqSeqID, digest, preOrderType string) bool {
	a.mu.Lock()
	existing := a.payments[reqSeqID]
	if existing == nil {
		a.mu.Unlock()
		return false
	}
	copy := *existing
	a.mu.Unlock()
	if copy.RequestDigest != digest {
		a.record("idempotency.conflict", r.URL.Path, reqSeqID, map[string]any{
			"kind": "hosting",
			"want": copy.RequestDigest,
			"got":  digest,
		})
		a.writeGatewayData(w, localError("LS000006", "idempotency conflict: same req_seq_id with different payload"))
		return true
	}
	a.record("payment.idempotent_replay", r.URL.Path, reqSeqID, map[string]any{"kind": "hosting", "state": copy.State})
	a.writeGatewayData(w, addPaymentExtensions(map[string]any{
		"resp_code":      "00000000",
		"resp_desc":      "idempotent replay",
		"req_date":       copy.ReqDate,
		"req_seq_id":     copy.ReqSeqID,
		"huifu_id":       copy.HuifuID,
		"pre_order_type": preOrderType,
		"pre_order_id":   copy.PreOrderID,
		"jump_url":       a.hostingPreorderJumpURL(copy.PreOrderID, preOrderType, copy.ChannelResponse),
		"trans_stat":     copy.State,
	}, copy))
	return true
}

func (a *App) findAggregationPayment(data map[string]any) (*Payment, error) {
	a.mu.Lock()
	defer a.mu.Unlock()
	if hfSeqID := stringValue(data["hf_seq_id"]); hfSeqID != "" {
		if reqSeqID, ok := a.hfIndex[hfSeqID]; ok {
			return a.payments[reqSeqID], nil
		}
		return nil, errors.New("unknown hf_seq_id")
	}
	if outOrdID := stringValue(data["out_ord_id"]); outOrdID != "" {
		for _, payment := range a.payments {
			if payment != nil && payment.Kind == "aggregation" && aggregationOutOrdID(*payment) == outOrdID {
				return payment, nil
			}
		}
		return nil, errors.New("unknown out_ord_id")
	}
	reqSeqID := stringValue(data["req_seq_id"])
	reqDate := stringValue(data["req_date"])
	if reqSeqID == "" || reqDate == "" {
		return nil, errors.New("query requires out_ord_id, hf_seq_id, or req_date + req_seq_id")
	}
	payment, ok := a.payments[reqSeqID]
	if !ok || payment.ReqDate != reqDate {
		return nil, errors.New("unknown req_date + req_seq_id")
	}
	return payment, nil
}

func (a *App) findHostingPayment(data map[string]any) (*Payment, error) {
	a.mu.Lock()
	defer a.mu.Unlock()
	if partyOrderID := stringValue(data["party_order_id"]); partyOrderID != "" {
		reqSeqID, err := a.findHostingPaymentByPartyOrderIDLocked(partyOrderID)
		if err != nil {
			return nil, err
		}
		return a.payments[reqSeqID], nil
	}
	reqSeqID := stringValue(data["org_req_seq_id"])
	reqDate := stringValue(data["org_req_date"])
	huifuID := stringValue(data["huifu_id"])
	if reqSeqID == "" || reqDate == "" || huifuID == "" {
		return nil, errors.New("query requires party_order_id or huifu_id + org_req_date + org_req_seq_id")
	}
	payment, ok := a.payments[reqSeqID]
	if !ok || payment.ReqDate != reqDate || payment.HuifuID != huifuID {
		return nil, errors.New("unknown org_req_date + org_req_seq_id")
	}
	return payment, nil
}

func startHTTPServer(ctx context.Context, host string, port int, handler http.Handler) (*http.Server, net.Listener, error) {
	ln, err := net.Listen("tcp", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		return nil, nil, err
	}
	srv := &http.Server{Handler: handler, ReadHeaderTimeout: 5 * time.Second, ReadTimeout: 30 * time.Second, WriteTimeout: 30 * time.Second, IdleTimeout: 60 * time.Second}
	go func() {
		<-ctx.Done()
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		_ = srv.Shutdown(shutdownCtx)
	}()
	go func() {
		if err := srv.Serve(ln); err != nil && !errors.Is(err, http.ErrServerClosed) {
			panic(err)
		}
	}()
	return srv, ln, nil
}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json;charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(value)
}

func localError(code, desc string) map[string]any {
	return map[string]any{
		"resp_code": code,
		"resp_desc": "[LOCAL-SANDBOX] " + desc,
	}
}

func missingFields(data map[string]any, fields []string) []string {
	var missing []string
	for _, field := range fields {
		if stringValue(data[field]) == "" {
			missing = append(missing, field)
		}
	}
	return missing
}

func parseJSONStringObject(raw string) (map[string]any, error) {
	var out map[string]any
	if err := json.Unmarshal([]byte(raw), &out); err != nil {
		return nil, err
	}
	if out == nil {
		return nil, errors.New("not object")
	}
	return out, nil
}

func (a *App) hostingJumpURL(preOrderID string) string {
	base := a.controlBaseURL
	if base == "" {
		base = "http://127.0.0.1"
	}
	return strings.TrimRight(base, "/") + "/__merchant/hosting/callback?pre_order_id=" + url.QueryEscape(preOrderID)
}

func (a *App) hostingPreorderJumpURL(preOrderID, preOrderType string, channelResponse map[string]any) string {
	switch preOrderType {
	case "2":
		appSchema := "https://example.invalid/alipay-mini/callback"
		if appData, err := parseJSONStringObject(stringValue(channelResponse["app_data"])); err == nil {
			if value := stringValue(appData["app_schema"]); value != "" {
				appSchema = value
			}
		}
		page := "pages/cashier/cashier?p=" + preOrderID + "&s=app"
		return "alipays://platformapi/startapp?appId=ALIAPP-LOCAL-SANDBOX&thirdPartSchema=" + url.QueryEscape(appSchema) + "&page=" + url.QueryEscape(page) + "&bank_switch=Y"
	case "3":
		return "&bank_switch=Y"
	case "4":
		return "https://cashier.ulpay.com/bytepay-cashdesk/bytepay-invoke?prepay_id=DY-PREPAY-" + url.QueryEscape(preOrderID)
	default:
		return a.hostingJumpURL(preOrderID)
	}
}

func hostingQueryPayType(payment Payment) string {
	switch {
	case payment.BusinessVariant == "hosting.wechat-mini":
		return "T_MINIAPP"
	case strings.Contains(payment.BusinessVariant, "wechat"):
		return "T_JSAPI"
	case strings.Contains(payment.BusinessVariant, "alipay"):
		return "A_JSAPI"
	case strings.Contains(payment.BusinessVariant, "unionpay"):
		return "U_NATIVE"
	case strings.Contains(payment.BusinessVariant, "douyin"):
		return "Y_APP"
	default:
		return "A_JSAPI"
	}
}

func hostingQueryBankCode(payment Payment) string {
	if payment.State == "F" {
		return "CLOSED"
	}
	switch {
	case strings.HasPrefix(hostingQueryPayType(payment), "A_"):
		return "TRADE_SUCCESS"
	case strings.HasPrefix(hostingQueryPayType(payment), "T_"):
		return "SUCCESS"
	default:
		return "SUCCESS"
	}
}

func hostingQueryBankDesc(payment Payment) string {
	if payment.State == "F" {
		return "交易已关单"
	}
	switch {
	case strings.HasPrefix(hostingQueryPayType(payment), "A_"):
		return "TRADE_SUCCESS"
	case strings.HasPrefix(hostingQueryPayType(payment), "T_"):
		return "交易成功"
	default:
		return "交易成功"
	}
}

func hostingQueryFeeAmount(payment Payment) string {
	if strings.HasPrefix(hostingQueryPayType(payment), "A_") {
		return "0.04"
	}
	if strings.HasPrefix(hostingQueryPayType(payment), "T_") {
		return "0.03"
	}
	return "0.00"
}

func hostingQueryDivFlag(payment Payment) string {
	if stringValue(payment.ChannelResponse["acct_split_bunch"]) != "" {
		return "Y"
	}
	return "N"
}

func readHostingConfirmIDs(r *http.Request) (string, string, error) {
	preOrderID := r.URL.Query().Get("pre_order_id")
	reqSeqID := r.URL.Query().Get("req_seq_id")
	if strings.Contains(strings.ToLower(r.Header.Get("Content-Type")), "application/json") {
		body, err := io.ReadAll(io.LimitReader(r.Body, 1<<20))
		if err != nil {
			return "", "", err
		}
		if len(strings.TrimSpace(string(body))) > 0 {
			var data map[string]any
			if err := json.Unmarshal(body, &data); err != nil {
				return "", "", err
			}
			if preOrderID == "" {
				preOrderID = stringValue(data["pre_order_id"])
			}
			if reqSeqID == "" {
				reqSeqID = stringValue(data["req_seq_id"])
			}
		}
	} else if err := r.ParseForm(); err == nil {
		if preOrderID == "" {
			preOrderID = r.Form.Get("pre_order_id")
		}
		if reqSeqID == "" {
			reqSeqID = r.Form.Get("req_seq_id")
		}
	}
	if preOrderID == "" && reqSeqID == "" {
		return "", "", errors.New("pre_order_id or req_seq_id is required")
	}
	return preOrderID, reqSeqID, nil
}

func (a *App) findHostingCallbackPayment(preOrderID, reqSeqID string) (Payment, bool) {
	a.mu.Lock()
	defer a.mu.Unlock()
	if preOrderID != "" {
		if indexedReqSeqID, ok := a.preIndex[preOrderID]; ok {
			payment, ok := a.payments[indexedReqSeqID]
			if ok {
				return *payment, true
			}
		}
	}
	if reqSeqID != "" {
		payment, ok := a.payments[reqSeqID]
		if ok {
			return *payment, true
		}
	}
	return Payment{}, false
}

func stringValue(value any) string {
	switch v := value.(type) {
	case string:
		return v
	case nil:
		return ""
	default:
		return fmt.Sprint(v)
	}
}

func isLoopbackHost(host string) bool {
	ip := net.ParseIP(host)
	if ip != nil {
		return ip.IsLoopback()
	}
	return host == "localhost"
}

func isAllowedLocalOrigin(raw string) bool {
	u, err := url.Parse(raw)
	if err != nil {
		return false
	}
	if u.Scheme != "http" && u.Scheme != "https" {
		return false
	}
	host := strings.ToLower(u.Hostname())
	if host == "localhost" {
		return true
	}
	ip := net.ParseIP(host)
	return ip != nil && ip.IsLoopback()
}

func isSameOriginOrNoOrigin(r *http.Request) bool {
	origin := strings.TrimSpace(r.Header.Get("Origin"))
	if origin == "" {
		return true
	}
	u, err := url.Parse(origin)
	if err != nil {
		return false
	}
	return strings.EqualFold(u.Host, r.Host)
}
