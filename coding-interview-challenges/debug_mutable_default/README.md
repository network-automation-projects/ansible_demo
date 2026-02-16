# Debug: Second Run Includes Devices From First Run

Debugging challenge for **automation-style** interviews. Focus: Python mutable default arguments.

## Challenge

An automation script processes a batch of devices and returns a report. When you run it **twice in a row** with different device lists, the second run's report includes devices from the **first** run as well.

**Your task:** Figure out why results from previous runs are leaking into later runs.

## What You Have

- **buggy_runner.py** — Batch processor that returns a list of processed devices. Run it twice with different inputs.
- Run: `python buggy_runner.py`

## Expected vs Actual Behavior

- **Expected:** Each run returns only the devices passed to that run. Run 1: [A, B]. Run 2: [C, D]. Output: [C, D].
- **Actual:** Run 2 outputs [A, B, C, D] — devices from run 1 are still there.

## How to Approach

1. Run the script (it simulates two batches).
2. Observe: the second batch includes devices from the first.
3. Find the bug. Hint: default argument evaluation.
4. Fix it.
5. Verify: each batch should report only its own devices.

## Files

- **buggy_runner.py** — Code to debug
- **ANSWER.md** — Full explanation (read after attempting)
