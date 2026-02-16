# Drill 1: Retry Decorator (Simple — no ParamSpec/TypeVar)

Same retry decorator as the main drill, but using simplified type hints:
`Callable[..., Any]` instead of `ParamSpec` and `TypeVar`.

Use this variant if you prefer simpler typing or are on Python < 3.10.

## Requirements

**Base:**
- `@retry(max_attempts=3, delay=1)` — decorator with configurable max attempts and delay
- Retry the function when it raises an exception
- Stop after `max_attempts` attempts
- Re-raise the final exception if all attempts fail

**Stretch:**
- Add exponential backoff (delay doubles each retry: 1s, 2s, 4s, ...)

## Files

- **exercise.py** — Skeleton with TODOs; implement the logic yourself first.
- **solution.py** — Reference solution (simplified typing).

## Production alternatives

Same retry concept, using standard libraries:

- **retry_with_requests.py** — HTTP retries via `urllib3.Retry` + `HTTPAdapter`. Use when making HTTP calls.
- **retry_with_tenacity.py** — General-purpose retries via `tenacity`. Use for any callable (HTTP, DB, file I/O, etc.).
