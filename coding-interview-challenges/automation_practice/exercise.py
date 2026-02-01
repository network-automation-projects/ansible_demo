"""
Exercise: implement device load, filter by role, fake API, and report.
Fill in the TODOs. See README.md for the problem description.
"""

from pathlib import Path
from typing import Any


def load_devices_from_txt(path: str) -> list[dict[str, str]]:
    """Parse devices.txt: one line per device, format hostname,role,ip. Skip invalid lines."""
    devices = []
    # TODO: open path, loop over lines, strip, skip blank and comment (#)
    # TODO: split by comma, expect 3 parts; append {"hostname", "role", "ip"}
    # TODO: use try/except FileNotFoundError, print message and return []
    
    
    return devices


def load_devices_from_json(path: str) -> list[dict[str, str]]:
    """Load devices from JSON file. Skip items missing hostname, role, or ip."""
    # TODO: open path, json.load; handle FileNotFoundError and json.JSONDecodeError
    # TODO: for each item, if dict with hostname/role/ip keys, append to list
    return []


def get_device_status(hostname: str) -> dict[str, Any]:
    """Fake API: return status dict. Simulate failure for hostname 'core-sw2'."""
    # TODO: if hostname == "core-sw2": raise ConnectionError("Simulated timeout")
    # TODO: return {"hostname": hostname, "status": "up", "uptime_hours": 720}
    return {}


def build_report(
    devices: list[dict[str, str]], role_filter: str = "router"
) -> list[dict[str, Any]]:
    """Filter devices by role_filter, call get_device_status for each, build report list."""
    # TODO: filtered = [d for d in devices if d.get("role") == role_filter]
    # TODO: for each d, try: status_info = get_device_status(d["hostname"]); append to report
    # TODO: except: append same device with status "unknown", uptime_hours None
    report = []
    return report


def main() -> None:
    base = Path(__file__).parent
    path_txt = base / "devices.txt"
    devices = load_devices_from_txt(str(path_txt))
    if not devices:
        print("No devices loaded.")
        return
    report = build_report(devices, role_filter="router")
    for r in report:
        print(r)


if __name__ == "__main__":
    main()
