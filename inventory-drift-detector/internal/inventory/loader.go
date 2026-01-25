package inventory

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v3"
)

// Device represents a network device in the inventory
type Device struct {
	Hostname  string                 `json:"hostname,omitempty" yaml:"hostname,omitempty"`
	IP        string                 `json:"ip,omitempty" yaml:"ip,omitempty"`
	MgmtIP    string                 `json:"mgmt_ip,omitempty" yaml:"mgmt_ip,omitempty"`
	Model     string                 `json:"model,omitempty" yaml:"model,omitempty"`
	DeviceType string                `json:"device_type,omitempty" yaml:"device_type,omitempty"`
	Platform  string                 `json:"platform,omitempty" yaml:"platform,omitempty"`
	Status    string                 `json:"status,omitempty" yaml:"status,omitempty"`
	Serial    string                 `json:"serial,omitempty" yaml:"serial,omitempty"`
	// Additional fields for extensibility
	Extra     map[string]interface{} `json:"extra,omitempty" yaml:"extra,omitempty"`
}

// Inventory represents a collection of devices
type Inventory struct {
	Devices []Device `json:"devices,omitempty" yaml:"devices,omitempty"`
}

// normalizeDevice normalizes field names across different inventory formats
func normalizeDevice(d Device) Device {
	normalized := d
	
	// Normalize IP fields - prefer mgmt_ip, fallback to ip
	if normalized.MgmtIP == "" && normalized.IP != "" {
		normalized.MgmtIP = normalized.IP
	}
	if normalized.IP == "" && normalized.MgmtIP != "" {
		normalized.IP = normalized.MgmtIP
	}
	
	// Normalize device type - prefer device_type, fallback to model
	if normalized.DeviceType == "" && normalized.Model != "" {
		normalized.DeviceType = normalized.Model
	}
	if normalized.Model == "" && normalized.DeviceType != "" {
		normalized.Model = normalized.DeviceType
	}
	
	return normalized
}

// GetKey returns the value of the specified key field for a device
func (d *Device) GetKey(keyField string) string {
	keyField = strings.ToLower(keyField)
	switch keyField {
	case "hostname":
		return d.Hostname
	case "ip", "mgmt_ip", "mgmtip":
		if d.MgmtIP != "" {
			return d.MgmtIP
		}
		return d.IP
	case "serial":
		return d.Serial
	default:
		// Try to get from Extra map
		if d.Extra != nil {
			if val, ok := d.Extra[keyField]; ok {
				if str, ok := val.(string); ok {
					return str
				}
			}
		}
		return ""
	}
}

// LoadInventory loads an inventory from a JSON or YAML file
// Auto-detects format based on file extension
func LoadInventory(path string) (*Inventory, error) {
	ext := strings.ToLower(filepath.Ext(path))
	
	switch ext {
	case ".json":
		return loadJSON(path)
	case ".yaml", ".yml":
		return loadYAML(path)
	default:
		// Try JSON first, then YAML
		if inv, err := loadJSON(path); err == nil {
			return inv, nil
		}
		return loadYAML(path)
	}
}

// loadJSON loads an inventory from a JSON file
func loadJSON(path string) (*Inventory, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read JSON file %s: %w", path, err)
	}
	
	var inventory Inventory
	
	// Try parsing as direct array of devices
	var devices []Device
	if err := json.Unmarshal(data, &devices); err == nil {
		inventory.Devices = devices
	} else {
		// Try parsing as Inventory struct
		if err := json.Unmarshal(data, &inventory); err != nil {
			return nil, fmt.Errorf("failed to parse JSON file %s: %w", path, err)
		}
	}
	
	// Normalize all devices
	for i := range inventory.Devices {
		inventory.Devices[i] = normalizeDevice(inventory.Devices[i])
	}
	
	return &inventory, nil
}

// loadYAML loads an inventory from a YAML file
func loadYAML(path string) (*Inventory, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read YAML file %s: %w", path, err)
	}
	
	var inventory Inventory
	
	// Try parsing as direct array of devices
	var devices []Device
	if err := yaml.Unmarshal(data, &devices); err == nil {
		inventory.Devices = devices
	} else {
		// Try parsing as Inventory struct
		if err := yaml.Unmarshal(data, &inventory); err != nil {
			return nil, fmt.Errorf("failed to parse YAML file %s: %w", path, err)
		}
	}
	
	// Normalize all devices
	for i := range inventory.Devices {
		inventory.Devices[i] = normalizeDevice(inventory.Devices[i])
	}
	
	return &inventory, nil
}
