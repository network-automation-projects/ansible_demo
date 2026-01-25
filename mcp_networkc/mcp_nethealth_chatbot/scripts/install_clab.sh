#!/bin/bash
# Install Containerlab wrapper for Apple Silicon (or other platforms without native binary)

set -e

echo "Installing Containerlab wrapper..."

# Determine installation location
if [ -w /usr/local/bin ]; then
    CLAB_PATH="/usr/local/bin/clab"
elif [ -w ~/.local/bin ]; then
    CLAB_PATH="$HOME/.local/bin/clab"
    mkdir -p ~/.local/bin
    export PATH="$HOME/.local/bin:$PATH"
else
    CLAB_PATH="./clab"
    echo "WARNING: Installing to current directory. Add to PATH manually."
fi

# Create the wrapper script
cat > "$CLAB_PATH" << 'CLABWRAPPER_EOF'
#!/bin/bash
# Containerlab Docker wrapper for platforms without native binary

# Get the absolute path of current directory
CURRENT_DIR=$(pwd)

# Check if running in non-interactive mode (for scripts)
if [ -t 0 ]; then
    IT_FLAG="-it"
else
    IT_FLAG=""
fi

# Mount the host directory and pass it as CLAB_WORKDIR so Containerlab uses host paths for mounts
docker run --rm $IT_FLAG --privileged \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$CURRENT_DIR":/workspace \
  -w /workspace \
  -e CLAB_WORKDIR="$CURRENT_DIR" \
  ghcr.io/srl-labs/clab:latest \
  clab "$@"
CLABWRAPPER_EOF

# Make it executable
chmod +x "$CLAB_PATH"

echo "✓ Containerlab wrapper installed to $CLAB_PATH"

# Test if it works
if command -v docker &> /dev/null; then
    echo "Testing Containerlab installation..."
    if "$CLAB_PATH" version &> /dev/null; then
        echo "✓ Containerlab is working!"
        "$CLAB_PATH" version
    else
        echo "⚠ Containerlab wrapper created but test failed."
        echo "  This might be because the Docker image needs to be pulled first."
        echo "  Try running: docker pull ghcr.io/srl-labs/clab:latest"
    fi
else
    echo "⚠ Docker not found. Install Docker Desktop first."
fi

