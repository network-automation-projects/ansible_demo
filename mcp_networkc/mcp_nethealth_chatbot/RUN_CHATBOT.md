# Quick Start Guide - Running the Network Health Chatbot

## Step 1: Install Python Dependencies

Run this command in your terminal:

```bash
cd /Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering/conceptprojects/mcp_networkc/mcp_nethealth_chatbot
pip3 install -r requirements.txt
```

If you encounter permission issues, try:
```bash
pip3 install --user -r requirements.txt
```

Or use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Set OpenAI API Key

You need an OpenAI API key to use the chatbot. Set it as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
export OPENAI_MODEL='gpt-4'  # or 'gpt-3.5-turbo'
```

**Note:** Get your API key from https://platform.openai.com/api-keys

## Step 3: Deploy Network Topology

Deploy the Containerlab network topology:

```bash
clab deploy -t topology.yml
```

**If you get an error that containers already exist**, use one of these options:

**Option A: Reconfigure existing containers (recommended)**
```bash
clab deploy -t topology.yml --reconfigure
```

**Option B: Destroy and redeploy**
```bash
clab destroy -t topology.yml
clab deploy -t topology.yml
```

Wait for the routers to start (this may take a minute or two). Verify they're running:

```bash
docker ps | grep router
```

You should see:
- `clab-mcp-nethealth-chatbot-router1`
- `clab-mcp-nethealth-chatbot-router2`

## Step 4: (Optional) Start Prometheus

If you want metrics collection:

```bash
cd prometheus
docker run -d \
  --name prometheus-nethealth \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus:latest
```

Verify Prometheus is running:
```bash
curl http://localhost:9090/api/v1/query?query=up
```

## Step 5: Run the Chatbot

### Option A: Interactive Mode (Recommended)

```bash
python3 network_agent.py --interactive
```

This will start an interactive session where you can ask questions about the network.

### Option B: Single Query

```bash
python3 network_agent.py --query "Check network health" --router router1
```

### Option C: Demo Queries

```bash
python3 scripts/demo_queries.py
```

## Example Queries

Once running, try these queries:

- "Check the network health status"
- "What is the status of router1?"
- "Are there any interface issues?"
- "Compare current network state with historical data"

## Troubleshooting

### If dependencies fail to install:
- Try: `python3 -m pip install --user -r requirements.txt`
- Or use a virtual environment (see Step 1)

### If Containerlab fails:
- Make sure Docker Desktop is running
- Check: `docker ps` should work
- Verify Containerlab: `clab version`

### If OpenAI API errors:
- Verify your API key: `echo $OPENAI_API_KEY`
- Make sure you have credits in your OpenAI account

### If routers don't start:

**First, run the diagnostic script:**
```bash
bash scripts/diagnose_routers.sh
```

**Common issues and solutions:**

1. **"mounts denied" error with `/workspace` path:**
   This is the most common issue on macOS with Containerlab Docker wrapper.
   
   **Quick fixes to try:**
   - **Restart Docker Desktop** - Often fixes file sharing recognition
   - **Update Docker Desktop** - Make sure you have the latest version
   - **Try VirtioFS**: Docker Desktop → Settings → General → Enable "Use VirtioFS for file sharing"
   - **Deploy from simpler path**: Try `cd /tmp && mkdir test && cd test` then copy topology.yml and deploy
   
   **Root cause**: Containerlab wrapper uses `/workspace` inside container, but Docker Desktop needs host paths.
   See [DOCKER_FIX_V2.md](DOCKER_FIX_V2.md) for detailed solutions.

2. **No containers found at all:**
   - Check Docker Desktop is running: `docker ps` should work
   - Verify Containerlab: `clab version`
   - Try deploying: `clab deploy -t topology.yml`
   - Check for errors in the deployment output

3. **Containers exist but are stopped:**
   - Check logs: `docker logs clab-mcp-nethealth-chatbot-router1`
   - Check all containers: `docker ps -a | grep router`
   - Try restarting: `docker start clab-mcp-nethealth-chatbot-router1`
   - Or redeploy: `clab destroy -t topology.yml && clab deploy -t topology.yml`

4. **Containerlab permission errors:**
   - If using Docker wrapper, ensure Docker Desktop is running
   - Try: `docker pull ghcr.io/srl-labs/clab:latest`
   - Verify wrapper: `cat /usr/local/bin/clab`

## Router Credentials

Set the following environment variables before running:
```bash
export ROUTER_USERNAME='admin'
export ROUTER_PASSWORD='your-router-password'
```

Or create a `.env` file (see `.env.example`) and source it:
```bash
source .env
```

## Stopping Everything

To clean up:

```bash
# Stop and remove network topology
clab destroy -t topology.yml

# Stop Prometheus (if running)
docker stop prometheus-nethealth
docker rm prometheus-nethealth
```

