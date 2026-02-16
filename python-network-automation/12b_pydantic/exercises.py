"""
Python Network Automation - Pydantic Exercises
================================================

Fill-in-the-blank exercises for Pydantic (beginner to advanced).
"""

from typing import Any, Optional

# Use Pydantic v2
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator, ValidationError


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
# EXERCISE 5 (Beginner): JSON round-trip
# ============================================================================

"""
Tutorial: model_validate_json and model_dump_json
------------------------------------------------

- model_validate_json(json_string) parses a JSON string and validates into a model.
- model_dump_json() returns a JSON string; use exclude_none=True or indent=2 for readability.
"""


def device_from_json(json_str: str) -> Optional[Device]:
    """Parse JSON string into a Device; return None on validation error."""
    # TODO: Use Device.model_validate_json(json_str) in try/except ValidationError
    try:
        return Device.model_validate_json(json_str)
    except ValidationError:
        return None


def device_to_json(device: Device, indent: int = 0) -> str:
    """Serialize Device to JSON string. If indent > 0, pretty-print."""
    # TODO: return device.model_dump_json(exclude_none=True, indent=indent or None)
    return device.model_dump_json(exclude_none=True, indent=indent if indent else None)


# ============================================================================
# EXERCISE 6 (Intermediate): Field constraints
# ============================================================================

"""
Tutorial: Field constraints
---------------------------

- Field(..., ge=1, le=65535) enforces range (>=1 and <=65535).
- Field(default=30, gt=0, le=300) for timeouts keeps values in a valid range.
"""


class DeviceWithConstraints(BaseModel):
    """Device with constrained port and timeout."""

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")
    # TODO: port int, default 22, ge=1, le=65535
    port: int = Field(22, ge=1, le=65535, description="SSH port")
    # TODO: timeout_seconds int, default 30, gt=0, le=300
    timeout_seconds: int = Field(30, gt=0, le=300, description="Connection timeout")


# ============================================================================
# EXERCISE 7 (Intermediate): Inspect ValidationError
# ============================================================================

"""
Tutorial: ValidationError.errors()
----------------------------------

- Catch ValidationError; call e.errors() to get a list of dicts.
- Each dict has 'loc' (field path), 'msg', 'type'; useful for reporting.
"""


def get_validation_errors(data: dict) -> list[dict[str, Any]]:
    """
    Try to validate data as Device. On ValidationError, return a list of
    error dicts with keys 'loc' and 'msg' (from e.errors()).
    On success, return empty list.
    """
    # TODO: try Device.model_validate(data); return [] on success.
    # TODO: except ValidationError as e: return [{"loc": err["loc"], "msg": err["msg"]} for err in e.errors()]
    try:
        Device.model_validate(data)
        return []
    except ValidationError as e:
        return [{"loc": err["loc"], "msg": err["msg"]} for err in e.errors()]


# ============================================================================
# EXERCISE 8 (Intermediate): model_validator (cross-field)
# ============================================================================

"""
Tutorial: model_validator (Pydantic v2)
--------------------------------------

- @model_validator(mode="after") runs after all fields are set; self is the model.
- Use for cross-field checks (e.g. "at least one of A or B", "start < end").
- Return self.
"""


class ConnectionOptions(BaseModel):
    """Either port or port_range must be provided."""

    port: Optional[int] = Field(None, ge=1, le=65535, description="Single port")
    port_range: Optional[tuple[int, int]] = Field(None, description="(min, max) ports")

    # TODO: Add @model_validator(mode="after") that raises ValueError if both port and port_range are None
    @model_validator(mode="after")
    def require_port_or_range(self) -> "ConnectionOptions":
        if self.port is None and self.port_range is None:
            raise ValueError("either port or port_range must be set")
        return self


# ============================================================================
# EXERCISE 9 (Intermediate): ConfigDict extra='forbid'
# ============================================================================

"""
Tutorial: ConfigDict
--------------------

- model_config = ConfigDict(extra="forbid") rejects unknown keys in the input.
- Helps catch typos (e.g. "hostnmae" instead of "hostname").
"""


class DeviceStrictKeys(BaseModel):
    """Device that forbids extra keys in input."""

    # TODO: Set model_config = ConfigDict(extra="forbid")
    model_config = ConfigDict(extra="forbid")

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")


# ============================================================================
# EXERCISE 10 (Intermediate): Optional and default_factory
# ============================================================================

"""
Tutorial: default_factory for mutable defaults
---------------------------------------------

- For list or dict fields, use Field(default_factory=list) or default_factory=dict.
- Never use field: list = [] (mutable default is shared across instances).
"""


