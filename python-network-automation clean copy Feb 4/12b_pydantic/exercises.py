"""
Python Network Automation - Pydantic Exercises
================================================

Fill-in-the-blank exercises for Pydantic (beginner to advanced).
"""

from typing import Optional

# Use Pydantic v2
from pydantic import BaseModel, Field, field_validator, ValidationError


# ============================================================================
# EXERCISE 1 (Beginner): Define a Device model and parse a dict
# ============================================================================

"""
Tutorial: BaseModel and Field
-----------------------------

- Subclass BaseModel; add class attributes with type hints.
- Field(...) = required; Field(default=x) = optional with default.
- model_validate(dict) parses and validates; raises ValidationError if invalid.
- model_dump() returns a dict; model_dump_json() returns a JSON string.
"""


class Device(BaseModel):
    """Device model for inventory validation."""

    # TODO: Add fields: hostname (str, required), ip (str, required), port (int, optional, default 22)
    hostname: str = Field(..., description="Device hostname")
    ip: str = Field(..., description="Management IP")
    port: int = Field(22, description="SSH port")


def validate_device_data(data: dict) -> Optional[Device]:
    """
    Validate device data and return a Device instance or None on error.
    """
    # TODO: Use Device.model_validate(data) inside try/except ValidationError; return None on error
    try:
        return Device.model_validate(data)
    except ValidationError:
        return None


def device_to_dict(device: Device) -> dict:
    """Return device as a dictionary (exclude defaults for compact output)."""
    # TODO: return device.model_dump(exclude_defaults=True)
    return device.model_dump(exclude_defaults=True)


# ============================================================================
# EXERCISE 2 (Intermediate): Add a field validator
# ============================================================================

"""
Tutorial: field_validator (Pydantic v2)
----------------------------------------

- @field_validator("field_name", mode="before") runs before type coercion.
- Return the value (possibly transformed); raise ValueError for invalid.
- Use @classmethod and cls as first arg.
"""


class DeviceStrict(BaseModel):
    """Device with normalized hostname (no leading/trailing space)."""

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")

    # TODO: Add a field_validator for "hostname" that strips whitespace and lowercases.
    # If the result is empty, raise ValueError("hostname cannot be empty").
    @field_validator("hostname", mode="before")
    @classmethod
    def normalize_hostname(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip().lower()
            if not v:
                raise ValueError("hostname cannot be empty")
            return v
        raise ValueError("hostname must be a string")


# ============================================================================
# EXERCISE 3 (Intermediate): Nested model
# ============================================================================

"""
Tutorial: Nested models
-----------------------

- A field can be another BaseModel or list[BaseModel].
- Parsing a dict with nested dicts will validate the nested structure too.
"""


class Interface(BaseModel):
    """Interface with name and status."""

    name: str = Field(..., description="Interface name")
    status: str = Field(default="down", description="up or down")


class DeviceWithInterfaces(BaseModel):
    """Device with a list of interfaces."""

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")
    # TODO: Add field interfaces: list[Interface] with default_factory=list
    interfaces: list[Interface] = Field(default_factory=list, description="Interfaces")


# ============================================================================
# EXERCISE 4 (Advanced): ValidationReport-style (optional)
# ============================================================================

"""
Tutorial: Nested report structure
---------------------------------

- Build a report with summary (total, passed, failed) and list of per-device results.
- Use Field(ge=0) for non-negative integers.
- See automation-preflight models/device.py for ValidationReport pattern.
"""


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


# ============================================================================
# Run demos (uncomment to test)
# ============================================================================

if __name__ == "__main__":
    # Exercise 1
    d = validate_device_data({"hostname": "r1", "ip": "10.0.0.1"})
    print("Device:", d)
    if d:
        print("dict:", device_to_dict(d))

    # Exercise 2
    ds = DeviceStrict.model_validate({"hostname": "  R1  ", "ip": "10.0.0.1"})
    print("Normalized hostname:", repr(ds.hostname))

    # Exercise 3
    dw = DeviceWithInterfaces.model_validate(
        {"hostname": "sw1", "ip": "10.0.0.2", "interfaces": [{"name": "Gi0/1", "status": "up"}]}
    )
    print("Interfaces:", dw.interfaces)

    # Exercise 4
    report = ValidationReport(total=1, passed=1, failed=0, devices=[])
    print("Report:", report.model_dump())
