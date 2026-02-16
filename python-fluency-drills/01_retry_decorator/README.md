# Drill 1: Retry Decorator

Write a decorator that retries a function on exception.

## Requirements

**Base:**
- `@retry(max_attempts=3, delay=1)` — decorator with configurable max attempts and delay
- Retry the function when it raises an exception
- Stop after `max_attempts` attempts
- Re-raise the final exception if all attempts fail

**Stretch:**
- Add exponential backoff (delay doubles each retry: 1s, 2s, 4s, ...)

## Example

```python
@retry(max_attempts=3, delay=0.1)
def flaky_api():
    # Simulated flaky call
    raise ConnectionError("Temporary failure")

# After 3 attempts, ConnectionError is re-raised
```

## Files

- **exercise.py** — Skeleton with TODOs; implement the logic yourself first.
- **solution.py** — Reference solution (uses ParamSpec/TypeVar for full type preservation).
- **simple/** — Variant without ParamSpec/TypeVar; uses `Callable[..., Any]` instead.
