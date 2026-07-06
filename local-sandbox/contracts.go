package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

const (
	appName            = "hf-payment-local-sandbox"
	appVersion         = "1.0.0"
	contractBundle     = "huifu-pay-integration-1.3.0-r4"
	skillVersion       = "1.3.1"
	skillSource        = "hfps/" + skillVersion
	sandboxSkillSource = skillSource + ";sandbox/" + appVersion
	reportSchema       = "1.7"
	scenarioSchema     = "1.0"
)

type ReferenceCoverage struct {
	SchemaVersion      string                           `json:"schema_version"`
	ContractBundle     string                           `json:"contract_bundle"`
	SourceSkillVersion string                           `json:"source_skill_version"`
	Statuses           []string                         `json:"statuses"`
	References         map[string]ReferenceCoverageItem `json:"references"`
}

type ReferenceCoverageItem struct {
	Status           string `json:"status"`
	Reason           string `json:"reason"`
	RemainingGapType string `json:"remaining_gap_type,omitempty"`
}

type EndpointContracts struct {
	SchemaVersion      string             `json:"schema_version"`
	ContractBundle     string             `json:"contract_bundle"`
	SourceSkillVersion string             `json:"source_skill_version"`
	Endpoints          []EndpointContract `json:"endpoints"`
}

type EndpointContract struct {
	ID                     string             `json:"id"`
	Method                 string             `json:"method"`
	Path                   string             `json:"path"`
	SourceReference        string             `json:"source_reference"`
	RequiredData           []string           `json:"required_data"`
	RecommendedData        []string           `json:"recommended_data"`
	OptionalData           []string           `json:"optional_data"`
	RequiredHostingData    []string           `json:"required_hosting_data"`
	ConditionalGroups      [][]string         `json:"conditional_groups"`
	ConditionalHostingData []ConditionalField `json:"conditional_hosting_data"`
	StateEntity            string             `json:"state_entity"`
	StatusField            string             `json:"status_field"`
	StatusFields           []string           `json:"status_fields"`
	PositiveFixture        string             `json:"positive_fixture"`
	NegativeFixture        string             `json:"negative_fixture"`
	VariantFixtures        []string           `json:"variant_fixtures"`
	Assertions             []string           `json:"assertions"`
}

type ConditionalField struct {
	WhenDataPresent string   `json:"when_data_present"`
	Required        []string `json:"required"`
}

type ScenarioCatalog struct {
	SchemaVersion  string     `json:"schema_version"`
	ContractBundle string     `json:"contract_bundle"`
	Scenarios      []Scenario `json:"scenarios"`
}

type Scenario struct {
	ID         string   `json:"id"`
	Phase      string   `json:"phase"`
	Name       string   `json:"name"`
	Endpoints  []string `json:"endpoints"`
	Assertions []string `json:"assertions"`
}

type ReferenceDigests struct {
	SchemaVersion                string                `json:"schema_version"`
	ContractBundle               string                `json:"contract_bundle"`
	SourceSkillVersion           string                `json:"source_skill_version"`
	ReferenceDigestSchemaVersion string                `json:"reference_digest_schema_version"`
	Files                        []ReferenceDigestFile `json:"files"`
}

type ReferenceDigestFile struct {
	Path      string `json:"path"`
	SHA256    string `json:"sha256"`
	SizeBytes int64  `json:"size_bytes"`
}

type FixtureDefinition struct {
	SchemaVersion    string                  `json:"schema_version"`
	ContractBundle   string                  `json:"contract_bundle"`
	ID               string                  `json:"id"`
	EndpointID       string                  `json:"endpoint_id"`
	Method           string                  `json:"method"`
	Path             string                  `json:"path"`
	Kind             string                  `json:"kind"`
	HeadersProfile   string                  `json:"headers_profile"`
	Request          FixtureRequest          `json:"request"`
	Expected         FixtureExpected         `json:"expected"`
	ExpectedRespCode string                  `json:"expected_resp_code"`
	Assertions       []string                `json:"assertions"`
	FieldAssertions  []FixtureFieldAssertion `json:"field_assertions"`
	EventAssertions  []string                `json:"event_assertions"`
	SourceSampleID   string                  `json:"source_sample_id,omitempty"`
	SampleDigest     string                  `json:"sample_digest,omitempty"`
	SampleCoverage   string                  `json:"sample_coverage_level,omitempty"`
}

type FixtureRequest struct {
	Data map[string]any `json:"data"`
}

