# Debug: Retry Never Succeeds

Debugging challenge for **automation-style** interviews. Focus: control flow in retry-with-backoff logic.

## Challenge

A device runner uses retry-with-backoff when tasks fail. The simulated task fails the first 2 attempts and succeeds on the 3rd. Yet the runner **always reports failure** after 3 attempts — it never succeeds on retry.

**Your task:** Figure out why the retry logic never allows a subsequent attempt to succeed.

## What You Have

- **buggy_runner.py** — Retry logic with a subtle bug. The code runs without crashing.
- Run it: `python buggy_runner.py`

## Expected vs Actual Behavior

- **Expected:** With `max_attempts=3` and a task that fails twice then succeeds, the runner should succeed on attempt 3.
- **Actual:** The runner reports failure after attempt 1 (or always fails). The retry loop never gives the task a second or third chance.

## How to Approach

1. Run the script and observe the output.
2. Trace the control flow: when does the loop continue vs return?
3. Find the bug. Fix it.
4. Verify: the runner should now succeed on the 3rd attempt.

## Files

- **buggy_runner.py** — Code to debug
- **ANSWER.md** — Full explanation (read after attempting)
