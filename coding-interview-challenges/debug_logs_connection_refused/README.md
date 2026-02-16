# Debug: Logs Show Connection Refused, Report Says Success

Debugging challenge for **automation-style** interviews. Focus: correlating error logs with code to find exception-handling bugs.

## Challenge

A batch job connects to multiple devices. The error logs show `ConnectionRefusedError` for device `core-sw2`. Yet the final report lists `core-sw2` as **success**.

**Your task:** Using the error logs and the code, figure out why the report incorrectly shows success for a device that failed.

## What You Have

- **buggy_batch.py** — Batch runner that processes devices. No real network; uses a mock that raises `ConnectionRefusedError` for `core-sw2`.
- **error_logs.txt** — Sample stderr/stdout from a run of the batch job.
- Run the code: `python buggy_batch.py` (output will match the logs)

## Expected vs Actual Behavior

- **Expected:** When a device raises `ConnectionRefusedError`, the report should show that device as failed.
- **Actual:** The report shows `core-sw2: success` despite logs showing connection refused.

## How to Approach

1. Read `error_logs.txt` and note the ERROR line for `core-sw2`.
2. Open `buggy_batch.py` and trace where that error would be raised and caught.
3. Find the bug: what happens in the exception handler?
4. Fix it.
5. Verify: the report should now show `core-sw2` as failed.

## Files

- **buggy_batch.py** — Code to debug
- **error_logs.txt** — Error output from a failed run
- **ANSWER.md** — Full explanation (read after attempting)
