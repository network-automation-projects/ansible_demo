# Nautobot API Driver (Python)

Practice exercise for **pynautobot** and **Nautobot REST API** usage. Focus: connect to Nautobot (or use an in-memory mock), get devices for a site, and get a device by name. When `NAUTOBOT_URL` and `NAUTOBOT_TOKEN` are unset, use mock data so the exercise runs without a live Nautobot instance.

## What You'll Use

- **pynautobot:** `pynautobot.api(url=..., token=...)`, `api.dcim.devices.filter(site=...)`, query by name
- **Environment variables:** `os.environ.get("NAUTOBOT_URL")`, `os.environ.get("NAUTOBOT_TOKEN")` to decide real API vs mock
- **Abstraction:** One code path that works with either a real pynautobot API instance or a mock dict `{"devices": [...]}` (same device shape as the device-queries exercise)

## Problem

1. **get_nautobot_api(url, token)**  
   If `url` and `token` are non-empty, return `pynautobot.api(url=url, token=token)`. If either is empty, return `None` (caller will use mock).

2. **get_devices_for_site(api, site_name)**  
   - If `api` is a pynautobot API instance: return `list(api.dcim.devices.filter(site=site_name))`.
   - If `api` is a dict with key `"devices"`: return the result of `filter_devices_by_site(api["devices"], site_name)` (same logic as the nautobot_device_queries exercise).

3. **get_device_by_name(api, name)**  
   - If real API: query devices by name (e.g. filter by `name=name`), return the first match or `None`.
   - If mock: find the device dict in `api["devices"]` where `d["name"] == name`; return that dict or `None`.

4. **main()**  
   - If `NAUTOBOT_URL` and `NAUTOBOT_TOKEN` are set: create API with `get_nautobot_api`, call `get_devices_for_site` and `get_device_by_name`, print counts/results.
   - Else: build mock `{"devices": SAMPLE_DEVICES}` (in-file list, same structure as nautobot_device_queries), call the same functions with the mock, print results.

## Files

- **exercise.py** – Skeleton with TODOs and in-file `SAMPLE_DEVICES` for mock mode.
- **solution.py** – Reference solution with real API + mock fallback.
- **requirements.txt** – `pynautobot>=1.4.0` (only needed when using real Nautobot).

## How to Practice

1. Read this README. Install pynautobot if you want to run against a real Nautobot: `pip install -r requirements.txt`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python solution.py` (or `python3 solution.py`): without env vars it uses mock data; with `NAUTOBOT_URL` and `NAUTOBOT_TOKEN` it uses the live API.
4. Compare with `solution.py`.

## Prerequisites

- **Optional:** A running Nautobot instance and a token. If not available, the solution runs in mock mode and still demonstrates all logic.
