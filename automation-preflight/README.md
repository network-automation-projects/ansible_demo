# Automation Preflight Validation Tool

A Python CLI tool that validates network device readiness before automation runs. This tool acts as a guardrail to ensure devices meet required preconditions before making configuration changes.

## Why This Tool?

**Interview Value:** Demonstrates senior-level "validation before changes" thinking, showing you understand the importance of safety checks in network automation.

**Real-World Use:** Prevents unsafe automation runs by validating:
- Device connectivity and accessibility
- OS version compatibility
- Device stability (uptime checks)
- Required configuration variables

## Features

- **YAML Inventory Support**: Load devices from structured inventory files
- **Multiple Validation Checks**:
  - Hostname presence and validity
  - OS version compatibility (configurable minimums)
  - Uptime thresholds (ensures device stability)
  - Required variables validation
- **Mock Mode**: Safe testing without live device connections (`--mock` flag)
- **Dry-Run Mode**: Validate configuration without connecting (`--dry-run`)
- **Flexible Output**: Human-readable text or structured JSON
- **Structured Logging**: Detailed logs for debugging and audit trails
- **Exit Codes**: Integration-friendly (0=pass, 1=fail, 2=config error)

## Requirements

- Python 3.9+
- Dependencies (see `requirements.txt`):
  - `netmiko>=4.3.0` (for device connections)
  - `pyyaml>=6.0` (for inventory parsing)
  - `pydantic>=2.0.0` (for data validation)
  - `packaging>=21.0` (for version comparison)

## Installation

1. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Configure Inventory

Edit `config/inventory.yaml` with your devices:

```yaml
devices:
  - hostname: r1.example.com
    ip: 192.168.1.1
    device_type: cisco_ios
    uptime_threshold: 3600  # Optional: require 1 hour uptime
    os_version_min: "16.0"  # Optional: minimum OS version

  - hostname: r2.example.com
    ip: 192.168.1.2
    device_type: cisco_ios
```

### 2. Set Credentials

Use environment variables (recommended):

```bash
export NET_USER=admin
export NET_PASS=secretpassword
```

### 3. Run Validation

**Mock mode (safe for demos):**
```bash
python preflight.py --mock
```

**Real device connections:**
```bash
python preflight.py
```

**Dry-run mode (validates config only):**
```bash
python preflight.py --dry-run
```

**JSON output:**
```bash
python preflight.py --output-format json
```

## Usage Examples

### Basic Validation

```bash
# Validate all devices in default inventory
python preflight.py --mock

# Use custom inventory file
python preflight.py --inventory /path/to/inventory.yaml --mock
```

### Text Output Example

```
=== Preflight Validation Results ===

Device: r1.example.com (192.168.1.1)
Status: ✓ PASS
  ✓ Hostname present
  ✓ OS version supported (17.03.01a >= 16.0)
  ✓ Uptime sufficient (86400s >= 0s)
  ✓ Required variables defined

Device: r2.example.com (192.168.1.2)
Status: ✗ FAIL
  ✓ Hostname present
  ✗ OS version not supported (15.5.3 < 16.0)
  ✓ Uptime sufficient (7200s >= 0s)
  ✓ Required variables defined

=== Summary ===
Total devices: 2
Passed: 1
Failed: 1
```

### JSON Output Example

```bash
python preflight.py --output-format json --mock
```

```json
{
  "summary": {
    "total": 2,
    "passed": 1,
    "failed": 1
  },
  "devices": [
    {
      "hostname": "r1.example.com",
      "ip": "192.168.1.1",
      "status": "pass",
      "checks": {
        "hostname": {"status": "pass", "reason": null},
        "os_version": {"status": "pass", "reason": null},
        "uptime": {"status": "pass", "reason": null},
        "variables": {"status": "pass", "reason": null}
      }
    }
  ]
}
```

## CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--inventory` | Path to inventory YAML file | `config/inventory.yaml` |
| `--mock` | Use mock device facts (no real connections) | `False` |
| `--dry-run` | Validate config without connecting (same as `--mock`) | `False` |
| `--output-format` | Output format: `text` or `json` | `text` |
| `--log-level` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |

## Exit Codes

- `0`: All devices passed validation
- `1`: One or more devices failed validation
- `2`: Configuration error (e.g., missing inventory file)

## Project Structure

```
automation-preflight/
├── preflight.py              # Main CLI entry point
├── core/
│   ├── inventory.py          # YAML inventory loading
│   ├── validator.py          # Core validation logic
│   └── connection.py         # Device connection (real/mock)
├── models/
│   └── device.py             # Pydantic models for device data
├── config/
│   └── inventory.yaml        # Example inventory file
├── logs/                     # Auto-created log directory
├── requirements.txt
├── README.md
└── tests/
    └── test_validator.py     # Unit tests
```

