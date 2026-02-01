# MCP Network Health Chatbot

An AI-powered network monitoring assistant using MCP (Model Context Protocol) that maintains persistent context across interactions. This system monitors virtual network devices (Containerlab), queries device status/metrics, stores historical context via MCP, and provides AI-driven insights using OpenAI.

## 🎯 Overview

This project demonstrates how to build an intelligent network monitoring system that:
- **Monitors network devices** via Netmiko (SSH-based automation)
- **Maintains persistent context** using MCP for historical tracking
- **Integrates with Prometheus** for metrics collection
- **Provides AI-powered insights** using OpenAI GPT models
- **Remembers past issues** and provides context-aware recommendations

Perfect for demonstrating AI/ML applications in network operations, SRE practices, and automation skills.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Containerlab Network                      │
│  ┌──────────────┐              ┌──────────────┐           │
│  │   router1    │◄─────────────►│   router2    │           │
│  │ Nokia SR L   │  ethernet-1/1│ Nokia SR L   │           │
│  └──────────────┘              └──────────────┘           │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ Netmiko SSH
                            │
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  network_monitor_server.py                           │  │
│  │  - check_interface_status                            │  │
│  │  - get_device_info                                   │  │
│  │  - store_network_context                             │  │
│  │  - retrieve_network_context                          │  │
│  │  - query_prometheus                                  │  │
│  │  - detect_issues                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                │
│                            ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MCP Context Storage (In-Memory/Persistent)         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  network_agent.py                                     │  │
│  │  - Retrieves context from MCP                        │  │
│  │  - Queries network state                              │  │
│  │  - Calls OpenAI API                                  │  │
│  │  - Updates context with insights                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Prometheus                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Metrics Collection & Query API                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- **Docker Desktop** - For running containers
- **Containerlab** - For network topology simulation
  ```bash
  # macOS (Intel)
  brew install containerlab
  
  # macOS (Apple Silicon) or if brew install fails
  # The setup script will automatically install a Docker-based wrapper
  bash scripts/install_clab.sh
  
  # Linux
  bash -c "$(curl -sL https://get.containerlab.dev)"
  
  # Note: Apple Silicon users - Containerlab doesn't have native ARM64 binaries.
  # The setup script will automatically install a Docker wrapper for you.
  ```
- **Python 3.11+** - For running the MCP server and AI agent
- **OpenAI API Key** - Get one from https://platform.openai.com/api-keys
- **Network Access** - To pull Docker images (Nokia SR Linux, Prometheus)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd ConceptProjects/mcp_networkc/mcp_nethealth_chatbot
```

### 2. Install Dependencies

```bash
# Run the setup script
./scripts/setup.sh

# Or manually:
pip3 install -r requirements.txt
```

### 3. Set Environment Variables

```bash
# Required: OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
export OPENAI_MODEL='gpt-4'  # or 'gpt-3.5-turbo'

# Required: Router credentials (for Containerlab Nokia SR Linux)
export ROUTER_USERNAME='admin'
export ROUTER_PASSWORD='your-router-password'

# Optional
export PROMETHEUS_URL='http://localhost:9090'
export ROUTER_PORT='22'  # Default: 22
```

**Note:** For security, create a `.env` file (see `.env.example`) and load it:
```bash
# Using python-dotenv (install with: pip install python-dotenv)
source .env  # or use: export $(cat .env | xargs)
```

### 4. Deploy Network Topology

```bash
# Deploy the Containerlab topology
clab deploy -t topology.yml

# Verify routers are running
docker ps | grep router
```

The routers will be accessible at:
- `clab-mcp-nethealth-chatbot-router1`
- `clab-mcp-nethealth-chatbot-router2`

**Router Credentials:**
- Set `ROUTER_USERNAME` and `ROUTER_PASSWORD` environment variables
- Default username is `admin` if not set
- Password must be set via `ROUTER_PASSWORD` environment variable
- See `.env.example` for configuration template

### 5. Start Prometheus (Optional)

```bash
cd prometheus
docker run -d \
  --name prometheus-nethealth \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus:latest

