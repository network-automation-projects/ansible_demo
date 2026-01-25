# Deployment Orchestrator - Python & Go Comparison Project

A production-ready deployment automation tool implemented in both Python and Go, demonstrating the deployment and operational differences between interpreted and compiled languages in DevOps workflows.

## Overview

The **Deployment Orchestrator** is a CLI tool that automates application deployments with features like:

- Multi-environment deployment (dev, staging, prod)
- Deployment status tracking and health checks
- Rollback capabilities
- Configuration management
- Deployment history and audit logging
- Integration with common deployment targets (Docker, Kubernetes, Terraform, Ansible, SSH)

Both implementations provide identical functionality but demonstrate different deployment characteristics:

- **Python**: venv isolation, requirements.txt, Dockerfile with Python runtime
- **Go**: go.mod dependencies, static binary, minimal Dockerfile (scratch/alpine)

## Quick Start

### Python Version

```bash
cd python-version
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

deployctl deploy --env dev --app go-monitor --version latest
```

### Go Version

```bash
cd go-version
go mod download
go build -o deployctl ./cmd/deployctl

./deployctl deploy --env dev --app go-monitor --version latest
```

## Features

### Deployment Types Supported

- **Docker Compose** - Multi-container applications
- **Docker** - Single container deployments
- **Kubernetes** - Container orchestration
- **Terraform** - Infrastructure as Code
- **Ansible** - Configuration management

### Core Capabilities

1. **Multi-Environment Support**
   - Separate configurations for dev, staging, and production
   - Environment-specific variables and settings
   - Approval workflows for production

2. **Health Checks**
   - Pre and post-deployment health verification
   - Configurable endpoints and timeouts
   - Retry logic with exponential backoff

3. **Rollback Management**
   - Automatic rollback on deployment failure
   - Manual rollback to previous versions
   - Deployment history tracking

4. **Deployment History**
   - Complete audit trail of all deployments
   - Version tracking per environment
   - Status monitoring

## Real-World Deployment Targets

This orchestrator can deploy actual demo projects:

- **go-monitor** - Go application with Docker Compose
- **dashboard-netmiko** - Python Flask web application
- **kubernetes-coffee** - Kubernetes manifests
- **terraform-aws-demo** - AWS infrastructure
- **ansible-demo** - Network device automation

See `examples/real-projects/` for deployment configurations.

## CLI Commands

Both Python and Go versions provide identical CLI interfaces:

```bash
# Deploy an application
deployctl deploy --env staging --app myapp --version v1.2.3

# Check deployment status
deployctl status --env staging --app myapp

# Rollback deployment
deployctl rollback --env staging --app myapp --version v1.2.2

# Health check
deployctl health --env staging --app myapp

# List deployments
deployctl list --env staging

# Show deployment history
deployctl history --app myapp
```

## Project Structure

```
deployment-orchestrator/
├── README.md                      # This file
├── python-version/                # Python implementation
│   ├── deployctl/                 # Main package
│   ├── config/                    # Configuration files
│   ├── scripts/                   # Helper scripts
│   ├── Dockerfile                 # Python container image
│   └── requirements.txt           # Python dependencies
├── go-version/                    # Go implementation
│   ├── cmd/deployctl/             # CLI entry point
│   ├── internal/                  # Internal packages
│   ├── config/                    # Configuration files
│   ├── Dockerfile                 # Go static binary container
│   └── go.mod                     # Go module dependencies
├── docs/                          # Documentation
│   ├── architecture.md            # System architecture
│   ├── deployment-comparison.md   # Python vs Go comparison
│   └── production-usage.md       # Production integration guide
└── examples/                      # Example configurations
    ├── docker-deployment.yaml
    ├── kubernetes-deployment.yaml
    └── real-projects/             # Real deployment configs
```

## Feature Comparison

| Feature | Python Version | Go Version |
|---------|---------------|------------|
| **Dependency Management** | requirements.txt + venv | go.mod + go.sum |
| **Build Process** | pip install | go build |
| **Runtime** | Python interpreter required | Static binary, no runtime |
| **Docker Image** | Python base image (~100MB+) | Alpine/scratch (~10MB) |
| **Startup Time** | Slower (interpreter startup) | Fast (native binary) |
| **Development** | Fast iteration | Compile step required |
| **Deployment** | Requires Python + deps | Single binary |

## Production Usage

### How Real Teams Would Use This

In production, network automation teams would integrate this tool into their existing CI/CD workflows:

1. **GitHub Actions / GitLab CI** - Call deployctl as a CI/CD step
2. **Ansible Tower/AWX** - Use as a custom module in playbooks
3. **Terraform Cloud** - Trigger deployments after infrastructure provisioning
4. **Kubernetes Operators** - Manage application deployments in clusters
5. **Standalone Tool** - For local development and testing

See [Production Usage Guide](docs/production-usage.md) for detailed integration patterns.

### CI/CD Integration Example

```yaml
# .github/workflows/deploy.yml
- name: Deploy using orchestrator
  run: |
    deployctl deploy --env ${{ github.ref_name }} \
      --app ${{ github.event.repository.name }} \
      --version ${{ github.sha }}
```

## Documentation

- [Python Version README](python-version/README.md) - Python-specific setup and usage
- [Go Version README](go-version/README.md) - Go-specific setup and usage
- [Architecture Documentation](docs/architecture.md) - System design and components
- [Deployment Comparison](docs/deployment-comparison.md) - Python vs Go differences
- [Production Usage Guide](docs/production-usage.md) - Real-world integration patterns

## Requirements

### Python Version
- Python 3.9+
- pip
- Docker (for Docker deployments)
- kubectl (for Kubernetes deployments)
- terraform (for Terraform deployments)
- ansible (for Ansible deployments)

### Go Version
- Go 1.21+
- Docker (for Docker deployments)
- kubectl (for Kubernetes deployments)
- terraform (for Terraform deployments)
- ansible (for Ansible deployments)

## Installation

### Python Version

```bash
cd python-version
./scripts/setup.sh
source .venv/bin/activate
```

### Go Version

```bash
cd go-version
go mod download
make build
```

## Usage Examples

### Deploy go-monitor

```bash
# Python version
deployctl deploy --env dev --app go-monitor --version latest

# Go version
./deployctl deploy --env dev --app go-monitor --version latest
```

### Deploy Terraform Infrastructure

```bash
deployctl deploy --env staging --app terraform-aws-demo --version v1.0.0
```

### Run Ansible Playbook

```bash
deployctl deploy --env dev --app ansible-demo \
  --playbook playbooks/backup_config.yml
```

## Portfolio Learning Objectives

This project demonstrates:

- Understanding of deployment automation patterns
- Python vs Go deployment trade-offs
- Integration with industry-standard tools (Ansible, Terraform, Docker, K8s)
- CI/CD pipeline design
- Multi-environment deployment strategies
- Production-ready code structure and practices

## Contributing

This is a portfolio/learning project. Contributions welcome for:

- Additional deployment types
- Enhanced error handling
- More comprehensive health checks
- Extended documentation
- Additional example configurations

## License

This project is provided as-is for educational and portfolio purposes.

## Author

Created by **Rebecca Clarke** as a portfolio project to demonstrate deployment automation skills and best practices.
