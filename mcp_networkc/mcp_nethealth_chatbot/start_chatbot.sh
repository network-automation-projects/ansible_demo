#!/bin/bash
# Startup script for Network Health Chatbot

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Network Health Chatbot - Startup"
echo "=========================================="
echo

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY is not set"
    echo ""
    echo "Please set it with:"
    echo "  export OPENAI_API_KEY='your-api-key'"
    echo ""
    echo "Get your API key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if dependencies are installed
echo "Checking Python dependencies..."
if ! python3 -c "import mcp; import netmiko; import openai; import requests" 2>/dev/null; then
    echo "❌ Dependencies are missing!"
    echo ""
    echo "Installing dependencies..."
    pip3 install -r requirements.txt || {
        echo "⚠️  Installation failed. Try:"
        echo "   pip3 install --user -r requirements.txt"
        echo "   OR"
        echo "   python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    }
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies are installed"
fi

# Check if network topology is deployed
echo ""
echo "Checking network topology..."
if docker ps | grep -q "clab-mcp-nethealth-chatbot-router1"; then
    echo "✓ Network topology is already deployed and running"
elif docker ps -a | grep -q "clab-mcp-nethealth-chatbot-router1"; then
    echo "⚠️  Containers exist but may not be running"
    echo ""
    echo "Redeploying network topology with --reconfigure flag..."
    clab deploy -t topology.yml --reconfigure || {
        echo "❌ Failed to redeploy topology"
        echo "Try manually: clab destroy -t topology.yml && clab deploy -t topology.yml"
        exit 1
    }
    echo "✓ Network topology redeployed"
    echo "Waiting for routers to be ready..."
    sleep 10
else
    echo "⚠️  Network topology is not deployed"
    echo ""
    echo "Deploying network topology (this may take a minute)..."
    clab deploy -t topology.yml || {
        echo "❌ Failed to deploy topology"
        echo "Make sure Docker Desktop is running and Containerlab is installed"
        exit 1
    }
    echo "✓ Network topology deployed"
    echo "Waiting for routers to be ready..."
    sleep 10
fi

# Check if Prometheus is running (optional)
echo ""
echo "Checking Prometheus (optional)..."
if ! docker ps | grep -q "prometheus-nethealth"; then
    echo "ℹ️  Prometheus is not running (optional)"
    echo "   Start it with: cd prometheus && docker run -d --name prometheus-nethealth -p 9090:9090 -v \$(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus:latest"
else
    echo "✓ Prometheus is running"
fi

# Start the chatbot
echo ""
echo "=========================================="
echo "Starting Network Health Chatbot"
echo "=========================================="
echo ""
echo "Type 'exit', 'quit', or 'q' to quit"
echo ""

python3 network_agent.py --interactive

