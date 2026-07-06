package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"
)

func (a *App) WriteReport() error {
	if a.reportDir == "" {
		return nil
	}
	if err := os.MkdirAll(a.reportDir, 0o700); err != nil {
		return err
	}
	a.mu.Lock()
	events := sanitizeEventsForReport(a.events)
	payments := map[string]*Payment{}
	for key, value := range a.payments {
		copy := *value
		copy.NotifyURL = redactTarget(copy.NotifyURL)
		payments[key] = &copy
	}
	refunds := map[string]*RefundOperation{}
	for key, value := range a.refunds {
		copy := *value
		copy.NotifyURL = redactTarget(copy.NotifyURL)
		refunds[key] = &copy
	}
	closes := map[string]*CloseOperation{}
	for key, value := range a.closes {
		copy := *value
		closes[key] = &copy
	}
	reconciliations := map[string]*ReconciliationFile{}
	for key, value := range a.reconciliations {
		copy := *value
		copy.DownloadURL = redactTarget(copy.DownloadURL)
		reconciliations[key] = &copy
	}
	notifications := make([]NotificationDelivery, len(a.notifications))
	copy(notifications, a.notifications)
	for i := range notifications {
		notifications[i] = sanitizeNotificationDeliveryForOutput(notifications[i])
		notifications[i].Target = notifications[i].TargetRedacted
	}
	webhooks := make([]WebhookDelivery, len(a.webhooks))
	copy(webhooks, a.webhooks)
	for i := range webhooks {
		webhooks[i] = sanitizeWebhookDeliveryForOutput(webhooks[i])
		webhooks[i].Sign = signatureDigest(webhooks[i].Sign)
		webhooks[i].Target = webhooks[i].TargetRedacted
	}
	requestLogs := make([]RequestLog, len(a.requestLogs))
	copy(requestLogs, a.requestLogs)
	for i := range requestLogs {
		requestLogs[i] = sanitizeRequestLogForReport(requestLogs[i])
	}
	securityFindings := append([]SecurityFinding(nil), a.securityFindings...)
	for i := range securityFindings {
		securityFindings[i].Target = securityFindings[i].TargetRedacted
	}
	scenarioResults := append([]ScenarioResult(nil), a.scenarioResults...)
	fixtureResults := append([]FixtureResult(nil), a.fixtureResults...)
	a.mu.Unlock()

	summary := map[string]any{
		"name":                     appName,
		"version":                  appVersion,
		"skill_source":             skillSource,
		"sandbox_skill_source":     sandboxSkillSource,
		"run_id":                   a.runID,
		"started_at":               a.startedAt.Format(time.RFC3339Nano),
		"ended_at":                 time.Now().UTC().Format(time.RFC3339Nano),
		"contract_bundle":          contractBundle,
		"contract_digest":          a.bundle.Digest,
		"report_schema_version":    reportSchema,
		"synthetic":                true,
		"contains_production_data": false,
		"mode":                     a.mode,
		"credential_profile":       firstNonEmpty(a.creds.ProfileName, "synthetic"),
		"signature_model":          firstNonEmpty(a.creds.SignatureModel, "synthetic-dual-key"),
		"official_signature":       a.mode == "official-proxy",
	}
	if a.creds.HuifuPublic != nil {
		summary["huifu_public_fingerprint"] = publicKeyFingerprint(a.creds.HuifuPublic)
	}
	if a.creds.MerchantPublic != nil {
		summary["merchant_public_fingerprint"] = publicKeyFingerprint(a.creds.MerchantPublic)
	}
	finalState := map[string]any{"payments": payments, "refunds": refunds, "closes": closes, "reconciliation_files": reconciliations}
	contractCoverage := contractCoverage(a.bundle)
	endpointCoverageData := endpointCoverage(a.bundle, scenarioResults, fixtureResults)
	fixtureCoverageData := fixtureCoverage(a.bundle, fixtureResults)
	businessScenarioCoverageData := businessScenarioCoverage(a.bundle, scenarioResults, fixtureResults)
	sampleCoverageData := sampleCoverage(a.bundle, fixtureResults)
	sampleImportData := sampleImportReport(a.bundle)
	scopeBoundariesData := sandboxScopeBoundaries(a.bundle)
	scenarioResultsData := map[string]any{"coverage_runner_version": coverageRunnerVersion, "fixture_runner_version": fixtureRunnerVersion, "scenarios": scenarioResults}
	notifyData := map[string]any{"deliveries": notifications}
	webhookData := map[string]any{"deliveries": webhooks}
	requestLogData := map[string]any{"logs": requestLogs, "max_retained": maxGatewayRequestLogs}
	reconciliationData := map[string]any{"files": reconciliations}

	reportContents, err := marshalReportContents(map[string]any{
		"summary.json":                    summary,
		"events.ndjson":                   events,
		"final-state.json":                finalState,
		"contract-coverage.json":          contractCoverage,
		"endpoint-coverage.json":          endpointCoverageData,
		"fixture-coverage.json":           fixtureCoverageData,
		"business-scenario-coverage.json": businessScenarioCoverageData,
		"sample-coverage.json":            sampleCoverageData,
		"sample-import-report.json":       sampleImportData,
		"sandbox-scope-boundaries.json":   scopeBoundariesData,
		"scenario-results.json":           scenarioResultsData,
		"notify-attempts.json":            notifyData,
		"webhook-attempts.json":           webhookData,
		"request-logs.json":               requestLogData,
		"reconciliation-files.json":       reconciliationData,
	})
	if err != nil {
		return err
	}
	secretScan := scanReportSecrets(reportContents)
	for _, finding := range secretScan {
		securityFindings = append(securityFindings, SecurityFinding{
			Time:           time.Now().UTC().Format(time.RFC3339Nano),
			Type:           "report_secret_scan",
			Severity:       finding.Severity,
			Target:         "report",
			TargetRedacted: "report",
			Reason:         finding.Message,
		})
	}
	securityData := map[string]any{
		"findings":      securityFindings,
		"secret_scan":   map[string]any{"status": passWarning(len(secretScan)), "findings": secretScan},
		"not_evaluated": []string{},
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "summary.json"), summary); err != nil {
		return err
	}
	if err := writeEvents(filepath.Join(a.reportDir, "events.ndjson"), events); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "final-state.json"), finalState); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "contract-coverage.json"), contractCoverage); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "endpoint-coverage.json"), endpointCoverageData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "fixture-coverage.json"), fixtureCoverageData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "business-scenario-coverage.json"), businessScenarioCoverageData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "sample-coverage.json"), sampleCoverageData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "sample-import-report.json"), sampleImportData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "sandbox-scope-boundaries.json"), scopeBoundariesData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "scenario-results.json"), scenarioResultsData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "notify-attempts.json"), notifyData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "webhook-attempts.json"), webhookData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "request-logs.json"), requestLogData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "reconciliation-files.json"), reconciliationData); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "secret-scan.json"), map[string]any{"status": passWarning(len(secretScan)), "findings": secretScan}); err != nil {
		return err
	}
	if err := writeJSONFile(filepath.Join(a.reportDir, "security-findings.json"), securityData); err != nil {
		return err
	}
	if err := writeManifest(a.reportDir); err != nil {
		return err
	}
	return nil
}

