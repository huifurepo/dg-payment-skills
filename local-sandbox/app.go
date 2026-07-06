package main

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"sync"
	"time"
)

type App struct {
	bundle          *ContractBundle
	creds           *CredentialSet
	startedAt       time.Time
	runID           string
	mode            string
	officialGateway string
	adminToken      string
	adminDisabled   bool
	csrfToken       string
	shutdown        func()
	reportDir       string
	dataDir         string
	gatewayBaseURL  string
	httpClient      *http.Client
	mu              sync.Mutex
	events          []Event
	payments        map[string]*Payment
	refunds         map[string]*RefundOperation
	closes          map[string]*CloseOperation
	reconciliations map[string]*ReconciliationFile
	hfIndex         map[string]string
	preIndex        map[string]string
	refundHFIndex   map[string]string
	refundMerIndex  map[string]string
	closeIndex      map[string]string

	notifyAllowlist    map[string]struct{}
	notifyMaxAttempt   int
	notifyRetryDelay   time.Duration
	faultTimeoutDelay  time.Duration
	notifications      []NotificationDelivery
	webhookEndpointKey string
	webhookTargets     []string
	webhooks           []WebhookDelivery
	securityFindings   []SecurityFinding
	controlBaseURL     string
	updateIndexURL     string
	scenarioResults    []ScenarioResult
	fixtureResults     []FixtureResult
	requestLogSeq      int
	requestLogs        []RequestLog
}

type AppOptions struct {
	DataDir           string
	ReportDir         string
	Ephemeral         bool
	CredentialProfile string
	Mode              string
	OfficialGateway   string
	UpdateIndexURL    string
}

type Event struct {
	Time       string         `json:"time"`
	Type       string         `json:"type"`
	Endpoint   string         `json:"endpoint,omitempty"`
	EntityID   string         `json:"entity_id,omitempty"`
	ScenarioID string         `json:"scenario_id,omitempty"`
	Details    map[string]any `json:"details,omitempty"`
}

type RequestLog struct {
	ID                string         `json:"id"`
	Time              string         `json:"time"`
	Method            string         `json:"method"`
	Path              string         `json:"path"`
	Kind              string         `json:"kind"`
	HTTPStatus        int            `json:"http_status"`
	RespCode          string         `json:"resp_code,omitempty"`
	RespDesc          string         `json:"resp_desc,omitempty"`
	ReqSeqID          string         `json:"req_seq_id,omitempty"`
	HuifuID           string         `json:"huifu_id,omitempty"`
	ProductID         string         `json:"product_id,omitempty"`
	SysID             string         `json:"sys_id,omitempty"`
	SignatureStatus   string         `json:"signature_status,omitempty"`
	RequestDataStatus string         `json:"request_data_status,omitempty"`
	RequestEnvelope   map[string]any `json:"request_envelope,omitempty"`
	RequestData       map[string]any `json:"request_data,omitempty"`
	ResponseEnvelope  map[string]any `json:"response_envelope,omitempty"`
	ResponseData      map[string]any `json:"response_data,omitempty"`
	ResponseBody      string         `json:"response_body,omitempty"`
}

