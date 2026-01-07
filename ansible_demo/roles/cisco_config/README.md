# Cisco Config Role

This role handles configuration management for Cisco IOS devices.

## Purpose

The `cisco_config` role provides a reusable way to apply configurations to Cisco devices with backup, validation, and reporting capabilities.

## Usage

### Basic Usage

```yaml
- name: Configure Cisco devices
  hosts: cisco_devices
  roles:
    - cisco_config
  vars:
    config_lines:
      - "hostname NEW_HOSTNAME"
      - "ip domain-name example.com"
```

### With Template

```yaml
- name: Configure from template
  hosts: cisco_devices
  roles:
    - role: cisco_config
      vars:
        config_template: templates/router_config.j2
```

### With Interface Configuration

```yaml
- name: Configure interfaces
  hosts: cisco_devices
  roles:
    - role: cisco_config
      vars:
        interface_configs:
          - name: GigabitEthernet0/0
            config:
              - "description Management Interface"
              - "ip address 192.168.1.1 255.255.255.0"
              - "no shutdown"
```

## Role Variables

### Default Variables

- `backup_dest_dir`: Directory to store backups (default: `backups`)
- `backup_before_change`: Backup before applying changes (default: `true`)
- `backup_after_change`: Backup after applying changes (default: `true`)
- `validate_config`: Validate configuration after changes (default: `true`)
- `generate_report`: Whether to generate configuration report (default: `true`)

### Configuration Variables

- `config_template`: Path to Jinja2 template file
- `config_lines`: List of configuration lines to apply
- `interface_configs`: List of interface configurations

## Tasks

1. Gathers device facts
2. Backs up configuration before changes (optional)
3. Applies configuration from template or lines
4. Applies interface configurations (if provided)
5. Validates configuration (optional)
6. Backs up configuration after changes (optional)
7. Generates configuration report (optional)

## Handlers

- `config_applied`: Triggered when configuration is successfully applied

## Templates

- `config_report.j2`: Jinja2 template for configuration reports

## Dependencies

- Requires `cisco.ios` collection
- Requires network connectivity to target devices

## Best Practices

1. Always enable `backup_before_change` in production
2. Use templates for complex configurations
3. Validate configurations after changes
4. Review reports before considering changes complete