func sanitizeRequestLogForReport(log RequestLog) RequestLog {
	log.RequestEnvelope = sanitizeGatewayLogMap(log.RequestEnvelope)
	log.RequestData = sanitizeGatewayLogMap(log.RequestData)
	log.ResponseEnvelope = sanitizeGatewayLogMap(log.ResponseEnvelope)
	log.ResponseData = sanitizeGatewayLogMap(log.ResponseData)
	log.ResponseBody = sanitizePlainLogText(log.ResponseBody)
	return log
}

func sanitizeNotificationDeliveryForOutput(delivery NotificationDelivery) NotificationDelivery {
	delivery.TargetRedacted = firstNonEmpty(delivery.TargetRedacted, redactTarget(delivery.Target))
	delivery.Target = delivery.TargetRedacted
	delivery.AckBody = sanitizePlainLogText(delivery.AckBody)
	delivery.Error = sanitizePlainLogText(delivery.Error)
	delivery.Diagnosis = sanitizePlainLogText(delivery.Diagnosis)
	delivery.Attempts = append([]NotificationAttempt(nil), delivery.Attempts...)
	for i := range delivery.Attempts {
		delivery.Attempts[i].AckBody = sanitizePlainLogText(delivery.Attempts[i].AckBody)
		delivery.Attempts[i].Error = sanitizePlainLogText(delivery.Attempts[i].Error)
		delivery.Attempts[i].Diagnosis = sanitizePlainLogText(delivery.Attempts[i].Diagnosis)
	}
	return delivery
}