type Payment struct {
	Kind                string         `json:"kind"`
	HuifuID             string         `json:"huifu_id"`
	ReqDate             string         `json:"req_date"`
	ReqSeqID            string         `json:"req_seq_id"`
	HFSeqID             string         `json:"hf_seq_id,omitempty"`
	PreOrderID          string         `json:"pre_order_id,omitempty"`
	TradeType           string         `json:"trade_type,omitempty"`
	PreOrderType        string         `json:"pre_order_type,omitempty"`
	BusinessVariant     string         `json:"business_variant,omitempty"`
	TransAmt            string         `json:"trans_amt"`
	TransAmtFen         int64          `json:"trans_amt_fen"`
	GoodsDesc           string         `json:"goods_desc"`
	NotifyURL           string         `json:"notify_url,omitempty"`
	RequestDigest       string         `json:"request_digest,omitempty"`
	RefundedAmt         string         `json:"refunded_amount"`
	RefundedFen         int64          `json:"refunded_amount_fen"`
	RefundableAmt       string         `json:"refundable_amount"`
	RefundableFen       int64          `json:"refundable_amount_fen"`
	State               string         `json:"state"`
	QueryCount          int            `json:"query_count"`
	Notified            bool           `json:"notified"`
	Webhooked           bool           `json:"webhooked"`
	HostingCallbackSeen bool           `json:"hosting_callback_seen,omitempty"`
	HostingConfirmed    bool           `json:"hosting_confirmed,omitempty"`
	ConfirmCount        int            `json:"confirm_count,omitempty"`
	TxMetadata          map[string]any `json:"tx_metadata,omitempty"`
	ChannelResponse     map[string]any `json:"channel_response,omitempty"`
}

type RefundOperation struct {
	Kind              string         `json:"kind"`
	ProductID         string         `json:"product_id,omitempty"`
	HuifuID           string         `json:"huifu_id"`
	ReqDate           string         `json:"req_date"`
	ReqSeqID          string         `json:"req_seq_id"`
	HFSeqID           string         `json:"hf_seq_id"`
	MerOrdID          string         `json:"mer_ord_id,omitempty"`
	PaymentReqSeqID   string         `json:"payment_req_seq_id"`
	PaymentReqDate    string         `json:"payment_req_date"`
	PaymentHFSeqID    string         `json:"payment_hf_seq_id,omitempty"`
	PaymentPreOrderID string         `json:"payment_pre_order_id,omitempty"`
	OrdAmt            string         `json:"ord_amt"`
	OrdAmtFen         int64          `json:"ord_amt_fen"`
	NotifyURL         string         `json:"notify_url,omitempty"`
	RequestDigest     string         `json:"request_digest,omitempty"`
	State             string         `json:"state"`
	QueryCount        int            `json:"query_count"`
	Settled           bool           `json:"settled"`
	Notified          bool           `json:"notified"`
	Webhooked         bool           `json:"webhooked"`
	BusinessVariant   string         `json:"business_variant,omitempty"`
	ChannelResponse   map[string]any `json:"channel_response,omitempty"`
}

type CloseOperation struct {
	Kind            string         `json:"kind"`
	HuifuID         string         `json:"huifu_id"`
	ReqDate         string         `json:"req_date"`
	ReqSeqID        string         `json:"req_seq_id"`
	PaymentReqSeqID string         `json:"payment_req_seq_id"`
	PaymentReqDate  string         `json:"payment_req_date"`
	PaymentHFSeqID  string         `json:"payment_hf_seq_id,omitempty"`
	NotifyURL       string         `json:"notify_url,omitempty"`
	State           string         `json:"state"`
	RequestDigest   string         `json:"request_digest,omitempty"`
	QueryCount      int            `json:"query_count"`
	Notified        bool           `json:"notified"`
	Webhooked       bool           `json:"webhooked"`
	BusinessVariant string         `json:"business_variant,omitempty"`
	ChannelResponse map[string]any `json:"channel_response,omitempty"`
}

type ReconciliationFile struct {
	ID             string `json:"id"`
	HuifuID        string `json:"huifu_id"`
	FileDate       string `json:"file_date"`
	BillType       string `json:"bill_type"`
	FileName       string `json:"file_name"`
	QueryCount     int    `json:"query_count"`
	TaskStat       string `json:"task_stat"`
	Ready          bool   `json:"ready"`
	DownloadURL    string `json:"download_url,omitempty"`
	RowCount       int    `json:"row_count"`
	DownloadStatus string `json:"download_status,omitempty"`
}

