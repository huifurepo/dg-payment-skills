package main

import (
	"encoding/json"
	"fmt"
	"sort"
	"strings"
)

type businessValidationError struct {
	code string
	msg  string
}

func (e businessValidationError) Error() string {
	return e.msg
}

func aggregationBusinessFields(data map[string]any) (string, map[string]any, map[string]any, error) {
	tradeType := strings.ToUpper(strings.TrimSpace(stringValue(data["trade_type"])))
	if stringValue(data["tx_metadata"]) != "" {
		return "", nil, nil, businessValidationError{code: "LS200008", msg: "tx_metadata must not be sent as a request wrapper"}
	}
	txMetadata, err := topLevelTxMetadata(data)
	if err != nil {
		return "", nil, nil, businessValidationError{code: "LS200008", msg: err.Error()}
	}
	variant := aggregationVariant(tradeType)
	channelResponse := map[string]any{}
	methodExpandRaw := stringValue(data["method_expand"])
	if methodExpandRaw != "" || isAggregationMicropay(tradeType) {
		methodExpand, err := parseJSONStringObject(methodExpandRaw)
		if err != nil {
			return "", nil, nil, businessValidationError{code: "LS200007", msg: "method_expand must be a JSON object string"}
		}
		if isAggregationMicropay(tradeType) && stringValue(methodExpand["auth_code"]) == "" {
			return "", nil, nil, businessValidationError{code: "LS200007", msg: "micropay method_expand.auth_code is required"}
		}
		channelResponse["method_expand"] = methodExpand
	}
	if key := aggregationChannelResponseKey(tradeType); key != "" {
		channelResponse[key] = compactJSONString(aggregationChannelPayload(tradeType))
	}
	return variant, txMetadata, channelResponse, nil
}

func hostingBusinessFields(data map[string]any) (string, map[string]any, error) {
	preOrderType := strings.TrimSpace(stringValue(data["pre_order_type"]))
	channelResponse := map[string]any{}
	for _, field := range []string{"wx_data", "alipay_data", "unionpay_data", "dy_data", "terminal_device_data", "largeamt_data", "app_data", "miniapp_data", "acct_split_bunch"} {
		if stringValue(data[field]) == "" {
			continue
		}
		if _, err := parseJSONStringObject(stringValue(data[field])); err != nil {
			return "", nil, businessValidationError{code: "LS200009", msg: field + " must be a JSON object string"}
		}
	}
	addHostingPreorderEchoFields(channelResponse, data)
	switch preOrderType {
	case "1":
		if stringValue(data["wx_data"]) != "" {
			channelResponse["wx_response"] = compactJSONString(hostingChannelPayload("wx"))
		}
		if stringValue(data["alipay_data"]) != "" {
			channelResponse["alipay_response"] = compactJSONString(hostingChannelPayload("alipay"))
		}
		if stringValue(data["unionpay_data"]) != "" {
			channelResponse["unionpay_response"] = compactJSONString(hostingChannelPayload("unionpay"))
		}
		if stringValue(data["dy_data"]) != "" {
			channelResponse["dy_response"] = compactJSONString(hostingChannelPayload("dy"))
		}
		if stringValue(data["largeamt_data"]) != "" {
			channelResponse["largeamt_response"] = compactJSONString(hostingChannelPayload("largeamt"))
		}
		if stringValue(data["terminal_device_data"]) != "" {
			channelResponse["terminal_device_response"] = compactJSONString(hostingChannelPayload("terminal_device"))
		}
		return hostingVariant(preOrderType, data), channelResponse, nil
	case "2":
		if stringValue(data["app_data"]) == "" {
			return "", nil, businessValidationError{code: "LS200009", msg: "pre_order_type=2 requires app_data"}
		}
		channelResponse["alipay_response"] = compactJSONString(hostingChannelPayload("alipay"))
		return "hosting.alipay-mini", channelResponse, nil
	case "3":
		if stringValue(data["miniapp_data"]) == "" {
			return "", nil, businessValidationError{code: "LS200009", msg: "pre_order_type=3 requires miniapp_data"}
		}
		channelResponse["miniapp_data"] = compactJSONString(hostingMiniappPayload(data))
		channelResponse["wx_response"] = compactJSONString(hostingChannelPayload("wx"))
		return "hosting.wechat-mini", channelResponse, nil
	case "4":
		if stringValue(data["dy_data"]) == "" {
			return "", nil, businessValidationError{code: "LS200009", msg: "pre_order_type=4 requires dy_data"}
		}
		channelResponse["dy_response"] = compactJSONString(hostingChannelPayload("dy"))
		return "hosting.douyin-direct", channelResponse, nil
	default:
		return "", nil, businessValidationError{code: "LS200009", msg: "unsupported pre_order_type " + preOrderType}
	}
}

