"""
Nautobot API driver: connect (real or mock), get devices for site, get device by name.
"""

import os
from typing import Any

try:
    import pynautobot
except ImportError:
    pynautobot = None  # type: ignore[assignment]

# Same shape as nautobot_device_queries; used when NAUTOBOT_URL / NAUTOBOT_TOKEN are unset.
SAMPLE_DEVICES: list[dict] = [
    {
        "name": "sw1",
        "site": {"name": "dc1", "slug": "dc1"},
        "primary_ip": {"address": "10.0.1.1/24"},
        "device_role": {"name": "switch"},
        "status": {"value": "active"},
    },
    {
        "name": "sw2",
        "site": {"name": "dc1", "slug": "dc1"},
        "primary_ip": None,
        "device_role": {"name": "switch"},
        "status": {"value": "active"},
    },
    {
        "name": "sw3",
        "site": {"name": "dc2", "slug": "dc2"},
        "primary_ip": {"address": "10.0.2.1/24"},
        "device_role": {"name": "router"},
        "status": {"value": "active"},
    },
]


def filter_devices_by_site(devices: list[dict], site_name: str) -> list[dict]:
    """Return devices whose site name or slug equals site_name. (Used by mock path.)"""
    result: list[dict] = []
    for d in devices:
        site = d.get("site")
        if not isinstance(site, dict):
            continue
        if site.get("name") == site_name or site.get("slug") == site_name:
            result.append(d)
    return result


def get_nautobot_api(url: str, token: str) -> Any:
    """Return pynautobot api instance if url and token are non-empty; else None."""
    if not url or not token or pynautobot is None:
        return None
    return pynautobot.api(url=url, token=token)


def get_devices_for_site(api: Any, site_name: str) -> list:
    """If api is dict with 'devices': filter by site. Else use pynautobot dcim.devices.filter(site=site_name)."""
    if isinstance(api, dict) and "devices" in api:
        return filter_devices_by_site(api["devices"], site_name)
    return list(api.dcim.devices.filter(site=site_name))


def get_device_by_name(api: Any, name: str) -> dict | Any | None:
    """If mock: return device dict or None. If real API: return first match or None."""
    if isinstance(api, dict) and "devices" in api:
        for d in api["devices"]:
            if d.get("name") == name:
                return d
        return None
    matches = list(api.dcim.devices.filter(name=name))
    return matches[0] if matches else None


def main() -> None:
    url = os.environ.get("NAUTOBOT_URL", "").strip()
    token = os.environ.get("NAUTOBOT_TOKEN", "").strip()

    if url and token and pynautobot is not None:
        api = get_nautobot_api(url, token)
        if api is not None:
            print("Using real Nautobot API at", url)
            devices_dc1 = get_devices_for_site(api, "dc1")
            dev = get_device_by_name(api, "sw1")
            print("Devices at site dc1:", len(devices_dc1))
            print("Device sw1:", dev.name if dev else None)
            return
    # Mock path
    api = {"devices": SAMPLE_DEVICES}
    print("Using mock data (NAUTOBOT_URL/NAUTOBOT_TOKEN unset or pynautobot not installed)")
    devices_dc1 = get_devices_for_site(api, "dc1")
    dev = get_device_by_name(api, "sw1")
    assert len(devices_dc1) == 2
    assert dev is not None and dev.get("name") == "sw1"
    print("Devices at site dc1:", [d["name"] for d in devices_dc1])
    print("Device sw1:", dev.get("name"))
    print("Mock assertions passed.")


if __name__ == "__main__":
    main()
