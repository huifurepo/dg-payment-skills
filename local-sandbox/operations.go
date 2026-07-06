package main

import (
	"errors"
	"net/http"
	"strings"
)

func (a *App) handleAggregationRefund(w http.ResponseWriter, r *http.Request) {
	a.handleRefund(w, r, "aggregation", "/v4/trade/payment/scanpay/refund")
}

func (a *App) handleHostingRefund(w http.ResponseWriter, r *http.Request) {
	a.handleRefund(w, r, "hosting", "/v2/trade/hosting/payment/htRefund")
}

func (a *App) handleAggregationRefundQuery(w http.ResponseWriter, r *http.Request) {
	a.handleRefundQuery(w, r, "aggregation", "/v4/trade/payment/scanpay/refundquery")
}

func (a *App) handleHostingRefundQuery(w http.ResponseWriter, r *http.Request) {
	a.handleRefundQuery(w, r, "hosting", "/v2/trade/hosting/payment/queryRefundInfo")
}

func (a *App) handleAggregationClose(w http.ResponseWriter, r *http.Request) {
	a.handleClose(w, r, "aggregation", "/v2/trade/payment/scanpay/close")
}

func (a *App) handleHostingClose(w http.ResponseWriter, r *http.Request) {
	a.handleClose(w, r, "hosting", "/v2/trade/hosting/payment/close")
}

func (a *App) handleAggregationCloseQuery(w http.ResponseWriter, r *http.Request) {
	env, ok := a.readGatewayEnvelope(w, r, "/v2/trade/payment/scanpay/closequery")
	if !ok {
		return
	}
	normalizeCloseQueryAliases(env.Data)
	if missing := missingFields(env.Data, []string{"huifu_id", "org_req_date"}); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	a.mu.Lock()
	paymentReqSeqID, err := a.findCloseOriginalPaymentKeyLocked("aggregation", env.Data)
	if err == nil {
		closeKey, ok := a.closeIndex[operationKey("aggregation", paymentReqSeqID)]
		if !ok {
			err = errors.New("unknown close operation for original payment")
		} else if closeOp := a.closes[closeKey]; closeOp != nil {
			closeOp.QueryCount++
			if closeOp.QueryCount >= 2 {
				closeOp.State = "S"
				if payment := a.payments[paymentReqSeqID]; payment != nil {
					payment.State = "F"
				}
			}
			closeCopy := *closeOp
			paymentCopy := *a.payments[paymentReqSeqID]
			a.mu.Unlock()
			a.record("close.query", r.URL.Path, closeCopy.ReqSeqID, map[string]any{"kind": "aggregation", "state": closeCopy.State, "query_count": closeCopy.QueryCount})
			if closeCopy.State == "S" {
				a.record("close.settled", r.URL.Path, closeCopy.ReqSeqID, map[string]any{"kind": "aggregation", "payment_req_seq_id": closeCopy.PaymentReqSeqID})
				a.maybeNotifyClose(closeCopy.ReqSeqID, "aggregation")
				a.maybeWebhookClose(closeCopy.ReqSeqID, "aggregation")
			}
			a.writeGatewayData(w, closeQueryResponse(closeCopy, paymentCopy, env.Data, env.ProductID))
			return
		}
	}
	a.mu.Unlock()
	a.writeGatewayData(w, localError("LS000004", err.Error()))
}

func (a *App) handleHostingSplitpayQuery(w http.ResponseWriter, r *http.Request) {
	env, ok := a.readGatewayEnvelope(w, r, "/v2/trade/hosting/payment/splitpay/query")
	if !ok {
		return
	}
	if missing := missingFields(env.Data, []string{"req_date", "req_seq_id", "huifu_id", "org_req_date", "org_req_seq_id"}); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	a.mu.Lock()
	payment, ok := a.payments[stringValue(env.Data["org_req_seq_id"])]
	if !ok || payment.Kind != "hosting" || payment.ReqDate != stringValue(env.Data["org_req_date"]) {
		a.mu.Unlock()
		a.writeGatewayData(w, localError("LS000004", "unknown org_req_date + org_req_seq_id"))
		return
	}
	paymentCopy := *payment
	a.mu.Unlock()
	a.record("splitpay.query", r.URL.Path, paymentCopy.ReqSeqID, map[string]any{"kind": "hosting", "state": paymentCopy.State})
	a.writeGatewayData(w, map[string]any{
		"resp_code":        "00000000",
		"resp_desc":        "查询成功",
		"product_id":       env.ProductID,
		"req_date":         stringValue(env.Data["req_date"]),
		"req_seq_id":       stringValue(env.Data["req_seq_id"]),
		"huifu_id":         firstNonEmpty(stringValue(env.Data["huifu_id"]), paymentCopy.HuifuID),
		"org_req_date":     paymentCopy.ReqDate,
		"org_req_seq_id":   paymentCopy.ReqSeqID,
		"pre_order_id":     paymentCopy.PreOrderID,
		"order_stat":       hostingOrderStat(paymentCopy),
		"business_variant": "hosting.splitpay",
		"trans_list":       hostingSplitpayTransList(paymentCopy),
	})
}

