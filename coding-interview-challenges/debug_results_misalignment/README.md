# Debug: Device Output Mismatch (router-3 Shows router-2's Data)

Debugging challenge for **automation-style** interviews. Focus: list indexing when some iterations skip appending.

## Challenge

A device runner processes three routers and builds a report. The output shows **router-2** with 360h (router-3's uptime) and **router-3** as "failed" even though router-3's data was collected successfully. The report is misaligned.

**Your task:** Figure out why device-to-result pairing is incorrect when one device fails.

## What You Have

- **buggy_runner.py** — Processes devices; one device (router-2) is simulated to fail.
- Run: `python buggy_runner.py`

## Expected vs Actual Behavior

- **Expected:** Report shows router-1: 100h, router-2: failed, router-3: 360h.
- **Actual:** Report shows router-1: 100h, router-2: 360h (wrong — should be failed), router-3: failed (wrong — should be 360h).

## How to Approach

1. Run the script and compare the report to the mock data.
2. Trace: when router-2 fails, what gets appended to the results list?
3. Find the bug: how does the code pair devices with results?
4. Fix it.
5. Verify: each device should show its own data (or "failed").

## Files

- **buggy_runner.py** — Code to debug
- **ANSWER.md** — Full explanation (read after attempting)
