# Infoblox Demo

A comprehensive Python-based demo project for Infoblox automation that demonstrates DNS, DHCP, and IPAM (IP Address Management) operations through the Infoblox WAPI (Web API). The project includes a mock Infoblox server for safe testing without requiring real Infoblox hardware.

## Overview

This project provides:

- **Infoblox WAPI Client** - REST API client for interacting with Infoblox
- **DNS Manager** - Create, read, update, and delete DNS records (A, AAAA, CNAME, PTR)
- **DHCP Manager** - Manage DHCP networks, ranges, and reservations
- **IPAM Manager** - IP address allocation, tracking, and network management
- **Mock Infoblox Server** - Flask-based mock server for learning and testing
- **Example Scripts** - Complete workflows demonstrating real-world automation

## Features

### DNS Operations
- Create A, AAAA, CNAME, and PTR records
- Search and filter DNS records
- Update and delete records
- Zone management

### DHCP Operations
- Create and manage DHCP networks
- Define DHCP ranges (IP pools)
- Create static IP reservations
- Query leases and reservations

### IPAM Operations
- Network creation and management
- IP address allocation and tracking
- Next available IP queries
- IP status checking (USED, AVAILABLE, RESERVED)
- Network hierarchy management

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Infoblox Client                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  InfobloxClient (REST API wrapper)                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ DNS Manager  │   │ DHCP Manager  │   │ IPAM Manager │
│              │   │               │   │              │
│ - A records  │   │ - Networks    │   │ - Networks   │
│ - CNAME      │   │ - Ranges      │   │ - IP alloc   │
│ - PTR        │   │ - Reservations│   │ - Tracking   │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────┐
        │   Mock Infoblox WAPI Server          │
        │   (Flask-based, in-memory store)     │
        └──────────────────────────────────────┘
```

## Prerequisites

- **Python 3.9+**
- **pip** - Python package manager
- **Virtual environment** (recommended)

## Quick Start

### 1. Setup Environment

```bash
# Navigate to project directory
cd infoblox-demo

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure (Optional)

Copy the example configuration:

```bash
cp config/config.example.yaml config/config.yaml
```

The default configuration uses the mock server, so no changes are needed to get started.

### 3. Start Mock Server

In one terminal:

```bash
python scripts/start_mock_server.py
```

The mock server will start on `http://localhost:8080`.

### 4. Run Examples

In another terminal (with venv activated):

```bash
# DNS examples
python examples/dns_examples.py

# DHCP examples
python examples/dhcp_examples.py

# IPAM examples
python examples/ipam_examples.py

# Complete automation workflow
python examples/automation_workflow.py
```

## Usage

### Basic Usage

```python
from src.infoblox_client import InfobloxClient
from src.dns_manager import DNSManager
from src.dhcp_manager import DHCPManager
from src.ipam_manager import IPAMManager

# Initialize client (uses mock server by default)
client = InfobloxClient.from_config_file()

# DNS operations
dns = DNSManager(client)
a_record = dns.create_a_record("web.example.com", "192.168.1.10")
records = dns.get_a_records(name="web.example.com")

# DHCP operations
dhcp = DHCPManager(client)
network = dhcp.create_network("192.168.1.0/24")
reservation = dhcp.create_reservation("192.168.1.50", "00:11:22:33:44:55")

# IPAM operations
ipam = IPAMManager(client)
network = ipam.create_network("192.168.1.0/24")
next_ip = ipam.get_next_available_ip("192.168.1.0/24")
ipam.allocate_ip("192.168.1.0/24", "192.168.1.10", name="web-server")
```

### Using Real Infoblox Instance

To use a real Infoblox instance instead of the mock server:

1. Update `config/config.yaml`:
```yaml
infoblox:
  use_mock: false
  url: "https://your-infoblox-server.com"
  username: ""  # Set via environment variable
  password: ""  # Set via environment variable
  verify_ssl: true
```

2. Set environment variables:
```bash
export INFOBLOX_USERNAME="your-username"
export INFOBLOX_PASSWORD="your-password"
```

3. Use the client as normal - it will automatically connect to your Infoblox instance.

## Project Structure

```
infoblox-demo/
├── README.md                 # This file
├── QUICKSTART.md             # Quick start guide
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
├── config/
│   ├── config.example.yaml   # Example configuration
│   └── mock_data.yaml        # Sample data for mock server
├── src/
│   ├── __init__.py
│   ├── infoblox_client.py    # Main Infoblox API client
│   ├── dns_manager.py        # DNS operations
│   ├── dhcp_manager.py       # DHCP operations
│   ├── ipam_manager.py       # IPAM operations
│   └── models.py             # Data models
├── mock_server/
│   ├── __init__.py
│   ├── server.py             # Mock Infoblox WAPI server
│   ├── data_store.py         # In-memory data store
│   └── handlers/
│       ├── dns_handler.py    # DNS endpoint handlers
│       ├── dhcp_handler.py   # DHCP endpoint handlers
│       └── ipam_handler.py   # IPAM endpoint handlers
├── examples/
│   ├── dns_examples.py       # DNS operation examples
│   ├── dhcp_examples.py      # DHCP operation examples
│   ├── ipam_examples.py      # IPAM operation examples
│   └── automation_workflow.py # Complete automation workflow
├── tests/
│   ├── __init__.py
│   ├── test_infoblox_client.py
│   ├── test_dns_manager.py
│   ├── test_dhcp_manager.py
│   └── test_ipam_manager.py
└── scripts/
    └── start_mock_server.py  # Script to start mock server
```