func sanitizeWebhookDeliveryForOutput(delivery WebhookDelivery) WebhookDelivery {
	delivery.TargetRedacted = firstNonEmpty(delivery.TargetRedacted, redactTarget(delivery.Target))
	delivery.Target = delivery.TargetRedacted
	delivery.Error = sanitizePlainLogText(delivery.Error)
	delivery.Diagnosis = sanitizePlainLogText(delivery.Diagnosis)
	delivery.Attempts = append([]WebhookAttempt(nil), delivery.Attempts...)
	for i := range delivery.Attempts {
		delivery.Attempts[i].AckBody = sanitizePlainLogText(delivery.Attempts[i].AckBody)
		delivery.Attempts[i].Error = sanitizePlainLogText(delivery.Attempts[i].Error)
		delivery.Attempts[i].Diagnosis = sanitizePlainLogText(delivery.Attempts[i].Diagnosis)
	}
	return delivery
}

func sanitizeEventsForReport(events []Event) []Event {
	out := make([]Event, len(events))
	copy(out, events)
	for i := range out {
		out[i].Endpoint = sanitizePlainLogText(out[i].Endpoint)
		out[i].EntityID = sanitizePlainLogText(out[i].EntityID)
		out[i].ScenarioID = sanitizePlainLogText(out[i].ScenarioID)
		out[i].Details = sanitizeGatewayLogMap(out[i].Details)
	}
	return out
}

func contractCoverage(bundle *ContractBundle) map[string]any {
	return map[string]any{
		"contract_bundle":             contractBundle,
		"references":                  bundle.References,
		"reference_digest_validation": referenceDigestCheck(bundle),
	}
}

func endpointCoverage(bundle *ContractBundle, scenarioResults []ScenarioResult, fixtureResults []FixtureResult) map[string]any {
	scenarioStatus := endpointScenarioStatus(scenarioResults)
	fixtureStatus := fixtureStatusMap(fixtureResults)
	items := []map[string]any{}
	for _, endpoint := range bundle.Endpoints.Endpoints {
		status := scenarioStatus[endpoint.ID]
		if status == "" {
			status = "not_executed"
		}
		items = append(items, map[string]any{
			"id":                  endpoint.ID,
			"path":                endpoint.Path,
			"status":              status,
			"request_contract":    true,
			"response_contract":   true,
			"positive_fixture":    endpoint.PositiveFixture,
			"positive_status":     defaultStatus(fixtureStatus[endpoint.PositiveFixture]),
			"negative_fixture":    endpoint.NegativeFixture,
			"negative_status":     defaultStatus(fixtureStatus[endpoint.NegativeFixture]),
			"variant_fixtures":    variantFixtureCoverage(endpoint.VariantFixtures, fixtureStatus),
			"state_event_mapping": endpoint.StateEntity != "",
			"test_assertions":     endpoint.Assertions,
		})
	}
	return map[string]any{"contract_bundle": contractBundle, "endpoints": items}
}

func fixtureCoverage(bundle *ContractBundle, fixtureResults []FixtureResult) map[string]any {
	statuses := fixtureStatusMap(fixtureResults)
	fixtures := []map[string]any{}
	for _, endpoint := range bundle.Endpoints.Endpoints {
		for _, fixtureID := range endpointFixtureIDs(endpoint) {
			fixture := bundle.Fixtures[fixtureID]
			item := map[string]any{"id": fixtureID, "endpoint": endpoint.ID, "kind": fixture.Kind, "status": defaultStatus(statuses[fixtureID])}
			addFixtureSampleMetadata(item, fixture)
			fixtures = append(fixtures, item)
		}
	}
	return map[string]any{"contract_bundle": contractBundle, "fixtures": fixtures}
}

