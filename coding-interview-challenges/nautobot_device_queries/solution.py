"""
Nautobot device/site queries: filter by site, group by site, summary list, device list diff.
"""

# Sample data mirroring Nautobot REST API device shape.
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
    result: list[dict] = []
    for d in devices:
        site = d.get("site")
        if not isinstance(site, dict):
            continue
        if site.get("name") == site_name or site.get("slug") == site_name:
            result.append(d)
    return result


def group_devices_by_site(devices: list[dict]) -> dict[str, list[str]]:
    """Return dict mapping site name to list of device names."""
    result: dict[str, list[str]] = {}
    for d in devices:
        site = d.get("site")
        if not isinstance(site, dict):
            continue
        site_name = site.get("name") or site.get("slug")
        if site_name is None:
            continue
        if site_name not in result:
            result[site_name] = []
        name = d.get("name")
        if name is not None:
            result[site_name].append(name)
    return result


def device_summary_list(devices: list[dict]) -> list[dict]:
    """Return list of {"name", "site_name", "primary_ip"} (primary_ip is str or None)."""
    out: list[dict] = []
    for d in devices:
        name = d.get("name")
        site = d.get("site")
        site_name = ""
        if isinstance(site, dict):
            site_name = site.get("name") or site.get("slug") or ""
        primary_ip_val: str | None = None
        pi = d.get("primary_ip")
        if isinstance(pi, dict) and pi.get("address"):
            primary_ip_val = pi["address"]
        out.append(
            {"name": name, "site_name": site_name, "primary_ip": primary_ip_val}
        )
    return out


def device_list_diff(
    expected_names: list[str], devices: list[dict]
) -> tuple[list[str], list[str]]:
    """Return (missing, extra): expected not in devices, device names not in expected. Sorted."""
    device_names = {d["name"] for d in devices if d.get("name") is not None}
    expected_set = set(expected_names)
    missing = sorted(expected_set - device_names)
    extra = sorted(device_names - expected_set)
    return (missing, extra)


def main() -> None:
    # 1. Filter by site
    dc1_devices = filter_devices_by_site(SAMPLE_DEVICES, "dc1")
    assert len(dc1_devices) == 2
    assert [d["name"] for d in dc1_devices] == ["sw1", "sw2"]
    dc2_devices = filter_devices_by_site(SAMPLE_DEVICES, "dc2")
    assert len(dc2_devices) == 1 and dc2_devices[0]["name"] == "sw3"

    # 2. Group by site
    grouped = group_devices_by_site(SAMPLE_DEVICES)
    assert grouped["dc1"] == ["sw1", "sw2"] and grouped["dc2"] == ["sw3"]

    # 3. Summary list
    summaries = device_summary_list(SAMPLE_DEVICES)
    assert len(summaries) == 3
    assert summaries[0]["name"] == "sw1" and summaries[0]["site_name"] == "dc1"
    assert summaries[0]["primary_ip"] == "10.0.1.1/24"
    assert summaries[1]["primary_ip"] is None

    # 4. Device list diff
    missing, extra = device_list_diff(["sw1", "sw9"], SAMPLE_DEVICES)
    assert missing == ["sw9"] and extra == ["sw2", "sw3"]

    print("filter_devices_by_site(dc1):", [d["name"] for d in dc1_devices])
    print("group_devices_by_site:", grouped)
    print("device_summary_list (first):", summaries[0])
    print("device_list_diff([sw1, sw9], devices): missing=", missing, "extra=", extra)
    print("All assertions passed.")


if __name__ == "__main__":
    main()
