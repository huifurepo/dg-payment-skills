package main

import (
	"context"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"net/url"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"runtime"
	"strings"
	"syscall"
	"time"
)

func main() {
	if err := run(os.Args[1:]); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(exitCode(err))
	}
}

func run(args []string) error {
	if len(args) == 0 {
		printUsage()
		return nil
	}
	switch args[0] {
	case "serve":
		return runServe(args[1:])
	case "version":
		return runVersion(args[1:])
	case "doctor":
		return runDoctor(args[1:])
	case "validate":
		return runValidate(args[1:])
	case "credentials":
		return runCredentials(args[1:])
	case "report":
		return runReport(args[1:])
	case "purge":
		return runPurge(args[1:])
	case "replay":
		return runReplay(args[1:])
	case "-h", "--help", "help":
		printUsage()
		return nil
	default:
		return usageError("unknown command " + args[0])
	}
}

func runServe(args []string) error {
	fs := flag.NewFlagSet("serve", flag.ContinueOnError)
	fs.SetOutput(os.Stderr)
	open := fs.Bool("open", false, "")
	noOpen := fs.Bool("no-open", false, "")
	controlPort := fs.Int("control-port", 8765, "")
	gatewayHost := fs.String("gateway-host", "127.0.0.1", "")
	gatewayPort := fs.Int("gateway-port", 8766, "")
	profile := fs.String("profile", "strict", "")
	mode := fs.String("mode", "local-simulation", "")
	credentialProfile := fs.String("credential-profile", "", "")
	officialGatewayURL := fs.String("official-gateway-url", "", "")
	dataDir := fs.String("data-dir", "", "")
	reportDir := fs.String("report-dir", "", "")
	printJSON := fs.Bool("print-json", false, "")
	ephemeral := fs.Bool("ephemeral", false, "")
	disableAdmin := fs.Bool("disable-admin", false, "")
	unsafeExposeGateway := fs.Bool("unsafe-expose-gateway", false, "")
	updateIndexURL := fs.String("update-index-url", defaultUpdateIndexURL, "")
	_ = fs.String("scenario", "", "")
	_ = fs.String("log-format", "text", "")
	_ = fs.String("log-level", "info", "")
	webhookEndpointKey := fs.String("webhook-endpoint-key", "", "")
	var notifyAllows repeatedFlag
	fs.Var(&notifyAllows, "notify-allow", "exact URL allowlist")
	var webhookTargets repeatedFlag
	fs.Var(&webhookTargets, "webhook-target", "local webhook target URL")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *profile != "strict" && *profile != "local-dev" {
		return usageError("--profile must be strict or local-dev")
	}
	if *mode != "local-simulation" && *mode != "official-proxy" {
		return usageError("--mode must be local-simulation or official-proxy")
	}
	if *mode == "official-proxy" {
		if strings.TrimSpace(*credentialProfile) == "" {
			return usageError("--mode official-proxy requires --credential-profile")
		}
		if err := validateOfficialGatewayURL(*officialGatewayURL); err != nil {
			return err
		}
	}
	if *credentialProfile != "" && *unsafeExposeGateway {
		return securityError("--credential-profile requires loopback gateway; do not use --unsafe-expose-gateway")
	}
	if !isLoopbackHost(*gatewayHost) && !*unsafeExposeGateway {
		return securityError("non-loopback gateway requires --unsafe-expose-gateway")
	}
	if !isLoopbackHost(*gatewayHost) {
		fmt.Fprintln(os.Stderr, "[security] WARNING: gateway bound to non-loopback host", *gatewayHost, "- network-reachable; ensure only trusted clients can reach it")
	}
	app, err := NewAppWithOptions(AppOptions{
		DataDir:           *dataDir,
		ReportDir:         *reportDir,
		Ephemeral:         *ephemeral,
		CredentialProfile: *credentialProfile,
		Mode:              *mode,
		OfficialGateway:   *officialGatewayURL,
		UpdateIndexURL:    *updateIndexURL,
	})
	if err != nil {
		return err
	}
	if *webhookEndpointKey != "" {
		if err := app.setWebhookEndpointKey(*webhookEndpointKey); err != nil {
			return err
		}
	}
	for _, raw := range notifyAllows {
		if err := app.addNotifyAllow(raw); err != nil {
			return err
		}
	}
	for _, raw := range webhookTargets {
		if err := app.addWebhookTarget(raw); err != nil {
			return err
		}
	}
	if *disableAdmin {
		app.adminDisabled = true
		app.adminToken = ""
	}

	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()
	app.shutdown = cancel
	_, controlListener, err := startHTTPServer(ctx, "127.0.0.1", *controlPort, app.controlHandler())
	if err != nil {
		return err
	}
	_, gatewayListener, err := startHTTPServer(ctx, *gatewayHost, *gatewayPort, app.gatewayHandler())
	if err != nil {
		cancel()
		return err
	}
	controlURL := "http://" + controlListener.Addr().String()
	gatewayURL := "http://" + gatewayListener.Addr().String()
	app.controlBaseURL = controlURL
	app.gatewayBaseURL = gatewayURL
	if *printJSON {
		ready := map[string]any{
			"event":                "ready",
			"name":                 appName,
			"version":              appVersion,
			"skill_source":         skillSource,
			"sandbox_skill_source": sandboxSkillSource,
			"contract_bundle":      contractBundle,
			"contract_digest":      app.bundle.Digest,
			"control_url":          controlURL,
			"gateway_url":          gatewayURL,
			"health_url":           controlURL + "/__health/ready",
			"data_dir":             app.dataDir,
			"report_dir":           app.reportDir,
			"run_id":               app.runID,
			"mode":                 app.mode,
			"credential_profile":   firstNonEmpty(app.creds.ProfileName, "synthetic"),
			"signature_model":      firstNonEmpty(app.creds.SignatureModel, "synthetic-dual-key"),
			"admin_token":          app.adminToken,
			"csrf_token":           app.csrfToken,
			"webhook_endpoint_key": app.webhookEndpointKeySnapshot(),
			"update_index_url":     app.updateIndexURL,
		}
		_ = json.NewEncoder(os.Stdout).Encode(ready)
	} else {
		fmt.Fprintf(os.Stderr, "%s %s ready\nControl: %s\nGateway: %s\n", appName, appVersion, controlURL, gatewayURL)
		if app.adminDisabled {
			fmt.Fprintln(os.Stderr, "Admin: disabled")
		} else {
			fmt.Fprintf(os.Stderr, "Admin token: %s\n", app.adminToken)
			fmt.Fprintln(os.Stderr, "Keep this window open while testing. Press Ctrl+C to stop.")
		}
	}
	if *open && !*noOpen {
		if err := openBrowser(controlURL); err != nil {
			fmt.Fprintf(os.Stderr, "open browser failed: %v\n", err)
		}
	}
	<-ctx.Done()
	if err := app.WriteReport(); err != nil {
		return err
	}
	return nil
}

