# Inventory Drift Detector

A Go CLI tool that compares two network device inventories (JSON or YAML) and reports drift - missing devices, mismatched attributes, and extra/unexpected devices. This tool models how enterprise automation teams detect drift between systems like CMDBs, discovery tools, and source-of-truth inventories.

## Features

- **Dual Format Support**: Loads both JSON and YAML inventory files
- **Flexible Comparison**: Configurable unique key field (hostname, IP, serial, etc.)
- **Comprehensive Drift Detection**: 
  - Missing devices (in expected but not in actual)
  - Extra/unexpected devices (in actual but not in expected)
  - Mismatched attributes (same device, different properties)
- **Multiple Output Formats**: Human-readable reports, JSON diff, or both
- **Mock Ticket Creation**: Optional flag to generate mock tickets for drift issues
- **Field Normalization**: Handles different field naming conventions (e.g., `ip` vs `mgmt_ip`)

## Installation

### Prerequisites

- Go 1.21 or higher

### Build

```bash
cd inventory-drift-detector
go mod download
go build -o driftdetector ./cmd/driftdetector
```

## Usage

### Basic Usage

```bash
./driftdetector --expected examples/expected.json --actual examples/actual.json
```

### All Options

```bash
./driftdetector \
  --expected <path> \     # Path to expected inventory (required)
  --actual <path> \       # Path to actual inventory (required)
  --key <field> \         # Unique key field (default: hostname)
  --output <format> \     # Output format: human, json, or both (default: human)
  --json-output <path> \  # Save JSON diff to file (optional)
  --ticket \              # Create mock ticket for drift (flag)
  --verbose               # Enable verbose logging
```

### Examples

#### Human-readable output (default)

```bash
./driftdetector --expected examples/expected.json --actual examples/actual.json
```

#### JSON output

```bash
./driftdetector --expected examples/expected.json --actual examples/actual.json --output json
```

#### Both formats with JSON saved to file

```bash
./driftdetector \
  --expected examples/expected.yaml \
  --actual examples/actual.yaml \
  --output both \
  --json-output drift-report.json
```

#### Compare using IP as key field

```bash
./driftdetector \
  --expected examples/expected.json \
  --actual examples/actual.json \
  --key ip
```

#### Create mock ticket for drift

```bash
./driftdetector \
  --expected examples/expected.json \
  --actual examples/actual.json \
  --ticket
```

## Inventory File Formats

### JSON Format

```json
{
  "devices": [
    {
      "hostname": "r1.border",
      "ip": "10.0.0.1",
      "model": "Cisco ASR1000",
      "platform": "cisco_ios",
      "status": "active",
      "serial": "FTX12345678"
    }
  ]
}
```

### YAML Format

```yaml
devices:
  - hostname: r1.border
    ip: 10.0.0.1
    model: Cisco ASR1000
    platform: cisco_ios
    status: active
    serial: FTX12345678
```

### Supported Fields

- `hostname` (string) - Device hostname
- `ip` or `mgmt_ip` (string) - Management IP address
- `model` or `device_type` (string) - Device model/type
- `platform` (string) - Network platform (e.g., cisco_ios, cisco_nxos)
- `status` (string) - Device status
- `serial` (string) - Serial number
- `extra` (map) - Additional custom fields

### Field Normalization

The tool automatically normalizes field names:
- `ip` and `mgmt_ip` are treated as equivalent
- `model` and `device_type` are treated as equivalent

## Output Examples

### Human-readable Output

```
================================================================================
INVENTORY DRIFT REPORT
================================================================================

SUMMARY
--------------------------------------------------------------------------------
Missing devices:    1
Extra devices:      1
Mismatched devices: 1
Total issues:       3

MISSING DEVICES
--------------------------------------------------------------------------------
1. Hostname: sw1.access, IP: 10.0.0.10, Model: Cisco Catalyst 9300, Platform: cisco_ios, Status: active

EXTRA/UNEXPECTED DEVICES
--------------------------------------------------------------------------------
1. Hostname: sw2.access, IP: 10.0.0.20, Model: Cisco Catalyst 9300, Platform: cisco_ios, Status: active

MISMATCHED DEVICES
--------------------------------------------------------------------------------
1. Device: r1.border
   Differences:
     - status:
       Expected: active
       Actual:   maintenance

================================================================================
```

### JSON Output

```json
{
  "missing": [
    {
      "hostname": "sw1.access",
      "ip": "10.0.0.10",
      "model": "Cisco Catalyst 9300",
      "platform": "cisco_ios",
      "status": "active",
      "serial": "CAT11111111"
    }
  ],
  "extra": [
    {
      "hostname": "sw2.access",
      "ip": "10.0.0.20",
      "model": "Cisco Catalyst 9300",
      "platform": "cisco_ios",
      "status": "active",
      "serial": "CAT22222222"
    }
  ],
  "mismatched": [
    {
      "device": {...},
      "expected": {...},
      "actual": {...},
      "differences": {
        "status": {
          "expected": "active",
          "actual": "maintenance"
        }
      }
    }
  ]
}
```

## Exit Codes

- `0` - No drift detected (inventories match)
- `1` - Drift detected or error occurred

## Project Structure

```
inventory-drift-detector/
├── cmd/
│   └── driftdetector/
│       └── main.go              # CLI entry point
├── internal/
│   ├── inventory/
│   │   └── loader.go            # Load and parse JSON/YAML inventories
│   ├── compare/
│   │   └── diff.go              # Core comparison logic
│   ├── report/
│   │   └── formatter.go         # Human-readable and JSON output formatting
│   └── ticket/
│       └── mock.go              # Mock ticket creation
├── examples/
│   ├── expected.json            # Sample expected inventory
│   ├── expected.yaml            # Sample expected inventory (YAML)
│   ├── actual.json              # Sample actual inventory
│   └── actual.yaml              # Sample actual inventory (YAML)
├── go.mod                       # Go module definition
├── go.sum                       # Dependency checksums
└── README.md                    # This file
```

## Use Cases

This tool models how enterprise automation teams handle inventory drift:

1. **CMDB vs Discovery Tools**: Compare expected inventory from CMDB against actual devices discovered by network scanning
2. **Multi-Source Validation**: Validate inventory consistency across different systems (Device42, Jira, custom CMDBs)
3. **Change Detection**: Identify configuration drift or unauthorized device changes
4. **Audit Compliance**: Generate drift reports for compliance audits

## Development

### Dependencies

- `gopkg.in/yaml.v3` - YAML parsing

### Adding New Fields

To support additional device fields, update the `Device` struct in `internal/inventory/loader.go` and add comparison logic in `internal/compare/diff.go`.

### Testing

```bash
# Run tests (when implemented)
go test ./...

# Build and test with examples
go build -o driftdetector ./cmd/driftdetector
./driftdetector --expected examples/expected.json --actual examples/actual.json
```

## License

This is a demonstration project for learning purposes.
