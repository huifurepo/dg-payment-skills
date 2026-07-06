package main

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
)

type adminDeliveryRequest struct {
	Channel    string `json:"channel"`
	EntityType string `json:"entity_type"`
	Kind       string `json:"kind,omitempty"`
	ReqSeqID   string `json:"req_seq_id"`
	Outcome    string `json:"outcome"`
}

func (a *App) handleAdminDeliver(w http.ResponseWriter, r *http.Request) {
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

	var req adminDeliveryRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]any{"error": "invalid_json"})
		return
	}
	normalizeAdminDeliveryRequest(&req)
	if err := validateAdminDeliveryRequest(req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]any{"error": err.Error()})
		return
	}

	switch req.Channel {
	case "notify":
		delivery, attempted, err := a.adminNotifyDelivery(req)
		if !attempted {
			writeJSON(w, http.StatusBadRequest, map[string]any{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"ok":           err == nil,
			"channel":      req.Channel,
			"entity_type":  req.EntityType,
			"req_seq_id":   req.ReqSeqID,
			"outcome":      req.Outcome,
			"notification": adminNotificationDeliveryResponse(delivery),
			"error":        errorString(err),
		})
	case "webhook":
		deliveries, attempted, err := a.adminWebhookDelivery(req)
		if !attempted {
			writeJSON(w, http.StatusBadRequest, map[string]any{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"ok":          err == nil,
			"channel":     req.Channel,
			"entity_type": req.EntityType,
			"req_seq_id":  req.ReqSeqID,
			"outcome":     req.Outcome,
			"webhooks":    adminWebhookDeliveryResponses(deliveries),
			"error":       errorString(err),
		})
	default:
		writeJSON(w, http.StatusBadRequest, map[string]any{"error": "unsupported channel"})
	}
}

func normalizeAdminDeliveryRequest(req *adminDeliveryRequest) {
	req.Channel = strings.ToLower(strings.TrimSpace(req.Channel))
	req.EntityType = strings.ToLower(strings.TrimSpace(req.EntityType))
	req.Kind = strings.ToLower(strings.TrimSpace(req.Kind))
	req.ReqSeqID = strings.TrimSpace(req.ReqSeqID)
	req.Outcome = strings.ToLower(strings.TrimSpace(req.Outcome))
}

func validateAdminDeliveryRequest(req adminDeliveryRequest) error {
	if req.Channel != "notify" && req.Channel != "webhook" {
		return usageError("channel must be notify or webhook")
	}
	switch req.EntityType {
	case "payment", "refund", "close":
	default:
		return usageError("entity_type must be payment, refund, or close")
	}
	if req.ReqSeqID == "" {
		return usageError("req_seq_id is required")
	}
	if req.Outcome != "success" && req.Outcome != "failure" {
		return usageError("outcome must be success or failure")
	}
	return nil
}

func adminNotificationDeliveryResponse(delivery NotificationDelivery) map[string]any {
	delivery = sanitizeNotificationDeliveryForOutput(delivery)
	return map[string]any{
		"id":                 delivery.ID,
		"time":               delivery.Time,
		"payment_req_seq_id": delivery.PaymentReqSeqID,
		"target_redacted":    firstNonEmpty(delivery.TargetRedacted, redactTarget(delivery.Target)),
		"status":             delivery.Status,
		"expected_ack":       delivery.ExpectedACK,
		"ack_body":           delivery.AckBody,
		"error":              delivery.Error,
		"diagnosis":          delivery.Diagnosis,
		"duplicate":          delivery.Duplicate,
		"resp_data_sha256":   delivery.RespDataSHA256,
		"resp_data_keys":     delivery.RespDataKeys,
		"attempts":           delivery.Attempts,
	}
}

func adminWebhookDeliveryResponses(deliveries []WebhookDelivery) []map[string]any {
	out := make([]map[string]any, 0, len(deliveries))
	for _, delivery := range deliveries {
		out = append(out, adminWebhookDeliveryResponse(delivery))
	}
	return out
}

func adminWebhookDeliveryResponse(delivery WebhookDelivery) map[string]any {
	delivery = sanitizeWebhookDeliveryForOutput(delivery)
	return map[string]any{
		"id":              delivery.ID,
		"time":            delivery.Time,
		"event_type":      delivery.EventType,
		"entity_id":       delivery.EntityID,
		"target_redacted": firstNonEmpty(delivery.TargetRedacted, redactTarget(delivery.Target)),
		"status":          delivery.Status,
		"sign_sha256":     signatureDigest(delivery.Sign),
		"raw_body_sha256": delivery.RawBodySHA256,
		"payload_keys":    delivery.PayloadKeys,
		"error":           delivery.Error,
		"diagnosis":       delivery.Diagnosis,
		"attempts":        delivery.Attempts,
	}
}

func (a *App) adminNotifyDelivery(req adminDeliveryRequest) (NotificationDelivery, bool, error) {
	switch req.EntityType {
	case "payment":
		payment, ok := a.paymentSnapshot(req.ReqSeqID)
		if !ok {
			return NotificationDelivery{}, false, usageError("unknown payment " + req.ReqSeqID)
		}
		if payment.NotifyURL == "" {
			return NotificationDelivery{}, false, usageError("payment has no notify_url")
		}
		payment.State = deliveryState(req.Outcome)
		respData := notificationRespData(payment)
		applyManualNotificationOutcome(respData, req.Outcome)
		delivery, err := a.deliverNotificationPayload(payment.ReqSeqID, payment.NotifyURL, respData, false)
		a.recordAdminNotification(req, delivery, err)
		return delivery, true, err
	case "refund":
		refund, ok := a.refundSnapshot(req.Kind, req.ReqSeqID)
		if !ok {
			return NotificationDelivery{}, false, usageError("unknown refund " + req.ReqSeqID)
		}
		if refund.NotifyURL == "" {
			return NotificationDelivery{}, false, usageError("refund has no notify_url")
		}
		refund.State = deliveryState(req.Outcome)
		respData := a.refundNotificationRespData(refund)
		applyManualNotificationOutcome(respData, req.Outcome)
		delivery, err := a.deliverNotificationPayload(refund.ReqSeqID, refund.NotifyURL, respData, false)
		a.recordAdminNotification(req, delivery, err)
		return delivery, true, err
	case "close":
		closeOp, ok := a.closeSnapshot(req.Kind, req.ReqSeqID)
		if !ok {
			return NotificationDelivery{}, false, usageError("unknown close " + req.ReqSeqID)
		}
		if closeOp.NotifyURL == "" {
			return NotificationDelivery{}, false, usageError("close has no notify_url inherited from original payment")
		}
		closeOp.State = deliveryState(req.Outcome)
		respData := closeNotificationRespData(closeOp)
		applyManualNotificationOutcome(respData, req.Outcome)
		delivery, err := a.deliverNotificationPayload(closeOp.ReqSeqID, closeOp.NotifyURL, respData, false)
		a.recordAdminNotification(req, delivery, err)
		return delivery, true, err
	default:
		return NotificationDelivery{}, false, usageError("unsupported notify entity type")
	}
}

func (a *App) handleAdminHostingSuccess(w http.ResponseWriter, r *http.Request) {
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
	preOrderID, reqSeqID, err := readHostingConfirmIDs(r)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]any{"error": err.Error()})
		return
	}
	payment, err := a.simulateHostingSuccess(preOrderID, reqSeqID)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]any{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"ok":           true,
		"req_seq_id":   payment.ReqSeqID,
		"pre_order_id": payment.PreOrderID,
		"state":        payment.State,
		"next":         "queryorderinfo",
	})
}

