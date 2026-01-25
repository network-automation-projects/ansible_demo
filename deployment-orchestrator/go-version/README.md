# Deployment Orchestrator - Go Version

Go implementation of the deployment orchestrator demonstrating static binary compilation, go.mod dependency management, and minimal runtime deployment patterns.

## Overview

This Go version showcases:

- **Static Binary** - Single executable, no runtime dependencies
- **go.mod** - Dependency management with checksums (go.sum)
- **Multi-Platform Builds** - Compile for Linux, macOS, Windows
- **Minimal Docker Image** - Alpine/scratch base (~10MB)

## Installation

### Prerequisites

- Go 1.21 or higher
- Docker (for Docker deployments)
- kubectl (for Kubernetes deployments)
- terraform (for Terraform deployments)
- ansible (for Ansible deployments)

### Setup

1. **Install dependencies:**

```bash
cd go-version
go mod download
go mod tidy
```

2. **Build binary:**

```bash
go build -o deployctl ./cmd/deployctl
```

Or use Make:

```bash
make build
```

## Usage

### Basic Commands

```bash
# Build first
make build

# Deploy an application
./deployctl deploy --env dev --app go-monitor --version latest

# Check status
./deployctl status --env dev --app go-monitor

# Rollback
./deployctl rollback --env dev --app go-monitor

# Health check
./deployctl health --env dev --app go-monitor
```

### Deploy Real Projects

```bash
# Deploy go-monitor (Docker Compose)
./deployctl deploy --env dev --app go-monitor --version latest

# Deploy dashboard-netmiko (Docker)
./deployctl deploy --env staging --app dashboard-netmiko --version v1.0.0

# Deploy Terraform infrastructure
./deployctl deploy --env prod --app terraform-aws-demo --version v1.0.0

# Run Ansible playbook
./deployctl deploy --env dev --app ansible-demo --playbook playbooks/backup_config.yml
```

## Dependency Management

### go.mod

Dependencies are managed in `go.mod`:

```go
module deployment-orchestrator

go 1.21

require (
    github.com/spf13/cobra v1.8.0
    gopkg.in/yaml.v3 v3.0.1
    // ... other dependencies
)
```

### go.sum

The `go.sum` file contains checksums for all dependencies, ensuring:

- **Reproducibility** - Exact dependency versions
- **Security** - Checksum verification
- **Consistency** - Same dependencies across environments

### Managing Dependencies

```bash
# Add a dependency
go get github.com/package/name

# Update dependencies
go get -u ./...

# Remove unused dependencies
go mod tidy

# Verify dependencies
go mod verify
```

## Building

### Single Platform

```bash
# Build for current platform
go build -o deployctl ./cmd/deployctl

# Build with optimizations
go build -ldflags="-s -w" -o deployctl ./cmd/deployctl
```

### Multi-Platform Builds

```bash
# Build for multiple platforms
make build-all
```

This creates:
- `deployctl-linux-amd64`
- `deployctl-darwin-amd64`
- `deployctl-darwin-arm64`
- `deployctl-windows-amd64.exe`

### Cross-Compilation

```bash
# Build for Linux from macOS
GOOS=linux GOARCH=amd64 go build -o deployctl-linux ./cmd/deployctl

# Build for Windows from Linux
GOOS=windows GOARCH=amd64 go build -o deployctl.exe ./cmd/deployctl
```

## Docker Deployment

### Building Docker Image

```bash
docker build -t deployctl-go:latest .
```

### Dockerfile Characteristics

The Dockerfile demonstrates:

- **Multi-stage build** - Build stage + minimal runtime
- **Static binary** - CGO_ENABLED=0 for static linking
- **Alpine base** - Minimal runtime image (~10MB)
- **No runtime dependencies** - Single binary, no Go runtime needed

### Running in Docker

```bash
docker run --rm deployctl-go:latest --help
docker run --rm deployctl-go:latest deploy --env dev --app go-monitor --version latest
```

## CI/CD Pipeline

The Go version includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

1. **Lints** - Runs golangci-lint
2. **Tests** - Runs go test
3. **Builds** - Multi-platform builds (Linux, macOS, Windows)
4. **Docker** - Creates minimal Docker image
5. **Deploys** - Deploys to staging/production based on branch

### Local CI/CD Testing

```bash
# Run linting
golangci-lint run

# Run tests
go test ./...

# Build for all platforms
make build-all

# Build Docker image
docker build -t deployctl-go:latest .
```

## Production Integration

### How Real Teams Would Use This

In production, the Go version would be integrated into CI/CD pipelines:

**GitHub Actions:**
```yaml
- name: Build Go orchestrator
  run: |
    cd go-version
    go build -o deployctl ./cmd/deployctl
    
- name: Deploy using Go orchestrator
  run: |
    ./deployctl deploy --env ${{ github.ref_name }} --app ${{ github.event.repository.name }}
```

**GitLab CI:**
```yaml
deploy:production:
  script:
    - cd go-version
    - go build -o deployctl ./cmd/deployctl
    - ./deployctl deploy --env production --app $CI_PROJECT_NAME
```

**Kubernetes:**
- Deploy as a single binary in a minimal container
- No runtime dependencies required
- Fast startup time

### Advantages in Production

- **Single Binary** - No runtime dependencies, easy distribution
- **Fast Startup** - Native binary, no interpreter overhead
- **Small Images** - Minimal Docker images (~10MB)
- **Cross-Platform** - Build once, deploy anywhere
- **Performance** - Compiled code, faster execution

### Considerations

- **Compilation Time** - Requires build step
- **Development Speed** - Slower iteration than interpreted languages
- **Binary Size** - Larger than Python scripts (but no runtime needed)
- **Platform-Specific** - Need to build for each target platform

## Project Structure

```
go-version/
├── cmd/
│   └── deployctl/
│       └── main.go            # CLI entry point
├── internal/                  # Internal packages
│   ├── deployer/              # Core deployment logic
│   ├── health/                # Health check implementation
│   ├── rollback/              # Rollback functionality
│   ├── config/                # Configuration management
│   └── logger/                # Structured logging
├── config/                    # Configuration files
│   └── environments.yaml
├── go.mod                     # Go module dependencies
├── go.sum                     # Dependency checksums
├── Makefile                   # Build automation
└── Dockerfile                 # Go static binary container
```

## Troubleshooting

### Build Issues

```bash
# Clean build cache
go clean -cache

# Verify Go installation
go version

# Check module status
go mod verify
```

### Dependency Issues

```bash
# Download missing dependencies
go mod download

# Update all dependencies
go get -u ./...

# Tidy module
go mod tidy
```

### Cross-Compilation Issues

```bash
# Check supported platforms
go tool dist list

# Build with verbose output
go build -v -o deployctl ./cmd/deployctl
```

## Development

### Running Tests

```bash
# Run all tests
go test ./...

# Run with coverage
go test -cover ./...

# Run specific package
go test ./internal/deployer
```

### Code Formatting

```bash
# Format code
go fmt ./...

# Run goimports
goimports -w .
```

### Linting

```bash
# Install golangci-lint
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Run linter
golangci-lint run
```

## License

This project is provided as-is for educational and portfolio purposes.