func openBrowser(target string) error {
	if strings.TrimSpace(target) == "" {
		return usageError("browser target is required")
	}
	var candidates [][]string
	switch runtime.GOOS {
	case "windows":
		candidates = [][]string{{"rundll32", "url.dll,FileProtocolHandler", target}}
	case "darwin":
		candidates = [][]string{{"open", target}}
	default:
		candidates = [][]string{{"xdg-open", target}, {"gio", "open", target}, {"sensible-browser", target}}
	}
	var lastErr error
	for _, item := range candidates {
		cmd := exec.Command(item[0], item[1:]...)
		if err := cmd.Start(); err != nil {
			lastErr = err
			continue
		}
		return nil
	}
	if lastErr == nil {
		lastErr = errors.New("no browser opener configured")
	}
	return lastErr
}

func runVersion(args []string) error {
	fs := flag.NewFlagSet("version", flag.ContinueOnError)
	asJSON := fs.Bool("json", false, "")
	if err := fs.Parse(args); err != nil {
		return err
	}
	bundle, err := loadContractBundle()
	if err != nil {
		return err
	}
	if *asJSON {
		return json.NewEncoder(os.Stdout).Encode(map[string]any{
			"name":                            appName,
			"version":                         appVersion,
			"os_arch":                         runtimeOSArch(),
			"contract_bundle":                 contractBundle,
			"contract_digest":                 bundle.Digest,
			"source_skill_version":            skillVersion,
			"skill_source":                    skillSource,
			"sandbox_skill_source":            sandboxSkillSource,
			"report_schema_version":           reportSchema,
			"scenario_schema_version":         scenarioSchema,
			"signing_profile":                 signingProfile,
			"golden_vector_version":           goldenVectorVersion,
			"release_evidence_schema_version": releaseEvidenceSchemaVersion,
			"source_archive_schema_version":   sourceArchiveSchemaVersion,
			"coverage_runner_version":         coverageRunnerVersion,
			"reference_digest_schema_version": referenceDigestSchemaVersion,
			"fixture_runner_version":          fixtureRunnerVersion,
			"ops_cli_schema_version":          opsCLISchemaVersion,
			"sample_schema_version":           sampleSchemaVersion,
			"sample_importer_version":         sampleImporterVersion,
			"build_commit":                    buildCommit,
			"build_time":                      buildTime,
			"build_dirty":                     buildDirtyBool(),
			"release_channel":                 releaseChannel,
			"code_signed":                     false,
			"notarized":                       false,
		})
	}
	fmt.Println(appVersion)
	return nil
}