type NotificationDelivery struct {
	ID              string                `json:"id"`
	Time            string                `json:"time"`
	PaymentReqSeqID string                `json:"payment_req_seq_id"`
	Target          string                `json:"target"`
	TargetRedacted  string                `json:"target_redacted"`
	Status          string                `json:"status"`
	ExpectedACK     string                `json:"expected_ack"`
	AckBody         string                `json:"ack_body,omitempty"`
	Error           string                `json:"error,omitempty"`
	Diagnosis       string                `json:"diagnosis,omitempty"`
	Duplicate       bool                  `json:"duplicate"`
	RespDataSHA256  string                `json:"resp_data_sha256"`
	RespDataKeys    []string              `json:"resp_data_keys,omitempty"`
	Attempts        []NotificationAttempt `json:"attempts"`
}

type NotificationAttempt struct {
	Attempt    int    `json:"attempt"`
	Time       string `json:"time"`
	Status     string `json:"status"`
	HTTPStatus int    `json:"http_status,omitempty"`
	AckBody    string `json:"ack_body,omitempty"`
	Error      string `json:"error,omitempty"`
	Diagnosis  string `json:"diagnosis,omitempty"`
}

type WebhookDelivery struct {
	ID             string           `json:"id"`
	Time           string           `json:"time"`
	EventType      string           `json:"event_type"`
	EntityID       string           `json:"entity_id"`
	Target         string           `json:"target"`
	TargetRedacted string           `json:"target_redacted"`
	Status         string           `json:"status"`
	Sign           string           `json:"sign,omitempty"`
	RawBodySHA256  string           `json:"raw_body_sha256"`
	PayloadKeys    []string         `json:"payload_keys,omitempty"`
	Error          string           `json:"error,omitempty"`
	Diagnosis      string           `json:"diagnosis,omitempty"`
	Attempts       []WebhookAttempt `json:"attempts"`
}

type WebhookAttempt struct {
	Attempt    int    `json:"attempt"`
	Time       string `json:"time"`
	Status     string `json:"status"`
	HTTPStatus int    `json:"http_status,omitempty"`
	AckBody    string `json:"ack_body,omitempty"`
	Error      string `json:"error,omitempty"`
	Diagnosis  string `json:"diagnosis,omitempty"`
}

type SecurityFinding struct {
	Time           string `json:"time"`
	Type           string `json:"type"`
	Severity       string `json:"severity"`
	Target         string `json:"target"`
	TargetRedacted string `json:"target_redacted"`
	Reason         string `json:"reason"`
}

type ScenarioResult struct {
	ID          string   `json:"id"`
	Status      string   `json:"status"`
	Requests    int      `json:"requests"`
	EndpointIDs []string `json:"endpoint_ids,omitempty"`
	FixtureIDs  []string `json:"fixture_ids,omitempty"`
	Events      []string `json:"events,omitempty"`
	ReportFiles []string `json:"report_files,omitempty"`
	Error       string   `json:"error,omitempty"`
}

type FixtureResult struct {
	ID         string `json:"id"`
	EndpointID string `json:"endpoint_id"`
	Kind       string `json:"kind"`
	Status     string `json:"status"`
	ScenarioID string `json:"scenario_id,omitempty"`
	Requests   int    `json:"requests"`
	Error      string `json:"error,omitempty"`
}

func NewApp(dataDir, reportDir string, ephemeral bool) (*App, error) {
	return NewAppWithOptions(AppOptions{DataDir: dataDir, ReportDir: reportDir, Ephemeral: ephemeral})
}

