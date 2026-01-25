package deployer

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"

	"deployment-orchestrator/internal/config"
	"deployment-orchestrator/internal/health"
	"deployment-orchestrator/internal/rollback"

	"github.com/sirupsen/logrus"
)

// DeploymentError represents a deployment error
type DeploymentError struct {
	Message string
}

func (e *DeploymentError) Error() string {
	return e.Message
}

// Deployer orchestrates deployments
type Deployer struct {
	config          *config.Config
	rollbackManager *rollback.RollbackManager
	logger          *logrus.Logger
}

// NewDeployer creates a new deployer
func NewDeployer(configDir string) *Deployer {
	return &Deployer{
		config:          config.NewConfig(configDir),
		rollbackManager: rollback.NewRollbackManager(""),
		logger:          logrus.StandardLogger(),
	}
}

// Deploy deploys an application
func (d *Deployer) Deploy(app, env, version, configPath string, options map[string]string) error {
	if configPath == "" {
		var err error
		configPath, err = d.findDeploymentConfig(app)
		if err != nil {
			return err
		}
	}

	deploymentConfig, err := d.config.LoadDeploymentConfig(configPath)
	if err != nil {
		return err
	}

	envConfig, err := d.config.GetEnvironmentConfig(env, deploymentConfig)
	if err != nil {
		return err
	}

	d.logger.WithFields(logrus.Fields{
		"app":     app,
		"env":     env,
		"version": version,
		"type":    deploymentConfig["type"],
	}).Info("Starting deployment")

	// Run pre-deploy hooks
	if err := d.runPreDeployHooks(envConfig); err != nil {
		return err
	}

	// Perform deployment based on type
	deployType, ok := deploymentConfig["type"].(string)
	if !ok {
		deployType = "docker"
	}

	var success bool
	switch deployType {
	case "docker-compose":
		success = d.deployDockerCompose(app, env, version, envConfig)
	case "docker":
		success = d.deployDocker(app, env, version, envConfig)
	case "kubernetes":
		success = d.deployKubernetes(app, env, version, envConfig, options)
	case "terraform":
		success = d.deployTerraform(app, env, version, envConfig)
	case "ansible":
		success = d.deployAnsible(app, env, version, envConfig, options)
	default:
		return &DeploymentError{Message: fmt.Sprintf("Unsupported deployment type: %s", deployType)}
	}

	// Run health check
	if success {
		if !d.runHealthCheck(envConfig) {
			success = false
		}
	}

	// Record deployment
	status := "success"
	if !success {
		status = "failed"
	}
	d.rollbackManager.RecordDeployment(app, env, version, envConfig, status)

	if !success {
		return &DeploymentError{Message: fmt.Sprintf("Deployment failed for %s in %s", app, env)}
	}

	d.logger.WithFields(logrus.Fields{
		"app":     app,
		"env":     env,
		"version": version,
		"status":  "success",
	}).Info("Deployment completed")

	return nil
}

func (d *Deployer) findDeploymentConfig(app string) (string, error) {
	examplesDir := filepath.Join("..", "..", "examples", "real-projects")
	configFile := filepath.Join(examplesDir, fmt.Sprintf("%s.yaml", app))
	if _, err := os.Stat(configFile); err == nil {
		return configFile, nil
	}
	return "", fmt.Errorf("deployment config not found for app: %s", app)
}

func (d *Deployer) runPreDeployHooks(config map[string]interface{}) error {
	hooks, ok := config["pre_deploy"].([]interface{})
	if !ok {
		return nil
	}

	for _, hookInterface := range hooks {
		hook, ok := hookInterface.(map[string]interface{})
		if !ok {
			continue
		}

		hookType, ok := hook["type"].(string)
		if !ok {
			continue
		}

		switch hookType {
		case "file_check":
			path, ok := hook["path"].(string)
			if ok {
				if _, err := os.Stat(path); os.IsNotExist(err) {
					return fmt.Errorf("pre-deploy check failed: %s not found", path)
				}
			}
		case "directory_check":
			path, ok := hook["path"].(string)
			if ok {
				os.MkdirAll(path, 0755)
			}
		}
	}

	return nil
}

func (d *Deployer) runHealthCheck(config map[string]interface{}) bool {
	healthConfig, ok := config["health_check"].(map[string]interface{})
	if !ok {
		d.logger.Info("No health check configured, skipping")
		return true
	}

	checker, err := health.FromConfig(healthConfig)
	if err != nil {
		d.logger.WithError(err).Error("Failed to create health checker")
		return false
	}

	return checker.Check()
}

func (d *Deployer) deployDockerCompose(app, env, version string, config map[string]interface{}) bool {
	path, _ := config["path"].(string)
	if path == "" {
		path = "."
	}

	composeFile, _ := config["compose_file"].(string)
	if composeFile == "" {
		composeFile = "docker-compose.yml"
	}

	composePath := filepath.Join(path, composeFile)
	if _, err := os.Stat(composePath); os.IsNotExist(err) {
		d.logger.WithError(err).Error("Docker Compose file not found")
		return false
	}

	cmd := exec.Command("docker-compose", "-f", composePath, "up", "-d")
	cmd.Dir = path
	output, err := cmd.CombinedOutput()
	if err != nil {
		d.logger.WithError(err).Errorf("Docker Compose failed: %s", string(output))
		return false
	}

	return true
}

