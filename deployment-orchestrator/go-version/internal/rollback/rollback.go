package rollback

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"time"
)

// DeploymentRecord represents a deployment history entry
type DeploymentRecord struct {
	App       string                 `json:"app"`
	Env       string                 `json:"env"`
	Version   string                 `json:"version"`
	Timestamp string                 `json:"timestamp"`
	Status    string                 `json:"status"`
	Config    map[string]interface{} `json:"config"`
}

// RollbackManager manages deployment rollbacks
type RollbackManager struct {
	historyDir string
}

// NewRollbackManager creates a new rollback manager
func NewRollbackManager(historyDir string) *RollbackManager {
	if historyDir == "" {
		home, _ := os.UserHomeDir()
		historyDir = filepath.Join(home, ".deployctl", "history")
	}
	os.MkdirAll(historyDir, 0755)
	return &RollbackManager{historyDir: historyDir}
}

// RecordDeployment records a deployment in history
func (r *RollbackManager) RecordDeployment(app, env, version string, config map[string]interface{}, status string) (string, error) {
	record := DeploymentRecord{
		App:       app,
		Env:       env,
		Version:   version,
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Status:    status,
		Config:    config,
	}

	filename := fmt.Sprintf("%s_%s_%s.json", app, env, record.Timestamp)
	filename = filepath.Join(r.historyDir, filename)

	data, err := json.MarshalIndent(record, "", "  ")
	if err != nil {
		return "", err
	}

	if err := os.WriteFile(filename, data, 0644); err != nil {
		return "", err
	}

	return filename, nil
}

// GetDeploymentHistory retrieves deployment history
func (r *RollbackManager) GetDeploymentHistory(app string, env string, limit int) ([]DeploymentRecord, error) {
	pattern := filepath.Join(r.historyDir, fmt.Sprintf("%s_*.json", app))
	matches, err := filepath.Glob(pattern)
	if err != nil {
		return nil, err
	}

	var records []DeploymentRecord
	for _, match := range matches {
		data, err := os.ReadFile(match)
		if err != nil {
			continue
		}

		var record DeploymentRecord
		if err := json.Unmarshal(data, &record); err != nil {
			continue
		}

		if env == "" || record.Env == env {
			records = append(records, record)
		}
	}

	// Sort by timestamp descending
	sort.Slice(records, func(i, j int) bool {
		return records[i].Timestamp > records[j].Timestamp
	})

	if limit > 0 && limit < len(records) {
		records = records[:limit]
	}

	return records, nil
}

// GetPreviousVersion gets the previous deployment version
func (r *RollbackManager) GetPreviousVersion(app, env, currentVersion string) (string, error) {
	history, err := r.GetDeploymentHistory(app, env, 10)
	if err != nil {
		return "", err
	}

	for _, record := range history {
		if record.Version != currentVersion && record.Status == "success" {
			return record.Version, nil
		}
	}

	return "", fmt.Errorf("no previous version found")
}
