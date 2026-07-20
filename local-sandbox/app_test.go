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
	"net/http/httptest"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"sync"
	"testing"
	"time"
)

const r4ContractAssetsSHA256 = "0be7dc6263dcbbb8a1f48df6a472dd1a1fb612ba63444d1ec909eaa019862c16"

func TestR4ContractAssetsStayFrozen(t *testing.T) {
	root := filepath.Join("contracts", "huifu-pay-integration-1.3.0-r4")
	var files []string
	err := filepath.WalkDir(root, func(path string, entry os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if !entry.IsDir() {
			files = append(files, path)
		}
		return nil
	})
	if err != nil {
		t.Fatal(err)
	}
	sort.Strings(files)
	hash := sha256.New()
	for _, path := range files {
		body, err := os.ReadFile(path)
		if err != nil {
			t.Fatal(err)
		}
		rel, err := filepath.Rel(root, path)
		if err != nil {
			t.Fatal(err)
		}
		sum := sha256.Sum256(body)
		fmt.Fprintf(hash, "%s\n%x\n", filepath.ToSlash(rel), sum)
	}
	if got := fmt.Sprintf("%x", hash.Sum(nil)); got != r4ContractAssetsSHA256 {
		t.Fatalf("r4 contract assets changed: got %s want %s", got, r4ContractAssetsSHA256)
	}
}

func TestFrozenReferenceEvidenceUsesVersionedReportContract(t *testing.T) {
	if appVersion != "1.0.1" {
		t.Fatalf("frozen reference evidence requires app version 1.0.1, got %s", appVersion)
	}
	if reportSchema != "1.8" {
		t.Fatalf("frozen reference evidence requires report schema 1.8, got %s", reportSchema)
	}
	bundle, err := loadContractBundle()
	if err != nil {
		t.Fatal(err)
	}
	check := referenceDigestCheck(bundle)
	if check.Status != "frozen_snapshot" || check.Checked != len(bundle.ReferenceDigests.Files) || len(check.Problems) != 0 {
		t.Fatalf("unexpected frozen reference evidence: %+v", check)
	}
}

func TestContractCoverageIsFrozenSnapshotOfSkillReferences(t *testing.T) {
	bundle, err := loadContractBundle()
	if err != nil {
		t.Fatal(err)
	}
	problems := validateContractBundle(bundle)
	if len(problems) > 0 {
		t.Fatalf("contract bundle has problems: %v", problems)
	}

	expected := map[string]bool{}
	for _, name := range readExpectedReferences(t) {
		expected[name] = true
	}
	for name := range bundle.References.References {
		if !expected[name] {
			t.Fatalf("frozen contract reference %s is no longer declared by the Skill", name)
		}
	}
}

func TestSDKSortedJSONCanonicalization(t *testing.T) {
	data := map[string]any{
		"req_seq_id":    "REQ-SDK-001",
		"huifu_id":      "6666000100000001",
		"trade_type":    "A_NATIVE",
		"trans_amt":     "0.01",
		"goods_desc":    "测试/desc <tag>&value",
		"method_expand": `{"b":"2","a":"1"}`,
		"notify_url":    "http://127.0.0.1:18080/notify?a=1&b=2",
	}
	canonical, err := canonicalData(data)
	if err != nil {
		t.Fatal(err)
	}
	want := `{"goods_desc":"测试/desc <tag>&value","huifu_id":"6666000100000001","method_expand":"{\"b\":\"2\",\"a\":\"1\"}","notify_url":"http://127.0.0.1:18080/notify?a=1&b=2","req_seq_id":"REQ-SDK-001","trade_type":"A_NATIVE","trans_amt":"0.01"}`
	if canonical != want {
		t.Fatalf("canonical data mismatch\ngot:  %s\nwant: %s", canonical, want)
	}

	app := newTestApp(t)
	signature, err := signData(data, app.creds.MerchantPrivate)
	if err != nil {
		t.Fatal(err)
	}
	if err := verifyData(data, signature, app.creds.MerchantPublic); err != nil {
		t.Fatalf("signature should verify over SDK sorted JSON canonical data: %v", err)
	}
}

func TestGatewayCoreEndpoints(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	control := app.controlHandler()

	createData := map[string]any{
		"req_seq_id": "REQ1001",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.01",
		"goods_desc": "local sandbox test",
	}
	createResp := postGateway(t, app, handler, "/v4/trade/payment/create", createData)
	assertDataCode(t, app, createResp, "00000100")
	assertNoTopLevelRespCode(t, createResp)
	hfSeqID := stringValue(createResp.Data["hf_seq_id"])
	if hfSeqID == "" || stringValue(createResp.Data["trans_stat"]) != "P" {
		t.Fatalf("unexpected create response: %+v", createResp.Data)
	}

	queryData := map[string]any{
		"huifu_id":  "6666000100000001",
		"hf_seq_id": hfSeqID,
	}
	queryResp1 := postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", queryData)
	assertDataCode(t, app, queryResp1, "00000000")
	if got := stringValue(queryResp1.Data["trans_stat"]); got != "P" {
		t.Fatalf("first query trans_stat = %s, want P", got)
	}
	queryResp2 := postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", queryData)
	if got := stringValue(queryResp2.Data["trans_stat"]); got != "S" {
		t.Fatalf("second query trans_stat = %s, want S", got)
	}

	hostingData := map[string]any{"project_title": "Sandbox Project", "project_id": "P123", "request_type": "P"}
	hostingRaw, _ := json.Marshal(hostingData)
	preorderData := map[string]any{
		"req_seq_id":     "HREQ1001",
		"req_date":       "20260624",
		"huifu_id":       "6666000100000001",
		"trans_amt":      "0.01",
		"goods_desc":     "hosting sandbox test",
		"pre_order_type": "1",
		"trans_type":     "A_NATIVE",
		"hosting_data":   string(hostingRaw),
	}
	preorderResp := postGateway(t, app, handler, "/v2/trade/hosting/payment/preorder", preorderData)
	assertDataCode(t, app, preorderResp, "00000000")
	preOrderID := stringValue(preorderResp.Data["pre_order_id"])
	if preOrderID == "" || stringValue(preorderResp.Data["jump_url"]) == "" {
		t.Fatalf("unexpected preorder response: %+v", preorderResp.Data)
	}

	hostingQueryResp := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "QRY-HREQ1001-PENDING",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "HREQ1001",
	})
	assertDataCode(t, app, hostingQueryResp, "00000000")
	if got := stringValue(hostingQueryResp.Data["trans_stat"]); got != "P" {
		t.Fatalf("hosting query before confirm trans_stat = %s, want P", got)
	}

	callbackResp := getControlJSON(t, control, "/__merchant/hosting/callback?pre_order_id="+preOrderID)
	if got := stringValue(callbackResp["state"]); got != "P" {
		t.Fatalf("hosting callback state = %s, want P", got)
	}
	confirmResp := postControlJSON(t, app, control, "/__merchant/hosting/confirm", map[string]any{"pre_order_id": preOrderID})
	if got := stringValue(confirmResp["state"]); got != "P" {
		t.Fatalf("hosting confirm state = %s, want P before query", got)
	}

	hostingQueryResp = postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "QRY-HREQ1001-SUCCESS",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "HREQ1001",
	})
	assertDataCode(t, app, hostingQueryResp, "00000000")
	if got := stringValue(hostingQueryResp.Data["pay_type"]); got == "" {
		t.Fatalf("hosting query missing pay_type: %+v", hostingQueryResp.Data)
	}
	if got := stringValue(hostingQueryResp.Data["trans_stat"]); got != "S" {
		t.Fatalf("hosting query trans_stat = %s, want S", got)
	}
}

func TestHostingMultipayPreorderProjection(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	preorder := postGateway(t, app, handler, "/v2/trade/hosting/payment/preorder", map[string]any{
		"req_seq_id":         "REQ-HOST-MULTIPAY",
		"req_date":           "20260701",
		"huifu_id":           "6666000100000001",
		"pre_order_type":     "1",
		"trans_amt":          "0.05",
		"time_expire":        "20260720125858",
		"usage_type":         "P",
		"goods_desc":         "hosting multipay",
		"notify_url":         "https://example.invalid/notify",
		"delay_acct_flag":    "N",
		"acct_split_bunch":   `{"percentage_flag":"N","is_clean_split":"N","acct_infos":[{"div_amt":"0.02","huifu_id":"6666000100000002"},{"div_amt":"0.02","huifu_id":"6666000100000003"},{"div_amt":"0.01","huifu_id":"6666000100000001"}]}`,
		"hosting_data":       `{"request_type":"P","project_title":"local multipay","project_id":"PROJECT-HOST-MULTIPAY-001","private_info":"local private info","callback_url":"https://example.invalid/callback"}`,
		"app_data":           `{"app_schema":"https://example.invalid/app-callback","private_info":""}`,
		"miniapp_data":       `{"seq_id":"","need_scheme":"Y"}`,
		"dy_data":            `{"sub_appid":"dy-local-sandbox","h5_info":{"type":"Ios"},"scene_info":{"payer_client_ip":"127.0.0.1"}}`,
		"unionpay_data":      `{"addn_data":"{\"customData\":\"local\"}","pnr_ins_id_cd":"UP-INS-LOCAL","front_url":"https://example.invalid/unionpay","term_info":"UP-TERM-LOCAL","pid_info":"{\"pnr_order_id\":\"PNR-LOCAL-001\",\"pid_sct\":\"LOCAL\",\"trade_scene\":\"1\"}"}`,
		"multi_pay_way_flag": "Y",
	})
	assertDataCode(t, app, preorder, "00000000")
	for _, field := range []string{"pre_order_id", "jump_url", "current_time", "hosting_data", "app_data", "unionpay_response", "dy_response"} {
		if stringValue(preorder.Data[field]) == "" {
			t.Fatalf("multipay preorder missing %s: %+v", field, preorder.Data)
		}
	}
	if got := stringValue(preorder.Data["business_variant"]); got != "hosting.h5pc.multi-pay" {
		t.Fatalf("business_variant = %s, want hosting.h5pc.multi-pay", got)
	}
	if _, ok := preorder.Data["order_type"]; ok {
		t.Fatalf("preorder response should not include legacy order_type=HT: %+v", preorder.Data)
	}
	if got := stringValue(preorder.Data["usage_type"]); got != "P" {
		t.Fatalf("usage_type = %s, want P", got)
	}
	hostingData, err := parseJSONStringObject(stringValue(preorder.Data["hosting_data"]))
	if err != nil {
		t.Fatalf("hosting_data is not JSON object string: %v", err)
	}
	if got := stringValue(hostingData["request_type"]); got != "P" {
		t.Fatalf("hosting_data.request_type = %s, want P", got)
	}
	appData, err := parseJSONStringObject(stringValue(preorder.Data["app_data"]))
	if err != nil {
		t.Fatalf("app_data is not JSON object string: %v", err)
	}
	if got := stringValue(appData["app_schema"]); got != "https://example.invalid/app-callback" {
		t.Fatalf("app_data.app_schema = %s", got)
	}
}

func TestHostingAlipayMiniPreorderJumpURLProjection(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	control := app.controlHandler()
	preorder := postGateway(t, app, handler, "/v2/trade/hosting/payment/preorder", map[string]any{
		"req_seq_id":       "REQ-HOST-ALI-MINI",
		"req_date":         "20260701",
		"huifu_id":         "6666000100000001",
		"pre_order_type":   "2",
		"trans_amt":        "0.05",
		"time_expire":      "20260720125858",
		"usage_type":       "P",
		"goods_desc":       "hosting alipay mini",
		"notify_url":       "https://example.invalid/notify",
		"hosting_data":     `{"request_type":"P","project_title":"local alipay mini","project_id":"PROJECT-HOST-ALI-MINI-001","private_info":"local private info","callback_url":"https://example.invalid/callback"}`,
		"app_data":         `{"app_schema":"https://example.invalid/app-callback","private_info":""}`,
		"miniapp_data":     `{"seq_id":"","need_scheme":"Y"}`,
		"dy_data":          `{"sub_appid":"dy-local-sandbox","h5_info":{"type":"Ios"},"scene_info":{"payer_client_ip":"127.0.0.1"}}`,
		"unionpay_data":    `{"addn_data":"{\"customData\":\"local\"}","pnr_ins_id_cd":"UP-INS-LOCAL","front_url":"https://example.invalid/unionpay"}`,
		"acct_split_bunch": `{"percentage_flag":"N","is_clean_split":"N","acct_infos":[{"div_amt":"0.02","huifu_id":"6666000100000002"},{"div_amt":"0.02","huifu_id":"6666000100000003"},{"div_amt":"0.01","huifu_id":"6666000100000001"}]}`,
	})
	assertDataCode(t, app, preorder, "00000000")
	if got := stringValue(preorder.Data["business_variant"]); got != "hosting.alipay-mini" {
		t.Fatalf("business_variant = %s, want hosting.alipay-mini", got)
	}
	jumpURL := stringValue(preorder.Data["jump_url"])
	if !strings.HasPrefix(jumpURL, "alipays://platformapi/startapp?") {
		t.Fatalf("jump_url = %s, want alipay scheme", jumpURL)
	}
	if !strings.Contains(jumpURL, "thirdPartSchema=https%3A%2F%2Fexample.invalid%2Fapp-callback") || !strings.Contains(jumpURL, "bank_switch=Y") {
		t.Fatalf("jump_url missing alipay mini parameters: %s", jumpURL)
	}
	if stringValue(preorder.Data["hosting_data"]) == "" || stringValue(preorder.Data["app_data"]) == "" || stringValue(preorder.Data["alipay_response"]) == "" {
		t.Fatalf("alipay mini response missing channel fields: %+v", preorder.Data)
	}
	if got := stringValue(preorder.Data["usage_type"]); got != "P" {
		t.Fatalf("usage_type = %s, want P", got)
	}
	preOrderID := stringValue(preorder.Data["pre_order_id"])
	getControlJSON(t, control, "/__merchant/hosting/callback?pre_order_id="+preOrderID)
	postControlJSON(t, app, control, "/__merchant/hosting/confirm", map[string]any{"pre_order_id": preOrderID})
	query := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", map[string]any{
		"product_id":     "YYZY",
		"req_date":       stringValue(preorder.Data["req_date"]),
		"req_seq_id":     "QRY-HOST-ALI-MINI",
		"huifu_id":       "6666000100000001",
		"org_req_date":   stringValue(preorder.Data["req_date"]),
		"org_req_seq_id": stringValue(preorder.Data["req_seq_id"]),
	})
	assertDataCode(t, app, query, "00000000")
	for key, want := range map[string]string{
		"pay_type":      "A_JSAPI",
		"bank_code":     "TRADE_SUCCESS",
		"bank_desc":     "TRADE_SUCCESS",
		"is_div":        "Y",
		"is_delay_acct": "N",
		"fee_amt":       "0.04",
		"ref_amt":       "0.00",
	} {
		if got := stringValue(query.Data[key]); got != want {
			t.Fatalf("alipay mini query %s = %s, want %s; data=%+v", key, got, want, query.Data)
		}
	}
	if stringValue(query.Data["org_hf_seq_id"]) == "" || stringValue(query.Data["out_trans_id"]) == "" || stringValue(query.Data["party_order_id"]) == "" {
		t.Fatalf("alipay mini query missing order identifiers: %+v", query.Data)
	}
	if _, err := parseJSONStringObject(stringValue(query.Data["acct_split_bunch"])); err != nil {
		t.Fatalf("alipay mini query acct_split_bunch is not JSON object string: %v", err)
	}
	if _, err := parseJSONStringObject(stringValue(query.Data["alipay_response"])); err != nil {
		t.Fatalf("alipay mini query alipay_response is not JSON object string: %v", err)
	}
}

func TestHostingWechatMiniPreorderProjection(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	preorder := postGateway(t, app, handler, "/v2/trade/hosting/payment/preorder", map[string]any{
		"req_seq_id":       "REQ-HOST-WX-MINI",
		"req_date":         "20260701",
		"huifu_id":         "6666000100000001",
		"pre_order_type":   "3",
		"trans_amt":        "0.05",
		"time_expire":      "20260720125858",
		"usage_type":       "P",
		"goods_desc":       "hosting wechat mini",
		"notify_url":       "https://example.invalid/notify",
		"hosting_data":     `{"request_type":"P","project_title":"local wechat mini","project_id":"PROJECT-HOST-WX-MINI-001","private_info":"local private info","callback_url":"https://example.invalid/callback"}`,
		"app_data":         `{"app_schema":"https://example.invalid/app-callback","private_info":""}`,
		"miniapp_data":     `{"seq_id":"","need_scheme":"Y"}`,
		"dy_data":          `{"sub_appid":"dy-local-sandbox","h5_info":{"type":"Ios"},"scene_info":{"payer_client_ip":"127.0.0.1"}}`,
		"unionpay_data":    `{"addn_data":"{\"customData\":\"local\"}","pnr_ins_id_cd":"UP-INS-LOCAL","front_url":"https://example.invalid/unionpay"}`,
		"acct_split_bunch": `{"percentage_flag":"N","is_clean_split":"N","acct_infos":[{"div_amt":"0.02","huifu_id":"6666000100000002"},{"div_amt":"0.02","huifu_id":"6666000100000003"},{"div_amt":"0.01","huifu_id":"6666000100000001"}]}`,
	})
	assertDataCode(t, app, preorder, "00000000")
	if got := stringValue(preorder.Data["business_variant"]); got != "hosting.wechat-mini" {
		t.Fatalf("business_variant = %s, want hosting.wechat-mini", got)
	}
	if got := stringValue(preorder.Data["jump_url"]); got != "&bank_switch=Y" {
		t.Fatalf("jump_url = %s, want &bank_switch=Y", got)
	}
	miniappData, err := parseJSONStringObject(stringValue(preorder.Data["miniapp_data"]))
	if err != nil {
		t.Fatalf("miniapp_data is not JSON object string: %v", err)
	}
	if got := stringValue(miniappData["seq_id"]); got != "" {
		t.Fatalf("miniapp_data.seq_id = %s, want empty", got)
	}
	for key, want := range map[string]string{
		"need_scheme": "Y",
		"appid":       "wx-local-sandbox",
		"gh_id":       "gh_local_sandbox",
		"path":        "pages/cashier/cashier",
	} {
		if got := stringValue(miniappData[key]); got != want {
			t.Fatalf("miniapp_data.%s = %s, want %s", key, got, want)
		}
	}
	if !strings.HasPrefix(stringValue(miniappData["scheme_code"]), "weixin://dl/business/?t=") {
		t.Fatalf("miniapp_data.scheme_code = %s", stringValue(miniappData["scheme_code"]))
	}
	if stringValue(preorder.Data["hosting_data"]) == "" || stringValue(preorder.Data["app_data"]) == "" || stringValue(preorder.Data["wx_response"]) == "" {
		t.Fatalf("wechat mini response missing channel fields: %+v", preorder.Data)
	}
}

func TestHostingDouyinDirectPreorderWithoutHostingData(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	preorder := postGateway(t, app, handler, "/v2/trade/hosting/payment/preorder", map[string]any{
		"req_seq_id":         "REQ-HOST-DY-DIRECT",
		"req_date":           "20260701",
		"huifu_id":           "6666000100000001",
		"pre_order_type":     "4",
		"trans_amt":          "0.05",
		"time_expire":        "20261229235959",
		"goods_desc":         "hosting douyin direct",
		"style_id":           "STYLE-LOCAL",
		"delay_acct_flag":    "Y",
		"dy_data":            `{"busi_scene":"H5","sub_appid":"dy-local-sandbox","h5_info":{"type":"Ios"},"scene_info":{"payer_client_ip":"127.0.0.1"}}`,
		"multi_pay_way_flag": "Y",
	})
	assertDataCode(t, app, preorder, "00000000")
	if got := stringValue(preorder.Data["business_variant"]); got != "hosting.douyin-direct" {
		t.Fatalf("business_variant = %s, want hosting.douyin-direct", got)
	}
	if jumpURL := stringValue(preorder.Data["jump_url"]); !strings.HasPrefix(jumpURL, "https://cashier.ulpay.com/bytepay-cashdesk/bytepay-invoke?prepay_id=DY-PREPAY-") {
		t.Fatalf("jump_url = %s, want douyin cashier", jumpURL)
	}
	if stringValue(preorder.Data["dy_response"]) == "" {
		t.Fatalf("douyin direct response missing dy_response: %+v", preorder.Data)
	}
	if got := stringValue(preorder.Data["time_expire"]); got != "20261229235959" {
		t.Fatalf("time_expire = %s, want 20261229235959", got)
	}
}

