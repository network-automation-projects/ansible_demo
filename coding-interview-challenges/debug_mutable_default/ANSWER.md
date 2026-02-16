# Answer: Why the Second Run Includes Devices From the First

## Root Cause

The function uses a **mutable default argument** `results: list[str] = []`. In Python, default arguments are evaluated **once** when the function is defined, not each time it is called. The same list object is reused across all calls. Appending to it in one call persists for the next.

## Why It Manifests

1. First call: `process_batch(["router-1", "router-2"])` — the default `[]` is used. We append "router-1" and "router-2". The list now has 2 items. We return it.
2. Second call: `process_batch(["core-sw1", "core-sw2"])` — Python reuses the **same** list object (it was never replaced). We append "core-sw1" and "core-sw2". The list now has 4 items: router-1, router-2, core-sw1, core-sw2.
3. Both `batch1` and `batch2` reference the same list. Printing `batch2` shows all 4.

## Code Fix

Use `None` as the default and create a new list inside the function:

```python
def process_batch(devices: list[str], results: list[str] | None = None) -> list[str]:
    if results is None:
        results = []
    for device in devices:
        results.append(device)
    return results
```

Or, if the function should always start fresh, omit the parameter and build the list locally:

```python
def process_batch(devices: list[str]) -> list[str]:
    results: list[str] = []
    for device in devices:
        results.append(device)
    return results
```

## How to Spot Similar Bugs

- **Mutable defaults:** Any default like `= []`, `= {}`, `= set()` is a red flag. The object is shared across calls.
- **Accumulation across calls:** If results "accumulate" or "leak" between invocations, check default arguments.
- **`id()` check:** `id(results)` will be the same across calls if it's the same object.

## Best Practices

1. **Never use mutable defaults:** Use `None` and assign a new mutable inside the function.
2. **Pylint/type checkers:** Tools like Pylint flag `W0102` (dangerous-default-value) for this pattern.
3. **Documentation:** If a function intentionally mutates a passed-in list, document it. For "return new results," don't use a default at all.
