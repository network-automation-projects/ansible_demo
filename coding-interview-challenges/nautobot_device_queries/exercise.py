"""
Exercise: Nautobot-style device/site queries (filter, group, summary, diff).
Fill in the TODOs. See README.md for the problem description.
"""

# Sample data mirroring Nautobot REST API device shape (2–3 sites, 4–6 devices).
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
    """Return devices whose site name or slug equals site_name."""
    # TODO: for each device, get site = device.get("site"); if site and isinstance(site, dict),
    #       check site.get("name") == site_name or site.get("slug") == site_name; collect matches
    raise NotImplementedError("TODO: implement filter_devices_by_site")


def group_devices_by_site(devices: list[dict]) -> dict[str, list[str]]:
    """Return dict mapping site name to list of device names."""
    # TODO: build result[site_name] = list of device["name"]; derive site_name from device["site"]["name"] or slug
    raise NotImplementedError("TODO: implement group_devices_by_site")


def device_summary_list(devices: list[dict]) -> list[dict]:
    """Return list of {"name", "site_name", "primary_ip"} (primary_ip is str or None)."""
    # TODO: for each device: name = device.get("name"); site_name from device.get("site"); primary_ip from device.get("primary_ip")["address"] or None
    raise NotImplementedError("TODO: implement device_summary_list")


def device_list_diff(
    expected_names: list[str], devices: list[dict]
) -> tuple[list[str], list[str]]:
    """Return (missing, extra): expected not in devices, device names not in expected. Sorted."""
    # TODO: device_names = set(d["name"] for d in devices if d.get("name")); expected_set = set(expected_names)
    # TODO: missing = sorted(expected_set - device_names); extra = sorted(device_names - expected_set)
    raise NotImplementedError("TODO: implement device_list_diff")


def main() -> None:
    # TODO: run assertions against SAMPLE_DEVICES for all four functions; print results
    pass


if __name__ == "__main__":
    main()