func TestAggregationWechatJSAPIQueryProjection(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	createData := map[string]any{
		"req_seq_id":       "REQ-WX-JSAPI-PROJECTION",
		"req_date":         "20260701",
		"huifu_id":         "6666000100000001",
		"trade_type":       "T_JSAPI",
		"trans_amt":        "825.00",
		"goods_desc":       "wechat jsapi projection",
		"method_expand":    `{"sub_appid":"wx-local-jsapi-appid","sub_openid":"sub-openid-wx-jsapi-001"}`,
		"acct_split_bunch": `{"acct_infos":[{"div_amt":"2.47","huifu_id":"6666000100000002"},{"div_amt":"822.53","huifu_id":"6666000100000001"}]}`,
	}
	createResp := postGateway(t, app, handler, "/v4/trade/payment/create", createData)
	assertDataCode(t, app, createResp, "00000100")
	if stringValue(createResp.Data["pay_info"]) == "" {
		t.Fatalf("T_JSAPI create response missing pay_info: %+v", createResp.Data)
	}

	queryData := map[string]any{
		"huifu_id":   "6666000100000001",
		"req_date":   "20260701",
		"req_seq_id": "REQ-WX-JSAPI-PROJECTION",
	}
	postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", queryData)
	queryResp := postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", queryData)
	if got := stringValue(queryResp.Data["trans_stat"]); got != "S" {
		t.Fatalf("query trans_stat = %s, want S", got)
	}
	if _, ok := queryResp.Data["wx_response"]; ok {
		t.Fatalf("T_JSAPI query should project method_expand, not wx_response: %+v", queryResp.Data)
	}
	methodExpand, err := parseJSONStringObject(stringValue(queryResp.Data["method_expand"]))
	if err != nil {
		t.Fatalf("method_expand is not a JSON object string: %v", err)
	}
	if got := stringValue(methodExpand["sub_appid"]); got != "wx-local-jsapi-appid" {
		t.Fatalf("method_expand.sub_appid = %s", got)
	}
	paymentFee, err := parseJSONStringObject(stringValue(queryResp.Data["payment_fee"]))
	if err != nil {
		t.Fatalf("payment_fee is not a JSON object string: %v", err)
	}
	if got := stringValue(paymentFee["fee_amount"]); got != "1.73" {
		t.Fatalf("payment_fee.fee_amount = %s, want 1.73", got)
	}
	split, err := parseJSONStringObject(stringValue(queryResp.Data["acct_split_bunch"]))
	if err != nil {
		t.Fatalf("acct_split_bunch is not a JSON object string: %v", err)
	}
	infos, ok := split["acct_infos"].([]any)
	if !ok || len(infos) != 2 {
		t.Fatalf("acct_split_bunch.acct_infos = %+v, want two split rows", split["acct_infos"])
	}
}

func TestAggregationUnionpayMicropayCreateProjectionFromLatestLog(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	create := postGateway(t, app, handler, "/v4/trade/payment/create", map[string]any{
		"req_seq_id":           "PAY-UP-MICROPAY-PROJECTION",
		"req_date":             "20260701",
		"huifu_id":             "6666000100000001",
		"trade_type":           "U_MICROPAY",
		"trans_amt":            "0.10",
		"goods_desc":           "测试商品",
		"method_expand":        `{"auth_code":"AUTHCODE-UP-MICROPAY-LOCAL"}`,
		"terminal_device_data": `{"device_ip":"10.10.0.1"}`,
		"notify_url":           "https://example.invalid/notify",
	})
	assertDataCode(t, app, create, "00000100")
	for key, want := range map[string]string{
		"resp_desc":       "下单成功",
		"trade_type":      "U_MICROPAY",
		"trans_stat":      "P",
		"acct_stat":       "I",
		"bank_message":    "成功[0000000]",
		"delay_acct_flag": "N",
		"settlement_amt":  "0.10",
		"unconfirm_amt":   "0.09",
	} {
		if got := stringValue(create.Data[key]); got != want {
			t.Fatalf("unionpay micropay create %s = %s, want %s; data=%+v", key, got, want, create.Data)
		}
	}
	paymentFee, err := parseJSONStringObject(stringValue(create.Data["payment_fee"]))
	if err != nil {
		t.Fatalf("payment_fee is not JSON object string: %v", err)
	}
	if got := stringValue(paymentFee["fee_flag"]); got != "2" {
		t.Fatalf("payment_fee.fee_flag = %s, want 2", got)
	}
	if got := stringValue(paymentFee["fee_huifu_id"]); got != "6666000100000001" {
		t.Fatalf("payment_fee.fee_huifu_id = %s", got)
	}
	txMetadata, ok := create.Data["tx_metadata"].(map[string]any)
	if !ok {
		t.Fatalf("tx_metadata missing or not object: %+v", create.Data["tx_metadata"])
	}
	terminal, ok := txMetadata["terminal_device_data"].(map[string]any)
	if !ok {
		t.Fatalf("terminal_device_data missing or not object: %+v", txMetadata)
	}
	if got := stringValue(terminal["device_ip"]); got != "10.10.0.1" {
		t.Fatalf("terminal_device_data.device_ip = %s, want 10.10.0.1", got)
	}
	unionpayResp, err := parseJSONStringObject(stringValue(create.Data["unionpay_response"]))
	if err != nil {
		t.Fatalf("unionpay_response is not JSON object string: %v", err)
	}
	if got := stringValue(unionpayResp["resp_msg"]); got != "成功[0000000]" {
		t.Fatalf("unionpay_response.resp_msg = %s", got)
	}
}

func TestGatewayLogKindLabels(t *testing.T) {
	cases := []struct {
		path string
		want string
	}{
		{"/v4/trade/payment/create", "聚合支付下单"},
		{"/v4/trade/payment/scanpay/query", "聚合查单"},
		{"/v4/trade/payment/scanpay/refundquery", "退款查询"},
		{"/v2/trade/payment/scanpay/closequery", "关单查询"},
		{"/v2/trade/hosting/payment/preorder", "托管预下单"},
		{"/v2/trade/hosting/payment/queryorderinfo", "托管查单"},
		{"/v2/trade/hosting/payment/queryRefundInfo", "退款查询"},
		{"/v2/trade/hosting/payment/splitpay/query", "拆单查询"},
		{"/v2/trade/check/filequery", "对账文件查询"},
	}
	for _, tc := range cases {
		t.Run(tc.path, func(t *testing.T) {
			if got := gatewayLogKind(tc.path); got != tc.want {
				t.Fatalf("gatewayLogKind(%q) = %q, want %q", tc.path, got, tc.want)
			}
		})
	}
}

func TestGatewayRequestLogCapturesRequestAndResponseDetails(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	data := map[string]any{
		"req_seq_id": "REQ-LOG-001",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.01",
		"goods_desc": "request log test",
		"notify_url": "http://127.0.0.1:9000/notify?secret=value",
	}
	resp := postGateway(t, app, handler, "/v4/trade/payment/create", data)
	assertDataCode(t, app, resp, "00000100")

	app.mu.Lock()
	if len(app.requestLogs) != 1 {
		t.Fatalf("request log count = %d, want 1", len(app.requestLogs))
	}
	log := app.requestLogs[0]
	app.mu.Unlock()
	if log.Path != "/v4/trade/payment/create" || log.Kind != "聚合支付下单" {
		t.Fatalf("unexpected request log route metadata: %+v", log)
	}
	if log.SignatureStatus != "verified" {
		t.Fatalf("signature_status = %s, want verified", log.SignatureStatus)
	}
	if log.RequestDataStatus != "captured_verified" {
		t.Fatalf("request_data_status = %s, want captured_verified", log.RequestDataStatus)
	}
	if got := stringValue(log.RequestData["req_seq_id"]); got != "REQ-LOG-001" {
		t.Fatalf("request log req_seq_id = %s", got)
	}
	if got := stringValue(log.ResponseData["resp_code"]); got != "00000100" {
		t.Fatalf("response log resp_code = %s", got)
	}
	if _, ok := log.RequestEnvelope["sign"]; ok {
		t.Fatalf("request envelope leaked raw sign: %+v", log.RequestEnvelope)
	}
	if stringValue(log.RequestEnvelope["sign_sha256"]) == "" {
		t.Fatalf("request envelope missing sign digest: %+v", log.RequestEnvelope)
	}
	if got := stringValue(log.RequestEnvelope["status"]); got != "parsed" {
		t.Fatalf("request envelope status = %s, want parsed: %+v", got, log.RequestEnvelope)
	}
	if got := stringValue(log.RequestEnvelope["sign_status"]); got != "present" {
		t.Fatalf("request envelope sign_status = %s, want present: %+v", got, log.RequestEnvelope)
	}
	if stringValue(log.ResponseEnvelope["sign_sha256"]) == "" {
		t.Fatalf("response envelope missing sign digest: %+v", log.ResponseEnvelope)
	}
	if got := stringValue(log.ResponseEnvelope["status"]); got != "signed_response" {
		t.Fatalf("response envelope status = %s, want signed_response: %+v", got, log.ResponseEnvelope)
	}
	raw, err := json.Marshal(log)
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(string(raw), "secret=value") {
		t.Fatalf("request log leaked URL query secret: %s", raw)
	}
	snapshot := app.uiSnapshot()
	counts := snapshot["counts"].(map[string]int)
	if got := counts["request_logs"]; got != 1 {
		t.Fatalf("UI request log count = %d, want 1", got)
	}
	rows := snapshot["request_logs"].([]map[string]any)
	if len(rows) != 1 || stringValue(rows[0]["actions"]) == "" {
		t.Fatalf("UI request log row missing action id: %+v", rows)
	}
	summarySnapshot := app.uiSnapshotFor(false)
	summaryRows := summarySnapshot["request_logs"].([]map[string]any)
	if _, ok := summaryRows[0]["request_data"]; ok {
		t.Fatalf("summary UI state exposed request data: %+v", summaryRows[0])
	}
	if got := summaryRows[0]["detail_available"]; got != false {
		t.Fatalf("summary detail_available = %v, want false", got)
	}
}

func TestGatewayRequestLogOmitsUnverifiedPayloadAndUsesStableIDs(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	data := map[string]any{
		"req_seq_id":  "REQ-UNVERIFIED-001",
		"huifu_id":    "6666000100000001",
		"trade_type":  "A_NATIVE",
		"trans_amt":   "0.01",
		"goods_desc":  strings.Repeat("x", 5000),
		"secret_note": "must-not-leak",
	}
	body, _ := json.Marshal(Envelope{SysID: "SYS", ProductID: "MYPAY", Sign: "bad", Data: data})
	req := httptest.NewRequest(http.MethodPost, "/v4/trade/payment/create", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("jpt-x-skill-source", sandboxSkillSource)
	req.Header.Set("jpt-x-skill-huifu_id", "6666000100000001")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("status = %d", rec.Code)
	}
	app.mu.Lock()
	if len(app.requestLogs) != 1 {
		t.Fatalf("request log count = %d, want 1", len(app.requestLogs))
	}
	log := app.requestLogs[0]
	app.mu.Unlock()
	if log.SignatureStatus != "failed" {
		t.Fatalf("signature status = %s, want failed", log.SignatureStatus)
	}
	if log.RequestData != nil {
		t.Fatalf("unverified request data was captured: %+v", log.RequestData)
	}
	if got := stringValue(log.RequestEnvelope["sign_status"]); got != "present" {
		t.Fatalf("unverified request envelope sign_status = %s, want present: %+v", got, log.RequestEnvelope)
	}
	if stringValue(log.RequestEnvelope["sign_sha256"]) == "" {
		t.Fatalf("unverified request envelope missing sign digest: %+v", log.RequestEnvelope)
	}
	if got := stringValue(log.ResponseEnvelope["status"]); got != "signed_response" {
		t.Fatalf("unverified response envelope status = %s, want signed_response: %+v", got, log.ResponseEnvelope)
	}
	raw, err := json.Marshal(log)
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(string(raw), "must-not-leak") || strings.Contains(string(raw), strings.Repeat("x", 100)) {
		t.Fatalf("unverified request log leaked payload: %s", raw)
	}
	app.mu.Lock()
	app.requestLogSeq = 200
	app.requestLogs = make([]RequestLog, maxGatewayRequestLogs)
	for i := range app.requestLogs {
		app.requestLogs[i] = RequestLog{ID: fmt.Sprintf("REQLOG-%06d", i+1)}
	}
	app.mu.Unlock()
	postGateway(t, app, handler, "/v4/trade/payment/create", map[string]any{
		"req_seq_id": "REQ-STABLE-ID",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.01",
		"goods_desc": "stable id",
	})
	app.mu.Lock()
	last := app.requestLogs[len(app.requestLogs)-1].ID
	app.mu.Unlock()
	if last != "REQLOG-000201" {
		t.Fatalf("last request log id = %s, want REQLOG-000201", last)
	}
}

func TestGatewayRequestLogExplainsMissingEnvelopeFields(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	raw, _ := json.Marshal(map[string]any{
		"req_seq_id": "REQ-DIRECT-BODY",
		"huifu_id":   "6666000100000001",
		"trans_amt":  "0.01",
	})
	req := httptest.NewRequest(http.MethodPost, "/v4/trade/payment/create", bytes.NewReader(raw))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("jpt-x-skill-source", sandboxSkillSource)
	req.Header.Set("jpt-x-skill-huifu_id", "6666000100000001")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("status = %d", rec.Code)
	}
	app.mu.Lock()
	if len(app.requestLogs) != 1 {
		t.Fatalf("request log count = %d, want 1", len(app.requestLogs))
	}
	log := app.requestLogs[0]
	app.mu.Unlock()
	if log.SignatureStatus != "invalid_envelope" {
		t.Fatalf("signature status = %s, want invalid_envelope", log.SignatureStatus)
	}
	if got := stringValue(log.RequestEnvelope["status"]); got != "invalid_envelope" {
		t.Fatalf("request envelope status = %s, want invalid_envelope: %+v", got, log.RequestEnvelope)
	}
	if got := stringValue(log.RequestEnvelope["sign_status"]); got != "missing" {
		t.Fatalf("request envelope sign_status = %s, want missing: %+v", got, log.RequestEnvelope)
	}
	missing := fmt.Sprint(log.RequestEnvelope["missing_fields"])
	for _, field := range []string{"sys_id", "product_id", "sign", "data"} {
		if !strings.Contains(missing, field) {
			t.Fatalf("missing_fields should include %s: %+v", field, log.RequestEnvelope)
		}
	}
	if stringValue(log.RequestEnvelope["body_sha256"]) == "" {
		t.Fatalf("request envelope missing body digest: %+v", log.RequestEnvelope)
	}
	if got := stringValue(log.ResponseEnvelope["status"]); got != "signed_response" {
		t.Fatalf("response envelope status = %s, want signed_response: %+v", got, log.ResponseEnvelope)
	}
}

func TestGatewayRejectsInvalidSignatureAndMissingHeaders(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()

	data := map[string]any{
		"req_seq_id": "REQ2001",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.01",
		"goods_desc": "local sandbox test",
	}
	body, _ := json.Marshal(Envelope{SysID: "SYS", ProductID: "MYPAY", Sign: "bad", Data: data})
	req := httptest.NewRequest(http.MethodPost, "/v4/trade/payment/create", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("jpt-x-skill-source", sandboxSkillSource)
	req.Header.Set("jpt-x-skill-huifu_id", "6666000100000001")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("status = %d", rec.Code)
	}
	var resp SignedResponse
	if err := json.Unmarshal(rec.Body.Bytes(), &resp); err != nil {
		t.Fatal(err)
	}
	if got := stringValue(resp.Data["resp_code"]); got != "LS000003" {
		t.Fatalf("resp_code = %s, want LS000003", got)
	}
}

func TestOfficialDemoProfileSummaryRedactsKeyMaterial(t *testing.T) {
	creds, err := loadCredentialProfile(officialDemoProfileName, t.TempDir(), true)
	if err != nil {
		t.Fatal(err)
	}
	if creds.ProfileName != officialDemoProfileName {
		t.Fatalf("profile = %s, want %s", creds.ProfileName, officialDemoProfileName)
	}
	if creds.SysID != officialDemoSysID || creds.ProductID != officialDemoProductID {
		t.Fatalf("profile ids = %s/%s, want %s/%s", creds.SysID, creds.ProductID, officialDemoSysID, officialDemoProductID)
	}
	if creds.SignatureModel != "dual_key_local_sandbox" {
		t.Fatalf("signature model = %s", creds.SignatureModel)
	}
	if creds.HuifuPublic == nil {
		t.Fatal("Huifu public key was not loaded")
	}
	if creds.GatewayPrivate == creds.MerchantPrivate {
		t.Fatal("official-demo should use separate merchant and sandbox private keys")
	}
	if publicKeyFingerprint(creds.HuifuPublic) != publicKeyFingerprint(creds.GatewayPublic) {
		t.Fatal("exported huifu public key should match the local sandbox response public key")
	}
	if creds.MerchantKeySource == "" {
		t.Fatal("merchant key source was not recorded")
	}
	data := map[string]any{"req_seq_id": "KEY-DIR-001", "huifu_id": "6666000100000001"}
	reqSig, err := signData(data, creds.MerchantPrivate)
	if err != nil {
		t.Fatal(err)
	}
	if err := verifyData(data, reqSig, creds.MerchantPublic); err != nil {
		t.Fatalf("merchant request signature should verify with merchant public key: %v", err)
	}
	if err := verifyData(data, reqSig, creds.GatewayPublic); err == nil {
		t.Fatal("merchant request signature unexpectedly verified with sandbox public key")
	}
	respSig, err := signData(data, creds.GatewayPrivate)
	if err != nil {
		t.Fatal(err)
	}
	if err := verifyData(data, respSig, creds.HuifuPublic); err != nil {
		t.Fatalf("sandbox response signature should verify with exported huifu public key: %v", err)
	}
	if err := verifyData(data, respSig, creds.MerchantPublic); err == nil {
		t.Fatal("sandbox response signature unexpectedly verified with merchant public key")
	}
	summary := credentialProfileSummary(creds)
	raw, err := json.Marshal(summary)
	if err != nil {
		t.Fatal(err)
	}
	text := string(raw)
	for _, forbidden := range []string{"merchant_private", "PRIVATE KEY", "BEGIN " + "RSA PRIVATE KEY"} {
		if strings.Contains(text, forbidden) {
			t.Fatalf("profile summary leaked key material marker %q: %s", forbidden, text)
		}
	}
	if stringValue(summary["merchant_key_source"]) == "" {
		t.Fatalf("profile summary missing merchant_key_source: %s", text)
	}
	if stringValue(summary["sandbox_public_fingerprint"]) == "" {
		t.Fatalf("profile summary missing sandbox_public_fingerprint: %s", text)
	}
}