func hostingSplitpayTransList(payment Payment) string {
	return compactJSONString([]map[string]any{
		{
			"pay_type":       "A_NATIVE",
			"org_hf_seq_id":  "ORG-HF-" + payment.ReqSeqID + "-ALI",
			"trans_amt":      "0.10",
			"party_order_id": "PARTY-" + payment.ReqSeqID + "-ALI",
			"fee_amt":        "0.04",
			"ref_amt":        "0.00",
			"trans_stat":     "S",
			"trans_time":     payment.ReqDate + "161340",
			"bank_code":      "TRADE_SUCCESS",
			"bank_desc":      "TRADE_SUCCESS",
			"alipay_response": compactJSONString(map[string]any{
				"buyer_id":       "buyer-ali-splitpay-001",
				"buyer_logon_id": "buyer-ali-splitpay@example.invalid",
			}),
		},
		{
			"pay_type":       "T_MINIAPP",
			"org_hf_seq_id":  "ORG-HF-" + payment.ReqSeqID + "-WX",
			"trans_amt":      "0.05",
			"party_order_id": "PARTY-" + payment.ReqSeqID + "-WX",
			"fee_amt":        "0.03",
			"ref_amt":        "0.00",
			"trans_stat":     "S",
			"trans_time":     payment.ReqDate + "161323",
			"bank_code":      "SUCCESS",
			"bank_desc":      "交易成功",
			"wx_response": compactJSONString(map[string]any{
				"wx_user_id": "",
				"sub_appid":  "wx-local-splitpay",
				"openid":     "openid-wx-splitpay-001",
				"sub_openid": "sub-openid-wx-splitpay-001",
				"bank_type":  "BOSH",
				"coupon_fee": "0.00",
			}),
		},
	})
}

func (a *App) handleRefund(w http.ResponseWriter, r *http.Request, kind, endpoint string) {
	env, ok := a.readGatewayEnvelope(w, r, endpoint)
	if !ok {
		return
	}
	if missing := missingFields(env.Data, []string{"req_date", "req_seq_id", "huifu_id", "ord_amt", "org_req_date"}); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	reqSeqID := stringValue(env.Data["req_seq_id"])
	digest, err := dataDigest(env.Data)
	if err != nil {
		a.writeGatewayData(w, localError("LS000005", "request digest failed"))
		return
	}
	ordFen, err := parseAmountFen(stringValue(env.Data["ord_amt"]))
	if err != nil {
		a.writeGatewayData(w, localError("LS000005", "invalid ord_amt: "+err.Error()))
		return
	}
	a.mu.Lock()
	if refund, ok := a.refunds[operationKey(kind, reqSeqID)]; ok {
		refundCopy := *refund
		a.mu.Unlock()
		if refundCopy.RequestDigest != digest {
			a.record("idempotency.conflict", r.URL.Path, reqSeqID, map[string]any{"kind": kind, "entity": "refund"})
			a.writeGatewayData(w, localError("LS000006", "idempotency conflict: same refund req_seq_id with different payload"))
			return
		}
		a.record("refund.idempotent_replay", r.URL.Path, reqSeqID, map[string]any{"kind": kind, "state": refundCopy.State})
		a.writeGatewayData(w, refundAcceptedResponse(refundCopy))
		return
	}
	paymentReqSeqID, err := a.findRefundOriginalPaymentKeyLocked(kind, env.Data)
	if err != nil {
		a.mu.Unlock()
		a.writeGatewayData(w, localError("LS000004", err.Error()))
		return
	}
	payment := a.payments[paymentReqSeqID]
	if payment.State != "S" {
		a.mu.Unlock()
		a.writeGatewayData(w, localError("LS200002", "refund requires successful original payment"))
		return
	}
	pendingFen := a.pendingRefundFenLocked(kind, payment.ReqSeqID)
	if ordFen > payment.TransAmtFen-payment.RefundedFen-pendingFen {
		paymentCopy := *payment
		a.mu.Unlock()
		if kind == "aggregation" {
			a.writeGatewayData(w, aggregationRefundRejectedResponse(env.Data, paymentCopy, "23000003", "申请退款金额大于可退款余额"))
			return
		}
		a.writeGatewayData(w, localError("LS200003", "refund amount exceeds refundable amount"))
		return
	}
	refund := &RefundOperation{
		Kind:              kind,
		ProductID:         env.ProductID,
		HuifuID:           stringValue(env.Data["huifu_id"]),
		ReqDate:           stringValue(env.Data["req_date"]),
		ReqSeqID:          reqSeqID,
		HFSeqID:           nextID("RF"),
		MerOrdID:          stringValue(env.Data["mer_ord_id"]),
		PaymentReqSeqID:   payment.ReqSeqID,
		PaymentReqDate:    payment.ReqDate,
		PaymentHFSeqID:    payment.HFSeqID,
		PaymentPreOrderID: payment.PreOrderID,
		OrdAmt:            stringValue(env.Data["ord_amt"]),
		OrdAmtFen:         ordFen,
		NotifyURL:         firstNonEmpty(stringValue(env.Data["refund_notify_url"]), stringValue(env.Data["notify_url"]), payment.NotifyURL),
		RequestDigest:     digest,
		State:             "P",
		BusinessVariant:   payment.BusinessVariant,
		ChannelResponse:   refundChannelResponse(kind, payment.BusinessVariant, payment.ChannelResponse, stringValue(env.Data["ord_amt"])),
	}
	key := operationKey(kind, refund.ReqSeqID)
	a.refunds[key] = refund
	a.refundHFIndex[refund.HFSeqID] = key
	if refund.MerOrdID != "" {
		a.refundMerIndex[operationKey(kind, refund.MerOrdID)] = key
	}
	refundCopy := *refund
	a.mu.Unlock()
	a.record("refund.accepted", r.URL.Path, refundCopy.ReqSeqID, map[string]any{"kind": kind, "state": "P", "payment_req_seq_id": refundCopy.PaymentReqSeqID})
	a.writeGatewayData(w, refundAcceptedResponse(refundCopy))
}

