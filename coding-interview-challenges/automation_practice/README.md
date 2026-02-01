# Automation Practice: Device List + Filter + Fake API

Practice exercise for **automation-style** technical interviews (e.g. network reliability & automation roles). Focus: read a file or list of devices, filter/transform, optionally "call" a fake API, and handle errors cleanly.

## What You'll Use

- **File I/O:** `open()`, reading lines or `json.load`
- **Parsing:** `split()` or `re` for `hostname,role,ip`; validating JSON
- **Dicts/lists:** list of dicts, filtering (e.g. list comprehension), building a report
- **Error handling:** `try/except` for missing file, bad JSON, "API" failures
- **Structure:** small functions (load, filter, get_status, report) instead of one big block

## Problem

1. **Read devices** from `devices.txt` (format: `hostname,role,ip` per line) or from `devices.json`.
   - Skip blank lines and lines that don't match the expected format.
   - For JSON, skip entries missing `hostname`, `role`, or `ip`.
2. **Filter** to devices where `role` equals a given value (e.g. `"router"`).
3. **Fake API:** For each filtered device, call `get_device_status(hostname)` that returns e.g. `{"status": "up", "uptime_hours": 720}`. Implement it as a stub (no real HTTP). If the "API" raises for a device, catch and set `status` to `"unknown"`.
4. **Report:** Build a list of dicts with `hostname`, `ip`, `role`, `status`, and optionally `uptime_hours`. Print or return it.
5. **Errors:** If the file is missing or empty, print a clear message and exit (or return empty list). Use `try/except` around file and JSON.

## Files

- **devices.txt** – Sample input (one device per line: `hostname,role,ip`).
- **devices.json** – Same data in JSON for optional "load from JSON" practice.
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and the sample files.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run against `devices.txt` and optionally `devices.json`; check output.
4. Compare with `solution.py` and refine (e.g. add regex validation, or support both file types in one script).

## Example Output (solution.py)

When run with `role_filter="router"`, you should see routers with status; `core-sw2` is simulated to "fail" the API call and appear as `status: unknown`.
