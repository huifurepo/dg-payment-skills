package main

import (
	"fmt"
	"net/http"
	"strings"
)

var supportedBillTypes = map[string]struct{}{
	"TRADE_BILL":             {},
	"SPLIT_BILL":             {},
	"WITHDRAWAL_BILL":        {},
	"SETTLE_BILL":            {},
	"TRADE_BILL_MONTH":       {},
	"SETTLE_BILL_MONTH":      {},
	"SETTLE_USER_BILL":       {},
	"SETTLE_BILL_USER_MONTH": {},
	"SETTLE_FUND_BILL":       {},
	"MERGE_BILL":             {},
}

func (a *App) handleReconciliationFileQuery(w http.ResponseWriter, r *http.Request) {
	env, ok := a.readGatewayEnvelope(w, r, "/v2/trade/check/filequery")
	if !ok {
		return
	}
	if missing := missingFields(env.Data, []string{"req_date", "req_seq_id", "huifu_id", "file_date"}); len(missing) > 0 {
		a.writeGatewayData(w, localError("LS000002", "missing required data: "+strings.Join(missing, ",")))
		return
	}
	if !isYYYYMMDD(stringValue(env.Data["req_date"])) || !isYYYYMMDD(stringValue(env.Data["file_date"])) {
		a.writeGatewayData(w, localError("LS200010", "req_date and file_date must use yyyyMMdd"))
		return
	}
	billType := stringValue(env.Data["bill_type"])
	if billType == "" {
		billType = "TRADE_BILL"
	}
	if _, ok := supportedBillTypes[billType]; !ok {
		a.writeGatewayData(w, localError("LS200006", "unsupported bill_type "+billType))
		return
	}
	huifuID := stringValue(env.Data["huifu_id"])
	fileDate := stringValue(env.Data["file_date"])
	key := reconciliationKey(huifuID, fileDate, billType)

	a.mu.Lock()
	file := a.reconciliations[key]
	if file == nil {
		rowCount, downloadStatus := reconciliationScenarioOptions(stringValue(env.Data["sandbox_scenario"]))
		file = &ReconciliationFile{
			ID:             nextID("RC"),
			HuifuID:        huifuID,
			FileDate:       fileDate,
			BillType:       billType,
			FileName:       fmt.Sprintf("%s_%s_%s.csv", fileDate, huifuID, billType),
			TaskStat:       "FP",
			RowCount:       rowCount,
			DownloadStatus: downloadStatus,
		}
		a.reconciliations[key] = file
	}
	file.QueryCount++
	if file.QueryCount >= 2 {
		file.Ready = true
		file.TaskStat = "S"
		file.DownloadURL = a.reconciliationDownloadURL(file.ID)
	}
	fileCopy := *file
	a.mu.Unlock()

	a.record("reconciliation.query", r.URL.Path, fileCopy.ID, map[string]any{
		"huifu_id":    fileCopy.HuifuID,
		"file_date":   fileCopy.FileDate,
		"bill_type":   fileCopy.BillType,
		"query_count": fileCopy.QueryCount,
		"ready":       fileCopy.Ready,
	})
	a.writeGatewayData(w, reconciliationResponse(env.Data, fileCopy))
}

func (a *App) handleReconciliationDownload(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	fileID := strings.TrimPrefix(r.URL.Path, "/__download/reconciliation/")
	if fileID == "" || strings.Contains(fileID, "/") {
		http.NotFound(w, r)
		return
	}
	file, ok := a.reconciliationByID(fileID)
	if !ok {
		http.NotFound(w, r)
		return
	}
	if !file.Ready {
		writeJSON(w, http.StatusConflict, map[string]any{"error": "reconciliation_file_not_ready"})
		return
	}
	switch file.DownloadStatus {
	case "expired":
		writeJSON(w, http.StatusGone, map[string]any{"error": "reconciliation_file_expired"})
		return
	case "forbidden":
		writeJSON(w, http.StatusForbidden, map[string]any{"error": "reconciliation_file_forbidden"})
		return
	}
	w.Header().Set("Content-Type", "text/csv;charset=utf-8")
	w.Header().Set("Content-Disposition", `attachment; filename="`+file.FileName+`"`)
	_, _ = fmt.Fprintf(w, "huifu_id,file_date,bill_type,synthetic,total_count,total_amount\n")
	if file.RowCount > 0 {
		_, _ = fmt.Fprintf(w, "%s,%s,%s,true,%d,0.01\n", file.HuifuID, file.FileDate, file.BillType, file.RowCount)
	}
}

func (a *App) reconciliationByID(fileID string) (ReconciliationFile, bool) {
	a.mu.Lock()
	defer a.mu.Unlock()
	for _, file := range a.reconciliations {
		if file.ID == fileID {
			return *file, true
		}
	}
	return ReconciliationFile{}, false
}

func (a *App) reconciliationDownloadURL(fileID string) string {
	base := a.controlBaseURL
	if base == "" {
		base = "http://127.0.0.1"
	}
	return strings.TrimRight(base, "/") + "/__download/reconciliation/" + fileID
}

func reconciliationResponse(request map[string]any, file ReconciliationFile) map[string]any {
	resp := map[string]any{
		"resp_code":  "00000000",
		"resp_desc":  "reconciliation query success",
		"req_date":   stringValue(request["req_date"]),
		"req_seq_id": stringValue(request["req_seq_id"]),
		"huifu_id":   file.HuifuID,
		"file_date":  file.FileDate,
		"bill_type":  file.BillType,
		"task_details": map[string]any{
			"task_stat": file.TaskStat,
		},
	}
	if file.Ready {
		details := map[string]any{
			"file_id":         file.ID,
			"file_name":       file.FileName,
			"file_Name":       file.FileName,
			"download_url":    file.DownloadURL,
			"bill_type":       file.BillType,
			"file_date":       file.FileDate,
			"record_count":    file.RowCount,
			"download_status": firstNonEmpty(file.DownloadStatus, "ready"),
		}
		resp["file_details"] = details
	}
	return resp
}

func reconciliationKey(huifuID, fileDate, billType string) string {
	return huifuID + "|" + fileDate + "|" + billType
}

func reconciliationScenarioOptions(raw string) (int, string) {
	switch strings.ToUpper(strings.TrimSpace(raw)) {
	case "RECON_EMPTY":
		return 0, "ready"
	case "RECON_EXPIRED":
		return 1, "expired"
	case "RECON_FORBIDDEN":
		return 1, "forbidden"
	default:
		return 1, "ready"
	}
}

func isYYYYMMDD(value string) bool {
	if len(value) != 8 {
		return false
	}
	for _, ch := range value {
		if ch < '0' || ch > '9' {
			return false
		}
	}
	return true
}