## API Reference

### InfobloxClient

Main client for interacting with Infoblox WAPI.

**Methods:**
- `from_config_file(config_path)` - Create client from config file
- `get(endpoint, params)` - GET request
- `post(endpoint, data, json_data)` - POST request
- `put(endpoint, json_data)` - PUT request
- `delete(endpoint)` - DELETE request
- `search(endpoint, search_params)` - Search for objects

### DNSManager

Manages DNS operations.

**Methods:**
- `create_a_record(name, ipv4addr, comment, ttl)` - Create A record
- `create_aaaa_record(name, ipv6addr, comment, ttl)` - Create AAAA record
- `create_cname(name, canonical, comment, ttl)` - Create CNAME record
- `create_ptr_record(ipv4addr, ptrdname, comment, ttl)` - Create PTR record
- `get_a_records(name, ipv4addr)` - Get A records
- `get_cname_records(name, canonical)` - Get CNAME records
- `get_ptr_records(ipv4addr, ptrdname)` - Get PTR records
- `search_records(name)` - Search all DNS records
- `delete_record(ref)` - Delete DNS record

### DHCPManager

Manages DHCP operations.

**Methods:**
- `create_network(network, comment)` - Create DHCP network
- `get_networks(network)` - Get DHCP networks
- `create_range(start_ip, end_ip, network, comment)` - Create DHCP range
- `get_ranges(network)` - Get DHCP ranges
- `create_reservation(ipv4addr, mac, name, comment)` - Create reservation
- `get_reservations(ipv4addr, mac)` - Get reservations
- `delete_reservation(ref)` - Delete reservation

### IPAMManager

Manages IPAM operations.

**Methods:**
- `create_network(network, comment)` - Create IPAM network
- `get_networks(network)` - Get IPAM networks
- `list_all_networks()` - List all networks
- `get_next_available_ip(network)` - Get next available IP
- `allocate_ip(network, ip, name, comment)` - Allocate IP address
- `get_ip_status(ip)` - Get IP address status
- `release_ip(ip)` - Release IP address

## Example Workflows

### Workflow 1: Provision New Server

```python
# Get next available IP
ip = ipam.get_next_available_ip("192.168.1.0/24")

# Allocate IP in IPAM
ipam.allocate_ip("192.168.1.0/24", ip, name="web-server")

# Create DNS records
dns.create_a_record("web-server.example.com", ip)
dns.create_ptr_record(ip, "web-server.example.com")

# Create DHCP reservation
dhcp.create_reservation(ip, "00:11:22:33:44:55", name="web-server")
```

### Workflow 2: Decommission Server

```python
# Find and delete DNS records
records = dns.search_records("web-server.example.com")
for record in records:
    dns.delete_record(record._ref)

# Delete DHCP reservation
reservations = dhcp.get_reservations(ipv4addr=ip)
for res in reservations:
    dhcp.delete_reservation(res._ref)

# Release IP in IPAM
ipam.release_ip(ip)
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_dns_manager.py

# Run with coverage
pytest --cov=src tests/
```

## Configuration

The project uses YAML configuration files. See `config/config.example.yaml` for all available options:

- `use_mock` - Use mock server (default: true)
- `mock_url` - Mock server URL
- `url` - Real Infoblox server URL
- `username` - Username (or set INFOBLOX_USERNAME env var)
- `password` - Password (or set INFOBLOX_PASSWORD env var)
- `wapi_version` - WAPI version (default: v2.12)
- `verify_ssl` - Verify SSL certificates
- `timeout` - Request timeout in seconds
- `max_retries` - Maximum retry attempts

## Error Handling

The project includes comprehensive error handling:

- `InfobloxClientError` - Base exception
- `InfobloxAuthenticationError` - Authentication failures
- `InfobloxAPIError` - API call failures

All errors are logged and provide clear error messages.

## Logging

The project uses Python's `logging` module. Set log level via environment variable:

```bash
export LOG_LEVEL=DEBUG
python examples/dns_examples.py
```

## Contributing

This is a demo project. Feel free to:

- Add more examples
- Extend functionality
- Improve error handling
- Add more tests

## License

This project is for educational purposes.

## References

- [Infoblox WAPI Documentation](https://docs.infoblox.com/)
- [Infoblox REST API Guide](https://docs.infoblox.com/display/API/Infoblox+REST+API+Guide)

## Troubleshooting

### Mock Server Won't Start

- Ensure port 8080 is not in use
- Check Python version (3.9+)
- Verify all dependencies are installed

### Connection Errors

- Verify mock server is running
- Check configuration file path
- Ensure network connectivity (for real Infoblox)

### Authentication Errors

- Verify credentials are correct
- Check environment variables are set
- Ensure SSL verification settings match your environment