func TestOfficialDemoProfileExportRequiresExplicitPrivateOptIn(t *testing.T) {
	dataDir := t.TempDir()
	err := run([]string{"credentials", "export", "--credential-profile", officialDemoProfileName, "--data-dir", dataDir, "--format", "json"})
	if err == nil {
		t.Fatal("official-demo export unexpectedly succeeded without --allow-private-export")
	}
	if !strings.Contains(err.Error(), "--allow-private-export") {
		t.Fatalf("unexpected export error: %v", err)
	}

	out := filepath.Join(t.TempDir(), "creds.json")
	if err := run([]string{"credentials", "export", "--credential-profile", officialDemoProfileName, "--data-dir", dataDir, "--format", "json", "--allow-private-export", "--output", out}); err != nil {
		t.Fatalf("official-demo export with explicit opt-in failed: %v", err)
	}
	raw, err := os.ReadFile(out)
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(string(raw), "merchant_private_key") {
		t.Fatalf("export output missing official SDK private key field: %s", raw)
	}
	if !strings.Contains(string(raw), "merchant_public_key") {
		t.Fatalf("export output missing official SDK public key field: %s", raw)
	}
	var payload map[string]any
	if err := json.Unmarshal(raw, &payload); err != nil {
		t.Fatalf("decode export output: %v body=%s", err, raw)
	}
	wantKeys := []string{"gateway_url", "sys_id", "product_id", "huifu_id", "skill_source", "merchant_private_key", "merchant_public_key", "signature_model", "usage"}
	if len(payload) != len(wantKeys) {
		t.Fatalf("export output should use flat project config keys only: %+v", payload)
	}
	for _, key := range wantKeys {
		if _, ok := payload[key]; !ok {
			t.Fatalf("export output missing flat key %s: %+v", key, payload)
		}
	}
	for _, key := range []string{"sys_id", "product_id", "huifu_id", "skill_source", "merchant_private_key", "merchant_public_key", "signature_model", "usage"} {
		if strings.TrimSpace(stringValue(payload[key])) == "" {
			t.Fatalf("export output empty %s: %+v", key, payload)
		}
	}
	if stringValue(payload["skill_source"]) != sandboxSkillSource {
		t.Fatalf("skill_source = %s, want %s", payload["skill_source"], sandboxSkillSource)
	}
	for _, forbidden := range []string{"merchant_config", "sandbox_config", "field_usage", "export_schema", "watermark", "profile", "huifu_public_key", "merchant_private_pem", "huifu_public_pem", "BEGIN RSA PRIVATE KEY", "BEGIN RSA PUBLIC KEY", "\\n", "商户项目配置", "沙箱侧信息"} {
		if strings.Contains(string(raw), forbidden) {
			t.Fatalf("export output contains unclean key material marker %q: %s", forbidden, raw)
		}
	}
	if strings.Contains(string(raw), "local_response_public_pem") {
		t.Fatalf("export output should not expose a separate local response key field: %s", raw)
	}
}

func TestOfficialDemoProfileEnvelopeEnforcement(t *testing.T) {
	app := newTestAppWithOptions(t, AppOptions{CredentialProfile: officialDemoProfileName})
	handler := app.gatewayHandler()
	okResp := postGateway(t, app, handler, "/v4/trade/payment/create", map[string]any{
		"req_seq_id": "OFFICIAL-DEMO-OK",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.01",
		"goods_desc": "official demo profile",
	})
	assertDataCode(t, app, okResp, "00000100")

	data := map[string]any{
		"req_seq_id": "OFFICIAL-DEMO-BAD-SYS",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.01",
		"goods_desc": "official demo profile mismatch",
	}
	signature, err := signData(data, app.creds.MerchantPrivate)
	if err != nil {
		t.Fatal(err)
	}
	body, _ := json.Marshal(Envelope{SysID: "SYS", ProductID: officialDemoProductID, Sign: signature, Data: data})
	req := httptest.NewRequest(http.MethodPost, "/v4/trade/payment/create", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("jpt-x-skill-source", sandboxSkillSource)
	req.Header.Set("jpt-x-skill-huifu_id", "6666000100000001")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("mismatch status = %d body=%s", rec.Code, rec.Body.String())
	}
	var resp SignedResponse
	if err := json.Unmarshal(rec.Body.Bytes(), &resp); err != nil {
		t.Fatal(err)
	}
	assertDataCode(t, app, resp, "LS000008")
}

func TestOfficialDemoProfileReportMarksLocalSimulation(t *testing.T) {
	app := newTestAppWithOptions(t, AppOptions{CredentialProfile: officialDemoProfileName})
	if err := app.WriteReport(); err != nil {
		t.Fatal(err)
	}
	raw, err := os.ReadFile(filepath.Join(app.reportDir, "summary.json"))
	if err != nil {
		t.Fatal(err)
	}
	text := string(raw)
	for _, forbidden := range []string{"merchant_private_pem", "PRIVATE KEY", "BEGIN " + "RSA PRIVATE KEY"} {
		if strings.Contains(text, forbidden) {
			t.Fatalf("summary leaked private key marker %q: %s", forbidden, text)
		}
	}
	var summary map[string]any
	if err := json.Unmarshal(raw, &summary); err != nil {
		t.Fatal(err)
	}
	if got := stringValue(summary["credential_profile"]); got != officialDemoProfileName {
		t.Fatalf("credential_profile = %s", got)
	}
	if got := stringValue(summary["signature_model"]); got != "dual_key_local_sandbox" {
		t.Fatalf("signature_model = %s", got)
	}
	if got := summary["official_signature"]; got != false {
		t.Fatalf("official_signature = %v, want false", got)
	}
	if stringValue(summary["huifu_public_fingerprint"]) == "" || stringValue(summary["merchant_public_fingerprint"]) == "" {
		t.Fatalf("summary missing fingerprints: %+v", summary)
	}
}

func TestOfficialProxyPassesThroughResponseWithoutResigning(t *testing.T) {
	upstreamCalled := false
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		upstreamCalled = true
		if r.URL.Path != "/v4/trade/payment/create" {
			t.Errorf("upstream path = %s", r.URL.Path)
		}
		raw, err := io.ReadAll(r.Body)
		if err != nil {
			t.Errorf("read upstream body: %v", err)
		}
		if !bytes.Contains(raw, []byte(`"sys_id":"`+officialDemoSysID+`"`)) {
			t.Errorf("upstream body missing official sys_id: %s", raw)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("X-Upstream-Trace", "official")
		_, _ = w.Write([]byte(`{"sign":"OFFICIAL_SIGN","data":{"resp_code":"00000000","resp_desc":"ok"}}`))
	}))
	defer upstream.Close()

	app := newTestAppWithOptions(t, AppOptions{
		CredentialProfile: officialDemoProfileName,
		Mode:              "official-proxy",
		OfficialGateway:   upstream.URL,
	})
	handler := app.gatewayHandler()
	data := map[string]any{
		"req_seq_id": "OFFICIAL-PROXY-001",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.01",
		"goods_desc": "official proxy",
	}
	signature, err := signData(data, app.creds.MerchantPrivate)
	if err != nil {
		t.Fatal(err)
	}
	body, _ := json.Marshal(Envelope{SysID: officialDemoSysID, ProductID: officialDemoProductID, Sign: signature, Data: data})
	req := httptest.NewRequest(http.MethodPost, "/v4/trade/payment/create", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("jpt-x-skill-source", sandboxSkillSource)
	req.Header.Set("jpt-x-skill-huifu_id", "6666000100000001")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("proxy status = %d body=%s", rec.Code, rec.Body.String())
	}
	if !upstreamCalled {
		t.Fatal("upstream was not called")
	}
	if got := rec.Header().Get("X-Upstream-Trace"); got != "official" {
		t.Fatalf("upstream header = %s, want official", got)
	}
	var resp SignedResponse
	if err := json.Unmarshal(rec.Body.Bytes(), &resp); err != nil {
		t.Fatal(err)
	}
	if resp.Sign != "OFFICIAL_SIGN" {
		t.Fatalf("proxy rewrote response sign = %s", resp.Sign)
	}
}

func TestValidateOfficialGatewayURLAllowlist(t *testing.T) {
	for _, raw := range []string{
		"https://paas.huifu.com/api",
		"https://api.huifu.com.cn/v2",
		"https://service.cloudpnr.com/gateway",
	} {
		if err := validateOfficialGatewayURL(raw); err != nil {
			t.Fatalf("official gateway URL %s was rejected: %v", raw, err)
		}
	}
	for _, raw := range []string{
		"http://paas.huifu.com/api",
		"https://example.com/api",
		"https://huifu.com.evil.test/api",
	} {
		if err := validateOfficialGatewayURL(raw); err == nil {
			t.Fatalf("official gateway URL %s unexpectedly passed", raw)
		}
	}
}

func TestAggregationRefundFlowAndAmountInvariant(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	payment := createPaidAggregationPayment(t, app, handler, "REQ-REFUND-AGG", "1.00")

	refund := postGateway(t, app, handler, "/v4/trade/payment/scanpay/refund", map[string]any{
		"req_date":      "20260624",
		"req_seq_id":    "RF-AGG-1",
		"huifu_id":      payment.HuifuID,
		"ord_amt":       "0.40",
		"org_req_date":  payment.ReqDate,
		"org_hf_seq_id": payment.HFSeqID,
	})
	assertDataCode(t, app, refund, "00000100")
	if got := stringValue(refund.Data["trans_stat"]); got != "P" {
		t.Fatalf("refund accepted trans_stat = %s, want P", got)
	}
	if got := stringValue(refund.Data["trade_type"]); got != "TRANS_REFUND" {
		t.Fatalf("refund trade_type = %s, want TRANS_REFUND", got)
	}
	if got := stringValue(refund.Data["org_hf_seq_id"]); got != payment.HFSeqID {
		t.Fatalf("refund org_hf_seq_id = %s, want %s", got, payment.HFSeqID)
	}

	overPending := postGateway(t, app, handler, "/v4/trade/payment/scanpay/refund", map[string]any{
		"req_date":      "20260624",
		"req_seq_id":    "RF-AGG-OVER-PENDING",
		"huifu_id":      payment.HuifuID,
		"ord_amt":       "0.70",
		"org_req_date":  payment.ReqDate,
		"org_hf_seq_id": payment.HFSeqID,
	})
	assertDataCode(t, app, overPending, "23000003")
	if got := stringValue(overPending.Data["trans_stat"]); got != "F" {
		t.Fatalf("over amount refund trans_stat = %s, want F", got)
	}

	query1 := postGateway(t, app, handler, "/v4/trade/payment/scanpay/refundquery", map[string]any{
		"huifu_id":       payment.HuifuID,
		"org_req_date":   "20260624",
		"org_req_seq_id": "RF-AGG-1",
	})
	assertDataCode(t, app, query1, "00000000")
	if got := stringValue(query1.Data["trans_stat"]); got != "P" {
		t.Fatalf("first refund query trans_stat = %s, want P", got)
	}
	query2 := postGateway(t, app, handler, "/v4/trade/payment/scanpay/refundquery", map[string]any{
		"huifu_id":       payment.HuifuID,
		"org_req_date":   "20260624",
		"org_req_seq_id": "RF-AGG-1",
	})
	if got := stringValue(query2.Data["trans_stat"]); got != "S" {
		t.Fatalf("second refund query trans_stat = %s, want S", got)
	}
	if got := stringValue(query2.Data["bank_message"]); got != "退款成功" {
		t.Fatalf("second refund query bank_message = %s, want 退款成功", got)
	}
	if _, ok := query2.Data["remark"]; !ok {
		t.Fatalf("second refund query missing remark: %+v", query2.Data)
	}

	app.mu.Lock()
	stored := *app.payments[payment.ReqSeqID]
	app.mu.Unlock()
	if stored.State != "S" {
		t.Fatalf("payment state changed by refund = %s, want S", stored.State)
	}
	if stored.RefundableAmt != "0.60" || stored.RefundedAmt != "0.40" {
		t.Fatalf("refund summary = refunded %s refundable %s, want 0.40/0.60", stored.RefundedAmt, stored.RefundableAmt)
	}

	wrongLocator := postGateway(t, app, handler, "/v4/trade/payment/scanpay/refundquery", map[string]any{
		"huifu_id":       payment.HuifuID,
		"org_req_date":   payment.ReqDate,
		"org_req_seq_id": payment.ReqSeqID,
	})
	assertDataCode(t, app, wrongLocator, "23000001")
	if got := stringValue(wrongLocator.Data["resp_desc"]); got != "原交易不存在" {
		t.Fatalf("wrong refund locator resp_desc = %s, want 原交易不存在", got)
	}
	if _, ok := wrongLocator.Data["trade_type"]; !ok {
		t.Fatalf("wrong refund locator missing trade_type: %+v", wrongLocator.Data)
	}
}

func TestAggregationOfficialLocators(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	create := postGateway(t, app, handler, "/v4/trade/payment/create", map[string]any{
		"req_seq_id": "REQ-AGG-LOCATOR",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.30",
		"goods_desc": "aggregation locator",
	})
	assertDataCode(t, app, create, "00000100")
	outOrdID := stringValue(create.Data["out_ord_id"])
	partyOrderID := stringValue(create.Data["party_order_id"])
	if outOrdID == "" || partyOrderID == "" {
		t.Fatalf("aggregation create missing official locators: %+v", create.Data)
	}

	query := postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", map[string]any{
		"huifu_id":   "6666000100000001",
		"out_ord_id": outOrdID,
	})
	assertDataCode(t, app, query, "00000000")
	if got := stringValue(query.Data["req_seq_id"]); got != "REQ-AGG-LOCATOR" {
		t.Fatalf("out_ord_id query req_seq_id = %s, want REQ-AGG-LOCATOR; data=%+v", got, query.Data)
	}

	postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", map[string]any{
		"huifu_id":   "6666000100000001",
		"out_ord_id": outOrdID,
	})
	refund := postGateway(t, app, handler, "/v4/trade/payment/scanpay/refund", map[string]any{
		"req_date":           "20260624",
		"req_seq_id":         "RF-AGG-PARTY-1",
		"huifu_id":           "6666000100000001",
		"ord_amt":            "0.10",
		"org_req_date":       "20260624",
		"org_party_order_id": partyOrderID,
	})
	assertDataCode(t, app, refund, "00000100")
	if got := stringValue(refund.Data["org_req_seq_id"]); got != "REQ-AGG-LOCATOR" {
		t.Fatalf("org_party_order_id refund org_req_seq_id = %s, want REQ-AGG-LOCATOR; data=%+v", got, refund.Data)
	}
}

func TestAggregationCloseFlowAndPaidGuard(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	create := postGateway(t, app, handler, "/v4/trade/payment/create", map[string]any{
		"req_seq_id": "REQ-CLOSE-AGG",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.30",
		"goods_desc": "close aggregation",
	})
	assertDataCode(t, app, create, "00000100")

	closeResp := postGateway(t, app, handler, "/v2/trade/payment/scanpay/close", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "CL-AGG-1",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-CLOSE-AGG",
	})
	assertDataCode(t, app, closeResp, "00000000")
	if got := stringValue(closeResp.Data["trans_stat"]); got != "P" {
		t.Fatalf("close trans_stat = %s, want P", got)
	}
	closeQuery1 := postGateway(t, app, handler, "/v2/trade/payment/scanpay/closequery", map[string]any{
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-CLOSE-AGG",
	})
	if got := stringValue(closeQuery1.Data["trans_stat"]); got != "P" {
		t.Fatalf("first close query trans_stat = %s, want P", got)
	}
	if got := stringValue(closeQuery1.Data["orgTransStat"]); got != "P" {
		t.Fatalf("first close query orgTransStat = %s, want P", got)
	}
	closeQuery2 := postGateway(t, app, handler, "/v2/trade/payment/scanpay/closequery", map[string]any{
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-CLOSE-AGG",
		"product_id":     "CLOSEPROD",
		"req_date":       "20260701",
		"req_seq_id":     "CO-REQ-CLOSE-AGG",
	})
	if got := stringValue(closeQuery2.Data["trans_stat"]); got != "S" {
		t.Fatalf("second close query trans_stat = %s, want S", got)
	}
	if got := stringValue(closeQuery2.Data["org_trans_stat"]); got != "F" {
		t.Fatalf("second close query org_trans_stat = %s, want F", got)
	}
	if got := stringValue(closeQuery2.Data["orgTransStat"]); got != "F" {
		t.Fatalf("second close query orgTransStat = %s, want F", got)
	}
	if got := stringValue(closeQuery2.Data["transStat"]); got != "S" {
		t.Fatalf("second close query transStat = %s, want S", got)
	}
	if got := stringValue(closeQuery2.Data["subRespCode"]); got != "00000000" {
		t.Fatalf("second close query subRespCode = %s, want 00000000", got)
	}
	if got := stringValue(closeQuery2.Data["subRespDesc"]); got != "查询成功" {
		t.Fatalf("second close query subRespDesc = %s, want 查询成功", got)
	}
	if got := stringValue(closeQuery2.Data["reqSeqId"]); got != "CO-REQ-CLOSE-AGG" {
		t.Fatalf("second close query reqSeqId = %s, want CO-REQ-CLOSE-AGG", got)
	}
	if got := stringValue(closeQuery2.Data["productId"]); got != "CLOSEPROD" {
		t.Fatalf("second close query productId = %s, want CLOSEPROD", got)
	}

	paid := createPaidAggregationPayment(t, app, handler, "REQ-CLOSE-PAID", "0.30")
	paidClose := postGateway(t, app, handler, "/v2/trade/payment/scanpay/close", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "CL-AGG-PAID",
		"huifu_id":       paid.HuifuID,
		"org_req_date":   paid.ReqDate,
		"org_req_seq_id": paid.ReqSeqID,
	})
	assertDataCode(t, app, paidClose, "LS200004")
}

func TestHostingRefundCloseAndSplitpay(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	control := app.controlHandler()
	hosting := createPaidHostingPayment(t, app, handler, control, "REQ-HOST-OPS", "1.20")

	refund := postGateway(t, app, handler, "/v2/trade/hosting/payment/htRefund", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "RF-HOST-1",
		"huifu_id":       hosting.HuifuID,
		"ord_amt":        "0.50",
		"org_req_date":   hosting.ReqDate,
		"org_req_seq_id": hosting.ReqSeqID,
	})
	assertDataCode(t, app, refund, "00000000")
	missingRefundQueryFields := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryRefundInfo", map[string]any{
		"huifu_id":       hosting.HuifuID,
		"org_req_date":   "20260624",
		"org_req_seq_id": "RF-HOST-1",
	})
	assertDataCode(t, app, missingRefundQueryFields, "LS000002")
	refundQueryReq := map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "QRY-RF-HOST-1",
		"huifu_id":       hosting.HuifuID,
		"org_req_date":   "20260624",
		"org_req_seq_id": "RF-HOST-1",
	}
	postGateway(t, app, handler, "/v2/trade/hosting/payment/queryRefundInfo", refundQueryReq)
	refundQuery2 := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryRefundInfo", refundQueryReq)
	if got := stringValue(refundQuery2.Data["trans_stat"]); got != "S" {
		t.Fatalf("hosting refund query trans_stat = %s, want S", got)
	}

	openHosting := createHostingPayment(t, app, handler, "REQ-HOST-CLOSE", "0.80")
	closeResp := postGateway(t, app, handler, "/v2/trade/hosting/payment/close", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "CL-HOST-1",
		"huifu_id":       openHosting.HuifuID,
		"org_req_date":   openHosting.ReqDate,
		"org_req_seq_id": openHosting.ReqSeqID,
	})
	assertDataCode(t, app, closeResp, "00000000")
	for key, want := range map[string]string{
		"resp_desc":      "操作成功",
		"org_trans_stat": "F",
		"trans_stat":     "S",
		"close_stat":     "S",
	} {
		if got := stringValue(closeResp.Data[key]); got != want {
			t.Fatalf("hosting close %s = %s, want %s", key, got, want)
		}
	}
	closeQuery := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", hostingQueryByOriginal(openHosting, "QRY-HOST-CLOSE-STATE"))
	if got := stringValue(closeQuery.Data["close_stat"]); got != "S" {
		t.Fatalf("hosting query close_stat = %s, want S", got)
	}
	if got := stringValue(closeQuery.Data["trans_stat"]); got != "F" {
		t.Fatalf("hosting query trans_stat = %s, want F", got)
	}
	if got := stringValue(closeQuery.Data["org_trans_stat"]); got != "F" {
		t.Fatalf("hosting query org_trans_stat = %s, want F", got)
	}
	if got := stringValue(closeQuery.Data["bank_code"]); got != "CLOSED" {
		t.Fatalf("hosting query bank_code = %s, want CLOSED", got)
	}
	if got := stringValue(closeQuery.Data["bank_desc"]); got != "交易已关单" {
		t.Fatalf("hosting query bank_desc = %s, want 交易已关单", got)
	}

	ordinaryQuery := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", hostingQueryByOriginal(hosting, "QRY-HOST-SPLITPAY-ORDINARY"))
	if _, ok := ordinaryQuery.Data["trans_list"]; ok {
		t.Fatal("ordinary queryorderinfo unexpectedly returned trans_list")
	}
	missingSplitpayFields := postGateway(t, app, handler, "/v2/trade/hosting/payment/splitpay/query", map[string]any{
		"huifu_id":       hosting.HuifuID,
		"org_req_date":   hosting.ReqDate,
		"org_req_seq_id": hosting.ReqSeqID,
	})
	assertDataCode(t, app, missingSplitpayFields, "LS000002")
	splitpay := postGateway(t, app, handler, "/v2/trade/hosting/payment/splitpay/query", map[string]any{
		"huifu_id":       hosting.HuifuID,
		"req_date":       "20260630",
		"req_seq_id":     "REQ-HOST-SPLITPAY-QRY-TEST",
		"org_req_date":   hosting.ReqDate,
		"org_req_seq_id": hosting.ReqSeqID,
	})
	expectedProductID := firstNonEmpty(app.creds.ProductID, "MYPAY")
	for key, want := range map[string]string{
		"resp_desc":        "查询成功",
		"product_id":       expectedProductID,
		"req_date":         "20260630",
		"req_seq_id":       "REQ-HOST-SPLITPAY-QRY-TEST",
		"order_stat":       "6",
		"business_variant": "hosting.splitpay",
	} {
		if got := stringValue(splitpay.Data[key]); got != want {
			t.Fatalf("splitpay %s = %s, want %s; data=%+v", key, got, want, splitpay.Data)
		}
	}
	transListRaw := stringValue(splitpay.Data["trans_list"])
	if transListRaw == "" {
		t.Fatalf("splitpay response missing trans_list: %+v", splitpay.Data)
	}
	var transList []map[string]any
	if err := json.Unmarshal([]byte(transListRaw), &transList); err != nil {
		t.Fatalf("splitpay trans_list is not JSON array string: %v; raw=%s", err, transListRaw)
	}
	if len(transList) != 2 {
		t.Fatalf("splitpay trans_list length = %d, want 2; list=%+v", len(transList), transList)
	}
	if got := stringValue(transList[0]["pay_type"]); got != "A_NATIVE" {
		t.Fatalf("splitpay first pay_type = %s, want A_NATIVE", got)
	}
	if got := stringValue(transList[1]["pay_type"]); got != "T_MINIAPP" {
		t.Fatalf("splitpay second pay_type = %s, want T_MINIAPP", got)
	}
	for i, item := range transList {
		if got := stringValue(item["trans_stat"]); got != "S" {
			t.Fatalf("splitpay item %d trans_stat = %s, want S", i, got)
		}
	}
	if _, err := parseJSONStringObject(stringValue(transList[0]["alipay_response"])); err != nil {
		t.Fatalf("splitpay alipay_response is not JSON object string: %v", err)
	}
	if _, err := parseJSONStringObject(stringValue(transList[1]["wx_response"])); err != nil {
		t.Fatalf("splitpay wx_response is not JSON object string: %v", err)
	}
}

