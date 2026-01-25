# Architecture Documentation

System architecture and design of the Deployment Orchestrator.

## System Overview

The Deployment Orchestrator is a CLI tool that automates application deployments across multiple deployment types and environments. It provides a unified interface for deploying applications using Docker, Kubernetes, Terraform, and Ansible.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface                        │
│  (Python: Click / Go: Cobra)                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Core Deployer                          │
│  - Deployment orchestration                             │
│  - Configuration management                             │
│  - Error handling                                       │
└──────┬──────────────┬──────────────┬────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Config     │ │  Health     │ │  Rollback   │
│  Manager    │ │  Checker    │ │  Manager    │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│              Deployment Executors                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ Docker   │ │Kubernetes │ │Terraform │ │ Ansible  │ │
│  │ Compose  │ │           │ │          │ │          │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Component Design

### CLI Layer

**Python Implementation:**
- Uses Click framework for CLI
- Command structure: `deployctl <command> [options]`
- Commands: deploy, status, rollback, health, list, history

**Go Implementation:**
- Uses Cobra framework for CLI
- Identical command structure
- Same commands as Python version

### Core Deployer

**Responsibilities:**
- Orchestrates deployment workflow
- Loads and validates configuration
- Executes deployment based on type
- Manages deployment lifecycle
- Handles errors and rollbacks

**Key Methods:**
- `deploy()` - Main deployment method
- `get_status()` - Get deployment status
- `rollback()` - Rollback to previous version

### Configuration Manager

**Responsibilities:**
- Load environment configurations
- Load deployment configurations
- Merge environment-specific settings
- Validate configuration

**Configuration Files:**
- `environments.yaml` - Environment definitions
- `deployments.yaml` - Deployment configurations

### Health Checker

**Responsibilities:**
- Perform pre-deployment health checks
- Perform post-deployment verification
- Retry logic with exponential backoff
- Configurable endpoints and timeouts

**Health Check Flow:**
1. Configure health check from deployment config
2. Perform HTTP GET request to endpoint
3. Verify response status code
4. Retry on failure with backoff
5. Report success/failure

### Rollback Manager

**Responsibilities:**
- Record deployment history
- Track deployment versions
- Enable rollback to previous versions
- Maintain audit trail

**History Storage:**
- JSON files in `~/.deployctl/history/`
- Format: `{app}_{env}_{timestamp}.json`
- Contains: app, env, version, timestamp, status, config

## Deployment Types

### Docker Compose

**Flow:**
1. Load docker-compose.yml file
2. Set environment variables
3. Run `docker-compose up -d`
4. Verify containers are running

**Configuration:**
```yaml
type: docker-compose
path: ../go-monitor
compose_file: docker-compose.yml
env_vars:
  HOST: google.com
```

### Docker

**Flow:**
1. Build Docker image
2. Run container with configuration
3. Expose ports
4. Verify container is running

**Configuration:**
```yaml
type: docker
path: ../dashboard-netmiko
build:
  dockerfile: Dockerfile
port: 5001
```

### Kubernetes

**Flow:**
1. Load Kubernetes manifests
2. Apply manifests to cluster
3. Verify deployment status
4. Check pod health

**Configuration:**
```yaml
type: kubernetes
path: ../docker-kubernetes-demo/manifests
namespace: coffee-dev
```

### Terraform

**Flow:**
1. Initialize Terraform
2. Validate configuration
3. Plan changes
4. Apply changes (with approval)
5. Verify infrastructure

**Configuration:**
```yaml
type: terraform
path: ../terraform-aws-demo
var_file: terraform.tfvars.prod
auto_approve: false
```

### Ansible

**Flow:**
1. Load inventory
2. Execute playbook
3. Handle vault passwords
4. Verify playbook execution

**Configuration:**
```yaml
type: ansible
path: ../ansible_demo
inventory: inventories/hosts.yml
playbook: playbooks/backup_config.yml
vault_password_file: vault/.prod_password
```

