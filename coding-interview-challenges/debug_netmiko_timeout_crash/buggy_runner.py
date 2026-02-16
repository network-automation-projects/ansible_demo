"""
Buggy device runner using a mock Netmiko-style connection.

When core-sw2 is processed, the mock raises NetmikoTimeoutException.
The script crashes instead of recording failure and continuing. Why?
"""

import logging
from dataclasses import dataclass
from typing import Literal

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Simulate NetmikoTimeoutException when netmiko is not installed
try:
    from netmiko import ConnectHandler, NetmikoTimeoutException
except ImportError:
    NetmikoTimeoutException = type("NetmikoTimeoutException", (Exception,), {})


@dataclass
class DeviceResult:
    hostname: str
    status: Literal["success", "failed"]
    output: str | None = None
    error: str | None = None


def connect_and_run(hostname: str) -> DeviceResult:
    """
    Mock connection and command. Raises NetmikoTimeoutException for core-sw2.
    """
    if hostname == "core-sw2":
        raise NetmikoTimeoutException(f"Connection timed out to {hostname}")
    return DeviceResult(
        hostname=hostname,
        status="success",
        output=f"show version output for {hostname}",
    )


def run_batch(devices: list[str]) -> list[DeviceResult]:
    """Process each device and collect results. No exception handling."""
    results: list[DeviceResult] = []

    for hostname in devices:
        result = connect_and_run(hostname)
        results.append(result)

    return results


def main() -> None:
    devices = ["router-1", "core-sw1", "core-sw2", "edge-sw1"]
    results = run_batch(devices)

    print("\n--- Report ---")
    for r in results:
        err = f" ({r.error})" if r.error else ""
        print(f"  {r.hostname}: {r.status}{err}")


if __name__ == "__main__":
    main()
