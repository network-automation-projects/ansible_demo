# Practical: Retry with Backoff

Practice exercise for **automation-style** interviews. Focus: wrap a flaky function (e.g. "call API") in retry logic with exponential backoff and a maximum number of attempts; catch specific exceptions.

## What You'll Use

- **try/except:** catch the exception that the flaky call raises (e.g. `ConnectionError`, `TimeoutError`)
- **Loop:** retry up to N times; break on success
- **time.sleep:** wait between attempts; e.g. 1s, 2s, 4s (exponential backoff)
- **Optional:** cap the sleep time (e.g. max 30 seconds)

## Problem

1. **Flaky function:** You are given a callable that may raise an exception (e.g. `ConnectionError`) on failure. On success it returns a value.
2. **Retry decorator or wrapper:** Implement a function `retry_with_backoff(func, max_attempts=3, base_delay=1.0, max_delay=30.0)` that:
   - Calls `func()` (no arguments for simplicity).
   - If it succeeds, return the result.
   - If it raises the designated exception(s), wait `base_delay` seconds (then 2×, then 4×, …), then retry, up to `max_attempts` times.
   - If all attempts fail, re-raise the last exception (or raise a custom "max retries exceeded").
3. **Exponential backoff:** delay = min(base_delay * (2 ** attempt_index), max_delay). attempt_index is 0 before first retry, 1 before second retry, etc.

## Files

- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run and check that a flaky call eventually succeeds or fails after max attempts.
4. Compare with `solution.py`.

## Example

A fake "API" that fails twice then succeeds: `retry_with_backoff(flaky_api, max_attempts=3, base_delay=0.1)` should succeed on the third try after two short waits.
