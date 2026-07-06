package main

import (
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

func (a *App) maybeNotifyPayment(reqSeqID string) {
	a.mu.Lock()
	payment, ok := a.payments[reqSeqID]
	if !ok || payment.NotifyURL == "" || payment.Notified || payment.State != "S" {
		a.mu.Unlock()
		return
	}
	payment.Notified = true
	snapshot := *payment
	target := payment.NotifyURL
	a.mu.Unlock()

	delivery, err := a.deliverNotification(snapshot, target, false)
	details := map[string]any{
		"target":           delivery.TargetRedacted,
		"status":           delivery.Status,
		"attempts":         len(delivery.Attempts),
		"expected_ack":     delivery.ExpectedACK,
		"resp_data_sha256": delivery.RespDataSHA256,
	}
	if err != nil {
		details["error"] = err.Error()
	}
	a.record("notify.delivery", "", reqSeqID, details)
}

func (a *App) dispatchPaymentNotify(reqSeqID, target string, duplicate bool) (NotificationDelivery, error) {
	payment, ok := a.paymentSnapshot(reqSeqID)
	if !ok {
		return NotificationDelivery{}, usageError("unknown payment " + reqSeqID)
	}
	if target == "" {
		target = payment.NotifyURL
	}
	return a.deliverNotification(payment, target, duplicate)
}

func (a *App) paymentSnapshot(reqSeqID string) (Payment, bool) {
	a.mu.Lock()
	defer a.mu.Unlock()
	payment, ok := a.payments[reqSeqID]
	if !ok {
		return Payment{}, false
	}
	return *payment, true
}

func (a *App) deliverNotification(payment Payment, target string, duplicate bool) (NotificationDelivery, error) {
	return a.deliverNotificationPayload(payment.ReqSeqID, target, notificationRespData(payment), duplicate)
}

func (a *App) maybeNotifyRefund(reqSeqID, kind string) {
	key := operationKey(kind, reqSeqID)
	a.mu.Lock()
	refund, ok := a.refunds[key]
	if !ok || refund.NotifyURL == "" || refund.Notified || refund.State != "S" {
		a.mu.Unlock()
		return
	}
	refund.Notified = true
	snapshot := *refund
	target := refund.NotifyURL
	a.mu.Unlock()

	delivery, err := a.deliverNotificationPayload(snapshot.ReqSeqID, target, a.refundNotificationRespData(snapshot), false)
	details := map[string]any{
		"target":           delivery.TargetRedacted,
		"status":           delivery.Status,
		"attempts":         len(delivery.Attempts),
		"expected_ack":     delivery.ExpectedACK,
		"resp_data_sha256": delivery.RespDataSHA256,
		"kind":             kind,
	}
	if err != nil {
		details["error"] = err.Error()
	}
	a.record("notify.refund_delivery", "", reqSeqID, details)
}

func (a *App) maybeNotifyClose(reqSeqID, kind string) {
	key := operationKey(kind, reqSeqID)
	a.mu.Lock()
	closeOp, ok := a.closes[key]
	if !ok || closeOp == nil || closeOp.NotifyURL == "" || closeOp.Notified || closeOp.State != "S" {
		a.mu.Unlock()
		return
	}
	closeOp.Notified = true
	snapshot := *closeOp
	target := closeOp.NotifyURL
	a.mu.Unlock()

	delivery, err := a.deliverNotificationPayload(snapshot.ReqSeqID, target, closeNotificationRespData(snapshot), false)
	details := map[string]any{
		"target":           delivery.TargetRedacted,
		"status":           delivery.Status,
		"attempts":         len(delivery.Attempts),
		"expected_ack":     delivery.ExpectedACK,
		"resp_data_sha256": delivery.RespDataSHA256,
		"kind":             kind,
	}
	if delivery.Diagnosis != "" {
		details["diagnosis"] = delivery.Diagnosis
	}
	if err != nil {
		details["error"] = err.Error()
	}
	a.record("notify.close_delivery", "", reqSeqID, details)
}

func (a *App) deliverNotificationPayload(entityReqSeqID, target string, respData map[string]any, duplicate bool) (NotificationDelivery, error) {
	respRaw, err := json.Marshal(respData)
	if err != nil {
		return NotificationDelivery{}, err
	}
	respString := string(respRaw)
	signature, err := signRaw(respString, a.creds.GatewayPrivate)
	if err != nil {
		return NotificationDelivery{}, err
	}
	sum := sha256.Sum256(respRaw)
	delivery := NotificationDelivery{
		ID:              nextID("ND"),
		Time:            time.Now().UTC().Format(time.RFC3339Nano),
		PaymentReqSeqID: entityReqSeqID,
		Target:          target,
		TargetRedacted:  redactTarget(target),
		Status:          "pending",
		ExpectedACK:     expectedNotifyACK(entityReqSeqID),
		Duplicate:       duplicate,
		RespDataSHA256:  "sha256:" + hex.EncodeToString(sum[:]),
		RespDataKeys:    mapKeys(respData),
	}
	pinned, err := a.validateNotifyTarget(target)
	if err != nil {
		delivery.Status = "blocked"
		delivery.Error = sanitizePlainLogText(err.Error())
		a.storeNotification(delivery)
		return delivery, err
	}
	delivery.Target = pinned.String()
	delivery.TargetRedacted = redactTarget(pinned.String())

	maxAttempt := a.notifyMaxAttempt
	if maxAttempt <= 0 {
		maxAttempt = 1
	}
	for attemptNo := 1; attemptNo <= maxAttempt; attemptNo++ {
		attempt := a.postNotificationAttempt(pinned, signature, respString, delivery.ExpectedACK, attemptNo)
		delivery.Attempts = append(delivery.Attempts, attempt)
		delivery.AckBody = attempt.AckBody
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
			delivery.Error = "notify ACK was not received"
		}
	}
	a.storeNotification(delivery)
	if delivery.Status != "delivered" {
		return delivery, fmt.Errorf("notify delivery %s: %s", delivery.Status, delivery.Error)
	}
	return delivery, nil
}

