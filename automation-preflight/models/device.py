"""Pydantic models for device inventory, facts, and validation results."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class DeviceInventory(BaseModel):
    """Device inventory entry from YAML file."""

    hostname: str = Field(..., description="Device hostname")
    ip: str = Field(..., description="Device IP address")
    device_type: str = Field(..., description="Netmiko device type")
    username: Optional[str] = Field(None, description="SSH username")
    password: Optional[str] = Field(None, description="SSH password")
    port: Optional[int] = Field(22, description="SSH port")
    uptime_threshold: Optional[int] = Field(0, description="Minimum uptime in seconds")
    os_version_min: Optional[str] = Field(None, description="Minimum OS version")


class DeviceFacts(BaseModel):
    """Collected device facts from connection."""

    hostname: Optional[str] = Field(None, description="Device hostname from device")
    os_version: Optional[str] = Field(None, description="OS version string")
    uptime: Optional[int] = Field(None, description="Uptime in seconds")
    variables: Dict = Field(default_factory=dict, description="Additional variables")


class CheckResult(BaseModel):
    """Result of a single validation check."""

    status: str = Field(..., description="'pass' or 'fail'")
    reason: Optional[str] = Field(None, description="Failure reason if status is 'fail'")


class ValidationResult(BaseModel):
    """Complete validation result for a device."""

    hostname: str = Field(..., description="Device hostname")
    ip: str = Field(..., description="Device IP address")
    status: str = Field(..., description="'pass' or 'fail'")
    checks: Dict[str, CheckResult] = Field(
        default_factory=dict, description="Individual check results"
    )
    connection_error: Optional[str] = Field(
        None, description="Connection error message if connection failed"
    )


class ValidationSummary(BaseModel):
    """Summary of validation across all devices."""

    total: int = Field(..., description="Total number of devices")
    passed: int = Field(..., description="Number of devices that passed")
    failed: int = Field(..., description="Number of devices that failed")


class ValidationReport(BaseModel):
    """Complete validation report with summary and device results."""

    summary: ValidationSummary = Field(..., description="Validation summary")
    devices: List[ValidationResult] = Field(..., description="Per-device results")
