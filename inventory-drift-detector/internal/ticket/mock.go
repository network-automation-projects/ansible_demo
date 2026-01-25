package ticket

import (
	"fmt"
	"strings"
	"time"

	"inventory-drift-detector/internal/compare"
	"inventory-drift-detector/internal/inventory"
)

// MockTicket represents a mock ticket created for drift
type MockTicket struct {
	ID          string    `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	CreatedAt   time.Time `json:"created_at"`
	Status      string    `json:"status"`
}

// CreateTicket creates a mock ticket from drift results
func CreateTicket(result *compare.DriftResult) (*MockTicket, error) {
	if !result.HasDrift() {
		return nil, fmt.Errorf("no drift detected, cannot create ticket")
	}

	// Generate mock ticket ID (simple timestamp-based)
	ticketID := fmt.Sprintf("DRIFT-%d", time.Now().Unix())

	// Generate title
	title := generateTitle(result)

	// Generate description
	description := generateDescription(result)

	ticket := &MockTicket{
		ID:          ticketID,
		Title:       title,
		Description: description,
		CreatedAt:   time.Now(),
		Status:      "OPEN",
	}

	return ticket, nil
}

// generateTitle generates a title for the ticket
func generateTitle(result *compare.DriftResult) string {
	totalIssues := len(result.Missing) + len(result.Extra) + len(result.Mismatched)
	
	if len(result.Missing) > 0 && len(result.Extra) == 0 && len(result.Mismatched) == 0 {
		return fmt.Sprintf("Inventory Drift: %d Missing Device(s)", len(result.Missing))
	}
	
	if len(result.Extra) > 0 && len(result.Missing) == 0 && len(result.Mismatched) == 0 {
		return fmt.Sprintf("Inventory Drift: %d Extra/Unexpected Device(s)", len(result.Extra))
	}
	
	if len(result.Mismatched) > 0 && len(result.Missing) == 0 && len(result.Extra) == 0 {
		return fmt.Sprintf("Inventory Drift: %d Device(s) with Mismatched Attributes", len(result.Mismatched))
	}
	
	return fmt.Sprintf("Inventory Drift Detected: %d Total Issue(s)", totalIssues)
}

// generateDescription generates a detailed description for the ticket
func generateDescription(result *compare.DriftResult) string {
	var desc strings.Builder
	
	desc.WriteString("Inventory drift detected between expected and actual inventories.\n\n")
	
	if len(result.Missing) > 0 {
		desc.WriteString(fmt.Sprintf("MISSING DEVICES (%d):\n", len(result.Missing)))
		for i, device := range result.Missing {
			desc.WriteString(fmt.Sprintf("  %d. %s\n", i+1, formatDeviceBrief(device)))
		}
		desc.WriteString("\n")
	}
	
	if len(result.Extra) > 0 {
		desc.WriteString(fmt.Sprintf("EXTRA/UNEXPECTED DEVICES (%d):\n", len(result.Extra)))
		for i, device := range result.Extra {
			desc.WriteString(fmt.Sprintf("  %d. %s\n", i+1, formatDeviceBrief(device)))
		}
		desc.WriteString("\n")
	}
	
	if len(result.Mismatched) > 0 {
		desc.WriteString(fmt.Sprintf("MISMATCHED DEVICES (%d):\n", len(result.Mismatched)))
		for i, mismatch := range result.Mismatched {
			desc.WriteString(fmt.Sprintf("  %d. %s\n", i+1, getDeviceIdentifier(mismatch.Device)))
			for field, diff := range mismatch.Differences {
				desc.WriteString(fmt.Sprintf("     - %s: Expected=%v, Actual=%v\n", field, diff.Expected, diff.Actual))
			}
		}
	}
	
	return desc.String()
}

// formatDeviceBrief formats a device briefly for ticket descriptions
func formatDeviceBrief(device inventory.Device) string {
	var parts []string
	
	if device.Hostname != "" {
		parts = append(parts, device.Hostname)
	}
	
	ip := device.IP
	if ip == "" {
		ip = device.MgmtIP
	}
	if ip != "" {
		parts = append(parts, fmt.Sprintf("IP:%s", ip))
	}
	
	return strings.Join(parts, " ")
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