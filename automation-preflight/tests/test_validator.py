"""Unit tests for validator and inventory loading."""

import pytest
import yaml
from pathlib import Path
import tempfile
import os

from models.device import DeviceInventory, DeviceFacts, CheckResult
from core.validator import (
    check_hostname,
    check_os_version,
    check_uptime,
    check_variables,
    validate_device,
)
from core.inventory import load_inventory, get_credentials


class TestHostnameCheck:
    """Test hostname validation check."""

    def test_hostname_present(self):
        """Test pass when hostname is present."""
        facts = DeviceFacts(hostname="router1", os_version="17.0", uptime=1000)
        result = check_hostname(facts)
        assert result.status == "pass"
        assert result.reason is None

    def test_hostname_missing(self):
        """Test fail when hostname is missing."""
        facts = DeviceFacts(hostname=None, os_version="17.0", uptime=1000)
        result = check_hostname(facts)
        assert result.status == "fail"
        assert "not detected" in result.reason.lower()

    def test_hostname_empty(self):
        """Test fail when hostname is empty string."""
        facts = DeviceFacts(hostname="", os_version="17.0", uptime=1000)
        result = check_hostname(facts)
        assert result.status == "fail"


class TestOSVersionCheck:
    """Test OS version validation check."""

    def test_os_version_pass(self):
        """Test pass when OS version meets requirement."""
        facts = DeviceFacts(hostname="r1", os_version="17.03.01a", uptime=1000)
        device = DeviceInventory(
            hostname="r1", ip="192.168.1.1", device_type="cisco_ios", os_version_min="16.0"
        )
        result = check_os_version(facts, device)
        assert result.status == "pass"

    def test_os_version_fail(self):
        """Test fail when OS version below minimum."""
        facts = DeviceFacts(hostname="r1", os_version="15.5.3", uptime=1000)
        device = DeviceInventory(
            hostname="r1", ip="192.168.1.1", device_type="cisco_ios", os_version_min="16.0"
        )
        result = check_os_version(facts, device)
        assert result.status == "fail"
        assert "not supported" in result.reason.lower()

    def test_os_version_missing(self):
        """Test fail when OS version not detected."""
        facts = DeviceFacts(hostname="r1", os_version=None, uptime=1000)
        device = DeviceInventory(
            hostname="r1", ip="192.168.1.1", device_type="cisco_ios"
        )
        result = check_os_version(facts, device)
        assert result.status == "fail"
        assert "not detected" in result.reason.lower()

    def test_os_version_no_requirement(self):
        """Test pass when no minimum version specified."""
        facts = DeviceFacts(hostname="r1", os_version="17.0", uptime=1000)
        device = DeviceInventory(
            hostname="r1", ip="192.168.1.1", device_type="cisco_ios"
        )
        result = check_os_version(facts, device, default_min=None)
        assert result.status == "pass"


class TestUptimeCheck:
    """Test uptime validation check."""

    def test_uptime_pass(self):
        """Test pass when uptime meets threshold."""
        facts = DeviceFacts(hostname="r1", os_version="17.0", uptime=86400)
        device = DeviceInventory(
            hostname="r1", ip="192.168.1.1", device_type="cisco_ios", uptime_threshold=3600
        )
        result = check_uptime(facts, device)
        assert result.status == "pass"

    def test_uptime_fail(self):
        """Test fail when uptime below threshold."""
        facts = DeviceFacts(hostname="r1", os_version="17.0", uptime=1800)
        device = DeviceInventory(
            hostname="r1", ip="192.168.1.1", device_type="cisco_ios", uptime_threshold=3600
        )
        result = check_uptime(facts, device)
        assert result.status == "fail"
        assert "below threshold" in result.reason.lower()

    def test_uptime_default_threshold(self):
        """Test pass with default threshold of 0."""
        facts = DeviceFacts(hostname="r1", os_version="17.0", uptime=0)
        device = DeviceInventory(hostname="r1", ip="192.168.1.1", device_type="cisco_ios")
        result = check_uptime(facts, device)
        assert result.status == "pass"

    def test_uptime_missing(self):
        """Test fail when uptime not detected."""
        facts = DeviceFacts(hostname="r1", os_version="17.0", uptime=None)
        device = DeviceInventory(hostname="r1", ip="192.168.1.1", device_type="cisco_ios")
        result = check_uptime(facts, device)
        assert result.status == "fail"
        assert "not detected" in result.reason.lower()


