package main

import (
	"net/http"
	"sort"
	"strings"
	"time"
)

func (a *App) handleControlUI(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path == "/favicon.ico" {
		w.WriteHeader(http.StatusNoContent)
		return
	}
	if r.URL.Path != "/" && r.URL.Path != "/ui" && r.URL.Path != "/ui/" {
		http.NotFound(w, r)
		return
	}
	if r.Method != http.MethodGet && r.Method != http.MethodHead {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.Header().Set("Content-Type", "text/html;charset=utf-8")
	w.Header().Set("Cache-Control", "no-store")
	_, _ = w.Write([]byte(controlUIHTML))
}

func (a *App) handleUIAsset(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet && r.Method != http.MethodHead {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	name := strings.TrimPrefix(r.URL.Path, "/__asset/")
	switch name {
	case "huifu-logo.png", "support-groups.png":
	default:
		http.NotFound(w, r)
		return
	}
	data, err := embeddedUIAssets.ReadFile("ui-assets/" + name)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "image/png")
	w.Header().Set("Cache-Control", "public, max-age=86400")
	w.Header().Set("X-Content-Type-Options", "nosniff")
	if r.Method == http.MethodHead {
		return
	}
	_, _ = w.Write(data)
}

func (a *App) uiSnapshot() map[string]any {
	return a.uiSnapshotFor(true)
}

func (a *App) uiSnapshotFor(includeRequestDetails bool) map[string]any {
	a.mu.Lock()
	defer a.mu.Unlock()

	payments := uiPaymentRows(a.payments, 100)
	refunds := uiRefundRows(a.refunds, 100)
	closes := uiCloseRows(a.closes, 100)
	reconciliations := uiReconciliationRows(a.reconciliations, 100)
	events := uiEventRows(a.events, 120)
	notifications := uiNotificationRows(a.notifications, 80)
	webhooks := uiWebhookRows(a.webhooks, 80)
	securityFindings := uiSecurityRows(a.securityFindings, 80)
	requestLogs := uiRequestLogRows(a.requestLogs, 160, includeRequestDetails)

	paymentStateCounts := paymentStateCounts(a.payments)
	refundStateCounts := refundStateCounts(a.refunds)
	closeStateCounts := closeStateCounts(a.closes)

	return map[string]any{
		"ready": map[string]any{
			"ok":                   true,
			"name":                 appName,
			"version":              appVersion,
			"skill_source":         skillSource,
			"sandbox_skill_source": sandboxSkillSource,
			"contract_bundle":      contractBundle,
			"contract_digest":      a.bundle.Digest,
			"run_id":               a.runID,
			"started_at":           a.startedAt.Format(time.RFC3339Nano),
			"uptime_seconds":       int(time.Since(a.startedAt).Seconds()),
			"mode":                 a.mode,
			"credential_profile":   firstNonEmpty(a.creds.ProfileName, "synthetic"),
			"signature_model":      firstNonEmpty(a.creds.SignatureModel, "synthetic-dual-key"),
			"control_url":          a.controlBaseURL,
			"gateway_url":          a.gatewayBaseURL,
			"update_index_url":     a.updateIndexURL,
			"data_dir":             a.dataDir,
			"report_dir":           a.reportDir,
			"detail_level":         uiDetailLevel(includeRequestDetails),
			"webhook_target_count": len(a.webhookTargets),
			"webhook_targets":      redactedTargets(a.webhookTargets),
		},
		"profile": credentialProfileSummary(a.creds),
		"counts": map[string]int{
			"payments":          len(a.payments),
			"refunds":           len(a.refunds),
			"closes":            len(a.closes),
			"reconciliations":   len(a.reconciliations),
			"events":            len(a.events),
			"notifications":     len(a.notifications),
			"webhooks":          len(a.webhooks),
			"security_findings": len(a.securityFindings),
			"request_logs":      len(a.requestLogs),
		},
		"payment_state_counts": paymentStateCounts,
		"refund_state_counts":  refundStateCounts,
		"close_state_counts":   closeStateCounts,
		"payments":             payments,
		"refunds":              refunds,
		"closes":               closes,
		"reconciliations":      reconciliations,
		"request_logs":         requestLogs,
		"events":               events,
		"notifications":        notifications,
		"webhooks":             webhooks,
		"security_findings":    securityFindings,
	}
}

func redactedTargets(targets []string) []string {
	out := make([]string, 0, len(targets))
	for _, target := range targets {
		out = append(out, redactTarget(target))
	}
	return out
}

func uiDetailLevel(includeRequestDetails bool) string {
	if includeRequestDetails {
		return "admin"
	}
	return "summary"
}

func paymentStateCounts(payments map[string]*Payment) map[string]int {
	counts := map[string]int{}
	for _, payment := range payments {
		if payment != nil {
			counts[payment.State]++
		}
	}
	return counts
}

func refundStateCounts(refunds map[string]*RefundOperation) map[string]int {
	counts := map[string]int{}
	for _, refund := range refunds {
		if refund != nil {
			counts[refund.State]++
		}
	}
	return counts
}

func closeStateCounts(closes map[string]*CloseOperation) map[string]int {
	counts := map[string]int{}
	for _, closeOp := range closes {
		if closeOp != nil {
			counts[closeOp.State]++
		}
	}
	return counts
}

func uiPaymentRows(payments map[string]*Payment, limit int) []map[string]any {
	keys := make([]string, 0, len(payments))
	for key := range payments {
		keys = append(keys, key)
	}
	sort.Sort(sort.Reverse(sort.StringSlice(keys)))
	if len(keys) > limit {
		keys = keys[:limit]
	}
	rows := make([]map[string]any, 0, len(keys))
	for _, key := range keys {
		payment := payments[key]
		if payment == nil {
			continue
		}
		rows = append(rows, map[string]any{
			"kind":             payment.Kind,
			"req_date":         payment.ReqDate,
			"req_seq_id":       payment.ReqSeqID,
			"huifu_id":         payment.HuifuID,
			"hf_seq_id":        payment.HFSeqID,
			"pre_order_id":     payment.PreOrderID,
			"trade_type":       firstNonEmpty(payment.TradeType, payment.PreOrderType),
			"trans_amt":        payment.TransAmt,
			"refundable_amt":   payment.RefundableAmt,
			"state":            payment.State,
			"query_count":      payment.QueryCount,
			"notified":         payment.Notified,
			"webhooked":        payment.Webhooked,
			"business_variant": payment.BusinessVariant,
			"notify_url":       redactTarget(payment.NotifyURL),
			"delivery_actions": payment.ReqSeqID,
		})
	}
	return rows
}

func uiRefundRows(refunds map[string]*RefundOperation, limit int) []map[string]any {
	keys := make([]string, 0, len(refunds))
	for key := range refunds {
		keys = append(keys, key)
	}
	sort.Sort(sort.Reverse(sort.StringSlice(keys)))
	if len(keys) > limit {
		keys = keys[:limit]
	}
	rows := make([]map[string]any, 0, len(keys))
	for _, key := range keys {
		refund := refunds[key]
		if refund == nil {
			continue
		}
		rows = append(rows, map[string]any{
			"kind":               refund.Kind,
			"req_date":           refund.ReqDate,
			"req_seq_id":         refund.ReqSeqID,
			"huifu_id":           refund.HuifuID,
			"hf_seq_id":          refund.HFSeqID,
			"payment_req_seq_id": refund.PaymentReqSeqID,
			"ord_amt":            refund.OrdAmt,
			"state":              refund.State,
			"query_count":        refund.QueryCount,
			"settled":            refund.Settled,
			"settled_status":     refundCompletionLabel(refund),
			"notified":           refund.Notified,
			"webhooked":          refund.Webhooked,
			"business_variant":   refund.BusinessVariant,
			"notify_url":         redactTarget(refund.NotifyURL),
			"delivery_actions":   refund.ReqSeqID,
		})
	}
	return rows
}

func refundCompletionLabel(refund *RefundOperation) string {
	if refund == nil {
		return "未完成"
	}
	if refund.Settled || strings.EqualFold(refund.State, "S") {
		return "已完成"
	}
	switch strings.ToUpper(refund.State) {
	case "F":
		return "失败"
	case "P":
		return "处理中"
	}
	return "未完成"
}

func uiCloseRows(closes map[string]*CloseOperation, limit int) []map[string]any {
	keys := make([]string, 0, len(closes))
	for key := range closes {
		keys = append(keys, key)
	}
	sort.Sort(sort.Reverse(sort.StringSlice(keys)))
	if len(keys) > limit {
		keys = keys[:limit]
	}
	rows := make([]map[string]any, 0, len(keys))
	for _, key := range keys {
		closeOp := closes[key]
		if closeOp == nil {
			continue
		}
		rows = append(rows, map[string]any{
			"kind":               closeOp.Kind,
			"req_date":           closeOp.ReqDate,
			"req_seq_id":         closeOp.ReqSeqID,
			"huifu_id":           closeOp.HuifuID,
			"payment_req_seq_id": closeOp.PaymentReqSeqID,
			"state":              closeOp.State,
			"query_count":        closeOp.QueryCount,
			"notify_url":         redactTarget(closeOp.NotifyURL),
			"notified":           closeOp.Notified,
			"webhooked":          closeOp.Webhooked,
			"business_variant":   closeOp.BusinessVariant,
			"delivery_actions":   closeOp.ReqSeqID,
		})
	}
	return rows
}

func uiReconciliationRows(files map[string]*ReconciliationFile, limit int) []map[string]any {
	keys := make([]string, 0, len(files))
	for key := range files {
		keys = append(keys, key)
	}
	sort.Sort(sort.Reverse(sort.StringSlice(keys)))
	if len(keys) > limit {
		keys = keys[:limit]
	}
	rows := make([]map[string]any, 0, len(keys))
	for _, key := range keys {
		file := files[key]
		if file == nil {
			continue
		}
		rows = append(rows, map[string]any{
			"id":              file.ID,
			"huifu_id":        file.HuifuID,
			"file_date":       file.FileDate,
			"bill_type":       file.BillType,
			"file_name":       file.FileName,
			"task_stat":       file.TaskStat,
			"ready":           file.Ready,
			"query_count":     file.QueryCount,
			"row_count":       file.RowCount,
			"download_status": file.DownloadStatus,
			"download_url":    redactTarget(file.DownloadURL),
		})
	}
	return rows
}

func uiEventRows(events []Event, limit int) []map[string]any {
	start := 0
	if len(events) > limit {
		start = len(events) - limit
	}
	rows := make([]map[string]any, 0, len(events)-start)
	for i := len(events) - 1; i >= start; i-- {
		event := events[i]
		rows = append(rows, map[string]any{
			"time":        event.Time,
			"type":        event.Type,
			"endpoint":    sanitizePlainLogText(event.Endpoint),
			"entity_id":   sanitizePlainLogText(event.EntityID),
			"scenario_id": sanitizePlainLogText(event.ScenarioID),
			"details":     uiSanitizeMap(event.Details),
		})
	}
	return rows
}

func uiNotificationRows(deliveries []NotificationDelivery, limit int) []map[string]any {
	start := 0
	if len(deliveries) > limit {
		start = len(deliveries) - limit
	}
	rows := make([]map[string]any, 0, len(deliveries)-start)
	for i := len(deliveries) - 1; i >= start; i-- {
		delivery := deliveries[i]
		rows = append(rows, map[string]any{
			"id":                 delivery.ID,
			"time":               delivery.Time,
			"payment_req_seq_id": delivery.PaymentReqSeqID,
			"target":             firstNonEmpty(delivery.TargetRedacted, redactTarget(delivery.Target)),
			"status":             delivery.Status,
			"duplicate":          delivery.Duplicate,
			"attempts":           len(delivery.Attempts),
			"error":              sanitizePlainLogText(delivery.Error),
			"diagnosis":          sanitizePlainLogText(delivery.Diagnosis),
		})
	}
	return rows
}

func uiWebhookRows(deliveries []WebhookDelivery, limit int) []map[string]any {
	start := 0
	if len(deliveries) > limit {
		start = len(deliveries) - limit
	}
	rows := make([]map[string]any, 0, len(deliveries)-start)
	for i := len(deliveries) - 1; i >= start; i-- {
		delivery := deliveries[i]
		rows = append(rows, map[string]any{
			"id":         delivery.ID,
			"time":       delivery.Time,
			"event_type": delivery.EventType,
			"entity_id":  delivery.EntityID,
			"target":     firstNonEmpty(delivery.TargetRedacted, redactTarget(delivery.Target)),
			"status":     delivery.Status,
			"attempts":   len(delivery.Attempts),
			"error":      sanitizePlainLogText(delivery.Error),
			"diagnosis":  sanitizePlainLogText(delivery.Diagnosis),
		})
	}
	return rows
}

func uiSecurityRows(findings []SecurityFinding, limit int) []map[string]any {
	start := 0
	if len(findings) > limit {
		start = len(findings) - limit
	}
	rows := make([]map[string]any, 0, len(findings)-start)
	for i := len(findings) - 1; i >= start; i-- {
		finding := findings[i]
		rows = append(rows, map[string]any{
			"time":     finding.Time,
			"type":     finding.Type,
			"severity": finding.Severity,
			"target":   firstNonEmpty(finding.TargetRedacted, redactTarget(finding.Target)),
			"reason":   finding.Reason,
		})
	}
	return rows
}

func uiRequestLogRows(logs []RequestLog, limit int, includeDetails bool) []map[string]any {
	start := 0
	if len(logs) > limit {
		start = len(logs) - limit
	}
	rows := make([]map[string]any, 0, len(logs)-start)
	for i := len(logs) - 1; i >= start; i-- {
		log := logs[i]
		row := map[string]any{
			"id":                  log.ID,
			"time":                log.Time,
			"method":              log.Method,
			"path":                log.Path,
			"kind":                log.Kind,
			"http_status":         log.HTTPStatus,
			"resp_code":           log.RespCode,
			"resp_desc":           log.RespDesc,
			"req_seq_id":          log.ReqSeqID,
			"huifu_id":            log.HuifuID,
			"product_id":          log.ProductID,
			"sys_id":              log.SysID,
			"signature_status":    log.SignatureStatus,
			"request_data_status": log.RequestDataStatus,
			"detail_available":    includeDetails,
			"actions":             log.ID,
		}
		if includeDetails {
			row["request_envelope"] = uiSanitizeMap(log.RequestEnvelope)
			row["request_data"] = uiSanitizeMap(log.RequestData)
			row["response_envelope"] = uiSanitizeMap(log.ResponseEnvelope)
			row["response_data"] = uiSanitizeMap(log.ResponseData)
			row["response_body"] = sanitizePlainLogText(log.ResponseBody)
		}
		rows = append(rows, row)
	}
	return rows
}

func uiSanitizeMap(in map[string]any) map[string]any {
	if len(in) == 0 {
		return nil
	}
	out := make(map[string]any, len(in))
	for key, value := range in {
		out[key] = sanitizeGatewayLogValue(key, value, 0)
	}
	return out
}

func uiSanitizeValue(value any) any {
	switch typed := value.(type) {
	case string:
		if strings.Contains(typed, "://") {
			return redactTarget(typed)
		}
		return typed
	case map[string]any:
		return uiSanitizeMap(typed)
	case []any:
		out := make([]any, len(typed))
		for i, item := range typed {
			out[i] = uiSanitizeValue(item)
		}
		return out
	default:
		return typed
	}
}

const controlUIHTML = `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>汇付支付本地沙箱服务</title>
<style>
:root {
  color-scheme: light;
  --bg: #f7f8f7;
  --surface: #ffffff;
  --line: #d9dedb;
  --text: #1b1f1d;
  --muted: #66706b;
  --accent: #0f766e;
  --accent-2: #9a3412;
  --support: #165dff;
  --danger: #b91c1c;
  --warning: #b45309;
  --ok: #15803d;
  --pending: #7c3aed;
  --shadow: 0 8px 24px rgba(24, 33, 28, 0.08);
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Source Han Sans SC", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
  letter-spacing: 0;
}
body.modal-open { overflow: hidden; }
button, input { font: inherit; }
.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 16px;
  align-items: center;
  min-height: 72px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.96);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(10px);
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}
.brand-logo {
  width: 44px;
  height: 44px;
  flex: 0 0 44px;
  object-fit: contain;
  border-radius: 8px;
  background: #fff;
  border: 1px solid #edf0ee;
}
.brand-copy {
  display: grid;
  gap: 3px;
  min-width: 0;
}
.brand h1 {
  margin: 0;
  font-size: 20px;
  line-height: 1.2;
  font-weight: 700;
}
.brand span {
  color: var(--muted);
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.toolbar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  flex-wrap: wrap;
}
.token {
  width: 230px;
  max-width: 42vw;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px 10px;
  background: var(--surface);
}
.btn {
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px 11px;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
}
.btn:disabled {
  cursor: not-allowed;
  opacity: 0.62;
}
.btn.small {
  padding: 5px 8px;
  font-size: 12px;
  line-height: 1.2;
}
.btn:hover { border-color: var(--accent); color: var(--accent); }
.btn:focus-visible,
.tab:focus-visible,
.token:focus-visible,
.config-input:focus-visible {
  outline: 2px solid rgba(15, 118, 110, 0.35);
  outline-offset: 2px;
}
.btn.primary {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}
.btn.danger {
  border-color: #e7b4b4;
  color: var(--danger);
}
.btn.support {
  border-color: #b9c8ff;
  color: #0f4bd8;
  background: #f5f8ff;
}
.btn.support:hover {
  border-color: var(--support);
  color: var(--support);
}
.toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--muted);
  font-size: 13px;
}
main { padding: 20px 24px 36px; }
.statusline {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(320px, 1fr);
  gap: 16px;
  margin-bottom: 18px;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow);
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--line);
}
.panel-header h2 {
  margin: 0;
  font-size: 15px;
  line-height: 1.3;
}
.panel-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  flex-wrap: wrap;
}
.panel-body { padding: 14px 16px; }
.kv {
  display: grid;
  grid-template-columns: 150px minmax(0, 1fr);
  gap: 8px 12px;
  font-size: 13px;
}
.kv div:nth-child(odd) { color: var(--muted); }
code, .mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 12px;
}
.integration-kv {
	display: grid;
	grid-template-columns: 156px minmax(0, 1fr);
	gap: 8px 12px;
	font-size: 13px;
}
.integration-kv div:nth-child(odd) { color: var(--muted); }
.webhook-config {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
}
.webhook-config label {
  display: block;
  margin-bottom: 6px;
  color: var(--muted);
  font-size: 13px;
}
.webhook-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
}
.update-box {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
}
.update-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.update-title {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
}
.update-detail,
.update-meta {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.5;
}
.update-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}
.update-actions a.btn {
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}
.config-input {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px 10px;
  background: var(--surface);
  color: var(--text);
}
.metrics {
	display: grid;
	grid-template-columns: repeat(7, minmax(116px, 1fr));
	gap: 10px;
	margin-bottom: 18px;
}
.metric {
	background: var(--surface);
	border: 1px solid var(--line);
	border-radius: 8px;
	padding: 12px;
	min-height: 112px;
}
.metric b {
	display: block;
	font-size: 24px;
	line-height: 1;
  margin-bottom: 6px;
}
.metric span {
	color: var(--muted);
	font-size: 12px;
}
.metric-head {
	display: flex;
	align-items: baseline;
	justify-content: space-between;
	gap: 8px;
	margin-bottom: 10px;
}
.metric-head b {
	margin-bottom: 0;
}
.metric-title {
	color: var(--muted);
	font-size: 12px;
	white-space: nowrap;
}
.metric-subgrid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 6px;
}
.metric-sub {
	min-width: 0;
	border-top: 1px solid #edf0ee;
	padding-top: 7px;
}
.metric-sub strong {
	display: block;
	font-size: 14px;
	line-height: 1.1;
}
.metric-sub span {
	display: block;
	margin-top: 3px;
	white-space: nowrap;
}
.workspace {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  overflow: hidden;
  box-shadow: var(--shadow);
}
.workspace-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  background: #fbfcfb;
}
.workspace-panel {
  border: 0;
  border-radius: 0;
  box-shadow: none;
}
.workspace-panel[hidden] { display: none; }
.workspace-panel .panel-header {
  border-top: 0;
}
.tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.tab {
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #f9faf9;
  padding: 6px 9px;
  cursor: pointer;
  color: var(--muted);
  font-size: 13px;
}
.tab.active {
  background: #eef8f6;
  border-color: #8ed1c9;
  color: var(--accent);
}
.table-wrap {
  overflow-x: auto;
}
.table-wrap.request-log-table td:last-child,
.table-wrap.request-log-table th:last-child {
  position: sticky;
  right: 0;
  background: var(--surface);
  box-shadow: -8px 0 12px rgba(255, 255, 255, 0.88);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
th, td {
  padding: 10px 9px;
  border-bottom: 1px solid #edf0ee;
  text-align: left;
  vertical-align: top;
}
th {
  color: var(--muted);
  font-weight: 600;
  background: #fbfcfb;
  white-space: nowrap;
}
td { min-width: 72px; }
.empty {
  color: var(--muted);
  padding: 18px 0;
  font-size: 13px;
}
.pill {
  display: inline-flex;
  align-items: center;
  min-height: 22px;
  padding: 2px 7px;
  border-radius: 999px;
  border: 1px solid var(--line);
  font-size: 12px;
  white-space: nowrap;
}
.pill.ok { color: var(--ok); border-color: #9bd5ad; background: #f1fbf3; }
.pill.pending { color: var(--pending); border-color: #c8b5f4; background: #f7f3ff; }
.pill.warn { color: var(--warning); border-color: #e9c58d; background: #fff7ed; }
.pill.bad { color: var(--danger); border-color: #efb0b0; background: #fff5f5; }
.details {
  max-width: 480px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.delivery-actions {
  display: flex;
  min-width: 300px;
  gap: 8px;
  flex-wrap: wrap;
}
.delivery-group {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px;
  border: 1px solid #e1e8e4;
  border-radius: 6px;
  background: #fbfcfb;
}
.delivery-group span {
  padding: 0 4px;
  color: var(--muted);
  font-size: 12px;
  white-space: nowrap;
}
.btn.mini {
  min-height: 26px;
  padding: 3px 7px;
  font-size: 12px;
}
.btn[disabled] {
  cursor: not-allowed;
  opacity: 0.52;
}
.notice {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.5;
}
.toast {
  position: fixed;
  right: 18px;
  bottom: 74px;
  max-width: min(420px, calc(100vw - 36px));
  border-radius: 8px;
  border: 1px solid var(--line);
  background: var(--surface);
  box-shadow: var(--shadow);
  padding: 12px 14px;
  color: var(--text);
  display: none;
  z-index: 20;
}
.toast.show { display: block; }
.toast.bad {
  border-color: #efb0b0;
  background: #fff5f5;
  color: var(--danger);
}
.float-top {
  position: fixed;
  right: 18px;
  bottom: 18px;
  z-index: 18;
  width: 42px;
  height: 42px;
  border: 1px solid #9ccfc6;
  border-radius: 50%;
  background: #ffffff;
  color: var(--accent);
  box-shadow: var(--shadow);
  cursor: pointer;
  font-size: 20px;
  line-height: 1;
}
.modal[hidden] { display: none; }
.modal {
  position: fixed;
  inset: 0;
  z-index: 40;
  display: grid;
  place-items: center;
  padding: 24px;
}
.modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(13, 20, 17, 0.42);
}
.support-dialog {
  position: relative;
  width: min(620px, calc(100vw - 32px));
  max-height: calc(100vh - 48px);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: 0 18px 50px rgba(24, 33, 28, 0.18);
}
.usage-dialog {
  position: relative;
  width: min(920px, calc(100vw - 32px));
  max-height: calc(100vh - 48px);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: 0 18px 50px rgba(24, 33, 28, 0.18);
}
.declaration-dialog {
  position: relative;
  width: min(720px, calc(100vw - 32px));
  max-height: calc(100vh - 48px);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: 0 18px 50px rgba(24, 33, 28, 0.18);
}
.log-dialog {
  position: relative;
  width: min(1040px, calc(100vw - 32px));
  max-height: calc(100vh - 48px);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: 0 18px 50px rgba(24, 33, 28, 0.18);
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
}
.modal-header h2 {
  margin: 0;
  font-size: 15px;
  line-height: 1.3;
}
.support-image-wrap {
  overflow: auto;
  padding: 10px;
  background: #f7f9fb;
}
.support-image {
  display: block;
  width: 100%;
  height: auto;
  max-height: calc(100vh - 128px);
  object-fit: contain;
}
.usage-body {
  overflow: auto;
  padding: 16px;
}
.usage-body h3 {
  margin: 18px 0 8px;
  font-size: 14px;
}
.usage-body h3:first-child { margin-top: 0; }
.usage-list {
  margin: 0;
  padding-left: 20px;
  color: var(--text);
  font-size: 13px;
  line-height: 1.7;
}
.usage-note {
  margin: 10px 0 0;
  padding: 10px 12px;
  border: 1px solid #dbe7e2;
  border-radius: 6px;
  background: #fbfdfc;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.6;
}
.declaration-body {
  overflow: auto;
  padding: 16px;
}
.declaration-body p {
  margin: 0 0 10px;
  color: var(--text);
  font-size: 13px;
  line-height: 1.7;
}
.declaration-body ul {
  margin: 0;
  padding-left: 20px;
  color: var(--text);
  font-size: 13px;
  line-height: 1.75;
}
.declaration-check {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--muted);
  font-size: 13px;
}
.declaration-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  border-top: 1px solid var(--line);
}
.declaration-buttons {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  flex-wrap: wrap;
}
.decline-message {
  padding: 16px;
  color: var(--danger);
  font-size: 13px;
  line-height: 1.6;
}
.log-body {
  overflow: auto;
  padding: 16px;
}
.log-summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(140px, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}
.log-summary-item {
  min-width: 0;
  border: 1px solid #e5ebe8;
  border-radius: 6px;
  padding: 9px 10px;
  background: #fbfcfb;
}
.log-summary-item span {
  display: block;
  margin-bottom: 5px;
  color: var(--muted);
  font-size: 12px;
}
.log-summary-item b {
  display: block;
  overflow-wrap: anywhere;
  font-size: 13px;
  font-weight: 600;
}
.json-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.json-block {
  min-width: 0;
  border: 1px solid #e1e8e4;
  border-radius: 8px;
  overflow: hidden;
  background: #fcfdfc;
}
.json-block.wide {
  grid-column: 1 / -1;
}
.json-block h3 {
  margin: 0;
  padding: 10px 12px;
  border-bottom: 1px solid #edf0ee;
  background: #f7faf8;
  font-size: 13px;
}
.json-block pre {
  margin: 0;
  min-height: 160px;
  max-height: 340px;
  overflow: auto;
  padding: 12px;
  color: #18211c;
  font-size: 12px;
  line-height: 1.55;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.locked-detail {
  padding: 16px;
  border: 1px dashed #d9dedb;
  border-radius: 8px;
  background: #fbfcfb;
  color: var(--muted);
  font-size: 13px;
}
.flow {
  display: grid;
  grid-template-columns: repeat(5, minmax(110px, 1fr));
  gap: 8px;
  align-items: stretch;
  margin-top: 10px;
}
.flow-step {
  position: relative;
  min-height: 78px;
  padding: 10px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #fbfcfb;
  font-size: 12px;
  line-height: 1.45;
}
.flow-step b {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
}
.flow-step::after {
  content: ">";
  position: absolute;
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--muted);
}
.flow-step:last-child::after { content: ""; }
@media (max-width: 1180px) {
  .metrics { grid-template-columns: repeat(4, minmax(110px, 1fr)); }
  .statusline { grid-template-columns: 1fr; }
  .flow { grid-template-columns: 1fr; }
  .flow-step::after { content: ""; }
}
@media (max-width: 720px) {
  .topbar { grid-template-columns: 1fr; padding: 12px 14px; }
  main { padding: 14px; }
  .brand h1 { font-size: 18px; }
  .toolbar {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    justify-content: stretch;
    width: 100%;
  }
  .toolbar .toggle,
  .toolbar .token {
    grid-column: 1 / -1;
  }
  .toolbar .btn { width: 100%; }
  .token { width: 100%; max-width: none; }
  .metrics { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
  .kv { grid-template-columns: 1fr; }
  .integration-kv { grid-template-columns: 1fr; }
  .panel-actions { justify-content: flex-start; width: 100%; }
  .panel-actions .btn { flex: 1 1 130px; }
  .modal { padding: 12px; }
  .support-dialog { width: calc(100vw - 24px); max-height: calc(100vh - 24px); }
  .usage-dialog { width: calc(100vw - 24px); max-height: calc(100vh - 24px); }
  .declaration-dialog { width: calc(100vw - 24px); max-height: calc(100vh - 24px); }
  .declaration-actions { align-items: stretch; flex-direction: column; }
  .declaration-buttons { width: 100%; justify-content: stretch; }
  .declaration-buttons .btn { flex: 1 1 120px; }
  .log-dialog { width: calc(100vw - 24px); max-height: calc(100vh - 24px); }
  .support-image { max-height: calc(100vh - 104px); }
  .log-summary { grid-template-columns: 1fr; }
  .json-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<header class="topbar">
  <div class="brand">
    <img class="brand-logo" src="/__asset/huifu-logo.png" alt="汇付天下">
    <div class="brand-copy">
      <h1>汇付支付本地沙箱服务</h1>
      <span id="subtitle">connecting...</span>
    </div>
  </div>
  <div class="toolbar">
    <label class="toggle"><input id="autoRefresh" type="checkbox" checked> 自动刷新</label>
    <input id="adminToken" class="token" type="password" autocomplete="off" placeholder="admin token">
    <button id="refreshBtn" class="btn" title="刷新状态">↻ 刷新</button>
    <button id="reportBtn" class="btn primary" title="生成报告">生成报告</button>
    <button id="shutdownBtn" class="btn danger" title="停止沙箱">停止</button>
    <button id="usageBtn" class="btn" title="使用说明">使用说明</button>
    <button id="supportBtn" class="btn support" title="技术支持">支持</button>
  </div>
</header>

<main>
  <section class="statusline">
    <div class="panel">
      <div class="panel-header">
        <h2>接入信息</h2>
        <span id="liveState" class="pill pending">loading</span>
      </div>
      <div class="panel-body">
        <div class="kv" id="runtimeKV"></div>
        <div class="update-box" id="updateBox" aria-label="版本更新">
          <div class="update-head">
            <div>
              <b class="update-title">版本更新</b>
              <p class="update-detail" id="updateDetail">尚未检查更新。</p>
            </div>
            <span id="updateStatus" class="pill pending">未检查</span>
          </div>
          <div class="update-actions" id="updateActions">
            <button id="checkUpdateBtn" class="btn" type="button" title="检查本地沙箱最新版本">检查更新</button>
          </div>
          <p class="update-meta mono" id="updateMeta"></p>
        </div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header">
        <h2>项目接入配置</h2>
        <div class="panel-actions">
          <button id="exportCredentialsBtn" class="btn primary" title="导出 sandbox-credentials.json">导出凭证</button>
          <button id="copyProjectConfigBtn" class="btn" title="复制接入配置">⧉ 复制配置</button>
          <button id="showWebhookKeyBtn" class="btn" title="显示 Webhook 验签密钥">显示 Webhook Key</button>
        </div>
      </div>
      <div class="panel-body">
        <div class="integration-kv" id="integrationKV"></div>
        <div class="webhook-config" aria-label="Webhook 目标配置">
          <label for="webhookTargetInput">Webhook 目标地址</label>
          <div class="webhook-row">
            <input id="webhookTargetInput" class="config-input" type="url" autocomplete="off" inputmode="url" placeholder="http://127.0.0.1:18081/webhook">
            <button id="saveWebhookTargetBtn" class="btn" type="button" title="保存本次运行的 Webhook 目标">保存 Webhook</button>
          </div>
          <p id="webhookTargetHint" class="notice">未配置 Webhook 目标时，业务状态里的 Webhook 按钮会禁用。</p>
        </div>
        <p class="notice">页面不展示完整私钥。<code>webhook_endpoint_key</code> 需输入 <code>admin_token</code> 后显示、复制或导出，用于客户项目验证本地沙箱 Webhook 签名。</p>
      </div>
    </div>
  </section>

  <section class="metrics" id="metrics"></section>

  <section class="workspace" aria-label="沙箱工作区">
    <div class="workspace-tabs" id="workspaceTabs" role="tablist" aria-label="工作区标签">
      <button class="tab active" type="button" data-workspace-view="business">业务状态</button>
      <button class="tab" type="button" data-workspace-view="logs">请求日志</button>
      <button class="tab" type="button" data-workspace-view="events">事件流</button>
      <button class="tab" type="button" data-workspace-view="ops">通知与安全</button>
    </div>

    <div class="panel workspace-panel" data-workspace-panel="business">
      <div class="panel-header">
        <h2>业务状态</h2>
        <div class="tabs" id="businessTabs">
          <button class="tab active" type="button" data-view="payments">支付</button>
          <button class="tab" type="button" data-view="refunds">退款</button>
          <button class="tab" type="button" data-view="closes">关单</button>
          <button class="tab" type="button" data-view="reconciliations">对账</button>
        </div>
      </div>
      <div class="panel-body">
        <div class="table-wrap" id="businessTable"></div>
      </div>
    </div>

    <div class="panel workspace-panel" data-workspace-panel="logs" hidden>
      <div class="panel-header">
        <h2>请求日志</h2>
        <span class="notice">点击详情查看入参与响应参数</span>
      </div>
      <div class="panel-body">
        <div class="table-wrap request-log-table" id="requestLogTable"></div>
      </div>
    </div>

    <div class="panel workspace-panel" data-workspace-panel="events" hidden>
      <div class="panel-header">
        <h2>事件流</h2>
        <span class="notice">最新事件在上方</span>
      </div>
      <div class="panel-body">
        <div class="table-wrap" id="eventTable"></div>
      </div>
    </div>

    <div class="panel workspace-panel" data-workspace-panel="ops" hidden>
      <div class="panel-header">
        <h2>通知与安全</h2>
        <div class="tabs" id="opsTabs">
          <button class="tab active" type="button" data-view="notifications">Notify</button>
          <button class="tab" type="button" data-view="webhooks">Webhook</button>
          <button class="tab" type="button" data-view="security_findings">安全发现</button>
        </div>
      </div>
      <div class="panel-body">
        <div class="table-wrap" id="opsTable"></div>
      </div>
    </div>
  </section>
</main>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<button id="scrollTopBtn" class="float-top" type="button" title="回到顶部" aria-label="回到顶部">↑</button>
<div id="declarationModal" class="modal" role="dialog" aria-modal="true" aria-labelledby="declarationTitle" hidden>
  <div class="modal-backdrop"></div>
  <section class="declaration-dialog">
    <div class="modal-header">
      <h2 id="declarationTitle">本地沙箱服务使用声明</h2>
    </div>
    <div class="declaration-body" id="declarationBody">
      <p>欢迎使用汇付支付本地沙箱服务。该服务用于开发阶段的本地协议模拟、场景演练、SDK sample 检查和自检报告生成，不创建真实交易，不发生真实资金流转。</p>
      <ul>
        <li>本地沙箱通过不代表汇付官方联调通过，也不代表具备生产上线条件。</li>
        <li>本地沙箱不验证真实商户权限、通道开通、费率、风控、清结算、资金结果或生产路由。</li>
        <li>请勿在本地沙箱、报告、截图、工单或聊天窗口中填写、上传或传播真实生产私钥、真实用户敏感信息、真实订单流水或生产回调地址。</li>
        <li>页面导出的凭证仅用于本机沙箱模拟；正式联调或生产环境应使用官方流程下发的真实凭证和证书材料。</li>
        <li>检查更新只读取公开版本索引，不上传本地凭证、请求日志、报告、Webhook 地址或 Notify 地址。</li>
      </ul>
      <p class="usage-note">选择“我已知晓并同意”后继续使用；选择“拒绝”将停止当前本地沙箱服务并尝试关闭本页面。</p>
    </div>
    <div class="declaration-actions">
      <label class="declaration-check"><input id="declarationDontShow" type="checkbox" checked> 不再提示</label>
      <div class="declaration-buttons">
        <button id="declineDeclarationBtn" class="btn danger" type="button">拒绝</button>
        <button id="acceptDeclarationBtn" class="btn primary" type="button">我已知晓并同意</button>
      </div>
    </div>
  </section>
</div>
<div id="logDetailModal" class="modal" role="dialog" aria-modal="true" aria-labelledby="logDetailTitle" hidden>
  <div class="modal-backdrop" data-close-log-detail></div>
  <section class="log-dialog">
    <div class="modal-header">
      <h2 id="logDetailTitle">请求日志详情</h2>
      <div class="panel-actions">
        <button id="copyLogDetailBtn" class="btn" type="button">复制 JSON</button>
        <button id="logDetailCloseBtn" class="btn" type="button" aria-label="关闭">×</button>
      </div>
    </div>
    <div class="log-body">
      <div class="log-summary" id="logDetailSummary"></div>
      <div class="json-grid">
        <section class="json-block">
          <h3>入参 data</h3>
          <pre id="logRequestJson"></pre>
        </section>
        <section class="json-block">
          <h3>响应 data</h3>
          <pre id="logResponseJson"></pre>
        </section>
        <section class="json-block wide">
          <h3>信封与签名摘要</h3>
          <pre id="logEnvelopeJson"></pre>
        </section>
      </div>
    </div>
  </section>
</div>
<div id="supportModal" class="modal" role="dialog" aria-modal="true" aria-labelledby="supportTitle" hidden>
  <div class="modal-backdrop" data-close-support></div>
  <section class="support-dialog">
    <div class="modal-header">
      <h2 id="supportTitle">技术支持</h2>
      <button id="supportCloseBtn" class="btn" type="button" aria-label="关闭">×</button>
    </div>
    <div class="support-image-wrap">
      <img class="support-image" src="/__asset/support-groups.png" alt="加入对应微信群或企业微信群获得专属技术支持">
    </div>
  </section>
</div>
<div id="usageModal" class="modal" role="dialog" aria-modal="true" aria-labelledby="usageTitle" hidden>
  <div class="modal-backdrop" data-close-usage></div>
  <section class="usage-dialog">
    <div class="modal-header">
      <h2 id="usageTitle">使用说明</h2>
      <button id="usageCloseBtn" class="btn" type="button" aria-label="关闭">×</button>
    </div>
    <div class="usage-body">
      <h3>页面功能说明</h3>
      <ol class="usage-list">
        <li>“接入信息”展示当前沙箱运行编号、模式、凭证档案、签名模型、控制台地址和报告目录，用于确认当前服务实例。</li>
        <li>“项目接入配置”展示客户项目需要配置的网关地址、系统号、产品号、汇付 ID 示例、请求签名私钥字段和响应验签公钥字段。</li>
        <li>顶部指标卡中支付、退款、关单的主数字为总数，下方只展示成功、处理中和失败数量；退款失败多数是失败响应，不一定形成退款业务记录，关单成功可能使原支付进入失败状态。</li>
        <li>“业务状态”“请求日志”“事件流”“通知与安全”使用标签页切换；业务状态内可按支付、退款、关单和对账查看本地演练记录。</li>
        <li>请求日志详情里的“信封与签名摘要”只展示摘要，不展示原始 sign；如果看到 <code>invalid_envelope</code>、<code>sign_status=missing</code> 或 <code>missing_fields</code>，通常表示客户项目没有按 <code>sys_id/product_id/sign/data</code> envelope 发送请求。</li>
        <li>托管支付记录可点击“模拟成功”，用于模拟用户完成托管收银台支付；项目再次查单会得到成功状态。</li>
        <li>支付、退款和关单记录可手动触发成功或失败 Notify；支付、退款和关单记录也可手动触发成功或失败 Webhook。没有 notify_url 或未配置 Webhook 目标时按钮会禁用，Webhook 目标可在“项目接入配置”中填写并保存。</li>
        <li>手动 Notify/Webhook 只发送测试通知并记录投递结果，不会修改业务主记录；“模拟成功”会修改托管支付主记录。Notify 接收方需返回 <code>RECV_ORD_ID_&lt;req_seq_id&gt;</code>，Webhook 接收方需返回任意 HTTP 2xx。</li>
        <li>请求日志详情、导出凭证、复制配置、生成报告、停止服务和手动触发通知都需要输入启动窗口打印的 admin token。</li>
        <li>“通知与安全”用于查看 Notify、Webhook 投递结果和本地安全发现；生成报告前建议先确认这里没有未处理高风险项。</li>
        <li>“版本更新”会读取公开 <code>hf-payment-local-sandbox-latest.json</code> 索引并提示新版下载地址和 SHA256；不会上传本地凭证、日志、报告或回调地址，也不会静默替换当前程序。</li>
      </ol>

      <h3>接入步骤</h3>
      <ol class="usage-list">
        <li>启动本地沙箱后，把 <code>gateway_url</code> 配置到客户项目的 SDK 网关地址、base URL、endpoint 或支付出口层。</li>
        <li>在页面输入启动窗口打印的 <code>admin token</code>，点击“导出凭证”，下载 <code>sandbox-credentials.json</code>。</li>
        <li>把 <code>sys_id</code>、<code>product_id</code>、<code>merchant_private_key</code> 配置到项目请求签名配置中；这是官方 SDK 常用的 PKCS8 Base64 私钥格式，无 PEM 头尾，无换行。</li>
        <li>把 <code>merchant_public_key</code> 配置到项目响应和通知验签公钥中；这是官方 SDK 常用的 X509 Base64 公钥格式，无 PEM 头尾，无换行，由本地沙箱响应签名私钥派生，用来模拟平台响应签名链路。</li>
        <li>如果项目要接 Webhook，把 <code>webhook_endpoint_key</code> 配置到项目 Webhook 终端密钥中；沙箱会用它计算大写 <code>MD5(raw_body + webhook_endpoint_key)</code>，业务侧用同一个值验签。</li>
        <li>把 <code>skill_source</code> 配置为 <code>hfps/1.3.1;sandbox/1.0.1</code>；官方联调或生产环境使用 <code>hfps/1.3.2</code>，不要携带沙箱后缀。</li>
        <li>每笔请求的 <code>data.huifu_id</code> 使用客户自己的汇付 ID；本地样例可使用 <code>6666000100000001</code>。</li>
        <li>如需测试 Webhook，在页面“Webhook 目标地址”中填写本机接收地址，例如 <code>http://127.0.0.1:18081/webhook</code>，保存后业务状态里的 Webhook 按钮会变为可用。</li>
        <li>客户项目建议从后端 SDK、支付出口层或本地开发代理访问 <code>gateway_url</code>；浏览器前端跨 Origin 直连可能被本地安全策略拦截。</li>
      </ol>
      <p class="usage-note"><code>merchant_private_key</code> 和 <code>merchant_public_key</code> 是商户项目需要配置的两项值：前者用于请求加签，后者用于响应和通知验签，不表示同一对 RSA 密钥。</p>
      <p class="usage-note">如果官方 SDK 不能改网关地址，不要改 SDK 源码，也不要用 hosts 劫持官方域名。建议在客户项目的支付出口层增加仅本地启用的 <code>local-sandbox</code> 分支。</p>

      <h3>请求签名流程</h3>
      <div class="flow" aria-label="请求签名流程">
        <div class="flow-step"><b>1. 组装 data</b>业务字段放入 JSON data，包含 huifu_id、req_seq_id 等字段。</div>
        <div class="flow-step"><b>2. 排序序列化</b>按 SDK v2 sorted-json 口径生成 canonical data。</div>
        <div class="flow-step"><b>3. 私钥签名</b>用 merchant_private_key 做 SHA256withRSA 签名。</div>
        <div class="flow-step"><b>4. 组装 envelope</b>发送 sys_id、product_id、sign、data 到 gateway_url。</div>
        <div class="flow-step"><b>5. 沙箱验签</b>沙箱用本机保存的商户请求验签公钥验证签名和 profile 匹配。</div>
      </div>

      <h3>响应验签流程</h3>
      <div class="flow" aria-label="响应验签流程">
        <div class="flow-step"><b>1. 收到响应</b>响应包含 sign 和 data。</div>
        <div class="flow-step"><b>2. 沙箱加签</b>沙箱用本机沙箱私钥生成响应 sign。</div>
        <div class="flow-step"><b>3. 排序序列化</b>对响应 data 使用同一 canonical 口径。</div>
        <div class="flow-step"><b>4. 验证签名</b>商户项目用 merchant_public_key 做 SHA256withRSA verify。</div>
        <div class="flow-step"><b>5. 业务处理</b>验签通过后再处理 resp_code、状态和幂等。</div>
      </div>
    </div>
  </section>
</div>

<script>
(function () {
  var current = null;
  var workspaceView = "business";
  var businessView = "payments";
  var opsView = "notifications";
  var timer = null;
  var updateChecked = false;
  var updateState = null;
  var revealedCredentials = null;
  var declarationStorageKey = "hf_sandbox_declaration_ack_v1";
  var tokenInput = document.getElementById("adminToken");
  var declarationModal = document.getElementById("declarationModal");
  var supportModal = document.getElementById("supportModal");
  var usageModal = document.getElementById("usageModal");
  var logDetailModal = document.getElementById("logDetailModal");
  var activeLogDetail = null;
  var modalFocusReturn = null;
  tokenInput.value = "";

  document.getElementById("usageBtn").addEventListener("click", openUsage);
  document.getElementById("usageCloseBtn").addEventListener("click", closeUsage);
  document.getElementById("acceptDeclarationBtn").addEventListener("click", acceptDeclaration);
  document.getElementById("declineDeclarationBtn").addEventListener("click", declineDeclaration);
  document.getElementById("supportBtn").addEventListener("click", openSupport);
  document.getElementById("supportCloseBtn").addEventListener("click", closeSupport);
  document.getElementById("logDetailCloseBtn").addEventListener("click", closeLogDetail);
  document.getElementById("copyLogDetailBtn").addEventListener("click", copyLogDetail);
  document.getElementById("saveWebhookTargetBtn").addEventListener("click", saveWebhookTarget);
  document.getElementById("scrollTopBtn").addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
  document.getElementById("businessTable").addEventListener("click", function (event) {
    var button = event.target.closest("button[data-delivery-channel]");
    if (button) {
      triggerManualDelivery(button);
      return;
    }
    button = event.target.closest("button[data-hosting-success]");
    if (button) {
      triggerHostingSuccess(button);
    }
  });
  document.getElementById("requestLogTable").addEventListener("click", function (event) {
    var button = event.target.closest("button[data-log-detail]");
    if (!button) return;
    openLogDetail(button.getAttribute("data-log-detail"));
  });
  usageModal.addEventListener("click", function (event) {
    if (event.target && event.target.hasAttribute("data-close-usage")) closeUsage();
  });
  supportModal.addEventListener("click", function (event) {
    if (event.target && event.target.hasAttribute("data-close-support")) closeSupport();
  });
  logDetailModal.addEventListener("click", function (event) {
    if (event.target && event.target.hasAttribute("data-close-log-detail")) closeLogDetail();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !usageModal.hasAttribute("hidden")) closeUsage();
    if (event.key === "Escape" && !supportModal.hasAttribute("hidden")) closeSupport();
    if (event.key === "Escape" && !logDetailModal.hasAttribute("hidden")) closeLogDetail();
    if (event.key === "Tab") trapModalFocus(event);
  });
  document.getElementById("refreshBtn").addEventListener("click", loadState);
  document.getElementById("checkUpdateBtn").addEventListener("click", function () { checkUpdate(true); });
  document.getElementById("reportBtn").addEventListener("click", generateReport);
  document.getElementById("shutdownBtn").addEventListener("click", shutdownSandbox);
  document.getElementById("exportCredentialsBtn").addEventListener("click", exportCredentials);
  document.getElementById("copyProjectConfigBtn").addEventListener("click", copyProjectConfig);
  document.getElementById("showWebhookKeyBtn").addEventListener("click", revealWebhookEndpointKey);
  document.getElementById("autoRefresh").addEventListener("change", configureTimer);
  bindWorkspaceTabs();
  bindTabs("businessTabs", function (view) {
    businessView = view;
    renderBusiness();
  });
  bindTabs("opsTabs", function (view) {
    opsView = view;
    renderOps();
  });

  function bindTabs(id, onChange) {
    var root = document.getElementById(id);
    root.addEventListener("click", function (event) {
      var button = event.target.closest("button[data-view]");
      if (!button) return;
      Array.prototype.forEach.call(root.querySelectorAll(".tab"), function (item) {
        item.classList.toggle("active", item === button);
      });
      onChange(button.getAttribute("data-view"));
    });
  }

  function bindWorkspaceTabs() {
    var root = document.getElementById("workspaceTabs");
    root.addEventListener("click", function (event) {
      var button = event.target.closest("button[data-workspace-view]");
      if (!button) return;
      workspaceView = button.getAttribute("data-workspace-view");
      syncWorkspaceTabs();
    });
  }

  function syncWorkspaceTabs() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-workspace-view]"), function (button) {
      button.classList.toggle("active", button.getAttribute("data-workspace-view") === workspaceView);
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-workspace-panel]"), function (panel) {
      if (panel.getAttribute("data-workspace-panel") === workspaceView) {
        panel.removeAttribute("hidden");
      } else {
        panel.setAttribute("hidden", "");
      }
    });
  }

  function openUsage() {
    openModal(usageModal, "#usageCloseBtn");
  }

  function closeUsage() {
    closeModal(usageModal);
  }

  function openSupport() {
    openModal(supportModal, "#supportCloseBtn");
  }

  function closeSupport() {
    closeModal(supportModal);
  }

  function openLogDetail(id) {
    var logs = current && current.request_logs ? current.request_logs : [];
    activeLogDetail = logs.find(function (item) { return item.id === id; }) || null;
    if (!activeLogDetail) {
      toast("未找到请求日志详情");
      return;
    }
    document.getElementById("logDetailTitle").textContent = "请求日志详情 · " + (activeLogDetail.kind || activeLogDetail.path || id);
    var summaryRows = [
      ["日志 ID", activeLogDetail.id],
      ["时间", formatTime(activeLogDetail.time)],
      ["接口", activeLogDetail.path],
      ["请求号", activeLogDetail.req_seq_id || "-"],
      ["汇付 ID", activeLogDetail.huifu_id || "-"],
      ["HTTP", activeLogDetail.http_status || "-"],
      ["响应码", activeLogDetail.resp_code || "-"],
      ["签名状态", activeLogDetail.signature_status || "-"]
    ];
    document.getElementById("logDetailSummary").innerHTML = summaryRows.map(function (row) {
      return "<div class=\"log-summary-item\"><span>" + esc(row[0]) + "</span><b class=\"mono\">" + esc(row[1] || "-") + "</b></div>";
    }).join("");
    if (activeLogDetail.detail_available === false) {
      document.getElementById("logRequestJson").innerHTML = lockedDetailHTML("请求入参明细需要输入 admin token 后刷新页面状态。");
      document.getElementById("logResponseJson").innerHTML = lockedDetailHTML("响应参数明细需要输入 admin token 后刷新页面状态。");
      document.getElementById("logEnvelopeJson").innerHTML = lockedDetailHTML("信封和签名摘要需要输入 admin token 后刷新页面状态。");
    } else {
      document.getElementById("logRequestJson").textContent = prettyJSON(activeLogDetail.request_data || {});
      document.getElementById("logResponseJson").textContent = prettyJSON(activeLogDetail.response_data || activeLogDetail.response_body || {});
      document.getElementById("logEnvelopeJson").textContent = prettyJSON({
        request_envelope: activeLogDetail.request_envelope || {},
        response_envelope: activeLogDetail.response_envelope || {}
      });
    }
    openModal(logDetailModal, "#logDetailCloseBtn");
  }

  function closeLogDetail() {
    activeLogDetail = null;
    closeModal(logDetailModal);
  }

  function copyLogDetail() {
    if (!activeLogDetail) {
      toast("暂无可复制内容");
      return;
    }
    copyText(JSON.stringify(activeLogDetail, null, 2), "已复制请求日志详情");
  }

  function lockedDetailHTML(message) {
    return "<div class=\"locked-detail\">" + esc(message) + "</div>";
  }

  function openModal(modal, focusSelector) {
    modalFocusReturn = document.activeElement;
    modal.removeAttribute("hidden");
    document.body.classList.add("modal-open");
    window.setTimeout(function () {
      var target = modal.querySelector(focusSelector || "button, [href], input, textarea, select, [tabindex]:not([tabindex='-1'])");
      if (target) target.focus();
    }, 0);
  }

  function closeModal(modal) {
    modal.setAttribute("hidden", "");
    syncModalState();
    if (modalFocusReturn && document.contains(modalFocusReturn)) {
      modalFocusReturn.focus();
    }
    modalFocusReturn = null;
  }

  function activeModal() {
    if (!declarationModal.hasAttribute("hidden")) return declarationModal;
    if (!logDetailModal.hasAttribute("hidden")) return logDetailModal;
    if (!usageModal.hasAttribute("hidden")) return usageModal;
    if (!supportModal.hasAttribute("hidden")) return supportModal;
    return null;
  }

  function trapModalFocus(event) {
    var modal = activeModal();
    if (!modal) return;
    var focusables = Array.prototype.slice.call(modal.querySelectorAll("button, [href], input, textarea, select, [tabindex]:not([tabindex='-1'])"))
      .filter(function (el) { return !el.disabled && el.offsetParent !== null; });
    if (!focusables.length) return;
    var first = focusables[0];
    var last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function syncModalState() {
    var anyOpen = !declarationModal.hasAttribute("hidden") || !usageModal.hasAttribute("hidden") || !supportModal.hasAttribute("hidden") || !logDetailModal.hasAttribute("hidden");
    document.body.classList.toggle("modal-open", anyOpen);
  }

  function showDeclarationIfNeeded() {
    try {
      if (localStorage.getItem(declarationStorageKey) === "accepted") return;
    } catch (error) {
      // localStorage may be unavailable in restricted browser modes; show the declaration each time.
    }
    openModal(declarationModal, "#acceptDeclarationBtn");
  }

  function acceptDeclaration() {
    var dontShow = document.getElementById("declarationDontShow");
    if (dontShow && dontShow.checked) {
      try {
        localStorage.setItem(declarationStorageKey, "accepted");
      } catch (error) {
        // Ignore storage errors; the user can still continue for this page session.
      }
    }
    closeModal(declarationModal);
  }

  async function declineDeclaration() {
    setBusy("declineDeclarationBtn", true, "停止中...");
    setBusy("acceptDeclarationBtn", true, "已拒绝");
    try {
      await fetch("/__ui/declaration/decline", {
        method: "POST",
        cache: "no-store",
        headers: { "Content-Type": "application/json" },
        body: "{}"
      });
    } catch (error) {
      // The service may already be shutting down; continue with local page close flow.
    }
    document.getElementById("declarationBody").innerHTML = "<div class=\"decline-message\">已拒绝本地沙箱服务使用声明，正在停止本地沙箱服务。若浏览器未自动关闭本页面，请手动关闭当前标签页。</div>";
    var actions = declarationModal.querySelector(".declaration-actions");
    if (actions) actions.innerHTML = "<span class=\"notice\">服务停止中...</span>";
    window.setTimeout(function () {
      try {
        window.open("", "_self");
        window.close();
      } catch (error) {
        // Ignore close errors; browser may block scripts from closing user-opened tabs.
      }
      try {
        window.location.replace("about:blank");
      } catch (error) {
        document.body.innerHTML = "<main><section class=\"panel\"><div class=\"panel-body\"><p class=\"notice\">服务已停止，请关闭当前页面。</p></div></section></main>";
      }
    }, 700);
  }

  async function loadState() {
    try {
      var headers = {};
      var token = tokenInput.value.trim();
      if (token) headers.Authorization = "Bearer " + token;
      var response = await fetch("/__ui/state", { cache: "no-store", headers: headers });
      if (!response.ok) throw new Error("HTTP " + response.status);
      current = await response.json();
      renderAll();
      setLive(true);
      if (!updateChecked) {
        updateChecked = true;
        window.setTimeout(function () { checkUpdate(false); }, 200);
      }
    } catch (error) {
      setLive(false, error.message);
    }
  }

  function setLive(ok, msg) {
    var el = document.getElementById("liveState");
    el.className = "pill " + (ok ? "ok" : "bad");
    el.textContent = ok ? "live" : ("offline " + (msg || ""));
  }

  function renderAll() {
    if (!current) return;
    var ready = current.ready || {};
    document.getElementById("subtitle").textContent = [
      ready.version || "-",
      ready.mode || "-",
      ready.credential_profile || "-"
    ].join(" · ");
    renderRuntime(ready, current.profile || {});
    renderUpdateBox(ready);
    renderIntegrationConfig(ready, current.profile || {});
    renderMetrics();
    renderBusiness();
    renderRequestLogs();
    renderEvents();
    renderOps();
    syncWorkspaceTabs();
  }

  function renderRuntime(ready, profile) {
    var rows = [
      ["运行编号", ready.run_id],
      ["运行模式", ready.mode],
      ["凭证档案", ready.credential_profile],
      ["签名模型", ready.signature_model],
      ["契约包", ready.contract_bundle],
      ["运行时长", formatDuration(ready.uptime_seconds || 0)],
      ["控制台地址", ready.control_url || location.origin],
      ["报告目录", ready.report_dir],
      ["请求验签公钥指纹", profile.merchant_public_fingerprint],
      ["响应签名公钥指纹", profile.sandbox_public_fingerprint || profile.huifu_public_fingerprint]
    ];
    document.getElementById("runtimeKV").innerHTML = rows.map(function (row) {
      return "<div>" + esc(row[0]) + "</div><div class=\"mono\">" + esc(row[1] || "-") + "</div>";
    }).join("");
  }

  function renderUpdateBox(ready) {
    var status = document.getElementById("updateStatus");
    var detail = document.getElementById("updateDetail");
    var actions = document.getElementById("updateActions");
    var meta = document.getElementById("updateMeta");
    if (!status || !detail || !actions || !meta) return;
    var buttonHTML = "<button id=\"checkUpdateBtn\" class=\"btn\" type=\"button\" title=\"检查本地沙箱最新版本\">检查更新</button>";
    if (!updateState) {
      status.className = "pill pending";
      status.textContent = "未检查";
      detail.textContent = "尚未检查更新。";
      actions.innerHTML = buttonHTML;
      meta.textContent = "更新索引：" + (ready.update_index_url || "-");
      document.getElementById("checkUpdateBtn").addEventListener("click", function () { checkUpdate(true); });
      return;
    }
    if (updateState.status === "checking") {
      status.className = "pill pending";
      status.textContent = "检查中";
      detail.textContent = "正在读取公开版本索引...";
      actions.innerHTML = buttonHTML;
      meta.textContent = "更新索引：" + (ready.update_index_url || updateState.source_url || "-");
      document.getElementById("checkUpdateBtn").addEventListener("click", function () { checkUpdate(true); });
      setBusy("checkUpdateBtn", true, "检查中...");
      return;
    }
    if (updateState.ok === false) {
      status.className = "pill bad";
      status.textContent = "检查失败";
      detail.textContent = updateState.error || "无法读取公开版本索引。";
      actions.innerHTML = buttonHTML;
      meta.textContent = "更新索引：" + (ready.update_index_url || updateState.source_url || "-");
      document.getElementById("checkUpdateBtn").addEventListener("click", function () { checkUpdate(true); });
      return;
    }
    var currentVersion = updateState.current_version || ready.version || "-";
    var latestVersion = updateState.latest_version || "-";
    var download = updateState.download || {};
    var links = [buttonHTML];
    if (updateState.update_available && updateState.platform_supported && download.url) {
      links.push("<a class=\"btn primary\" target=\"_blank\" rel=\"noopener\" href=\"" + esc(download.url) + "\">下载新版</a>");
    }
    if (updateState.release_notes_url) {
      links.push("<a class=\"btn\" target=\"_blank\" rel=\"noopener\" href=\"" + esc(updateState.release_notes_url) + "\">更新说明</a>");
    } else if (updateState.download_page_url) {
      links.push("<a class=\"btn\" target=\"_blank\" rel=\"noopener\" href=\"" + esc(updateState.download_page_url) + "\">下载页面</a>");
    }
    actions.innerHTML = links.join("");
    document.getElementById("checkUpdateBtn").addEventListener("click", function () { checkUpdate(true); });
    if (updateState.update_available) {
      status.className = "pill warn";
      status.textContent = "有新版本";
      if (updateState.platform_supported) {
        detail.textContent = "当前 " + currentVersion + "，最新 " + latestVersion + "，可下载当前平台包。";
      } else {
        detail.textContent = "当前 " + currentVersion + "，最新 " + latestVersion + "，但索引中没有当前平台 " + (updateState.platform || "-") + " 的下载项。";
      }
    } else {
      status.className = "pill ok";
      status.textContent = "已是最新";
      detail.textContent = "当前 " + currentVersion + "，公开索引最新版本为 " + latestVersion + "。";
    }
    var metaParts = [
      "平台：" + (updateState.platform || "-"),
      "索引：" + (updateState.source_url || ready.update_index_url || "-")
    ];
    if (download.name) metaParts.push("文件：" + download.name);
    if (download.sha256) metaParts.push("SHA256：" + download.sha256);
    if (download.size_bytes) metaParts.push("大小：" + formatBytes(download.size_bytes));
    meta.textContent = metaParts.join(" · ");
  }

  async function checkUpdate(force) {
    updateState = { status: "checking" };
    renderUpdateBox((current && current.ready) || {});
    try {
      var response = await fetch("/__ui/update/check", { cache: "no-store" });
      var data = await response.json().catch(function () { return {}; });
      if (!response.ok) throw new Error(data.error || ("HTTP " + response.status));
      updateState = data;
      renderUpdateBox((current && current.ready) || {});
      if (force) {
        toast(data.update_available ? "发现新版本 " + data.latest_version : "当前已是最新版本");
      }
    } catch (error) {
      updateState = { ok: false, error: error.message };
      renderUpdateBox((current && current.ready) || {});
      if (force) toast("检查更新失败：" + error.message, "bad");
    }
  }

  function renderIntegrationConfig(ready, profile) {
    var rows = [
      ["网关地址 gateway_url", ready.gateway_url || "-"],
      ["系统号 sys_id", profile.sys_id || "-"],
      ["产品号 product_id", profile.product_id || "-"],
      ["汇付 ID huifu_id", "6666000100000001"],
      ["Skill 来源 skill_source", ready.sandbox_skill_source || "-"],
      ["请求签名私钥", "官方 SDK 优先使用 merchant_private_key"],
      ["响应验签公钥", "官方 SDK 优先使用 merchant_public_key"],
      ["Webhook 验签密钥 webhook_endpoint_key", (revealedCredentials && revealedCredentials.webhook_endpoint_key) || "需输入 admin_token 后点击“显示 Webhook Key”"]
    ];
    document.getElementById("integrationKV").innerHTML = rows.map(function (row) {
      return "<div>" + esc(row[0]) + "</div><div class=\"mono\">" + esc(row[1]) + "</div>";
    }).join("");
    renderWebhookTargetConfig(ready);
  }

  function renderWebhookTargetConfig(ready) {
    var targets = Array.isArray(ready.webhook_targets) ? ready.webhook_targets : [];
    var hint = document.getElementById("webhookTargetHint");
    if (!hint) return;
    if (targets.length) {
      hint.innerHTML = "已配置 " + targets.length + " 个目标：" + targets.map(function (target) {
        return "<code>" + esc(target) + "</code>";
      }).join("，") + "。输入新地址并保存会替换当前运行时目标。";
      return;
    }
    hint.textContent = "未配置 Webhook 目标时，业务状态里的 Webhook 按钮会禁用。建议使用本机地址，例如 http://127.0.0.1:18081/webhook。";
  }

  function projectConfigPayload(credentials) {
    var ready = current.ready || {};
    var profile = current.profile || {};
    credentials = credentials || {};
    return {
      gateway_url: credentials.gateway_url || ready.gateway_url || "",
      sys_id: credentials.sys_id || profile.sys_id || "",
      product_id: credentials.product_id || profile.product_id || "",
      huifu_id: "6666000100000001",
      skill_source: credentials.skill_source || ready.sandbox_skill_source || "",
      merchant_private_key: credentials.merchant_private_key || "",
      merchant_public_key: credentials.merchant_public_key || "",
      webhook_endpoint_key: credentials.webhook_endpoint_key || "",
      signature_model: credentials.signature_model || ready.signature_model || "",
      usage: credentials.usage || ("本地沙箱模式下 skill_source 使用 " + (credentials.skill_source || ready.sandbox_skill_source || "hfps/1.3.1;sandbox/1.0.1") + "；merchant_private_key 用于客户项目请求加签；merchant_public_key 用于客户项目验证本地沙箱响应和通知签名；webhook_endpoint_key 用于客户项目验证本地沙箱 Webhook 签名。RSA 密钥值均为无 PEM 头尾、无换行的 Base64。")
    };
  }

  function copyText(value, okMessage) {
    if (!value || value === "-") {
      toast("暂无可复制内容");
      return;
    }
    navigator.clipboard.writeText(value).then(function () {
      toast(okMessage);
    }, function () {
      toast("复制失败，请使用导出凭证或浏览器允许剪贴板权限后重试。", "bad");
    });
  }

  function setBusy(id, busy, label) {
    var button = document.getElementById(id);
    if (!button) return;
    if (busy) {
      if (!button.dataset.idleText) button.dataset.idleText = button.textContent;
      button.disabled = true;
      button.setAttribute("aria-busy", "true");
      button.textContent = label || "处理中...";
      return;
    }
    button.disabled = false;
    button.removeAttribute("aria-busy");
    if (button.dataset.idleText) button.textContent = button.dataset.idleText;
  }

  function setElementBusy(button, busy, label) {
    if (!button) return;
    if (busy) {
      if (!button.dataset.idleText) button.dataset.idleText = button.textContent;
      button.disabled = true;
      button.setAttribute("aria-busy", "true");
      button.textContent = label || "发送中";
      return;
    }
    button.disabled = false;
    button.removeAttribute("aria-busy");
    if (button.dataset.idleText) button.textContent = button.dataset.idleText;
  }

  async function exportCredentials() {
    var token = tokenInput.value.trim();
    if (!token) {
      toast("请输入启动时打印的 admin_token");
      return;
    }
    setBusy("exportCredentialsBtn", true, "导出中...");
    try {
      var response = await requestCredentialExport(token);
      response.clone().json().then(function (credentials) {
        revealedCredentials = credentials;
        renderIntegrationConfig((current && current.ready) || {}, (current && current.profile) || {});
      }).catch(function () {});
      var blob = await response.blob();
      var url = URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = "sandbox-credentials.json";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      toast("已导出 sandbox-credentials.json");
    } catch (error) {
      toast("导出凭证失败：" + error.message, "bad");
    } finally {
      setBusy("exportCredentialsBtn", false);
    }
  }

  async function copyProjectConfig() {
    if (!current) {
      toast("状态尚未加载");
      return;
    }
    var token = tokenInput.value.trim();
    if (!token) {
      toast("请输入启动时打印的 admin_token");
      return;
    }
    setBusy("copyProjectConfigBtn", true, "复制中...");
    try {
      var response = await requestCredentialExport(token);
      var credentials = await response.json();
      revealedCredentials = credentials;
      renderIntegrationConfig((current && current.ready) || {}, (current && current.profile) || {});
      copyText(JSON.stringify(projectConfigPayload(credentials), null, 2), "已复制带凭证的接入配置");
    } catch (error) {
      toast("复制配置失败：" + error.message, "bad");
    } finally {
      setBusy("copyProjectConfigBtn", false);
    }
  }

  async function revealWebhookEndpointKey() {
    var token = tokenInput.value.trim();
    if (!token) {
      toast("请输入启动时打印的 admin_token");
      return;
    }
    setBusy("showWebhookKeyBtn", true, "读取中...");
    try {
      var response = await requestCredentialExport(token);
      revealedCredentials = await response.json();
      renderIntegrationConfig((current && current.ready) || {}, (current && current.profile) || {});
      if (revealedCredentials.webhook_endpoint_key) {
        toast("已显示 webhook_endpoint_key");
      } else {
        toast("当前运行未返回 webhook_endpoint_key", "bad");
      }
    } catch (error) {
      toast("显示 Webhook Key 失败：" + error.message, "bad");
    } finally {
      setBusy("showWebhookKeyBtn", false);
    }
  }

  async function saveWebhookTarget() {
    var token = tokenInput.value.trim();
    if (!token) {
      toast("请输入启动时打印的 admin_token");
      return;
    }
    var input = document.getElementById("webhookTargetInput");
    var target = input ? input.value.trim() : "";
    if (!target) {
      toast("请输入 Webhook 目标地址", "bad");
      return;
    }
    setBusy("saveWebhookTargetBtn", true, "保存中...");
    try {
      var session = await adminSession(token);
      var response = await fetch("/__admin/webhook-targets", {
        method: "POST",
        cache: "no-store",
        headers: {
          "Authorization": "Bearer " + token,
          "X-Huifu-Sandbox-CSRF": session.csrf_token,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ target: target })
      });
      var data = await response.json().catch(function () { return {}; });
      if (!response.ok) throw new Error(data.error || ("HTTP " + response.status));
      toast("已保存 Webhook 目标");
      await loadState();
    } catch (error) {
      toast("保存 Webhook 目标失败：" + error.message, "bad");
    } finally {
      setBusy("saveWebhookTargetBtn", false);
    }
  }

  async function requestCredentialExport(token) {
    var session = await adminSession(token);
    var response = await fetch("/__admin/credentials/export", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + token,
        "X-Huifu-Sandbox-CSRF": session.csrf_token,
        "Content-Type": "application/json"
      },
      body: "{}"
    });
    if (!response.ok) {
      var err = await response.json().catch(function () { return {}; });
      throw new Error(err.error || ("HTTP " + response.status));
    }
    return response;
  }

  async function triggerManualDelivery(button) {
    var token = tokenInput.value.trim();
    if (!token) {
      toast("请输入启动时打印的 admin_token");
      return;
    }
    var payload = {
      channel: button.getAttribute("data-delivery-channel"),
      entity_type: button.getAttribute("data-delivery-entity"),
      kind: button.getAttribute("data-delivery-kind") || "",
      req_seq_id: button.getAttribute("data-delivery-req"),
      outcome: button.getAttribute("data-delivery-outcome")
    };
    if (!payload.channel || !payload.entity_type || !payload.req_seq_id || !payload.outcome) {
      toast("触发参数不完整", "bad");
      return;
    }
    setElementBusy(button, true, "发送中");
    try {
      var session = await adminSession(token);
      var response = await fetch("/__admin/deliver", {
        method: "POST",
        cache: "no-store",
        headers: {
          "Authorization": "Bearer " + token,
          "X-Huifu-Sandbox-CSRF": session.csrf_token,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });
      var data = await response.json().catch(function () { return {}; });
      if (!response.ok) throw new Error(data.error || ("HTTP " + response.status));
      if (data.ok === false) {
        toast(deliveryToastLabel(payload) + "已发送，但目标未确认：" + deliveryFailureMessage(data), "bad");
      } else {
        toast(deliveryToastLabel(payload) + "已触发");
      }
      await loadState();
    } catch (error) {
      toast("触发失败：" + error.message, "bad");
    } finally {
      setElementBusy(button, false);
    }
  }

  function deliveryToastLabel(payload) {
    var channel = payload.channel === "notify" ? "Notify" : "Webhook";
    var outcome = payload.outcome === "success" ? "成功" : "失败";
    return channel + outcome;
  }

  function deliveryFailureMessage(data) {
    if (data.notification && data.notification.diagnosis) return data.notification.diagnosis;
    if (data.webhooks && data.webhooks.length && data.webhooks[0].diagnosis) return data.webhooks[0].diagnosis;
    return data.error || "未收到预期确认";
  }

  async function triggerHostingSuccess(button) {
    var token = tokenInput.value.trim();
    if (!token) {
      toast("请输入启动时打印的 admin_token");
      return;
    }
    var payload = {
      pre_order_id: button.getAttribute("data-hosting-pre") || "",
      req_seq_id: button.getAttribute("data-hosting-req") || ""
    };
    if (!payload.pre_order_id && !payload.req_seq_id) {
      toast("托管确认参数不完整", "bad");
      return;
    }
    setElementBusy(button, true, "确认中");
    try {
      var session = await adminSession(token);
      var response = await fetch("/__admin/hosting/success", {
        method: "POST",
        cache: "no-store",
        headers: {
          "Authorization": "Bearer " + token,
          "X-Huifu-Sandbox-CSRF": session.csrf_token,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });
      var data = await response.json().catch(function () { return {}; });
      if (!response.ok) throw new Error(data.error || ("HTTP " + response.status));
      toast("托管支付已模拟成功，项目再次查单会返回成功");
      await loadState();
    } catch (error) {
      toast("模拟托管成功失败：" + error.message, "bad");
    } finally {
      setElementBusy(button, false);
    }
  }

	function renderMetrics() {
	  var counts = current.counts || {};
	  var paymentStates = current.payment_state_counts || {};
	  var refundStates = current.refund_state_counts || {};
	  var closeStates = current.close_state_counts || {};
	  var metrics = [
	    { title: "支付", value: counts.payments || 0, sub: stateSubCounts(paymentStates) },
	    { title: "退款", value: counts.refunds || 0, sub: stateSubCounts(refundStates) },
	    { title: "关单", value: counts.closes || 0, sub: stateSubCounts(closeStates) },
	    { title: "对账", value: counts.reconciliations || 0 },
	    { title: "请求日志", value: counts.request_logs || 0 },
	    { title: "事件", value: counts.events || 0 },
	    { title: "安全发现", value: counts.security_findings || 0 }
    ];
    document.getElementById("metrics").innerHTML = metrics.map(function (item) {
      var html = "<div class=\"metric\"><div class=\"metric-head\"><b>" + esc(item.value) + "</b><span class=\"metric-title\">" + esc(item.title) + "</span></div>";
      if (item.sub) {
        html += "<div class=\"metric-subgrid\">" + item.sub.map(function (sub) {
          return "<div class=\"metric-sub\"><strong>" + esc(sub[1]) + "</strong><span>" + esc(sub[0]) + "</span></div>";
        }).join("") + "</div>";
      }
      return html + "</div>";
	    }).join("");
	  }

	  function stateSubCounts(states) {
	    return [["成功", states.S || 0], ["处理中", states.P || 0], ["失败", states.F || 0]];
	  }

  function renderBusiness() {
    if (!current) return;
    var columns = {
      payments: [
        ["req_seq_id", "请求号"], ["kind", "类型"], ["state", "状态"], ["trans_amt", "金额"],
        ["trade_type", "交易类型"], ["pre_order_id", "预下单"], ["hf_seq_id", "汇付流水"], ["query_count", "查询"], ["business_variant", "场景"], ["delivery_actions", "操作"]
      ],
      refunds: [
        ["req_seq_id", "退款请求号"], ["kind", "类型"], ["state", "状态"], ["ord_amt", "金额"],
        ["payment_req_seq_id", "原请求号"], ["query_count", "查询"], ["settled_status", "完成"], ["business_variant", "场景"], ["delivery_actions", "操作"]
      ],
      closes: [
        ["req_seq_id", "关单请求号"], ["kind", "类型"], ["state", "状态"],
        ["payment_req_seq_id", "原请求号"], ["query_count", "查询"], ["notified", "Notify"], ["webhooked", "Webhook"], ["business_variant", "场景"], ["delivery_actions", "操作"]
      ],
      reconciliations: [
        ["id", "任务"], ["bill_type", "账单"], ["file_date", "日期"], ["task_stat", "状态"],
        ["ready", "可下载"], ["row_count", "行数"], ["download_status", "下载"]
      ]
    };
    renderTable("businessTable", current[businessView] || [], columns[businessView], "暂无业务请求。项目访问 gateway_url 后这里会自动出现记录。");
  }

  function renderRequestLogs() {
    renderTable("requestLogTable", current.request_logs || [], [
      ["time", "时间"], ["kind", "类型"], ["method", "方法"], ["path", "接口"],
      ["req_seq_id", "请求号"], ["http_status", "HTTP"], ["resp_code", "响应码"], ["signature_status", "签名"], ["actions", "操作"]
    ], "暂无请求日志。客户项目访问 gateway_url 后这里会记录入参与响应。");
  }

  function renderEvents() {
    renderTable("eventTable", current.events || [], [
      ["time", "时间"], ["type", "事件"], ["endpoint", "接口"], ["entity_id", "对象"], ["details", "详情"]
    ], "暂无事件。");
  }

  function renderOps() {
    var columns = {
      notifications: [
        ["time", "时间"], ["payment_req_seq_id", "业务请求号"], ["status", "状态"], ["target", "目标"], ["attempts", "次数"], ["diagnosis", "诊断"], ["error", "错误"]
      ],
      webhooks: [
        ["time", "时间"], ["event_type", "事件"], ["entity_id", "对象"], ["status", "状态"], ["target", "目标"], ["attempts", "次数"], ["diagnosis", "诊断"], ["error", "错误"]
      ],
      security_findings: [
        ["time", "时间"], ["severity", "级别"], ["type", "类型"], ["target", "目标"], ["reason", "原因"]
      ]
    };
    renderTable("opsTable", current[opsView] || [], columns[opsView], "暂无记录。");
  }

  function renderTable(id, rows, columns, emptyText) {
    var root = document.getElementById(id);
    if (!rows.length) {
      root.innerHTML = "<div class=\"empty\">" + esc(emptyText) + "</div>";
      return;
    }
    var head = columns.map(function (col) { return "<th>" + esc(col[1]) + "</th>"; }).join("");
    var body = rows.map(function (row) {
      return "<tr>" + columns.map(function (col) {
        return "<td>" + renderValue(col[0], row[col[0]], row) + "</td>";
      }).join("") + "</tr>";
    }).join("");
    root.innerHTML = "<table><thead><tr>" + head + "</tr></thead><tbody>" + body + "</tbody></table>";
  }

  function renderValue(key, value, row) {
    if (value === undefined || value === null || value === "") return "<span class=\"notice\">-</span>";
    if (key === "delivery_actions") return renderDeliveryActions(row);
    if (key === "actions") {
      var label = row.detail_available === false ? "摘要" : "详情";
      var title = row.detail_available === false ? "输入 admin token 后刷新可查看入参和响应明细" : "查看入参和响应明细";
      return "<button class=\"btn small\" type=\"button\" title=\"" + esc(title) + "\" data-log-detail=\"" + esc(value) + "\">" + esc(label) + "</button>";
    }
    if (typeof value === "boolean") return value ? "<span class=\"pill ok\">是</span>" : "<span class=\"pill\">否</span>";
    if (key === "http_status") return "<span class=\"" + httpPillClass(value) + "\">" + esc(value) + "</span>";
    if (key === "state" || key === "status" || key === "task_stat" || key === "severity" || key === "signature_status" || key === "resp_code" || key === "settled_status") {
      return "<span class=\"" + pillClass(value) + "\">" + esc(value) + "</span>";
    }
    if (key === "time") return esc(formatTime(value));
    if (key === "details") return "<span class=\"details mono\" title=\"" + esc(JSON.stringify(value || {})) + "\">" + esc(JSON.stringify(value || {})) + "</span>";
    if (typeof value === "object") return "<span class=\"details mono\">" + esc(JSON.stringify(value)) + "</span>";
    return "<span class=\"mono\">" + esc(value) + "</span>";
  }

  function renderDeliveryActions(row) {
    var entity = deliveryEntityForBusinessView(businessView);
    if (!entity || !row.req_seq_id) return "<span class=\"notice\">-</span>";
    var notifySupported = entity === "payment" || entity === "refund" || entity === "close";
    var notifyAvailable = notifySupported && Boolean(row.notify_url);
    var webhookAvailable = Number((current.ready || {}).webhook_target_count || 0) > 0;
    var html = "<div class=\"delivery-actions\">";
    if (businessView === "payments" && row.kind === "hosting") {
      html += renderDeliveryGroup("托管", [hostingSuccessButton(row)]);
    }
    if (notifySupported) {
      html += renderDeliveryGroup("Notify", [
        deliveryButton("notify", entity, row, "success", notifyAvailable, "当前记录没有 notify_url"),
        deliveryButton("notify", entity, row, "failure", notifyAvailable, "当前记录没有 notify_url")
      ]);
    }
    html += renderDeliveryGroup("Webhook", [
      deliveryButton("webhook", entity, row, "success", webhookAvailable, "未配置 Webhook 目标"),
      deliveryButton("webhook", entity, row, "failure", webhookAvailable, "未配置 Webhook 目标")
    ]);
    return html + "</div>";
  }

  function renderDeliveryGroup(label, buttons) {
    return "<span class=\"delivery-group\"><span>" + esc(label) + "</span>" + buttons.join("") + "</span>";
  }

  function hostingSuccessButton(row) {
    var state = String(row.state || "").toUpperCase();
    var enabled = Boolean(row.pre_order_id || row.req_seq_id) && state !== "S" && state !== "F";
    var title = enabled ? "模拟用户完成托管支付，沙箱将订单置为成功并触发后续通知" : (state === "S" ? "托管交易已成功" : "托管交易已终态");
    var disabled = enabled ? "" : " disabled aria-disabled=\"true\"";
    return "<button class=\"btn mini\" type=\"button\" title=\"" + esc(title) + "\"" +
      " data-hosting-success=\"1\"" +
      " data-hosting-pre=\"" + esc(row.pre_order_id || "") + "\"" +
      " data-hosting-req=\"" + esc(row.req_seq_id || "") + "\"" + disabled + ">模拟成功</button>";
  }

  function deliveryButton(channel, entity, row, outcome, enabled, disabledReason) {
    var label = outcome === "success" ? "成功" : "失败";
    var title = enabled ? ("触发" + (channel === "notify" ? " Notify " : " Webhook ") + label) : disabledReason;
    var disabled = enabled ? "" : " disabled aria-disabled=\"true\"";
    return "<button class=\"btn mini\" type=\"button\" title=\"" + esc(title) + "\"" +
      " data-delivery-channel=\"" + esc(channel) + "\"" +
      " data-delivery-entity=\"" + esc(entity) + "\"" +
      " data-delivery-kind=\"" + esc(row.kind || "") + "\"" +
      " data-delivery-req=\"" + esc(row.req_seq_id || "") + "\"" +
      " data-delivery-outcome=\"" + esc(outcome) + "\"" + disabled + ">" + esc(label) + "</button>";
  }

  function deliveryEntityForBusinessView(view) {
    if (view === "payments") return "payment";
    if (view === "refunds") return "refund";
    if (view === "closes") return "close";
    return "";
  }

  function pillClass(value) {
    var raw = String(value || "").toLowerCase();
    if (raw === "s" || raw === "success" || raw === "delivered" || raw === "passed" || raw === "low") return "pill ok";
    if (raw === "verified" || raw === "00000000" || raw === "已完成") return "pill ok";
    if (raw === "p" || raw === "processing" || raw === "pending" || raw === "fp" || raw === "处理中") return "pill pending";
    if (raw === "high" || raw === "failed" || raw === "blocked" || raw === "失败" || raw.indexOf("ls000003") === 0) return "pill bad";
    if (raw === "warning" || raw === "medium" || raw === "not_verified" || raw.indexOf("ls") === 0) return "pill warn";
    return "pill";
  }

  function httpPillClass(value) {
    var code = Number(value) || 0;
    if (code >= 200 && code < 300) return "pill ok";
    if (code >= 400 && code < 500) return "pill warn";
    if (code >= 500) return "pill bad";
    return "pill";
  }

  async function generateReport() {
    var token = tokenInput.value.trim();
    if (!token) {
      toast("请输入启动时打印的 admin_token");
      return;
    }
    setBusy("reportBtn", true, "生成中...");
    try {
      var session = await adminSession(token);
      var response = await fetch("/__admin/report", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + token,
          "X-Huifu-Sandbox-CSRF": session.csrf_token,
          "Content-Type": "application/json"
        },
        body: "{}"
      });
      var data = await response.json();
      if (!response.ok) throw new Error(data.error || ("HTTP " + response.status));
      toast("报告已生成：" + data.report_dir);
      loadState();
    } catch (error) {
      toast("生成报告失败：" + error.message, "bad");
    } finally {
      setBusy("reportBtn", false);
    }
  }

  async function shutdownSandbox() {
    var token = tokenInput.value.trim();
    if (!token) {
      toast("请输入启动时打印的 admin_token");
      return;
    }
    if (!confirm("停止当前本地沙箱服务？")) return;
    setBusy("shutdownBtn", true, "停止中...");
    try {
      var session = await adminSession(token);
      var response = await fetch("/__admin/shutdown", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + token,
          "X-Huifu-Sandbox-CSRF": session.csrf_token,
          "Content-Type": "application/json"
        },
        body: "{}"
      });
      if (!response.ok) throw new Error("HTTP " + response.status);
      toast("已发送停止命令");
    } catch (error) {
      toast("停止失败：" + error.message, "bad");
      setBusy("shutdownBtn", false);
    }
  }

  async function adminSession(token) {
    var response = await fetch("/__admin/session", {
      cache: "no-store",
      headers: { "Authorization": "Bearer " + token }
    });
    var data = await response.json();
    if (!response.ok) throw new Error(data.error || ("HTTP " + response.status));
    if (!data.csrf_token) throw new Error("csrf_missing");
    return data;
  }

  function configureTimer() {
    if (timer) clearInterval(timer);
    timer = null;
    if (document.getElementById("autoRefresh").checked) {
      timer = setInterval(loadState, 2500);
    }
  }

  function formatTime(value) {
    if (!value) return "-";
    var date = new Date(value);
    if (isNaN(date.getTime())) return value;
    return date.toLocaleString();
  }

  function formatDuration(total) {
    total = Math.max(0, Number(total) || 0);
    var h = Math.floor(total / 3600);
    var m = Math.floor((total % 3600) / 60);
    var s = Math.floor(total % 60);
    if (h) return h + "h " + m + "m";
    if (m) return m + "m " + s + "s";
    return s + "s";
  }

  function formatBytes(value) {
    var n = Number(value) || 0;
    if (n >= 1024 * 1024) return (n / 1024 / 1024).toFixed(1) + " MB";
    if (n >= 1024) return (n / 1024).toFixed(1) + " KB";
    return n + " B";
  }

  function prettyJSON(value) {
    if (typeof value === "string") return value || "{}";
    try {
      return JSON.stringify(value || {}, null, 2);
    } catch (error) {
      return String(value);
    }
  }

  function esc(value) {
    return String(value === undefined || value === null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function toast(message, kind) {
    var el = document.getElementById("toast");
    el.textContent = message;
    el.classList.toggle("bad", kind === "bad");
    el.classList.add("show");
    setTimeout(function () {
      el.classList.remove("show");
      el.classList.remove("bad");
    }, kind === "bad" ? 6200 : 4200);
  }

  showDeclarationIfNeeded();
  configureTimer();
  loadState();
})();
</script>
</body>
</html>
`