func topLevelTxMetadata(data map[string]any) (map[string]any, error) {
	out := map[string]any{}
	for _, field := range []string{"acct_split_bunch", "terminal_device_data", "combinedpay_data", "combinedpay_data_fee_info", "trans_fee_allowance_info"} {
		value, ok := data[field]
		if !ok || stringValue(value) == "" {
			continue
		}
		parsed, err := parseJSONValue(value)
		if err != nil {
			return nil, fmt.Errorf("%s must be a JSON value string", field)
		}
		out[field] = parsed
	}
	return out, nil
}

func parseJSONValue(value any) (any, error) {
	raw, ok := value.(string)
	if !ok {
		return value, nil
	}
	var out any
	if err := json.Unmarshal([]byte(raw), &out); err != nil {
		return nil, err
	}
	return out, nil
}

func aggregationVariant(tradeType string) string {
	switch {
	case strings.HasPrefix(tradeType, "T_"):
		return "aggregation.wechat"
	case strings.HasPrefix(tradeType, "A_"):
		return "aggregation.alipay"
	case strings.HasPrefix(tradeType, "U_"):
		return "aggregation.unionpay"
	default:
		return "aggregation.generic"
	}
}

func hostingVariant(preOrderType string, data map[string]any) string {
	if preOrderType == "1" && isHostingMultiPay(data) {
		return "hosting.h5pc.multi-pay"
	}
	switch {
	case stringValue(data["wx_data"]) != "":
		return "hosting.h5pc.wechat"
	case stringValue(data["alipay_data"]) != "":
		return "hosting.h5pc.alipay"
	case stringValue(data["unionpay_data"]) != "":
		return "hosting.h5pc.unionpay"
	case stringValue(data["dy_data"]) != "":
		return "hosting.h5pc.douyin"
	case stringValue(data["largeamt_data"]) != "":
		return "hosting.h5pc.largeamt"
	case stringValue(data["terminal_device_data"]) != "":
		return "hosting.h5pc.terminal"
	default:
		return "hosting.h5pc"
	}
}

func hostingMiniappPayload(data map[string]any) map[string]any {
	miniappData, _ := parseJSONStringObject(stringValue(data["miniapp_data"]))
	if miniappData == nil {
		miniappData = map[string]any{}
	}
	if _, ok := miniappData["need_scheme"]; !ok {
		miniappData["need_scheme"] = "Y"
	}
	if _, ok := miniappData["seq_id"]; !ok {
		miniappData["seq_id"] = "APP_LOCAL_SANDBOX"
	}
	miniappData["appid"] = "wx-local-sandbox"
	miniappData["gh_id"] = "gh_local_sandbox"
	miniappData["path"] = "pages/cashier/cashier"
	miniappData["scheme_code"] = "weixin://dl/business/?t=localSandbox"
	return miniappData
}

func addHostingPreorderEchoFields(out map[string]any, data map[string]any) {
	if hostingData, err := parseJSONStringObject(stringValue(data["hosting_data"])); err == nil && len(hostingData) > 0 {
		out["hosting_data"] = compactJSONString(hostingData)
	}
	if appData, err := parseJSONStringObject(stringValue(data["app_data"])); err == nil && len(appData) > 0 {
		out["app_data"] = compactJSONString(appData)
	}
	if acctSplit, err := parseJSONStringObject(stringValue(data["acct_split_bunch"])); err == nil && len(acctSplit) > 0 {
		out["acct_split_bunch"] = compactJSONString(acctSplit)
	}
	for _, field := range []string{"usage_type", "time_expire"} {
		if value := stringValue(data[field]); value != "" {
			out[field] = value
		}
	}
}

func isHostingMultiPay(data map[string]any) bool {
	if strings.EqualFold(strings.TrimSpace(stringValue(data["multi_pay_way_flag"])), "Y") {
		return true
	}
	count := 0
	for _, field := range []string{"wx_data", "alipay_data", "unionpay_data", "dy_data", "largeamt_data", "terminal_device_data"} {
		if stringValue(data[field]) != "" {
			count++
		}
	}
	return count > 1
}

func isAggregationMicropay(tradeType string) bool {
	return tradeType == "T_MICROPAY" || tradeType == "A_MICROPAY" || tradeType == "U_MICROPAY"
}

func aggregationChannelResponseKey(tradeType string) string {
	switch {
	case strings.HasPrefix(tradeType, "T_"):
		return "wx_response"
	case strings.HasPrefix(tradeType, "A_"):
		return "alipay_response"
	case strings.HasPrefix(tradeType, "U_"):
		return "unionpay_response"
	default:
		return ""
	}
}

