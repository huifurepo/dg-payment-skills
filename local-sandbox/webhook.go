package main

import (
	"bytes"
	"crypto/md5"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
)

const (
	webhookEventPayment = "trans.pay"
	webhookEventRefund  = "refund.standard"
	webhookEventClose   = "trans.close"
)

func (a *App) setWebhookEndpointKey(key string) error {
	if len(key) != 32 {
		return usageError("--webhook-endpoint-key must be exactly 32 characters")
	}
	a.mu.Lock()
	defer a.mu.Unlock()
	a.webhookEndpointKey = key
	return nil
}

func (a *App) addWebhookTarget(raw string) error {
	u, err := parseNotifyURL(raw)
	if err != nil {
		return err
	}
	a.mu.Lock()
	defer a.mu.Unlock()
	a.webhookTargets = append(a.webhookTargets, u.String())
	return nil
}

func (a *App) setRuntimeWebhookTarget(raw string) (string, error) {
	raw = strings.TrimSpace(raw)
	if raw == "" {
		return "", usageError("webhook target is required")
	}
	pinned, err := a.validateWebhookTarget(raw)
	if err != nil {
		return "", err
	}
	normalized := pinned.String()
	a.mu.Lock()
	a.webhookTargets = []string{normalized}
	a.mu.Unlock()
	a.record("admin.webhook_target_configured", "", "", map[string]any{"target": redactTarget(normalized)})
	return normalized, nil
}

func (a *App) webhookTargetsSnapshot() []string {
	a.mu.Lock()
	defer a.mu.Unlock()
	return append([]string(nil), a.webhookTargets...)
}

func (a *App) webhookEndpointKeySnapshot() string {
	a.mu.Lock()
	defer a.mu.Unlock()
	return a.webhookEndpointKey
}

func (a *App) maybeWebhookPayment(reqSeqID string) {
	if len(a.webhookTargetsSnapshot()) == 0 {
		return
	}
	a.mu.Lock()
	payment, ok := a.payments[reqSeqID]
	if !ok || payment.Webhooked || payment.State != "S" {
		a.mu.Unlock()
		return
	}
	payment.Webhooked = true
	snapshot := *payment
	a.mu.Unlock()
	a.dispatchWebhookEvent(webhookEventPayment, snapshot.ReqSeqID, paymentWebhookPayload(snapshot))
}

func (a *App) maybeWebhookRefund(reqSeqID, kind string) {
	if len(a.webhookTargetsSnapshot()) == 0 {
		return
	}
	key := operationKey(kind, reqSeqID)
	a.mu.Lock()
	refund, ok := a.refunds[key]
	if !ok || refund.Webhooked || refund.State != "S" {
		a.mu.Unlock()
		return
	}
	refund.Webhooked = true
	snapshot := *refund
	a.mu.Unlock()
	a.dispatchWebhookEvent(webhookEventRefund, snapshot.ReqSeqID, refundWebhookPayload(snapshot))
}

func (a *App) maybeWebhookClose(reqSeqID, kind string) {
	if len(a.webhookTargetsSnapshot()) == 0 {
		return
	}
	key := operationKey(kind, reqSeqID)
	a.mu.Lock()
	closeOp, ok := a.closes[key]
	if !ok || closeOp.Webhooked || closeOp.State != "S" {
		a.mu.Unlock()
		return
	}
	closeOp.Webhooked = true
	snapshot := *closeOp
	a.mu.Unlock()
	a.dispatchWebhookEvent(webhookEventClose, snapshot.ReqSeqID, closeWebhookPayload(snapshot))
}

func (a *App) maybeWebhookCloseByPayment(kind, paymentReqSeqID string) {
	if len(a.webhookTargetsSnapshot()) == 0 {
		return
	}
	a.mu.Lock()
	closeKey, ok := a.closeIndex[operationKey(kind, paymentReqSeqID)]
	if !ok {
		a.mu.Unlock()
		return
	}
	closeOp, ok := a.closes[closeKey]
	if !ok || closeOp.Webhooked || closeOp.State != "S" {
		a.mu.Unlock()
		return
	}
	closeOp.Webhooked = true
	snapshot := *closeOp
	a.mu.Unlock()
	a.dispatchWebhookEvent(webhookEventClose, snapshot.ReqSeqID, closeWebhookPayload(snapshot))
}

func (a *App) dispatchWebhookEvent(eventType, entityID string, payload map[string]any) {
	for _, target := range a.webhookTargetsSnapshot() {
		delivery, err := a.deliverWebhook(target, eventType, entityID, payload)
		details := map[string]any{
			"event_type":       eventType,
			"target":           delivery.TargetRedacted,
			"status":           delivery.Status,
			"attempts":         len(delivery.Attempts),
			"raw_body_sha256":  delivery.RawBodySHA256,
			"ack_rule":         "any-http-2xx",
			"signature_scheme": "md5(raw_body+endpoint_key)",
		}
		if err != nil {
			details["error"] = err.Error()
		}
		a.record("webhook.delivery", "", entityID, details)
	}
}

