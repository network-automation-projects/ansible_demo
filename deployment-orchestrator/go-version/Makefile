.PHONY: build clean test lint run

# Build the Go binary
build:
	go build -o deployctl ./cmd/deployctl

# Build for multiple platforms
build-all:
	GOOS=linux GOARCH=amd64 go build -o deployctl-linux-amd64 ./cmd/deployctl
	GOOS=darwin GOARCH=amd64 go build -o deployctl-darwin-amd64 ./cmd/deployctl
	GOOS=darwin GOARCH=arm64 go build -o deployctl-darwin-arm64 ./cmd/deployctl
	GOOS=windows GOARCH=amd64 go build -o deployctl-windows-amd64.exe ./cmd/deployctl

# Clean build artifacts
clean:
	rm -f deployctl deployctl-*

# Run tests
test:
	go test ./...

# Lint code
lint:
	golangci-lint run

# Run the application
run:
	go run ./cmd/deployctl

# Install dependencies
deps:
	go mod download
	go mod tidy
