# Module 04: Device Management

Connecting to and managing network devices using Netmiko, NAPALM, and Paramiko.

## Learning Objectives

By completing this module, you will learn:

- How to establish SSH connections to network devices
- How to execute commands and gather facts
- How to deploy configurations safely
- How to use vendor-agnostic libraries (NAPALM)
- How to handle connection errors and timeouts

## Prerequisites

- Module 01: Core Fundamentals
- Module 03: File I/O Operations
- Basic understanding of SSH and network devices

## Concepts Covered

### Netmiko
- `ConnectHandler` - Establish SSH connections
- `send_command` - Execute show commands
- `send_config_set` - Send configuration commands
- `save_config` - Save running config
- `disconnect` - Close connections
- `enable` - Enter privileged mode

### NAPALM
- `get_network_driver` - Get vendor driver
- `get_facts` - Gather device facts
- `get_interfaces` - Get interface information
- `get_bgp_neighbors` - Get BGP neighbor status
- `load_merge_candidate` - Stage configuration
- `compare_config` - Compare candidate vs running
- `commit_config` - Apply configuration
- `discard_config` - Discard staged config
- `close` - Close connection

### Paramiko
- `SSHClient` - Low-level SSH client
- `connect` - Establish connection
- `exec_command` - Execute commands
- `SFTPClient` - File transfer

## Use Cases in Network Automation

### Device Connection
- Connect to routers and switches via SSH
- Handle authentication and timeouts
- Support multiple vendors

### Facts Gathering
- Collect device information (hostname, version, serial)
- Gather interface details
- Retrieve BGP neighbor information

### Configuration Deployment
- Deploy configuration changes safely
- Compare before and after configs
- Rollback on errors

### Backup Operations
- Backup device configurations
- Save running configs to files
- Restore from backups

## Related Modules

- **Module 01:** Core Fundamentals (prerequisite)
- **Module 03:** File I/O (for saving configs)
- **Module 08:** Concurrency (for parallel device operations)

## Exercises

Work through `exercises.py` to practice these concepts with fill-in-the-blank exercises.

## Examples

Review `examples.py` for complete, production-ready implementations.

## Note

These examples use mock connections for safety. In production, ensure you have:
- Proper credentials management
- Network connectivity to devices
- Appropriate permissions
- Backup procedures before changes
