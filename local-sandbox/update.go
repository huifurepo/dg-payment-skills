package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"runtime"
	"strconv"
	"strings"
	"time"
)

const (
	updateIndexFileName   = "hf-payment-local-sandbox-latest.json"
	defaultUpdateIndexURL = "https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/huifuskills/" + updateIndexFileName
	maxUpdateIndexBytes   = 1 << 20
)

type updateIndex struct {
	SchemaVersion      string                    `json:"schema_version"`
	Name               string                    `json:"name"`
	Channel            string                    `json:"channel"`
	LatestVersion      string                    `json:"latest_version"`
	Version            string                    `json:"version"`
	PublishedAt        string                    `json:"published_at"`
	ContractBundle     string                    `json:"contract_bundle"`
	SourceSkillVersion string                    `json:"source_skill_version"`
	ReleaseNotesURL    string                    `json:"release_notes_url"`
	DownloadPageURL    string                    `json:"download_page_url"`
	Downloads          map[string]updateDownload `json:"downloads"`
}

type updateDownload struct {
	Name      string `json:"name"`
	URL       string `json:"url"`
	SHA256    string `json:"sha256"`
	SizeBytes int64  `json:"size_bytes"`
}

func (a *App) checkUpdate(parent context.Context) (map[string]any, error) {
	indexURL := strings.TrimSpace(a.updateIndexURL)
	if indexURL == "" {
		return nil, errors.New("update index URL is empty")
	}
	if err := validateUpdateIndexURL(indexURL); err != nil {
		return nil, err
	}
	ctx, cancel := context.WithTimeout(parent, 6*time.Second)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, indexURL, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Accept", "application/json")
	req.Header.Set("User-Agent", appName+"/"+appVersion+" "+runtimeOSArch()+" "+releaseChannel)
	client := &http.Client{
		Timeout: 7 * time.Second,
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return validateUpdateIndexURL(req.URL.String())
		},
	}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return nil, fmt.Errorf("update index HTTP %d", resp.StatusCode)
	}
	raw, err := io.ReadAll(io.LimitReader(resp.Body, maxUpdateIndexBytes+1))
	if err != nil {
		return nil, err
	}
	if len(raw) > maxUpdateIndexBytes {
		return nil, errors.New("update index is too large")
	}
	var index updateIndex
	if err := json.Unmarshal(raw, &index); err != nil {
		return nil, err
	}
	return updateResultFromIndex(index, indexURL)
}

func updateResultFromIndex(index updateIndex, sourceURL string) (map[string]any, error) {
	if index.Name != "" && index.Name != appName {
		return nil, fmt.Errorf("update index name %q does not match %q", index.Name, appName)
	}
	latest := firstNonEmpty(index.LatestVersion, index.Version)
	if strings.TrimSpace(latest) == "" {
		return nil, errors.New("update index latest_version is missing")
	}
	compare, err := compareVersions(appVersion, latest)
	if err != nil {
		return nil, err
	}
	platform := updatePlatformKey()
	download, hasDownload := index.Downloads[platform]
	if hasDownload {
		if err := validateUpdateDownload(download); err != nil {
			return nil, err
		}
	}
	result := map[string]any{
		"ok":                   true,
		"name":                 appName,
		"current_version":      appVersion,
		"latest_version":       latest,
		"update_available":     compare < 0,
		"platform":             platform,
		"platform_supported":   hasDownload,
		"channel":              firstNonEmpty(index.Channel, releaseChannel),
		"published_at":         index.PublishedAt,
		"contract_bundle":      index.ContractBundle,
		"source_skill_version": index.SourceSkillVersion,
		"release_notes_url":    index.ReleaseNotesURL,
		"download_page_url":    index.DownloadPageURL,
		"source_url":           sourceURL,
		"checked_at":           time.Now().UTC().Format(time.RFC3339Nano),
	}
	if hasDownload {
		result["download"] = map[string]any{
			"name":       firstNonEmpty(download.Name, fileNameFromURL(download.URL)),
			"url":        download.URL,
			"sha256":     download.SHA256,
			"size_bytes": download.SizeBytes,
		}
	}
	return result, nil
}

func updatePlatformKey() string {
	return runtime.GOOS + "_" + runtime.GOARCH
}

func validateUpdateIndexURL(raw string) error {
	u, err := url.Parse(raw)
	if err != nil {
		return err
	}
	if u.Scheme != "https" {
		if u.Scheme == "http" && isLoopbackHost(u.Hostname()) {
			return nil
		}
		return errors.New("update index URL must use https")
	}
	if strings.TrimSpace(u.Hostname()) == "" {
		return errors.New("update index URL host is missing")
	}
	return nil
}

func validateUpdateDownload(download updateDownload) error {
	if strings.TrimSpace(download.URL) == "" {
		return errors.New("update download URL is missing")
	}
	u, err := url.Parse(download.URL)
	if err != nil {
		return err
	}
	if u.Scheme != "https" {
		if u.Scheme != "http" || !isLoopbackHost(u.Hostname()) {
			return errors.New("update download URL must use https")
		}
	}
	if strings.TrimSpace(u.Hostname()) == "" {
		return errors.New("update download URL host is missing")
	}
	if strings.TrimSpace(download.SHA256) != "" && !isHexSHA256(download.SHA256) {
		return errors.New("update download sha256 is invalid")
	}
	return nil
}

func isHexSHA256(value string) bool {
	if len(value) != 64 {
		return false
	}
	for _, r := range value {
		if (r < '0' || r > '9') && (r < 'a' || r > 'f') && (r < 'A' || r > 'F') {
			return false
		}
	}
	return true
}

func compareVersions(current, latest string) (int, error) {
	a, err := versionParts(current)
	if err != nil {
		return 0, err
	}
	b, err := versionParts(latest)
	if err != nil {
		return 0, err
	}
	max := len(a)
	if len(b) > max {
		max = len(b)
	}
	for i := 0; i < max; i++ {
		av, bv := 0, 0
		if i < len(a) {
			av = a[i]
		}
		if i < len(b) {
			bv = b[i]
		}
		if av < bv {
			return -1, nil
		}
		if av > bv {
			return 1, nil
		}
	}
	return 0, nil
}

func versionParts(value string) ([]int, error) {
	value = strings.TrimSpace(strings.TrimPrefix(value, "v"))
	if i := strings.IndexAny(value, "-+"); i >= 0 {
		value = value[:i]
	}
	if value == "" {
		return nil, errors.New("version is empty")
	}
	rawParts := strings.Split(value, ".")
	parts := make([]int, 0, len(rawParts))
	for _, raw := range rawParts {
		if raw == "" {
			return nil, fmt.Errorf("invalid version %q", value)
		}
		part, err := strconv.Atoi(raw)
		if err != nil {
			return nil, fmt.Errorf("invalid version %q", value)
		}
		parts = append(parts, part)
	}
	return parts, nil
}

func fileNameFromURL(raw string) string {
	u, err := url.Parse(raw)
	if err != nil {
		return ""
	}
	path := strings.TrimRight(u.Path, "/")
	if path == "" {
		return ""
	}
	parts := strings.Split(path, "/")
	return parts[len(parts)-1]
}