func variantFixtureCoverage(ids []string, statuses map[string]string) []map[string]any {
	out := make([]map[string]any, 0, len(ids))
	for _, id := range ids {
		out = append(out, map[string]any{"id": id, "status": defaultStatus(statuses[id])})
	}
	return out
}

func businessScenarioCoverage(bundle *ContractBundle, scenarioResults []ScenarioResult, fixtureResults []FixtureResult) map[string]any {
	fixtureStatus := fixtureStatusMap(fixtureResults)
	scenarios := []map[string]any{}
	sampleBackedCount := 0
	for _, result := range scenarioResults {
		if !isBusinessScenarioID(result.ID) {
			continue
		}
		fixtures := []map[string]string{}
		sampleBacked := false
		for _, fixtureID := range result.FixtureIDs {
			fixtures = append(fixtures, map[string]string{"id": fixtureID, "status": defaultStatus(fixtureStatus[fixtureID])})
			if fixture := bundle.Fixtures[fixtureID]; fixture.SourceSampleID != "" {
				sampleBacked = true
			}
		}
		coverageLevel := businessCoverageLevel(result.ID)
		if sampleBacked {
			coverageLevel = "sample_backed"
			sampleBackedCount++
		}
		scenarios = append(scenarios, map[string]any{
			"id":             result.ID,
			"status":         result.Status,
			"coverage_level": coverageLevel,
			"sample_backed":  sampleBacked,
			"endpoint_ids":   result.EndpointIDs,
			"fixture_ids":    result.FixtureIDs,
			"fixtures":       fixtures,
			"events":         result.Events,
			"report_files":   result.ReportFiles,
		})
	}
	syntheticCount := len(scenarios) - sampleBackedCount
	return map[string]any{
		"contract_bundle":       contractBundle,
		"scenarios":             scenarios,
		"sample_backed_count":   sampleBackedCount,
		"synthetic_count":       syntheticCount,
		"sample_backed_percent": percent(sampleBackedCount, len(scenarios)),
	}
}

func sampleCoverage(bundle *ContractBundle, fixtureResults []FixtureResult) map[string]any {
	statuses := fixtureStatusMap(fixtureResults)
	fixtures := []map[string]any{}
	byLevel := map[string]int{}
	for _, fixture := range bundle.Fixtures {
		if fixture.SourceSampleID == "" {
			continue
		}
		item := map[string]any{
			"id":                    fixture.ID,
			"endpoint_id":           fixture.EndpointID,
			"status":                defaultStatus(statuses[fixture.ID]),
			"source_sample_id":      fixture.SourceSampleID,
			"sample_digest":         fixture.SampleDigest,
			"sample_coverage_level": fixture.SampleCoverage,
		}
		fixtures = append(fixtures, item)
		byLevel[fixture.SampleCoverage]++
	}
	sort.Slice(fixtures, func(i, j int) bool { return stringValue(fixtures[i]["id"]) < stringValue(fixtures[j]["id"]) })
	status := "sample_backed"
	if len(fixtures) == 0 {
		status = "awaiting_samples"
	}
	return map[string]any{
		"contract_bundle":         contractBundle,
		"sample_schema_version":   sampleSchemaVersion,
		"sample_importer_version": sampleImporterVersion,
		"status":                  status,
		"sample_backed_fixtures":  fixtures,
		"counts_by_level":         byLevel,
	}
}

func sampleImportReport(bundle *ContractBundle) map[string]any {
	required := []map[string]string{}
	for name, item := range bundle.References.References {
		if item.Status == "partial" && item.RemainingGapType == "requires_production_sample" {
			required = append(required, map[string]string{"reference": name, "reason": item.Reason})
		}
	}
	sort.Slice(required, func(i, j int) bool { return required[i]["reference"] < required[j]["reference"] })
	imported := 0
	for _, fixture := range bundle.Fixtures {
		if fixture.SourceSampleID != "" {
			imported++
		}
	}
	status := "passed"
	if imported == 0 && len(required) > 0 {
		status = "awaiting_samples"
	} else if len(required) > 0 {
		status = "partial"
	}
	return map[string]any{
		"contract_bundle":                  contractBundle,
		"sample_schema_version":            sampleSchemaVersion,
		"sample_importer_version":          sampleImporterVersion,
		"status":                           status,
		"imported_sample_backed_fixtures":  imported,
		"requires_production_sample_count": len(required),
		"requires_production_sample":       required,
		"raw_samples_embedded":             false,
		"raw_samples_in_public_release":    false,
	}
}

