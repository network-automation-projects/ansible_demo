package health

import (
	"fmt"
	"net/http"
	"time"
)

// HealthChecker performs health checks
type HealthChecker struct {
	Endpoint      string
	Timeout       time.Duration
	Interval      time.Duration
	Retries       int
	ExpectedStatus int
}

// NewHealthChecker creates a new health checker
func NewHealthChecker(endpoint string, timeout, interval time.Duration, retries, expectedStatus int) *HealthChecker {
	return &HealthChecker{
		Endpoint:       endpoint,
		Timeout:        timeout,
		Interval:       interval,
		Retries:        retries,
		ExpectedStatus: expectedStatus,
	}
}

// Check performs a health check
func (h *HealthChecker) Check() bool {
	client := &http.Client{
		Timeout: h.Timeout,
	}

	for attempt := 1; attempt <= h.Retries; attempt++ {
		resp, err := client.Get(h.Endpoint)
		if err != nil {
			if attempt < h.Retries {
				time.Sleep(h.Interval)
			}
			continue
		}
		resp.Body.Close()

		if resp.StatusCode == h.ExpectedStatus {
			return true
		}

		if attempt < h.Retries {
			time.Sleep(h.Interval)
		}
	}

	return false
}

// FromConfig creates a health checker from configuration map
func FromConfig(config map[string]interface{}) (*HealthChecker, error) {
	endpoint, ok := config["endpoint"].(string)
	if !ok {
		return nil, fmt.Errorf("endpoint not found in health check config")
	}

	timeout := 30 * time.Second
	if t, ok := config["timeout"].(int); ok {
		timeout = time.Duration(t) * time.Second
	}

	interval := 5 * time.Second
	if i, ok := config["interval"].(int); ok {
		interval = time.Duration(i) * time.Second
	}

	retries := 3
	if r, ok := config["retries"].(int); ok {
		retries = r
	}

	expectedStatus := 200
	if s, ok := config["expected_status"].(int); ok {
		expectedStatus = s
	}

	return NewHealthChecker(endpoint, timeout, interval, retries, expectedStatus), nil
}
