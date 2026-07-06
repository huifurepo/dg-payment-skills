package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"
)

type PurgeResult struct {
	OpsCLISchemaVersion string   `json:"ops_cli_schema_version"`
	DataDir             string   `json:"data_dir"`
	RunsDir             string   `json:"runs_dir"`
	RunID               string   `json:"run_id,omitempty"`
	OlderThan           string   `json:"older_than,omitempty"`
	DryRun              bool     `json:"dry_run"`
	Matched             int      `json:"matched"`
	Deleted             int      `json:"deleted"`
	DeletedRunIDs       []string `json:"deleted_run_ids"`
}

func purgeRuns(dataDir, runID, olderThan string, dryRun bool) (PurgeResult, error) {
	runsDir, err := safeRunsDir(dataDir)
	if err != nil {
		return PurgeResult{}, err
	}
	result := PurgeResult{
		OpsCLISchemaVersion: opsCLISchemaVersion,
		DataDir:             dataDir,
		RunsDir:             runsDir,
		RunID:               runID,
		OlderThan:           olderThan,
		DryRun:              dryRun,
	}
	var targets []string
	if runID != "" {
		path, err := safeRunPath(dataDir, runID)
		if err != nil {
			return result, err
		}
		targets = append(targets, path)
	}
	if olderThan != "" {
		cutoff, err := parseOlderThan(olderThan, time.Now())
		if err != nil {
			return result, err
		}
		entries, err := os.ReadDir(runsDir)
		if err != nil {
			if os.IsNotExist(err) {
				return result, nil
			}
			return result, err
		}
		for _, entry := range entries {
			if !entry.IsDir() {
				continue
			}
			path, err := safeRunPath(dataDir, entry.Name())
			if err != nil {
				return result, err
			}
			info, err := os.Lstat(path)
			if err != nil {
				return result, err
			}
			if info.Mode()&os.ModeSymlink != 0 {
				return result, fmt.Errorf("refusing to purge symlink run directory %s", entry.Name())
			}
			if info.ModTime().Before(cutoff) {
				targets = append(targets, path)
			}
		}
	}
	seen := map[string]bool{}
	for _, target := range targets {
		if seen[target] {
			continue
		}
		seen[target] = true
		runID := filepath.Base(target)
		result.Matched++
		if !dryRun {
			info, err := os.Lstat(target)
			if err != nil {
				if os.IsNotExist(err) {
					continue
				}
				return result, err
			}
			if !info.IsDir() || info.Mode()&os.ModeSymlink != 0 {
				return result, fmt.Errorf("refusing to purge unsafe run path %s", target)
			}
			if err := os.RemoveAll(target); err != nil {
				return result, err
			}
			result.Deleted++
		}
		result.DeletedRunIDs = append(result.DeletedRunIDs, runID)
	}
	return result, nil
}

func safeRunsDir(dataDir string) (string, error) {
	if dataDir == "" {
		dataDir = defaultDataDir()
	}
	runsDir, err := filepath.Abs(filepath.Join(dataDir, "runs"))
	if err != nil {
		return "", err
	}
	return runsDir, nil
}

func safeRunPath(dataDir, runID string) (string, error) {
	if strings.TrimSpace(runID) == "" {
		return "", usageError("run-id is required")
	}
	if filepath.IsAbs(runID) || filepath.Clean(runID) != runID || strings.Contains(runID, "..") || strings.ContainsAny(runID, `/\`) {
		return "", securityError("run-id must be a single sandbox run directory name")
	}
	runsDir, err := safeRunsDir(dataDir)
	if err != nil {
		return "", err
	}
	target, err := filepath.Abs(filepath.Join(runsDir, runID))
	if err != nil {
		return "", err
	}
	if !isWithinDir(runsDir, target) {
		return "", securityError("run path escapes sandbox runs directory")
	}
	return target, nil
}

func isWithinDir(parent, child string) bool {
	rel, err := filepath.Rel(parent, child)
	if err != nil {
		return false
	}
	return rel == "." || (rel != ".." && !strings.HasPrefix(rel, ".."+string(filepath.Separator)))
}

func parseOlderThan(raw string, now time.Time) (time.Time, error) {
	value := strings.TrimSpace(raw)
	if value == "" {
		return time.Time{}, usageError("--older-than is required")
	}
	if strings.HasSuffix(value, "d") {
		days, err := time.ParseDuration(strings.TrimSuffix(value, "d") + "h")
		if err != nil {
			return time.Time{}, usageError("invalid --older-than duration")
		}
		return now.Add(-24 * days), nil
	}
	if duration, err := time.ParseDuration(value); err == nil {
		return now.Add(-duration), nil
	}
	for _, layout := range []string{time.RFC3339, "2006-01-02", "20060102"} {
		if parsed, err := time.Parse(layout, value); err == nil {
			return parsed, nil
		}
	}
	return time.Time{}, usageError("invalid --older-than; use duration like 24h/7d or an absolute date")
}