func TestHostingQueryOfficialOrderStatAndPartyOrderLocator(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	control := app.controlHandler()
	payment := createHostingPayment(t, app, handler, "REQ-HOST-ORDER-STAT", "1.00")

	preOrderQuery := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", map[string]any{
		"req_date":     payment.ReqDate,
		"req_seq_id":   "QRY-HOST-ORDER-STAT-PREORDER",
		"pre_order_id": payment.PreOrderID,
	})
	assertDataCode(t, app, preOrderQuery, "LS000004")
	missingHuifuQuery := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", map[string]any{
		"req_date":       payment.ReqDate,
		"req_seq_id":     "QRY-HOST-ORDER-STAT-NO-HUIFU",
		"org_req_date":   payment.ReqDate,
		"org_req_seq_id": payment.ReqSeqID,
	})
	assertDataCode(t, app, missingHuifuQuery, "LS000004")

	pending := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", hostingQueryByOriginal(payment, "QRY-HOST-ORDER-STAT-PENDING"))
	assertDataCode(t, app, pending, "00000000")
	partyOrderID := stringValue(pending.Data["party_order_id"])
	if partyOrderID == "" {
		t.Fatalf("hosting query missing party_order_id: %+v", pending.Data)
	}
	if got := stringValue(pending.Data["order_stat"]); got != "2" {
		t.Fatalf("pending hosting order_stat = %s, want 2; data=%+v", got, pending.Data)
	}

	partyOnly := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", hostingQueryByParty(payment, "QRY-HOST-ORDER-STAT-PARTY", partyOrderID))
	assertDataCode(t, app, partyOnly, "00000000")
	if got := stringValue(partyOnly.Data["req_seq_id"]); got == "" {
		t.Fatalf("party_order_id query missing req_seq_id: %+v", partyOnly.Data)
	}

	code, body := postAdminJSON(t, app, control, "/__admin/hosting/success", map[string]any{"pre_order_id": payment.PreOrderID})
	if code != http.StatusOK || body["ok"] != true {
		t.Fatalf("/__admin/hosting/success status = %d body=%+v", code, body)
	}
	success := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", hostingQueryByParty(payment, "QRY-HOST-ORDER-STAT-SUCCESS", partyOrderID))
	assertDataCode(t, app, success, "00000000")
	if got := stringValue(success.Data["trans_stat"]); got != "S" {
		t.Fatalf("success hosting trans_stat = %s, want S; data=%+v", got, success.Data)
	}
	if got := stringValue(success.Data["order_stat"]); got != "1" {
		t.Fatalf("success hosting order_stat = %s, want 1; data=%+v", got, success.Data)
	}
}

func TestHostingRefundChannelProjectionFromLatestLogs(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	control := app.controlHandler()
	preorder := postGateway(t, app, handler, "/v2/trade/hosting/payment/preorder", map[string]any{
		"req_seq_id":     "REQ-HOST-RF-WX-ORIG",
		"req_date":       "20260701",
		"huifu_id":       "6666000100000001",
		"pre_order_type": "1",
		"trans_amt":      "0.05",
		"goods_desc":     "hosting refund channel original",
		"hosting_data":   `{"project_title":"local refund project","project_id":"PROJECT-HOST-RF-001","request_type":"P","private_info":"local refund private"}`,
		"wx_data":        `{"sub_appid":"wx-local-refund","body":"hosting refund channel original"}`,
	})
	assertDataCode(t, app, preorder, "00000000")
	preOrderID := stringValue(preorder.Data["pre_order_id"])
	getControlJSON(t, control, "/__merchant/hosting/callback?pre_order_id="+preOrderID)
	postControlJSON(t, app, control, "/__merchant/hosting/confirm", map[string]any{"pre_order_id": preOrderID})
	query := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", map[string]any{
		"req_date":       "20260701",
		"req_seq_id":     "QRY-HOST-RF-WX-ORIG",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260701",
		"org_req_seq_id": "REQ-HOST-RF-WX-ORIG",
	})
	assertDataCode(t, app, query, "00000000")
	if got := stringValue(query.Data["trans_stat"]); got != "S" {
		t.Fatalf("original hosting query trans_stat = %s, want S", got)
	}

	refund := postGateway(t, app, handler, "/v2/trade/hosting/payment/htRefund", map[string]any{
		"product_id":           "MYPAY",
		"req_seq_id":           "REQ-HOST-RF-WX",
		"req_date":             "20260701",
		"huifu_id":             "6666000100000001",
		"ord_amt":              "0.05",
		"org_req_date":         "20260701",
		"org_req_seq_id":       "REQ-HOST-RF-WX-ORIG",
		"terminal_device_data": `{"device_type":"4"}`,
		"risk_check_data":      `{"risk_mng_info":{"sub_trade_type":"4300"},"ip_address":"127.0.0.1"}`,
		"bank_info_data":       `{"card_acct_type":"P","bank_card_no":""}`,
		"notify_url":           "https://example.invalid/hosting-refund-notify",
	})
	assertDataCode(t, app, refund, "00000000")
	for key, want := range map[string]string{
		"product_id":   "MYPAY",
		"trans_stat":   "P",
		"bank_code":    "00000100",
		"bank_message": "交易正在处理中",
		"fee_amt":      "0.03",
		"pay_channel":  "T",
	} {
		if got := stringValue(refund.Data[key]); got != want {
			t.Fatalf("refund %s = %s, want %s; data=%+v", key, got, want, refund.Data)
		}
	}
	wxRefund, err := parseJSONStringObject(stringValue(refund.Data["wx_response"]))
	if err != nil {
		t.Fatalf("refund wx_response is not JSON object string: %v", err)
	}
	if got := stringValue(wxRefund["cash_refund_fee"]); got != "0.05" {
		t.Fatalf("refund wx_response.cash_refund_fee = %s, want 0.05", got)
	}

	queryReq := map[string]any{
		"product_id":     "MYPAY",
		"req_date":       "20260701",
		"req_seq_id":     "QRY-HOST-RF-WX",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260701",
		"org_req_seq_id": "REQ-HOST-RF-WX",
	}
	postGateway(t, app, handler, "/v2/trade/hosting/payment/queryRefundInfo", queryReq)
	refundQuery := postGateway(t, app, handler, "/v2/trade/hosting/payment/queryRefundInfo", queryReq)
	assertDataCode(t, app, refundQuery, "00000000")
	for key, want := range map[string]string{
		"product_id":     "MYPAY",
		"trans_stat":     "S",
		"bank_code":      "SUCCESS",
		"bank_message":   "退款成功",
		"fee_amt":        "0.03",
		"actual_ref_amt": "0.05",
		"pay_channel":    "T",
	} {
		if got := stringValue(refundQuery.Data[key]); got != want {
			t.Fatalf("refund query %s = %s, want %s; data=%+v", key, got, want, refundQuery.Data)
		}
	}
	if stringValue(refundQuery.Data["org_party_order_id"]) == "" || stringValue(refundQuery.Data["org_out_order_id"]) == "" || stringValue(refundQuery.Data["trans_finish_time"]) == "" {
		t.Fatalf("refund query missing original/order projection: %+v", refundQuery.Data)
	}
	acctSplit, err := parseJSONStringObject(stringValue(refundQuery.Data["acct_split_bunch"]))
	if err != nil {
		t.Fatalf("refund query acct_split_bunch is not JSON object string: %v", err)
	}
	if infos, ok := acctSplit["acct_infos"].([]any); !ok || len(infos) != 3 {
		t.Fatalf("refund query acct_split_bunch.acct_infos = %+v, want 3 rows", acctSplit["acct_infos"])
	}
	splitFeeInfo, err := parseJSONStringObject(stringValue(refundQuery.Data["split_fee_info"]))
	if err != nil {
		t.Fatalf("refund query split_fee_info is not JSON object string: %v", err)
	}
	if _, ok := splitFeeInfo["split_fee_details"].([]any); !ok {
		t.Fatalf("refund query split_fee_info missing details: %+v", splitFeeInfo)
	}
}

func TestGatewayFaultInjectionAndIdempotency(t *testing.T) {
	app := newTestApp(t)
	app.faultTimeoutDelay = time.Millisecond
	handler := app.gatewayHandler()

	businessFail := map[string]any{
		"req_seq_id":       "REQ-FAULT-BIZ",
		"req_date":         "20260624",
		"huifu_id":         "6666000100000001",
		"trade_type":       "A_NATIVE",
		"trans_amt":        "0.01",
		"goods_desc":       "fault business",
		"sandbox_scenario": "BUSINESS_FAIL",
	}
	failResp := postGateway(t, app, handler, "/v4/trade/payment/create", businessFail)
	assertDataCode(t, app, failResp, "LS200001")

	base := map[string]any{
		"req_seq_id": "REQ-IDEMP-1",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.01",
		"goods_desc": "idempotency",
	}
	first := postGateway(t, app, handler, "/v4/trade/payment/create", base)
	replay := postGateway(t, app, handler, "/v4/trade/payment/create", base)
	if stringValue(first.Data["hf_seq_id"]) != stringValue(replay.Data["hf_seq_id"]) {
		t.Fatalf("idempotent replay returned a different hf_seq_id: %v vs %v", first.Data, replay.Data)
	}
	conflictData := map[string]any{}
	for key, value := range base {
		conflictData[key] = value
	}
	conflictData["trans_amt"] = "0.02"
	conflict := postGateway(t, app, handler, "/v4/trade/payment/create", conflictData)
	assertDataCode(t, app, conflict, "LS000006")

	status, _ := postGatewayRaw(t, app, handler, "/v4/trade/payment/create", base, map[string]string{"jpt-x-sandbox-scenario": "FAULT-500"})
	if status != http.StatusInternalServerError {
		t.Fatalf("FAULT-500 status = %d, want 500", status)
	}
	status, _ = postGatewayRaw(t, app, handler, "/v4/trade/payment/create", base, map[string]string{"jpt-x-sandbox-scenario": "TIMEOUT"})
	if status != http.StatusGatewayTimeout {
		t.Fatalf("TIMEOUT status = %d, want 504", status)
	}
}

func TestControlSecurityRequiresCSRFAndLocalOrigin(t *testing.T) {
	app := newTestApp(t)
	handler := app.controlHandler()

	body, _ := json.Marshal(map[string]any{"pre_order_id": "PO-UNKNOWN"})
	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__merchant/hosting/confirm", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("missing CSRF status = %d, want 403", rec.Code)
	}

	req = httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__health/ready", nil)
	req.Header.Set("Origin", "https://example.com")
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("external Origin status = %d, want 403", rec.Code)
	}
}

func TestHealthReadyRedactsControlSecrets(t *testing.T) {
	app := newTestApp(t)
	handler := app.controlHandler()

	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__health/ready", nil))
	if rec.Code != http.StatusOK {
		t.Fatalf("ready status = %d body=%s", rec.Code, rec.Body.String())
	}
	body := rec.Body.String()
	for _, leaked := range []string{app.adminToken, app.csrfToken, app.webhookEndpointKey} {
		if leaked != "" && strings.Contains(body, leaked) {
			t.Fatalf("ready leaked control secret %q: %s", leaked, body)
		}
	}
}

func TestNextIDUsesLetterSeparator(t *testing.T) {
	id := nextID("HF")
	if strings.Contains(id, ".") {
		t.Fatalf("nextID contains dot: %s", id)
	}
	if !regexp.MustCompile(`^HF[0-9]{14}N[0-9]{9}$`).MatchString(id) {
		t.Fatalf("nextID format = %s, want prefix + yyyyMMddHHmmss + N + nanoseconds", id)
	}
}

func TestDeclarationDeclineStopsOnlyFromSameOrigin(t *testing.T) {
	app := newTestApp(t)
	stopped := make(chan struct{}, 1)
	app.shutdown = func() { stopped <- struct{}{} }
	handler := app.controlHandler()

	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__ui/declaration/decline", bytes.NewReader([]byte(`{}`)))
	req.Header.Set("Origin", "http://127.0.0.1:9999")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("cross-port decline status = %d, want 403", rec.Code)
	}
	select {
	case <-stopped:
		t.Fatal("cross-origin decline stopped service")
	default:
	}

	req = httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__ui/declaration/decline", bytes.NewReader([]byte(`{}`)))
	req.Header.Set("Origin", "http://127.0.0.1")
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("same-origin decline status = %d body=%s", rec.Code, rec.Body.String())
	}
	select {
	case <-stopped:
	case <-time.After(time.Second):
		t.Fatal("same-origin decline did not stop service")
	}
}

func TestUpdateCheckEndpointReportsAvailableVersion(t *testing.T) {
	sha := strings.Repeat("a", 64)
	var updateServer *httptest.Server
	updateServer = httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]any{
			"schema_version":       "1.0",
			"name":                 appName,
			"channel":              "preview",
			"latest_version":       "1.0.2",
			"contract_bundle":      contractBundle,
			"source_skill_version": skillVersion,
			"release_notes_url":    "https://paas.huifu.com/docs/devtools/#/skillsv1_0",
			"download_page_url":    "https://paas.huifu.com/docs/devtools/#/skillsv1_0",
			"downloads": map[string]any{
				updatePlatformKey(): map[string]any{
					"name":       "hf-payment-local-sandbox_1.0.2_" + strings.ReplaceAll(runtimeOSArch(), "/", "_") + ".tar.gz",
					"url":        updateServer.URL + "/hf-payment-local-sandbox.tar.gz",
					"sha256":     sha,
					"size_bytes": 12345,
				},
			},
		})
	}))
	defer updateServer.Close()

	app := newTestAppWithOptions(t, AppOptions{UpdateIndexURL: updateServer.URL + "/hf-payment-local-sandbox-latest.json"})
	handler := app.controlHandler()
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__ui/update/check", nil))
	if rec.Code != http.StatusOK {
		t.Fatalf("update check status = %d body=%s", rec.Code, rec.Body.String())
	}
	body := rec.Body.String()
	for _, leaked := range []string{app.adminToken, app.csrfToken, app.webhookEndpointKey} {
		if leaked != "" && strings.Contains(body, leaked) {
			t.Fatalf("update check leaked control secret %q: %s", leaked, body)
		}
	}
	var result map[string]any
	if err := json.Unmarshal([]byte(body), &result); err != nil {
		t.Fatalf("decode update result: %v", err)
	}
	if result["update_available"] != true {
		t.Fatalf("update_available = %v, want true; body=%s", result["update_available"], body)
	}
	if result["platform_supported"] != true {
		t.Fatalf("platform_supported = %v, want true; body=%s", result["platform_supported"], body)
	}
	download, ok := result["download"].(map[string]any)
	if !ok {
		t.Fatalf("missing download: %+v", result)
	}
	if got := stringValue(download["sha256"]); got != sha {
		t.Fatalf("download sha256 = %s, want %s", got, sha)
	}
}