## Validation Checks

### Hostname Check
- **Purpose**: Verify device hostname is present and valid
- **Pass**: Hostname detected from device
- **Fail**: Hostname missing or empty

### OS Version Check
- **Purpose**: Ensure device OS version meets minimum requirements
- **Pass**: OS version >= minimum (configurable per device or device type)
- **Fail**: OS version below minimum or version not detected
- **Default minimums**: Cisco IOS XE >= 16.0, NX-OS >= 7.0

### Uptime Check
- **Purpose**: Ensure device has been up long enough (indicates stability)
- **Pass**: Uptime >= threshold (default: 0 seconds)
- **Fail**: Uptime below threshold or not detected
- **Configurable**: Set `uptime_threshold` per device in inventory

### Required Variables Check
- **Purpose**: Verify all required inventory fields are present
- **Pass**: All required fields (`hostname`, `ip`, `device_type`) present
- **Fail**: Missing required field(s)

## Inventory Format

```yaml
devices:
  - hostname: r1.example.com        # Required
    ip: 192.168.1.1                 # Required
    device_type: cisco_ios          # Required
    port: 22                        # Optional (default: 22)
    uptime_threshold: 3600          # Optional (default: 0)
    os_version_min: "16.0"          # Optional (uses device type default if not set)
    # username/password from env vars (NET_USER, NET_PASS)
```

## Credentials

Credentials can be provided via:

1. **Environment variables** (recommended):
   ```bash
   export NET_USER=admin
   export NET_PASS=secretpassword
   ```

2. **Individual device entries** (not recommended for production):
   ```yaml
   devices:
     - hostname: r1
       username: admin
       password: secret
   ```

## Logging

Logs are written to `logs/preflight.log` with timestamps and log levels:

```
2025-01-20 10:30:45,123 - INFO - Loaded 2 devices from inventory
2025-01-20 10:30:45,456 - INFO - Connecting to r1.example.com (192.168.1.1)...
2025-01-20 10:30:47,789 - INFO - Device r1.example.com passed all validation checks
```

## Testing

Run unit tests:

```bash
pytest tests/
```

Tests cover:
- Validation check logic
- Inventory loading
- Error handling
- Mock vs real mode differences

## Use Cases

### Before Configuration Changes

```bash
# Validate devices before running automation
python preflight.py

# Only proceed if exit code is 0
if [ $? -eq 0 ]; then
    ansible-playbook deploy-config.yml
else
    echo "Preflight checks failed - aborting deployment"
fi
```

### CI/CD Integration

```bash
# In CI pipeline
python preflight.py --output-format json > preflight-results.json

# Parse JSON in pipeline to fail build if devices don't pass
```

### Interactive Validation

```bash
# Check specific inventory with verbose logging
python preflight.py --inventory staging-inventory.yaml --log-level DEBUG
```

## Architecture

The tool follows a modular design:

1. **CLI Layer** (`preflight.py`): Argument parsing, output formatting, orchestration
2. **Inventory Module** (`core/inventory.py`): YAML loading, credential management
3. **Connection Module** (`core/connection.py`): Netmiko integration, mock mode
4. **Validator Module** (`core/validator.py`): Validation checks, result aggregation
5. **Models** (`models/device.py`): Pydantic models for type safety and validation

This separation enables:
- Easy testing of individual components
- Clear responsibilities per module
- Simple extension with new validation checks

## Extending the Tool

### Adding New Validation Checks

1. Add check function in `core/validator.py`:
   ```python
   def check_new_requirement(facts: DeviceFacts, device: DeviceInventory) -> CheckResult:
       # Your validation logic
       if requirement_met:
           return CheckResult(status="pass")
       else:
           return CheckResult(status="fail", reason="...")
   ```

2. Add to `validate_device()` function:
   ```python
   checks = {
       # ... existing checks
       "new_requirement": check_new_requirement(facts, device),
   }
   ```

### Supporting New Device Types

Add OS version defaults in `core/connection.py`:
```python
DEFAULT_OS_VERSION_MIN = {
    # ... existing
    "new_device_type": "1.0",
}
```

## Troubleshooting

**Connection failures:**
- Check credentials are set (`NET_USER`, `NET_PASS`)
- Verify device IP and port are correct
- Ensure SSH connectivity to devices

**YAML parsing errors:**
- Validate YAML syntax (use online YAML validator)
- Check `devices` key exists and contains a list

**Version comparison issues:**
- Ensure version strings follow semantic versioning
- Check `os_version_min` format matches device output

## Contributing

This is a learning/demo project. Suggestions welcome for:
- Additional validation checks
- Support for more device types
- Enhanced output formatting
- Performance improvements

## License

This is a demonstration project for learning network automation.
