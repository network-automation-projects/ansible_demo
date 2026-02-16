# Debug: Wrong or Missing Results When Running Devices in Parallel

Debugging challenge for **parallel device handling** (e.g. ThreadPoolExecutor with Netmiko). Focus: race conditions when sharing mutable state across threads.

## Challenge

A script uses a thread pool to run a show command on multiple devices in parallel. The mock returns each device's hostname and uptime. Sometimes the **report is wrong**: missing devices, duplicate entries, or device names paired with another device's uptime. Running the script multiple times may show different (wrong) results.

**Your task:** Find why parallel execution produces inconsistent or incorrect results and fix it.

## What You Have

- **buggy_runner.py** — Uses `concurrent.futures.ThreadPoolExecutor` to query devices. Mock returns (hostname, uptime) per device. No real network.
- Run: `python buggy_runner.py` (run a few times and compare output if needed)

## Expected vs Actual Behavior

- **Expected:** Report shows exactly one result per device with the correct hostname and uptime (e.g. router-1: 100h, core-sw1: 200h, core-sw2: 150h).
- **Actual:** Results may be missing, duplicated, or misaligned (e.g. router-1 showing 200h instead of 100h). Output may change between runs.

## How to Approach

1. Run the script several times and note any inconsistency or wrong pairing.
2. Find where results are collected. Is a single list (or other mutable structure) shared across threads?
3. Identify the bug: appending to a shared list from multiple threads without synchronization, or relying on order of completion.
4. Fix it by collecting results from futures (e.g. return value from each task, then gather) instead of appending to a shared list inside workers.
5. Verify: run multiple times; output should be correct and stable.

## Files

- **buggy_runner.py** — Code to debug
- **ANSWER.md** — Full explanation (read after attempting)