type FixtureExpected struct {
	RespCode string            `json:"resp_code"`
	Fields   map[string]string `json:"fields"`
}

type FixtureFieldAssertion struct {
	Path   string `json:"path"`
	Equals string `json:"equals,omitempty"`
	Exists bool   `json:"exists,omitempty"`
}

type ScenarioStep struct {
	Type      string         `json:"type"`
	FixtureID string         `json:"fixture_id,omitempty"`
	Name      string         `json:"name,omitempty"`
	Store     map[string]any `json:"store,omitempty"`
}

type ScenarioAssertions struct {
	SchemaVersion         string              `json:"schema_version"`
	ContractBundle        string              `json:"contract_bundle"`
	SourceSkillVersion    string              `json:"source_skill_version"`
	CoverageRunnerVersion string              `json:"coverage_runner_version"`
	FixtureRunnerVersion  string              `json:"fixture_runner_version"`
	Scenarios             []ScenarioAssertion `json:"scenarios"`
}

type ScenarioAssertion struct {
	ID                  string         `json:"id"`
	Runnable            bool           `json:"runnable"`
	EndpointIDs         []string       `json:"endpoint_ids"`
	FixtureIDs          []string       `json:"fixture_ids"`
	ExpectedEvents      []string       `json:"expected_events"`
	ExpectedReportFiles []string       `json:"expected_report_files"`
	Assertions          []string       `json:"assertions"`
	Steps               []ScenarioStep `json:"steps"`
}

type ContractBundle struct {
	References         ReferenceCoverage
	ReferenceDigests   ReferenceDigests
	Endpoints          EndpointContracts
	Scenarios          ScenarioCatalog
	ScenarioAssertions ScenarioAssertions
	Fixtures           map[string]FixtureDefinition
	Digest             string
	RawFiles           map[string][]byte
}

func loadContractBundle() (*ContractBundle, error) {
	base := "contracts/huifu-pay-integration-1.3.0-r4"
	files := map[string][]byte{}
	for _, name := range []string{"reference-coverage.json", "reference-digests.json", "endpoint-contracts.json", "scenario-catalog.json", "scenario-assertions.json"} {
		path := base + "/" + name
		b, err := embeddedContracts.ReadFile(path)
		if err != nil {
			return nil, fmt.Errorf("read embedded contract %s: %w", name, err)
		}
		files[name] = b
	}

	var refs ReferenceCoverage
	if err := json.Unmarshal(files["reference-coverage.json"], &refs); err != nil {
		return nil, err
	}
	var digests ReferenceDigests
	if err := json.Unmarshal(files["reference-digests.json"], &digests); err != nil {
		return nil, err
	}
	var endpoints EndpointContracts
	if err := json.Unmarshal(files["endpoint-contracts.json"], &endpoints); err != nil {
		return nil, err
	}
	var scenarios ScenarioCatalog
	if err := json.Unmarshal(files["scenario-catalog.json"], &scenarios); err != nil {
		return nil, err
	}
	var scenarioAssertions ScenarioAssertions
	if err := json.Unmarshal(files["scenario-assertions.json"], &scenarioAssertions); err != nil {
		return nil, err
	}
	fixtures := map[string]FixtureDefinition{}
	if err := fs.WalkDir(embeddedContracts, base+"/fixtures", func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() || !strings.HasSuffix(path, ".json") {
			return nil
		}
		b, err := embeddedContracts.ReadFile(path)
		if err != nil {
			return err
		}
		files[strings.TrimPrefix(path, base+"/")] = b
		var fixture FixtureDefinition
		if err := json.Unmarshal(b, &fixture); err != nil {
			return fmt.Errorf("decode fixture %s: %w", path, err)
		}
		fixtures[fixture.ID] = fixture
		return nil
	}); err != nil {
		return nil, err
	}

	h := sha256.New()
	names := make([]string, 0, len(files))
	for name := range files {
		names = append(names, name)
	}
	sort.Strings(names)
	for _, name := range names {
		h.Write([]byte(name))
		h.Write(files[name])
	}

	return &ContractBundle{
		References:         refs,
		ReferenceDigests:   digests,
		Endpoints:          endpoints,
		Scenarios:          scenarios,
		ScenarioAssertions: scenarioAssertions,
		Fixtures:           fixtures,
		Digest:             "sha256:" + hex.EncodeToString(h.Sum(nil)),
		RawFiles:           files,
	}, nil
}

