"""
Pydantic interview challenge - PRACTICE (fill in the TODOs)
Device model with validation, parse from dict, serialize to dict.

Task: Implement a small Pydantic-based device model with validation, 
parsing from a dict, and serialization back to a dict.

Device model: hostname, ip, optional port (1-65535). Hostname normalized.

"""

from typing import Optional 

from pydantic import BaseModel, Field, field_validator, ValidationError


class Device(BaseModel):
    """Device model: hostname, ip, optional port (1-65535). Hostname normalized."""

    # TODO: hostname (str, required), ip (str, required), port (int, default 22, between 1 and 65535)
    hostname: str = Field(...)  # TODO: add description
    ip: str = Field(...)  # TODO: add description
    port: int = Field(22, ge=1, le=65535)  # TODO: add description

    # TODO: Add field_validator for "hostname", mode="before":
    #       - If v is str: strip, lower; if empty raise ValueError("hostname cannot be empty")
    #       - Otherwise raise ValueError("hostname must be a string")
    @field_validator("hostname", mode="before")
    @classmethod
    def normalize_hostname(cls, v: object) -> str:
        # TODO: implement
        ...


def validate_device_data(data: dict) -> Optional[Device]:
    """Validate device data; return Device or None on ValidationError."""
    # TODO: try: return Device.model_validate(data); except ValidationError: return None
    ...


def device_to_dict(device: Device) -> dict:
    """Serialize device to dict (e.g. for JSON/YAML)."""
    # TODO: return device.model_dump()
    ...


if __name__ == "__main__":
    d = validate_device_data({"hostname": "  R1  ", "ip": "10.0.0.1"})
    assert d is not None and d.hostname == "r1" and d.port == 22
    print("Valid:", device_to_dict(d))
    bad = validate_device_data({"hostname": "r2", "ip": "10.0.0.2", "port": 99999})
    assert bad is None
    print("Invalid port -> None:", bad)
