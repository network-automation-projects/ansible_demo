# Production Usage Guide

How real network automation teams would use the Deployment Orchestrator in production environments.

## Overview

In production, network automation teams don't build custom orchestrators from scratch. Instead, they use existing CI/CD platforms and integrate specialized tools. This orchestrator demonstrates deployment automation concepts that would be integrated into these existing workflows.

## Integration Patterns

### 1. CI/CD Pipeline Integration

#### GitHub Actions

**How Real Teams Would Use It:**

```yaml
name: Deploy Application

on:
  push:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install orchestrator
        run: |
          cd deployment-orchestrator/python-version
          pip install -r requirements.txt
          pip install -e .
      
      - name: Deploy to environment
        env:
          DEPLOY_ENV: ${{ github.ref == 'refs/heads/main' && 'prod' || 'staging' }}
        run: |
          deployctl deploy \
            --env $DEPLOY_ENV \
            --app ${{ github.event.repository.name }} \
            --version ${{ github.sha }}
```

**Production Context:**
- Teams use GitHub Actions for automated deployments
- Orchestrator is called as a step in the pipeline
- Environment determined by branch (main = prod, develop = staging)
- Version tied to Git commit SHA

#### GitLab CI

**How Real Teams Would Use It:**

```yaml
stages:
  - deploy

deploy:staging:
  stage: deploy
  script:
    - cd deployment-orchestrator/go-version
    - go build -o deployctl ./cmd/deployctl
    - ./deployctl deploy --env staging --app $CI_PROJECT_NAME --version $CI_COMMIT_SHA
  only:
    - develop
  when: on_success

deploy:production:
  stage: deploy
  script:
    - cd deployment-orchestrator/go-version
    - go build -o deployctl ./cmd/deployctl
    - ./deployctl deploy --env production --app $CI_PROJECT_NAME --version $CI_COMMIT_SHA
  only:
    - main
  when: manual  # Requires manual approval
```

**Production Context:**
- GitLab CI is common in enterprise environments
- Manual approval gates for production
- Environment promotion (dev → staging → prod)
- Integration with GitLab's environment management

### 2. Ansible Tower/AWX Integration

**How Real Teams Would Use It:**

```yaml
# Ansible playbook using orchestrator
- name: Deploy application using orchestrator
  hosts: localhost
  tasks:
    - name: Install orchestrator
      pip:
        name:
          - click
          - pyyaml
          - requests
          - docker
        virtualenv: /opt/orchestrator/venv
    
    - name: Deploy application
      command: >
        /opt/orchestrator/venv/bin/deployctl deploy
        --env {{ deploy_env }}
        --app {{ app_name }}
        --version {{ app_version }}
      register: deploy_result
    
    - name: Verify deployment
      assert:
        that:
          - deploy_result.rc == 0
```

**Production Context:**
- Ansible Tower provides centralized playbook execution
- Orchestrator used as a module in playbooks
- Integrates with Tower's inventory and credentials
- Job templates with approval workflows
- Audit logging through Tower

### 3. Terraform Cloud Integration

**How Real Teams Would Use It:**

```hcl
# Terraform configuration
resource "null_resource" "deploy_app" {
  triggers = {
    app_version = var.app_version
  }

  provisioner "local-exec" {
    command = <<-EOT
      cd ../deployment-orchestrator/go-version
      ./deployctl deploy \
        --env ${var.environment} \
        --app ${var.app_name} \
        --version ${var.app_version}
    EOT
  }

  depends_on = [aws_instance.app_server]
}
```

**Production Context:**
- Terraform Cloud manages infrastructure state
- Orchestrator triggered after infrastructure provisioning
- Workspace-based environment management
- State file encryption and backup
- Policy as code (Sentinel/OPA) for governance

### 4. Kubernetes Operator Pattern

**How Real Teams Would Use It:**

```yaml
# Kubernetes Job using orchestrator
apiVersion: batch/v1
kind: Job
metadata:
  name: deploy-app
spec:
  template:
    spec:
      containers:
      - name: deployctl
        image: deployctl-go:latest
        command:
          - ./deployctl
          - deploy
          - --env
          - production
          - --app
          - myapp
          - --version
          - v1.2.3
      restartPolicy: Never
```

**Production Context:**
- Kubernetes operators manage application lifecycle
- Orchestrator runs as a Job or CronJob
- Integrates with K8s service discovery
- Uses ConfigMaps and Secrets for configuration
- Monitoring via Prometheus metrics

## GitOps Patterns

### How Real Teams Would Use It

**GitOps Workflow:**

1. **Configuration in Git**
   - Deployment configs stored in Git
   - Environment-specific branches
   - Version control for all changes

2. **Automated Deployment**
   ```bash
   # On push to main branch
   deployctl deploy \
     --env production \
     --app myapp \
     --version $(git rev-parse HEAD) \
     --config configs/production.yaml
   ```