func (a *App) handleRefundQuery(w http.ResponseWriter, r *http.Request, kind, endpoint string) {
	env, ok := a.readGatewayEnvelope(w, r, endpoint)
	if !ok {
		return
	}
	required := []string{"huifu_id"}
	if kind == "hosting" {
		required = []string{"req_date", "req_seq_id", "huifu_id", "org_req_date"}
	}
	if missing := missingFields(env.Data, required); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	a.mu.Lock()
	refund, err := a.findRefundLocked(kind, env.Data)
	if err != nil {
		a.mu.Unlock()
		if kind == "aggregation" && hasRefundQueryLocator(env.Data) {
			a.writeGatewayData(w, aggregationRefundQueryNotFoundResponse(env.Data))
			return
		}
		a.writeGatewayData(w, localError("LS000004", err.Error()))
		return
	}
	refund.QueryCount++
	if refund.QueryCount >= 2 {
		refund.State = "S"
	}
	if refund.State == "S" && !refund.Settled {
		if payment := a.payments[refund.PaymentReqSeqID]; payment != nil {
			payment.RefundedFen += refund.OrdAmtFen
			payment.RefundableFen -= refund.OrdAmtFen
			payment.RefundedAmt = formatFen(payment.RefundedFen)
			payment.RefundableAmt = formatFen(payment.RefundableFen)
			refund.Settled = true
		}
	}
	refundCopy := *refund
	a.mu.Unlock()
	a.record("refund.query", r.URL.Path, refundCopy.ReqSeqID, map[string]any{"kind": kind, "state": refundCopy.State, "query_count": refundCopy.QueryCount})
	if refundCopy.State == "S" {
		a.record("refund.settled", r.URL.Path, refundCopy.ReqSeqID, map[string]any{"kind": kind, "payment_req_seq_id": refundCopy.PaymentReqSeqID})
		a.maybeNotifyRefund(refundCopy.ReqSeqID, kind)
		a.maybeWebhookRefund(refundCopy.ReqSeqID, kind)
	}
	a.writeGatewayData(w, refundQueryResponse(refundCopy))
}