func aggregationChannelPayload(tradeType string) map[string]any {
	if tradeType == "U_MICROPAY" {
		return map[string]any{
			"trade_type":        tradeType,
			"channel":           aggregationVariant(tradeType),
			"fund_channel":      "UNIONPAY",
			"pay_channel_type":  "U",
			"resp_code":         "00",
			"resp_msg":          "成功[0000000]",
			"party_order_id":    "PARTY-UP-MICROPAY-LOCAL",
			"atu_sub_mer_id":    "UP-MER-LOCAL",
			"channel_status":    "P",
			"channel_synthetic": true,
		}
	}
	return map[string]any{
		"trade_type":   tradeType,
		"channel":      aggregationVariant(tradeType),
		"fund_channel": "LOCAL_SANDBOX",
		"synthetic":    true,
	}
}

func hostingChannelPayload(kind string) map[string]any {
	return map[string]any{
		"channel":   kind,
		"synthetic": true,
		"sandbox":   "local",
	}
}

func compactJSONString(value any) string {
	b, _ := json.Marshal(value)
	return string(b)
}

func aggregationCreateResp(tradeType string) (string, string) {
	if isWeChatMicropay(tradeType) {
		return "00000000", "交易成功"
	}
	if isWeChatInvokePay(tradeType) || isAlipayInvokePay(tradeType) || isAlipayNativePay(tradeType) || isUnionPayNativePay(tradeType) || isUnionPayMicropay(tradeType) {
		return "00000100", "下单成功"
	}
	return "00000000", "受理成功"
}

func aggregationInitialState(tradeType string) string {
	if isWeChatMicropay(tradeType) {
		return "S"
	}
	return "P"
}

func isWeChatInvokePay(tradeType string) bool {
	return tradeType == "T_JSAPI" || tradeType == "T_MINIAPP" || tradeType == "T_APP"
}

func isWeChatMicropay(tradeType string) bool {
	return tradeType == "T_MICROPAY"
}

func isAlipayNativePay(tradeType string) bool {
	return tradeType == "A_NATIVE"
}

func isAlipayInvokePay(tradeType string) bool {
	return tradeType == "A_JSAPI"
}

func isUnionPayNativePay(tradeType string) bool {
	return tradeType == "U_NATIVE"
}

func isUnionPayMicropay(tradeType string) bool {
	return tradeType == "U_MICROPAY"
}

func addPaymentCreateExtensions(out map[string]any, payment Payment) map[string]any {
	if payment.BusinessVariant != "" {
		out["business_variant"] = payment.BusinessVariant
	}
	if len(payment.TxMetadata) > 0 {
		out["tx_metadata"] = payment.TxMetadata
	}
	if isWeChatInvokePay(payment.TradeType) {
		out["pay_info"] = compactJSONString(wechatInvokePayInfo(payment))
		return out
	}
	if isWeChatMicropay(payment.TradeType) {
		out["method_expand"] = compactJSONString(wechatMicropayMethodExpand(payment))
		return out
	}
	if isAlipayInvokePay(payment.TradeType) {
		delete(out, "qr_code")
		out["pay_info"] = compactJSONString(alipayInvokePayInfo(payment))
		return out
	}
	if isAlipayNativePay(payment.TradeType) || isUnionPayNativePay(payment.TradeType) {
		return out
	}
	if isUnionPayMicropay(payment.TradeType) {
		out["acct_id"] = "F-LOCAL-UP-MICROPAY"
		out["acct_stat"] = "I"
		out["atu_sub_mer_id"] = "UP-MER-LOCAL"
		out["bank_message"] = "成功[0000000]"
		out["delay_acct_flag"] = "N"
		out["payment_fee"] = compactJSONString(map[string]any{
			"fee_flag":     2,
			"fee_huifu_id": payment.HuifuID,
		})
		out["settlement_amt"] = payment.TransAmt
		out["unconfirm_amt"] = unionpayMicropayUnconfirmAmt(payment.TransAmt)
		for key, value := range payment.ChannelResponse {
			out[key] = value
		}
		return out
	}
	for key, value := range payment.ChannelResponse {
		out[key] = value
	}
	return out
}

func unionpayMicropayUnconfirmAmt(transAmt string) string {
	fen, err := parseAmountFen(transAmt)
	if err != nil {
		return transAmt
	}
	return formatFen(fen - 1)
}

func wechatInvokePayInfo(payment Payment) map[string]any {
	appID := "wx-local-sandbox"
	if methodExpand, ok := payment.ChannelResponse["method_expand"].(map[string]any); ok {
		if subAppID := stringValue(methodExpand["sub_appid"]); subAppID != "" {
			appID = subAppID
		}
	}
	return map[string]any{
		"appId":     appID,
		"timeStamp": "1234567890",
		"nonceStr":  "nonce-local-sandbox",
		"package":   "prepay_id=wx-prepay-local-" + payment.ReqSeqID,
		"signType":  "RSA",
		"paySign":   "RSA-SIGNATURE-LOCAL",
	}
}

