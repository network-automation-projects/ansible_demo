package report

import (
	"encoding/json"
	"fmt"
	"strings"

	"inventory-drift-detector/internal/compare"
	"inventory-drift-detector/internal/inventory"
)

// FormatHuman formats drift results as a human-readable report
func FormatHuman(result *compare.DriftResult) string {
	var sb strings.Builder

	// Summary statistics
	sb.WriteString("=" + strings.Repeat("=", 79) + "\n")
	sb.WriteString("INVENTORY DRIFT REPORT\n")
	sb.WriteString("=" + strings.Repeat("=", 79) + "\n\n")

	totalIssues := len(result.Missing) + len(result.Extra) + len(result.Mismatched)
	if totalIssues == 0 {
		sb.WriteString("✓ No drift detected. Inventories match perfectly.\n\n")
		return sb.String()
	}

	sb.WriteString("SUMMARY\n")
	sb.WriteString("-" + strings.Repeat("-", 79) + "\n")
	sb.WriteString(fmt.Sprintf("Missing devices:    %d\n", len(result.Missing)))
	sb.WriteString(fmt.Sprintf("Extra devices:      %d\n", len(result.Extra)))
	sb.WriteString(fmt.Sprintf("Mismatched devices: %d\n", len(result.Mismatched)))
	sb.WriteString(fmt.Sprintf("Total issues:       %d\n\n", totalIssues))

	// Missing devices
	if len(result.Missing) > 0 {
		sb.WriteString("MISSING DEVICES\n")
		sb.WriteString("-" + strings.Repeat("-", 79) + "\n")
		for i, device := range result.Missing {
			sb.WriteString(fmt.Sprintf("%d. %s", i+1, formatDevice(device)))
			if i < len(result.Missing)-1 {
				sb.WriteString("\n")
			}
		}
		sb.WriteString("\n\n")
	}

	// Extra devices
	if len(result.Extra) > 0 {
		sb.WriteString("EXTRA/UNEXPECTED DEVICES\n")
		sb.WriteString("-" + strings.Repeat("-", 79) + "\n")
		for i, device := range result.Extra {
			sb.WriteString(fmt.Sprintf("%d. %s", i+1, formatDevice(device)))
			if i < len(result.Extra)-1 {
				sb.WriteString("\n")
			}
		}
		sb.WriteString("\n\n")
	}

	// Mismatched devices
	if len(result.Mismatched) > 0 {
		sb.WriteString("MISMATCHED DEVICES\n")
		sb.WriteString("-" + strings.Repeat("-", 79) + "\n")
		for i, mismatch := range result.Mismatched {
			sb.WriteString(fmt.Sprintf("%d. Device: %s\n", i+1, getDeviceIdentifier(mismatch.Device)))
			sb.WriteString("   Differences:\n")
			for field, diff := range mismatch.Differences {
				sb.WriteString(fmt.Sprintf("     - %s:\n", field))
				sb.WriteString(fmt.Sprintf("       Expected: %v\n", formatValue(diff.Expected)))
				sb.WriteString(fmt.Sprintf("       Actual:   %v\n", formatValue(diff.Actual)))
			}
			if i < len(result.Mismatched)-1 {
				sb.WriteString("\n")
			}
		}
		sb.WriteString("\n")
	}

	sb.WriteString("=" + strings.Repeat("=", 79) + "\n")
	return sb.String()
}

// formatDevice formats a device for display
func formatDevice(device inventory.Device) string {
	var parts []string
	
	if device.Hostname != "" {
		parts = append(parts, fmt.Sprintf("Hostname: %s", device.Hostname))
	}
	
	ip := device.IP
	if ip == "" {
		ip = device.MgmtIP
	}
	if ip != "" {
		parts = append(parts, fmt.Sprintf("IP: %s", ip))
	}
	
	model := device.Model
	if model == "" {
		model = device.DeviceType
	}
	if model != "" {
		parts = append(parts, fmt.Sprintf("Model: %s", model))
	}
	
	if device.Platform != "" {
		parts = append(parts, fmt.Sprintf("Platform: %s", device.Platform))
	}
	
	if device.Status != "" {
		parts = append(parts, fmt.Sprintf("Status: %s", device.Status))
	}
	
	return strings.Join(parts, ", ")
}

// getDeviceIdentifier returns a unique identifier for a device
func getDeviceIdentifier(device inventory.Device) string {
	if device.Hostname != "" {
		return device.Hostname
	}
	if device.MgmtIP != "" {
		return device.MgmtIP
	}
	if device.IP != "" {
		return device.IP
	}
	if device.Serial != "" {
		return device.Serial
	}
	return "unknown"
}

// formatValue formats a value for display
func formatValue(v interface{}) string {
	if v == nil {
		return "<nil>"
	}
	return fmt.Sprintf("%v", v)
}

// FormatJSON formats drift results as JSON
func FormatJSON(result *compare.DriftResult) ([]byte, error) {
	data, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		return nil, fmt.Errorf("failed to marshal drift result to JSON: %w", err)
	}
	return data, nil
}