class TestVariablesCheck:
    """Test required variables validation check."""

    def test_variables_pass(self):
        """Test pass when all required variables present."""
        device = DeviceInventory(hostname="r1", ip="192.168.1.1", device_type="cisco_ios")
        result = check_variables(device)
        assert result.status == "pass"

    def test_variables_missing_hostname(self):
        """Test fail when hostname missing."""
        device_dict = {"ip": "192.168.1.1", "device_type": "cisco_ios"}
        with pytest.raises(Exception):
            DeviceInventory(**device_dict)


class TestValidateDevice:
    """Test complete device validation."""

    def test_validate_device_all_pass(self):
        """Test validation when all checks pass."""
        device = DeviceInventory(hostname="r1", ip="192.168.1.1", device_type="cisco_ios")
        facts = DeviceFacts(hostname="r1", os_version="17.03.01a", uptime=86400)
        result = validate_device(device, facts)
        assert result.status == "pass"
        assert len(result.checks) == 4
        assert all(check.status == "pass" for check in result.checks.values())

    def test_validate_device_some_fail(self):
        """Test validation when some checks fail."""
        device = DeviceInventory(
            hostname="r1", ip="192.168.1.1", device_type="cisco_ios", os_version_min="18.0"
        )
        facts = DeviceFacts(hostname="r1", os_version="17.03.01a", uptime=86400)
        result = validate_device(device, facts)
        assert result.status == "fail"
        assert result.checks["os_version"].status == "fail"
        assert result.checks["hostname"].status == "pass"


class TestInventoryLoading:
    """Test inventory YAML loading."""

    def test_load_valid_inventory(self):
        """Test loading a valid inventory file."""
        inventory_yaml = """
devices:
  - hostname: r1.example.com
    ip: 192.168.1.1
    device_type: cisco_ios
  - hostname: r2.example.com
    ip: 192.168.1.2
    device_type: cisco_ios
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(inventory_yaml)
            temp_path = f.name

        try:
            devices = load_inventory(temp_path)
            assert len(devices) == 2
            assert devices[0].hostname == "r1.example.com"
            assert devices[1].hostname == "r2.example.com"
        finally:
            os.unlink(temp_path)

    def test_load_inventory_with_env_credentials(self, monkeypatch):
        """Test inventory loading uses env vars for credentials."""
        monkeypatch.setenv("NET_USER", "testuser")
        monkeypatch.setenv("NET_PASS", "testpass")

        inventory_yaml = """
devices:
  - hostname: r1.example.com
    ip: 192.168.1.1
    device_type: cisco_ios
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(inventory_yaml)
            temp_path = f.name

        try:
            devices = load_inventory(temp_path)
            assert len(devices) == 1
            assert devices[0].username == "testuser"
            assert devices[0].password == "testpass"
        finally:
            os.unlink(temp_path)

    def test_load_inventory_file_not_found(self):
        """Test error when inventory file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_inventory("nonexistent.yaml")

    def test_load_inventory_invalid_yaml(self):
        """Test error when YAML is invalid."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_path = f.name

        try:
            with pytest.raises(Exception):
                load_inventory(temp_path)
        finally:
            os.unlink(temp_path)

    def test_load_inventory_missing_devices_key(self):
        """Test error when 'devices' key is missing."""
        inventory_yaml = "some_other_key: value"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(inventory_yaml)
            temp_path = f.name

        try:
            with pytest.raises(ValueError):
                load_inventory(temp_path)
        finally:
            os.unlink(temp_path)
