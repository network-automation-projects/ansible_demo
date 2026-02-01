"""
Exercise: Nautobot API driver — connect, get devices for site, get device by name (real API or mock).
Fill in the TODOs. See README.md for the problem description.
"""

import os
from typing import Any

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
    # TODO: same logic as nautobot_device_queries: collect devices where site["name"] or site["slug"] == site_name
    raise NotImplementedError("TODO: implement filter_devices_by_site (or reuse from device_queries)")


def get_nautobot_api(url: str, token: str) -> Any:
    """Return pynautobot api instance if url and token are non-empty; else None."""
    # TODO: if url and token: return pynautobot.api(url=url, token=token); else return None
    raise NotImplementedError("TODO: implement get_nautobot_api")


def get_devices_for_site(api: Any, site_name: str) -> list:
    """If api is pynautobot: return list(api.dcim.devices.filter(site=site_name)). If api is dict: return filter_devices_by_site(api['devices'], site_name)."""
    # TODO: if api is dict and "devices" in api: return filter_devices_by_site(api["devices"], site_name)
    # TODO: else: return list(api.dcim.devices.filter(site=site_name))
    raise NotImplementedError("TODO: implement get_devices_for_site")


def get_device_by_name(api: Any, name: str) -> dict | None:
    """If real API: filter devices by name, return first match or None. If mock: return device dict or None."""
    # TODO: if api is dict and "devices" in api: find d in api["devices"] where d.get("name") == name; return d or None
    # TODO: else: return first from api.dcim.devices.filter(name=name) or None
    raise NotImplementedError("TODO: implement get_device_by_name")


def main() -> None:
    # TODO: url = os.environ.get("NAUTOBOT_URL", ""); token = os.environ.get("NAUTOBOT_TOKEN", "")
    # TODO: if url and token: api = get_nautobot_api(url, token); else: api = {"devices": SAMPLE_DEVICES}
    # TODO: devices_dc1 = get_devices_for_site(api, "dc1"); dev = get_device_by_name(api, "sw1"); print counts/results
    pass


if __name__ == "__main__":
    main()