# Verify Prometheus is running
curl http://localhost:9090/api/v1/query?query=up
```

### 6. Test MCP Server

```bash
# In one terminal, run the MCP server
python3 network_monitor_server.py
```

The server will communicate via stdio (standard input/output) as per MCP protocol.

### 7. Run the AI Agent

```bash
# Interactive mode
python3 network_agent.py --interactive

# Single query
python3 network_agent.py --query "Check network health" --router router1

# Demo queries
python3 scripts/demo_queries.py
```

## 📖 Usage Examples

### Example 1: Basic Health Check

```bash
python3 network_agent.py --query "Check the network health status" --router router1
```

**Expected Output:**
```
AI Response:
Current Network Status Assessment:
- Router1 is operational with interface ethernet-1/1 in UP state
- No critical issues detected
- System uptime: [retrieved from device]
- All interfaces are functioning normally

Recommended Actions:
- Continue monitoring interface status
- Check Prometheus metrics for historical trends
```

### Example 2: Context-Aware Query

```bash
python3 network_agent.py --query "Are there any latency issues? Compare with yesterday's data" --router router1
```

**Expected Output:**
```
AI Response:
Latency Analysis:
- Current latency measurements: [from Prometheus/metrics]
- Historical context shows: [from stored MCP context]
- Comparison: Similar to yesterday's spike at 14:30, interface eth-1/1 shows elevated latency
- Previous resolution: Interface restart resolved the issue

Recommendation:
- Monitor for 5 minutes
- If latency persists, restart interface ethernet-1/1
- Reference: Similar issue resolved on 2025-01-XX with interface restart
```

### Example 3: Diagnostic Query

```bash
python3 network_agent.py --query "Diagnose any network problems and suggest fixes" --router router2
```

## 🔧 MCP Server Tools

The MCP server exposes the following tools:

### `check_interface_status`
Query interface status on a network device.

**Parameters:**
- `router` (string): Router name ("router1" or "router2")

**Example:**
```python
{
  "router": "router1"
}
```

### `get_device_info`
Get device information including hostname, version, uptime.

**Parameters:**
- `router` (string): Router name

### `store_network_context`
Store network state to MCP persistent storage.

**Parameters:**
- `device` (string): Device/router name
- `interfaces` (array): Interface status objects
- `alerts` (array): Alert messages
- `metrics` (object): Additional metrics

### `retrieve_network_context`
Retrieve historical network context.

**Parameters:**
- `device` (string, optional): Device name filter
- `limit` (integer): Max entries to return (default: 10)

### `query_prometheus`
Query Prometheus metrics API.

**Parameters:**
- `query` (string): PromQL query string
- `prometheus_url` (string): Prometheus API URL (default: http://localhost:9090)

### `detect_issues`
Analyze network state and detect issues.

**Parameters:**
- `router` (string): Router name
- `check_interfaces` (boolean): Check interface status
- `check_latency` (boolean): Check for latency issues

## 🐳 Docker Integration

### Build MCP Server Image

```bash
docker build -t network-monitor-mcp:latest .
```

### Run MCP Server in Docker

```bash
docker run -it --rm \
  --network clab \
  network-monitor-mcp:latest
```

### Add to Docker MCP Catalog

1. Copy `catalog.yaml` to `~/.docker/mcp/catalogs/`
2. Update `~/.docker/mcp/registry.yaml`:

```yaml
network-monitor:
  ref: network-monitor-mcp:latest
```

3. Restart Docker Desktop or your MCP client

## 📊 Prometheus Integration

The system can query Prometheus for metrics. Example queries:

```promql
# Check if targets are up
up{job="containerlab-routers"}

# Interface errors
interface_errors_total{device="router1"}

# Interface packets
interface_packets_total{device="router1",direction="in"}
```

Configure Prometheus scrape targets in `prometheus/prometheus.yml`.

## 🧪 Testing

### Test MCP Server Tools

```bash
# Test interface status check
python3 -c "
import asyncio
from network_monitor_server import query_device
print(query_device('router1', 'show interface ethernet-1/1 state'))
"
```

### Test AI Agent

```bash
# Run demo queries
python3 scripts/demo_queries.py