func runDoctor(args []string) error {
	fs := flag.NewFlagSet("doctor", flag.ContinueOnError)
	asJSON := fs.Bool("json", false, "")
	if err := fs.Parse(args); err != nil {
		return err
	}
	bundle, err := loadContractBundle()
	if err != nil {
		return err
	}
	problems := validateContractBundle(bundle)
	result := map[string]any{
		"ok":              len(problems) == 0,
		"version":         appVersion,
		"contract_bundle": contractBundle,
		"contract_digest": bundle.Digest,
		"problems":        problems,
		"network_checked": false,
	}
	if *asJSON {
		return json.NewEncoder(os.Stdout).Encode(result)
	}
	if len(problems) > 0 {
		return fmt.Errorf(strings.Join(problems, "; "))
	}
	fmt.Println("OK")
	return nil
}

func runValidate(args []string) error {
	if len(args) == 0 {
		return usageError("validate requires contract, report, or code")
	}
	switch args[0] {
	case "contract":
		bundle, err := loadContractBundle()
		if err != nil {
			return err
		}
		if problems := validateContractBundle(bundle); len(problems) > 0 {
			return contractError(strings.Join(problems, "; "))
		}
		return json.NewEncoder(os.Stdout).Encode(map[string]any{"ok": true, "contract_bundle": contractBundle, "contract_digest": bundle.Digest})
	case "report":
		fs := flag.NewFlagSet("validate report", flag.ContinueOnError)
		path := fs.String("path", "", "")
		if err := fs.Parse(args[1:]); err != nil {
			return err
		}
		if *path == "" {
			return usageError("--path is required")
		}
		for _, name := range []string{"summary.json", "events.ndjson", "final-state.json", "contract-coverage.json", "endpoint-coverage.json", "fixture-coverage.json", "business-scenario-coverage.json", "sample-coverage.json", "sample-import-report.json", "sandbox-scope-boundaries.json", "scenario-results.json", "notify-attempts.json", "webhook-attempts.json", "reconciliation-files.json", "security-findings.json", "secret-scan.json", "report-manifest.json"} {
			if !fileExists(filepath.Join(*path, name)) {
				return contractError("report missing " + name)
			}
		}
		if err := validateReportManifest(*path); err != nil {
			return contractError(err.Error())
		}
		return json.NewEncoder(os.Stdout).Encode(map[string]any{"ok": true, "path": *path})
	case "scenarios":
		fs := flag.NewFlagSet("validate scenarios", flag.ContinueOnError)
		reportDir := fs.String("report-dir", "", "")
		printJSON := fs.Bool("print-json", false, "")
		if err := fs.Parse(args[1:]); err != nil {
			return err
		}
		if *reportDir == "" {
			return usageError("--report-dir is required")
		}
		result, err := runScenarioValidation(*reportDir)
		if *printJSON {
			_ = json.NewEncoder(os.Stdout).Encode(result)
		}
		return err
	case "code":
		fs := flag.NewFlagSet("validate code", flag.ContinueOnError)
		path := fs.String("path", ".", "")
		if err := fs.Parse(args[1:]); err != nil {
			return err
		}
		findings, err := scanCodeAdvisories(*path)
		if err != nil {
			return err
		}
		status := "pass"
		if len(findings) > 0 {
			status = "warning"
		}
		return json.NewEncoder(os.Stdout).Encode(map[string]any{
			"status":        status,
			"advisory_only": true,
			"path":          *path,
			"findings":      findings,
		})
	default:
		return usageError("unknown validate target " + args[0])
	}
}