func addFixtureSampleMetadata(item map[string]any, fixture FixtureDefinition) {
	if fixture.SourceSampleID == "" {
		return
	}
	item["source_sample_id"] = fixture.SourceSampleID
	item["sample_digest"] = fixture.SampleDigest
	item["sample_coverage_level"] = fixture.SampleCoverage
}

func isBusinessScenarioID(id string) bool {
	for _, prefix := range []string{"AGG-CHANNEL-", "AGG-TX-META", "AGG-SPLIT-", "AGG-COMBINED-", "AGG-FEE-", "AGG-REFUND-CHANNEL", "AGG-CLOSE-CHANNEL", "HOST-H5-", "HOST-MINI-", "HOST-DY-", "HOST-LARGEAMT", "HOST-TERMINAL", "HOST-CHANNEL-COMBO", "HOST-REFUND-CHANNEL", "HOST-CLOSE-CHANNEL", "CHANNEL-NOTIFY", "RECON-BILL-TYPES", "RECON-DOWNLOAD-EDGES", "ERROR-FIELDS"} {
		if strings.HasPrefix(id, prefix) {
			return true
		}
	}
	return false
}

func businessCoverageLevel(id string) string {
	switch {
	case strings.HasPrefix(id, "CHANNEL-NOTIFY"), strings.HasPrefix(id, "ERROR-FIELDS"):
		return "synthetic_exact"
	case strings.HasPrefix(id, "RECON-DOWNLOAD-EDGES"):
		return "synthetic_representative"
	default:
		return "synthetic_representative"
	}
}

func sandboxScopeBoundaries(bundle *ContractBundle) map[string]any {
	var checkout []map[string]string
	var notSandboxable []map[string]string
	for name, item := range bundle.References.References {
		entry := map[string]string{"reference": name, "status": item.Status, "reason": item.Reason}
		if strings.Contains(name, "checkout") || name == "shared-frontend-sdk-matrix.md" {
			checkout = append(checkout, entry)
		}
		if item.Status == "not_sandboxable" {
			notSandboxable = append(notSandboxable, entry)
		}
	}
	sort.Slice(checkout, func(i, j int) bool { return checkout[i]["reference"] < checkout[j]["reference"] })
	sort.Slice(notSandboxable, func(i, j int) bool { return notSandboxable[i]["reference"] < notSandboxable[j]["reference"] })
	return map[string]any{
		"contract_bundle": contractBundle,
		"boundaries": []map[string]any{
			{"id": "checkout", "status": "not_sandboxable", "reason": "Checkout frontend/component integration does not need local-sandbox coverage; only hosting preorder/query/notify prerequisites are simulated.", "references": checkout},
			{"id": "merchant_onboarding", "status": "not_sandboxable", "reason": "Merchant onboarding, interface permissions, channel configuration, appid/openid binding, and go-live approvals require official/business systems."},
			{"id": "commercial_policy", "status": "not_sandboxable", "reason": "Fees, compliance, policy approval, risk controls, and channel admission cannot be validated locally."},
			{"id": "real_funds_and_production_files", "status": "not_sandboxable", "reason": "Real fund movement, production routing, and production reconciliation files are never produced by this synthetic sandbox."},
		},
		"not_sandboxable_references": notSandboxable,
	}
}

func endpointScenarioStatus(results []ScenarioResult) map[string]string {
	out := map[string]string{}
	for _, result := range results {
		for _, endpointID := range result.EndpointIDs {
			if result.Status == "failed" {
				out[endpointID] = "failed"
				continue
			}
			if result.Status == "passed" && out[endpointID] == "" {
				out[endpointID] = "covered"
			}
		}
	}
	return out
}

func fixtureStatusMap(results []FixtureResult) map[string]string {
	out := map[string]string{}
	for _, result := range results {
		if result.Status == "failed" {
			out[result.ID] = "failed"
			continue
		}
		if result.Status == "passed" && out[result.ID] == "" {
			out[result.ID] = "covered"
		}
	}
	return out
}

