# Drill 2: Rate Limiter Decorator

Limit a function to X calls per Y seconds.

## Requirements

**Base:**
- Decorator: `@rate_limit(calls=5, period=10)` — allow at most 5 calls per 10 seconds
- When limit exceeded, block until a slot is available (or raise, your choice; blocking is common)

**Stretch:**
- Make it thread-safe using `threading.Lock`

## Example

```python
@rate_limit(calls=2, period=1)
def api_call():
    return "ok"

# First 2 calls succeed immediately; 3rd blocks until 1 second has passed
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