class DeviceWithTags(BaseModel):
    """Device with optional tags and metadata (mutable defaults)."""

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")
    # TODO: tags: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list, description="Tags")
    # TODO: metadata: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict, description="Extra key-value data")


# ============================================================================
# EXERCISE 11 (Advanced): BaseSettings (optional)
# ============================================================================

"""
Tutorial: BaseSettings
---------------------

- From pydantic_settings: BaseSettings loads from environment variables.
- Use model_config = {"env_prefix": "APP_"} so APP_LOG_LEVEL maps to log_level.
- Optional: only run this exercise if pydantic_settings is installed.
"""

try:
    from pydantic_settings import BaseSettings
except ImportError:
    BaseSettings = None  # type: ignore

if BaseSettings is not None:

    class AppConfig(BaseSettings):
        """Load app name and timeout from environment (e.g. APP_APP_NAME, APP_TIMEOUT)."""

        # TODO: app_name: str = Field(default="network-tool", ...)
        app_name: str = Field(default="network-tool", description="Application name")
        # TODO: timeout_seconds: int = Field(default=30, ge=1, le=300, ...)
        timeout_seconds: int = Field(default=30, ge=1, le=300, description="Default timeout")

        # TODO: model_config = {"env_prefix": "APP_", "extra": "ignore"}
        model_config = ConfigDict(env_prefix="APP_", extra="ignore")


# ============================================================================
# EXERCISE 12 (Intermediate): Constrained type / field validator
# ============================================================================

"""
Tutorial: Custom validation for domain values
---------------------------------------------

- Use field_validator to enforce VLAN ID range (1-4094) or simple IP format.
- Return the value (or transformed value); raise ValueError if invalid.
"""


class VLANConfig(BaseModel):
    """Interface VLAN config with validated vlan_id."""

    name: str = Field(..., description="Interface name")
    # TODO: vlan_id: int = Field(..., ge=1, le=4094)
    vlan_id: int = Field(..., ge=1, le=4094, description="VLAN ID 1-4094")


# Optional: add a field_validator that normalizes vlan_id (e.g. strip whitespace from string input)
# Here we use Field(ge=1, le=4094) for int; for string input use mode="before" and convert.


# ============================================================================
# EXERCISE 13 (Beginner): JSON schema
# ============================================================================

"""
Tutorial: model_json_schema()
-----------------------------

- model_json_schema() returns a dict describing the model (OpenAPI/JSON Schema).
- Use for API docs or to inspect required fields and property types.
"""


def device_required_fields() -> list[str]:
    """Return the list of required field names for the Device model (from JSON schema)."""
    # TODO: schema = Device.model_json_schema(); return schema.get("required", [])
    schema = Device.model_json_schema()
    return list(schema.get("required", []))


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

    # Exercise 5
    json_str = '{"hostname": "r2", "ip": "10.0.0.2"}'
    d5 = device_from_json(json_str)
    print("From JSON:", d5)
    if d5:
        print("To JSON:", device_to_json(d5, indent=2))

    # Exercise 6
    dc = DeviceWithConstraints.model_validate({"hostname": "r1", "ip": "10.0.0.1", "port": 22})
    print("Constrained port:", dc.port, "timeout:", dc.timeout_seconds)

    # Exercise 7
    errs = get_validation_errors({"hostname": "r1"})  # missing ip
    print("Validation errors:", errs)

    # Exercise 8
    opt = ConnectionOptions.model_validate({"port": 443})
    print("ConnectionOptions:", opt)
    # ConnectionOptions.model_validate({})  # would raise

    # Exercise 9
    DeviceStrictKeys.model_validate({"hostname": "r1", "ip": "10.0.0.1"})
    # DeviceStrictKeys.model_validate({"hostname": "r1", "ip": "10.0.0.1", "typo": 1})  # would raise

    # Exercise 10
    dt = DeviceWithTags.model_validate({"hostname": "r1", "ip": "10.0.0.1"})
    print("Tags:", dt.tags, "metadata:", dt.metadata)

    # Exercise 11 (if pydantic_settings installed)
    if BaseSettings is not None:
        cfg = AppConfig()
        print("AppConfig app_name:", cfg.app_name)

    # Exercise 12
    vlan = VLANConfig.model_validate({"name": "Gi0/1", "vlan_id": 100})
    print("VLANConfig:", vlan)

    # Exercise 13
    print("Device required fields:", device_required_fields())