## Data Flow

### Deployment Flow

```
1. CLI receives deploy command
   │
   ▼
2. Load deployment configuration
   │
   ▼
3. Load environment-specific config
   │
   ▼
4. Run pre-deploy hooks
   │
   ▼
5. Execute deployment (based on type)
   │
   ├─ Docker Compose → docker-compose up
   ├─ Docker → docker build + run
   ├─ Kubernetes → kubectl apply
   ├─ Terraform → terraform apply
   └─ Ansible → ansible-playbook
   │
   ▼
6. Run health check
   │
   ▼
7. Record deployment in history
   │
   ▼
8. Return success/failure
```

### Rollback Flow

```
1. CLI receives rollback command
   │
   ▼
2. Get current deployment status
   │
   ▼
3. Find previous successful version
   │
   ▼
4. Load previous deployment config
   │
   ▼
5. Execute deployment with previous config
   │
   ▼
6. Verify rollback success
   │
   ▼
7. Record rollback in history
```

## Error Handling

### Error Types

1. **Configuration Errors**
   - Missing configuration files
   - Invalid configuration format
   - Missing required fields

2. **Deployment Errors**
   - Command execution failures
   - Timeout errors
   - Resource conflicts

3. **Health Check Errors**
   - Endpoint unreachable
   - Unexpected status codes
   - Timeout failures

### Error Recovery

- **Automatic Rollback**: On deployment failure
- **Retry Logic**: For health checks
- **Error Logging**: Structured logging for debugging
- **Error Reporting**: Clear error messages to user

## Security Considerations

### Configuration Security

- **Secrets Management**: Integration with vault systems
- **Environment Variables**: Secure handling of sensitive data
- **File Permissions**: Proper permissions on config files

### Deployment Security

- **SSH Keys**: Secure key management for SSH deployments
- **Kubernetes**: RBAC and service account management
- **Terraform**: State file encryption
- **Ansible**: Vault password protection

## Production Architecture

### How Real Teams Would Integrate

```
┌─────────────────────────────────────────────────┐
│         CI/CD Platform                          │
│  (GitHub Actions / GitLab CI / Jenkins)        │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│      Deployment Orchestrator                    │
│  (deployctl - Python or Go)                     │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │ Docker │ │   K8s  │ │Terraform│
   └────────┘ └────────┘ └────────┘
        │          │          │
        ▼          ▼          ▼
   ┌──────────────────────────────┐
   │    Target Infrastructure     │
   └──────────────────────────────┘
```

### Integration Points

1. **CI/CD Pipelines**
   - Called as a step in pipeline
   - Receives environment and version from pipeline
   - Reports deployment status back to pipeline

2. **Ansible Tower/AWX**
   - Used as a custom module
   - Integrates with Tower inventory
   - Uses Tower credentials

3. **Terraform Cloud**
   - Triggers after infrastructure provisioning
   - Manages application deployments
   - Handles state management

4. **Kubernetes Operators**
   - Manages application lifecycle
   - Integrates with K8s API
   - Handles rolling updates

## Scalability

### Horizontal Scaling

- Multiple orchestrator instances
- Stateless design (except history)
- Can run in parallel for different apps

### Vertical Scaling

- Handles multiple concurrent deployments
- Efficient resource usage
- Minimal memory footprint (especially Go version)

## Monitoring and Observability

### Logging

- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Deployment audit trail

### Metrics

- Deployment success/failure rates
- Deployment duration
- Health check status
- Rollback frequency

## Future Enhancements

1. **Multi-Service Orchestration**
   - Deploy multiple services together
   - Dependency management
   - Coordinated rollbacks

2. **Advanced Health Checks**
   - Custom health check scripts
   - Multi-endpoint health checks
   - Health check aggregation

3. **Deployment Strategies**
   - Blue-green deployments
   - Canary deployments
   - Rolling updates

4. **Integration Enhancements**
   - ServiceNow integration
   - Jira integration
   - Slack notifications