func runCredentials(args []string) error {
	if len(args) == 0 {
		return usageError("credentials requires show, show-profile, export, or rotate")
	}
	fs := flag.NewFlagSet("credentials "+args[0], flag.ContinueOnError)
	dataDir := fs.String("data-dir", "", "")
	format := fs.String("format", "json", "")
	output := fs.String("output", "", "")
	credentialProfile := fs.String("credential-profile", "", "")
	allowPrivateExport := fs.Bool("allow-private-export", false, "")
	name := fs.String("name", "", "")
	if err := fs.Parse(args[1:]); err != nil {
		return err
	}
	if *dataDir == "" {
		*dataDir = defaultDataDir()
	}
	switch args[0] {
	case "show":
		creds, err := loadOrCreateCredentialsProfile(*dataDir, false, *credentialProfile)
		if err != nil {
			return err
		}
		result := map[string]any{
			"watermark":                   credentialWatermark(creds),
			"directory":                   creds.Directory,
			"merchant_public_fingerprint": publicKeyFingerprint(creds.MerchantPublic),
			"gateway_public_fingerprint":  publicKeyFingerprint(creds.GatewayPublic),
		}
		for key, value := range credentialProfileSummary(creds) {
			result[key] = value
		}
		return json.NewEncoder(os.Stdout).Encode(result)
	case "show-profile":
		profileName := firstNonEmpty(*name, *credentialProfile)
		if profileName == "" && fs.NArg() > 0 {
			profileName = fs.Arg(0)
		}
		if profileName == "" {
			profileName = officialDemoProfileName
		}
		creds, err := loadOrCreateCredentialsProfile(*dataDir, false, profileName)
		if err != nil {
			return err
		}
		return json.NewEncoder(os.Stdout).Encode(credentialProfileSummary(creds))
	case "export":
		creds, err := loadOrCreateCredentialsProfile(*dataDir, false, *credentialProfile)
		if err != nil {
			return err
		}
		if *format != "json" && *format != "env" {
			return usageError("--format must be json or env")
		}
		if creds.ProfileName == officialDemoProfileName && !*allowPrivateExport {
			return usageError(officialDemoMerchantKeyWarning)
		}
		content := ""
		if *format == "env" {
			content = fmt.Sprintf(
				"HUIFU_SANDBOX_PROFILE=%q\nHUIFU_SANDBOX_SIGNATURE_MODEL=%q\nHUIFU_SANDBOX_SKILL_SOURCE=%q\nHUIFU_SANDBOX_SYS_ID=%q\nHUIFU_SANDBOX_PRODUCT_ID=%q\nHUIFU_SANDBOX_MERCHANT_PRIVATE_KEY=%q\nHUIFU_SANDBOX_MERCHANT_PUBLIC_KEY=%q\n",
				firstNonEmpty(creds.ProfileName, "synthetic"),
				firstNonEmpty(creds.SignatureModel, "synthetic-dual-key"),
				sandboxSkillSource,
				creds.SysID,
				creds.ProductID,
				privateKeyPKCS8Base64(creds.MerchantPrivate),
				publicKeyPKIXBase64(creds.GatewayPublic),
			)
		} else {
			b, _ := json.MarshalIndent(credentialExportPayload(creds, "", ""), "", "  ")
			content = string(b) + "\n"
		}
		if *output != "" {
			return os.WriteFile(*output, []byte(content), 0o600)
		}
		fmt.Print(content)
		return nil
	case "rotate":
		if *credentialProfile != "" {
			return usageError("rotate is only supported for synthetic local credentials")
		}
		dir := filepath.Join(*dataDir, "credentials")
		_ = os.Remove(filepath.Join(dir, "merchant-sandbox-private.pem"))
		_ = os.Remove(filepath.Join(dir, "gateway-sandbox-private.pem"))
		_, err := loadOrCreateCredentials(*dataDir, false)
		return err
	default:
		return usageError("unknown credentials command " + args[0])
	}
}

