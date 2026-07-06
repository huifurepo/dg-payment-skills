package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"
)

type ScenarioValidationReport struct {
	OK                    bool              `json:"ok"`
	CoverageRunnerVersion string            `json:"coverage_runner_version"`
	FixtureRunnerVersion  string            `json:"fixture_runner_version"`
	ReportDir             string            `json:"report_dir"`
	ScenarioCount         int               `json:"scenario_count"`
	Passed                int               `json:"passed"`
	Failed                int               `json:"failed"`
	EndpointSummary       map[string]string `json:"endpoint_summary"`
	FixtureSummary        map[string]string `json:"fixture_summary"`
	Scenarios             []ScenarioResult  `json:"scenarios"`
	Fixtures              []FixtureResult   `json:"fixtures"`
}

type scenarioRunner struct {
	app           *App
	gateway       http.Handler
	control       http.Handler
	controlServer *localScenarioServer
	notifyServer  *localScenarioServer
	webhookServer *localScenarioServer
	requests      int
	fixtures      map[string]FixtureResult
}

type localScenarioServer struct {
	URL    string
	server *http.Server
	ln     net.Listener
}

func newLocalScenarioServer(handler http.Handler) (*localScenarioServer, error) {
	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		return nil, err
	}
	server := &http.Server{Handler: handler, ReadHeaderTimeout: 5 * time.Second}
	out := &localScenarioServer{URL: "http://" + ln.Addr().String(), server: server, ln: ln}
	go func() {
		if err := server.Serve(ln); err != nil && !errors.Is(err, http.ErrServerClosed) {
			fmt.Fprintf(os.Stderr, "local scenario server error: %v\n", err)
		}
	}()
	return out, nil
}

func (s *localScenarioServer) Close() {
	if s == nil || s.server == nil {
		return
	}
	_ = s.server.Close()
}

type localResponseRecorder struct {
	Code   int
	header http.Header
	Body   *bytes.Buffer
	wrote  bool
}

func newLocalResponseRecorder() *localResponseRecorder {
	return &localResponseRecorder{Code: http.StatusOK, header: http.Header{}, Body: &bytes.Buffer{}}
}

func (r *localResponseRecorder) Header() http.Header {
	return r.header
}

func (r *localResponseRecorder) WriteHeader(code int) {
	if r.wrote {
		return
	}
	r.Code = code
	r.wrote = true
}

func (r *localResponseRecorder) Write(p []byte) (int, error) {
	if !r.wrote {
		r.WriteHeader(http.StatusOK)
	}
	return r.Body.Write(p)
}

func newLocalRequest(method, target string, body io.Reader) (*http.Request, error) {
	req, err := http.NewRequest(method, target, body)
	if err != nil {
		return nil, err
	}
	req.RemoteAddr = "127.0.0.1:1"
	return req, nil
}

func runScenarioValidation(reportDir string) (*ScenarioValidationReport, error) {
	app, err := NewApp("", reportDir, true)
	if err != nil {
		return nil, err
	}
	app.notifyRetryDelay = 0
	app.faultTimeoutDelay = 0
	r := &scenarioRunner{app: app, gateway: app.gatewayHandler(), control: app.controlHandler(), fixtures: map[string]FixtureResult{}}
	r.controlServer, err = newLocalScenarioServer(app.controlHandler())
	if err != nil {
		return nil, err
	}
	defer r.controlServer.Close()
	app.controlBaseURL = r.controlServer.URL
	r.notifyServer, err = newLocalScenarioServer(http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) {
		_ = req.ParseForm()
		var data map[string]any
		_ = json.Unmarshal([]byte(req.Form.Get("resp_data")), &data)
		_, _ = w.Write([]byte(expectedNotifyACK(stringValue(data["req_seq_id"]))))
	}))
	if err != nil {
		return nil, err
	}
	defer r.notifyServer.Close()
	r.webhookServer, err = newLocalScenarioServer(http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) {
		raw, _ := io.ReadAll(req.Body)
		if got, want := req.URL.Query().Get("sign"), webhookSignature(raw, app.webhookEndpointKeySnapshot()); got != want {
			http.Error(w, "bad webhook sign", http.StatusBadRequest)
			return
		}
		w.WriteHeader(http.StatusNoContent)
	}))
	if err != nil {
		return nil, err
	}
	defer r.webhookServer.Close()
	if err := app.addWebhookTarget(r.webhookServer.URL + "/webhook?case=scenario"); err != nil {
		return nil, err
	}

	var results []ScenarioResult
	for _, scenario := range app.bundle.Scenarios.Scenarios {
		startRequests := r.requests
		startEvents := r.eventCount()
		err := r.runScenario(scenario.ID)
		result := r.resultForScenario(scenario.ID, startRequests, startEvents, err)
		results = append(results, result)
	}
	fixtures := r.fixtureResults()
	app.mu.Lock()
	app.scenarioResults = append([]ScenarioResult(nil), results...)
	app.fixtureResults = append([]FixtureResult(nil), fixtures...)
	app.mu.Unlock()
	if err := app.WriteReport(); err != nil {
		return nil, err
	}
	if err := r.assertReportFiles(results); err != nil {
		results = append(results, ScenarioResult{ID: "REPORT-01", Status: "failed", Error: err.Error()})
		app.mu.Lock()
		app.scenarioResults = append([]ScenarioResult(nil), results...)
		app.mu.Unlock()
		_ = app.WriteReport()
	}
	report := scenarioValidationReport(app, reportDir)
	if !report.OK {
		return report, phaseError("scenario validation failed")
	}
	return report, nil
}

