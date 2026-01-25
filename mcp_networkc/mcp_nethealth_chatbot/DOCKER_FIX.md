# Fixing Docker Desktop File Sharing Issue

## Problem
When deploying Containerlab on macOS, you may see errors like:
```
mounts denied: The path /workspace/clab-mcp-nethealth-chatbot/router1/config is not shared from the host
```

## Solution: Configure Docker Desktop File Sharing

1. **Open Docker Desktop**
   - Click the Docker icon in your menu bar
   - Select "Settings" or "Preferences"

2. **Navigate to File Sharing**
   - Go to: **Settings → Resources → File Sharing**

3. **Add the Required Directory**
   - Click the "+" button to add a new path
   - Add this directory:
     ```
     /Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering
     ```
   - Or add the entire Documents folder:
     ```
     /Users/rebeccaclarke/Documents
     ```
   - Click "Apply & Restart"

4. **Wait for Docker to Restart**
   - Docker Desktop will restart to apply the changes

5. **Redeploy the Topology**
   ```bash
   cd /Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering/conceptprojects/mcp_networkc/mcp_nethealth_chatbot
   clab destroy -t topology.yml
   clab deploy -t topology.yml
   ```

## Alternative: Use Docker Desktop's Default Shared Directories

If you don't want to add custom paths, you can:
1. Move the project to a directory Docker Desktop already shares (like `/Users` or `/tmp`)
2. Or work from within Docker Desktop's default shared directories

## Verify It's Working

After adding the directory and redeploying, check:
```bash
docker ps | grep router
```

You should see both routers running:
- `clab-mcp-nethealth-chatbot-router1`
- `clab-mcp-nethealth-chatbot-router2`

