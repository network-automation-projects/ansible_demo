# Ansible Network Automation Project

A comprehensive Ansible project demonstrating network automation best practices for Cisco IOS devices. This project showcases key Ansible concepts including playbooks, roles, templates, variables, handlers, and Ansible Vault for secure credential management.

## Project Overview

This project provides a complete Ansible-based solution for network device management, including:
- Configuration backups
- Device fact gathering
- Configuration management
- Compliance checking
- Secure credential handling

## Prerequisites

- Python 3.9 or higher
- Ansible 2.9 or higher (or Ansible Core 2.11+)
- Network access to target Cisco devices
- SSH credentials for network devices

## Installation

### 1. Clone or navigate to the project directory

```bash
cd ansible_demo
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ansible collections

```bash
ansible-galaxy collection install -r requirements.yml
```

### 5. Configure inventory

Edit `inventories/hosts.yml` with your network devices. See the inventory file for examples.

### 6. Set up credentials (using Ansible Vault)

For secure credential management, encrypt sensitive data:

```bash
ansible-vault create vault/vault.yml
```

Add your credentials:
```yaml
vault_username: your_username
vault_password: your_password
vault_enable_password: your_enable_password
```

Then reference these in your inventory or group_vars.

## Project Structure

```
ansible_demo/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── requirements.yml          # Ansible collections
├── ansible.cfg              # Ansible configuration
├── .gitignore               # Git ignore patterns
├── inventories/             # Device inventory
│   └── hosts.yml
├── playbooks/               # Ansible playbooks
│   ├── backup_config.yml
│   ├── gather_facts.yml
│   ├── configure_device.yml
│   ├── compliance_check.yml
│   └── run_commands.yml
├── roles/                   # Reusable Ansible roles
│   ├── cisco_backup/
│   └── cisco_config/
├── group_vars/              # Group-level variables
│   └── cisco_devices.yml
├── host_vars/               # Host-specific variables
├── templates/               # Jinja2 templates
├── vault/                   # Encrypted files (Ansible Vault)
│   └── vault.yml.example
├── backups/                 # Configuration backups
├── logs/                    # Ansible logs
├── run_playbook.sh          # Helper script to run playbooks
└── setup.sh                 # Setup script
```

## Usage

### Running Playbooks

#### Using the helper script:

```bash
./run_playbook.sh playbooks/backup_config.yml
```

#### Direct Ansible command:

```bash
ansible-playbook -i inventories/hosts.yml playbooks/backup_config.yml
```

#### With vault password:

```bash
ansible-playbook -i inventories/hosts.yml playbooks/backup_config.yml --ask-vault-pass
```

Or use a vault password file:

```bash
ansible-playbook -i inventories/hosts.yml playbooks/backup_config.yml --vault-password-file ~/.vault_pass
```

### Available Playbooks

#### 1. Backup Configuration (`backup_config.yml`)
Backs up running configurations from Cisco devices.

```bash
ansible-playbook -i inventories/hosts.yml playbooks/backup_config.yml
```

**What it does:**
- Gathers device facts (hostname, version, interfaces)
- Displays device information
- Runs verification commands
- Backs up running configuration
- Saves backup to local `backups/` directory

#### 2. Gather Facts (`gather_facts.yml`)
Comprehensive fact gathering and device information collection.

```bash
ansible-playbook -i inventories/hosts.yml playbooks/gather_facts.yml
```

**What it does:**
- Collects comprehensive device facts
- Gathers interface information
- Collects routing table data
- Generates a device information report

#### 3. Configure Device (`configure_device.yml`)
Configuration management playbook for device changes.

```bash
ansible-playbook -i inventories/hosts.yml playbooks/configure_device.yml
```

**What it does:**
- Applies configuration changes using templates
- Manages interface configurations
- Updates ACLs (if configured)
- Validates configuration changes

#### 4. Compliance Check (`compliance_check.yml`)
Audit playbook checking for security best practices.

```bash
ansible-playbook -i inventories/hosts.yml playbooks/compliance_check.yml
```

**What it does:**
- Checks for security best practices
- Validates password policies
- Checks SNMP configuration
- Verifies logging settings
- Generates compliance report

#### 5. Run Commands (`run_commands.yml`)
Generic playbook for running arbitrary show commands.

```bash
ansible-playbook -i inventories/hosts.yml playbooks/run_commands.yml -e "commands='show ip route,show version'"
```

**What it does:**
- Runs custom show commands
- Displays command output
- Saves output to files (optional)

### Using Roles

Roles provide reusable, modular automation. Example:

```bash
ansible-playbook -i inventories/hosts.yml playbooks/backup_config.yml
```

The playbook uses the `cisco_backup` role, which can be reused across different playbooks.

## Key Ansible Concepts Demonstrated

### 1. Playbooks
Multiple playbooks demonstrate different automation scenarios and use cases.

### 2. Roles
Reusable, modular code organization in `roles/cisco_backup/` and `roles/cisco_config/`.

### 3. Templates
Jinja2 templates in `templates/` for dynamic configuration generation.

### 4. Variables
- **Group variables**: `group_vars/cisco_devices.yml`
- **Host variables**: `host_vars/`
- **Role variables**: Defined in roles

### 5. Inventory
YAML inventory with groups, hosts, and variables in `inventories/hosts.yml`.

### 6. Handlers
Event-driven task execution (see roles for examples).

### 7. Ansible Vault
Secure credential management using encrypted files in `vault/`.

### 8. Best Practices
- Proper project structure
- Comprehensive documentation
- Security awareness (Vault)
- Code organization (roles)

## Configuration

### Ansible Configuration (`ansible.cfg`)

The `ansible.cfg` file configures:
- Inventory path
- Roles path
- Host key checking
- Retry files location
- Logging

### Inventory (`inventories/hosts.yml`)

The inventory file defines:
- Device groups
- Host-specific variables
- Connection parameters
- Credentials (or references to Vault)

### Variables

- **Group variables**: Applied to all devices in a group
- **Host variables**: Applied to specific hosts
- **Role variables**: Defined within roles

## Security Best Practices

1. **Use Ansible Vault** for sensitive data (passwords, API keys)
2. **Never commit** vault password files or unencrypted credentials
3. **Use SSH keys** where possible instead of passwords
4. **Limit access** to inventory and vault files
5. **Review** `.gitignore` to ensure sensitive files are excluded

## Troubleshooting

### Common Issues

1. **Connection Timeouts (Especially with Cisco Sandboxes)**
   - **Sandbox Status**: First, verify your Cisco DevNet sandbox is **Active/Ready** on the DevNet portal
   - **Timeout Settings**: Timeouts have been increased to 60 seconds in `ansible.cfg` and `group_vars/cisco_devices.yml` for sandbox connections
   - **Port Configuration**: Many Cisco sandboxes use non-standard SSH ports (not 22). Check the sandbox "Access" tab:
     - Common ports: `22` (default), `8181`, `2222`, `830` (NETCONF)
     - Update `ansible_port` in `inventories/hosts.yml` if needed
   - **Network Issues**: 
     - Try disabling VPN if active
     - Test with mobile hotspot to rule out corporate firewall blocking
     - Verify basic connectivity: `ping <sandbox_ip>`
   - **Manual SSH Test**: Test connection manually first:
     ```bash
     ssh developer@<sandbox_ip> -p <port>
     ```
     If manual SSH fails, Ansible will also fail - this indicates a sandbox or network issue, not an Ansible problem

2. **Authentication Failures**
   - **Sandbox Credentials**: Verify credentials match the sandbox reservation:
     - Default: `developer` / `C1sco12345`
     - Some sandboxes rotate credentials per reservation - check DevNet portal
     - Copy/paste can include invisible spaces - retype manually if needed
   - **Production**: Verify credentials in inventory or Vault
   - Check device access permissions
   - Ensure SSH is enabled on devices

3. **Sandbox-Specific Issues**
   - **Sandbox Down**: Cisco sandboxes occasionally go down silently. Signs:
     - Connection timeout (not auth failure)
     - Ping works but SSH doesn't
     - Worked yesterday, broken today
   - **Rate Limiting**: Always-On sandboxes may rate-limit connections
   - **Reservable Sandboxes**: Must be started and show "Active" status
   - **Solution**: Check DevNet sandbox comments, try a different sandbox, or retry later

4. **Collection Not Found**
   - Install collections: `ansible-galaxy collection install -r requirements.yml`
   - Verify collection names in playbooks

5. **Vault Errors**
   - Ensure vault password is provided (`--ask-vault-pass` or `--vault-password-file`)
   - Verify vault file path is correct

## Learning Resources

This project demonstrates:
- Ansible playbook structure
- Role-based organization
- Variable management
- Template usage
- Secure credential handling
- Network device automation

## Contributing

This is a learning and portfolio project. Feel free to:
- Add more playbooks
- Create additional roles
- Enhance templates
- Improve documentation

## License

This project is open source and available for educational and portfolio purposes.

## Author

Created as a portfolio project to demonstrate Ansible network automation skills and best practices.

