# Cisco Backup Role

This role handles backup operations for Cisco IOS devices.

## Purpose

The `cisco_backup` role provides a reusable way to backup Cisco device configurations with consistent naming, reporting, and storage.

## Usage

### Basic Usage

```yaml
- name: Backup Cisco devices
  hosts: cisco_devices
  roles:
    - cisco_backup
```

### With Custom Variables

```yaml
- name: Backup with custom destination
  hosts: cisco_devices
  roles:
    - role: cisco_backup
      vars:
        backup_dest_dir: /path/to/backups
        generate_report: true
```

## Role Variables

### Default Variables

- `backup_dest_dir`: Directory to store backups (default: `backups`)
- `generate_report`: Whether to generate backup report (default: `true`)
- `backup_filename_format`: Format for backup filenames

### Override Variables

You can override these variables in:
- Playbook `vars:` section
- `group_vars/` files
- `host_vars/` files
- Role invocation

## Tasks

1. Gathers device facts
2. Displays device information
3. Backs up running configuration
4. Saves backup to local directory
5. Generates backup report (optional)

## Handlers

- `backup_completed`: Triggered when backup is successfully saved

## Templates

- `backup_report.j2`: Jinja2 template for backup reports

## Dependencies

- Requires `cisco.ios` collection
- Requires network connectivity to target devices