func (a *App) handleClose(w http.ResponseWriter, r *http.Request, kind, endpoint string) {
	env, ok := a.readGatewayEnvelope(w, r, endpoint)
	if !ok {
		return
	}
	if missing := missingFields(env.Data, []string{"req_date", "req_seq_id", "huifu_id", "org_req_date"}); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	reqSeqID := stringValue(env.Data["req_seq_id"])
	digest, err := dataDigest(env.Data)
	if err != nil {
		a.writeGatewayData(w, localError("LS000005", "request digest failed"))
		return
	}
	a.mu.Lock()
	if closeOp, ok := a.closes[operationKey(kind, reqSeqID)]; ok {
		closeCopy := *closeOp
		paymentCopy := Payment{State: ""}
		if payment := a.payments[closeOp.PaymentReqSeqID]; payment != nil {
			paymentCopy = *payment
		}
		a.mu.Unlock()
		if closeCopy.RequestDigest != digest {
			a.record("idempotency.conflict", r.URL.Path, reqSeqID, map[string]any{"kind": kind, "entity": "close"})
			a.writeGatewayData(w, localError("LS000006", "idempotency conflict: same close req_seq_id with different payload"))
			return
		}
		a.record("close.idempotent_replay", r.URL.Path, reqSeqID, map[string]any{"kind": kind, "state": closeCopy.State})
		a.writeGatewayData(w, closeAcceptedResponse(closeCopy, paymentCopy))
		return
	}
	paymentReqSeqID, err := a.findCloseOriginalPaymentKeyLocked(kind, env.Data)
	if err != nil {
		a.mu.Unlock()
		a.writeGatewayData(w, localError("LS000004", err.Error()))
		return
	}
	payment := a.payments[paymentReqSeqID]
	if kind == "aggregation" && payment.State == "S" {
		a.mu.Unlock()
		a.writeGatewayData(w, localError("LS200004", "successful aggregation payment cannot be closed"))
		return
	}
	if _, exists := a.closeIndex[operationKey(kind, paymentReqSeqID)]; exists {
		a.mu.Unlock()
		a.writeGatewayData(w, localError("LS200005", "close operation already exists for original payment"))
		return
	}
	closeOp := &CloseOperation{
		Kind:            kind,
		HuifuID:         stringValue(env.Data["huifu_id"]),
		ReqDate:         stringValue(env.Data["req_date"]),
		ReqSeqID:        reqSeqID,
		PaymentReqSeqID: payment.ReqSeqID,
		PaymentReqDate:  payment.ReqDate,
		PaymentHFSeqID:  payment.HFSeqID,
		NotifyURL:       payment.NotifyURL,
		State:           "P",
		RequestDigest:   digest,
		BusinessVariant: payment.BusinessVariant,
		ChannelResponse: copyMap(payment.ChannelResponse),
	}
	if kind == "hosting" {
		closeOp.State = "S"
		payment.State = "F"
	}
	key := operationKey(kind, closeOp.ReqSeqID)
	a.closes[key] = closeOp
	a.closeIndex[operationKey(kind, paymentReqSeqID)] = key
	closeCopy := *closeOp
	paymentCopy := *payment
	a.mu.Unlock()
	a.record("close.accepted", r.URL.Path, closeCopy.ReqSeqID, map[string]any{"kind": kind, "state": closeCopy.State, "payment_req_seq_id": closeCopy.PaymentReqSeqID})
	if closeCopy.State == "S" {
		a.maybeNotifyClose(closeCopy.ReqSeqID, kind)
		a.maybeWebhookClose(closeCopy.ReqSeqID, kind)
	}
	a.writeGatewayData(w, closeAcceptedResponse(closeCopy, paymentCopy))
}

func (a *App) advanceHostingCloseLocked(paymentReqSeqID string) string {
	closeKey, ok := a.closeIndex[operationKey("hosting", paymentReqSeqID)]
	if !ok {
		return ""
	}
	closeOp := a.closes[closeKey]
	if closeOp == nil {
		return ""
	}
	closeOp.QueryCount++
	closeOp.State = "S"
	if payment := a.payments[paymentReqSeqID]; payment != nil {
		payment.State = "F"
	}
	return closeOp.State
}

func (a *App) findRefundOriginalPaymentKeyLocked(kind string, data map[string]any) (string, error) {
	if hfSeqID := stringValue(data["org_hf_seq_id"]); hfSeqID != "" {
		reqSeqID, err := a.findPaymentByHFSeqIDLocked(kind, hfSeqID)
		if err != nil {
			return "", err
		}
		return reqSeqID, nil
	}
	if partyOrderID := stringValue(data["org_party_order_id"]); partyOrderID != "" {
		reqSeqID, err := a.findPaymentByPartyOrderIDLocked(kind, partyOrderID)
		if err != nil {
			return "", err
		}
		return reqSeqID, nil
	}
	reqSeqID := stringValue(data["org_req_seq_id"])
	reqDate := stringValue(data["org_req_date"])
	if reqSeqID == "" || reqDate == "" {
		if kind == "aggregation" {
			return "", errors.New("requires org_req_date and org_req_seq_id, org_hf_seq_id, or org_party_order_id")
		}
		return "", errors.New("requires org_req_date and org_req_seq_id, org_hf_seq_id, or org_party_order_id")
	}
	payment := a.payments[reqSeqID]
	if payment == nil || payment.Kind != kind || payment.ReqDate != reqDate {
		return "", errors.New("unknown org_req_date + org_req_seq_id")
	}
	return reqSeqID, nil
}

func (a *App) findCloseOriginalPaymentKeyLocked(kind string, data map[string]any) (string, error) {
	if kind == "aggregation" {
		if hfSeqID := stringValue(data["org_hf_seq_id"]); hfSeqID != "" {
			reqSeqID, err := a.findPaymentByHFSeqIDLocked(kind, hfSeqID)
			if err != nil {
				return "", err
			}
			return reqSeqID, nil
		}
	}
	reqSeqID := stringValue(data["org_req_seq_id"])
	reqDate := stringValue(data["org_req_date"])
	if reqSeqID == "" || reqDate == "" {
		if kind == "aggregation" {
			return "", errors.New("requires org_req_date and org_req_seq_id or org_hf_seq_id")
		}
		return "", errors.New("requires org_req_date and org_req_seq_id")
	}
	payment := a.payments[reqSeqID]
	if payment == nil || payment.Kind != kind || payment.ReqDate != reqDate {
		return "", errors.New("unknown org_req_date + org_req_seq_id")
	}
	return reqSeqID, nil
}

