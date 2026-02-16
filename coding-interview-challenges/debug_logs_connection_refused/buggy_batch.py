"""
Buggy batch runner for device automation.

Connects to multiple devices and builds a report.
Logs show ConnectionRefusedError for core-sw2, but the report says success. Why?
"""

import logging
from dataclasses import dataclass
from typing import Literal

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class TaskResult:
    hostname: str
    status: Literal["success", "failed"]
    error: str | None = None


def connect_and_run(hostname: str) -> TaskResult:
    """
    Simulated connection + task execution.
    Raises ConnectionRefusedError for core-sw2 (simulated unreachable device).
    """
    if hostname == "core-sw2":
        raise ConnectionRefusedError(
            f"Connection refused for device {hostname}"
        )
    return TaskResult(hostname=hostname, status="success")


def run_batch(devices: list[str]) -> list[TaskResult]:
    """Process each device and collect results."""
    results: list[TaskResult] = []

    for hostname in devices:
        status = "success"
        error = None
        try:
            result = connect_and_run(hostname)
            results.append(result)
        except Exception as e:
            logger.error(f"Connection refused for device {hostname}: {e}")
            error = str(e)
            status = "failed"
        
        results.append(TaskResult(hostname=hostname, status=status, error=error))

    return results


def main() -> None:
    devices = ["router-1", "core-sw1", "core-sw2", "edge-sw1"]
    results = run_batch(devices)

    print("\n--- Report ---")
    for r in results:
        print(f"{r.hostname}: {r.status}")


if __name__ == "__main__":
    main()
