# Nautobot Device/Site Queries (Python)

Practice exercise for **Nautobot data model** and **query patterns**. Focus: work with in-memory data that mirrors Nautobot REST API device responses—filter by site, group by site, build summaries, and diff expected vs actual device lists. No Nautobot server or pynautobot required.

## What You'll Use

- **Dict/list navigation:** Nested access (`device["site"]["name"]`), safe handling of `primary_ip` (may be `None`)
- **Filtering:** List comprehensions or loops to filter devices by site name or slug
- **Grouping:** Build dict mapping site name → list of device names
- **Set-style diff:** Expected vs actual device names; return sorted lists for stable output
- **Defensive coding:** Use `.get()` for optional keys (e.g. `site`, `primary_ip`)

## Problem

1. **filter_devices_by_site(devices, site_name)**  
   Return devices whose `site["name"]` or `site["slug"]` equals `site_name`. Return a list of device dicts. Use defensive access (e.g. skip devices with missing or non-dict `site`).

2. **group_devices_by_site(devices)**  
   Return a dict mapping each site name to a list of device **names** (e.g. `{"dc1": ["sw1", "sw2"], "dc2": ["sw3"]}`). Derive site name from `device["site"]["name"]` or `device["site"]["slug"]`; skip devices without a valid site.

3. **device_summary_list(devices)**  
   Return a list of summary dicts: `{"name": str, "site_name": str, "primary_ip": str | None}`. Extract `site_name` from nested `site`; extract `primary_ip` from `primary_ip["address"]` if present, else `None`.

4. **device_list_diff(expected_names, devices)**  
   Return `(missing, extra)` where `missing` = names in `expected_names` not present in the device list, and `extra` = device names not in `expected_names`. Both lists must be **sorted** for stable output.

## Files

- **exercise.py** – Skeleton with TODOs and in-file `SAMPLE_DEVICES`; implement the four functions yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect `SAMPLE_DEVICES` in `exercise.py`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py`; all assertions should pass (or add your own in `main()`).
4. Compare with `solution.py`.

## Example

- **filter_devices_by_site:** devices with site "dc1" → list of 2 device dicts.
- **group_devices_by_site:** → `{"dc1": ["sw1", "sw2"], "dc2": ["sw3"]}` (site name → device names).
- **device_summary_list:** → `[{"name": "sw1", "site_name": "dc1", "primary_ip": "10.0.1.1"}, ...]`; devices with no primary_ip get `"primary_ip": None`.
- **device_list_diff(expected_names=["sw1", "sw9"], devices):** → `(missing=["sw9"], extra=["sw2", "sw3"])` (sorted).
