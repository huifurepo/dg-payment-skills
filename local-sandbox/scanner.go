package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

type AdvisoryFinding struct {
	File     string `json:"file"`
	Line     int    `json:"line"`
	Rule     string `json:"rule"`
	Severity string `json:"severity"`
	Message  string `json:"message"`
}

type SecretScanFinding struct {
	Rule     string `json:"rule"`
	Severity string `json:"severity"`
	Message  string `json:"message"`
}

var advisoryRules = []struct {
	id       string
	severity string
	message  string
	pattern  *regexp.Regexp
}{
	{"private-key", "high", "private key material appears in source", regexp.MustCompile(`(?i)BEGIN [A-Z ]*PRIVATE KEY`)},
	{"hardcoded-secret", "high", "hardcoded token/secret/password-like assignment", regexp.MustCompile(`(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*["'][^"']{8,}["']`)},
	{"tls-insecure-skip-verify", "high", "TLS certificate verification is disabled", regexp.MustCompile(`InsecureSkipVerify\s*:\s*true`)},
	{"hardcoded-huifu-production-url", "medium", "hardcoded Huifu-like production URL should be configurable", regexp.MustCompile(`(?i)https?://[^"'\s]*(huifu|huifupay)[^"'\s]*`)},
	{"self-maintained-payment-client", "medium", "self-maintained payment client wrapper may conflict with Skill-generated code constraints", regexp.MustCompile(`\b(HostingClient|AggregationClient)\b`)},
}

var reportSecretRules = []struct {
	id       string
	severity string
	message  string
	pattern  *regexp.Regexp
}{
	{"private-key", "high", "report contains private key material", regexp.MustCompile(`(?i)BEGIN [A-Z ]*PRIVATE KEY`)},
	{"query-secret", "high", "report contains an unredacted query secret", regexp.MustCompile(`(?i)[?&](token|secret|password|api[_-]?key)=([^&"\s]+)`)},
	{"authorization-header", "high", "report contains an authorization header value", regexp.MustCompile(`(?i)authorization"\s*:\s*"[^"]+`)},
}

func scanCodeAdvisories(root string) ([]AdvisoryFinding, error) {
	if root == "" {
		root = "."
	}
	var findings []AdvisoryFinding
	err := filepath.WalkDir(root, func(path string, entry os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if entry.IsDir() {
			if shouldSkipScanDir(entry.Name()) {
				return filepath.SkipDir
			}
			return nil
		}
		if !isScannableFile(path) {
			return nil
		}
		fileFindings, err := scanAdvisoryFile(path)
		if err != nil {
			return err
		}
		findings = append(findings, fileFindings...)
		return nil
	})
	return findings, err
}

func scanAdvisoryFile(path string) ([]AdvisoryFinding, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	var findings []AdvisoryFinding
	scanner := bufio.NewScanner(file)
	scanner.Buffer(make([]byte, 0, 64*1024), 1024*1024)
	lineNo := 0
	for scanner.Scan() {
		lineNo++
		line := scanner.Text()
		for _, rule := range advisoryRules {
			if rule.pattern.MatchString(line) {
				findings = append(findings, AdvisoryFinding{
					File:     path,
					Line:     lineNo,
					Rule:     rule.id,
					Severity: rule.severity,
					Message:  rule.message,
				})
			}
		}
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}
	return findings, nil
}

func shouldSkipScanDir(name string) bool {
	switch strings.ToLower(name) {
	case ".git", ".hg", ".svn", "node_modules", "vendor", "__pycache__", ".venv", "venv", "dist", "build", ".tmp":
		return true
	default:
		return false
	}
}

func isScannableFile(path string) bool {
	switch strings.ToLower(filepath.Ext(path)) {
	case ".go", ".java", ".php", ".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".json", ".yaml", ".yml", ".env":
		return true
	default:
		return false
	}
}

func scanReportSecrets(contents map[string][]byte) []SecretScanFinding {
	var findings []SecretScanFinding
	for name, content := range contents {
		if len(bytes.TrimSpace(content)) == 0 {
			continue
		}
		for _, rule := range reportSecretRules {
			if rule.pattern.Match(content) {
				findings = append(findings, SecretScanFinding{
					Rule:     rule.id,
					Severity: rule.severity,
					Message:  fmt.Sprintf("%s: %s", name, rule.message),
				})
			}
		}
	}
	return findings
}