func (a *App) findPaymentByHFSeqIDLocked(kind, hfSeqID string) (string, error) {
	reqSeqID, ok := a.hfIndex[hfSeqID]
	if !ok {
		return "", errors.New("unknown org_hf_seq_id")
	}
	payment := a.payments[reqSeqID]
	if payment == nil || payment.Kind != kind {
		return "", errors.New("unknown org_hf_seq_id")
	}
	return reqSeqID, nil
}

func (a *App) findHostingPaymentByPartyOrderIDLocked(partyOrderID string) (string, error) {
	return a.findPaymentByPartyOrderIDLocked("hosting", partyOrderID)
}

func (a *App) findPaymentByPartyOrderIDLocked(kind, partyOrderID string) (string, error) {
	for reqSeqID, payment := range a.payments {
		if payment == nil || payment.Kind != kind {
			continue
		}
		if kind == "hosting" && hostingPartyOrderID(*payment) == partyOrderID {
			return reqSeqID, nil
		}
		if kind == "aggregation" && aggregationPartyOrderID(*payment) == partyOrderID {
			return reqSeqID, nil
		}
	}
	return "", errors.New("unknown party_order_id")
}

func (a *App) findRefundLocked(kind string, data map[string]any) (*RefundOperation, error) {
	reqDate := stringValue(data["org_req_date"])
	if hfSeqID := stringValue(data["org_hf_seq_id"]); hfSeqID != "" {
		key, ok := a.refundHFIndex[hfSeqID]
		if !ok {
			return nil, errors.New("unknown refund org_hf_seq_id")
		}
		refund := a.refunds[key]
		if refund == nil || refund.Kind != kind {
			return nil, errors.New("unknown refund org_hf_seq_id")
		}
		if kind == "hosting" && refund.ReqDate != reqDate {
			return nil, errors.New("unknown refund org_req_date + org_hf_seq_id")
		}
		return refund, nil
	}
	if kind == "aggregation" {
		if merOrdID := stringValue(data["mer_ord_id"]); merOrdID != "" {
			key, ok := a.refundMerIndex[operationKey(kind, merOrdID)]
			if !ok {
				return nil, errors.New("unknown refund mer_ord_id")
			}
			return a.refunds[key], nil
		}
	}
	reqSeqID := stringValue(data["org_req_seq_id"])
	if reqSeqID == "" {
		if kind == "hosting" {
			return nil, errors.New("refund query requires org_hf_seq_id or org_req_seq_id")
		}
		return nil, errors.New("refund query requires org_hf_seq_id, mer_ord_id, or org_req_seq_id")
	}
	refund := a.refunds[operationKey(kind, reqSeqID)]
	if refund == nil || refund.Kind != kind {
		return nil, errors.New("unknown refund org_req_seq_id")
	}
	if reqDate != "" && refund.ReqDate != reqDate {
		return nil, errors.New("unknown refund org_req_date + org_req_seq_id")
	}
	return refund, nil
}

func hasRefundQueryLocator(data map[string]any) bool {
	return stringValue(data["org_hf_seq_id"]) != "" || stringValue(data["mer_ord_id"]) != "" || stringValue(data["org_req_seq_id"]) != ""
}

func (a *App) pendingRefundFenLocked(kind, paymentReqSeqID string) int64 {
	total := int64(0)
	for _, refund := range a.refunds {
		if refund.Kind == kind && refund.PaymentReqSeqID == paymentReqSeqID && refund.State != "S" {
			total += refund.OrdAmtFen
		}
	}
	return total
}

func refundAcceptedResponse(refund RefundOperation) map[string]any {
	if refund.Kind == "aggregation" {
		return aggregationRefundAcceptedResponse(refund)
	}
	return addOperationExtensions(map[string]any{
		"resp_code":      "00000000",
		"resp_desc":      "操作成功",
		"product_id":     refund.ProductID,
		"req_date":       refund.ReqDate,
		"req_seq_id":     refund.ReqSeqID,
		"huifu_id":       refund.HuifuID,
		"hf_seq_id":      refund.HFSeqID,
		"org_req_date":   refund.PaymentReqDate,
		"org_req_seq_id": refund.PaymentReqSeqID,
		"org_hf_seq_id":  refund.PaymentHFSeqID,
		"ord_amt":        refund.OrdAmt,
		"trans_time":     refund.ReqDate + "120000",
		"trans_stat":     refund.State,
		"bank_code":      "00000100",
		"bank_message":   "交易正在处理中",
		"fee_amt":        hostingRefundFeeAmount(refund),
		"pay_channel":    refundPayChannel(refund.BusinessVariant),
	}, refund.BusinessVariant, refund.ChannelResponse)
}

