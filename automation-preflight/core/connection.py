"""Device connection handling (real Netmiko and mock mode)."""

import logging
from typing import Dict, Optional

from netmiko import ConnectHandler
from netmiko.ssh_exception import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
    NetmikoBaseException,
)

from models.device import DeviceInventory, DeviceFacts

logger = logging.getLogger(__name__)

# Default minimum OS versions by device type
DEFAULT_OS_VERSION_MIN = {
    "cisco_ios": "15.0",
    "cisco_xe": "16.0",
    "cisco_nxos": "7.0",
    "cisco_xr": "6.0",
    "juniper_junos": "12.0",
    "arista_eos": "4.0",
}


def parse_uptime_from_show_version(output: str, device_type: str) -> Optional[int]:
    """
    Parse uptime in seconds from 'show version' output.

    This is a simplified parser. Real implementations would need
    device-specific parsing logic.

    Args:
        output: Output from 'show version' command
        device_type: Netmiko device type

    Returns:
        Uptime in seconds, or None if unable to parse
    """
    lines = output.split("\n")
    for line in lines:
        line_lower = line.lower()
        if "uptime" in line_lower or "uptime is" in line_lower:
            if device_type.startswith("cisco"):
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.lower() in ("uptime", "is"):
                        if i + 1 < len(parts):
                            uptime_str = parts[i + 1]
                            try:
                                uptime_seconds = int(uptime_str)
                                return uptime_seconds
                            except ValueError:
                                pass
    return None


def parse_os_version_from_show_version(output: str) -> Optional[str]:
    """
    Parse OS version from 'show version' output.

    Simplified parser that looks for version patterns.

    Args:
        output: Output from 'show version' command

    Returns:
        Version string, or None if unable to parse
    """
    lines = output.split("\n")
    for line in lines:
        line_lower = line.lower()
        if "version" in line_lower and any(
            x in line_lower for x in ["software", "ios", "xe", "nx-os"]
        ):
            parts = line.split()
            for i, part in enumerate(parts):
                if part.lower() == "version" and i + 1 < len(parts):
                    version = parts[i + 1].rstrip(",")
                    return version
    return None


def parse_hostname_from_show_version(output: str) -> Optional[str]:
    """
    Parse hostname from 'show version' output.

    Args:
        output: Output from 'show version' command

    Returns:
        Hostname string, or None if unable to parse
    """
    lines = output.split("\n")
    for line in lines:
        if "hostname:" in line.lower() or "hostname is" in line.lower():
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return None


def get_device_facts_real(device: DeviceInventory) -> DeviceFacts:
    """
    Connect to device and collect facts using Netmiko.

    Args:
        device: Device inventory entry

    Returns:
        DeviceFacts object with collected information

    Raises:
        Exception: Various Netmiko exceptions for connection/auth failures
    """
    if not device.username or not device.password:
        raise ValueError(
            "Username and password required for real connections. "
            "Set NET_USER and NET_PASS env vars or provide in inventory."
        )

    connection_params = {
        "device_type": device.device_type,
        "host": device.ip,
        "username": device.username,
        "password": device.password,
        "port": device.port or 22,
        "timeout": 20,
        "banner_timeout": 30,
    }

    logger.info(f"Connecting to {device.hostname} ({device.ip})...")

    try:
        with ConnectHandler(**connection_params) as conn:
            logger.debug(f"Connected to {device.hostname}")

            show_version = conn.send_command("show version")

            hostname = parse_hostname_from_show_version(show_version)
            if not hostname:
                hostname = conn.find_prompt().strip().replace("#", "").replace(">", "")

            os_version = parse_os_version_from_show_version(show_version)
            uptime = parse_uptime_from_show_version(show_version, device.device_type)

            facts = DeviceFacts(
                hostname=hostname,
                os_version=os_version,
                uptime=uptime,
                variables=device.model_dump(),
            )

            logger.info(f"Collected facts from {device.hostname}: hostname={hostname}")
            return facts

    except NetmikoAuthenticationException as e:
        logger.error(f"Authentication failed for {device.hostname}: {e}")
        raise
    except NetmikoTimeoutException as e:
        logger.error(f"Connection timeout for {device.hostname}: {e}")
        raise
    except NetmikoBaseException as e:
        logger.error(f"Netmiko error for {device.hostname}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to {device.hostname}: {e}")
        raise


def get_device_facts_mock(device: DeviceInventory) -> DeviceFacts:
    """
    Generate mock device facts without connecting.

    Args:
        device: Device inventory entry

    Returns:
        DeviceFacts object with mock data
    """
    logger.info(f"Using mock facts for {device.hostname}")

    mock_hostname = device.hostname or "mock-device"
    mock_os_version = "17.03.01a"
    mock_uptime = 86400

    facts = DeviceFacts(
        hostname=mock_hostname,
        os_version=mock_os_version,
        uptime=mock_uptime,
        variables=device.model_dump(),
    )

    return facts


def get_device_facts(device: DeviceInventory, mock: bool = False) -> DeviceFacts:
    """
    Get device facts (real or mock).

    Args:
        device: Device inventory entry
        mock: If True, use mock data instead of connecting

    Returns:
        DeviceFacts object
    """
    if mock:
        return get_device_facts_mock(device)
    else:
        return get_device_facts_real(device)
