# NRE Core Patterns — Live Coding Basics

Practice exercise for **network reliability / automation** live coding. Focus: dicts, lists, sets, input validation, drift detection, and batch operations with partial failure. All in-memory (no file I/O) so you can run and test quickly.

## What You'll Use

- **Dicts:** Grouping (role → list of hostnames), lookups, key sets for diff
- **Lists:** Filtering, iteration, list comprehensions
- **Sets:** Membership, deduplication, expected vs discovered diff
- **Validation:** `isinstance`, required keys, defensive `in` checks
- **Try/except:** Batch apply with intent; collect successes and failures without losing state

## Problem

### 1. Group devices by role

- **Function:** `group_devices_by_role(devices: list[dict]) -> dict[str, list[str]]`
- **Input:** List of dicts with at least `"hostname"` and `"role"`.
- **Output:** Dict mapping each role to list of hostnames.
- **Example:** `[{"hostname": "e1", "role": "edge"}, {"hostname": "e2", "role": "edge"}, {"hostname": "c1", "role": "core"}]` → `{"edge": ["e1", "e2"], "core": ["c1"]}`.

### 2. Filter and validate device list

- **Function:** `filter_valid_devices(devices: Any) -> list[dict]`
- **Rules:** If `devices` is not a list, raise `ValueError("devices must be a list")`. Return only items that are dicts and have both `"hostname"` and `"ip"` with non-empty strings.
- **Example:** `[{"hostname": "a", "ip": "1.2.3.4"}, {"hostname": "b"}]` → first only.

### 3. Expected vs discovered (sets)

- **Function:** `device_set_diff(expected: list[str] | set[str], discovered: list[str] | set[str]) -> tuple[set[str], set[str]]`
- **Return:** `(missing, extra)` where `missing = expected - discovered`, `extra = discovered - expected`. Accept list or set; convert to set internally.
- **Example:** `expected=["a","b","c"], discovered=["a","c","d"]` → `missing={"b"}`, `extra={"d"}`.

### 4. Drift: desired vs actual state

- **Function:** `config_drift(desired: dict[str, str], actual: dict[str, str]) -> tuple[list[str], list[str], list[str]]`
- **Return:** `(missing, extra, different)` — keys only in desired, only in actual, or in both with different values. Use sorted lists for stable output.
- **Example:** `desired={"a":"v1","b":"v2"}`, `actual={"a":"v1","b":"v3","c":"v"}` → missing=[], extra=["c"], different=["b"].

### 5. Batch with partial failure

- **Function:** `batch_apply(hostnames: list[str], apply_fn: Callable[[str], T]) -> dict[str, list]`
- **Semantics:** For each hostname, call `apply_fn(hostname)`. On success, append hostname to result `"ok"`; on exception, append `(hostname, str(e))` to result `"failed"`. Return `{"ok": [...], "failed": [(host, msg), ...]}`.
- **Skills:** Try/except with intent; do not lose state; collect successes and failures.

## Files

- **exercise.py** – Skeleton with TODOs; implement the five functions yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py`; all assertions should pass.
4. Compare with `solution.py` and refine.

## Example Output (solution.py)

When run, `main()` prints grouped devices, filtered list, set diff, config drift, and batch apply results; all assertions pass.