func (a *App) deliverWebhook(target, eventType, entityID string, payload map[string]any) (WebhookDelivery, error) {
	rawBody, err := json.Marshal(payload)
	if err != nil {
		return WebhookDelivery{}, err
	}
	sign := webhookSignature(rawBody, a.webhookEndpointKeySnapshot())
	sum := sha256.Sum256(rawBody)
	delivery := WebhookDelivery{
		ID:             nextID("WD"),
		Time:           time.Now().UTC().Format(time.RFC3339Nano),
		EventType:      eventType,
		EntityID:       entityID,
		Target:         target,
		TargetRedacted: redactTarget(target),
		Status:         "pending",
		Sign:           sign,
		RawBodySHA256:  "sha256:" + hex.EncodeToString(sum[:]),
		PayloadKeys:    mapKeys(payload),
	}
	pinned, err := a.validateWebhookTarget(target)
	if err != nil {
		delivery.Status = "blocked"
		delivery.Error = sanitizePlainLogText(err.Error())
		a.storeWebhook(delivery)
		return delivery, err
	}
	delivery.Target = pinned.String()
	delivery.TargetRedacted = redactTarget(pinned.String())

	maxAttempt := a.notifyMaxAttempt
	if maxAttempt <= 0 {
		maxAttempt = 1
	}
	for attemptNo := 1; attemptNo <= maxAttempt; attemptNo++ {
		attempt := a.postWebhookAttempt(pinned, sign, rawBody, attemptNo)
		delivery.Attempts = append(delivery.Attempts, attempt)
		delivery.Error = attempt.Error
		delivery.Diagnosis = attempt.Diagnosis
		if attempt.Status == "ack" {
			delivery.Status = "delivered"
			delivery.Error = ""
			delivery.Diagnosis = ""
			break
		}
		if attemptNo < maxAttempt && a.notifyRetryDelay > 0 {
			time.Sleep(a.notifyRetryDelay)
		}
	}
	if delivery.Status != "delivered" {
		delivery.Status = "failed"
		if delivery.Error == "" {
			delivery.Error = "webhook 2xx ACK was not received"
		}
	}
	a.storeWebhook(delivery)
	if delivery.Status != "delivered" {
		return delivery, fmt.Errorf("webhook delivery %s: %s", delivery.Status, delivery.Error)
	}
	return delivery, nil
}

func (a *App) validateWebhookTarget(raw string) (*PinnedTarget, error) {
	allowlist := a.notifyAllowlistSnapshot()
	u, err := validateNotifyTarget(raw, allowlist)
	if err != nil {
		a.recordSecurityFinding("webhook_target_blocked", raw, err.Error())
		return nil, err
	}
	return u, nil
}

func (a *App) postWebhookAttempt(target *PinnedTarget, sign string, rawBody []byte, attemptNo int) WebhookAttempt {
	attempt := WebhookAttempt{
		Attempt: attemptNo,
		Time:    time.Now().UTC().Format(time.RFC3339Nano),
		Status:  "pending",
	}
	signedTarget, err := addWebhookSign(target.String(), sign)
	if err != nil {
		attempt.Status = "request_error"
		attempt.Error = sanitizePlainLogText(err.Error())
		return attempt
	}
	req, err := http.NewRequest(http.MethodPost, signedTarget, bytes.NewReader(rawBody))
	if err != nil {
		attempt.Status = "request_error"
		attempt.Error = sanitizePlainLogText(err.Error())
		return attempt
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", appName+"/"+appVersion)
	resp, err := a.doPinned(req, target)
	if err != nil {
		if resp != nil && resp.Body != nil {
			_ = resp.Body.Close()
		}
		attempt.Status = "network_error"
		attempt.Error = sanitizePlainLogText(err.Error())
		if stringsContainsFold(err.Error(), "redirect") {
			attempt.Status = "redirect_blocked"
			a.recordSecurityFinding("webhook_redirect_blocked", target.String(), err.Error())
		}
		attempt.Diagnosis = diagnoseWebhookAttempt(attempt)
		return attempt
	}
	defer resp.Body.Close()
	body, readErr := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
	if readErr != nil {
		attempt.Status = "read_error"
		attempt.HTTPStatus = resp.StatusCode
		attempt.Error = sanitizePlainLogText(readErr.Error())
		attempt.Diagnosis = diagnoseWebhookAttempt(attempt)
		return attempt
	}
	attempt.HTTPStatus = resp.StatusCode
	attempt.AckBody = sanitizePlainLogText(string(body))
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		attempt.Status = "ack"
		return attempt
	}
	if resp.StatusCode >= 300 && resp.StatusCode < 400 {
		attempt.Status = "redirect_blocked"
		attempt.Error = "redirect response is not allowed"
		attempt.Diagnosis = diagnoseWebhookAttempt(attempt)
		a.recordSecurityFinding("webhook_redirect_blocked", target.String(), attempt.Error)
		return attempt
	}
	attempt.Status = "ack_mismatch"
	attempt.Error = "want any HTTP 2xx"
	attempt.Diagnosis = diagnoseWebhookAttempt(attempt)
	return attempt
}