func (r *scenarioRunner) runScenario(id string) error {
	switch id {
	case "AGG-01":
		return r.scenarioAggregationHappyPath(id)
	case "AGG-02":
		return r.scenarioAggregationMissingRequired(id)
	case "AGG-03":
		return r.scenarioAggregationQueryProcessingAndNegative(id)
	case "HOST-01":
		return r.scenarioHostingConfirm(id, "S10-HOST-01")
	case "HOST-02":
		return r.scenarioHostingNegatives(id)
	case "NOTIFY-01":
		return r.scenarioNotifySuccess(id)
	case "NOTIFY-02":
		return r.scenarioNotifyBadAck(id)
	case "NOTIFY-03":
		return r.scenarioNotifyDuplicate(id)
	case "NOTIFY-04":
		return r.scenarioNotifyBlocked(id)
	case "FAULT-01":
		return r.scenarioFaults(id)
	case "SEC-01":
		return r.scenarioControlSecurity(id)
	case "SEC-02":
		return r.scenarioIdempotencyConflicts(id)
	case "SEC-03":
		return r.scenarioReportRedaction(id)
	case "SCAN-01":
		return r.scenarioAdvisoryScan(id)
	case "REFUND-01":
		return r.scenarioAggregationRefund(id)
	case "REFUND-02":
		return r.scenarioRefundOverAmount(id)
	case "REFUND-03":
		return r.scenarioHostingRefund(id)
	case "CLOSE-01":
		return r.scenarioAggregationClose(id)
	case "CLOSE-02":
		return r.scenarioHostingClose(id)
	case "SPLITPAY-01":
		return r.scenarioSplitpay(id)
	case "WEBHOOK-01", "WEBHOOK-02", "WEBHOOK-03":
		return r.scenarioWebhookEvidence(id)
	case "RECON-01":
		return r.scenarioReconciliation(id)
	case "RECON-02":
		return r.scenarioReconciliationNegative(id)
	case "AGG-CHANNEL-WX-01":
		return r.scenarioAggregationChannel(id, "agg-channel-wx-create", "agg-channel-wx-query", "agg-channel-wx-micropay", "agg-channel-wx-micropay-missing-auth")
	case "AGG-CHANNEL-ALI-01":
		return r.scenarioAggregationChannel(id, "agg-channel-ali-create", "agg-channel-ali-query", "agg-channel-ali-micropay", "agg-channel-ali-micropay-missing-auth")
	case "AGG-CHANNEL-UP-01":
		return r.scenarioAggregationChannel(id, "agg-channel-up-create", "agg-channel-up-query", "agg-channel-up-micropay", "agg-channel-up-micropay-missing-auth")
	case "AGG-TX-META-01":
		return r.scenarioAggregationTxMetadata(id)
	case "HOST-H5-WX-01":
		return r.scenarioHostingVariant(id, "hosting-h5-wx-preorder", "hosting-h5-wx-query", "hosting-h5-wx-invalid-json", "wx_response")
	case "HOST-H5-ALI-01":
		return r.scenarioHostingVariant(id, "hosting-h5-ali-preorder", "hosting-h5-ali-query", "hosting-h5-ali-invalid-json", "alipay_response")
	case "HOST-H5-UP-01":
		return r.scenarioHostingVariant(id, "hosting-h5-up-preorder", "hosting-h5-up-query", "hosting-h5-up-invalid-json", "unionpay_response")
	case "HOST-H5-DY-01":
		return r.scenarioHostingVariant(id, "hosting-h5-dy-preorder", "hosting-h5-dy-query", "hosting-h5-dy-invalid-json", "dy_response")
	case "HOST-MINI-ALI-01":
		return r.scenarioHostingVariant(id, "hosting-mini-ali-preorder", "hosting-mini-ali-query", "hosting-mini-ali-missing-app-data", "alipay_response")
	case "HOST-MINI-WX-01":
		return r.scenarioHostingVariant(id, "hosting-mini-wx-preorder", "hosting-mini-wx-query", "hosting-mini-wx-missing-miniapp-data", "miniapp_data")
	case "HOST-DY-DIRECT-01":
		return r.scenarioHostingVariant(id, "hosting-dy-direct-preorder", "hosting-dy-direct-query", "hosting-dy-direct-missing-dy-data", "dy_response")
	case "CHANNEL-NOTIFY-01":
		return r.scenarioChannelNotify(id)
	case "AGG-SPLIT-01":
		return r.scenarioAggregationMetadataVariant(id, "agg-split-create", "agg-split-query", "tx_metadata.acct_split_bunch")
	case "AGG-COMBINED-01":
		return r.scenarioAggregationMetadataVariant(id, "agg-combined-create", "agg-combined-query", "tx_metadata.combinedpay_data")
	case "AGG-FEE-ALLOWANCE-01":
		return r.scenarioAggregationMetadataVariant(id, "agg-fee-allowance-create", "agg-fee-allowance-query", "tx_metadata.trans_fee_allowance_info")
	case "AGG-REFUND-CHANNEL-01":
		return r.scenarioAggregationChannelRefund(id)
	case "AGG-CLOSE-CHANNEL-01":
		return r.scenarioAggregationChannelClose(id)
	case "HOST-LARGEAMT-01":
		return r.scenarioHostingVariant(id, "hosting-largeamt-preorder", "hosting-largeamt-query", "hosting-unsupported-pre-order-type", "largeamt_response")
	case "HOST-TERMINAL-01":
		return r.scenarioHostingVariant(id, "hosting-terminal-preorder", "hosting-terminal-query", "hosting-unsupported-pre-order-type", "terminal_device_response")
	case "HOST-CHANNEL-COMBO-01":
		return r.scenarioHostingCombo(id)
	case "HOST-REFUND-CHANNEL-01":
		return r.scenarioHostingChannelRefund(id)
	case "HOST-CLOSE-CHANNEL-01":
		return r.scenarioHostingChannelClose(id)
	case "RECON-BILL-TYPES-01":
		return r.scenarioReconciliationBillTypes(id)
	case "RECON-DOWNLOAD-EDGES-01":
		return r.scenarioReconciliationDownloadEdges(id)
	case "ERROR-FIELDS-01":
		return r.scenarioFieldErrors(id)
	default:
		return fmt.Errorf("unknown scenario %s", id)
	}
}

