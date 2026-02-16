# Answer: Why Device Output Is Misaligned

## Root Cause

When a device "fails" (`get_uptime` returns `None`), the code **does not append** to the `uptimes` list. The `hostnames` and `uptimes` lists therefore have different lengths. The report pairs them by index (`hostnames[i]` with `uptimes[i]`), so once one device is skipped, every subsequent row is wrong.

## Why It Manifests

1. router-1: uptime 100 → append to hostnames, append 100 to uptimes. Both lists: [r1], [100].
2. router-2: uptime None → append to hostnames, **do not** append to uptimes. Lists: [r1, r2], [100].
3. router-3: uptime 360 → append to hostnames, append 360 to uptimes. Lists: [r1, r2, r3], [100, 360].

When printing:
- i=0: router-1 with uptimes[0]=100 ✓
- i=1: router-2 with uptimes[1]=360 (that's router-3's value)
- i=2: router-3 with uptimes[2] — index out of range, fallback to "failed"

## Code Fix

Always maintain a 1:1 correspondence. Append something for failures too (e.g. `None`):

```python
    for device in devices:
        hostnames.append(device)
        uptime = get_uptime(device)
        uptimes.append(uptime)  # Append None for failures too
```

Then in the report loop, handle `None`:

```python
    for i in range(len(hostnames)):
        u = uptimes[i]
        status = f"{u}h" if isinstance(u, int) else "failed"
        print(f"  {hostnames[i]}: {status}")
```

Or use a single list of `(hostname, uptime)` tuples to avoid parallel lists entirely.

## How to Spot Similar Bugs

- **Parallel lists:** When you have `list_a` and `list_b` that must stay in sync, any conditional append to only one will cause misalignment.
- **`zip` with unequal lengths:** `zip(devices, results)` truncates to the shorter list. If one list is shorter due to skipped failures, the last items are dropped.
- **Index-based pairing:** `devices[i]` and `results[i]` assume equal length. Trace what happens when one iteration skips appending.

## Best Practices

1. **One structure per device:** Use a list of dicts or dataclasses: `[{"hostname": "r1", "uptime": 100}, {"hostname": "r2", "uptime": None}, ...]`. No parallel lists.
2. **Always append:** When iterating, append a result for every item — use `None` or a failure sentinel rather than skipping.
3. **Avoid index pairing:** Prefer `for device, result in zip(devices, results)` only when you're certain lengths match, or iterate over a single list of (device, result) pairs.