func defaultStatus(value string) string {
	if value == "" {
		return "not_executed"
	}
	return value
}

func writeJSONFile(path string, value any) error {
	b, err := json.MarshalIndent(value, "", "  ")
	if err != nil {
		return err
	}
	b = append(b, '\n')
	return os.WriteFile(path, b, 0o600)
}

func marshalReportContents(values map[string]any) (map[string][]byte, error) {
	out := map[string][]byte{}
	for name, value := range values {
		b, err := json.MarshalIndent(value, "", "  ")
		if err != nil {
			return nil, err
		}
		out[name] = b
	}
	return out, nil
}

func passWarning(count int) string {
	if count == 0 {
		return "pass"
	}
	return "warning"
}

func percent(part, total int) float64 {
	if total == 0 {
		return 0
	}
	return float64(part) * 100 / float64(total)
}

func writeEvents(path string, events []Event) error {
	f, err := os.OpenFile(path, os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0o600)
	if err != nil {
		return err
	}
	defer f.Close()
	enc := json.NewEncoder(f)
	for _, event := range events {
		if err := enc.Encode(event); err != nil {
			return err
		}
	}
	return nil
}

func writeManifest(dir string) error {
	entries, err := os.ReadDir(dir)
	if err != nil {
		return err
	}
	manifest := map[string]string{}
	for _, entry := range entries {
		if entry.IsDir() || entry.Name() == "report-manifest.json" {
			continue
		}
		path := filepath.Join(dir, entry.Name())
		b, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		sum := sha256.Sum256(b)
		manifest[entry.Name()] = "sha256:" + hex.EncodeToString(sum[:])
	}
	names := make([]string, 0, len(manifest))
	for name := range manifest {
		names = append(names, name)
	}
	sort.Strings(names)
	ordered := []map[string]string{}
	for _, name := range names {
		ordered = append(ordered, map[string]string{"file": name, "sha256": manifest[name]})
	}
	return writeJSONFile(filepath.Join(dir, "report-manifest.json"), map[string]any{
		"generated_at": time.Now().UTC().Format(time.RFC3339Nano),
		"files":        ordered,
		"note":         "local-sandbox report manifest; not an official certification",
	})
}

func reportMarkdown(app *App) string {
	return fmt.Sprintf("# local-sandbox report\n\nrun_id: `%s`\n\ncontract_bundle: `%s`\n", app.runID, contractBundle)
}

type ReportBundle struct {
	Dir                      string         `json:"dir"`
	Summary                  map[string]any `json:"summary"`
	EndpointCoverage         map[string]any `json:"endpoint_coverage"`
	FixtureCoverage          map[string]any `json:"fixture_coverage"`
	BusinessScenarioCoverage map[string]any `json:"business_scenario_coverage"`
	SampleCoverage           map[string]any `json:"sample_coverage"`
	SampleImportReport       map[string]any `json:"sample_import_report"`
	ScopeBoundaries          map[string]any `json:"sandbox_scope_boundaries"`
	ScenarioResults          map[string]any `json:"scenario_results"`
	SecurityFindings         map[string]any `json:"security_findings"`
	Manifest                 map[string]any `json:"manifest"`
}

func loadReportBundle(dir string) (*ReportBundle, error) {
	if err := validateReportManifest(dir); err != nil {
		return nil, err
	}
	bundle := &ReportBundle{Dir: dir}
	if err := readReportJSON(filepath.Join(dir, "summary.json"), &bundle.Summary); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "endpoint-coverage.json"), &bundle.EndpointCoverage); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "fixture-coverage.json"), &bundle.FixtureCoverage); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "business-scenario-coverage.json"), &bundle.BusinessScenarioCoverage); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "sample-coverage.json"), &bundle.SampleCoverage); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "sample-import-report.json"), &bundle.SampleImportReport); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "sandbox-scope-boundaries.json"), &bundle.ScopeBoundaries); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "scenario-results.json"), &bundle.ScenarioResults); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "security-findings.json"), &bundle.SecurityFindings); err != nil {
		return nil, err
	}
	if err := readReportJSON(filepath.Join(dir, "report-manifest.json"), &bundle.Manifest); err != nil {
		return nil, err
	}
	return bundle, nil
}

