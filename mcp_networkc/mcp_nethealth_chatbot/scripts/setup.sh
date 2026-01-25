#!/bin/bash
# Setup script for MCP Network Health Chatbot

set -e

echo "=========================================="
echo "MCP Network Health Chatbot - Setup"
echo "=========================================="
echo

# Check prerequisites
echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo "Install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi
echo "✓ Docker found"

# Check Containerlab
if ! command -v clab &> /dev/null; then
    echo "⚠ Containerlab is not installed"
    
    # Detect Apple Silicon
    if [[ $(uname -m) == "arm64" ]] && [[ $(uname) == "Darwin" ]]; then
        echo "Detected Apple Silicon (ARM64) - Containerlab doesn't have native binaries."
        echo "Installing Docker-based wrapper..."
        if [ -f "$(dirname "$0")/install_clab.sh" ]; then
            bash "$(dirname "$0")/install_clab.sh"
            # Add to PATH if installed to ~/.local/bin
            if [ -f "$HOME/.local/bin/clab" ]; then
                export PATH="$HOME/.local/bin:$PATH"
            fi
        else
            echo "ERROR: install_clab.sh not found. Please install Containerlab manually."
            echo "See: https://containerlab.dev/install/"
            exit 1
        fi
    else
        echo "Attempting to install Docker wrapper (works on all platforms)..."
        if [ -f "$(dirname "$0")/install_clab.sh" ]; then
            bash "$(dirname "$0")/install_clab.sh"
            if [ -f "$HOME/.local/bin/clab" ]; then
                export PATH="$HOME/.local/bin:$PATH"
            fi
        else
            echo "ERROR: install_clab.sh not found."
            echo "Try manual installation: bash -c \"\$(curl -sL https://get.containerlab.dev)\""
            echo "Or see: https://containerlab.dev/install/"
            exit 1
        fi
    fi
fi

# Verify Containerlab works
if command -v clab &> /dev/null; then
    echo "✓ Containerlab found"
    # Try to pull the image if it's a Docker wrapper
    if grep -q "docker run" "$(which clab 2>/dev/null || echo '')" 2>/dev/null; then
        echo "Pulling Containerlab Docker image (first time may take a moment)..."
        docker pull ghcr.io/srl-labs/clab:latest 2>/dev/null || true
    fi
else
    echo "ERROR: Containerlab installation failed"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi
echo "✓ Python 3 found"

# Check OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "WARNING: OPENAI_API_KEY environment variable not set"
    echo "Set it with: export OPENAI_API_KEY='your-api-key'"
    echo
fi

echo
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo
echo "Building Docker images..."

# Build MCP server image
echo "Building MCP server image..."
docker build -t network-monitor-mcp:latest .

# Build Prometheus image
echo "Building Prometheus image..."
cd prometheus
docker build -t prometheus-nethealth:latest .
cd ..

echo
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "1. Deploy Containerlab topology:"
echo "   clab deploy -t topology.yml"
echo
echo "2. Start Prometheus (optional):"
echo "   docker run -d -p 9090:9090 -v \$(pwd)/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prometheus-nethealth:latest"
echo
echo "3. Test the MCP server:"
echo "   python3 network_monitor_server.py"
echo
echo "4. Run the AI agent:"
echo "   export OPENAI_API_KEY='your-api-key'"
echo "   python3 network_agent.py --interactive"
echo
echo "5. Run demo queries:"
echo "   python3 scripts/demo_queries.py"
echo