func validateOfficialGatewayURL(raw string) error {
	if strings.TrimSpace(raw) == "" {
		return usageError("--mode official-proxy requires --official-gateway-url")
	}
	parsed, err := url.Parse(raw)
	if err != nil || parsed.Scheme == "" || parsed.Host == "" {
		return usageError("--official-gateway-url must be an absolute URL")
	}
	if parsed.Scheme != "https" {
		return usageError("--official-gateway-url must use https")
	}
	host := strings.ToLower(parsed.Hostname())
	if !isAllowedOfficialGatewayHost(host) {
		return securityError("--official-gateway-url host is not in the official Huifu allowlist")
	}
	return nil
}

func isAllowedOfficialGatewayHost(host string) bool {
	if host == "huifu.com" || host == "huifu.com.cn" || host == "cloudpnr.com" {
		return true
	}
	for _, suffix := range []string{".huifu.com", ".huifu.com.cn", ".cloudpnr.com"} {
		if strings.HasSuffix(host, suffix) && len(host) > len(suffix) {
			return true
		}
	}
	return false
}

func runReport(args []string) error {
	fs := flag.NewFlagSet("report", flag.ContinueOnError)
	dataDir := fs.String("data-dir", defaultDataDir(), "")
	reportDir := fs.String("report-dir", "", "")
	runID := fs.String("run-id", "", "")
	format := fs.String("format", "json", "")
	output := fs.String("output", "", "")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *reportDir == "" {
		if *runID == "" {
			return usageError("--report-dir or --run-id is required")
		}
		path, err := safeRunPath(*dataDir, *runID)
		if err != nil {
			return err
		}
		*reportDir = path
	}
	if *format != "json" && *format != "md" && *format != "html" {
		return usageError("--format must be json, md, or html")
	}
	bundle, err := loadReportBundle(*reportDir)
	if err != nil {
		return err
	}
	content, err := renderReportBundle(bundle, *format)
	if err != nil {
		return err
	}
	if *output != "" {
		return os.WriteFile(*output, content, 0o600)
	}
	fmt.Print(string(content))
	return nil
}

func runPurge(args []string) error {
	fs := flag.NewFlagSet("purge", flag.ContinueOnError)
	dataDir := fs.String("data-dir", defaultDataDir(), "")
	runID := fs.String("run-id", "", "")
	olderThan := fs.String("older-than", "", "")
	dryRun := fs.Bool("dry-run", false, "")
	printJSON := fs.Bool("print-json", false, "")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *runID == "" && *olderThan == "" {
		return usageError("--run-id or --older-than is required")
	}
	result, err := purgeRuns(*dataDir, *runID, *olderThan, *dryRun)
	if *printJSON {
		_ = json.NewEncoder(os.Stdout).Encode(result)
	}
	if err != nil {
		return err
	}
	if !*printJSON {
		fmt.Fprintf(os.Stdout, "purge matched=%d deleted=%d dry_run=%t\n", result.Matched, result.Deleted, result.DryRun)
	}
	return nil
}