3. **Rollback via Git**
   ```bash
   # Revert to previous commit
   git revert HEAD
   deployctl rollback --env production --app myapp
   ```

**Production Context:**
- Git as single source of truth
- All changes tracked in version control
- Automated deployments on Git events
- Easy rollback via Git revert

## Enterprise Integration

### ServiceNow Integration

**How Real Teams Would Use It:**

```python
# ServiceNow script calling orchestrator
import subprocess

def deploy_application(change_request):
    """Deploy application from ServiceNow change request"""
    result = subprocess.run([
        'deployctl', 'deploy',
        '--env', change_request.environment,
        '--app', change_request.application,
        '--version', change_request.version
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        change_request.state = 'deployed'
    else:
        change_request.state = 'failed'
        change_request.notes = result.stderr
```

**Production Context:**
- ServiceNow manages change requests
- Orchestrator executes approved changes
- Integration via REST API or scripts
- Audit trail in ServiceNow

### Jira Integration

**How Real Teams Would Use It:**

```bash
# Jira webhook triggers deployment
curl -X POST http://deploy-server/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "env": "staging",
    "app": "myapp",
    "version": "v1.2.3",
    "jira_ticket": "PROJ-123"
  }'
```

**Production Context:**
- Jira tickets track deployments
- Webhooks trigger deployments
- Status updates back to Jira
- Integration with Jira automation

## Security Considerations

### Secrets Management

**How Real Teams Would Use It:**

```bash
# Using HashiCorp Vault
export VAULT_ADDR=https://vault.example.com
vault kv get -field=password secret/deploy/prod | \
  deployctl deploy --env prod --app myapp --version v1.0.0
```

**Production Context:**
- Secrets stored in Vault/AWS Secrets Manager
- Orchestrator retrieves secrets at runtime
- No secrets in configuration files
- RBAC for secret access

### RBAC and Approval Workflows

**How Real Teams Would Use It:**

```yaml
# Production deployment requires approval
deploy:production:
  script:
    - deployctl deploy --env prod --app $APP --version $VERSION
  only:
    - main
  when: manual  # Requires manual approval
  allow_failure: false
```

**Production Context:**
- Manual approval gates for production
- RBAC controls who can approve
- Audit logging of all approvals
- Integration with identity providers

## Monitoring and Observability

### Prometheus Metrics

**How Real Teams Would Use It:**

```python
# Orchestrator exposes metrics
from prometheus_client import Counter, Histogram

deployments_total = Counter('deployctl_deployments_total', 'Total deployments')
deployment_duration = Histogram('deployctl_deployment_duration_seconds', 'Deployment duration')
```

**Production Context:**
- Metrics exposed for Prometheus scraping
- Dashboards in Grafana
- Alerts on deployment failures
- SLA tracking

### Logging Integration

**How Real Teams Would Use It:**

```bash
# Structured logging to ELK stack
deployctl deploy --env prod --app myapp --version v1.0.0 \
  --json-log | \
  curl -X POST http://logstash:5044 -H "Content-Type: application/json" -d @-
```

**Production Context:**
- Logs sent to centralized logging (ELK, Splunk)
- Structured JSON logs for parsing
- Log retention policies
- Search and analysis capabilities

## Scaling Patterns

### Multi-Environment Deployments

**How Real Teams Would Use It:**

```bash
# Deploy to multiple environments
for env in dev staging prod; do
  deployctl deploy --env $env --app myapp --version v1.0.0
done
```

**Production Context:**
- Environment promotion workflows
- Parallel deployments to non-prod
- Sequential deployments to prod
- Environment-specific configurations

### Multi-Region Deployments

**How Real Teams Would Use It:**

```bash
# Deploy to multiple regions
for region in us-east-1 us-west-2 eu-west-1; do
  export AWS_REGION=$region
  deployctl deploy --env prod --app myapp --version v1.0.0
done
```

**Production Context:**
- Geographic distribution
- Region-specific configurations
- Disaster recovery deployments
- Multi-region health checks

## Best Practices

### 1. Version Management

- Use semantic versioning
- Tag releases in Git
- Track versions in deployment history
- Enable easy rollback

### 2. Configuration Management

- Environment-specific configs
- Secrets in vault systems
- Configuration validation
- Template support

### 3. Error Handling

- Automatic rollback on failure
- Retry logic for transient errors
- Clear error messages
- Comprehensive logging

### 4. Testing

- Test deployments in dev first
- Validate configurations
- Health checks after deployment
- Smoke tests

## Conclusion

In production, the Deployment Orchestrator would be:

1. **Integrated** into existing CI/CD platforms
2. **Extended** for specific team needs
3. **Used alongside** existing orchestration tools
4. **Enhanced** with enterprise features (RBAC, audit, monitoring)

This tool demonstrates understanding of deployment automation concepts and how they fit into real-world workflows, making it valuable for portfolio and learning purposes.
