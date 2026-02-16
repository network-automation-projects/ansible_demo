"""
Buggy parallel device runner.

Uses ThreadPoolExecutor to run a show command on multiple devices.
Results are sometimes wrong or inconsistent. Why?
"""

import random
import time
from concurrent.futures import ThreadPoolExecutor

# Shared mutable state: each thread writes here then appends to results.
# Another thread can overwrite before append, causing wrong device-to-uptime pairing.
_current_hostname: str = ""
_current_uptime: int = 0
results: list[tuple[str, int]] = []


def get_uptime(hostname: str) -> tuple[str, int]:
    """Mock: returns (hostname, uptime_hours) for the device."""
    uptimes = {"router-1": 100, "core-sw1": 200, "core-sw2": 150, "edge-sw1": 80}
    delay = random.uniform(0.01, 0.05)
    time.sleep(delay)
    return (hostname, uptimes.get(hostname, 0))


def run_one(hostname: str) -> None:
    """Run for one device. Bug: write to shared globals then append; no synchronization."""
    global _current_hostname, _current_uptime, results
    _current_hostname, _current_uptime = get_uptime(hostname)
    results.append((_current_hostname, _current_uptime))


def main() -> None:
    devices = ["router-1", "core-sw1", "core-sw2", "edge-sw1"]
    global results
    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(run_one, devices)

    print("Report:")
    for hostname, uptime in results:
        print(f"  {hostname}: {uptime}h")


if __name__ == "__main__":
    main()
