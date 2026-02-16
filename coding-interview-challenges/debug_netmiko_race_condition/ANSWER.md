# Answer: Why Parallel Results Are Wrong or Inconsistent

## Root Cause

The script uses **shared mutable global state** (`_current_hostname`, `_current_uptime`) that each worker thread writes, then reads when appending to `results`. There is no lock. Between one thread writing the globals and that same thread appending `(_current_hostname, _current_uptime)`, another thread can overwrite the globals. So the first thread may append the second thread's data, causing **misaligned device-to-uptime pairing** (e.g. router-1 listed with 200h instead of 100h). Result order can also be non-deterministic (completion order), so the report may not match the device list order.

## Why It Manifests

1. Thread A runs for router-1, sets `_current_hostname="router-1"`, `_current_uptime=100`.
2. Thread B runs for core-sw1, sets `_current_hostname="core-sw1"`, `_current_uptime=200`.
3. Thread A resumes and executes `results.append((_current_hostname, _current_uptime))` — but the globals were overwritten by B, so A appends `("core-sw1", 200)`.
4. Later, B may append again or another thread's data appears for a different device. The report shows wrong pairings or duplicate/missing entries depending on interleaving.

## Code Fix

**Do not share mutable state.** Have each worker return its result and collect results from the executor so the main thread is the only one writing the result list:

```python
def run_one(hostname: str) -> tuple[str, int]:
    """Run for one device; return (hostname, uptime). No shared state."""
    return get_uptime(hostname)


def main() -> None:
    devices = ["router-1", "core-sw1", "core-sw2", "edge-sw1"]

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run_one, devices))

    print("Report:")
    for hostname, uptime in results:
        print(f"  {hostname}: {uptime}h")
```

`executor.map` returns results in the **same order** as the input `devices` list, so device order is preserved and each result is correctly paired.

## How to Spot Similar Bugs

- **Globals or shared lists/dicts written by multiple threads:** If workers write to a single list, dict, or global instead of returning a value, interleaving can cause wrong or missing data. Prefer returning from the worker and collecting via `executor.map` or `future.result()`.
- **"Result varies between runs":** Non-deterministic behavior often indicates a race. Look for shared mutable state and any assumption about order of execution.
- **One variable holding "current" work item:** Pattern of "set global, then use it" in a loop or in multiple threads is fragile; another thread can overwrite the global before it's used.

## Best Practices

1. **Return values from workers:** Have each thread (or future) compute and return its result. The main thread (or the code that submitted the work) collects results via `executor.map`, `executor.submit` + `as_completed`, or `future.result()`. No shared mutable state.
2. **Preserve order when needed:** `ThreadPoolExecutor.map` returns an iterator in the same order as the input iterable. Use it when you need a stable report order; use `as_completed` when you only need to process results as they finish.
3. **Avoid global mutable state in concurrent code:** If you must share state, use a lock (e.g. `threading.Lock`) or thread-safe structures, and document why. Prefer designs that avoid sharing.
4. **Test with multiple runs:** Run the script many times; races may only appear occasionally. If output is sometimes wrong, suspect shared state or order assumptions.