func diagnoseWebhookAttempt(attempt WebhookAttempt) string {
	context := strings.ToLower(attempt.AckBody + " " + attempt.Error)
	if attempt.HTTPStatus == http.StatusUnsupportedMediaType ||
		strings.Contains(context, "content type") ||
		strings.Contains(context, "unsupported media type") {
		return "Webhook 接收端不支持平台事件通知的 JSON 格式。Webhook 应接收 application/json 原始请求体，并从 URL query 读取 sign；不要按 notify_url 的 sign/resp_data 表单解析。"
	}
	if attempt.Status == "redirect_blocked" {
		return "Webhook 目标返回了重定向；本地沙箱会拦截重定向。请把 Webhook 目标配成最终接收地址。"
	}
	if attempt.Status == "network_error" {
		return "Webhook 目标网络不可达或被本地安全策略拦截。请确认地址能从沙箱进程访问，外部地址需通过 --notify-allow 精确放行。"
	}
	if attempt.Status == "read_error" {
		return "Webhook 目标响应体读取失败。请检查接收端是否提前断开连接或返回了异常响应。"
	}
	if attempt.Status == "ack_mismatch" {
		return fmt.Sprintf("Webhook 接收端必须返回任意 HTTP 2xx；当前 HTTP 状态为 %d。Webhook 不使用 RECV_ORD_ID_ 回包。", attempt.HTTPStatus)
	}
	return ""
}

func (a *App) storeWebhook(delivery WebhookDelivery) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.webhooks = append(a.webhooks, delivery)
}

func addWebhookSign(target, sign string) (string, error) {
	u, err := url.Parse(target)
	if err != nil {
		return "", err
	}
	q := u.Query()
	q.Set("sign", sign)
	u.RawQuery = q.Encode()
	return u.String(), nil
}

func webhookSignature(rawBody []byte, endpointKey string) string {
	h := md5.New()
	h.Write(rawBody)
	h.Write([]byte(endpointKey))
	return strings.ToUpper(hex.EncodeToString(h.Sum(nil)))
}

func paymentWebhookPayload(payment Payment) map[string]any {
	payload := webhookBase(webhookEventPayment)
	payload["huifu_id"] = payment.HuifuID
	payload["req_date"] = payment.ReqDate
	payload["req_seq_id"] = payment.ReqSeqID
	payload["hf_seq_id"] = payment.HFSeqID
	payload["pre_order_id"] = payment.PreOrderID
	payload["kind"] = payment.Kind
	payload["trans_amt"] = payment.TransAmt
	payload["trans_stat"] = payment.State
	if payment.Kind == "hosting" {
		payload["order_stat"] = hostingOrderStat(payment)
		payload["party_order_id"] = hostingPartyOrderID(payment)
		payload["out_trans_id"] = "OUT-" + payment.ReqSeqID
	} else {
		payload["party_order_id"] = aggregationPartyOrderID(payment)
		payload["out_ord_id"] = aggregationOutOrdID(payment)
	}
	return addPaymentExtensions(payload, payment)
}

func refundWebhookPayload(refund RefundOperation) map[string]any {
	payload := webhookBase(webhookEventRefund)
	payload["huifu_id"] = refund.HuifuID
	payload["req_date"] = refund.ReqDate
	payload["req_seq_id"] = refund.ReqSeqID
	payload["hf_seq_id"] = refund.HFSeqID
	payload["org_req_date"] = refund.PaymentReqDate
	payload["org_req_seq_id"] = refund.PaymentReqSeqID
	payload["org_hf_seq_id"] = refund.PaymentHFSeqID
	payload["kind"] = refund.Kind
	payload["ord_amt"] = refund.OrdAmt
	payload["actual_ref_amt"] = refund.OrdAmt
	payload["party_order_id"] = refundPartyOrderID(refund)
	payload["trans_stat"] = refund.State
	return addOperationExtensions(payload, refund.BusinessVariant, refund.ChannelResponse)
}

func closeWebhookPayload(closeOp CloseOperation) map[string]any {
	payload := webhookBase(webhookEventClose)
	payload["huifu_id"] = closeOp.HuifuID
	payload["req_date"] = closeOp.ReqDate
	payload["req_seq_id"] = closeOp.ReqSeqID
	payload["org_req_date"] = closeOp.PaymentReqDate
	payload["org_req_seq_id"] = closeOp.PaymentReqSeqID
	payload["kind"] = closeOp.Kind
	payload["close_stat"] = closeOp.State
	payload["trans_stat"] = closeOp.State
	return addOperationExtensions(payload, closeOp.BusinessVariant, closeOp.ChannelResponse)
}

func webhookBase(eventType string) map[string]any {
	return map[string]any{
		"event_id":    nextID("EV"),
		"event_type":  eventType,
		"occurred_at": time.Now().UTC().Format(time.RFC3339Nano),
		"synthetic":   true,
	}
}

func stringsContainsFold(value, needle string) bool {
	return bytes.Contains(bytes.ToLower([]byte(value)), bytes.ToLower([]byte(needle)))
}