# Run single query
python3 scripts/demo_queries.py --query "Check router1 status" --router router1
```

### Test Prometheus Integration

```bash
# Query Prometheus directly
curl "http://localhost:9090/api/v1/query?query=up"

# Test via MCP tool
python3 network_agent.py --query "Query Prometheus for up metrics"
```

## 🐛 Troubleshooting

### Issue: Cannot connect to routers

**Solution:**
```bash
# Verify Containerlab topology is deployed
clab inspect -t topology.yml

# Check router containers
docker ps | grep router

# Test SSH connectivity
ssh admin@clab-mcp-nethealth-chatbot-router1
# Password: Use the value from ROUTER_PASSWORD environment variable
```

### Issue: OpenAI API errors

**Solution:**
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Issue: Containerlab installation fails (especially on Apple Silicon)

**Solution:**
```bash
# Apple Silicon users: Use the Docker wrapper installer
bash scripts/install_clab.sh

# Verify the wrapper was installed
which clab
clab version

# If clab command not found, add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or manually create the wrapper
cat > /usr/local/bin/clab << 'EOF'
#!/bin/bash
docker run --rm -it --privileged \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)":/workspace \
  -w /workspace \
  ghcr.io/srl-labs/clab:latest \
  "$@"
EOF
chmod +x /usr/local/bin/clab

# Pull the Docker image
docker pull ghcr.io/srl-labs/clab:latest
```

### Issue: Prometheus not accessible

**Solution:**
```bash
# Check if Prometheus is running
docker ps | grep prometheus

# Check Prometheus logs
docker logs prometheus-nethealth

# Verify port is accessible
curl http://localhost:9090/api/v1/query?query=up
```

### Issue: MCP server connection fails

**Solution:**
```bash
# Verify Python dependencies
pip3 list | grep mcp

# Test MCP server directly
python3 network_monitor_server.py

# Check for import errors
python3 -c "from mcp.server import Server; print('MCP OK')"
```

## 📁 Project Structure

```
mcp_nethealth_chatbot/
├── topology.yml                    # Containerlab topology
├── network_monitor_server.py       # MCP server implementation
├── network_agent.py                # AI agent with OpenAI integration
├── Dockerfile                       # MCP server container
├── requirements.txt                # Python dependencies
├── catalog.yaml                     # Docker MCP catalog entry
├── README.md                        # This file
├── prometheus/
│   ├── prometheus.yml              # Prometheus configuration
│   └── Dockerfile                  # Prometheus container
└── scripts/
    ├── setup.sh                    # Setup script
    └── demo_queries.py             # Demo queries
```

## 🔐 Security Notes

- **API Keys**: Never commit API keys to version control. Use environment variables.
- **Network Access**: Containerlab routers are isolated in Docker network by default.
- **Credentials**: Default Nokia SR Linux credentials are for demo purposes only.
- **Production**: For production use, implement proper secret management (e.g., Docker secrets, Vault).

## 🚀 Scaling to Production

To scale this to real networks:

1. **Replace Containerlab** with real network devices (Cisco, Juniper, Arista, etc.)
2. **Add authentication** via secrets management (HashiCorp Vault, AWS Secrets Manager)
3. **Persistent storage** for MCP context (PostgreSQL, Redis)
4. **Monitoring** integration (Grafana, Datadog, New Relic)
5. **Alerting** (PagerDuty, Slack, email)
6. **Multi-tenant** support for different network environments

## 📚 References

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Containerlab Documentation](https://containerlab.dev/)
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Prometheus Documentation](https://prometheus.io/docs/)

## 🤝 Contributing

This is a demo project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- Inspired by NetworkChuck's MCP tutorial
- Uses Nokia SR Linux for network simulation
- Built with MCP (Model Context Protocol) by Anthropic

---

**Built for demonstrating AI/ML applications in network operations and SRE practices.**