func TestControlUIDashboardAndStateRedaction(t *testing.T) {
	app := newTestApp(t)
	app.gatewayBaseURL = "http://127.0.0.1:8766"
	app.payments["REQ-UI"] = &Payment{
		Kind:          "aggregation",
		HuifuID:       "6666000100000001",
		ReqDate:       "20260624",
		ReqSeqID:      "REQ-UI",
		HFSeqID:       "HF-UI",
		TradeType:     "A_NATIVE",
		TransAmt:      "0.01",
		GoodsDesc:     "ui test",
		NotifyURL:     "http://127.0.0.1:9000/notify?secret=value",
		RequestDigest: "sha256:test",
		State:         "P",
	}
	app.refunds[operationKey("aggregation", "RF-UI")] = &RefundOperation{
		Kind:            "aggregation",
		HuifuID:         "6666000100000001",
		ReqDate:         "20260624",
		ReqSeqID:        "RF-UI",
		PaymentReqSeqID: "REQ-UI",
		OrdAmt:          "0.01",
		State:           "S",
	}
	app.closes[operationKey("aggregation", "CL-UI")] = &CloseOperation{
		Kind:            "aggregation",
		HuifuID:         "6666000100000001",
		ReqDate:         "20260624",
		ReqSeqID:        "CL-UI",
		PaymentReqSeqID: "REQ-UI",
		State:           "P",
	}
	app.record("ui.test", "/test", "REQ-UI", map[string]any{
		"target": "http://127.0.0.1:9000/webhook?token=value",
	})
	app.events = append(app.events, Event{
		Time:       time.Now().UTC().Format(time.RFC3339Nano),
		Type:       "ui.secret_top_fields",
		Endpoint:   "http://127.0.0.1:9000/event?token=ui-top-leak",
		EntityID:   "Authorization: Bearer ui-top-leak",
		ScenarioID: "token: ui-top-leak",
		Details: map[string]any{
			"note": "top field redaction",
		},
	})
	app.notifications = append(app.notifications, NotificationDelivery{
		ID:              "ND-UI",
		PaymentReqSeqID: "REQ-UI",
		Target:          "http://127.0.0.1:9000/notify?token=value",
		TargetRedacted:  "http://127.0.0.1:9000/notify?REDACTED",
		Status:          "blocked",
		ExpectedACK:     expectedNotifyACK("REQ-UI"),
		Error:           "Authorization: Bearer ui-top-leak",
		Diagnosis:       "token: ui-top-leak",
	})
	app.webhooks = append(app.webhooks, WebhookDelivery{
		ID:             "WD-UI",
		EventType:      webhookEventPayment,
		EntityID:       "REQ-UI",
		Target:         "http://127.0.0.1:9000/webhook?token=value",
		TargetRedacted: "http://127.0.0.1:9000/webhook?REDACTED",
		Status:         "blocked",
		Error:          "-----BEGIN CERTIFICATE-----\nui-top-leak\n-----END CERTIFICATE-----",
		Diagnosis:      "Bearer ui-top-leak",
	})
	app.securityFindings = append(app.securityFindings, SecurityFinding{
		Type:           "notify_target_blocked",
		Severity:       "high",
		Target:         "http://127.0.0.1:9000/notify?token=value",
		TargetRedacted: "http://127.0.0.1:9000/notify?REDACTED",
		Reason:         "test",
	})
	handler := app.controlHandler()

	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "http://127.0.0.1/", nil))
	if rec.Code != http.StatusOK {
		t.Fatalf("control UI status = %d, want 200", rec.Code)
	}
	html := rec.Body.String()
	if !strings.Contains(html, "汇付支付本地沙箱服务") || !strings.Contains(html, "/__asset/huifu-logo.png") || !strings.Contains(html, "supportModal") {
		t.Fatalf("control UI did not render dashboard HTML: %s", rec.Body.String())
	}
	for _, want := range []string{"usageModal", "exportCredentialsBtn", "导出凭证", "使用说明", "workspaceTabs", "scrollTopBtn", "data-delivery-channel", "requestLogTable", "logDetailModal", "复制 JSON", "webhookTargetInput", "saveWebhookTargetBtn", "showWebhookKeyBtn", "webhook_endpoint_key", "hfps/1.3.1;sandbox/1.0.1"} {
		if !strings.Contains(html, want) {
			t.Fatalf("control UI missing %q: %s", want, html)
		}
	}
	for _, forbidden := range []string{"copyCredentialCommandBtn", "credentialCommand", "credentials export --credential-profile"} {
		if strings.Contains(html, forbidden) {
			t.Fatalf("control UI still contains command export affordance %q: %s", forbidden, html)
		}
	}

	for _, asset := range []string{"huifu-logo.png", "support-groups.png"} {
		rec = httptest.NewRecorder()
		handler.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__asset/"+asset, nil))
		if rec.Code != http.StatusOK {
			t.Fatalf("asset %s status = %d body=%s", asset, rec.Code, rec.Body.String())
		}
		if got := rec.Header().Get("Content-Type"); got != "image/png" {
			t.Fatalf("asset %s content-type = %s, want image/png", asset, got)
		}
		if rec.Body.Len() == 0 {
			t.Fatalf("asset %s response body is empty", asset)
		}
	}

	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__ui/state", nil))
	if rec.Code != http.StatusOK {
		t.Fatalf("UI state status = %d, want 200", rec.Code)
	}
	body := rec.Body.String()
	for _, leaked := range []string{"secret=value", "token=value", "ui-top-leak", app.adminToken, app.csrfToken, app.webhookEndpointKey} {
		if strings.Contains(body, leaked) {
			t.Fatalf("UI state leaked %q: %s", leaked, body)
		}
	}
	if !strings.Contains(body, "REDACTED") {
		t.Fatalf("UI state did not include redacted targets: %s", body)
	}
	var snapshot map[string]any
	if err := json.Unmarshal([]byte(body), &snapshot); err != nil {
		t.Fatalf("decode UI state: %v", err)
	}
	ready, ok := snapshot["ready"].(map[string]any)
	if !ok {
		t.Fatalf("UI state missing ready: %+v", snapshot)
	}
	if got := stringValue(ready["gateway_url"]); got != app.gatewayBaseURL {
		t.Fatalf("gateway_url = %s, want %s", got, app.gatewayBaseURL)
	}
	if got := stringValue(ready["sandbox_skill_source"]); got != sandboxSkillSource {
		t.Fatalf("sandbox_skill_source = %s, want %s", got, sandboxSkillSource)
	}
	if got := snapshot["refund_state_counts"].(map[string]any)["S"]; got != float64(1) {
		t.Fatalf("refund success count = %v, want 1", got)
	}
	refundRows, ok := snapshot["refunds"].([]any)
	if !ok || len(refundRows) != 1 {
		t.Fatalf("UI state refund rows = %+v, want one row", snapshot["refunds"])
	}
	refundRow, ok := refundRows[0].(map[string]any)
	if !ok {
		t.Fatalf("UI state refund row has unexpected shape: %+v", refundRows[0])
	}
	if got := stringValue(refundRow["settled_status"]); got != "已完成" {
		t.Fatalf("refund settled_status = %s, want 已完成", got)
	}
	if got := snapshot["close_state_counts"].(map[string]any)["P"]; got != float64(1) {
		t.Fatalf("close processing count = %v, want 1", got)
	}
}

func TestAdminCredentialExportRequiresAuthAndCSRF(t *testing.T) {
	app := newTestAppWithOptions(t, AppOptions{CredentialProfile: officialDemoProfileName})
	app.gatewayBaseURL = "http://127.0.0.1:8766"
	handler := app.controlHandler()

	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/credentials/export", bytes.NewReader([]byte("{}"))))
	if rec.Code != http.StatusUnauthorized {
		t.Fatalf("unauthorized export status = %d, want 401", rec.Code)
	}

	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/credentials/export", bytes.NewReader([]byte("{}")))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("missing CSRF export status = %d, want 403", rec.Code)
	}

	req = httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__admin/credentials/export", nil)
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusMethodNotAllowed {
		t.Fatalf("GET export status = %d, want 405", rec.Code)
	}

	req = httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/credentials/export", bytes.NewReader([]byte("{}")))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("authorized export status = %d body=%s", rec.Code, rec.Body.String())
	}
	if got := rec.Header().Get("Content-Disposition"); !strings.Contains(got, `filename="sandbox-credentials.json"`) {
		t.Fatalf("Content-Disposition = %q", got)
	}
	if got := rec.Header().Get("Cache-Control"); got != "no-store" {
		t.Fatalf("Cache-Control = %q, want no-store", got)
	}
	var payload map[string]any
	if err := json.Unmarshal(rec.Body.Bytes(), &payload); err != nil {
		t.Fatalf("decode credential export: %v body=%s", err, rec.Body.String())
	}
	wantKeys := []string{"gateway_url", "sys_id", "product_id", "huifu_id", "skill_source", "merchant_private_key", "merchant_public_key", "webhook_endpoint_key", "signature_model", "usage"}
	if len(payload) != len(wantKeys) {
		t.Fatalf("credential export should be flat project config keys only, got %+v", payload)
	}
	for _, field := range wantKeys {
		if strings.TrimSpace(stringValue(payload[field])) == "" {
			t.Fatalf("credential export missing %s: %+v", field, payload)
		}
	}
	if stringValue(payload["sys_id"]) != officialDemoSysID || stringValue(payload["product_id"]) != officialDemoProductID {
		t.Fatalf("official-demo ids mismatch: %+v", payload)
	}
	if stringValue(payload["gateway_url"]) != app.gatewayBaseURL {
		t.Fatalf("gateway_url = %s, want %s", payload["gateway_url"], app.gatewayBaseURL)
	}
	if stringValue(payload["huifu_id"]) != "6666000100000001" {
		t.Fatalf("huifu_id = %s", payload["huifu_id"])
	}
	if stringValue(payload["skill_source"]) != sandboxSkillSource {
		t.Fatalf("skill_source = %s, want %s", payload["skill_source"], sandboxSkillSource)
	}
	if stringValue(payload["webhook_endpoint_key"]) != app.webhookEndpointKey {
		t.Fatalf("webhook_endpoint_key mismatch")
	}
	merchantPrivateKey := stringValue(payload["merchant_private_key"])
	merchantPublicKey := stringValue(payload["merchant_public_key"])
	if strings.Contains(merchantPrivateKey, "BEGIN ") || strings.Contains(merchantPublicKey, "BEGIN ") || strings.Contains(merchantPrivateKey, "\n") || strings.Contains(merchantPublicKey, "\n") {
		t.Fatalf("official SDK key fields should be headerless Base64: %+v", payload)
	}
	if strings.Contains(rec.Body.String(), "merchant_private_pem") || strings.Contains(rec.Body.String(), "huifu_public_pem") {
		t.Fatalf("credential export should not contain PEM compatibility fields: %s", rec.Body.String())
	}
	if strings.Contains(rec.Body.String(), "merchant_config") || strings.Contains(rec.Body.String(), "sandbox_config") || strings.Contains(rec.Body.String(), "field_usage") || strings.Contains(rec.Body.String(), "export_schema") || strings.Contains(rec.Body.String(), "watermark") || strings.Contains(rec.Body.String(), "profile") {
		t.Fatalf("credential export should not contain duplicate metadata or nested sections: %s", rec.Body.String())
	}
	if strings.Contains(rec.Body.String(), "huifu_public_key") || strings.Contains(rec.Body.String(), "商户项目配置") || strings.Contains(rec.Body.String(), "沙箱侧信息") {
		t.Fatalf("credential export should use English keys and merchant_public_key naming: %s", rec.Body.String())
	}
	if strings.Contains(rec.Body.String(), "merchant_private_key_format") || strings.Contains(rec.Body.String(), "merchant_public_key_format") || strings.Contains(rec.Body.String(), "huifu_id_hint") {
		t.Fatalf("credential export should not contain removed helper fields: %s", rec.Body.String())
	}
	if strings.Contains(rec.Body.String(), "local_response_public_pem") {
		t.Fatalf("credential export should not contain local_response_public_pem: %s", rec.Body.String())
	}
	if strings.Contains(rec.Body.String(), "sandbox_public_pem") {
		t.Fatalf("credential export should not contain a second public key alias: %s", rec.Body.String())
	}
	responseData := map[string]any{"resp_code": "00000000", "req_seq_id": "EXPORT-SIGN-001"}
	responseSign, err := signData(responseData, app.creds.GatewayPrivate)
	if err != nil {
		t.Fatal(err)
	}
	exportedMerchantPrivate, err := parsePrivateKeyMaterial(merchantPrivateKey)
	if err != nil {
		t.Fatalf("parse exported merchant_private_key: %v", err)
	}
	requestData := map[string]any{"req_seq_id": "EXPORT-SIGN-REQ-001", "huifu_id": "6666000100000001"}
	requestSign, err := signData(requestData, exportedMerchantPrivate)
	if err != nil {
		t.Fatal(err)
	}
	if err := verifyData(requestData, requestSign, app.creds.MerchantPublic); err != nil {
		t.Fatalf("exported merchant_private_key should sign requests verified by sandbox merchant public key: %v", err)
	}
	exportedMerchantPublicSDK, err := parsePublicKeyMaterial(merchantPublicKey)
	if err != nil {
		t.Fatalf("parse exported merchant_public_key: %v", err)
	}
	if err := verifyData(responseData, responseSign, exportedMerchantPublicSDK); err != nil {
		t.Fatalf("exported merchant_public_key should verify sandbox response signature: %v", err)
	}
}

func TestAdminWebhookTargetConfigurationRequiresAuthAndRedactsState(t *testing.T) {
	app := newTestApp(t)
	handler := app.controlHandler()
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNoContent)
	}))
	defer receiver.Close()
	target := receiver.URL + "/webhook?secret=value"

	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/webhook-targets", bytes.NewReader([]byte(`{"target":"`+target+`"}`)))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusUnauthorized {
		t.Fatalf("unauthorized webhook target status = %d, want 401", rec.Code)
	}

	req = httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/webhook-targets", bytes.NewReader([]byte(`{"target":"`+target+`"}`)))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("Content-Type", "application/json")
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("missing CSRF webhook target status = %d, want 403", rec.Code)
	}

	req = httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/webhook-targets", bytes.NewReader([]byte(`{"target":"http://example.com/webhook"}`)))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	req.Header.Set("Content-Type", "application/json")
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusBadRequest {
		t.Fatalf("external webhook target status = %d, want 400 body=%s", rec.Code, rec.Body.String())
	}

	req = httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/webhook-targets", bytes.NewReader([]byte(`{"target":"`+target+`"}`)))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	req.Header.Set("Content-Type", "application/json")
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("webhook target status = %d body=%s", rec.Code, rec.Body.String())
	}
	if len(app.webhookTargetsSnapshot()) != 1 {
		t.Fatalf("webhook target count = %d, want 1", len(app.webhookTargetsSnapshot()))
	}

	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__ui/state", nil))
	if rec.Code != http.StatusOK {
		t.Fatalf("UI state status = %d, want 200", rec.Code)
	}
	body := rec.Body.String()
	if strings.Contains(body, "secret=value") {
		t.Fatalf("UI state leaked webhook target query: %s", body)
	}
	var snapshot map[string]any
	if err := json.Unmarshal(rec.Body.Bytes(), &snapshot); err != nil {
		t.Fatalf("decode UI state: %v", err)
	}
	ready := snapshot["ready"].(map[string]any)
	if got := ready["webhook_target_count"]; got != float64(1) {
		t.Fatalf("webhook_target_count = %v, want 1", got)
	}
	targets, ok := ready["webhook_targets"].([]any)
	if !ok || len(targets) != 1 || !strings.Contains(stringValue(targets[0]), "REDACTED") {
		t.Fatalf("webhook_targets not redacted: %+v", ready["webhook_targets"])
	}
}

func TestAdminSessionAndReportRequireAuthAndCSRF(t *testing.T) {
	app := newTestApp(t)
	handler := app.controlHandler()

	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__admin/session", nil))
	if rec.Code != http.StatusUnauthorized {
		t.Fatalf("unauthorized session status = %d, want 401", rec.Code)
	}

	req := httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__admin/session", nil)
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("authorized session status = %d body=%s", rec.Code, rec.Body.String())
	}
	var session map[string]any
	if err := json.Unmarshal(rec.Body.Bytes(), &session); err != nil {
		t.Fatal(err)
	}
	if stringValue(session["csrf_token"]) != app.csrfToken {
		t.Fatalf("session csrf mismatch: %+v", session)
	}

	req = httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__admin/report", nil)
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusMethodNotAllowed {
		t.Fatalf("GET report status = %d, want 405", rec.Code)
	}

	req = httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/report", bytes.NewReader([]byte("{}")))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("missing CSRF report status = %d, want 403", rec.Code)
	}

	req = httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/report", bytes.NewReader([]byte("{}")))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	rec = httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("authorized report status = %d body=%s", rec.Code, rec.Body.String())
	}
}

func TestAdminManualDeliverySendsNotifyAndWebhook(t *testing.T) {
	app := newTestApp(t)
	app.notifyRetryDelay = 0
	handler := app.controlHandler()

	var notifyPayloads []map[string]any
	var webhookPayloads []map[string]any
	var webhookSigns []string
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/notify":
			if err := r.ParseForm(); err != nil {
				t.Errorf("parse notify form: %v", err)
			}
			respData := r.Form.Get("resp_data")
			sign := r.Form.Get("sign")
			if err := verifyRaw(respData, sign, app.creds.GatewayPublic); err != nil {
				t.Errorf("manual notify signature invalid: %v", err)
			}
			var payload map[string]any
			if err := json.Unmarshal([]byte(respData), &payload); err != nil {
				t.Errorf("decode notify resp_data: %v", err)
			}
			notifyPayloads = append(notifyPayloads, payload)
			_, _ = w.Write([]byte(expectedNotifyACK(stringValue(payload["req_seq_id"]))))
		case "/webhook":
			raw, err := io.ReadAll(r.Body)
			if err != nil {
				t.Errorf("read webhook body: %v", err)
			}
			webhookSigns = append(webhookSigns, r.URL.Query().Get("sign"))
			if got, want := r.URL.Query().Get("sign"), webhookSignature(raw, app.webhookEndpointKey); got != want {
				t.Errorf("manual webhook sign = %s, want %s", got, want)
			}
			var payload map[string]any
			if err := json.Unmarshal(raw, &payload); err != nil {
				t.Errorf("decode webhook body: %v", err)
			}
			webhookPayloads = append(webhookPayloads, payload)
			w.WriteHeader(http.StatusNoContent)
		default:
			http.NotFound(w, r)
		}
	}))
	defer receiver.Close()
	if err := app.addWebhookTarget(receiver.URL + "/webhook?secret=redact"); err != nil {
		t.Fatal(err)
	}
	app.payments["REQ-MANUAL-DELIVERY"] = &Payment{
		Kind:      "aggregation",
		HuifuID:   "6666000100000001",
		ReqDate:   "20260624",
		ReqSeqID:  "REQ-MANUAL-DELIVERY",
		HFSeqID:   "HF-MANUAL-DELIVERY",
		TransAmt:  "0.01",
		GoodsDesc: "manual delivery",
		NotifyURL: receiver.URL + "/notify?secret=redact",
		State:     "P",
	}

	postAdminDeliver := func(payload map[string]any) (int, map[string]any) {
		raw, _ := json.Marshal(payload)
		req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/deliver", bytes.NewReader(raw))
		req.Header.Set("Authorization", "Bearer "+app.adminToken)
		req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
		req.Header.Set("Content-Type", "application/json")
		rec := httptest.NewRecorder()
		handler.ServeHTTP(rec, req)
		var body map[string]any
		if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
			t.Fatalf("decode admin delivery response: %v body=%s", err, rec.Body.String())
		}
		return rec.Code, body
	}

	code, body := postAdminDeliver(map[string]any{
		"channel":     "notify",
		"entity_type": "payment",
		"req_seq_id":  "REQ-MANUAL-DELIVERY",
		"outcome":     "failure",
	})
	if code != http.StatusOK || body["ok"] != true {
		t.Fatalf("manual notify response = %d %+v", code, body)
	}
	if len(notifyPayloads) != 1 {
		t.Fatalf("notify payload count = %d, want 1", len(notifyPayloads))
	}
	if got := stringValue(notifyPayloads[0]["trans_stat"]); got != "F" {
		t.Fatalf("manual notify trans_stat = %s, want F", got)
	}
	if got := stringValue(notifyPayloads[0]["resp_code"]); got != "LS200099" {
		t.Fatalf("manual notify resp_code = %s, want LS200099", got)
	}
	notifyResponseRaw, _ := json.Marshal(body)
	if strings.Contains(string(notifyResponseRaw), "secret=redact") {
		t.Fatalf("manual notify response leaked raw target: %s", notifyResponseRaw)
	}

	code, body = postAdminDeliver(map[string]any{
		"channel":     "webhook",
		"entity_type": "payment",
		"req_seq_id":  "REQ-MANUAL-DELIVERY",
		"outcome":     "success",
	})
	if code != http.StatusOK || body["ok"] != true {
		t.Fatalf("manual webhook response = %d %+v", code, body)
	}
	if len(webhookPayloads) != 1 {
		t.Fatalf("webhook payload count = %d, want 1", len(webhookPayloads))
	}
	if got := stringValue(webhookPayloads[0]["trans_stat"]); got != "S" {
		t.Fatalf("manual webhook trans_stat = %s, want S", got)
	}
	if got := stringValue(webhookPayloads[0]["sandbox_manual_outcome"]); got != "success" {
		t.Fatalf("manual webhook outcome = %s, want success", got)
	}
	webhookResponseRaw, _ := json.Marshal(body)
	if strings.Contains(string(webhookResponseRaw), "secret=redact") {
		t.Fatalf("manual webhook response leaked raw target: %s", webhookResponseRaw)
	}
	if strings.Contains(string(webhookResponseRaw), `"sign":`) {
		t.Fatalf("manual webhook response leaked full sign field: %s", webhookResponseRaw)
	}
	if len(webhookSigns) == 1 && webhookSigns[0] != "" && strings.Contains(string(webhookResponseRaw), webhookSigns[0]) {
		t.Fatalf("manual webhook response leaked full sign value: %s", webhookResponseRaw)
	}
}

func TestAdminHostingSuccessSettlesHostingPayment(t *testing.T) {
	app := newTestApp(t)
	control := app.controlHandler()
	gateway := app.gatewayHandler()
	payment := createHostingPayment(t, app, gateway, "REQ-HOST-ADMIN-SUCCESS", "0.20")

	code, body := postAdminJSON(t, app, control, "/__admin/hosting/success", map[string]any{
		"pre_order_id": payment.PreOrderID,
	})
	if code != http.StatusOK || body["ok"] != true {
		t.Fatalf("hosting success response = %d %+v", code, body)
	}
	app.mu.Lock()
	stored := *app.payments[payment.ReqSeqID]
	app.mu.Unlock()
	if stored.State != "S" || !stored.HostingConfirmed || !stored.HostingCallbackSeen {
		t.Fatalf("hosting payment was not settled by admin success: %+v", stored)
	}
	query := postGateway(t, app, gateway, "/v2/trade/hosting/payment/queryorderinfo", hostingQueryByOriginal(payment, "QRY-HOST-ADMIN-SUCCESS"))
	if got := stringValue(query.Data["trans_stat"]); got != "S" {
		t.Fatalf("query trans_stat after admin success = %s, want S", got)
	}
}

