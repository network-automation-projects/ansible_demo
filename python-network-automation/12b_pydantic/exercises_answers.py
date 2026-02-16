"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator, ValidationError

try:
    from pydantic_settings import BaseSettings
except ImportError:
    BaseSettings = None  # type: ignore





class Device(BaseModel):
    """Device model for inventory validation."""

    hostname: str = Field(..., description="Device hostname")
    ip: str = Field(..., description="Management IP")
    port: int = Field(22, description="SSH port")


def validate_device_data(data: dict) -> Optional[Device]:
    """Validate device data and return a Device instance or None on error."""
    try:
        return Device.model_validate(data)          # built in function model_validate will kick back error if missing a required field or if a required field is malformed.
    except ValidationError:
        return None


def device_to_dict(device: Device) -> dict:
    """Return device as a dictionary (exclude defaults for compact output)."""
    return device.model_dump(exclude_defaults=True)


class DeviceStrict(BaseModel):
    """Device with normalized hostname (no leading/trailing space)."""

    model_config = ConfigDict(extra="forbid")           #rejects fields not in class definition

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")

    @field_validator("hostname", mode="before")
    @classmethod
    def normalize_hostname(cls, v: Any) -> str:         #cls is passed automatically (becomes DeviceStrict class instance)
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


# Exercise 5
def device_from_json(json_str: str) -> Optional[Device]:
    try:
        return Device.model_validate_json(json_str)
    except ValidationError:
        return None


def device_to_json(device: Device, indent: int = 0) -> str:
    return device.model_dump_json(exclude_none=True, indent=indent if indent else None)


# Exercise 6
class DeviceWithConstraints(BaseModel):
    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")
    port: int = Field(22, ge=1, le=65535, description="SSH port")
    timeout_seconds: int = Field(30, gt=0, le=300, description="Connection timeout")


# Exercise 7
def get_validation_errors(data: dict) -> list[dict[str, Any]]:
    try:
        Device.model_validate(data)
        return []
    except ValidationError as e:
        return [{"loc": err["loc"], "msg": err["msg"]} for err in e.errors()]


# Exercise 8
class ConnectionOptions(BaseModel):
    port: Optional[int] = Field(None, ge=1, le=65535, description="Single port")
    port_range: Optional[tuple[int, int]] = Field(None, description="(min, max) ports")

    @model_validator(mode="after")
    def require_port_or_range(self) -> "ConnectionOptions":
        if self.port is None and self.port_range is None:
            raise ValueError("either port or port_range must be set")
        return self


# Exercise 9
class DeviceStrictKeys(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")


# Exercise 10
class DeviceWithTags(BaseModel):
    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")
    tags: list[str] = Field(default_factory=list, description="Tags")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Extra key-value data")


# Exercise 11
if BaseSettings is not None:

    class AppConfig(BaseSettings):
        app_name: str = Field(default="network-tool", description="Application name")
        timeout_seconds: int = Field(default=30, ge=1, le=300, description="Default timeout")
        model_config = ConfigDict(env_prefix="APP_", extra="ignore")


# Exercise 12
class VLANConfig(BaseModel):
    name: str = Field(..., description="Interface name")
    vlan_id: int = Field(..., ge=1, le=4094, description="VLAN ID 1-4094")


# Exercise 13
def device_required_fields() -> list[str]:
    schema = Device.model_json_schema()
    return list(schema.get("required", []))


if __name__ == "__main__":
    print("12b_pydantic – answer key (run exercises.py to practice)")



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



##unrelated 'before' example:

#     from pydantic import BaseModel, field_validator

# class Device(BaseModel):
#     hostname: str
#     os: str

#     @field_validator("hostname")
#     @classmethod
#     def hostname_no_spaces(cls, v: str) -> str:
#         if " " in v:
#             raise ValueError("hostname must not contain spaces")
#         return v

#unrelated 'after' example:
# from pydantic import BaseModel, model_validator

# class ChangeRequest(BaseModel):
#     dry_run: bool = False
#     change_id: str | None = None

#     @model_validator(mode="after")
#     def require_change_id_when_not_dry_run(self):
#         if not self.dry_run and not self.change_id:
#             raise ValueError("change_id is required when dry_run is false")
#         return self

#unrelated example 3:
# from ipaddress import ip_address
# from pydantic import BaseModel, Field, field_validator

# ALLOWED_OS = {"iosxe", "nxos", "junos"}

# class PreflightRequest(BaseModel):
#     hostname: str = Field(min_length=1)
#     mgmt_ip: str
#     os: str
#     min_uptime_sec: int = Field(ge=0, default=300)
#     dry_run: bool = False

#     @field_validator("mgmt_ip")
#     @classmethod
#     def valid_ip(cls, v: str) -> str:
#         # raises ValueError if invalid
#         ip_address(v)
#         return v

#     @field_validator("os")
#     @classmethod
#     def allowed_os(cls, v: str) -> str:
#         v2 = v.lower().strip()
#         if v2 not in ALLOWED_OS:
#             raise ValueError(f"os must be one of {sorted(ALLOWED_OS)}")
#         return v2

# from flask import Flask, request, jsonify
# from pydantic import ValidationError

# app = Flask(__name__)

# @app.post("/preflight")
# def preflight():
#     try:
#         payload = request.get_json(force=True)  # keep demo simple
#         req = PreflightRequest.model_validate(payload)
#     except ValidationError as e:
#         return jsonify({"error": "validation_failed", "details": e.errors()}), 400

#     # Core logic would go here
#     return jsonify({"ok": True, "normalized": req.model_dump()}), 200

# import json
# import sys
# from pydantic import ValidationError

# def main():
#     raw = json.loads(sys.stdin.read())  # pretend it came from a file or pipeline
#     try:
#         req = PreflightRequest.model_validate(raw)
#     except ValidationError as e:
#         print(json.dumps({"ok": False, "errors": e.errors()}, indent=2))
#         raise SystemExit(2)

#     print(json.dumps({"ok": True, "request": req.model_dump()}, indent=2))

# if __name__ == "__main__":
#     main()

