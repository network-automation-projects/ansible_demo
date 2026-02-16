# Drill 11: Implement Exponential Backoff Function

Implement `backoff(base_delay, attempt)` and optionally add jitter.

## Requirements

**Base:**
- `backoff(base_delay: float, attempt: int) -> float`
- Return `base_delay * 2 ** attempt`

**Stretch:**
- Add jitter (random variation to avoid thundering herd)

## Example

```python
backoff(1.0, 0)  # 1.0
backoff(1.0, 1)  # 2.0
backoff(1.0, 2)  # 4.0
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