func runReplay(args []string) error {
	fs := flag.NewFlagSet("replay", flag.ContinueOnError)
	kind := fs.String("kind", "notify", "")
	target := fs.String("target", "", "")
	eventType := fs.String("event-type", webhookEventPayment, "")
	webhookEndpointKey := fs.String("webhook-endpoint-key", "", "")
	dataDir := fs.String("data-dir", "", "")
	reportDir := fs.String("report-dir", "", "")
	printJSON := fs.Bool("print-json", false, "")
	attempts := fs.Int("attempts", 4, "")
	retryMS := fs.Int("retry-ms", 0, "")
	var notifyAllows repeatedFlag
	fs.Var(&notifyAllows, "notify-allow", "exact URL allowlist")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *target == "" {
		return usageError("--target is required")
	}
	app, err := NewApp(*dataDir, *reportDir, true)
	if err != nil {
		return err
	}
	if *webhookEndpointKey != "" {
		if err := app.setWebhookEndpointKey(*webhookEndpointKey); err != nil {
			return err
		}
	}
	for _, raw := range notifyAllows {
		if err := app.addNotifyAllow(raw); err != nil {
			return err
		}
	}
	app.notifyMaxAttempt = *attempts
	app.notifyRetryDelay = time.Duration(*retryMS) * time.Millisecond
	payment := Payment{
		Kind:       "aggregation",
		HuifuID:    "6666000100000001",
		ReqDate:    nowDate(),
		ReqSeqID:   nextID("REPLAY"),
		HFSeqID:    nextID("HF"),
		TransAmt:   "0.01",
		GoodsDesc:  "local sandbox replay",
		NotifyURL:  *target,
		State:      "S",
		QueryCount: 1,
	}
	var delivery any
	var deliveryErr error
	switch *kind {
	case "notify":
		delivery, deliveryErr = app.deliverNotification(payment, *target, false)
	case "webhook":
		payload := paymentWebhookPayload(payment)
		payload["event_type"] = *eventType
		delivery, deliveryErr = app.deliverWebhook(*target, *eventType, payment.ReqSeqID, payload)
	default:
		return usageError("--kind must be notify or webhook")
	}
	reportErr := app.WriteReport()
	if *printJSON {
		_ = json.NewEncoder(os.Stdout).Encode(map[string]any{
			"ok":       deliveryErr == nil,
			"delivery": replayDeliveryResponse(delivery),
			"error":    errorString(deliveryErr),
		})
	}
	if deliveryErr != nil {
		return deliveryErr
	}
	return reportErr
}

func replayDeliveryResponse(delivery any) any {
	switch typed := delivery.(type) {
	case NotificationDelivery:
		return adminNotificationDeliveryResponse(typed)
	case WebhookDelivery:
		return adminWebhookDeliveryResponse(typed)
	default:
		return delivery
	}
}

func printUsage() {
	fmt.Fprintln(os.Stderr, "usage: hf-payment-local-sandbox <serve|version|doctor|validate|credentials|report|purge|replay>")
}

func runtimeOSArch() string {
	return runtime.GOOS + "/" + runtime.GOARCH
}

type codedError struct {
	code int
	err  string
}

func (e codedError) Error() string { return e.err }

func usageError(msg string) error    { return codedError{code: 2, err: msg} }
func securityError(msg string) error { return codedError{code: 6, err: msg} }
func contractError(msg string) error { return codedError{code: 7, err: msg} }
func phaseError(msg string) error    { return codedError{code: 1, err: msg} }

type repeatedFlag []string

func (f *repeatedFlag) String() string {
	return strings.Join(*f, ",")
}

func (f *repeatedFlag) Set(value string) error {
	*f = append(*f, value)
	return nil
}

func errorString(err error) string {
	if err == nil {
		return ""
	}
	return sanitizePlainLogText(err.Error())
}

func exitCode(err error) int {
	var coded codedError
	if errors.As(err, &coded) {
		return coded.code
	}
	return 1
}
