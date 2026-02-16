"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator, ValidationError


class Device(BaseModel):
    """Device model for inventory validation."""

    hostname: str = Field(..., description="Device hostname")
    ip: str = Field(..., description="Management IP")
    port: int = Field(22, description="SSH port")


def validate_device_data(data: dict) -> Optional[Device]:
    """Validate device data and return a Device instance or None on error."""
    try:
        return Device.model_validate(data)
    except ValidationError:
        return None


def device_to_dict(device: Device) -> dict:
    """Return device as a dictionary (exclude defaults for compact output)."""
    return device.model_dump(exclude_defaults=True)


class DeviceStrict(BaseModel):
    """Device with normalized hostname (no leading/trailing space)."""

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")

    @field_validator("hostname", mode="before")
    @classmethod
    def normalize_hostname(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip().lower()
            if not v:
                raise ValueError("hostname cannot be empty")
            return v
        raise ValueError("hostname must be a string")


class Interface(BaseModel):
    """Interface with name and status."""

    name: str = Field(..., description="Interface name")
    status: str = Field(default="down", description="up or down")


class DeviceWithInterfaces(BaseModel):
    """Device with a list of interfaces."""

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")
    interfaces: list[Interface] = Field(default_factory=list, description="Interfaces")


class CheckResult(BaseModel):
    """Single check result."""

    status: str = Field(..., description="pass or fail")
    reason: Optional[str] = Field(None, description="Failure reason")


class DeviceValidationResult(BaseModel):
    """Per-device validation result."""

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP")
    status: str = Field(..., description="pass or fail")
    checks: dict[str, CheckResult] = Field(default_factory=dict, description="Checks")


class ValidationReport(BaseModel):
    """Report with summary and device list."""

    total: int = Field(..., ge=0)
    passed: int = Field(..., ge=0)
    failed: int = Field(..., ge=0)
    devices: list[DeviceValidationResult] = Field(default_factory=list)


if __name__ == "__main__":
    print("12b_pydantic – answer key (run exercises.py to practice)")