func validateReportManifest(dir string) error {
	var manifest struct {
		Files []struct {
			File   string `json:"file"`
			SHA256 string `json:"sha256"`
		} `json:"files"`
	}
	if err := readReportJSON(filepath.Join(dir, "report-manifest.json"), &manifest); err != nil {
		return err
	}
	if len(manifest.Files) == 0 {
		return fmt.Errorf("report manifest has no files")
	}
	for _, item := range manifest.Files {
		if item.File == "" || item.SHA256 == "" {
			return fmt.Errorf("report manifest contains invalid file entry")
		}
		if filepath.Base(item.File) != item.File {
			return fmt.Errorf("report manifest file must be a basename: %s", item.File)
		}
		path := filepath.Join(dir, item.File)
		b, err := os.ReadFile(path)
		if err != nil {
			return fmt.Errorf("read report file %s: %w", item.File, err)
		}
		sum := sha256.Sum256(b)
		got := "sha256:" + hex.EncodeToString(sum[:])
		if got != item.SHA256 {
			return fmt.Errorf("report manifest hash mismatch for %s", item.File)
		}
	}
	return nil
}

func renderReportBundle(bundle *ReportBundle, format string) ([]byte, error) {
	switch format {
	case "json":
		return json.MarshalIndent(map[string]any{
			"ok":                         true,
			"ops_cli_schema":             opsCLISchemaVersion,
			"report_dir":                 bundle.Dir,
			"summary":                    bundle.Summary,
			"endpoint_coverage":          bundle.EndpointCoverage,
			"fixture_coverage":           bundle.FixtureCoverage,
			"business_scenario_coverage": bundle.BusinessScenarioCoverage,
			"sample_coverage":            bundle.SampleCoverage,
			"sample_import_report":       bundle.SampleImportReport,
			"sandbox_scope_boundaries":   bundle.ScopeBoundaries,
			"scenario_results":           bundle.ScenarioResults,
			"security_findings":          bundle.SecurityFindings,
			"manifest":                   bundle.Manifest,
		}, "", "  ")
	case "md":
		return []byte(reportBundleMarkdown(bundle)), nil
	case "html":
		return []byte(reportBundleHTML(bundle)), nil
	default:
		return nil, fmt.Errorf("unsupported report format %s", format)
	}
}

func reportBundleMarkdown(bundle *ReportBundle) string {
	summary := bundle.Summary
	return fmt.Sprintf("# local-sandbox report\n\nrun_id: `%s`\n\nversion: `%s`\n\ncontract_bundle: `%s`\n\nreport_dir: `%s`\n\nscenario_results: `%d passed / %d failed`\n",
		stringValue(summary["run_id"]),
		stringValue(summary["version"]),
		stringValue(summary["contract_bundle"]),
		bundle.Dir,
		countScenarioStatus(bundle.ScenarioResults, "passed"),
		countScenarioStatus(bundle.ScenarioResults, "failed"),
	)
}

func reportBundleHTML(bundle *ReportBundle) string {
	summary := bundle.Summary
	return fmt.Sprintf("<!doctype html><title>local-sandbox report</title><h1>local-sandbox report</h1><dl><dt>run_id</dt><dd>%s</dd><dt>version</dt><dd>%s</dd><dt>contract_bundle</dt><dd>%s</dd><dt>report_dir</dt><dd>%s</dd></dl>",
		stringValue(summary["run_id"]),
		stringValue(summary["version"]),
		stringValue(summary["contract_bundle"]),
		bundle.Dir,
	)
}

func countScenarioStatus(data map[string]any, status string) int {
	raw, ok := data["scenarios"].([]any)
	if !ok {
		return 0
	}
	count := 0
	for _, item := range raw {
		scenario, ok := item.(map[string]any)
		if ok && stringValue(scenario["status"]) == status {
			count++
		}
	}
	return count
}

func readReportJSON(path string, out any) error {
	b, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	if err := json.Unmarshal(b, out); err != nil {
		return fmt.Errorf("decode %s: %w", filepath.Base(path), err)
	}
	return nil
}