func TestHostingPaymentNotifyUsesOfficialFields(t *testing.T) {
	app := newTestApp(t)
	app.notifyRetryDelay = 0
	control := app.controlHandler()
	gateway := app.gatewayHandler()

	var notifyPayloads []map[string]any
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if err := r.ParseForm(); err != nil {
			t.Errorf("parse notify form: %v", err)
		}
		respData := r.Form.Get("resp_data")
		var payload map[string]any
		if err := json.Unmarshal([]byte(respData), &payload); err != nil {
			t.Errorf("decode hosting notify payload: %v body=%s", err, respData)
		}
		notifyPayloads = append(notifyPayloads, payload)
		_, _ = w.Write([]byte(expectedNotifyACK(stringValue(payload["req_seq_id"]))))
	}))
	defer receiver.Close()

	hostingData := `{"project_title":"Sandbox Project","project_id":"P123","request_type":"P"}`
	preorder := postGateway(t, app, gateway, "/v2/trade/hosting/payment/preorder", map[string]any{
		"req_seq_id":     "REQ-HOST-NOTIFY-FIELDS",
		"req_date":       "20260624",
		"huifu_id":       "6666000100000001",
		"trans_amt":      "0.50",
		"goods_desc":     "hosting notify fields",
		"pre_order_type": "1",
		"trans_type":     "A_NATIVE",
		"hosting_data":   hostingData,
		"notify_url":     receiver.URL + "/notify",
	})
	assertDataCode(t, app, preorder, "00000000")
	postAdminJSON(t, app, control, "/__admin/hosting/success", map[string]any{"pre_order_id": stringValue(preorder.Data["pre_order_id"])})

	if len(notifyPayloads) != 1 {
		t.Fatalf("hosting notify count = %d, want 1", len(notifyPayloads))
	}
	payload := notifyPayloads[0]
	for key, want := range map[string]string{
		"req_date":       "20260624",
		"req_seq_id":     "REQ-HOST-NOTIFY-FIELDS",
		"huifu_id":       "6666000100000001",
		"trans_stat":     "S",
		"trans_type":     "A_JSAPI",
		"party_order_id": "PARTY-REQ-HOST-NOTIFY-FIELDS",
		"out_trans_id":   "OUT-REQ-HOST-NOTIFY-FIELDS",
	} {
		if got := stringValue(payload[key]); got != want {
			t.Fatalf("hosting notify %s = %s, want %s; payload=%+v", key, got, want, payload)
		}
	}
	if stringValue(payload["hf_seq_id"]) == "" {
		t.Fatalf("hosting notify missing hf_seq_id: %+v", payload)
	}
	if _, ok := payload["order_stat"]; ok {
		t.Fatalf("hosting notify should not include order_stat; payload=%+v", payload)
	}
}

func TestHostingRefundOfficialLocatorsInheritOriginalNotifyURL(t *testing.T) {
	app := newTestApp(t)
	app.notifyRetryDelay = 0
	control := app.controlHandler()
	gateway := app.gatewayHandler()

	var notifyPayloads []map[string]any
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if err := r.ParseForm(); err != nil {
			t.Errorf("parse notify form: %v", err)
		}
		var payload map[string]any
		respData := r.Form.Get("resp_data")
		if err := json.Unmarshal([]byte(respData), &payload); err != nil {
			t.Errorf("decode notify payload: %v body=%s", err, respData)
		}
		notifyPayloads = append(notifyPayloads, payload)
		_, _ = w.Write([]byte(expectedNotifyACK(stringValue(payload["req_seq_id"]))))
	}))
	defer receiver.Close()

	hostingData := `{"project_title":"Sandbox Project","project_id":"P123","request_type":"P"}`
	preorder := postGateway(t, app, gateway, "/v2/trade/hosting/payment/preorder", map[string]any{
		"req_seq_id":     "REQ-HOST-RF-HF",
		"req_date":       "20260624",
		"huifu_id":       "6666000100000001",
		"trans_amt":      "0.50",
		"goods_desc":     "hosting refund official locator",
		"pre_order_type": "1",
		"trans_type":     "A_NATIVE",
		"hosting_data":   hostingData,
		"notify_url":     receiver.URL + "/notify",
	})
	assertDataCode(t, app, preorder, "00000000")
	preOrderID := stringValue(preorder.Data["pre_order_id"])
	postAdminJSON(t, app, control, "/__admin/hosting/success", map[string]any{"pre_order_id": preOrderID})
	payment := postGateway(t, app, gateway, "/v2/trade/hosting/payment/queryorderinfo", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "QRY-HOST-RF-HF",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-HOST-RF-HF",
	})
	assertDataCode(t, app, payment, "00000000")
	hfSeqID := stringValue(payment.Data["org_hf_seq_id"])
	partyOrderID := stringValue(payment.Data["party_order_id"])
	if hfSeqID == "" || partyOrderID == "" {
		t.Fatalf("hosting query missing official locators: %+v", payment.Data)
	}

	refund := postGateway(t, app, gateway, "/v2/trade/hosting/payment/htRefund", map[string]any{
		"req_date":           "20260624",
		"req_seq_id":         "RF-HOST-HF-1",
		"huifu_id":           "6666000100000001",
		"ord_amt":            "0.10",
		"org_req_date":       "20260624",
		"org_hf_seq_id":      hfSeqID,
		"org_party_order_id": partyOrderID,
	})
	assertDataCode(t, app, refund, "00000000")
	app.mu.Lock()
	refundRecord := *app.refunds[operationKey("hosting", "RF-HOST-HF-1")]
	app.mu.Unlock()
	if refundRecord.NotifyURL == "" {
		t.Fatalf("hosting refund did not inherit original notify_url: %+v", refundRecord)
	}
	postGateway(t, app, gateway, "/v2/trade/hosting/payment/queryRefundInfo", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "QRY-RF-HOST-HF-1",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "RF-HOST-HF-1",
	})
	query := postGateway(t, app, gateway, "/v2/trade/hosting/payment/queryRefundInfo", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "QRY-RF-HOST-HF-1",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "RF-HOST-HF-1",
	})
	if got := stringValue(query.Data["trans_stat"]); got != "S" {
		t.Fatalf("hosting refund query trans_stat = %s, want S", got)
	}
	if len(notifyPayloads) == 0 {
		t.Fatal("hosting refund success did not notify inherited notify_url")
	}
	last := notifyPayloads[len(notifyPayloads)-1]
	if got := stringValue(last["req_seq_id"]); got != "RF-HOST-HF-1" {
		t.Fatalf("refund notify req_seq_id = %s, want RF-HOST-HF-1; payload=%+v", got, last)
	}
	for key, want := range map[string]string{
		"org_req_seq_id": "REQ-HOST-RF-HF",
		"org_hf_seq_id":  hfSeqID,
		"ord_amt":        "0.10",
		"actual_ref_amt": "0.10",
		"trans_type":     "TRANS_REFUND",
		"trade_type":     "TRANS_REFUND",
		"party_order_id": partyOrderID,
		"trans_stat":     "S",
	} {
		if got := stringValue(last[key]); got != want {
			t.Fatalf("refund notify %s = %s, want %s; payload=%+v", key, got, want, last)
		}
	}
}

func TestCloseNotifyUsesOriginalPaymentNotifyURL(t *testing.T) {
	app := newTestApp(t)
	app.notifyRetryDelay = 0
	gateway := app.gatewayHandler()

	var notifyPayloads []map[string]any
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if err := r.ParseForm(); err != nil {
			t.Errorf("parse notify form: %v", err)
		}
		respData := r.Form.Get("resp_data")
		var payload map[string]any
		if err := json.Unmarshal([]byte(respData), &payload); err != nil {
			t.Errorf("decode close notify payload: %v body=%s", err, respData)
		}
		notifyPayloads = append(notifyPayloads, payload)
		_, _ = w.Write([]byte(expectedNotifyACK(stringValue(payload["req_seq_id"]))))
	}))
	defer receiver.Close()

	create := postGateway(t, app, gateway, "/v4/trade/payment/create", map[string]any{
		"req_seq_id": "REQ-CLOSE-NOTIFY",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.30",
		"goods_desc": "close notify",
		"notify_url": receiver.URL + "/notify",
	})
	assertDataCode(t, app, create, "00000100")
	closeResp := postGateway(t, app, gateway, "/v2/trade/payment/scanpay/close", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "CL-NOTIFY-1",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-CLOSE-NOTIFY",
	})
	assertDataCode(t, app, closeResp, "00000000")
	postGateway(t, app, gateway, "/v2/trade/payment/scanpay/closequery", map[string]any{
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-CLOSE-NOTIFY",
	})
	closeQuery := postGateway(t, app, gateway, "/v2/trade/payment/scanpay/closequery", map[string]any{
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-CLOSE-NOTIFY",
	})
	if got := stringValue(closeQuery.Data["trans_stat"]); got != "S" {
		t.Fatalf("close query trans_stat = %s, want S", got)
	}
	if len(notifyPayloads) != 1 {
		t.Fatalf("close notify count = %d, want 1", len(notifyPayloads))
	}
	if got := stringValue(notifyPayloads[0]["req_seq_id"]); got != "CL-NOTIFY-1" {
		t.Fatalf("close notify req_seq_id = %s, want CL-NOTIFY-1; payload=%+v", got, notifyPayloads[0])
	}
	if got := stringValue(notifyPayloads[0]["close_stat"]); got != "S" {
		t.Fatalf("close notify close_stat = %s, want S", got)
	}
}

func TestAdminManualDeliveryRejectsMissingTarget(t *testing.T) {
	app := newTestApp(t)
	handler := app.controlHandler()
	app.payments["REQ-NO-NOTIFY"] = &Payment{
		Kind:      "aggregation",
		HuifuID:   "6666000100000001",
		ReqDate:   "20260624",
		ReqSeqID:  "REQ-NO-NOTIFY",
		HFSeqID:   "HF-NO-NOTIFY",
		TransAmt:  "0.01",
		GoodsDesc: "manual delivery no target",
		State:     "P",
	}
	raw, _ := json.Marshal(map[string]any{
		"channel":     "notify",
		"entity_type": "payment",
		"req_seq_id":  "REQ-NO-NOTIFY",
		"outcome":     "success",
	})
	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1/__admin/deliver", bytes.NewReader(raw))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusBadRequest {
		t.Fatalf("manual notify without target status = %d body=%s", rec.Code, rec.Body.String())
	}
	if !strings.Contains(rec.Body.String(), "notify_url") {
		t.Fatalf("manual notify missing target error is unclear: %s", rec.Body.String())
	}
}

func TestDisableAdminRejectsEmptyBearer(t *testing.T) {
	app := newTestApp(t)
	app.adminDisabled = true
	app.adminToken = ""
	handler := app.controlHandler()
	req := httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__admin/state", nil)
	req.Header.Set("Authorization", "Bearer ")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusUnauthorized {
		t.Fatalf("disabled admin status = %d, want 401", rec.Code)
	}
}

func TestAdminStateDoesNotDeadlock(t *testing.T) {
	app := newTestApp(t)
	handler := app.controlHandler()
	req := httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__admin/state", nil)
	req.Header.Set("Authorization", "Bearer "+app.adminToken)

	done := make(chan *httptest.ResponseRecorder, 1)
	go func() {
		rec := httptest.NewRecorder()
		handler.ServeHTTP(rec, req)
		done <- rec
	}()

	select {
	case rec := <-done:
		if rec.Code != http.StatusOK {
			t.Fatalf("authorized admin state status = %d body=%s", rec.Code, rec.Body.String())
		}
	case <-time.After(500 * time.Millisecond):
		t.Fatal("authorized admin state request timed out; possible lock re-entry deadlock")
	}

	uiDone := make(chan *httptest.ResponseRecorder, 1)
	go func() {
		rec := httptest.NewRecorder()
		handler.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "http://127.0.0.1/__ui/state", nil))
		uiDone <- rec
	}()
	select {
	case rec := <-uiDone:
		if rec.Code != http.StatusOK {
			t.Fatalf("ui state after admin state status = %d body=%s", rec.Code, rec.Body.String())
		}
	case <-time.After(500 * time.Millisecond):
		t.Fatal("ui state timed out after admin state; global lock may still be held")
	}
}

func TestNotifyDeliveryAckSuccessAndDuplicate(t *testing.T) {
	app := newTestApp(t)
	app.notifyRetryDelay = 0
	payment := Payment{
		Kind:      "aggregation",
		HuifuID:   "6666000100000001",
		ReqDate:   "20260624",
		ReqSeqID:  "REQ-NOTIFY-1",
		HFSeqID:   "HF-NOTIFY-1",
		TransAmt:  "0.01",
		GoodsDesc: "notify test",
		State:     "S",
	}
	received := 0
	var receivedSign string
	var receivedRespData string
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		received++
		if r.Method != http.MethodPost {
			t.Errorf("method = %s, want POST", r.Method)
		}
		if !strings.Contains(r.Header.Get("Content-Type"), "application/x-www-form-urlencoded") {
			t.Errorf("content-type = %s", r.Header.Get("Content-Type"))
		}
		if err := r.ParseForm(); err != nil {
			t.Errorf("parse form: %v", err)
		}
		receivedSign = r.Form.Get("sign")
		receivedRespData = r.Form.Get("resp_data")
		_, _ = w.Write([]byte(expectedNotifyACK(payment.ReqSeqID)))
	}))
	defer receiver.Close()

	delivery, err := app.deliverNotification(payment, receiver.URL+"/notify?token=secret", false)
	if err != nil {
		t.Fatal(err)
	}
	if delivery.Status != "delivered" || len(delivery.Attempts) != 1 {
		t.Fatalf("delivery = %+v", delivery)
	}
	if strings.Contains(delivery.TargetRedacted, "secret") {
		t.Fatalf("target was not redacted: %s", delivery.TargetRedacted)
	}
	if err := verifyRaw(receivedRespData, receivedSign, app.creds.GatewayPublic); err != nil {
		t.Fatalf("notify signature invalid over raw resp_data: %v", err)
	}
	var respData map[string]any
	if err := json.Unmarshal([]byte(receivedRespData), &respData); err != nil {
		t.Fatal(err)
	}
	if got := stringValue(respData["req_seq_id"]); got != payment.ReqSeqID {
		t.Fatalf("notify req_seq_id = %s, want %s", got, payment.ReqSeqID)
	}

	duplicate, err := app.deliverNotification(payment, receiver.URL+"/notify", true)
	if err != nil {
		t.Fatal(err)
	}
	if !duplicate.Duplicate || duplicate.Status != "delivered" {
		t.Fatalf("duplicate delivery = %+v", duplicate)
	}
	if received != 2 {
		t.Fatalf("received notify count = %d, want 2", received)
	}
}

func TestNotifyDeliveryRetriesOnBadAck(t *testing.T) {
	app := newTestApp(t)
	app.notifyRetryDelay = 0
	payment := Payment{Kind: "aggregation", HuifuID: "6666000100000001", ReqDate: "20260624", ReqSeqID: "REQ-NOTIFY-2", HFSeqID: "HF-NOTIFY-2", TransAmt: "0.01", GoodsDesc: "notify retry", State: "S"}
	attempts := 0
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		attempts++
		_, _ = w.Write([]byte("BAD_ACK"))
	}))
	defer receiver.Close()

	delivery, err := app.deliverNotification(payment, receiver.URL+"/notify", false)
	if err == nil {
		t.Fatal("bad ACK delivery succeeded")
	}
	if delivery.Status != "failed" {
		t.Fatalf("delivery status = %s, want failed", delivery.Status)
	}
	if attempts != 4 || len(delivery.Attempts) != 4 {
		t.Fatalf("attempts = %d/%d, want 4", attempts, len(delivery.Attempts))
	}
}

func TestNotifyDeliveryDiagnosesUnsupportedContentType(t *testing.T) {
	app := newTestApp(t)
	app.notifyMaxAttempt = 1
	app.notifyRetryDelay = 0
	payment := Payment{Kind: "aggregation", HuifuID: "6666000100000001", ReqDate: "20260624", ReqSeqID: "REQ-NOTIFY-JSON", HFSeqID: "HF-NOTIFY-JSON", TransAmt: "0.01", GoodsDesc: "notify json-only", State: "S"}
	var contentType string
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		contentType = r.Header.Get("Content-Type")
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = w.Write([]byte(`{"success":false,"message":"Content type 'application/x-www-form-urlencoded;charset=UTF-8' not supported"}`))
	}))
	defer receiver.Close()

	delivery, err := app.deliverNotification(payment, receiver.URL+"/notify", false)
	if err == nil {
		t.Fatal("notify delivery unexpectedly succeeded")
	}
	if !strings.Contains(contentType, "application/x-www-form-urlencoded") {
		t.Fatalf("notify content-type = %s", contentType)
	}
	if !strings.Contains(contentType, "charset=UTF-8") {
		t.Fatalf("notify content-type missing charset: %s", contentType)
	}
	if !strings.Contains(delivery.Diagnosis, "表单参数 sign 和 resp_data") {
		t.Fatalf("diagnosis is unclear: %q", delivery.Diagnosis)
	}
	if len(delivery.Attempts) != 1 || !strings.Contains(delivery.Attempts[0].Diagnosis, "Webhook 才是 application/json") {
		t.Fatalf("attempt diagnosis missing: %+v", delivery.Attempts)
	}
}

func TestNotifyTargetBlockedAndReported(t *testing.T) {
	app := newTestApp(t)
	payment := Payment{Kind: "aggregation", HuifuID: "6666000100000001", ReqDate: "20260624", ReqSeqID: "REQ-NOTIFY-3", HFSeqID: "HF-NOTIFY-3", TransAmt: "0.01", GoodsDesc: "notify blocked", State: "S"}
	delivery, err := app.deliverNotification(payment, "http://192.168.1.9/notify?secret=value", false)
	if err == nil {
		t.Fatal("private non-loopback notify target was accepted")
	}
	if delivery.Status != "blocked" {
		t.Fatalf("delivery status = %s, want blocked", delivery.Status)
	}
	if len(app.securityFindings) != 1 {
		t.Fatalf("security findings = %d, want 1", len(app.securityFindings))
	}
	if strings.Contains(app.securityFindings[0].TargetRedacted, "value") {
		t.Fatalf("finding target was not redacted: %+v", app.securityFindings[0])
	}
}

func TestWebhookDeliveryDiagnosesUnsupportedContentType(t *testing.T) {
	app := newTestApp(t)
	app.notifyMaxAttempt = 1
	app.notifyRetryDelay = 0
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusUnsupportedMediaType)
		_, _ = w.Write([]byte(`{"success":false,"message":"Content type 'application/json' not supported"}`))
	}))
	defer receiver.Close()

	delivery, err := app.deliverWebhook(receiver.URL+"/webhook", webhookEventPayment, "REQ-WEBHOOK-JSON", map[string]any{
		"event_type": webhookEventPayment,
		"req_seq_id": "REQ-WEBHOOK-JSON",
	})
	if err == nil {
		t.Fatal("webhook delivery unexpectedly succeeded")
	}
	if !strings.Contains(delivery.Diagnosis, "application/json 原始请求体") {
		t.Fatalf("diagnosis is unclear: %q", delivery.Diagnosis)
	}
	if len(delivery.Attempts) != 1 || !strings.Contains(delivery.Attempts[0].Diagnosis, "URL query 读取 sign") {
		t.Fatalf("attempt diagnosis missing: %+v", delivery.Attempts)
	}
}

