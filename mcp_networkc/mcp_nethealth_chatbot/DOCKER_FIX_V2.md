# Fixing Docker Desktop File Sharing Issue - Solution

## Problem
When deploying Containerlab on macOS using the Docker wrapper, you get:
```
Error response from daemon: mounts denied: 
The path /workspace/clab-mcp-nethealth-chatbot/router1/config is not shared from the host
```

## Root Cause
Containerlab runs inside a Docker container (via the wrapper). It creates paths like `/workspace/clab-*/router*/config` inside that container, then tries to mount those paths into router containers. Docker Desktop doesn't recognize `/workspace` - it only knows about actual host paths.

## Solution Options

### Option 1: Use Native Containerlab (Best, if available)
If you're on Intel Mac or can install native Containerlab:
```bash
# Install native Containerlab
bash -c "$(curl -sL https://get.containerlab.dev)"
```

### Option 2: Fix Docker Desktop File Sharing
Even though `/Users` is shared, Docker Desktop might need the exact path. Try:

1. **Restart Docker Desktop** - Sometimes Docker needs a restart to recognize shared paths
2. **Check Docker Desktop version** - Update to latest version
3. **Try VirtioFS** - In Docker Desktop Settings → General → Use VirtioFS for file sharing

### Option 3: Work Around the Wrapper Issue
The Containerlab Docker wrapper creates the `/workspace` issue. We can try:

1. **Deploy from a simpler path** - Try deploying from `/tmp` or `/Users/rebeccaclarke` directly
2. **Use bind mounts differently** - Modify how Containerlab creates mounts

### Option 4: Use Docker Compose Instead
Deploy routers directly with Docker Compose instead of Containerlab:

```yaml
# docker-compose.yml
version: '3.8'
services:
  router1:
    image: ghcr.io/nokia/srlinux:latest
    container_name: clab-mcp-nethealth-chatbot-router1
    # ... configuration
```

## Quick Test

Try this to see if it's a path issue:
```bash
# Deploy from a simpler location
cd /tmp
mkdir test-clab && cd test-clab
# Copy your topology.yml here
clab deploy -t topology.yml
```

If this works, the issue is with the nested path structure.

## Recommended Next Steps

1. **First, try restarting Docker Desktop** - This often fixes file sharing issues
2. **Then try deploying again**: `clab deploy -t topology.yml`
3. **If still failing**, check Docker Desktop logs for more details
4. **As last resort**, consider using native Containerlab or Docker Compose

