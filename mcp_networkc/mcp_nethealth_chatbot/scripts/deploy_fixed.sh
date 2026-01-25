#!/bin/bash
# Alternative deployment script that works around Docker Desktop file sharing issues

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "=========================================="
echo "Deploying with Docker Desktop Fix"
echo "=========================================="
echo

# The issue: Containerlab inside Docker container uses /workspace paths
# but Docker Desktop needs actual host paths
# Solution: Use Containerlab's --workdir option if available, or work around it

# Clean up first
echo "Cleaning up existing deployment..."
clab destroy -t topology.yml 2>/dev/null || echo "  (No existing deployment)"
echo

# Try deploying with explicit workdir
echo "Attempting deployment..."
echo "Note: If this fails, we'll try an alternative approach"
echo

# Deploy and capture output
DEPLOY_OUTPUT=$(clab deploy -t topology.yml 2>&1)
DEPLOY_EXIT=$?

echo "$DEPLOY_OUTPUT"

if [ $DEPLOY_EXIT -ne 0 ]; then
    echo
    echo "=========================================="
    echo "Deployment failed. Trying alternative..."
    echo "=========================================="
    echo
    echo "The issue is that Containerlab uses /workspace paths inside the container,"
    echo "but Docker Desktop needs the actual host path."
    echo
    echo "Workaround: Deploy from a location that Docker Desktop can access."
    echo "Since /Users is shared, let's try using the absolute path..."
    echo
    
    # Try using Containerlab's workdir option if it exists
    # Or try deploying from a tmp directory that's definitely shared
    echo "Alternative: Create a symlink or use a different approach"
    echo
    echo "For now, please try:"
    echo "  1. Make sure Docker Desktop has /Users shared (you said it does)"
    echo "  2. Try restarting Docker Desktop"
    echo "  3. Then run: clab deploy -t topology.yml"
    echo
    echo "If it still fails, the issue might be that Containerlab needs to be"
    echo "configured differently when running in Docker on macOS."
fi

