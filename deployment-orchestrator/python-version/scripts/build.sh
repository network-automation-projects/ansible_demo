#!/bin/bash
# Build script for Python deployment orchestrator
# Builds Docker image

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

IMAGE_NAME="deployctl-python"
VERSION="${1:-latest}"

echo "Building Docker image: $IMAGE_NAME:$VERSION"

cd "$PROJECT_DIR"

docker build -t "$IMAGE_NAME:$VERSION" .

echo "✓ Build complete!"
echo ""
echo "To run the container:"
echo "  docker run --rm $IMAGE_NAME:$VERSION --help"
