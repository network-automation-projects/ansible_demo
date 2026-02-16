"""
Buggy device runner that collects uptime per device.

router-2 is simulated to fail. The report shows router-3 with router-2's uptime.
Why?
"""

from dataclasses import dataclass

# Mock: hostname -> uptime_hours. router-2 "fails" (not in dict).
MOCK_UPTIME = {
    "router-1": 100,
    "router-3": 360,
}
# router-2 would be 720 if it worked, but we simulate failure


def get_uptime(hostname: str) -> int | None:
    """Simulated API: returns uptime or None (failure)."""
    if hostname == "router-2":
        return None  # Simulated failure
    return MOCK_UPTIME.get(hostname)


def run_batch(devices: list[str]) -> tuple[list[str], list[int | None]]:
    """Process devices, return (hostnames, uptimes)."""
    hostnames: list[str] = []
    uptimes: list[int | None] = []

    for device in devices:
        hostnames.append(device)
        uptime = get_uptime(device)
        if uptime is not None:
            uptimes.append(uptime)
        # Bug: when uptime is None, we don't append — uptimes is now shorter

    return hostnames, uptimes


def main() -> None:
    devices = ["router-1", "router-2", "router-3"]
    hostnames, uptimes = run_batch(devices)

    print("Report:")
    for i in range(len(hostnames)):
        u = uptimes[i] if i < len(uptimes) else "N/A"
        status = f"{u}h" if isinstance(u, int) else "failed"
        print(f"  {hostnames[i]}: {status}")


if __name__ == "__main__":
    main()
