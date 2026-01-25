package compare

import (
	"fmt"

	"inventory-drift-detector/internal/inventory"
)

// Difference represents a single field difference between expected and actual
type Difference struct {
	Expected interface{} `json:"expected"`
	Actual   interface{} `json:"actual"`
}

// Mismatch tracks attribute differences for a device
type Mismatch struct {
	Device      inventory.Device          `json:"device"`
	Expected    inventory.Device          `json:"expected"`
	Actual      inventory.Device          `json:"actual"`
	Differences map[string]Difference     `json:"differences"`
}

// DriftResult contains the comparison results
type DriftResult struct {
	Missing    []inventory.Device `json:"missing"`
	Extra      []inventory.Device `json:"extra"`
	Mismatched []Mismatch         `json:"mismatched"`
}

// Compare compares two inventories and returns drift results
func Compare(expected, actual *inventory.Inventory, keyField string) (*DriftResult, error) {
	if keyField == "" {
		keyField = "hostname"
	}

	result := &DriftResult{
		Missing:    []inventory.Device{},
		Extra:      []inventory.Device{},
		Mismatched: []Mismatch{},
	}

	// Create maps keyed by unique identifier for O(1) lookup
	expectedMap := make(map[string]inventory.Device)
	actualMap := make(map[string]inventory.Device)

	// Build expected map
	for _, device := range expected.Devices {
		key := device.GetKey(keyField)
		if key == "" {
			return nil, fmt.Errorf("device missing required key field '%s': %+v", keyField, device)
		}
		if _, exists := expectedMap[key]; exists {
			return nil, fmt.Errorf("duplicate key '%s' found in expected inventory", key)
		}
		expectedMap[key] = device
	}

	// Build actual map and check for extra devices
	for _, device := range actual.Devices {
		key := device.GetKey(keyField)
		if key == "" {
			return nil, fmt.Errorf("device missing required key field '%s': %+v", keyField, device)
		}
		if _, exists := actualMap[key]; exists {
			return nil, fmt.Errorf("duplicate key '%s' found in actual inventory", key)
		}
		actualMap[key] = device

		// Check if device exists in expected
		if _, found := expectedMap[key]; !found {
			result.Extra = append(result.Extra, device)
		}
	}

	// Check for missing devices and mismatches
	for key, expectedDevice := range expectedMap {
		actualDevice, found := actualMap[key]
		if !found {
			result.Missing = append(result.Missing, expectedDevice)
		} else {
			// Compare attributes
			differences := compareDevices(expectedDevice, actualDevice)
			if len(differences) > 0 {
				result.Mismatched = append(result.Mismatched, Mismatch{
					Device:      expectedDevice,
					Expected:    expectedDevice,
					Actual:      actualDevice,
					Differences: differences,
				})
			}
		}
	}

	return result, nil
}

// compareDevices compares two devices and returns a map of field differences
func compareDevices(expected, actual inventory.Device) map[string]Difference {
	differences := make(map[string]Difference)

	// Compare hostname
	if expected.Hostname != actual.Hostname {
		differences["hostname"] = Difference{
			Expected: expected.Hostname,
			Actual:   actual.Hostname,
		}
	}

	// Compare IP (check both IP and MgmtIP)
	expectedIP := expected.IP
	if expectedIP == "" {
		expectedIP = expected.MgmtIP
	}
	actualIP := actual.IP
	if actualIP == "" {
		actualIP = actual.MgmtIP
	}
	if expectedIP != actualIP {
		differences["ip"] = Difference{
			Expected: expectedIP,
			Actual:   actualIP,
		}
	}

	// Compare model/device_type
	expectedModel := expected.Model
	if expectedModel == "" {
		expectedModel = expected.DeviceType
	}
	actualModel := actual.Model
	if actualModel == "" {
		actualModel = actual.DeviceType
	}
	if expectedModel != actualModel {
		differences["model"] = Difference{
			Expected: expectedModel,
			Actual:   actualModel,
		}
	}

	// Compare platform
	if expected.Platform != actual.Platform {
		differences["platform"] = Difference{
			Expected: expected.Platform,
			Actual:   actual.Platform,
		}
	}

	// Compare status
	if expected.Status != actual.Status {
		differences["status"] = Difference{
			Expected: expected.Status,
			Actual:   actual.Status,
		}
	}

	// Compare serial
	if expected.Serial != actual.Serial {
		differences["serial"] = Difference{
			Expected: expected.Serial,
			Actual:   actual.Serial,
		}
	}

	// Compare extra fields (simple comparison for common types)
	compareExtraFields(expected.Extra, actual.Extra, differences)

	return differences
}

// compareExtraFields compares extra map fields
func compareExtraFields(expected, actual map[string]interface{}, differences map[string]Difference) {
	// Check all expected extra fields
	if expected != nil {
		for key, expectedVal := range expected {
			actualVal, exists := actual[key]
			if !exists {
				differences["extra."+key] = Difference{
					Expected: expectedVal,
					Actual:   nil,
				}
			} else if expectedVal != actualVal {
				differences["extra."+key] = Difference{
					Expected: expectedVal,
					Actual:   actualVal,
				}
			}
		}
	}

	// Check for extra fields in actual that don't exist in expected
	if actual != nil {
		for key, actualVal := range actual {
			if expected == nil {
				differences["extra."+key] = Difference{
					Expected: nil,
					Actual:   actualVal,
				}
			} else if _, exists := expected[key]; !exists {
				differences["extra."+key] = Difference{
					Expected: nil,
					Actual:   actualVal,
				}
			}
		}
	}
}

// HasDrift returns true if there is any drift detected
func (dr *DriftResult) HasDrift() bool {
	return len(dr.Missing) > 0 || len(dr.Extra) > 0 || len(dr.Mismatched) > 0
}
