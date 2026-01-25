package config

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

// ConfigError represents a configuration error
type ConfigError struct {
	Message string
}

func (e *ConfigError) Error() string {
	return e.Message
}

// Config manages deployment configurations
type Config struct {
	configDir    string
	environments map[string]interface{}
}

// NewConfig creates a new configuration manager
func NewConfig(configDir string) *Config {
	if configDir == "" {
		configDir = filepath.Join(".", "config")
	}
	return &Config{
		configDir:    configDir,
		environments: make(map[string]interface{}),
	}
}

// LoadEnvironments loads environment configurations
func (c *Config) LoadEnvironments() (map[string]interface{}, error) {
	if c.environments != nil {
		return c.environments, nil
	}

	envFile := filepath.Join(c.configDir, "environments.yaml")
	if _, err := os.Stat(envFile); os.IsNotExist(err) {
		// Return defaults
		return map[string]interface{}{
			"dev":     map[string]interface{}{"description": "Development environment"},
			"staging": map[string]interface{}{"description": "Staging environment"},
			"prod":     map[string]interface{}{"description": "Production environment"},
		}, nil
	}

	data, err := os.ReadFile(envFile)
	if err != nil {
		return nil, &ConfigError{Message: fmt.Sprintf("Failed to read environments file: %v", err)}
	}

	var config map[string]interface{}
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, &ConfigError{Message: fmt.Sprintf("Failed to parse environments file: %v", err)}
	}

	envs, ok := config["environments"].(map[string]interface{})
	if !ok {
		return make(map[string]interface{}), nil
	}

	c.environments = envs
	return c.environments, nil
}

// LoadDeploymentConfig loads deployment configuration from file
func (c *Config) LoadDeploymentConfig(configPath string) (map[string]interface{}, error) {
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		return nil, &ConfigError{Message: fmt.Sprintf("Configuration file not found: %s", configPath)}
	}

	data, err := os.ReadFile(configPath)
	if err != nil {
		return nil, &ConfigError{Message: fmt.Sprintf("Failed to read config file: %v", err)}
	}

	var config map[string]interface{}
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, &ConfigError{Message: fmt.Sprintf("Failed to parse config file: %v", err)}
	}

	return config, nil
}

// GetEnvironmentConfig gets environment-specific configuration
func (c *Config) GetEnvironmentConfig(envName string, deploymentConfig map[string]interface{}) (map[string]interface{}, error) {
	environments, ok := deploymentConfig["environments"].(map[string]interface{})
	if !ok {
		return nil, &ConfigError{Message: fmt.Sprintf("No environments found in deployment config")}
	}

	envConfig, ok := environments[envName].(map[string]interface{})
	if !ok {
		return nil, &ConfigError{Message: fmt.Sprintf("Environment '%s' not found in deployment config", envName)}
	}

	// Merge base config with environment-specific config
	result := make(map[string]interface{})
	for k, v := range deploymentConfig {
		if k != "environments" {
			result[k] = v
		}
	}
	for k, v := range envConfig {
		result[k] = v
	}

	return result, nil
}