func alipayInvokePayInfo(payment Payment) map[string]any {
	return map[string]any{
		"tradeNO": "ALIPAY-TRADE-LOCAL-" + payment.ReqSeqID,
	}
}

func wechatMicropayMethodExpand(payment Payment) map[string]any {
	return map[string]any{
		"bank_type":  "OTHERS",
		"cash_fee":   payment.TransAmt,
		"coupon_fee": "0.00",
		"openid":     "openid-wx-micropay-local",
		"sub_openid": "sub-openid-wx-micropay-local",
	}
}

func addPaymentExtensions(out map[string]any, payment Payment) map[string]any {
	if payment.BusinessVariant != "" {
		out["business_variant"] = payment.BusinessVariant
	}
	if len(payment.TxMetadata) > 0 {
		out["tx_metadata"] = payment.TxMetadata
	}
	for key, value := range payment.ChannelResponse {
		out[key] = value
	}
	return out
}

func addAggregationQueryExtensions(out map[string]any, payment Payment) map[string]any {
	out["settlement_amt"] = payment.TransAmt
	out["delay_acct_flag"] = "N"
	out["acct_date"] = payment.ReqDate
	out["acct_stat"] = payment.State
	out["end_time"] = payment.ReqDate + "120000"
	out["out_trans_id"] = "OUT-" + payment.ReqSeqID
	out["party_order_id"] = "PARTY-" + payment.ReqSeqID
	out["payment_fee"] = compactJSONString(queryPaymentFee(payment))
	if split, ok := payment.TxMetadata["acct_split_bunch"]; ok {
		out["div_flag"] = "Y"
		out["acct_split_bunch"] = compactJSONString(split)
	} else {
		out["div_flag"] = "N"
	}
	if isWeChatInvokePay(payment.TradeType) {
		if payment.BusinessVariant != "" {
			out["business_variant"] = payment.BusinessVariant
		}
		if len(payment.TxMetadata) > 0 {
			out["tx_metadata"] = payment.TxMetadata
		}
		out["bank_message"] = "交易成功"
		out["method_expand"] = compactJSONString(wechatInvokeQueryMethodExpand(payment))
		out["wx_user_id"] = ""
		return out
	}
	return addPaymentExtensions(out, payment)
}

func queryPaymentFee(payment Payment) map[string]any {
	feeAmt := queryFeeAmount(payment.TransAmt)
	return map[string]any{
		"fee_amount":   feeAmt,
		"fee_huifu_id": payment.HuifuID,
		"fee_formula_infos": []map[string]any{
			{
				"fee_formula": "AMT*0.0021",
				"fee_type":    "TRANS_FEE",
			},
		},
	}
}

func queryFeeAmount(transAmt string) string {
	fen, err := parseAmountFen(transAmt)
	if err != nil {
		return "0.00"
	}
	return formatFen(fen * 21 / 10000)
}

func wechatInvokeQueryMethodExpand(payment Payment) map[string]any {
	subAppID := "wx-local-sandbox"
	subOpenID := "sub-openid-wx-jsapi-local"
	if methodExpand, ok := payment.ChannelResponse["method_expand"].(map[string]any); ok {
		if value := stringValue(methodExpand["sub_appid"]); value != "" {
			subAppID = value
		}
		if value := stringValue(methodExpand["sub_openid"]); value != "" {
			subOpenID = value
		}
	}
	return map[string]any{
		"bank_type":  "OTHERS",
		"coupon_fee": "0.00",
		"openid":     "openid-wx-jsapi-local",
		"sub_appid":  subAppID,
		"sub_openid": subOpenID,
	}
}

func addOperationExtensions(out map[string]any, businessVariant string, channelResponse map[string]any) map[string]any {
	if businessVariant != "" {
		out["business_variant"] = businessVariant
	}
	for key, value := range channelResponse {
		out[key] = value
	}
	return out
}

func copyMap(in map[string]any) map[string]any {
	if len(in) == 0 {
		return nil
	}
	out := make(map[string]any, len(in))
	for key, value := range in {
		out[key] = value
	}
	return out
}

func firstNonNilMap(values ...map[string]any) map[string]any {
	for _, value := range values {
		if len(value) > 0 {
			return value
		}
	}
	return nil
}

func mapKeys(value map[string]any) []string {
	keys := make([]string, 0, len(value))
	for key := range value {
		keys = append(keys, key)
	}
	sort.Strings(keys)
	return keys
}