func validateContractBundle(bundle *ContractBundle) []string {
	var problems []string
	if bundle.References.ContractBundle != contractBundle {
		problems = append(problems, "reference coverage contract_bundle mismatch")
	}
	if bundle.ReferenceDigests.ContractBundle != contractBundle {
		problems = append(problems, "reference digests contract_bundle mismatch")
	}
	if bundle.ReferenceDigests.ReferenceDigestSchemaVersion != referenceDigestSchemaVersion {
		problems = append(problems, "reference digests schema version mismatch")
	}
	if bundle.Endpoints.ContractBundle != contractBundle {
		problems = append(problems, "endpoint contracts contract_bundle mismatch")
	}
	if bundle.Scenarios.ContractBundle != contractBundle {
		problems = append(problems, "scenario catalog contract_bundle mismatch")
	}
	if bundle.ScenarioAssertions.ContractBundle != contractBundle {
		problems = append(problems, "scenario assertions contract_bundle mismatch")
	}
	if bundle.ScenarioAssertions.CoverageRunnerVersion != coverageRunnerVersion {
		problems = append(problems, "scenario assertions coverage_runner_version mismatch")
	}
	if bundle.ScenarioAssertions.FixtureRunnerVersion != fixtureRunnerVersion {
		problems = append(problems, "scenario assertions fixture_runner_version mismatch")
	}
	if len(bundle.References.References) == 0 {
		problems = append(problems, "reference coverage is empty")
	}
	allowed := map[string]bool{}
	for _, status := range bundle.References.Statuses {
		allowed[status] = true
	}
	for name, item := range bundle.References.References {
		if !allowed[item.Status] {
			problems = append(problems, fmt.Sprintf("%s has invalid coverage status %q", name, item.Status))
		}
		if item.Status == "blocked" {
			problems = append(problems, fmt.Sprintf("%s is blocked", name))
		}
		if item.Status == "partial" && item.RemainingGapType == "" {
			problems = append(problems, fmt.Sprintf("%s partial coverage missing remaining_gap_type", name))
		}
	}
	problems = append(problems, validateReferenceDigestManifest(bundle)...)
	if root, ok := findWorkspaceRoot(); ok {
		problems = append(problems, validateReferenceDigestsAgainstRoot(bundle, root)...)
	}
	if len(bundle.Endpoints.Endpoints) != 13 {
		problems = append(problems, fmt.Sprintf("expected 13 covered endpoints, got %d", len(bundle.Endpoints.Endpoints)))
	}
	if len(bundle.Scenarios.Scenarios) != 50 {
		problems = append(problems, fmt.Sprintf("expected 50 covered scenarios, got %d", len(bundle.Scenarios.Scenarios)))
	}
	seen := map[string]bool{}
	fixtureEndpointSeen := map[string]string{}
	for _, endpoint := range bundle.Endpoints.Endpoints {
		if endpoint.Method == "" || endpoint.Path == "" || endpoint.ID == "" {
			problems = append(problems, fmt.Sprintf("endpoint %+v missing id/method/path", endpoint))
		}
		if endpoint.PositiveFixture == "" || endpoint.NegativeFixture == "" {
			problems = append(problems, fmt.Sprintf("%s missing positive/negative fixture ids", endpoint.ID))
		}
		for _, fixtureID := range endpointFixtureIDs(endpoint) {
			fixture, ok := bundle.Fixtures[fixtureID]
			if !ok {
				problems = append(problems, fmt.Sprintf("%s references missing fixture %s", endpoint.ID, fixtureID))
				continue
			}
			if fixture.EndpointID != endpoint.ID {
				problems = append(problems, fmt.Sprintf("fixture %s endpoint_id=%s, want %s", fixture.ID, fixture.EndpointID, endpoint.ID))
			}
			if fixture.Path != endpoint.Path || fixture.Method != endpoint.Method {
				problems = append(problems, fmt.Sprintf("fixture %s method/path mismatch", fixture.ID))
			}
			if fixture.HeadersProfile == "" {
				problems = append(problems, fmt.Sprintf("fixture %s missing headers_profile", fixture.ID))
			}
			if len(fixture.Request.Data) == 0 {
				problems = append(problems, fmt.Sprintf("fixture %s missing request.data", fixture.ID))
			}
			if fixture.Kind != "negative" {
				for _, field := range endpoint.RequiredData {
					if _, ok := fixture.Request.Data[field]; !ok {
						problems = append(problems, fmt.Sprintf("fixture %s missing endpoint required_data %s", fixture.ID, field))
					}
				}
			}
			if fixture.Expected.RespCode == "" && fixture.ExpectedRespCode == "" {
				problems = append(problems, fmt.Sprintf("fixture %s missing expected.resp_code", fixture.ID))
			}
			if fixture.SourceSampleID != "" {
				if fixture.SampleDigest == "" || !strings.HasPrefix(fixture.SampleDigest, "sha256:") || len(strings.TrimPrefix(fixture.SampleDigest, "sha256:")) != 64 {
					problems = append(problems, fmt.Sprintf("fixture %s has invalid sample_digest", fixture.ID))
				}
				if !validSampleCoverageLevel(fixture.SampleCoverage) {
					problems = append(problems, fmt.Sprintf("fixture %s has invalid sample_coverage_level %q", fixture.ID, fixture.SampleCoverage))
				}
			} else if fixture.SampleDigest != "" || fixture.SampleCoverage != "" {
				problems = append(problems, fmt.Sprintf("fixture %s sample metadata is incomplete", fixture.ID))
			}
			fixtureEndpointSeen[fixtureID] = endpoint.ID
		}
		if len(endpoint.RequiredData) == 0 {
			problems = append(problems, fmt.Sprintf("%s missing required_data", endpoint.ID))
		}
		seen[endpoint.ID] = true
	}
	for fixtureID := range bundle.Fixtures {
		if fixtureEndpointSeen[fixtureID] == "" {
			problems = append(problems, fmt.Sprintf("fixture %s is not referenced by an endpoint", fixtureID))
		}
	}
	scenarioSeen := map[string]bool{}
	for _, scenario := range bundle.Scenarios.Scenarios {
		scenarioSeen[scenario.ID] = true
		for _, endpointID := range scenario.Endpoints {
			if !seen[endpointID] {
				problems = append(problems, fmt.Sprintf("scenario %s references unknown endpoint %s", scenario.ID, endpointID))
			}
		}
	}
	assertionSeen := map[string]bool{}
	for _, assertion := range bundle.ScenarioAssertions.Scenarios {
		assertionSeen[assertion.ID] = true
		if !scenarioSeen[assertion.ID] {
			problems = append(problems, fmt.Sprintf("scenario assertion %s references unknown scenario", assertion.ID))
		}
		for _, endpointID := range assertion.EndpointIDs {
			if !seen[endpointID] {
				problems = append(problems, fmt.Sprintf("scenario assertion %s references unknown endpoint %s", assertion.ID, endpointID))
			}
		}
		for _, fixtureID := range assertion.FixtureIDs {
			if _, ok := bundle.Fixtures[fixtureID]; !ok {
				problems = append(problems, fmt.Sprintf("scenario assertion %s references unknown fixture %s", assertion.ID, fixtureID))
			}
		}
		fixtureSteps := map[string]bool{}
		for _, step := range assertion.Steps {
			switch step.Type {
			case "gateway_fixture":
				if step.FixtureID == "" {
					problems = append(problems, fmt.Sprintf("scenario assertion %s has gateway_fixture step without fixture_id", assertion.ID))
				} else if _, ok := bundle.Fixtures[step.FixtureID]; !ok {
					problems = append(problems, fmt.Sprintf("scenario assertion %s step references unknown fixture %s", assertion.ID, step.FixtureID))
				}
				fixtureSteps[step.FixtureID] = true
			case "control_call", "notify_assert", "webhook_assert", "report_assert", "store":
			default:
				problems = append(problems, fmt.Sprintf("scenario assertion %s has unsupported step type %s", assertion.ID, step.Type))
			}
		}
		for _, fixtureID := range assertion.FixtureIDs {
			if !fixtureSteps[fixtureID] {
				problems = append(problems, fmt.Sprintf("scenario assertion %s fixture %s missing gateway_fixture step", assertion.ID, fixtureID))
			}
		}
	}
	for scenarioID := range scenarioSeen {
		if !assertionSeen[scenarioID] {
			problems = append(problems, fmt.Sprintf("scenario %s missing scenario assertion", scenarioID))
		}
	}
	return problems
}