func NewAppWithOptions(options AppOptions) (*App, error) {
	bundle, err := loadContractBundle()
	if err != nil {
		return nil, err
	}
	dataDir := options.DataDir
	if dataDir == "" {
		dataDir = defaultDataDir()
	}
	reportDir := options.ReportDir
	ephemeral := options.Ephemeral
	if reportDir == "" && !ephemeral {
		reportDir = filepath.Join(dataDir, "runs", time.Now().Format("20060102-150405"))
	}
	creds, err := loadOrCreateCredentialsProfile(dataDir, ephemeral, options.CredentialProfile)
	if err != nil {
		return nil, err
	}
	mode := firstNonEmpty(options.Mode, "local-simulation")
	runID := time.Now().Format("20060102-150405.000000000")
	token, err := randomToken()
	if err != nil {
		return nil, err
	}
	csrfToken, err := randomToken()
	if err != nil {
		return nil, err
	}
	webhookKey, err := randomFixedToken(32)
	if err != nil {
		return nil, err
	}
	app := &App{
		bundle:             bundle,
		creds:              creds,
		startedAt:          time.Now().UTC(),
		runID:              runID,
		mode:               mode,
		officialGateway:    options.OfficialGateway,
		adminToken:         token,
		csrfToken:          csrfToken,
		webhookEndpointKey: webhookKey,
		reportDir:          reportDir,
		dataDir:            dataDir,
		updateIndexURL:     firstNonEmpty(options.UpdateIndexURL, defaultUpdateIndexURL),
		httpClient: &http.Client{
			Timeout: 5 * time.Second,
			CheckRedirect: func(req *http.Request, via []*http.Request) error {
				return securityError("redirects are not allowed for notify delivery")
			},
		},
		payments:          map[string]*Payment{},
		refunds:           map[string]*RefundOperation{},
		closes:            map[string]*CloseOperation{},
		reconciliations:   map[string]*ReconciliationFile{},
		hfIndex:           map[string]string{},
		preIndex:          map[string]string{},
		refundHFIndex:     map[string]string{},
		refundMerIndex:    map[string]string{},
		closeIndex:        map[string]string{},
		notifyAllowlist:   map[string]struct{}{},
		notifyMaxAttempt:  4,
		notifyRetryDelay:  100 * time.Millisecond,
		faultTimeoutDelay: 200 * time.Millisecond,
	}
	app.record("sandbox.start", "", "", map[string]any{
		"version":              appVersion,
		"skill_source":         skillSource,
		"sandbox_skill_source": sandboxSkillSource,
		"contract_bundle":      contractBundle,
		"contract_digest":      bundle.Digest,
		"ephemeral":            ephemeral,
		"credential_profile":   firstNonEmpty(creds.ProfileName, "synthetic"),
		"signature_model":      firstNonEmpty(creds.SignatureModel, "synthetic-dual-key"),
		"mode":                 mode,
	})
	return app, nil
}

func (a *App) record(kind, endpoint, entityID string, details map[string]any) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.events = append(a.events, Event{
		Time:     time.Now().UTC().Format(time.RFC3339Nano),
		Type:     kind,
		Endpoint: endpoint,
		EntityID: entityID,
		Details:  details,
	})
}

func randomToken() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return base64.RawURLEncoding.EncodeToString(b), nil
}

func randomFixedToken(length int) (string, error) {
	token, err := randomToken()
	if err != nil {
		return "", err
	}
	for len(token) < length {
		more, err := randomToken()
		if err != nil {
			return "", err
		}
		token += more
	}
	return token[:length], nil
}

func defaultDataDir() string {
	if runtime.GOOS == "windows" {
		if base := os.Getenv("LOCALAPPDATA"); base != "" {
			return filepath.Join(base, "HuifuPaymentSandbox")
		}
	}
	if runtime.GOOS == "darwin" {
		if home, err := os.UserHomeDir(); err == nil {
			return filepath.Join(home, "Library", "Application Support", "HuifuPaymentSandbox")
		}
	}
	if state := os.Getenv("XDG_STATE_HOME"); state != "" {
		return filepath.Join(state, "huifu-payment-sandbox")
	}
	if home, err := os.UserHomeDir(); err == nil {
		return filepath.Join(home, ".local", "state", "huifu-payment-sandbox")
	}
	return filepath.Join(os.TempDir(), "huifu-payment-sandbox")
}

func nowDate() string {
	return time.Now().Format("20060102")
}

func nowDateTime() string {
	return time.Now().Format("20060102150405")
}

func nextID(prefix string) string {
	now := time.Now().UTC()
	return fmt.Sprintf("%s%sN%09d", prefix, now.Format("20060102150405"), now.Nanosecond())
}
