# Drill 18: Build a Mini AI Wrapper

Function `summarize(text)` that simulates an LLM call with timeout, retry, and structured logging.

## Requirements

**Base:**
- `summarize(text: str) -> str` — simulate LLM call (return truncated/simple summary)
- Add timeout (e.g. 2 seconds)
- Retry on "failure" (mock can randomly fail)
- Structured logging (JSON logs for calls, retries, success/failure)

## Example

```python
result = summarize("Long text here...")
# Logs: {"action": "summarize", "text_len": 14, "attempt": 1, "status": "ok"}
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