func (a *App) simulateHostingSuccess(preOrderID, reqSeqID string) (Payment, error) {
	a.mu.Lock()
	var payment *Payment
	if preOrderID != "" {
		if indexedReqSeqID, ok := a.preIndex[preOrderID]; ok {
			payment = a.payments[indexedReqSeqID]
		}
	}
	if payment == nil && reqSeqID != "" {
		payment = a.payments[reqSeqID]
	}
	if payment == nil || payment.Kind != "hosting" {
		a.mu.Unlock()
		return Payment{}, usageError("unknown hosting order")
	}
	if payment.State == "F" {
		a.mu.Unlock()
		return Payment{}, usageError("hosting order is already closed or failed")
	}
	payment.HostingCallbackSeen = true
	payment.HostingConfirmed = true
	payment.ConfirmCount++
	payment.State = "S"
	snapshot := *payment
	a.mu.Unlock()
	a.record("hosting.admin_success", "", snapshot.ReqSeqID, map[string]any{
		"pre_order_id": snapshot.PreOrderID,
		"state":        snapshot.State,
	})
	a.maybeNotifyPayment(snapshot.ReqSeqID)
	a.maybeWebhookPayment(snapshot.ReqSeqID)
	return snapshot, nil
}

func (a *App) adminWebhookDelivery(req adminDeliveryRequest) ([]WebhookDelivery, bool, error) {
	targets := a.webhookTargetsSnapshot()
	if len(targets) == 0 {
		return nil, false, usageError("no webhook targets configured")
	}

	var eventType string
	var entityID string
	var payload map[string]any
	switch req.EntityType {
	case "payment":
		payment, ok := a.paymentSnapshot(req.ReqSeqID)
		if !ok {
			return nil, false, usageError("unknown payment " + req.ReqSeqID)
		}
		payment.State = deliveryState(req.Outcome)
		eventType = webhookEventPayment
		entityID = payment.ReqSeqID
		payload = paymentWebhookPayload(payment)
	case "refund":
		refund, ok := a.refundSnapshot(req.Kind, req.ReqSeqID)
		if !ok {
			return nil, false, usageError("unknown refund " + req.ReqSeqID)
		}
		refund.State = deliveryState(req.Outcome)
		eventType = webhookEventRefund
		entityID = refund.ReqSeqID
		payload = refundWebhookPayload(refund)
	case "close":
		closeOp, ok := a.closeSnapshot(req.Kind, req.ReqSeqID)
		if !ok {
			return nil, false, usageError("unknown close " + req.ReqSeqID)
		}
		closeOp.State = deliveryState(req.Outcome)
		eventType = webhookEventClose
		entityID = closeOp.ReqSeqID
		payload = closeWebhookPayload(closeOp)
	default:
		return nil, false, usageError("unsupported webhook entity type")
	}
	payload["sandbox_manual_outcome"] = req.Outcome

	deliveries := make([]WebhookDelivery, 0, len(targets))
	var errorsOut []string
	for _, target := range targets {
		delivery, err := a.deliverWebhook(target, eventType, entityID, payload)
		deliveries = append(deliveries, delivery)
		a.recordAdminWebhook(req, delivery, err)
		if err != nil {
			errorsOut = append(errorsOut, err.Error())
		}
	}
	if len(errorsOut) > 0 {
		return deliveries, true, errors.New(strings.Join(errorsOut, "; "))
	}
	return deliveries, true, nil
}

