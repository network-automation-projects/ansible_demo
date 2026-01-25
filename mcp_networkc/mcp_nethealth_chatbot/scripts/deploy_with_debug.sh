#!/bin/bash
# Deploy Containerlab topology with debugging output

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "=========================================="
echo "Deploying Containerlab Topology"
echo "=========================================="
echo
echo "Project directory: $PROJECT_DIR"
echo

# Check prerequisites
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    exit 1
fi

if ! docker ps &> /dev/null; then
    echo "ERROR: Docker is not running"
    echo "Please start Docker Desktop"
    exit 1
fi

if ! command -v clab &> /dev/null; then
    echo "ERROR: Containerlab is not installed"
    echo "Run: bash scripts/install_clab.sh"
    exit 1
fi

# Clean up any existing deployment
echo "Cleaning up any existing deployment..."
clab destroy -t topology.yml 2>/dev/null || echo "  (No existing deployment to clean up)"
echo

# Pull required images
echo "Pulling required Docker images..."
echo "  - Containerlab image..."
docker pull ghcr.io/srl-labs/clab:latest || echo "  ⚠ Failed to pull Containerlab image"
echo "  - Nokia SR Linux image..."
docker pull ghcr.io/nokia/srlinux:latest || echo "  ⚠ Failed to pull Nokia SR Linux image"
echo

# Deploy with verbose output
echo "Deploying topology..."
echo "=========================================="
clab deploy -t topology.yml
DEPLOY_EXIT_CODE=$?
echo "=========================================="
echo

if [ $DEPLOY_EXIT_CODE -eq 0 ]; then
    echo "✓ Deployment command completed"
    echo
    echo "Waiting 30 seconds for routers to start..."
    sleep 30
    
    echo
    echo "Checking router status..."
    RUNNING=$(docker ps --format '{{.Names}}' | grep -E 'router[12]|clab-mcp-nethealth' || true)
    
    if [ -n "$RUNNING" ]; then
        echo "✓ Routers are running:"
        echo "$RUNNING" | while read -r container; do
            echo "   - $container"
        done
    else
        echo "⚠ No routers found running"
        echo
        echo "Checking for stopped containers..."
        STOPPED=$(docker ps -a --format '{{.Names}}' | grep -E 'router[12]|clab-mcp-nethealth' || true)
        if [ -n "$STOPPED" ]; then
            echo "Found stopped containers:"
            echo "$STOPPED" | while read -r container; do
                echo "   - $container"
                echo "     Checking logs..."
                docker logs "$container" 2>&1 | tail -10 | sed 's/^/       /'
            done
        else
            echo "No containers found at all"
        fi
    fi
else
    echo "✗ Deployment failed with exit code: $DEPLOY_EXIT_CODE"
    echo
    echo "Common issues:"
    echo "  1. Docker Desktop not running"
    echo "  2. File sharing not configured (but /Users should be sufficient)"
    echo "  3. Insufficient Docker resources (memory/CPU)"
    echo "  4. Network issues pulling images"
fi

echo

