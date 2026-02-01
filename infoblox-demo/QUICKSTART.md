# Infoblox Demo - Quick Start Guide

Get up and running with the Infoblox demo project in 5 minutes.

## Step 1: Setup (2 minutes)

```bash
# Navigate to project
cd infoblox-demo

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Start Mock Server (30 seconds)

Open a terminal and run:

```bash
python scripts/start_mock_server.py
```

You should see:
```
Starting Mock Infoblox WAPI server on http://localhost:8080
Press Ctrl+C to stop
```

Keep this terminal open.

## Step 3: Run Your First Example (1 minute)

Open a **new terminal** (keep the mock server running), activate the venv, and run:

```bash
# Activate venv (if not already active)
source .venv/bin/activate

# Run DNS examples
python examples/dns_examples.py
```

You should see output like:
```
=== DNS Management Examples ===

1. Creating A record: web.example.com -> 192.168.1.10
   Created: web.example.com -> 192.168.1.10 (ref: record:a/Z1:a/default)
...
```

## Step 4: Try More Examples (1 minute)

```bash
# DHCP examples
python examples/dhcp_examples.py

# IPAM examples
python examples/ipam_examples.py

# Complete automation workflow
python examples/automation_workflow.py
```

## Step 5: Write Your Own Code (1 minute)

Create a file `my_script.py`:

```python
#!/usr/bin/env python3
from src.infoblox_client import InfobloxClient
from src.dns_manager import DNSManager

# Initialize client (uses mock server by default)
client = InfobloxClient.from_config_file()
dns = DNSManager(client)

# Create a DNS record
record = dns.create_a_record("my-server.example.com", "192.168.1.100")
print(f"Created: {record.name} -> {record.ipv4addr}")

# Search for it
records = dns.get_a_records(name="my-server.example.com")
print(f"Found {len(records)} record(s)")
```

Run it:
```bash
python my_script.py
```

## Common Tasks

### Create DNS Record

```python
from src.infoblox_client import InfobloxClient
from src.dns_manager import DNSManager

client = InfobloxClient.from_config_file()
dns = DNSManager(client)

# A record
dns.create_a_record("web.example.com", "192.168.1.10")

# CNAME
dns.create_cname("www.example.com", "web.example.com")

# PTR (reverse DNS)
dns.create_ptr_record("192.168.1.10", "web.example.com")
```

### Create DHCP Reservation

```python
from src.infoblox_client import InfobloxClient
from src.dhcp_manager import DHCPManager

client = InfobloxClient.from_config_file()
dhcp = DHCPManager(client)

# Create network
dhcp.create_network("192.168.1.0/24")

# Create range
dhcp.create_range("192.168.1.100", "192.168.1.200", "192.168.1.0/24")

# Create reservation
dhcp.create_reservation("192.168.1.50", "00:11:22:33:44:55", name="server-01")
```

### Allocate IP Address

```python
from src.infoblox_client import InfobloxClient
from src.ipam_manager import IPAMManager

client = InfobloxClient.from_config_file()
ipam = IPAMManager(client)

# Create network
ipam.create_network("192.168.1.0/24")

# Get next available IP
ip = ipam.get_next_available_ip("192.168.1.0/24")
print(f"Next IP: {ip}")

# Allocate specific IP
ipam.allocate_ip("192.168.1.0/24", "192.168.1.10", name="web-server")
```

### Complete Workflow: Provision Server

```python
from src.infoblox_client import InfobloxClient
from src.dns_manager import DNSManager
from src.dhcp_manager import DHCPManager
from src.ipam_manager import IPAMManager

client = InfobloxClient.from_config_file()
ipam = IPAMManager(client)
dns = DNSManager(client)
dhcp = DHCPManager(client)

# 1. Get IP
ip = ipam.get_next_available_ip("192.168.1.0/24")

# 2. Allocate in IPAM
ipam.allocate_ip("192.168.1.0/24", ip, name="web-server")

# 3. Create DNS records
dns.create_a_record("web-server.example.com", ip)
dns.create_ptr_record(ip, "web-server.example.com")

# 4. Create DHCP reservation
dhcp.create_reservation(ip, "00:11:22:33:44:55", name="web-server")
```

## Using Real Infoblox

To use a real Infoblox instance:

1. **Update config** (`config/config.yaml`):
```yaml
infoblox:
  use_mock: false
  url: "https://your-infoblox-server.com"
```

2. **Set credentials**:
```bash
export INFOBLOX_USERNAME="your-username"
export INFOBLOX_PASSWORD="your-password"
```

3. **Use normally** - the client automatically detects the configuration.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the example scripts in `examples/`
- Check out the API reference in the README
- Write your own automation workflows

## Troubleshooting

**Mock server won't start?**
- Check if port 8080 is in use: `lsof -i :8080`
- Try a different port in `config/config.yaml`

**Import errors?**
- Make sure you're in the project directory
- Verify virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`

**Connection errors?**
- Ensure mock server is running
- Check the server URL in configuration
- Verify network connectivity (for real Infoblox)

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review example scripts in `examples/`
- Look at the code - it's well-commented!

Happy learning! 🚀