func aggregationRefundAcceptedResponse(refund RefundOperation) map[string]any {
	out := map[string]any{
		"resp_code":      "00000100",
		"resp_desc":      "交易处理中",
		"req_date":       refund.ReqDate,
		"req_seq_id":     refund.ReqSeqID,
		"huifu_id":       refund.HuifuID,
		"hf_seq_id":      refund.HFSeqID,
		"org_req_date":   refund.PaymentReqDate,
		"org_req_seq_id": refund.PaymentReqSeqID,
		"org_hf_seq_id":  refund.PaymentHFSeqID,
		"ord_amt":        refund.OrdAmt,
		"trans_stat":     refund.State,
		"trade_type":     "TRANS_REFUND",
		"trans_date":     refund.ReqDate,
		"trans_time":     "120000",
		"pay_channel":    refundPayChannel(refund.BusinessVariant),
		"bank_message":   "",
		"remark":         "",
		"fee_amount":     refundFeeAmount(refund.OrdAmt),
		"acct_split_bunch": compactJSONString(map[string]any{
			"acct_infos": []map[string]any{
				{
					"div_amt":  refund.OrdAmt,
					"huifu_id": refund.HuifuID,
				},
			},
			"fee_amount": refundFeeAmount(refund.OrdAmt),
		}),
	}
	if refund.BusinessVariant != "" {
		out["business_variant"] = refund.BusinessVariant
	}
	return out
}

func aggregationRefundRejectedResponse(data map[string]any, payment Payment, code, desc string) map[string]any {
	out := map[string]any{
		"resp_code":      code,
		"resp_desc":      desc,
		"sub_resp_code":  code,
		"sub_resp_desc":  desc,
		"req_date":       stringValue(data["req_date"]),
		"req_seq_id":     stringValue(data["req_seq_id"]),
		"huifu_id":       stringValue(data["huifu_id"]),
		"hf_seq_id":      payment.HFSeqID,
		"org_req_date":   firstNonEmpty(stringValue(data["org_req_date"]), payment.ReqDate),
		"org_req_seq_id": payment.ReqSeqID,
		"org_hf_seq_id":  payment.HFSeqID,
		"ord_amt":        stringValue(data["ord_amt"]),
		"trans_stat":     "F",
		"trade_type":     "TRANS_REFUND",
		"trans_date":     stringValue(data["req_date"]),
		"pay_channel":    refundPayChannel(payment.BusinessVariant),
		"loan_flag":      "N",
	}
	if payment.BusinessVariant != "" {
		out["business_variant"] = payment.BusinessVariant
	}
	return out
}

func refundQueryResponse(refund RefundOperation) map[string]any {
	if refund.Kind == "aggregation" {
		return addOperationExtensions(map[string]any{
			"resp_code":           "00000000",
			"resp_desc":           "查询成功",
			"req_date":            nowDate(),
			"req_seq_id":          nextID("RQ"),
			"huifu_id":            refund.HuifuID,
			"org_req_date":        refund.ReqDate,
			"org_req_seq_id":      refund.ReqSeqID,
			"org_hf_seq_id":       refund.HFSeqID,
			"ord_amt":             refund.OrdAmt,
			"actual_ref_amt":      refund.OrdAmt,
			"fee_amount":          refundFeeAmount(refund.OrdAmt),
			"combinedpay_fee_amt": "0.00",
			"pay_channel":         refundPayChannel(refund.BusinessVariant),
			"trade_type":          "TRANS_REFUND",
			"trans_date":          refund.ReqDate,
			"trans_time":          "120000",
			"trans_finish_time":   refund.ReqDate + "120000",
			"trans_stat":          refund.State,
			"remark":              "",
			"bank_message":        refundQueryBankMessage(refund.State),
			"acct_split_bunch":    refundAcctSplitBunch(refund),
			"business_variant":    refund.BusinessVariant,
		}, refund.BusinessVariant, refund.ChannelResponse)
	}
	return addOperationExtensions(map[string]any{
		"resp_code":          "00000000",
		"resp_desc":          "操作成功",
		"product_id":         refund.ProductID,
		"req_date":           nowDate(),
		"req_seq_id":         nextID("RQ"),
		"huifu_id":           refund.HuifuID,
		"org_req_date":       refund.ReqDate,
		"org_req_seq_id":     refund.ReqSeqID,
		"org_hf_seq_id":      refund.HFSeqID,
		"ord_amt":            refund.OrdAmt,
		"actual_ref_amt":     refund.OrdAmt,
		"trans_stat":         refund.State,
		"bank_code":          hostingRefundBankCode(refund.State),
		"bank_message":       hostingRefundBankMessage(refund.State),
		"fee_amt":            hostingRefundFeeAmount(refund),
		"acct_split_bunch":   hostingRefundAcctSplitBunch(refund),
		"split_fee_info":     hostingRefundSplitFeeInfo(refund),
		"org_party_order_id": "PARTY-" + refund.PaymentReqSeqID,
		"org_out_order_id":   "ORDER-" + refund.PaymentReqSeqID,
		"trans_finish_time":  refund.ReqDate + "120000",
		"pay_channel":        refundPayChannel(refund.BusinessVariant),
	}, refund.BusinessVariant, refund.ChannelResponse)
}