func (r *scenarioRunner) scenarioAggregationHappyPath(id string) error {
	resp, err := r.postGatewayFixture("agg-create-processing", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	hfSeqID := stringValue(resp.Data["hf_seq_id"])
	vars := map[string]string{"agg_hf_seq_id": hfSeqID}
	first, err := r.postGatewayFixture("agg-query-processing-then-success", id, vars, nil, nil, fixtureRunOptions{AssertFields: false})
	if err != nil {
		return err
	}
	if got := stringValue(first.Data["trans_stat"]); got != "P" {
		return fmt.Errorf("first aggregation query trans_stat=%s", got)
	}
	second, err := r.postGatewayFixture("agg-query-processing-then-success", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if got := stringValue(second.Data["trans_stat"]); got != "S" {
		return fmt.Errorf("second aggregation query trans_stat=%s", got)
	}
	return nil
}

func (r *scenarioRunner) scenarioAggregationMissingRequired(id string) error {
	resp, err := r.postGatewayFixture("agg-create-missing-goods-desc", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(resp, "LS000002"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioAggregationQueryProcessingAndNegative(id string) error {
	resp, err := r.postGatewayFixture("agg-create-processing", id, nil, map[string]any{"req_seq_id": "S11-AGG-03", "trans_amt": "0.01", "goods_desc": "scenario aggregation processing", "notify_url": ""}, nil, fixtureRunOptions{AssertFields: false})
	if err != nil {
		return err
	}
	hfSeqID := stringValue(resp.Data["hf_seq_id"])
	query, err := r.postGatewayFixture("agg-query-processing-then-success", id, map[string]string{"agg_hf_seq_id": hfSeqID}, nil, nil, fixtureRunOptions{AssertFields: false})
	if err != nil {
		return err
	}
	if got := stringValue(query.Data["trans_stat"]); got != "P" {
		return fmt.Errorf("aggregation query processing trans_stat=%s", got)
	}
	negative, err := r.postGatewayFixture("agg-query-missing-locator", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(negative, "LS000004"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioHostingConfirm(id, reqSeqID string) error {
	payment, err := r.createHosting(id, reqSeqID, "0.12", true)
	if err != nil {
		return err
	}
	if _, err := r.getControl("/__merchant/hosting/callback?pre_order_id=" + payment.PreOrderID); err != nil {
		return err
	}
	if _, err := r.postControl("/__merchant/hosting/confirm", map[string]any{"pre_order_id": payment.PreOrderID}); err != nil {
		return err
	}
	queryVars := map[string]string{"hosting_req_date": payment.ReqDate, "hosting_req_seq_id": payment.ReqSeqID, "hosting_pre_order_id": payment.PreOrderID}
	resp, err := r.postGatewayFixture("hosting-query-success", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if got := stringValue(resp.Data["trans_stat"]); got != "S" {
		return fmt.Errorf("hosting query trans_stat=%s", got)
	}
	return nil
}

func (r *scenarioRunner) scenarioHostingNegatives(id string) error {
	resp, err := r.postGatewayFixture("hosting-preorder-missing-project-id", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(resp, "LS000002"); err != nil {
		return err
	}
	query, err := r.postGatewayFixture("hosting-query-missing-locator", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(query, "LS000004"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioNotifySuccess(id string) error {
	payment := Payment{Kind: "aggregation", HuifuID: "6666000100000001", ReqDate: "20260624", ReqSeqID: "S10-NOTIFY-01", HFSeqID: "HF-S10-NOTIFY-01", TransAmt: "0.01", GoodsDesc: "notify", State: "S"}
	r.requests++
	delivery, err := r.app.deliverNotification(payment, r.notifyServer.URL+"/notify", false)
	if err != nil {
		return err
	}
	if delivery.Status != "delivered" {
		return fmt.Errorf("notify status=%s", delivery.Status)
	}
	return nil
}

func (r *scenarioRunner) scenarioNotifyBadAck(id string) error {
	bad, err := newLocalScenarioServer(http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) { _, _ = w.Write([]byte("BAD_ACK")) }))
	if err != nil {
		return err
	}
	defer bad.Close()
	payment := Payment{Kind: "aggregation", HuifuID: "6666000100000001", ReqDate: "20260624", ReqSeqID: "S10-NOTIFY-02", HFSeqID: "HF-S10-NOTIFY-02", TransAmt: "0.01", GoodsDesc: "notify bad", State: "S"}
	r.requests++
	delivery, err := r.app.deliverNotification(payment, bad.URL+"/notify", false)
	if err == nil || delivery.Status != "failed" || len(delivery.Attempts) != 4 {
		return fmt.Errorf("bad ACK delivery=%+v err=%v", delivery, err)
	}
	return nil
}

func (r *scenarioRunner) scenarioNotifyDuplicate(id string) error {
	payment := Payment{Kind: "aggregation", HuifuID: "6666000100000001", ReqDate: "20260624", ReqSeqID: "S10-NOTIFY-03", HFSeqID: "HF-S10-NOTIFY-03", TransAmt: "0.01", GoodsDesc: "notify dup", State: "S"}
	r.requests++
	delivery, err := r.app.deliverNotification(payment, r.notifyServer.URL+"/notify", true)
	if err != nil || !delivery.Duplicate || delivery.Status != "delivered" {
		return fmt.Errorf("duplicate delivery=%+v err=%v", delivery, err)
	}
	return nil
}

func (r *scenarioRunner) scenarioNotifyBlocked(id string) error {
	payment := Payment{Kind: "aggregation", HuifuID: "6666000100000001", ReqDate: "20260624", ReqSeqID: "S10-NOTIFY-04", HFSeqID: "HF-S10-NOTIFY-04", TransAmt: "0.01", GoodsDesc: "notify blocked", State: "S"}
	r.requests++
	delivery, err := r.app.deliverNotification(payment, "http://192.168.1.9/notify?"+"secret=value", false)
	if err == nil || delivery.Status != "blocked" {
		return fmt.Errorf("blocked delivery=%+v err=%v", delivery, err)
	}
	return nil
}

func (r *scenarioRunner) scenarioFaults(id string) error {
	business, err := r.postGatewayFixture("agg-create-missing-goods-desc", id, nil, map[string]any{"req_seq_id": "S11-FAULT-BIZ", "goods_desc": "fault", "sandbox_scenario": "BUSINESS_FAIL"}, nil, fixtureRunOptions{Mark: true, AssertFields: false, ExpectedRespCode: "LS200001"})
	if err != nil {
		return err
	}
	if err := expectRespCode(business, "LS200001"); err != nil {
		return err
	}
	if _, status, err := r.postGatewayRaw("/v4/trade/payment/create", map[string]any{"req_seq_id": "S10-FAULT-500", "huifu_id": "6666000100000001", "trade_type": "A_NATIVE", "trans_amt": "0.01", "goods_desc": "fault"}, map[string]string{"jpt-x-sandbox-scenario": "FAULT-500"}); err != nil || status != http.StatusInternalServerError {
		return fmt.Errorf("fault 500 status=%d err=%v", status, err)
	}
	if _, status, err := r.postGatewayRaw("/v4/trade/payment/create", map[string]any{"req_seq_id": "S10-FAULT-TIMEOUT", "huifu_id": "6666000100000001", "trade_type": "A_NATIVE", "trans_amt": "0.01", "goods_desc": "fault"}, map[string]string{"jpt-x-sandbox-scenario": "TIMEOUT"}); err != nil || status != http.StatusGatewayTimeout {
		return fmt.Errorf("fault timeout status=%d err=%v", status, err)
	}
	return nil
}

func (r *scenarioRunner) scenarioControlSecurity(id string) error {
	body, _ := json.Marshal(map[string]any{"pre_order_id": "PO-UNKNOWN"})
	req, err := newLocalRequest(http.MethodPost, "http://127.0.0.1/__merchant/hosting/confirm", bytes.NewReader(body))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	rec := newLocalResponseRecorder()
	r.control.ServeHTTP(rec, req)
	r.requests++
	if rec.Code != http.StatusForbidden {
		return fmt.Errorf("missing CSRF status=%d", rec.Code)
	}
	req, err = newLocalRequest(http.MethodGet, "http://127.0.0.1/__health/ready", nil)
	if err != nil {
		return err
	}
	req.Header.Set("Origin", "https://example.com")
	rec = newLocalResponseRecorder()
	r.control.ServeHTTP(rec, req)
	r.requests++
	if rec.Code != http.StatusForbidden {
		return fmt.Errorf("external origin status=%d", rec.Code)
	}
	return nil
}

func (r *scenarioRunner) scenarioIdempotencyConflicts(id string) error {
	if _, err := r.postGatewayFixture("agg-create-processing", id, nil, map[string]any{"req_seq_id": "S11-IDEMP-AGG", "trans_amt": "0.01", "goods_desc": "idempotency", "notify_url": ""}, nil, fixtureRunOptions{Mark: true, AssertFields: true}); err != nil {
		return err
	}
	resp, err := r.postGatewayFixture("agg-create-processing", id, nil, map[string]any{"req_seq_id": "S11-IDEMP-AGG", "trans_amt": "0.02", "goods_desc": "idempotency", "notify_url": ""}, nil, fixtureRunOptions{AssertFields: false, ExpectedRespCode: "LS000006"})
	if err != nil {
		return err
	}
	if err := expectRespCode(resp, "LS000006"); err != nil {
		return err
	}
	hosting, err := r.createHosting(id, "S11-IDEMP-HOST", "0.01", false)
	if err != nil {
		return err
	}
	resp, err = r.postGatewayFixture("hosting-preorder-accepted", id, nil, map[string]any{"req_seq_id": hosting.ReqSeqID, "trans_amt": "0.02", "goods_desc": "changed", "notify_url": ""}, nil, fixtureRunOptions{AssertFields: false, ExpectedRespCode: "LS000006"})
	if err != nil {
		return err
	}
	return expectRespCode(resp, "LS000006")
}

func (r *scenarioRunner) scenarioReportRedaction(id string) error {
	r.app.mu.Lock()
	r.app.securityFindings = append(r.app.securityFindings, SecurityFinding{Type: "test_redaction", Severity: "high", Target: "http://127.0.0.1/notify?" + "token=secret", TargetRedacted: "http://127.0.0.1/notify?REDACTED", Reason: "scenario"})
	r.app.mu.Unlock()
	return nil
}

func (r *scenarioRunner) scenarioAdvisoryScan(id string) error {
	dir, err := os.MkdirTemp("", "hf-sandbox-scan-")
	if err != nil {
		return err
	}
	defer os.RemoveAll(dir)
	path := filepath.Join(dir, "client.go")
	if err := os.WriteFile(path, []byte("package demo\nvar token = \"super-secret-token\"\n"), 0o600); err != nil {
		return err
	}
	findings, err := scanCodeAdvisories(dir)
	if err != nil {
		return err
	}
	if len(findings) == 0 {
		return fmt.Errorf("expected advisory finding")
	}
	return nil
}

func (r *scenarioRunner) scenarioAggregationRefund(id string) error {
	payment, err := r.createPaidAggregation(id, "S11-REFUND-AGG", "1.00")
	if err != nil {
		return err
	}
	refundVars := map[string]string{"payment_req_date": payment.ReqDate, "payment_req_seq_id": payment.ReqSeqID}
	refund, err := r.postGatewayFixture("agg-refund-accepted", id, refundVars, map[string]any{"req_seq_id": "S11-RF-AGG"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(refund, "00000100"); err != nil {
		return err
	}
	queryVars := map[string]string{"refund_req_seq_id": "S11-RF-AGG", "payment_req_date": payment.ReqDate, "payment_req_seq_id": payment.ReqSeqID}
	if _, err := r.postGatewayFixture("agg-refund-query-processing-then-success", id, queryVars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query2, err := r.postGatewayFixture("agg-refund-query-processing-then-success", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if got := stringValue(query2.Data["trans_stat"]); got != "S" {
		return fmt.Errorf("aggregation refund query trans_stat=%s", got)
	}
	wrong, err := r.postGatewayFixture("agg-refund-query-original-payment-locator", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(wrong, "23000001"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioRefundOverAmount(id string) error {
	payment, err := r.createPaidAggregation(id, "S11-REFUND-OVER-AGG", "0.50")
	if err != nil {
		return err
	}
	resp, err := r.postGatewayFixture("agg-refund-over-amount", id, map[string]string{"payment_req_date": payment.ReqDate, "payment_req_seq_id": payment.ReqSeqID}, map[string]any{"req_seq_id": "S11-RF-OVER-AGG"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(resp, "23000003"); err != nil {
		return err
	}
	hosting, err := r.createPaidHosting(id, "S11-REFUND-OVER-HOST", "0.50")
	if err != nil {
		return err
	}
	resp, err = r.postGatewayFixture("hosting-refund-over-amount", id, map[string]string{"hosting_req_date": hosting.ReqDate, "hosting_req_seq_id": hosting.ReqSeqID}, map[string]any{"req_seq_id": "S11-RF-OVER-HOST"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(resp, "LS200003"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioHostingRefund(id string) error {
	hosting, err := r.createPaidHosting(id, "S11-REFUND-HOST", "1.00")
	if err != nil {
		return err
	}
	refundVars := map[string]string{"hosting_req_date": hosting.ReqDate, "hosting_req_seq_id": hosting.ReqSeqID}
	resp, err := r.postGatewayFixture("hosting-refund-accepted", id, refundVars, map[string]any{"req_seq_id": "S11-RF-HOST"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(resp, "00000000"); err != nil {
		return err
	}
	queryVars := map[string]string{
		"refund_req_date":    stringValue(resp.Data["req_date"]),
		"refund_req_seq_id":  stringValue(resp.Data["req_seq_id"]),
		"hosting_req_date":   hosting.ReqDate,
		"hosting_req_seq_id": hosting.ReqSeqID,
	}
	if _, err := r.postGatewayFixture("hosting-refund-query-processing-then-success", id, queryVars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query2, err := r.postGatewayFixture("hosting-refund-query-processing-then-success", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if got := stringValue(query2.Data["trans_stat"]); got != "S" {
		return fmt.Errorf("hosting refund query trans_stat=%s", got)
	}
	wrong, err := r.postGatewayFixture("hosting-refund-query-original-payment-locator", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(wrong, "LS000004"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioAggregationClose(id string) error {
	create, err := r.postGatewayFixture("agg-create-processing", id, nil, map[string]any{"req_seq_id": "S11-CLOSE-AGG", "trans_amt": "0.20", "goods_desc": "close", "notify_url": ""}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(create, "00000100"); err != nil {
		return err
	}
	vars := map[string]string{"payment_req_date": "20260624", "payment_req_seq_id": "S11-CLOSE-AGG"}
	closeResp, err := r.postGatewayFixture("agg-close-accepted", id, vars, map[string]any{"req_seq_id": "S11-CL-AGG"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(closeResp, "00000000"); err != nil {
		return err
	}
	if _, err := r.postGatewayFixture("agg-close-query-processing-then-success", id, vars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query2, err := r.postGatewayFixture("agg-close-query-processing-then-success", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if got := stringValue(query2.Data["trans_stat"]); got != "S" {
		return fmt.Errorf("close query trans_stat=%s", got)
	}
	missing, err := r.postGatewayFixture("agg-close-query-missing-locator", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(missing, "LS000002"); err != nil {
		return err
	}
	paid, err := r.createPaidAggregation(id, "S11-CLOSE-PAID", "0.20")
	if err != nil {
		return err
	}
	paidClose, err := r.postGatewayFixture("agg-close-paid-payment", id, map[string]string{"payment_req_date": paid.ReqDate, "payment_req_seq_id": paid.ReqSeqID}, map[string]any{"req_seq_id": "S11-CL-PAID"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(paidClose, "LS200004"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioHostingClose(id string) error {
	hosting, err := r.createHosting(id, "S11-CLOSE-HOST", "0.20", false)
	if err != nil {
		return err
	}
	vars := map[string]string{"hosting_req_date": hosting.ReqDate, "hosting_req_seq_id": hosting.ReqSeqID, "hosting_pre_order_id": hosting.PreOrderID}
	closeResp, err := r.postGatewayFixture("hosting-close-accepted", id, vars, map[string]any{"req_seq_id": "S11-CL-HOST"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(closeResp, "00000000"); err != nil {
		return err
	}
	query, err := r.postGatewayFixture("hosting-query-success", id, vars, nil, nil, fixtureRunOptions{AssertFields: false})
	if err != nil {
		return err
	}
	if got := stringValue(query.Data["close_stat"]); got != "S" {
		return fmt.Errorf("hosting close_stat=%s", got)
	}
	negative, err := r.postGatewayFixture("hosting-close-missing-original", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(negative, "LS000004"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioSplitpay(id string) error {
	hosting, err := r.createPaidHosting(id, "S11-SPLITPAY", "0.60")
	if err != nil {
		return err
	}
	vars := map[string]string{"hosting_req_date": hosting.ReqDate, "hosting_req_seq_id": hosting.ReqSeqID, "hosting_pre_order_id": hosting.PreOrderID}
	ordinary, err := r.postGatewayFixture("hosting-query-success", id, vars, nil, nil, fixtureRunOptions{AssertFields: false})
	if err != nil {
		return err
	}
	if _, ok := ordinary.Data["trans_list"]; ok {
		return fmt.Errorf("ordinary query returned trans_list")
	}
	split, err := r.postGatewayFixture("hosting-splitpay-query-success", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if _, ok := split.Data["trans_list"]; !ok {
		return fmt.Errorf("splitpay missing trans_list")
	}
	negative, err := r.postGatewayFixture("hosting-splitpay-query-missing-original", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(negative, "LS000004"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioWebhookEvidence(id string) error {
	r.app.mu.Lock()
	defer r.app.mu.Unlock()
	seen := map[string]bool{}
	for _, delivery := range r.app.webhooks {
		if delivery.Status == "delivered" {
			seen[delivery.EventType] = true
		}
		if strings.Contains(delivery.TargetRedacted, "case=scenario") {
			return fmt.Errorf("webhook target query was not redacted")
		}
	}
	for _, eventType := range []string{webhookEventPayment, webhookEventRefund, webhookEventClose} {
		if !seen[eventType] {
			return fmt.Errorf("missing webhook event %s", eventType)
		}
	}
	return nil
}

func (r *scenarioRunner) scenarioReconciliation(id string) error {
	first, err := r.postGatewayFixture("reconciliation-filequery-fp-then-file", id, nil, nil, nil, fixtureRunOptions{AssertFields: false})
	if err != nil {
		return err
	}
	task := first.Data["task_details"].(map[string]any)
	if got := stringValue(task["task_stat"]); got != "FP" {
		return fmt.Errorf("first task_stat=%s", got)
	}
	second, err := r.postGatewayFixture("reconciliation-filequery-fp-then-file", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	task = second.Data["task_details"].(map[string]any)
	if got := stringValue(task["task_stat"]); got != "S" {
		return fmt.Errorf("second task_stat=%s", got)
	}
	fileDetails := second.Data["file_details"].(map[string]any)
	resp, err := http.Get(stringValue(fileDetails["download_url"]))
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("download status=%d", resp.StatusCode)
	}
	return nil
}

func (r *scenarioRunner) scenarioReconciliationNegative(id string) error {
	resp, err := r.postGatewayFixture("reconciliation-filequery-unsupported-bill-type", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if err := expectRespCode(resp, "LS200006"); err != nil {
		return err
	}
	return nil
}

func (r *scenarioRunner) scenarioAggregationChannel(id, createFixture, queryFixture, microFixture, negativeFixture string) error {
	create, err := r.postGatewayFixture(createFixture, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	vars := map[string]string{"agg_hf_seq_id": stringValue(create.Data["hf_seq_id"])}
	if _, err := r.postGatewayFixture(queryFixture, id, vars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query, err := r.postGatewayFixture(queryFixture, id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if got := stringValue(query.Data["trans_stat"]); got != "S" {
		return fmt.Errorf("%s query trans_stat=%s", queryFixture, got)
	}
	if _, err := r.postGatewayFixture(microFixture, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true}); err != nil {
		return err
	}
	negative, err := r.postGatewayFixture(negativeFixture, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	return expectRespCode(negative, "LS200007")
}

func (r *scenarioRunner) scenarioAggregationTxMetadata(id string) error {
	create, err := r.postGatewayFixture("agg-tx-metadata-create", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	vars := map[string]string{"agg_hf_seq_id": stringValue(create.Data["hf_seq_id"])}
	if _, err := r.postGatewayFixture("agg-tx-metadata-query", id, vars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query, err := r.postGatewayFixture("agg-tx-metadata-query", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if _, ok := fieldByPath(query.Data, "tx_metadata.terminal_device_data.terminal_ip"); !ok {
		return fmt.Errorf("tx_metadata terminal_device_data was not projected")
	}
	negative, err := r.postGatewayFixture("agg-tx-metadata-wrapper-error", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	return expectRespCode(negative, "LS200008")
}

func (r *scenarioRunner) scenarioHostingVariant(id, createFixture, queryFixture, negativeFixture, expectedField string) error {
	create, err := r.postGatewayFixture(createFixture, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	preOrderID := stringValue(create.Data["pre_order_id"])
	if preOrderID == "" {
		return fmt.Errorf("%s did not return pre_order_id", createFixture)
	}
	if _, err := r.getControl("/__merchant/hosting/callback?pre_order_id=" + preOrderID); err != nil {
		return err
	}
	if _, err := r.postControl("/__merchant/hosting/confirm", map[string]any{"pre_order_id": preOrderID}); err != nil {
		return err
	}
	queryVars := map[string]string{
		"hosting_req_date":     stringValue(create.Data["req_date"]),
		"hosting_req_seq_id":   stringValue(create.Data["req_seq_id"]),
		"hosting_pre_order_id": preOrderID,
	}
	query, err := r.postGatewayFixture(queryFixture, id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	if got := stringValue(query.Data["trans_stat"]); got != "S" {
		return fmt.Errorf("%s query trans_stat=%s", queryFixture, got)
	}
	if _, ok := query.Data[expectedField]; !ok {
		return fmt.Errorf("%s missing %s", queryFixture, expectedField)
	}
	negative, err := r.postGatewayFixture(negativeFixture, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	return expectRespCode(negative, "LS200009")
}

func (r *scenarioRunner) scenarioChannelNotify(id string) error {
	create, err := r.postGatewayFixture("agg-channel-wx-create", id, nil, map[string]any{"req_seq_id": "S12-CHANNEL-NOTIFY"}, nil, fixtureRunOptions{AssertFields: true})
	if err != nil {
		return err
	}
	vars := map[string]string{"agg_hf_seq_id": stringValue(create.Data["hf_seq_id"])}
	if _, err := r.postGatewayFixture("agg-channel-wx-query", id, vars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	if _, err := r.postGatewayFixture("agg-channel-wx-query", id, vars, nil, nil, fixtureRunOptions{Requests: 2, AssertFields: true}); err != nil {
		return err
	}
	r.app.mu.Lock()
	defer r.app.mu.Unlock()
	if len(r.app.notifications) == 0 {
		return fmt.Errorf("channel notify was not delivered")
	}
	notifyOK := false
	for _, delivery := range r.app.notifications {
		if delivery.PaymentReqSeqID == "S12-CHANNEL-NOTIFY" && containsString(delivery.RespDataKeys, "wx_response") {
			notifyOK = true
		}
	}
	if !notifyOK {
		return fmt.Errorf("notify resp_data keys did not include wx_response")
	}
	webhookOK := false
	for _, delivery := range r.app.webhooks {
		if delivery.EntityID == "S12-CHANNEL-NOTIFY" && delivery.EventType == webhookEventPayment && containsString(delivery.PayloadKeys, "wx_response") {
			webhookOK = true
		}
	}
	if !webhookOK {
		return fmt.Errorf("webhook payload keys did not include wx_response")
	}
	return nil
}

func (r *scenarioRunner) scenarioAggregationMetadataVariant(id, createFixture, queryFixture, expectedPath string) error {
	create, err := r.postGatewayFixture(createFixture, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	vars := map[string]string{"agg_hf_seq_id": stringValue(create.Data["hf_seq_id"])}
	if _, err := r.postGatewayFixture(queryFixture, id, vars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query, err := r.postGatewayFixture(queryFixture, id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if _, ok := fieldByPath(query.Data, expectedPath); !ok {
		return fmt.Errorf("%s was not projected", expectedPath)
	}
	return nil
}

func (r *scenarioRunner) scenarioAggregationChannelRefund(id string) error {
	create, err := r.postGatewayFixture("agg-channel-ali-create", id, nil, map[string]any{"req_seq_id": "S13-AGG-RF-ORIG", "trans_amt": "0.20", "notify_url": ""}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	vars := map[string]string{"agg_hf_seq_id": stringValue(create.Data["hf_seq_id"])}
	if _, err := r.postGatewayFixture("agg-channel-ali-query", id, vars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	if _, err := r.postGatewayFixture("agg-channel-ali-query", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2}); err != nil {
		return err
	}
	refundVars := map[string]string{"payment_req_date": "20260624", "payment_req_seq_id": "S13-AGG-RF-ORIG", "payment_hf_seq_id": stringValue(create.Data["hf_seq_id"])}
	refund, err := r.postGatewayFixture("agg-refund-channel-accepted", id, refundVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	queryVars := map[string]string{"refund_hf_seq_id": stringValue(refund.Data["hf_seq_id"])}
	if _, err := r.postGatewayFixture("agg-refund-channel-query", id, queryVars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query, err := r.postGatewayFixture("agg-refund-channel-query", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if _, ok := query.Data["alipay_response"]; !ok {
		return fmt.Errorf("aggregation refund channel response was not projected")
	}
	return nil
}

func (r *scenarioRunner) scenarioAggregationChannelClose(id string) error {
	create, err := r.postGatewayFixture("agg-channel-up-create", id, nil, map[string]any{"req_seq_id": "S13-AGG-CL-ORIG", "notify_url": ""}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	queryVars := map[string]string{"agg_hf_seq_id": stringValue(create.Data["hf_seq_id"])}
	if _, err := r.postGatewayFixture("agg-close-channel-unpaid-order-query", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true}); err != nil {
		return err
	}
	vars := map[string]string{"payment_req_date": "20260624", "payment_req_seq_id": "S13-AGG-CL-ORIG"}
	if _, err := r.postGatewayFixture("agg-close-channel-accepted", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true}); err != nil {
		return err
	}
	if _, err := r.postGatewayFixture("agg-close-channel-query", id, vars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query, err := r.postGatewayFixture("agg-close-channel-query", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if _, ok := query.Data["unionpay_response"]; !ok {
		return fmt.Errorf("aggregation close channel response was not projected")
	}
	return nil
}

func (r *scenarioRunner) scenarioHostingCombo(id string) error {
	create, err := r.postGatewayFixture("hosting-channel-combo-preorder", id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	preOrderID := stringValue(create.Data["pre_order_id"])
	if _, err := r.getControl("/__merchant/hosting/callback?pre_order_id=" + preOrderID); err != nil {
		return err
	}
	if _, err := r.postControl("/__merchant/hosting/confirm", map[string]any{"pre_order_id": preOrderID}); err != nil {
		return err
	}
	queryVars := map[string]string{
		"hosting_req_date":     stringValue(create.Data["req_date"]),
		"hosting_req_seq_id":   stringValue(create.Data["req_seq_id"]),
		"hosting_pre_order_id": preOrderID,
	}
	query, err := r.postGatewayFixture("hosting-channel-combo-query", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	for _, field := range []string{"hosting_data", "app_data", "unionpay_response", "dy_response"} {
		if _, ok := query.Data[field]; !ok {
			return fmt.Errorf("hosting combo query missing %s", field)
		}
	}
	return nil
}

func (r *scenarioRunner) scenarioHostingChannelRefund(id string) error {
	create, err := r.postGatewayFixture("hosting-h5-wx-preorder", id, nil, map[string]any{"req_seq_id": "S13-HOST-RF-ORIG", "trans_amt": "0.20"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	preOrderID := stringValue(create.Data["pre_order_id"])
	if _, err := r.getControl("/__merchant/hosting/callback?pre_order_id=" + preOrderID); err != nil {
		return err
	}
	if _, err := r.postControl("/__merchant/hosting/confirm", map[string]any{"pre_order_id": preOrderID}); err != nil {
		return err
	}
	queryVars := map[string]string{
		"hosting_req_date":     stringValue(create.Data["req_date"]),
		"hosting_req_seq_id":   stringValue(create.Data["req_seq_id"]),
		"hosting_pre_order_id": preOrderID,
	}
	if _, err := r.postGatewayFixture("hosting-h5-wx-query", id, queryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true}); err != nil {
		return err
	}
	refundVars := map[string]string{"hosting_req_date": "20260624", "hosting_req_seq_id": "S13-HOST-RF-ORIG"}
	refund, err := r.postGatewayFixture("hosting-refund-channel-accepted", id, refundVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	refundQueryVars := map[string]string{
		"refund_hf_seq_id":  stringValue(refund.Data["hf_seq_id"]),
		"refund_req_date":   stringValue(refund.Data["req_date"]),
		"refund_req_seq_id": stringValue(refund.Data["req_seq_id"]),
	}
	if _, err := r.postGatewayFixture("hosting-refund-channel-query", id, refundQueryVars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	query, err := r.postGatewayFixture("hosting-refund-channel-query", id, refundQueryVars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	if _, ok := query.Data["wx_response"]; !ok {
		return fmt.Errorf("hosting refund channel response was not projected")
	}
	return nil
}

func (r *scenarioRunner) scenarioHostingChannelClose(id string) error {
	create, err := r.postGatewayFixture("hosting-channel-combo-preorder", id, nil, map[string]any{"req_seq_id": "S13-HOST-CL-ORIG"}, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	preOrderID := stringValue(create.Data["pre_order_id"])
	vars := map[string]string{"hosting_req_date": stringValue(create.Data["req_date"]), "hosting_req_seq_id": "S13-HOST-CL-ORIG", "hosting_pre_order_id": preOrderID}
	if _, err := r.postGatewayFixture("hosting-close-channel-accepted", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true}); err != nil {
		return err
	}
	query, err := r.postGatewayFixture("hosting-close-channel-query", id, vars, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
	if err != nil {
		return err
	}
	for _, field := range []string{"unionpay_response", "dy_response"} {
		if _, ok := query.Data[field]; !ok {
			return fmt.Errorf("hosting close channel response missing %s", field)
		}
	}
	return nil
}

func (r *scenarioRunner) scenarioReconciliationBillTypes(id string) error {
	for _, fixtureID := range []string{"reconciliation-bill-split-bill", "reconciliation-bill-merge-bill", "reconciliation-bill-settle-bill"} {
		if _, err := r.postGatewayFixture(fixtureID, id, nil, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
			return err
		}
		resp, err := r.postGatewayFixture(fixtureID, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
		if err != nil {
			return err
		}
		if err := r.downloadReconciliation(resp, http.StatusOK); err != nil {
			return err
		}
	}
	return nil
}

func (r *scenarioRunner) scenarioReconciliationDownloadEdges(id string) error {
	if err := r.reconciliationEdge(id, "reconciliation-empty-file", http.StatusOK); err != nil {
		return err
	}
	if err := r.reconciliationEdge(id, "reconciliation-expired-download", http.StatusGone); err != nil {
		return err
	}
	return r.reconciliationEdge(id, "reconciliation-forbidden-download", http.StatusForbidden)
}

func (r *scenarioRunner) reconciliationEdge(id, fixtureID string, wantStatus int) error {
	if _, err := r.postGatewayFixture(fixtureID, id, nil, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return err
	}
	resp, err := r.postGatewayFixture(fixtureID, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true, Requests: 2})
	if err != nil {
		return err
	}
	return r.downloadReconciliation(resp, wantStatus)
}

func (r *scenarioRunner) downloadReconciliation(resp SignedResponse, wantStatus int) error {
	fileDetails, ok := resp.Data["file_details"].(map[string]any)
	if !ok {
		return fmt.Errorf("file_details missing")
	}
	downloadURL := stringValue(fileDetails["download_url"])
	got, err := http.Get(downloadURL)
	if err != nil {
		return err
	}
	defer got.Body.Close()
	if got.StatusCode != wantStatus {
		return fmt.Errorf("download status=%d want=%d", got.StatusCode, wantStatus)
	}
	return nil
}

func (r *scenarioRunner) scenarioFieldErrors(id string) error {
	for _, item := range []struct {
		fixture string
		code    string
	}{
		{"agg-create-invalid-amount", "LS000005"},
		{"reconciliation-invalid-date", "LS200010"},
		{"hosting-unsupported-pre-order-type", "LS200009"},
	} {
		resp, err := r.postGatewayFixture(item.fixture, id, nil, nil, nil, fixtureRunOptions{Mark: true, AssertFields: true})
		if err != nil {
			return err
		}
		if err := expectRespCode(resp, item.code); err != nil {
			return err
		}
	}
	return nil
}

func (r *scenarioRunner) createPaidAggregation(scenarioID, reqSeqID, amount string) (Payment, error) {
	create, err := r.postGatewayFixture("agg-create-processing", scenarioID, nil, map[string]any{"req_seq_id": reqSeqID, "trans_amt": amount, "goods_desc": "paid aggregation", "notify_url": ""}, nil, fixtureRunOptions{Mark: scenarioID != "", AssertFields: true})
	if err != nil {
		return Payment{}, err
	}
	hfSeqID := stringValue(create.Data["hf_seq_id"])
	vars := map[string]string{"agg_hf_seq_id": hfSeqID}
	if _, err := r.postGatewayFixture("agg-query-processing-then-success", scenarioID, vars, nil, nil, fixtureRunOptions{AssertFields: false}); err != nil {
		return Payment{}, err
	}
	if _, err := r.postGatewayFixture("agg-query-processing-then-success", scenarioID, vars, nil, nil, fixtureRunOptions{Mark: scenarioID != "", AssertFields: true, Requests: 2}); err != nil {
		return Payment{}, err
	}
	r.app.mu.Lock()
	defer r.app.mu.Unlock()
	return *r.app.payments[reqSeqID], nil
}

func (r *scenarioRunner) createHosting(scenarioID, reqSeqID, amount string, notify bool) (Payment, error) {
	overrides := map[string]any{"req_seq_id": reqSeqID, "trans_amt": amount, "goods_desc": "hosting scenario"}
	if !notify {
		overrides["notify_url"] = ""
	}
	resp, err := r.postGatewayFixture("hosting-preorder-accepted", scenarioID, nil, overrides, nil, fixtureRunOptions{Mark: scenarioID != "", AssertFields: true})
	if err != nil {
		return Payment{}, err
	}
	if err := expectRespCode(resp, "00000000"); err != nil {
		return Payment{}, err
	}
	r.app.mu.Lock()
	defer r.app.mu.Unlock()
	return *r.app.payments[reqSeqID], nil
}

func (r *scenarioRunner) createPaidHosting(scenarioID, reqSeqID, amount string) (Payment, error) {
	payment, err := r.createHosting(scenarioID, reqSeqID, amount, true)
	if err != nil {
		return Payment{}, err
	}
	if _, err := r.getControl("/__merchant/hosting/callback?pre_order_id=" + payment.PreOrderID); err != nil {
		return Payment{}, err
	}
	if _, err := r.postControl("/__merchant/hosting/confirm", map[string]any{"pre_order_id": payment.PreOrderID}); err != nil {
		return Payment{}, err
	}
	queryVars := map[string]string{"hosting_req_date": payment.ReqDate, "hosting_req_seq_id": payment.ReqSeqID, "hosting_pre_order_id": payment.PreOrderID}
	if _, err := r.postGatewayFixture("hosting-query-success", scenarioID, queryVars, nil, nil, fixtureRunOptions{Mark: scenarioID != "", AssertFields: true}); err != nil {
		return Payment{}, err
	}
	r.app.mu.Lock()
	defer r.app.mu.Unlock()
	return *r.app.payments[reqSeqID], nil
}

func (r *scenarioRunner) postGateway(path string, data map[string]any, headers map[string]string) (SignedResponse, error) {
	body, status, err := r.postGatewayRaw(path, data, headers)
	if err != nil {
		return SignedResponse{}, err
	}
	if status != http.StatusOK {
		return SignedResponse{}, fmt.Errorf("%s status=%d body=%s", path, status, body)
	}
	var resp SignedResponse
	if err := json.Unmarshal(body, &resp); err != nil {
		return resp, err
	}
	if err := verifyData(resp.Data, resp.Sign, r.app.creds.GatewayPublic); err != nil {
		return resp, err
	}
	return resp, nil
}

type fixtureRunOptions struct {
	Mark             bool
	AssertFields     bool
	Requests         int
	ExpectedRespCode string
}

func (r *scenarioRunner) postGatewayFixture(fixtureID, scenarioID string, vars map[string]string, overrides map[string]any, headers map[string]string, options fixtureRunOptions) (SignedResponse, error) {
	fixture, ok := r.app.bundle.Fixtures[fixtureID]
	if !ok {
		return SignedResponse{}, fmt.Errorf("unknown fixture %s", fixtureID)
	}
	data, err := r.fixtureRequestData(fixture, vars)
	if err != nil {
		if options.Mark {
			r.markFixture(fixtureID, scenarioID, "failed", maxInt(1, options.Requests), err.Error())
		}
		return SignedResponse{}, err
	}
	for key, value := range overrides {
		data[key] = value
	}
	resp, err := r.postGateway(fixture.Path, data, headers)
	if err != nil {
		if options.Mark {
			r.markFixture(fixtureID, scenarioID, "failed", maxInt(1, options.Requests), err.Error())
		}
		return SignedResponse{}, err
	}
	expectedCode := fixture.Expected.RespCode
	if expectedCode == "" {
		expectedCode = fixture.ExpectedRespCode
	}
	if options.ExpectedRespCode != "" {
		expectedCode = options.ExpectedRespCode
	}
	if expectedCode != "" {
		if err := expectRespCode(resp, expectedCode); err != nil {
			if options.Mark {
				r.markFixture(fixtureID, scenarioID, "failed", maxInt(1, options.Requests), err.Error())
			}
			return resp, err
		}
	}
	if options.AssertFields {
		if err := assertFixtureFields(resp.Data, fixture.FieldAssertions); err != nil {
			if options.Mark {
				r.markFixture(fixtureID, scenarioID, "failed", maxInt(1, options.Requests), err.Error())
			}
			return resp, err
		}
	}
	if options.Mark {
		r.markFixture(fixtureID, scenarioID, "passed", maxInt(1, options.Requests), "")
	}
	return resp, nil
}

func (r *scenarioRunner) fixtureRequestData(fixture FixtureDefinition, vars map[string]string) (map[string]any, error) {
	data := map[string]any{}
	for key, value := range fixture.Request.Data {
		resolved, err := r.resolveFixtureValue(value, vars)
		if err != nil {
			return nil, fmt.Errorf("%s.%s: %w", fixture.ID, key, err)
		}
		data[key] = resolved
	}
	return data, nil
}

func (r *scenarioRunner) resolveFixtureValue(value any, vars map[string]string) (any, error) {
	switch typed := value.(type) {
	case string:
		if strings.HasPrefix(typed, "{{") && strings.HasSuffix(typed, "}}") {
			token := strings.TrimSuffix(strings.TrimPrefix(typed, "{{"), "}}")
			if strings.HasPrefix(token, "notify_url:") {
				return r.notifyServer.URL + strings.TrimPrefix(token, "notify_url:"), nil
			}
			if v, ok := vars[token]; ok {
				return v, nil
			}
			return nil, fmt.Errorf("unresolved fixture token %s", token)
		}
		return typed, nil
	case map[string]any:
		out := map[string]any{}
		for key, nested := range typed {
			resolved, err := r.resolveFixtureValue(nested, vars)
			if err != nil {
				return nil, err
			}
			out[key] = resolved
		}
		return out, nil
	case []any:
		out := make([]any, len(typed))
		for i, nested := range typed {
			resolved, err := r.resolveFixtureValue(nested, vars)
			if err != nil {
				return nil, err
			}
			out[i] = resolved
		}
		return out, nil
	default:
		return value, nil
	}
}

func assertFixtureFields(data map[string]any, assertions []FixtureFieldAssertion) error {
	for _, assertion := range assertions {
		value, ok := fieldByPath(data, assertion.Path)
		if assertion.Exists {
			if !ok {
				return fmt.Errorf("expected response field %s to exist", assertion.Path)
			}
			continue
		}
		if assertion.Equals != "" {
			if !ok {
				return fmt.Errorf("expected response field %s=%s, field missing", assertion.Path, assertion.Equals)
			}
			if got := stringValue(value); got != assertion.Equals {
				return fmt.Errorf("expected response field %s=%s, got %s", assertion.Path, assertion.Equals, got)
			}
		}
	}
	return nil
}

func fieldByPath(data map[string]any, path string) (any, bool) {
	var current any = data
	for _, part := range strings.Split(path, ".") {
		switch typed := current.(type) {
		case map[string]any:
			value, ok := typed[part]
			if !ok {
				return nil, false
			}
			current = value
		default:
			return nil, false
		}
	}
	return current, true
}

func maxInt(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func (r *scenarioRunner) postGatewayRaw(path string, data map[string]any, headers map[string]string) ([]byte, int, error) {
	signature, err := signData(data, r.app.creds.MerchantPrivate)
	if err != nil {
		return nil, 0, err
	}
	body, _ := json.Marshal(Envelope{SysID: "SYS", ProductID: "MYPAY", Sign: signature, Data: data})
	req, err := newLocalRequest(http.MethodPost, path, bytes.NewReader(body))
	if err != nil {
		return nil, 0, err
	}
	req.Header.Set("Content-Type", "application/json;charset=UTF-8")
	req.Header.Set("jpt-x-skill-source", sandboxSkillSource)
	if huifuID := stringValue(data["huifu_id"]); huifuID != "" {
		req.Header.Set("jpt-x-skill-huifu_id", huifuID)
	}
	for key, value := range headers {
		req.Header.Set(key, value)
	}
	rec := newLocalResponseRecorder()
	r.gateway.ServeHTTP(rec, req)
	r.requests++
	return rec.Body.Bytes(), rec.Code, nil
}

func (r *scenarioRunner) getControl(path string) (map[string]any, error) {
	req, err := newLocalRequest(http.MethodGet, "http://127.0.0.1"+path, nil)
	if err != nil {
		return nil, err
	}
	rec := newLocalResponseRecorder()
	r.control.ServeHTTP(rec, req)
	r.requests++
	if rec.Code != http.StatusOK {
		return nil, fmt.Errorf("%s status=%d body=%s", path, rec.Code, rec.Body.String())
	}
	var out map[string]any
	return out, json.Unmarshal(rec.Body.Bytes(), &out)
}

func (r *scenarioRunner) postControl(path string, data map[string]any) (map[string]any, error) {
	body, _ := json.Marshal(data)
	req, err := newLocalRequest(http.MethodPost, "http://127.0.0.1"+path, bytes.NewReader(body))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Huifu-Sandbox-CSRF", r.app.csrfToken)
	rec := newLocalResponseRecorder()
	r.control.ServeHTTP(rec, req)
	r.requests++
	if rec.Code != http.StatusOK {
		return nil, fmt.Errorf("%s status=%d body=%s", path, rec.Code, rec.Body.String())
	}
	var out map[string]any
	return out, json.Unmarshal(rec.Body.Bytes(), &out)
}

func (r *scenarioRunner) markFixture(id, scenarioID, status string, requests int, errText string) {
	fixture := r.app.bundle.Fixtures[id]
	if existing, ok := r.fixtures[id]; ok {
		if existing.Status == "passed" && status == "passed" {
			existing.Requests += requests
			if existing.ScenarioID == "" {
				existing.ScenarioID = scenarioID
			}
			r.fixtures[id] = existing
			return
		}
		if existing.Status == "passed" && status != "passed" {
			return
		}
	}
	r.fixtures[id] = FixtureResult{ID: id, EndpointID: fixture.EndpointID, Kind: fixture.Kind, Status: status, ScenarioID: scenarioID, Requests: requests, Error: errText}
}

func (r *scenarioRunner) fixtureResults() []FixtureResult {
	out := make([]FixtureResult, 0, len(r.fixtures))
	for _, result := range r.fixtures {
		out = append(out, result)
	}
	sort.Slice(out, func(i, j int) bool { return out[i].ID < out[j].ID })
	return out
}

func (r *scenarioRunner) resultForScenario(id string, startRequests, startEvents int, err error) ScenarioResult {
	assertion := r.scenarioAssertion(id)
	status := "passed"
	errText := ""
	if err != nil {
		status = "failed"
		errText = err.Error()
	}
	return ScenarioResult{
		ID:          id,
		Status:      status,
		Requests:    r.requests - startRequests,
		EndpointIDs: assertion.EndpointIDs,
		FixtureIDs:  assertion.FixtureIDs,
		Events:      r.eventsSince(startEvents),
		ReportFiles: assertion.ExpectedReportFiles,
		Error:       errText,
	}
}

func (r *scenarioRunner) scenarioAssertion(id string) ScenarioAssertion {
	for _, assertion := range r.app.bundle.ScenarioAssertions.Scenarios {
		if assertion.ID == id {
			return assertion
		}
	}
	return ScenarioAssertion{ID: id}
}

func (r *scenarioRunner) eventCount() int {
	r.app.mu.Lock()
	defer r.app.mu.Unlock()
	return len(r.app.events)
}

func (r *scenarioRunner) eventsSince(start int) []string {
	r.app.mu.Lock()
	defer r.app.mu.Unlock()
	seen := map[string]bool{}
	var out []string
	for _, event := range r.app.events[start:] {
		if !seen[event.Type] {
			seen[event.Type] = true
			out = append(out, event.Type)
		}
	}
	sort.Strings(out)
	return out
}

func (r *scenarioRunner) assertReportFiles(results []ScenarioResult) error {
	needed := map[string]bool{}
	for _, result := range results {
		for _, name := range result.ReportFiles {
			needed[name] = true
		}
	}
	for name := range needed {
		if !fileExists(filepath.Join(r.app.reportDir, name)) {
			return fmt.Errorf("scenario report missing %s", name)
		}
	}
	return nil
}

func scenarioValidationReport(app *App, reportDir string) *ScenarioValidationReport {
	app.mu.Lock()
	scenarios := append([]ScenarioResult(nil), app.scenarioResults...)
	fixtures := append([]FixtureResult(nil), app.fixtureResults...)
	app.mu.Unlock()
	endpointSummary := endpointScenarioStatus(scenarios)
	fixtureSummary := fixtureStatusMap(fixtures)
	for _, endpoint := range app.bundle.Endpoints.Endpoints {
		if endpointSummary[endpoint.ID] == "" {
			endpointSummary[endpoint.ID] = "not_executed"
		}
	}
	for _, fixture := range app.bundle.Fixtures {
		if fixture.SourceSampleID != "" {
			continue
		}
		if fixtureSummary[fixture.ID] == "" {
			fixtureSummary[fixture.ID] = "not_executed"
		}
	}
	passed, failed := 0, 0
	for _, result := range scenarios {
		if result.Status == "passed" {
			passed++
		} else {
			failed++
		}
	}
	for _, status := range endpointSummary {
		if status != "covered" {
			failed++
		}
	}
	for _, status := range fixtureSummary {
		if status != "covered" {
			failed++
		}
	}
	return &ScenarioValidationReport{
		OK:                    failed == 0,
		CoverageRunnerVersion: coverageRunnerVersion,
		FixtureRunnerVersion:  fixtureRunnerVersion,
		ReportDir:             reportDir,
		ScenarioCount:         len(scenarios),
		Passed:                passed,
		Failed:                failed,
		EndpointSummary:       endpointSummary,
		FixtureSummary:        fixtureSummary,
		Scenarios:             scenarios,
		Fixtures:              fixtures,
	}
}

func expectRespCode(resp SignedResponse, want string) error {
	if got := stringValue(resp.Data["resp_code"]); got != want {
		return fmt.Errorf("resp_code=%s want %s data=%+v", got, want, resp.Data)
	}
	return nil
}

func cloneMap(in map[string]any) map[string]any {
	out := map[string]any{}
	for key, value := range in {
		out[key] = value
	}
	return out
}

func containsString(values []string, want string) bool {
	for _, value := range values {
		if value == want {
			return true
		}
	}
	return false
}
