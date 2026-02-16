"""
Pydantic interview challenge - FULL ANSWER
Device model with validation, parse from dict, serialize to dict.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator, ValidationError


class Device(BaseModel):
    """Device model: hostname, ip, optional port (1-65535). Hostname normalized."""

    hostname: str = Field(..., description="Device hostname")
    ip: str = Field(..., description="Management IP")
    port: int = Field(22, ge=1, le=65535, description="SSH port")

    @field_validator("hostname", mode="before")
    @classmethod
    def normalize_hostname(cls, v: object) -> str:
        if isinstance(v, str):
            normalized = v.strip().lower()
            if not normalized:
                raise ValueError("hostname cannot be empty")
            return normalized
        raise ValueError("hostname must be a string")


def validate_device_data(data: dict) -> Optional[Device]:
    """Validate device data; return Device or None on ValidationError."""
    try:
        return Device.model_validate(data)
    except ValidationError:
        return None


def device_to_dict(device: Device) -> dict:
    """Serialize device to dict (e.g. for JSON/YAML)."""
    return device.model_dump()


# --- Example usage (optional) ---
if __name__ == "__main__":
    # Valid
    d = validate_device_data({"hostname": "  R1  ", "ip": "10.0.0.1"})
    assert d is not None
    assert d.hostname == "r1"
    assert d.port == 22
    print("Valid:", device_to_dict(d))

    # Invalid port
    bad = validate_device_data({"hostname": "r2", "ip": "10.0.0.2", "port": 99999})
    assert bad is None
    print("Invalid port -> None:", bad)

    # Missing required
    missing = validate_device_data({"hostname": "r3"})
    assert missing is None
    print("Missing ip -> None:", missing)