func (a *App) refundSnapshot(kind, reqSeqID string) (RefundOperation, bool) {
	a.mu.Lock()
	defer a.mu.Unlock()
	if kind != "" {
		refund, ok := a.refunds[operationKey(kind, reqSeqID)]
		if !ok || refund == nil {
			return RefundOperation{}, false
		}
		return *refund, true
	}
	for _, refund := range a.refunds {
		if refund != nil && refund.ReqSeqID == reqSeqID {
			return *refund, true
		}
	}
	return RefundOperation{}, false
}

func (a *App) closeSnapshot(kind, reqSeqID string) (CloseOperation, bool) {
	a.mu.Lock()
	defer a.mu.Unlock()
	if kind != "" {
		closeOp, ok := a.closes[operationKey(kind, reqSeqID)]
		if !ok || closeOp == nil {
			return CloseOperation{}, false
		}
		return *closeOp, true
	}
	for _, closeOp := range a.closes {
		if closeOp != nil && closeOp.ReqSeqID == reqSeqID {
			return *closeOp, true
		}
	}
	return CloseOperation{}, false
}

func deliveryState(outcome string) string {
	if outcome == "success" {
		return "S"
	}
	return "F"
}

func applyManualNotificationOutcome(respData map[string]any, outcome string) {
	respData["sandbox_manual_outcome"] = outcome
	if outcome == "success" {
		respData["resp_code"] = "00000000"
		respData["resp_desc"] = "success"
		applyState(respData, "S")
		return
	}
	respData["resp_code"] = "LS200099"
	respData["resp_desc"] = "sandbox manual failure"
	applyState(respData, "F")
}

func applyState(respData map[string]any, state string) {
	for _, key := range []string{"trans_stat", "close_stat"} {
		if _, ok := respData[key]; ok {
			respData[key] = state
		}
	}
	if _, ok := respData["order_stat"]; ok {
		respData["order_stat"] = hostingOrderStatFromTransState(state)
	}
}

func (a *App) recordAdminNotification(req adminDeliveryRequest, delivery NotificationDelivery, err error) {
	details := map[string]any{
		"channel":          req.Channel,
		"entity_type":      req.EntityType,
		"outcome":          req.Outcome,
		"target":           delivery.TargetRedacted,
		"status":           delivery.Status,
		"attempts":         len(delivery.Attempts),
		"expected_ack":     delivery.ExpectedACK,
		"resp_data_sha256": delivery.RespDataSHA256,
		"manual":           true,
	}
	if delivery.Diagnosis != "" {
		details["diagnosis"] = delivery.Diagnosis
	}
	if err != nil {
		details["error"] = sanitizePlainLogText(err.Error())
	}
	a.record("admin.notify_delivery", "", req.ReqSeqID, details)
}

func (a *App) recordAdminWebhook(req adminDeliveryRequest, delivery WebhookDelivery, err error) {
	details := map[string]any{
		"channel":          req.Channel,
		"entity_type":      req.EntityType,
		"outcome":          req.Outcome,
		"event_type":       delivery.EventType,
		"target":           delivery.TargetRedacted,
		"status":           delivery.Status,
		"attempts":         len(delivery.Attempts),
		"raw_body_sha256":  delivery.RawBodySHA256,
		"signature_scheme": "md5(raw_body+endpoint_key)",
		"manual":           true,
	}
	if delivery.Diagnosis != "" {
		details["diagnosis"] = delivery.Diagnosis
	}
	if err != nil {
		details["error"] = sanitizePlainLogText(err.Error())
	}
	a.record("admin.webhook_delivery", "", req.ReqSeqID, details)
}