func (a *App) postNotificationAttempt(target *PinnedTarget, signature, respData, expectedACK string, attemptNo int) NotificationAttempt {
	attempt := NotificationAttempt{
		Attempt: attemptNo,
		Time:    time.Now().UTC().Format(time.RFC3339Nano),
		Status:  "pending",
	}
	form := url.Values{}
	form.Set("sign", signature)
	form.Set("resp_data", respData)
	req, err := http.NewRequest(http.MethodPost, target.String(), strings.NewReader(form.Encode()))
	if err != nil {
		attempt.Status = "request_error"
		attempt.Error = sanitizePlainLogText(err.Error())
		return attempt
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
	req.Header.Set("User-Agent", appName+"/"+appVersion)
	resp, err := a.doPinned(req, target)
	if err != nil {
		if resp != nil && resp.Body != nil {
			_ = resp.Body.Close()
		}
		attempt.Status = "network_error"
		attempt.Error = sanitizePlainLogText(err.Error())
		if strings.Contains(strings.ToLower(err.Error()), "redirect") {
			attempt.Status = "redirect_blocked"
			a.recordSecurityFinding("notify_redirect_blocked", target.String(), err.Error())
		}
		attempt.Diagnosis = diagnoseNotificationAttempt(attempt, expectedACK)
		return attempt
	}
	defer resp.Body.Close()
	body, readErr := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
	if readErr != nil {
		attempt.Status = "read_error"
		attempt.HTTPStatus = resp.StatusCode
		attempt.Error = sanitizePlainLogText(readErr.Error())
		attempt.Diagnosis = diagnoseNotificationAttempt(attempt, expectedACK)
		return attempt
	}
	attempt.HTTPStatus = resp.StatusCode
	ackBody := string(body)
	attempt.AckBody = sanitizePlainLogText(ackBody)
	if resp.StatusCode == http.StatusOK && ackBody == expectedACK {
		attempt.Status = "ack"
		return attempt
	}
	if resp.StatusCode >= 300 && resp.StatusCode < 400 {
		attempt.Status = "redirect_blocked"
		attempt.Error = "redirect response is not allowed"
		attempt.Diagnosis = diagnoseNotificationAttempt(attempt, expectedACK)
		a.recordSecurityFinding("notify_redirect_blocked", target.String(), attempt.Error)
		return attempt
	}
	attempt.Status = "ack_mismatch"
	attempt.Error = fmt.Sprintf("want HTTP 200 and body %q", expectedACK)
	attempt.Diagnosis = diagnoseNotificationAttempt(attempt, expectedACK)
	return attempt
}

func diagnoseNotificationAttempt(attempt NotificationAttempt, expectedACK string) string {
	context := strings.ToLower(attempt.AckBody + " " + attempt.Error)
	if attempt.HTTPStatus == http.StatusUnsupportedMediaType ||
		strings.Contains(context, "content type") ||
		strings.Contains(context, "unsupported media type") ||
		strings.Contains(context, "form-urlencoded") {
		return "Notify 接收端不支持交易异步通知的表单格式。交易 notify_url 应接收 application/x-www-form-urlencoded 表单参数 sign 和 resp_data；Webhook 才是 application/json 请求体。"
	}
	if attempt.Status == "redirect_blocked" {
		return "Notify 目标返回了重定向；本地沙箱会拦截重定向。请把 notify_url 配成最终接收地址。"
	}
	if attempt.Status == "network_error" {
		return "Notify 目标网络不可达或被本地安全策略拦截。请确认地址能从沙箱进程访问，外部地址需通过 --notify-allow 精确放行。"
	}
	if attempt.Status == "read_error" {
		return "Notify 目标响应体读取失败。请检查接收端是否提前断开连接或返回了异常响应。"
	}
	if attempt.Status == "ack_mismatch" {
		if attempt.HTTPStatus == http.StatusOK {
			return fmt.Sprintf("Notify 接收端返回了 HTTP 200，但响应体必须完全等于 %q。请返回纯文本 ACK，不要包 JSON。", expectedACK)
		}
		return fmt.Sprintf("Notify 接收端必须返回 HTTP 200 且响应体完全等于 %q；当前 HTTP 状态为 %d。", expectedACK, attempt.HTTPStatus)
	}
	return ""
}

func (a *App) storeNotification(delivery NotificationDelivery) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.notifications = append(a.notifications, delivery)
}