func TestWebhookDeliveryRawBodyAndFinalStateEvents(t *testing.T) {
	app := newTestApp(t)
	app.notifyRetryDelay = 0
	key := "12345678901234567890123456789012"
	if err := app.setWebhookEndpointKey(key); err != nil {
		t.Fatal(err)
	}
	handler := app.gatewayHandler()

	type receivedWebhook struct {
		eventType string
		sign      string
		raw       []byte
	}
	var received []receivedWebhook
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			t.Errorf("method = %s, want POST", r.Method)
		}
		if !strings.Contains(r.Header.Get("Content-Type"), "application/json") {
			t.Errorf("content-type = %s", r.Header.Get("Content-Type"))
		}
		raw, err := io.ReadAll(r.Body)
		if err != nil {
			t.Errorf("read webhook body: %v", err)
		}
		sign := r.URL.Query().Get("sign")
		wantSign := webhookSignature(raw, key)
		if sign == "" || sign != wantSign {
			t.Errorf("webhook sign = %s, want %s", sign, wantSign)
		}
		var payload map[string]any
		if err := json.Unmarshal(raw, &payload); err != nil {
			t.Errorf("decode webhook body: %v", err)
		}
		if strings.Contains(string(raw), "RECV_ORD_ID_") {
			t.Errorf("webhook body used notify ACK text: %s", raw)
		}
		received = append(received, receivedWebhook{eventType: stringValue(payload["event_type"]), sign: sign, raw: raw})
		w.WriteHeader(http.StatusNoContent)
	}))
	defer receiver.Close()
	if err := app.addWebhookTarget(receiver.URL + "/webhook?secret=should-redact"); err != nil {
		t.Fatal(err)
	}

	payment := createPaidAggregationPayment(t, app, handler, "REQ-WEBHOOK-PAY", "1.00")
	refund := postGateway(t, app, handler, "/v4/trade/payment/scanpay/refund", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "RF-WEBHOOK-1",
		"huifu_id":       payment.HuifuID,
		"ord_amt":        "0.20",
		"org_req_date":   payment.ReqDate,
		"org_req_seq_id": payment.ReqSeqID,
	})
	assertDataCode(t, app, refund, "00000100")
	postGateway(t, app, handler, "/v4/trade/payment/scanpay/refundquery", map[string]any{
		"huifu_id":       payment.HuifuID,
		"org_req_date":   "20260624",
		"org_req_seq_id": "RF-WEBHOOK-1",
	})
	postGateway(t, app, handler, "/v4/trade/payment/scanpay/refundquery", map[string]any{
		"huifu_id":       payment.HuifuID,
		"org_req_date":   "20260624",
		"org_req_seq_id": "RF-WEBHOOK-1",
	})

	postGateway(t, app, handler, "/v4/trade/payment/create", map[string]any{
		"req_seq_id": "REQ-WEBHOOK-CLOSE",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "0.30",
		"goods_desc": "webhook close",
	})
	closeResp := postGateway(t, app, handler, "/v2/trade/payment/scanpay/close", map[string]any{
		"req_date":       "20260624",
		"req_seq_id":     "CL-WEBHOOK-1",
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-WEBHOOK-CLOSE",
	})
	assertDataCode(t, app, closeResp, "00000000")
	postGateway(t, app, handler, "/v2/trade/payment/scanpay/closequery", map[string]any{
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-WEBHOOK-CLOSE",
	})
	postGateway(t, app, handler, "/v2/trade/payment/scanpay/closequery", map[string]any{
		"huifu_id":       "6666000100000001",
		"org_req_date":   "20260624",
		"org_req_seq_id": "REQ-WEBHOOK-CLOSE",
	})

	seen := map[string]bool{}
	for _, item := range received {
		seen[item.eventType] = true
		sum := md5.Sum(append(append([]byte{}, item.raw...), []byte(key)...))
		if item.sign != strings.ToUpper(hex.EncodeToString(sum[:])) {
			t.Fatalf("captured webhook signature mismatch for %s", item.eventType)
		}
	}
	for _, eventType := range []string{webhookEventPayment, webhookEventRefund, webhookEventClose} {
		if !seen[eventType] {
			t.Fatalf("missing webhook event type %s; received=%+v", eventType, received)
		}
	}
	if len(app.webhooks) != 3 {
		t.Fatalf("webhook deliveries = %d, want 3", len(app.webhooks))
	}
	if strings.Contains(app.webhooks[0].TargetRedacted, "should-redact") {
		t.Fatalf("webhook target was not redacted: %+v", app.webhooks[0])
	}
}

func TestReconciliationFileQueryFlow(t *testing.T) {
	app := newTestApp(t)
	controlServer := httptest.NewServer(app.controlHandler())
	defer controlServer.Close()
	app.controlBaseURL = controlServer.URL
	handler := app.gatewayHandler()

	data := map[string]any{
		"req_date":   "20260624",
		"req_seq_id": "RC-REQ-1",
		"huifu_id":   "6666000100000001",
		"file_date":  "20260623",
	}
	first := postGateway(t, app, handler, "/v2/trade/check/filequery", data)
	assertDataCode(t, app, first, "00000000")
	if got := stringValue(first.Data["bill_type"]); got != "TRADE_BILL" {
		t.Fatalf("default bill_type = %s, want TRADE_BILL", got)
	}
	task1 := first.Data["task_details"].(map[string]any)
	if got := stringValue(task1["task_stat"]); got != "FP" {
		t.Fatalf("first task_stat = %s, want FP", got)
	}
	if _, ok := first.Data["file_details"]; ok {
		t.Fatal("first filequery unexpectedly returned file_details")
	}

	second := postGateway(t, app, handler, "/v2/trade/check/filequery", data)
	assertDataCode(t, app, second, "00000000")
	task2 := second.Data["task_details"].(map[string]any)
	if got := stringValue(task2["task_stat"]); got != "S" {
		t.Fatalf("second task_stat = %s, want S", got)
	}
	fileDetails := second.Data["file_details"].(map[string]any)
	if stringValue(fileDetails["file_name"]) == "" || stringValue(fileDetails["file_Name"]) == "" {
		t.Fatalf("file details missing compatibility file names: %+v", fileDetails)
	}
	downloadURL := stringValue(fileDetails["download_url"])
	resp, err := http.Get(downloadURL)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	csvBody, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err)
	}
	if resp.StatusCode != http.StatusOK || !strings.Contains(string(csvBody), "TRADE_BILL") {
		t.Fatalf("download status/body = %d %s", resp.StatusCode, csvBody)
	}

	badType := postGateway(t, app, handler, "/v2/trade/check/filequery", map[string]any{
		"req_date":   "20260624",
		"req_seq_id": "RC-REQ-BAD",
		"huifu_id":   "6666000100000001",
		"file_date":  "20260623",
		"bill_type":  "BAD_BILL",
	})
	assertDataCode(t, app, badType, "LS200006")
}

func TestReportWritesCoverageFiles(t *testing.T) {
	app := newTestApp(t)
	app.record("test.event", "/test", "E1", map[string]any{"ok": true})
	if err := app.WriteReport(); err != nil {
		t.Fatal(err)
	}
	for _, name := range []string{
		"summary.json",
		"events.ndjson",
		"final-state.json",
		"contract-coverage.json",
		"endpoint-coverage.json",
		"fixture-coverage.json",
		"business-scenario-coverage.json",
		"sample-coverage.json",
		"sample-import-report.json",
		"sandbox-scope-boundaries.json",
		"scenario-results.json",
		"notify-attempts.json",
		"webhook-attempts.json",
		"request-logs.json",
		"reconciliation-files.json",
		"security-findings.json",
		"secret-scan.json",
		"report-manifest.json",
	} {
		if _, err := os.Stat(filepath.Join(app.reportDir, name)); err != nil {
			t.Fatalf("missing report file %s: %v", name, err)
		}
	}
	finalStateBytes, err := os.ReadFile(filepath.Join(app.reportDir, "final-state.json"))
	if err != nil {
		t.Fatal(err)
	}
	var finalState map[string]any
	if err := json.Unmarshal(finalStateBytes, &finalState); err != nil {
		t.Fatal(err)
	}
	for _, key := range []string{"payments", "refunds", "closes", "reconciliation_files"} {
		if _, ok := finalState[key]; !ok {
			t.Fatalf("final-state missing %s", key)
		}
	}
	endpointCoverageBytes, err := os.ReadFile(filepath.Join(app.reportDir, "endpoint-coverage.json"))
	if err != nil {
		t.Fatal(err)
	}
	var endpointCoverage map[string]any
	if err := json.Unmarshal(endpointCoverageBytes, &endpointCoverage); err != nil {
		t.Fatal(err)
	}
	endpoints := endpointCoverage["endpoints"].([]any)
	for _, raw := range endpoints {
		endpoint := raw.(map[string]any)
		if got := stringValue(endpoint["status"]); got != "not_executed" {
			t.Fatalf("endpoint %s status = %s, want not_executed without scenario runner", endpoint["id"], got)
		}
	}
}

func TestScenarioValidationProducesExecutionCoverage(t *testing.T) {
	reportDir := filepath.Join(t.TempDir(), "scenario-report")
	report, err := runScenarioValidation(reportDir)
	if err != nil {
		t.Fatalf("scenario validation failed: %v report=%+v", err, report)
	}
	if !report.OK || report.ScenarioCount != 50 || report.Passed != 50 {
		t.Fatalf("unexpected scenario report: %+v", report)
	}
	if report.FixtureRunnerVersion != fixtureRunnerVersion {
		t.Fatalf("fixture runner version = %s, want %s", report.FixtureRunnerVersion, fixtureRunnerVersion)
	}
	if len(report.EndpointSummary) != 13 {
		t.Fatalf("endpoint summary count = %d, want 13", len(report.EndpointSummary))
	}
	for endpointID, status := range report.EndpointSummary {
		if status != "covered" {
			t.Fatalf("endpoint %s status = %s, want covered", endpointID, status)
		}
	}
	if len(report.FixtureSummary) != 92 {
		t.Fatalf("fixture summary count = %d, want 92", len(report.FixtureSummary))
	}
	for fixtureID, status := range report.FixtureSummary {
		if status != "covered" {
			t.Fatalf("fixture %s status = %s, want covered", fixtureID, status)
		}
	}
	if report.FixtureSummary["agg-close-channel-unpaid-order-query"] != "covered" {
		t.Fatalf("agg-close-channel-unpaid-order-query status = %s, want covered", report.FixtureSummary["agg-close-channel-unpaid-order-query"])
	}
	for _, name := range []string{"scenario-results.json", "endpoint-coverage.json", "fixture-coverage.json", "contract-coverage.json", "business-scenario-coverage.json", "sample-coverage.json", "sample-import-report.json", "sandbox-scope-boundaries.json"} {
		if _, err := os.Stat(filepath.Join(reportDir, name)); err != nil {
			t.Fatalf("missing scenario report file %s: %v", name, err)
		}
	}
	endpointCoverageBytes, err := os.ReadFile(filepath.Join(reportDir, "endpoint-coverage.json"))
	if err != nil {
		t.Fatal(err)
	}
	var endpointCoverage map[string]any
	if err := json.Unmarshal(endpointCoverageBytes, &endpointCoverage); err != nil {
		t.Fatal(err)
	}
	for _, raw := range endpointCoverage["endpoints"].([]any) {
		endpoint := raw.(map[string]any)
		if got := stringValue(endpoint["status"]); got != "covered" {
			t.Fatalf("endpoint report %s status = %s, want covered", endpoint["id"], got)
		}
	}
}

func TestContractValidationCatchesManifestAndFixtureDrift(t *testing.T) {
	bundle, err := loadContractBundle()
	if err != nil {
		t.Fatal(err)
	}
	digestDrift := *bundle
	digestDrift.ReferenceDigests = bundle.ReferenceDigests
	digestDrift.ReferenceDigests.Files = append([]ReferenceDigestFile(nil), bundle.ReferenceDigests.Files...)
	digestDrift.ReferenceDigests.Files[0].SHA256 = strings.Repeat("0", 63)
	problems := validateContractBundle(&digestDrift)
	if !containsProblem(problems, "invalid reference digest entry") {
		t.Fatalf("invalid digest manifest was not detected: %v", problems)
	}

	missingFixture := *bundle
	missingFixture.Fixtures = map[string]FixtureDefinition{}
	for key, value := range bundle.Fixtures {
		missingFixture.Fixtures[key] = value
	}
	delete(missingFixture.Fixtures, bundle.Endpoints.Endpoints[0].PositiveFixture)
	problems = validateContractBundle(&missingFixture)
	if !containsProblem(problems, "references missing fixture") {
		t.Fatalf("missing fixture was not detected: %v", problems)
	}

	missingRequest := *bundle
	missingRequest.Fixtures = map[string]FixtureDefinition{}
	for key, value := range bundle.Fixtures {
		missingRequest.Fixtures[key] = value
	}
	fixtureID := bundle.Endpoints.Endpoints[0].PositiveFixture
	fixture := missingRequest.Fixtures[fixtureID]
	fixture.Request.Data = nil
	missingRequest.Fixtures[fixtureID] = fixture
	problems = validateContractBundle(&missingRequest)
	if !containsProblem(problems, "missing request.data") {
		t.Fatalf("missing fixture request data was not detected: %v", problems)
	}

	badSampleMeta := *bundle
	badSampleMeta.Fixtures = map[string]FixtureDefinition{}
	for key, value := range bundle.Fixtures {
		badSampleMeta.Fixtures[key] = value
	}
	fixture = badSampleMeta.Fixtures[fixtureID]
	fixture.SourceSampleID = "sample-without-digest"
	badSampleMeta.Fixtures[fixtureID] = fixture
	problems = validateContractBundle(&badSampleMeta)
	if !containsProblem(problems, "invalid sample_digest") {
		t.Fatalf("bad sample metadata was not detected: %v", problems)
	}
}

func TestReportCommandLoadsExistingReport(t *testing.T) {
	reportDir := filepath.Join(t.TempDir(), "scenario-report")
	if report, err := runScenarioValidation(reportDir); err != nil {
		t.Fatalf("scenario validation failed: %v report=%+v", err, report)
	}
	jsonOut := filepath.Join(t.TempDir(), "report.json")
	if err := run([]string{"report", "--report-dir", reportDir, "--format", "json", "--output", jsonOut}); err != nil {
		t.Fatalf("report json failed: %v", err)
	}
	content, err := os.ReadFile(jsonOut)
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(string(content), "not_loaded") {
		t.Fatalf("report command returned placeholder content: %s", content)
	}
	var rendered map[string]any
	if err := json.Unmarshal(content, &rendered); err != nil {
		t.Fatalf("decode rendered report: %v", err)
	}
	if rendered["ok"] != true {
		t.Fatalf("rendered report ok = %v", rendered["ok"])
	}
	summary := rendered["summary"].(map[string]any)
	if got := stringValue(summary["version"]); got != appVersion {
		t.Fatalf("rendered version = %s, want %s", got, appVersion)
	}
	scenarioResults := rendered["scenario_results"].(map[string]any)
	if got := stringValue(scenarioResults["fixture_runner_version"]); got != fixtureRunnerVersion {
		t.Fatalf("fixture runner version = %s, want %s", got, fixtureRunnerVersion)
	}
	businessCoverage := rendered["business_scenario_coverage"].(map[string]any)
	if got := len(businessCoverage["scenarios"].([]any)); got != 25 {
		t.Fatalf("business scenario coverage count = %d, want 25", got)
	}
	sampleCoverage := rendered["sample_coverage"].(map[string]any)
	if got := stringValue(sampleCoverage["status"]); got != "sample_backed" {
		t.Fatalf("sample coverage status = %s, want sample_backed", got)
	}
	if got := len(sampleCoverage["sample_backed_fixtures"].([]any)); got != 19 {
		t.Fatalf("sample backed fixture count = %d, want 19", got)
	}
	coverageLevels := sampleCoverage["counts_by_level"].(map[string]any)
	if got := coverageLevels["deidentified_production_sample"]; got != float64(18) {
		t.Fatalf("production sample count = %v, want 18", got)
	}
	if got := coverageLevels["deidentified_joint_debug_sample"]; got != float64(1) {
		t.Fatalf("joint debug sample count = %v, want 1", got)
	}
	sampleImportReport := rendered["sample_import_report"].(map[string]any)
	if got := stringValue(sampleImportReport["status"]); got != "partial" {
		t.Fatalf("sample import status = %s, want partial", got)
	}
	if got := sampleImportReport["imported_sample_backed_fixtures"]; got != float64(19) {
		t.Fatalf("imported sample backed fixtures = %v, want 19", got)
	}
	if got := sampleImportReport["requires_production_sample_count"]; got != float64(12) {
		t.Fatalf("requires production sample count = %v, want 12", got)
	}
	scopeBoundaries := rendered["sandbox_scope_boundaries"].(map[string]any)
	if got := len(scopeBoundaries["boundaries"].([]any)); got == 0 {
		t.Fatalf("sandbox scope boundaries were not rendered")
	}
	for _, format := range []string{"md", "html"} {
		out := filepath.Join(t.TempDir(), "report."+format)
		if err := run([]string{"report", "--report-dir", reportDir, "--format", format, "--output", out}); err != nil {
			t.Fatalf("report %s failed: %v", format, err)
		}
		if info, err := os.Stat(out); err != nil || info.Size() == 0 {
			t.Fatalf("report %s output invalid: info=%v err=%v", format, info, err)
		}
	}
}

// TestConcurrentAggregationQueryNoDataRace 验证并发同键查询不会触发数据竞争。
// 配合 `go test -race` 使用，回归 P1：handleAggregationQuery 曾在 Unlock 后解引用 *payment。
func TestConcurrentAggregationQueryNoDataRace(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	create := postGateway(t, app, handler, "/v4/trade/payment/create", map[string]any{
		"req_seq_id": "REQ-RACE-AGG",
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  "1.00",
		"goods_desc": "race",
	})
	assertDataCode(t, app, create, "00000100")
	hfSeqID := stringValue(create.Data["hf_seq_id"])
	queryData := map[string]any{"huifu_id": "6666000100000001", "hf_seq_id": hfSeqID}
	var wg sync.WaitGroup
	for i := 0; i < 8; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", queryData)
		}()
	}
	wg.Wait()
}

// TestConcurrentHostingQueryNoDataRace 验证并发托管查单不会触发数据竞争。
func TestConcurrentHostingQueryNoDataRace(t *testing.T) {
	app := newTestApp(t)
	handler := app.gatewayHandler()
	control := app.controlHandler()
	payment := createHostingPayment(t, app, handler, "REQ-RACE-HOST", "1.00")
	var wg sync.WaitGroup
	for i := 0; i < 8; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", hostingQueryByOriginal(payment, "QRY-RACE-HOST"))
		}()
	}
	wg.Wait()
	_ = control
}

func TestPurgeRunsSafely(t *testing.T) {
	dataDir := filepath.Join(t.TempDir(), "data")
	runsDir := filepath.Join(dataDir, "runs")
	oldRun := filepath.Join(runsDir, "old-run")
	newRun := filepath.Join(runsDir, "new-run")
	if err := os.MkdirAll(oldRun, 0o700); err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll(newRun, 0o700); err != nil {
		t.Fatal(err)
	}
	oldTime := time.Now().Add(-48 * time.Hour)
	if err := os.Chtimes(oldRun, oldTime, oldTime); err != nil {
		t.Fatal(err)
	}
	result, err := purgeRuns(dataDir, "", "24h", true)
	if err != nil {
		t.Fatalf("dry-run purge failed: %v", err)
	}
	if result.Matched != 1 || result.Deleted != 0 || !fileExists(oldRun) {
		t.Fatalf("unexpected dry-run result=%+v oldExists=%t", result, fileExists(oldRun))
	}
	result, err = purgeRuns(dataDir, "", "24h", false)
	if err != nil {
		t.Fatalf("older-than purge failed: %v", err)
	}
	if result.Deleted != 1 || fileExists(oldRun) || !fileExists(newRun) {
		t.Fatalf("unexpected purge result=%+v oldExists=%t newExists=%t", result, fileExists(oldRun), fileExists(newRun))
	}
	if _, err := purgeRuns(dataDir, "..\\escape", "", false); err == nil {
		t.Fatal("purge accepted path traversal run-id")
	}
	if _, err := purgeRuns(dataDir, "new-run", "not-a-duration", true); err == nil {
		t.Fatal("purge accepted invalid older-than")
	}
}