func validSampleCoverageLevel(level string) bool {
	switch level {
	case "deidentified_production_sample", "deidentified_joint_debug_sample":
		return true
	default:
		return false
	}
}

func endpointFixtureIDs(endpoint EndpointContract) []string {
	ids := []string{endpoint.PositiveFixture, endpoint.NegativeFixture}
	ids = append(ids, endpoint.VariantFixtures...)
	out := make([]string, 0, len(ids))
	seen := map[string]bool{}
	for _, id := range ids {
		if id == "" || seen[id] {
			continue
		}
		seen[id] = true
		out = append(out, id)
	}
	return out
}

func validateReferenceDigestManifest(bundle *ContractBundle) []string {
	var problems []string
	digestPaths := map[string]bool{}
	for _, file := range bundle.ReferenceDigests.Files {
		if file.Path == "" || len(file.SHA256) != 64 {
			problems = append(problems, fmt.Sprintf("invalid reference digest entry %+v", file))
			continue
		}
		digestPaths[file.Path] = true
	}
	if !digestPaths["huifu-pay-integration/SKILL.md"] {
		problems = append(problems, "reference digests missing huifu-pay-integration/SKILL.md")
	}
	for name := range bundle.References.References {
		path := "huifu-pay-integration/references/" + name
		if !digestPaths[path] {
			problems = append(problems, "reference digests missing "+path)
		}
	}
	if len(bundle.ReferenceDigests.Files) != len(bundle.References.References)+1 {
		problems = append(problems, fmt.Sprintf("reference digest count mismatch: got %d want %d", len(bundle.ReferenceDigests.Files), len(bundle.References.References)+1))
	}
	return problems
}

