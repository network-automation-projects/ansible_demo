"""
Python Network Automation - Pydantic Examples
===============================================

Complete working examples: BaseModel, Field, validators, nested models,
and BaseSettings (beginner to advanced).
"""

from typing import Any, Dict, List, Optional

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Pydantic v2
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError

# Optional: BaseSettings for advanced example (requires pydantic-settings or Pydantic 2+)
try:
    from pydantic_settings import BaseSettings
    HAS_SETTINGS = True
except ImportError:
    HAS_SETTINGS = False
    BaseSettings = None  # type: ignore


# ============================================================================
# Beginner: Device and Interface models, parse and serialize
# ============================================================================


class Interface(BaseModel):
    """Simple interface model (beginner)."""

    name: str = Field(..., description="Interface name")
    status: str = Field(default="down", description="up or down")


class Device(BaseModel):
    """Device model with required and optional fields (beginner)."""

    hostname: str = Field(..., description="Device hostname")
    ip: str = Field(..., description="Management IP")
    vendor: Optional[str] = Field(None, description="Vendor name")
    interfaces: List[Interface] = Field(default_factory=list, description="Interfaces")

    def model_post_init(self, __context: Any) -> None:
        """Optional: run after validation."""
        pass


# ============================================================================
# Intermediate: Nested inventory, field_validator, model_validator
# ============================================================================


class DeviceFacts(BaseModel):
    """Nested facts (intermediate)."""

    os_version: Optional[str] = Field(None, description="OS version")
    uptime_seconds: Optional[int] = Field(None, ge=0, description="Uptime in seconds")


class DeviceWithFacts(BaseModel):
    """Device with nested facts and validators (intermediate)."""

    hostname: str = Field(..., description="Hostname")
    ip: str = Field(..., description="IP address")
    facts: Optional[DeviceFacts] = Field(None, description="Gathered facts")

    @field_validator("hostname", mode="before")
    @classmethod
    def normalize_hostname(cls, v: Any) -> str:
        """Strip whitespace and lowercase hostname."""
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("ip", mode="before")
    @classmethod
    def ip_must_be_string(cls, v: Any) -> str:
        """Ensure IP is a non-empty string (simple check)."""
        if isinstance(v, str) and v.strip():
            return v.strip()
        raise ValueError("ip must be a non-empty string")

    @model_validator(mode="after")
    def hostname_not_empty(self) -> "DeviceWithFacts":
        """Model-level check."""
        if not self.hostname:
            raise ValueError("hostname cannot be empty after normalization")
        return self


# ============================================================================
# Advanced: ValidationReport-style (matching automation-preflight pattern)
# ============================================================================


class CheckResult(BaseModel):
    """Result of a single check (advanced)."""

    status: str = Field(..., description="pass or fail")
    reason: Optional[str] = Field(None, description="Failure reason")


class ValidationResult(BaseModel):
    """Per-device validation result (advanced)."""

    hostname: str = Field(..., description="Device hostname")
    ip: str = Field(..., description="Device IP")
    status: str = Field(..., description="pass or fail")
    checks: Dict[str, CheckResult] = Field(default_factory=dict, description="Check results")


class ValidationReport(BaseModel):
    """Full validation report with summary and device list (advanced)."""

    total: int = Field(..., ge=0, description="Total devices")
    passed: int = Field(..., ge=0, description="Passed count")
    failed: int = Field(..., ge=0, description="Failed count")
    devices: List[ValidationResult] = Field(default_factory=list, description="Per-device results")


# ============================================================================
# Advanced: BaseSettings (optional, if pydantic-settings installed)
# ============================================================================


if HAS_SETTINGS and BaseSettings is not None:

    class AppSettings(BaseSettings):
        """Load config from environment (advanced)."""

        app_name: str = Field(default="network-automation", description="Application name")
        log_level: str = Field(default="INFO", description="Logging level")
        timeout_seconds: int = Field(default=30, ge=1, le=300, description="Default timeout")

        model_config = {"env_prefix": "APP_", "extra": "ignore"}


# ============================================================================
# Demo: run examples
# ============================================================================


def demo_beginner() -> None:
    """Beginner: parse dict, serialize to dict/JSON."""
    data = {"hostname": "r1", "ip": "10.0.0.1", "vendor": "cisco"}
    device = Device.model_validate(data)
    logger.info("Device hostname: %s", device.hostname)
    logger.info("model_dump: %s", device.model_dump())
    logger.info("model_dump_json (exclude_none=True): %s", device.model_dump_json(exclude_none=True))

    # Nested
    data2 = {
        "hostname": "sw1",
        "ip": "10.0.0.2",
        "interfaces": [{"name": "Gi0/1", "status": "up"}, {"name": "Gi0/2", "status": "down"}],
    }
    device2 = Device.model_validate(data2)
    logger.info("Interfaces: %s", [i.name for i in device2.interfaces])


def demo_validation_error() -> None:
    """Show ValidationError when required field missing."""
    try:
        Device.model_validate({"hostname": "r1"})  # missing ip
    except ValidationError as e:
        logger.info("ValidationError (expected): %s", e.errors()[0]["msg"])


def demo_intermediate() -> None:
    """Intermediate: validators normalize hostname and validate ip."""
    d = DeviceWithFacts.model_validate({"hostname": "  R1  ", "ip": " 10.0.0.1 "})
    logger.info("Normalized hostname: %r", d.hostname)
    d2 = DeviceWithFacts.model_validate(
        {"hostname": "r2", "ip": "10.0.0.2", "facts": {"os_version": "15.2", "uptime_seconds": 3600}}
    )
    logger.info("Facts: %s", d2.facts)


def demo_advanced_report() -> None:
    """Advanced: build ValidationReport like automation-preflight."""
    report = ValidationReport(
        total=2,
        passed=1,
        failed=1,
        devices=[
            ValidationResult(
                hostname="r1",
                ip="10.0.0.1",
                status="pass",
                checks={"connectivity": CheckResult(status="pass")},
            ),
            ValidationResult(
                hostname="r2",
                ip="10.0.0.2",
                status="fail",
                checks={"connectivity": CheckResult(status="fail", reason="Connection refused")},
            ),
        ],
    )
    logger.info("Report JSON: %s", report.model_dump_json(indent=2)[:200] + "...")


def demo_settings() -> None:
    """Advanced: BaseSettings from env (if available)."""
    if not HAS_SETTINGS or BaseSettings is None:
        logger.info("pydantic-settings not installed; skip BaseSettings demo")
        return
    settings = AppSettings()
    logger.info("App settings: app_name=%s log_level=%s", settings.app_name, settings.log_level)


if __name__ == "__main__":
    demo_beginner()
    demo_validation_error()
    demo_intermediate()
    demo_advanced_report()
    demo_settings()
