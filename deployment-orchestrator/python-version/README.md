# Deployment Orchestrator - Python Version

Python implementation of the deployment orchestrator demonstrating venv isolation, requirements.txt dependency management, and Python runtime deployment patterns.

## Overview

This Python version showcases:

- **Virtual Environment Isolation** - `.venv/` for dependency isolation
- **requirements.txt** - Dependency pinning and reproducibility
- **Python Runtime** - Requires Python interpreter at runtime
- **Docker Deployment** - Python base image with venv setup

## Installation

### Prerequisites

- Python 3.9 or higher
- pip
- Docker (for Docker deployments)
- kubectl (for Kubernetes deployments)
- terraform (for Terraform deployments)
- ansible (for Ansible deployments)

### Setup

1. **Create virtual environment:**

```bash
cd python-version
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Install application:**

```bash
pip install -e .
```

Or use the setup script:

```bash
./scripts/setup.sh
source .venv/bin/activate
```

## Usage

### Basic Commands

```bash
# Activate virtual environment first
source .venv/bin/activate

# Deploy an application
deployctl deploy --env dev --app go-monitor --version latest

# Check status
deployctl status --env dev --app go-monitor

# Rollback
deployctl rollback --env dev --app go-monitor

# Health check
deployctl health --env dev --app go-monitor
```

### Deploy Real Projects

```bash
# Deploy go-monitor (Docker Compose)
deployctl deploy --env dev --app go-monitor --version latest

# Deploy dashboard-netmiko (Docker)
deployctl deploy --env staging --app dashboard-netmiko --version v1.0.0

# Deploy Terraform infrastructure
deployctl deploy --env prod --app terraform-aws-demo --version v1.0.0

# Run Ansible playbook
deployctl deploy --env dev --app ansible-demo --playbook playbooks/backup_config.yml
```

## Dependency Management

### requirements.txt

Dependencies are pinned in `requirements.txt`:

```
click>=8.1.0
pyyaml>=6.0
requests>=2.31.0
docker>=6.1.0
kubernetes>=28.1.0
paramiko>=3.3.0
structlog>=23.2.0
```

### Virtual Environment

The virtual environment (`.venv/`) provides:

- **Isolation** - Separate dependencies per project
- **Reproducibility** - Exact versions via requirements.txt
- **Portability** - Can be recreated anywhere with same Python version

### Updating Dependencies

```bash
# Update a package
pip install --upgrade package-name

# Update requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt
```

## Docker Deployment

### Building Docker Image

```bash
docker build -t deployctl-python:latest .
```

Or use the build script:

```bash
./scripts/build.sh
```

### Dockerfile Characteristics

The Dockerfile demonstrates:

- **Python base image** - `python:3.9-slim`
- **Virtual environment** - Created and activated in container
- **requirements.txt** - Dependencies installed via pip
- **Runtime** - Python interpreter required at runtime

### Running in Docker

```bash
docker run --rm deployctl-python:latest --help
docker run --rm deployctl-python:latest deploy --env dev --app go-monitor --version latest
```

## CI/CD Pipeline

The Python version includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

1. **Lints** - Runs Black, Flake8, and MyPy
2. **Builds** - Creates Docker image
3. **Deploys** - Deploys to staging/production based on branch

### Local CI/CD Testing

```bash
# Run linting
black --check .
flake8 . --max-line-length=88
mypy deployctl/ --ignore-missing-imports

# Build Docker image
docker build -t deployctl-python:latest .
```

## Production Integration

### How Real Teams Would Use This

In production, the Python version would be integrated into CI/CD pipelines:

**GitHub Actions:**
```yaml
- name: Deploy using Python orchestrator
  run: |
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    deployctl deploy --env ${{ github.ref_name }} --app ${{ github.event.repository.name }}
```

**GitLab CI:**
```yaml
deploy:production:
  script:
    - python3 -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt
    - deployctl deploy --env production --app $CI_PROJECT_NAME
```

**Ansible Tower/AWX:**
- Install as a Python package in Tower's virtual environment
- Use as a custom module in playbooks
- Integrate with Tower's inventory and credentials

### Advantages in Production

- **Fast Development** - Quick iteration without compilation
- **Rich Ecosystem** - Access to Python's extensive library ecosystem
- **Easy Debugging** - Interpreted language allows runtime inspection
- **Flexibility** - Easy to modify and extend

### Considerations

- **Runtime Dependency** - Requires Python interpreter
- **Startup Time** - Slower than compiled binaries
- **Image Size** - Larger Docker images (~100MB+)
- **Dependency Management** - Need to manage virtual environments

## Project Structure

```
python-version/
├── deployctl/                 # Main package
│   ├── __init__.py
│   ├── cli.py                 # CLI entry point
│   ├── deployer.py            # Core deployment logic
│   ├── health_check.py        # Health check implementation
│   ├── rollback.py            # Rollback functionality
│   ├── config.py              # Configuration management
│   └── logger.py              # Structured logging
├── config/                    # Configuration files
│   └── environments.yaml
├── scripts/                   # Helper scripts
│   ├── setup.sh               # venv setup script
│   └── build.sh               # Build script
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── Dockerfile                 # Python container image
└── .python-version            # Python version pinning
```

## Troubleshooting

### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Dependency Conflicts

```bash
# Check installed packages
pip list

# Check for conflicts
pip check

# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
```

### Import Errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Verify installation
pip show deployctl

# Reinstall in development mode
pip install -e .
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/
```

### Code Formatting

```bash
# Format code
black deployctl/

# Check formatting
black --check deployctl/
```

### Type Checking

```bash
# Run type checker
mypy deployctl/ --ignore-missing-imports
```

## License

This project is provided as-is for educational and portfolio purposes.