type ReferenceDigestCheck struct {
	Status   string   `json:"status"`
	Checked  int      `json:"checked"`
	Problems []string `json:"problems"`
}

func referenceDigestCheck(bundle *ContractBundle) ReferenceDigestCheck {
	root, ok := findWorkspaceRoot()
	if !ok {
		return ReferenceDigestCheck{Status: "not_evaluated", Problems: []string{"workspace Skill source is not available"}}
	}
	problems := validateReferenceDigestsAgainstRoot(bundle, root)
	status := "passed"
	if len(problems) > 0 {
		status = "failed"
	}
	return ReferenceDigestCheck{Status: status, Checked: len(bundle.ReferenceDigests.Files), Problems: problems}
}

func validateReferenceDigestsAgainstRoot(bundle *ContractBundle, root string) []string {
	var problems []string
	expected := map[string]ReferenceDigestFile{}
	for _, file := range bundle.ReferenceDigests.Files {
		expected[filepath.Clean(file.Path)] = file
	}
	actual := map[string]bool{}
	for _, rel := range expectedReferenceSourceFiles(root) {
		actual[filepath.Clean(rel)] = true
	}
	for _, file := range expected {
		path := filepath.Join(root, filepath.FromSlash(file.Path))
		b, err := os.ReadFile(path)
		if err != nil {
			problems = append(problems, "reference digest source missing "+file.Path)
			continue
		}
		sum := sha256.Sum256(b)
		if hex.EncodeToString(sum[:]) != file.SHA256 {
			problems = append(problems, "reference digest changed "+file.Path)
		}
		if int64(len(b)) != file.SizeBytes {
			problems = append(problems, "reference digest size changed "+file.Path)
		}
	}
	for rel := range actual {
		if _, ok := expected[rel]; !ok {
			problems = append(problems, "reference digest source added "+filepath.ToSlash(rel))
		}
	}
	return problems
}

func expectedReferenceSourceFiles(root string) []string {
	var out []string
	skill := filepath.Join(root, "huifu-pay-integration", "SKILL.md")
	if fileExists(skill) {
		out = append(out, filepath.ToSlash(filepath.Join("huifu-pay-integration", "SKILL.md")))
	}
	refsDir := filepath.Join(root, "huifu-pay-integration", "references")
	entries, err := os.ReadDir(refsDir)
	if err != nil {
		return out
	}
	for _, entry := range entries {
		if entry.IsDir() || !strings.HasSuffix(entry.Name(), ".md") {
			continue
		}
		out = append(out, filepath.ToSlash(filepath.Join("huifu-pay-integration", "references", entry.Name())))
	}
	sort.Strings(out)
	return out
}

func findWorkspaceRoot() (string, bool) {
	cwd, err := os.Getwd()
	if err != nil {
		return "", false
	}
	for {
		if fileExists(filepath.Join(cwd, "huifu-pay-integration", "SKILL.md")) {
			return cwd, true
		}
		parent := filepath.Dir(cwd)
		if parent == cwd {
			return "", false
		}
		cwd = parent
	}
}

func embeddedContractFileNames() ([]string, error) {
	var names []string
	err := fs.WalkDir(embeddedContracts, "contracts", func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if !d.IsDir() {
			names = append(names, path)
		}
		return nil
	})
	sort.Strings(names)
	return names, err
}
