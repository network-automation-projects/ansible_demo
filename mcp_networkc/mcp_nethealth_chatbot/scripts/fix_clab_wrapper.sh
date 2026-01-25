#!/bin/bash
# Fix Containerlab wrapper to handle Docker Desktop file sharing on macOS

set -e

echo "Fixing Containerlab wrapper for Docker Desktop file sharing..."
echo

# Check if clab exists
if ! command -v clab &> /dev/null; then
    echo "ERROR: Containerlab not found. Install it first with: bash scripts/install_clab.sh"
    exit 1
fi

CLAB_PATH=$(which clab)
echo "Found Containerlab at: $CLAB_PATH"
echo

# Backup original
if [ ! -f "${CLAB_PATH}.backup" ]; then
    echo "Creating backup: ${CLAB_PATH}.backup"
    cp "$CLAB_PATH" "${CLAB_PATH}.backup"
fi

# Create fixed wrapper
echo "Creating fixed wrapper..."
cat > "$CLAB_PATH" << 'EOF'
#!/bin/bash
# Containerlab Docker wrapper for platforms without native binary
# Fixed for Docker Desktop file sharing on macOS

# Get the absolute path of current directory
CURRENT_DIR=$(pwd)

# Check if running in non-interactive mode (for scripts)
if [ -t 0 ]; then
    IT_FLAG="-it"
else
    IT_FLAG=""
fi

# Mount the host directory and pass CLAB_WORKDIR so Containerlab uses host paths
# This ensures Docker Desktop can access the paths Containerlab creates
docker run --rm $IT_FLAG --privileged \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$CURRENT_DIR":/workspace \
  -w /workspace \
  -e CLAB_WORKDIR="$CURRENT_DIR" \
  ghcr.io/srl-labs/clab:latest \
  clab "$@"
EOF

chmod +x "$CLAB_PATH"

echo "✓ Wrapper updated"
echo
echo "Testing Containerlab..."
if clab version &> /dev/null; then
    echo "✓ Containerlab is working!"
    clab version
else
    echo "⚠ Containerlab test failed - check Docker Desktop is running"
fi
echo
echo "You can now try deploying: clab deploy -t topology.yml"