func hostingPartyOrderID(payment Payment) string {
	return "PARTY-" + payment.ReqSeqID
}

func aggregationPartyOrderID(payment Payment) string {
	return "PARTY-" + payment.ReqSeqID
}

func aggregationOutOrdID(payment Payment) string {
	return "OUT-" + payment.ReqSeqID
}

func hostingOrderStat(payment Payment) string {
	switch payment.State {
	case "S":
		if payment.RefundedFen > 0 && payment.RefundableFen <= 0 {
			return "3"
		}
		if payment.RefundedFen > 0 {
			return "6"
		}
		return "1"
	case "F":
		return "5"
	case "P":
		return "2"
	default:
		return "4"
	}
}

func hostingOrderStatFromTransState(state string) string {
	switch state {
	case "S":
		return "1"
	case "F":
		return "5"
	case "P":
		return "2"
	default:
		return "4"
	}
}

func aggregationRefundQueryNotFoundResponse(data map[string]any) map[string]any {
	return map[string]any{
		"resp_code":      "23000001",
		"resp_desc":      "原交易不存在",
		"huifu_id":       stringValue(data["huifu_id"]),
		"org_req_date":   stringValue(data["org_req_date"]),
		"org_req_seq_id": stringValue(data["org_req_seq_id"]),
		"trade_type":     "",
	}
}

func refundPayChannel(businessVariant string) string {
	switch businessVariant {
	case "aggregation.wechat":
		return "T"
	case "aggregation.alipay":
		return "A"
	case "aggregation.unionpay":
		return "U"
	case "hosting.h5pc.wechat", "hosting.wechat-mini":
		return "T"
	case "hosting.h5pc.alipay", "hosting.alipay-mini":
		return "A"
	case "hosting.h5pc.unionpay":
		return "U"
	default:
		return ""
	}
}

func refundChannelResponse(kind, businessVariant string, paymentChannelResponse map[string]any, ordAmt string) map[string]any {
	out := copyMap(paymentChannelResponse)
	if kind != "hosting" {
		return out
	}
	if out == nil {
		out = map[string]any{}
	}
	switch refundPayChannel(businessVariant) {
	case "T":
		out["wx_response"] = compactJSONString(map[string]any{
			"cash_refund_fee":       ordAmt,
			"coupon_refund_fee":     "0.00",
			"user_received_account": "支付用户零钱",
		})
	case "A":
		out["alipay_response"] = compactJSONString(map[string]any{
			"refund_detail_item_list": []map[string]any{
				{"amount": ordAmt, "fund_channel": "ALIPAYACCOUNT"},
			},
		})
	case "U":
		out["unionpay_response"] = compactJSONString(map[string]any{
			"refund_amount": ordAmt,
			"refund_status": "SUCCESS",
		})
	}
	return out
}

func hostingRefundFeeAmount(refund RefundOperation) string {
	if refund.OrdAmtFen <= 0 {
		return "0.00"
	}
	return "0.03"
}

func hostingRefundBankCode(state string) string {
	if state == "S" {
		return "SUCCESS"
	}
	return "00000100"
}

func hostingRefundBankMessage(state string) string {
	if state == "S" {
		return "退款成功"
	}
	return "交易正在处理中"
}

func hostingRefundAcctSplitBunch(refund RefundOperation) string {
	first := refund.OrdAmtFen * 2 / 5
	second := refund.OrdAmtFen * 2 / 5
	third := refund.OrdAmtFen - first - second
	return compactJSONString(map[string]any{
		"acct_infos": []map[string]any{
			{"div_amt": formatFen(first), "huifu_id": refund.HuifuID + "-SPLIT-01", "acct_id": "F-HOST-RF-001"},
			{"div_amt": formatFen(second), "huifu_id": refund.HuifuID + "-SPLIT-02", "acct_id": "F-HOST-RF-002"},
			{"div_amt": formatFen(third), "huifu_id": refund.HuifuID, "acct_id": "F-HOST-RF-003"},
		},
	})
}