func TestReportRedactsSecretsBeforeWriting(t *testing.T) {
	app := newTestApp(t)
	app.payments["REQ-SECRET"] = &Payment{
		Kind:          "aggregation",
		HuifuID:       "6666000100000001",
		ReqDate:       "20260624",
		ReqSeqID:      "REQ-SECRET",
		NotifyURL:     "http://127.0.0.1/notify?secret=report-leak",
		RequestDigest: "sha256:test",
		State:         "P",
	}
	app.notifications = append(app.notifications, NotificationDelivery{
		ID:              "ND-SECRET",
		PaymentReqSeqID: "REQ-SECRET",
		Target:          "http://127.0.0.1/notify?token=report-leak",
		TargetRedacted:  "http://127.0.0.1/notify?REDACTED",
		Status:          "blocked",
		ExpectedACK:     expectedNotifyACK("REQ-SECRET"),
		AckBody:         "-----BEGIN PRIVATE KEY-----\nMII-report-leak\n-----END PRIVATE KEY-----",
		Error:           `Post "http://127.0.0.1/notify?token=report-leak": connection refused`,
		Attempts: []NotificationAttempt{{
			Attempt: 1,
			Status:  "network_error",
			AckBody: "Authorization: Bearer report-leak",
			Error:   `Post "http://127.0.0.1/notify?token=report-leak": connection refused`,
		}},
	})
	app.webhooks = append(app.webhooks, WebhookDelivery{
		ID:             "WD-SECRET",
		EventType:      webhookEventPayment,
		EntityID:       "REQ-SECRET",
		Target:         "http://127.0.0.1/webhook?token=report-leak",
		TargetRedacted: "http://127.0.0.1/webhook?REDACTED",
		Status:         "blocked",
		Sign:           "full-sign-report-leak",
		Error:          `Post "http://127.0.0.1/webhook?token=report-leak&sign=full-sign-report-leak": connection refused`,
		Attempts: []WebhookAttempt{{
			Attempt: 1,
			Status:  "network_error",
			AckBody: "-----BEGIN CERTIFICATE-----\nMIIC-report-leak\n-----END CERTIFICATE-----\ntoken: report-leak",
			Error:   `Post "http://127.0.0.1/webhook?token=report-leak&sign=full-sign-report-leak": connection refused`,
		}},
	})
	app.requestLogs = append(app.requestLogs, RequestLog{
		ID:         "REQLOG-SECRET",
		Time:       time.Now().UTC().Format(time.RFC3339Nano),
		Method:     http.MethodPost,
		Path:       "/v4/trade/payment/create",
		HTTPStatus: http.StatusOK,
		RequestData: map[string]any{
			"notify_url": "http://127.0.0.1/notify?secret=report-leak",
			"message":    "Authorization: Bearer report-leak",
		},
		ResponseBody: "token=report-leak",
	})
	app.record("report.secret_event", "/notify?token=report-leak", "token=report-leak", map[string]any{
		"target": "http://127.0.0.1/webhook?token=report-leak",
		"sign":   "full-sign-report-leak",
	})
	if err := app.WriteReport(); err != nil {
		t.Fatal(err)
	}
	for _, name := range []string{"events.ndjson", "final-state.json", "notify-attempts.json", "webhook-attempts.json", "request-logs.json", "security-findings.json", "secret-scan.json"} {
		content, err := os.ReadFile(filepath.Join(app.reportDir, name))
		if err != nil {
			t.Fatal(err)
		}
		if strings.Contains(string(content), "report-leak") {
			t.Fatalf("%s contains an unredacted secret: %s", name, content)
		}
		for _, marker := range []string{"BEGIN PRIVATE KEY", "BEGIN CERTIFICATE", "Authorization:", "Bearer "} {
			if strings.Contains(string(content), marker) {
				t.Fatalf("%s contains unredacted credential marker %q: %s", name, marker, content)
			}
		}
	}
}

func captureStdout(t *testing.T, fn func() error) (string, error) {
	t.Helper()
	previous := os.Stdout
	reader, writer, err := os.Pipe()
	if err != nil {
		t.Fatal(err)
	}
	os.Stdout = writer
	runErr := fn()
	if err := writer.Close(); err != nil && runErr == nil {
		runErr = err
	}
	os.Stdout = previous
	content, err := io.ReadAll(reader)
	if err != nil {
		t.Fatal(err)
	}
	if err := reader.Close(); err != nil {
		t.Fatal(err)
	}
	return string(content), runErr
}

func assertReplayPrintJSONRedacted(t *testing.T, output string, forbidden ...string) {
	t.Helper()
	var decoded map[string]any
	if err := json.Unmarshal([]byte(output), &decoded); err != nil {
		t.Fatalf("invalid replay json %q: %v", output, err)
	}
	for _, value := range forbidden {
		if value != "" && strings.Contains(output, value) {
			t.Fatalf("replay json leaked %q: %s", value, output)
		}
	}
	for _, rawField := range []string{`"target":`, `"sign":`} {
		if strings.Contains(output, rawField) {
			t.Fatalf("replay json contains raw field %s: %s", rawField, output)
		}
	}
	if !strings.Contains(output, "target_redacted") {
		t.Fatalf("replay json missing target_redacted: %s", output)
	}
}

func TestAdvisoryScanFindsRiskPatterns(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "client.go")
	content := []byte("package demo\nvar token = \"super-secret-token\"\nvar _ = tls.Config{InsecureSkipVerify: true}\n")
	if err := os.WriteFile(path, content, 0o600); err != nil {
		t.Fatal(err)
	}
	findings, err := scanCodeAdvisories(dir)
	if err != nil {
		t.Fatal(err)
	}
	if len(findings) < 2 {
		t.Fatalf("findings = %+v, want at least 2", findings)
	}
}

func TestReplayTargetSafety(t *testing.T) {
	if err := validateReplayTarget("http://127.0.0.1:8080/api/notify"); err != nil {
		t.Fatalf("loopback target rejected: %v", err)
	}
	if err := validateReplayTarget("http://example.com/api/notify"); err == nil {
		t.Fatal("external target accepted without allowlist")
	}
	if err := validateReplayTarget("http://169.254.169.254/latest/meta-data"); err == nil {
		t.Fatal("metadata target accepted")
	}
}

func TestReplayDeliversToLoopbackAndWritesReport(t *testing.T) {
	reportDir := filepath.Join(t.TempDir(), "report")
	received := 0
	receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		received++
		if err := r.ParseForm(); err != nil {
			t.Errorf("parse form: %v", err)
		}
		var respData map[string]any
		if err := json.Unmarshal([]byte(r.Form.Get("resp_data")), &respData); err != nil {
			t.Errorf("decode resp_data: %v", err)
		}
		_, _ = w.Write([]byte(expectedNotifyACK(stringValue(respData["req_seq_id"]))))
	}))
	defer receiver.Close()

	notifyOutput, err := captureStdout(t, func() error {
		return run([]string{"replay", "--target", receiver.URL + "/notify?token=replay-leak", "--retry-ms", "0", "--report-dir", reportDir, "--print-json"})
	})
	if err != nil {
		t.Fatalf("replay failed: %v", err)
	}
	assertReplayPrintJSONRedacted(t, notifyOutput, "replay-leak")
	if received != 1 {
		t.Fatalf("received replay count = %d, want 1", received)
	}
	for _, name := range []string{"summary.json", "events.ndjson", "notify-attempts.json", "security-findings.json", "secret-scan.json"} {
		if _, err := os.Stat(filepath.Join(reportDir, name)); err != nil {
			t.Fatalf("missing replay report file %s: %v", name, err)
		}
	}
	if err := run([]string{"replay", "--target", "http://example.com/notify", "--report-dir", filepath.Join(t.TempDir(), "blocked")}); err == nil {
		t.Fatal("external replay target accepted without allowlist")
	}

	failedNotifyReportDir := filepath.Join(t.TempDir(), "failed-notify-report")
	failedNotifyOutput, err := captureStdout(t, func() error {
		return run([]string{
			"replay",
			"--target", "http://127.0.0.1:1/notify?token=replay-leak",
			"--retry-ms", "0",
			"--attempts", "1",
			"--report-dir", failedNotifyReportDir,
			"--print-json",
		})
	})
	if err == nil {
		t.Fatal("failed notify replay unexpectedly succeeded")
	}
	assertReplayPrintJSONRedacted(t, failedNotifyOutput, "replay-leak")
	failedNotifyReport, err := os.ReadFile(filepath.Join(failedNotifyReportDir, "notify-attempts.json"))
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(string(failedNotifyReport), "replay-leak") || strings.Contains(string(failedNotifyReport), "token=") {
		t.Fatalf("failed notify report leaked target query: %s", failedNotifyReport)
	}

	webhookReportDir := filepath.Join(t.TempDir(), "webhook-report")
	webhookKey := "abcdefghijklmnopqrstuvwx12345678"
	webhookReceived := 0
	webhookSign := ""
	webhookReceiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		webhookReceived++
		raw, err := io.ReadAll(r.Body)
		if err != nil {
			t.Errorf("read webhook body: %v", err)
		}
		if got, want := r.URL.Query().Get("sign"), webhookSignature(raw, webhookKey); got != want {
			t.Errorf("webhook replay sign = %s, want %s", got, want)
		} else {
			webhookSign = got
		}
		w.WriteHeader(http.StatusAccepted)
	}))
	defer webhookReceiver.Close()
	webhookOutput, err := captureStdout(t, func() error {
		return run([]string{
			"replay",
			"--kind", "webhook",
			"--target", webhookReceiver.URL + "/webhook?token=replay-leak",
			"--webhook-endpoint-key", webhookKey,
			"--retry-ms", "0",
			"--report-dir", webhookReportDir,
			"--print-json",
		})
	})
	if err != nil {
		t.Fatalf("webhook replay failed: %v", err)
	}
	assertReplayPrintJSONRedacted(t, webhookOutput, "replay-leak", webhookSign)
	if !strings.Contains(webhookOutput, "sign_sha256") {
		t.Fatalf("webhook replay json missing sign_sha256: %s", webhookOutput)
	}
	if webhookReceived != 1 {
		t.Fatalf("received webhook replay count = %d, want 1", webhookReceived)
	}
	if _, err := os.Stat(filepath.Join(webhookReportDir, "webhook-attempts.json")); err != nil {
		t.Fatalf("missing webhook replay report: %v", err)
	}
	if err := run([]string{"replay", "--kind", "webhook", "--target", "http://example.com/webhook", "--report-dir", filepath.Join(t.TempDir(), "blocked-webhook")}); err == nil {
		t.Fatal("external webhook replay target accepted without allowlist")
	}

	failedWebhookReportDir := filepath.Join(t.TempDir(), "failed-webhook-report")
	failedWebhookOutput, err := captureStdout(t, func() error {
		return run([]string{
			"replay",
			"--kind", "webhook",
			"--target", "http://127.0.0.1:1/webhook?token=replay-leak",
			"--webhook-endpoint-key", webhookKey,
			"--retry-ms", "0",
			"--attempts", "1",
			"--report-dir", failedWebhookReportDir,
			"--print-json",
		})
	})
	if err == nil {
		t.Fatal("failed webhook replay unexpectedly succeeded")
	}
	assertReplayPrintJSONRedacted(t, failedWebhookOutput, "replay-leak")
	failedWebhookReport, err := os.ReadFile(filepath.Join(failedWebhookReportDir, "webhook-attempts.json"))
	if err != nil {
		t.Fatal(err)
	}
	for _, leaked := range []string{"replay-leak", "token=", "sign="} {
		if strings.Contains(string(failedWebhookReport), leaked) {
			t.Fatalf("failed webhook report leaked %q: %s", leaked, failedWebhookReport)
		}
	}
}

func createPaidAggregationPayment(t *testing.T, app *App, handler http.Handler, reqSeqID, amount string) Payment {
	t.Helper()
	create := postGateway(t, app, handler, "/v4/trade/payment/create", map[string]any{
		"req_seq_id": reqSeqID,
		"req_date":   "20260624",
		"huifu_id":   "6666000100000001",
		"trade_type": "A_NATIVE",
		"trans_amt":  amount,
		"goods_desc": "paid aggregation",
	})
	assertDataCode(t, app, create, "00000100")
	hfSeqID := stringValue(create.Data["hf_seq_id"])
	postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", map[string]any{
		"huifu_id":  "6666000100000001",
		"hf_seq_id": hfSeqID,
	})
	postGateway(t, app, handler, "/v4/trade/payment/scanpay/query", map[string]any{
		"huifu_id":  "6666000100000001",
		"hf_seq_id": hfSeqID,
	})
	app.mu.Lock()
	defer app.mu.Unlock()
	return *app.payments[reqSeqID]
}

func postAdminJSON(t *testing.T, app *App, handler http.Handler, path string, payload map[string]any) (int, map[string]any) {
	t.Helper()
	raw, _ := json.Marshal(payload)
	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1"+path, bytes.NewReader(raw))
	req.Header.Set("Authorization", "Bearer "+app.adminToken)
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	var body map[string]any
	if rec.Body.Len() > 0 {
		if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
			t.Fatalf("decode admin response: %v body=%s", err, rec.Body.String())
		}
	}
	return rec.Code, body
}

func createHostingPayment(t *testing.T, app *App, handler http.Handler, reqSeqID, amount string) Payment {
	t.Helper()
	hostingData := map[string]any{"project_title": "Sandbox Project", "project_id": "P123", "request_type": "P"}
	hostingRaw, _ := json.Marshal(hostingData)
	preorderResp := postGateway(t, app, handler, "/v2/trade/hosting/payment/preorder", map[string]any{
		"req_seq_id":     reqSeqID,
		"req_date":       "20260624",
		"huifu_id":       "6666000100000001",
		"trans_amt":      amount,
		"goods_desc":     "hosting operations",
		"pre_order_type": "1",
		"trans_type":     "A_NATIVE",
		"hosting_data":   string(hostingRaw),
	})
	assertDataCode(t, app, preorderResp, "00000000")
	app.mu.Lock()
	defer app.mu.Unlock()
	return *app.payments[reqSeqID]
}

func hostingQueryByOriginal(payment Payment, reqSeqID string) map[string]any {
	return map[string]any{
		"req_date":       payment.ReqDate,
		"req_seq_id":     reqSeqID,
		"huifu_id":       payment.HuifuID,
		"org_req_date":   payment.ReqDate,
		"org_req_seq_id": payment.ReqSeqID,
	}
}

func hostingQueryByParty(payment Payment, reqSeqID, partyOrderID string) map[string]any {
	data := hostingQueryByOriginal(payment, reqSeqID)
	delete(data, "huifu_id")
	delete(data, "org_req_date")
	delete(data, "org_req_seq_id")
	data["party_order_id"] = partyOrderID
	return data
}

func createPaidHostingPayment(t *testing.T, app *App, handler http.Handler, control http.Handler, reqSeqID, amount string) Payment {
	t.Helper()
	payment := createHostingPayment(t, app, handler, reqSeqID, amount)
	getControlJSON(t, control, "/__merchant/hosting/callback?pre_order_id="+payment.PreOrderID)
	postControlJSON(t, app, control, "/__merchant/hosting/confirm", map[string]any{"pre_order_id": payment.PreOrderID})
	postGateway(t, app, handler, "/v2/trade/hosting/payment/queryorderinfo", hostingQueryByOriginal(payment, "QRY-"+reqSeqID))
	app.mu.Lock()
	defer app.mu.Unlock()
	return *app.payments[reqSeqID]
}

func newTestApp(t *testing.T) *App {
	t.Helper()
	dir := t.TempDir()
	app, err := NewApp(filepath.Join(dir, "data"), filepath.Join(dir, "report"), true)
	if err != nil {
		t.Fatal(err)
	}
	return app
}

func newTestAppWithOptions(t *testing.T, options AppOptions) *App {
	t.Helper()
	dir := t.TempDir()
	if options.DataDir == "" {
		options.DataDir = filepath.Join(dir, "data")
	}
	if options.ReportDir == "" {
		options.ReportDir = filepath.Join(dir, "report")
	}
	options.Ephemeral = true
	app, err := NewAppWithOptions(options)
	if err != nil {
		t.Fatal(err)
	}
	return app
}

func postGateway(t *testing.T, app *App, handler http.Handler, path string, data map[string]any) SignedResponse {
	t.Helper()
	status, body := postGatewayRaw(t, app, handler, path, data, nil)
	if status != http.StatusOK {
		t.Fatalf("%s status = %d body=%s", path, status, body)
	}
	var resp SignedResponse
	if err := json.Unmarshal(body, &resp); err != nil {
		t.Fatalf("decode response: %v body=%s", err, string(body))
	}
	if err := verifyData(resp.Data, resp.Sign, app.creds.GatewayPublic); err != nil {
		t.Fatalf("response signature invalid: %v", err)
	}
	return resp
}

func postGatewayRaw(t *testing.T, app *App, handler http.Handler, path string, data map[string]any, headers map[string]string) (int, []byte) {
	t.Helper()
	signature, err := signData(data, app.creds.MerchantPrivate)
	if err != nil {
		t.Fatal(err)
	}
	body, _ := json.Marshal(Envelope{
		SysID:     firstNonEmpty(app.creds.SysID, "SYS"),
		ProductID: firstNonEmpty(app.creds.ProductID, "MYPAY"),
		Sign:      signature,
		Data:      data,
	})
	req := httptest.NewRequest(http.MethodPost, path, bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json;charset=UTF-8")
	req.Header.Set("jpt-x-skill-source", sandboxSkillSource)
	if huifuID := stringValue(data["huifu_id"]); huifuID != "" {
		req.Header.Set("jpt-x-skill-huifu_id", huifuID)
	}
	for key, value := range headers {
		req.Header.Set(key, value)
	}
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	return rec.Code, rec.Body.Bytes()
}

func getControlJSON(t *testing.T, handler http.Handler, path string) map[string]any {
	t.Helper()
	req := httptest.NewRequest(http.MethodGet, "http://127.0.0.1"+path, nil)
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("%s status = %d body=%s", path, rec.Code, rec.Body.String())
	}
	var resp map[string]any
	if err := json.Unmarshal(rec.Body.Bytes(), &resp); err != nil {
		t.Fatalf("decode control response: %v body=%s", err, rec.Body.String())
	}
	return resp
}

func postControlJSON(t *testing.T, app *App, handler http.Handler, path string, data map[string]any) map[string]any {
	t.Helper()
	body, _ := json.Marshal(data)
	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1"+path, bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Huifu-Sandbox-CSRF", app.csrfToken)
	rec := httptest.NewRecorder()
	handler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("%s status = %d body=%s", path, rec.Code, rec.Body.String())
	}
	var resp map[string]any
	if err := json.Unmarshal(rec.Body.Bytes(), &resp); err != nil {
		t.Fatalf("decode control response: %v body=%s", err, rec.Body.String())
	}
	return resp
}

func assertDataCode(t *testing.T, app *App, resp SignedResponse, want string) {
	t.Helper()
	if err := verifyData(resp.Data, resp.Sign, app.creds.GatewayPublic); err != nil {
		t.Fatalf("response signature invalid: %v", err)
	}
	if got := stringValue(resp.Data["resp_code"]); got != want {
		t.Fatalf("resp_code = %s, want %s; data=%+v", got, want, resp.Data)
	}
}

func assertNoTopLevelRespCode(t *testing.T, resp SignedResponse) {
	t.Helper()
	raw, err := json.Marshal(resp)
	if err != nil {
		t.Fatal(err)
	}
	var top map[string]any
	if err := json.Unmarshal(raw, &top); err != nil {
		t.Fatal(err)
	}
	if _, ok := top["resp_code"]; ok {
		t.Fatal("resp_code appeared at top level")
	}
	if _, ok := top["data"]; !ok {
		t.Fatal("data missing at top level")
	}
	if _, ok := top["sign"]; !ok {
		t.Fatal("sign missing at top level")
	}
}

func readExpectedReferences(t *testing.T) []string {
	t.Helper()
	b, err := os.ReadFile(filepath.Join("..", "scripts", "skill_validation_config.py"))
	if err != nil {
		t.Fatal(err)
	}
	text := string(b)
	start := strings.Index(text, "EXPECTED_REFERENCES = {")
	if start < 0 {
		t.Fatal("EXPECTED_REFERENCES not found")
	}
	end := strings.Index(text[start:], "}\nALLOWED_TOP_LEVEL_KEYS")
	if end < 0 {
		t.Fatal("EXPECTED_REFERENCES end not found")
	}
	block := text[start : start+end]
	re := regexp.MustCompile(`"([^"]+\.md)"`)
	matches := re.FindAllStringSubmatch(block, -1)
	var out []string
	for _, match := range matches {
		out = append(out, match[1])
	}
	if len(out) == 0 {
		t.Fatal("no references parsed")
	}
	return out
}

func containsProblem(problems []string, want string) bool {
	for _, problem := range problems {
		if strings.Contains(problem, want) {
			return true
		}
	}
	return false
}
