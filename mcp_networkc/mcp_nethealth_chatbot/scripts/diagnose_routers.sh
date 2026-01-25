#!/bin/bash
# Diagnostic script for troubleshooting router startup issues

set -e

echo "=========================================="
echo "Router Startup Diagnostic Script"
echo "=========================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Project directory: $PROJECT_DIR"
echo

# 1. Check Docker
echo "1. Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    exit 1
fi

if ! docker ps &> /dev/null; then
    echo -e "${RED}✗ Docker is not running or not accessible${NC}"
    echo "   Make sure Docker Desktop is running"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo

# 2. Check Containerlab
echo "2. Checking Containerlab..."
if ! command -v clab &> /dev/null; then
    echo -e "${RED}✗ Containerlab is not installed${NC}"
    echo "   Run: bash scripts/install_clab.sh"
    exit 1
fi

CLAB_VERSION=$(clab version 2>&1 || echo "error")
if [[ "$CLAB_VERSION" == *"error"* ]] || [[ "$CLAB_VERSION" == *"permission denied"* ]]; then
    echo -e "${YELLOW}⚠ Containerlab found but may have permission issues${NC}"
    echo "   Version check output: $CLAB_VERSION"
else
    echo -e "${GREEN}✓ Containerlab is installed${NC}"
    echo "   Version: $CLAB_VERSION"
fi
echo

# 3. Check for existing containers
echo "3. Checking for existing containers..."
RUNNING=$(docker ps --format '{{.Names}}' | grep -E 'router[12]|clab-mcp-nethealth' || true)
STOPPED=$(docker ps -a --format '{{.Names}}' | grep -E 'router[12]|clab-mcp-nethealth' || true)

if [ -z "$RUNNING" ] && [ -z "$STOPPED" ]; then
    echo -e "${YELLOW}⚠ No router containers found (neither running nor stopped)${NC}"
elif [ -n "$STOPPED" ] && [ -z "$RUNNING" ]; then
    echo -e "${YELLOW}⚠ Found stopped containers:${NC}"
    echo "$STOPPED" | while read -r container; do
        echo "   - $container"
        STATUS=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null || echo "unknown")
        echo "     Status: $STATUS"
    done
    echo
    echo "Checking logs for stopped containers..."
    echo "$STOPPED" | head -1 | while read -r container; do
        echo "   Logs for $container:"
        docker logs "$container" 2>&1 | tail -20 | sed 's/^/     /'
    done
elif [ -n "$RUNNING" ]; then
    echo -e "${GREEN}✓ Found running containers:${NC}"
    echo "$RUNNING" | while read -r container; do
        echo "   - $container"
    done
fi
echo

# 4. Check Docker Desktop file sharing
echo "4. Checking Docker Desktop file sharing..."
PROJECT_PARENT=$(dirname "$PROJECT_DIR")
echo "   Project path: $PROJECT_DIR"
echo "   Parent path: $PROJECT_PARENT"
echo -e "${GREEN}✓ If /Users is shared in Docker Desktop, that's sufficient${NC}"
echo "   (All subdirectories are accessible)"
echo

# 5. Check topology file
echo "5. Checking topology file..."
if [ ! -f "topology.yml" ]; then
    echo -e "${RED}✗ topology.yml not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ topology.yml exists${NC}"
echo

# 6. Try to inspect topology
echo "6. Inspecting Containerlab topology..."
if clab inspect -t topology.yml 2>&1; then
    echo -e "${GREEN}✓ Topology inspection successful${NC}"
else
    echo -e "${YELLOW}⚠ Topology inspection had issues (this is normal if not deployed)${NC}"
fi
echo

# 7. Check Nokia SR Linux image
echo "7. Checking Nokia SR Linux Docker image..."
if docker images | grep -q "srlinux"; then
    echo -e "${GREEN}✓ Nokia SR Linux image found${NC}"
    docker images | grep srlinux | head -1
else
    echo -e "${YELLOW}⚠ Nokia SR Linux image not found locally${NC}"
    echo "   It will be pulled automatically on first deploy"
fi
echo

# 8. Try a test deployment (dry run)
echo "8. Testing Containerlab deployment (dry run)..."
echo "   Running: clab deploy -t topology.yml --dry-run"
if clab deploy -t topology.yml --dry-run 2>&1 | head -30; then
    echo -e "${GREEN}✓ Dry run completed${NC}"
else
    echo -e "${YELLOW}⚠ Dry run had issues (check output above)${NC}"
fi
echo

# 9. Recommendations
echo "=========================================="
echo "Next Steps"
echo "=========================================="
echo

if [ -z "$RUNNING" ]; then
    echo "Since /Users is already shared, try deploying:"
    echo
    echo "  1. Clean up any existing containers:"
    echo "     clab destroy -t topology.yml"
    echo
    echo "  2. Deploy the topology (watch for errors):"
    echo "     clab deploy -t topology.yml"
    echo
    echo "  3. If you see errors, check:"
    echo "     - Docker Desktop is running"
    echo "     - Containerlab image is pulled: docker pull ghcr.io/srl-labs/clab:latest"
    echo "     - Nokia image is available: docker pull ghcr.io/nokia/srlinux:latest"
    echo
    echo "  4. Wait 30-60 seconds for routers to start, then check:"
    echo "     docker ps | grep router"
    echo
    echo "  5. If containers start then stop, check logs:"
    echo "     docker logs clab-mcp-nethealth-chatbot-router1"
    echo
    echo "  6. If deployment fails silently, try verbose output:"
    echo "     clab deploy -t topology.yml -v"
else
    echo -e "${GREEN}Routers appear to be running!${NC}"
    echo "   Verify with: docker ps | grep router"
fi
echo