func notificationRespData(payment Payment) map[string]any {
	base := map[string]any{
		"resp_code":  "00000000",
		"resp_desc":  "success",
		"huifu_id":   payment.HuifuID,
		"req_date":   payment.ReqDate,
		"req_seq_id": payment.ReqSeqID,
		"hf_seq_id":  payment.HFSeqID,
		"trans_type": paymentNotifyTransType(payment),
		"trans_amt":  payment.TransAmt,
		"trans_stat": payment.State,
	}
	if payment.Kind == "hosting" {
		base["org_req_date"] = payment.ReqDate
		base["org_req_seq_id"] = payment.ReqSeqID
		base["pre_order_id"] = payment.PreOrderID
		base["out_trans_id"] = "OUT-" + payment.ReqSeqID
		base["party_order_id"] = hostingPartyOrderID(payment)
		base["goods_desc"] = payment.GoodsDesc
		return addPaymentExtensions(base, payment)
	}
	base["out_ord_id"] = aggregationOutOrdID(payment)
	base["party_order_id"] = aggregationPartyOrderID(payment)
	base["goods_desc"] = payment.GoodsDesc
	return addPaymentExtensions(base, payment)
}

func paymentNotifyTransType(payment Payment) string {
	if payment.Kind == "hosting" {
		return hostingQueryPayType(payment)
	}
	return firstNonEmpty(payment.TradeType, stringValue(payment.ChannelResponse["trans_type"]))
}

