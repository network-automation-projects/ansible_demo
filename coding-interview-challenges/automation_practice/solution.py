"""
Device list: read file, filter by role, fake API status, report.
Practice: open, json, dicts/lists, error handling.
"""

import json
from pathlib import Path
from typing import Any


def load_devices_from_txt(path: str) -> list[dict[str, str]]:
    """Parse devices.txt lines (hostname,role,ip). Skip invalid lines."""
    devices = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) == 3:
                    devices.append({
                        "hostname": parts[0],
                        "role": parts[1],
                        "ip": parts[2],
                    })
    except FileNotFoundError:
        print(f"File not found: {path}")
        return []
    return devices


def load_devices_from_json(path: str) -> list[dict[str, str]]:
    """Load devices from JSON. Skip entries missing hostname/role/ip."""
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return []

    devices = []
    for item in data:
        if isinstance(item, dict) and "hostname" in item and "role" in item and "ip" in item:
            devices.append({
                "hostname": item["hostname"],
                "role": item["role"],
                "ip": item["ip"],
            })
    return devices


def get_device_status(hostname: str) -> dict[str, Any]:
    """Fake API: return status for a device. Simulate failure for one host."""
    if hostname == "core-sw2":
        raise ConnectionError("Simulated timeout")
    return {
        "hostname": hostname,
        "status": "up",
        "uptime_hours": 720,
    }


def build_report(
    devices: list[dict[str, str]], role_filter: str = "router"
) -> list[dict[str, Any]]:
    """Filter by role and enrich with status from fake API."""
    filtered = [d for d in devices if d.get("role") == role_filter]
    report = []
    for d in filtered:
        try:
            status_info = get_device_status(d["hostname"])
            report.append({
                "hostname": d["hostname"],
                "ip": d["ip"],
                "role": d["role"],
                "status": status_info.get("status", "unknown"),
                "uptime_hours": status_info.get("uptime_hours"),
            })
        except Exception:
            report.append({
                "hostname": d["hostname"],
                "ip": d["ip"],
                "role": d["role"],
                "status": "unknown",
                "uptime_hours": None,
            })
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
