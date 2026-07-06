package main

import "strings"

var (
	buildCommit    = "unknown"
	buildTime      = "unknown"
	buildDirty     = "unknown"
	releaseChannel = "dev"
)

const (
	signingProfile               = "sdk-v2-sorted-json"
	goldenVectorVersion          = "1.0"
	releaseEvidenceSchemaVersion = "1.0"
	sourceArchiveSchemaVersion   = "1.0"
	coverageRunnerVersion        = "1.0"
	referenceDigestSchemaVersion = "1.0"
	fixtureRunnerVersion         = "1.0"
	opsCLISchemaVersion          = "1.0"
	sampleSchemaVersion          = "1.0"
	sampleImporterVersion        = "1.0"
)

func buildDirtyBool() bool {
	value := strings.ToLower(strings.TrimSpace(buildDirty))
	return value == "true" || value == "1" || value == "dirty" || value == "yes"
}