func (a *App) refundNotificationRespData(refund RefundOperation) map[string]any {
	amounts := a.refundNotificationAmounts(refund)
	return addOperationExtensions(map[string]any{
		"resp_code":         "00000000",
		"resp_desc":         "success",
		"product_id":        refund.ProductID,
		"huifu_id":          refund.HuifuID,
		"req_date":          refund.ReqDate,
		"req_seq_id":        refund.ReqSeqID,
		"hf_seq_id":         refund.HFSeqID,
		"org_req_date":      refund.PaymentReqDate,
		"org_req_seq_id":    refund.PaymentReqSeqID,
		"org_hf_seq_id":     refund.PaymentHFSeqID,
		"org_ord_amt":       amounts.orgOrdAmt,
		"org_fee_amt":       "0.00",
		"ord_amt":           refund.OrdAmt,
		"actual_ref_amt":    refund.OrdAmt,
		"total_ref_amt":     amounts.totalRefAmt,
		"total_ref_fee_amt": "0.00",
		"ref_cut":           amounts.refCut,
		"trans_date":        refund.ReqDate,
		"trans_time":        "120000",
		"trans_finish_time": refund.ReqDate + "120000",
		"trans_type":        "TRANS_REFUND",
		"trade_type":        "TRANS_REFUND",
		"trans_stat":        refund.State,
		"party_order_id":    refundPartyOrderID(refund),
		"bank_code":         refundNotifyBankCode(refund.State),
		"bank_message":      refundNotifyBankMessage(refund.State),
		"pay_channel":       refundPayChannel(refund.BusinessVariant),
	}, refund.BusinessVariant, refund.ChannelResponse)
}

type refundNotificationAmounts struct {
	orgOrdAmt   string
	totalRefAmt string
	refCut      string
}

func (a *App) refundNotificationAmounts(refund RefundOperation) refundNotificationAmounts {
	a.mu.Lock()
	defer a.mu.Unlock()

	orgFen := refund.OrdAmtFen
	if payment := a.payments[refund.PaymentReqSeqID]; payment != nil && payment.TransAmtFen > 0 {
		orgFen = payment.TransAmtFen
	}

	totalFen := int64(0)
	refCut := 0
	currentIncluded := false
	for _, stored := range a.refunds {
		if stored == nil || stored.Kind != refund.Kind || stored.PaymentReqSeqID != refund.PaymentReqSeqID || stored.State != "S" {
			continue
		}
		totalFen += stored.OrdAmtFen
		refCut++
		if stored.ReqSeqID == refund.ReqSeqID {
			currentIncluded = true
		}
	}
	if refund.State == "S" && !currentIncluded {
		totalFen += refund.OrdAmtFen
		refCut++
	}
	if refCut == 0 && refund.State == "S" {
		refCut = 1
		totalFen = refund.OrdAmtFen
	}

	return refundNotificationAmounts{
		orgOrdAmt:   formatFen(orgFen),
		totalRefAmt: formatFen(totalFen),
		refCut:      fmt.Sprintf("%d", refCut),
	}
}

func closeNotificationRespData(closeOp CloseOperation) map[string]any {
	base := map[string]any{
		"resp_code":      "00000000",
		"resp_desc":      "success",
		"huifu_id":       closeOp.HuifuID,
		"req_date":       closeOp.ReqDate,
		"req_seq_id":     closeOp.ReqSeqID,
		"org_req_date":   closeOp.PaymentReqDate,
		"org_req_seq_id": closeOp.PaymentReqSeqID,
		"org_trans_stat": "F",
		"trans_stat":     closeOp.State,
		"close_stat":     closeOp.State,
	}
	if closeOp.PaymentHFSeqID != "" {
		base["org_hf_seq_id"] = closeOp.PaymentHFSeqID
	}
	return addOperationExtensions(base, closeOp.BusinessVariant, closeOp.ChannelResponse)
}

func expectedNotifyACK(reqSeqID string) string {
	return "RECV_ORD_ID_" + reqSeqID
}

func refundPartyOrderID(refund RefundOperation) string {
	if refund.Kind == "hosting" {
		return hostingPartyOrderID(Payment{ReqSeqID: refund.PaymentReqSeqID})
	}
	return aggregationPartyOrderID(Payment{ReqSeqID: refund.PaymentReqSeqID})
}

func refundNotifyBankCode(state string) string {
	if state == "S" {
		return "SUCCESS"
	}
	if state == "F" {
		return "FAIL"
	}
	return "PROCESSING"
}

func refundNotifyBankMessage(state string) string {
	if state == "S" {
		return "退款成功"
	}
	if state == "F" {
		return "退款失败"
	}
	return "交易正在处理中"
}
