# Debug: Script Crashes on Device Timeout

Debugging challenge for **Netmiko/NAPALM-style** automation. Focus: exception handling so timeouts don't crash the whole run.

## Challenge

A device runner connects to multiple devices and runs a show command. When one device (e.g. `core-sw2`) is unreachable, the script raises an unhandled exception and **crashes** instead of recording that device as failed and continuing with the rest.

**Your task:** Find why a single device timeout stops the entire batch, and fix it so the report shows success/failure per device without crashing.

## What You Have

- **buggy_runner.py** — Batch runner that uses a mock connection. The mock raises `NetmikoTimeoutException` for `core-sw2`. No real network.
- Run: `python buggy_runner.py`

## Expected vs Actual Behavior

- **Expected:** When `core-sw2` times out, the script logs the failure, records that device as failed, and prints a report for all devices (e.g. router-1: success, core-sw1: success, core-sw2: failed, edge-sw1: success).
- **Actual:** The script crashes with `NetmikoTimeoutException` (or similar) when it hits `core-sw2`. No report is printed.

## How to Approach

1. Run the script and note the traceback when it crashes.
2. Find where the timeout is raised and where it should be caught.
3. Add (or fix) exception handling so timeouts are caught per device and recorded as failed.
4. Ensure the report is still printed after processing all devices.
5. Verify: run again; the script should complete and show core-sw2 as failed.

## Files

- **buggy_runner.py** — Code to debug
- **ANSWER.md** — Full explanation (read after attempting)