func (d *Deployer) deployDocker(app, env, version string, config map[string]interface{}) bool {
	path, _ := config["path"].(string)
	if path == "" {
		path = "."
	}

	buildConfig, _ := config["build"].(map[string]interface{})
	dockerfile, _ := buildConfig["dockerfile"].(string)
	if dockerfile == "" {
		dockerfile = "Dockerfile"
	}

	imageName := fmt.Sprintf("%s:%s", app, version)
	cmd := exec.Command("docker", "build", "-t", imageName, "-f", dockerfile, path)
	output, err := cmd.CombinedOutput()
	if err != nil {
		d.logger.WithError(err).Errorf("Docker build failed: %s", string(output))
		return false
	}

	port, _ := config["port"].(int)
	if port == 0 {
		port = 8080
	}

	containerName := fmt.Sprintf("%s-%s", app, env)
	cmd = exec.Command("docker", "run", "-d", "--name", containerName, "-p", fmt.Sprintf("%d:%d", port, port), imageName)
	output, err = cmd.CombinedOutput()
	if err != nil {
		d.logger.WithError(err).Errorf("Docker run failed: %s", string(output))
		return false
	}

	return true
}

func (d *Deployer) deployKubernetes(app, env, version string, config map[string]interface{}, options map[string]string) bool {
	path, _ := config["path"].(string)
	if path == "" {
		path = "."
	}

	namespace, _ := config["namespace"].(string)
	if namespace == "" {
		if ns, ok := options["namespace"]; ok {
			namespace = ns
		} else {
			namespace = "default"
		}
	}

	cmd := exec.Command("kubectl", "apply", "-f", path, "-n", namespace)
	output, err := cmd.CombinedOutput()
	if err != nil {
		d.logger.WithError(err).Errorf("Kubernetes apply failed: %s", string(output))
		return false
	}

	return true
}

func (d *Deployer) deployTerraform(app, env, version string, config map[string]interface{}) bool {
	path, _ := config["path"].(string)
	if path == "" {
		path = "."
	}

	varFile, _ := config["var_file"].(string)

	// Initialize
	cmd := exec.Command("terraform", "init")
	cmd.Dir = path
	output, err := cmd.CombinedOutput()
	if err != nil {
		d.logger.WithError(err).Errorf("Terraform init failed: %s", string(output))
		return false
	}

	// Plan
	cmd = exec.Command("terraform", "plan")
	if varFile != "" {
		cmd.Args = append(cmd.Args, "-var-file", varFile)
	}
	cmd.Dir = path
	output, err = cmd.CombinedOutput()
	if err != nil {
		d.logger.WithError(err).Errorf("Terraform plan failed: %s", string(output))
		return false
	}

	// Apply
	autoApprove, _ := config["auto_approve"].(bool)
	cmd = exec.Command("terraform", "apply")
	if autoApprove {
		cmd.Args = append(cmd.Args, "-auto-approve")
	}
	if varFile != "" {
		cmd.Args = append(cmd.Args, "-var-file", varFile)
	}
	cmd.Dir = path
	output, err = cmd.CombinedOutput()
	if err != nil {
		d.logger.WithError(err).Errorf("Terraform apply failed: %s", string(output))
		return false
	}

	return true
}

func (d *Deployer) deployAnsible(app, env, version string, config map[string]interface{}, options map[string]string) bool {
	path, _ := config["path"].(string)
	if path == "" {
		path = "."
	}

	inventory, _ := config["inventory"].(string)
	if inventory == "" {
		inventory = "inventories/hosts.yml"
	}

	playbook, _ := config["playbook"].(string)
	if playbook == "" {
		if pb, ok := options["playbook"]; ok {
			playbook = pb
		} else {
			playbook = "playbooks/main.yml"
		}
	}

	cmd := exec.Command("ansible-playbook", "-i", inventory, playbook)
	if vaultFile, ok := config["vault_password_file"].(string); ok && vaultFile != "" {
		cmd.Args = append(cmd.Args, "--vault-password-file", vaultFile)
	}
	cmd.Dir = path
	output, err := cmd.CombinedOutput()
	if err != nil {
		d.logger.WithError(err).Errorf("Ansible playbook failed: %s", string(output))
		return false
	}

	return true
}

// GetStatus gets deployment status
func (d *Deployer) GetStatus(app, env string) (map[string]interface{}, error) {
	history, err := d.rollbackManager.GetDeploymentHistory(app, env, 1)
	if err != nil {
		return nil, err
	}

	if len(history) > 0 {
		record := history[0]
		return map[string]interface{}{
			"app":       record.App,
			"env":       record.Env,
			"version":   record.Version,
			"timestamp": record.Timestamp,
			"status":    record.Status,
		}, nil
	}

	return map[string]interface{}{
		"status": "unknown",
		"app":    app,
		"env":    env,
	}, nil
}

// Rollback rolls back to a previous version
func (d *Deployer) Rollback(app, env, version string) error {
	if version == "" {
		status, err := d.GetStatus(app, env)
		if err != nil {
			return err
		}

		currentVersion, _ := status["version"].(string)
		prevVersion, err := d.rollbackManager.GetPreviousVersion(app, env, currentVersion)
		if err != nil {
			return err
		}
		version = prevVersion
	}

	d.logger.WithFields(logrus.Fields{
		"app":     app,
		"env":     env,
		"version": version,
	}).Info("Rolling back")

	return d.Deploy(app, env, version, "", nil)
}
