"""Core validation logic for device readiness checks."""

import logging
from packaging import version

from models.device import (
    DeviceInventory,
    DeviceFacts,
    ValidationResult,
    CheckResult,
    ValidationSummary,
    ValidationReport,
)
from core.connection import DEFAULT_OS_VERSION_MIN

logger = logging.getLogger(__name__)


def check_hostname(facts: DeviceFacts) -> CheckResult:
    """
    Check if hostname is present.

    Args:
        facts: Device facts

    Returns:
        CheckResult with pass/fail status
    """
    if not facts.hostname or not facts.hostname.strip():
        return CheckResult(
            status="fail", reason="Hostname not detected or empty"
        )
    return CheckResult(status="pass")


def check_os_version(
    facts: DeviceFacts, device: DeviceInventory, default_min: Optional[str] = None
) -> CheckResult:
    """
    Check if OS version meets minimum requirement.

    Args:
        facts: Device facts
        device: Device inventory entry
        default_min: Default minimum version (from device type defaults)

    Returns:
        CheckResult with pass/fail status
    """
    if not facts.os_version:
        return CheckResult(
            status="fail", reason="OS version not detected from device"
        )

    min_version_str = (
        device.os_version_min
        or default_min
        or DEFAULT_OS_VERSION_MIN.get(device.device_type)
    )

    if not min_version_str:
        return CheckResult(status="pass")

    try:
        device_version = version.parse(facts.os_version)
        min_version = version.parse(min_version_str)

        if device_version < min_version:
            return CheckResult(
                status="fail",
                reason=f"OS version {facts.os_version} not supported (minimum: {min_version_str})",
            )
        return CheckResult(status="pass")
    except version.InvalidVersion:
        logger.warning(
            f"Unable to parse version '{facts.os_version}' or '{min_version_str}'"
        )
        return CheckResult(
            status="fail",
            reason=f"Unable to parse version strings for comparison",
        )


def check_uptime(facts: DeviceFacts, device: DeviceInventory) -> CheckResult:
    """
    Check if uptime meets threshold.

    Args:
        facts: Device facts
        device: Device inventory entry

    Returns:
        CheckResult with pass/fail status
    """
    threshold = device.uptime_threshold or 0

    if facts.uptime is None:
        return CheckResult(
            status="fail", reason="Uptime not detected from device"
        )

    if facts.uptime < threshold:
        return CheckResult(
            status="fail",
            reason=f"Uptime {facts.uptime}s below threshold {threshold}s",
        )

    return CheckResult(status="pass")


def check_variables(device: DeviceInventory) -> CheckResult:
    """
    Check if required variables are present in inventory.

    Args:
        device: Device inventory entry

    Returns:
        CheckResult with pass/fail status
    """
    required_fields = ["hostname", "ip", "device_type"]
    missing = []

    for field in required_fields:
        value = getattr(device, field, None)
        if not value:
            missing.append(field)

    if missing:
        return CheckResult(
            status="fail", reason=f"Missing required field(s): {', '.join(missing)}"
        )

    return CheckResult(status="pass")


def validate_device(
    device: DeviceInventory, facts: DeviceFacts
) -> ValidationResult:
    """
    Validate a single device against all checks.

    Args:
        device: Device inventory entry
        facts: Device facts

    Returns:
        ValidationResult with all check results
    """
    logger.debug(f"Validating device {device.hostname}")

    default_min_version = DEFAULT_OS_VERSION_MIN.get(device.device_type)

    checks = {
        "hostname": check_hostname(facts),
        "os_version": check_os_version(facts, device, default_min_version),
        "uptime": check_uptime(facts, device),
        "variables": check_variables(device),
    }

    all_pass = all(check.status == "pass" for check in checks.values())
    overall_status = "pass" if all_pass else "fail"

    result = ValidationResult(
        hostname=device.hostname,
        ip=device.ip,
        status=overall_status,
        checks=checks,
    )

    if overall_status == "pass":
        logger.info(f"Device {device.hostname} passed all validation checks")
    else:
        failed_checks = [name for name, check in checks.items() if check.status == "fail"]
        logger.warning(
            f"Device {device.hostname} failed checks: {', '.join(failed_checks)}"
        )

    return result


def validate_devices(
    devices: list[DeviceInventory],
    facts_list: list[DeviceFacts],
    connection_errors: Optional[dict[str, str]] = None,
) -> ValidationReport:
    """
    Validate multiple devices and generate report.

    Args:
        devices: List of device inventory entries
        facts_list: List of device facts (one per device)
        connection_errors: Optional dict mapping hostname to error message

    Returns:
        ValidationReport with summary and per-device results
    """
    connection_errors = connection_errors or {}

    results = []
    for device, facts in zip(devices, facts_list):
        if device.hostname in connection_errors:
            result = ValidationResult(
                hostname=device.hostname,
                ip=device.ip,
                status="fail",
                checks={},
                connection_error=connection_errors[device.hostname],
            )
        else:
            result = validate_device(device, facts)
        results.append(result)

    passed = sum(1 for r in results if r.status == "pass")
    failed = len(results) - passed

    summary = ValidationSummary(total=len(results), passed=passed, failed=failed)

    return ValidationReport(summary=summary, devices=results)