func hostingRefundSplitFeeInfo(refund RefundOperation) string {
	return compactJSONString(map[string]any{
		"total_split_fee_amt": 0,
		"split_fee_details": []map[string]any{
			{"split_fee_amt": "0.00", "split_fee_huifu_id": refund.HuifuID + "-SPLIT-01", "split_fee_acct_id": "F-HOST-RF-001"},
			{"split_fee_amt": "0.00", "split_fee_huifu_id": refund.HuifuID + "-SPLIT-02", "split_fee_acct_id": "F-HOST-RF-002"},
		},
	})
}

func refundFeeAmount(ordAmt string) string {
	fen, err := parseAmountFen(ordAmt)
	if err != nil {
		return "0.00"
	}
	return formatFen(fen * 3 / 1000)
}

func refundAcctSplitBunch(refund RefundOperation) string {
	return compactJSONString(map[string]any{
		"acct_infos": []map[string]any{
			{
				"div_amt":  refund.OrdAmt,
				"huifu_id": refund.HuifuID,
			},
		},
	})
}

func refundQueryBankMessage(state string) string {
	if state == "S" {
		return "退款成功"
	}
	return ""
}

func closeAcceptedResponse(closeOp CloseOperation, payment Payment) map[string]any {
	respDesc := "close accepted"
	if closeOp.Kind == "hosting" {
		respDesc = "操作成功"
	}
	return addOperationExtensions(map[string]any{
		"resp_code":      "00000000",
		"resp_desc":      respDesc,
		"req_date":       closeOp.ReqDate,
		"req_seq_id":     closeOp.ReqSeqID,
		"huifu_id":       closeOp.HuifuID,
		"org_req_date":   closeOp.PaymentReqDate,
		"org_req_seq_id": closeOp.PaymentReqSeqID,
		"org_trans_stat": payment.State,
		"trans_stat":     closeOp.State,
		"close_stat":     closeOp.State,
	}, firstNonEmpty(closeOp.BusinessVariant, payment.BusinessVariant), firstNonNilMap(closeOp.ChannelResponse, payment.ChannelResponse))
}

func closeQueryResponse(closeOp CloseOperation, payment Payment, queryData map[string]any, productID string) map[string]any {
	reqDate := firstNonEmpty(stringValue(queryData["req_date"]), nowDate())
	reqSeqID := firstNonEmpty(stringValue(queryData["req_seq_id"]), nextID("CQ"))
	huifuID := firstNonEmpty(stringValue(queryData["huifu_id"]), closeOp.HuifuID)
	productID = firstNonEmpty(stringValue(queryData["product_id"]), productID)
	orgTransStat := payment.State
	resp := map[string]any{
		"resp_code":      "00000000",
		"resp_desc":      "查询成功",
		"req_date":       reqDate,
		"req_seq_id":     reqSeqID,
		"huifu_id":       huifuID,
		"org_req_date":   closeOp.PaymentReqDate,
		"org_req_seq_id": closeOp.PaymentReqSeqID,
		"org_hf_seq_id":  closeOp.PaymentHFSeqID,
		"org_trans_stat": orgTransStat,
		"sub_resp_code":  "00000000",
		"sub_resp_desc":  "查询成功",
		"trans_stat":     closeOp.State,
		"close_stat":     closeOp.State,
		"huifuId":        huifuID,
		"orgHfSeqId":     closeOp.PaymentHFSeqID,
		"orgReqDate":     closeOp.PaymentReqDate,
		"orgReqSeqId":    closeOp.PaymentReqSeqID,
		"orgTransStat":   orgTransStat,
		"reqDate":        reqDate,
		"reqSeqId":       reqSeqID,
		"subRespCode":    "00000000",
		"subRespDesc":    "查询成功",
		"transStat":      closeOp.State,
	}
	if productID != "" {
		resp["product_id"] = productID
		resp["productId"] = productID
	}
	return addOperationExtensions(resp, firstNonEmpty(closeOp.BusinessVariant, payment.BusinessVariant), firstNonNilMap(closeOp.ChannelResponse, payment.ChannelResponse))
}

func normalizeCloseQueryAliases(data map[string]any) {
	copyAlias(data, "huifu_id", "huifuId")
	copyAlias(data, "org_hf_seq_id", "orgHfSeqId")
	copyAlias(data, "org_req_date", "orgReqDate")
	copyAlias(data, "org_req_seq_id", "orgReqSeqId")
	copyAlias(data, "product_id", "productId")
	copyAlias(data, "req_date", "reqDate")
	copyAlias(data, "req_seq_id", "reqSeqId")
}

func copyAlias(data map[string]any, snake, camel string) {
	if data == nil || stringValue(data[snake]) != "" || stringValue(data[camel]) == "" {
		return
	}
	data[snake] = data[camel]
}

func operationKey(kind, id string) string {
	return kind + ":" + id
}

func firstNonEmpty(values ...string) string {
	for _, value := range values {
		if value != "" {
			return value
		}
	}
	return ""
}
