# Drill 10: Build a Basic REST Client

Using requests: retry on 500, timeout 3 seconds, structured JSON logging.

## Requirements

**Base:**
- Function `fetch(url: str) -> requests.Response` (or return dict/bytes)
- Retry on 500 status (e.g. up to 3 attempts with short delay)
- Timeout after 3 seconds
- Log structured JSON (e.g. `{"url": "...", "status": 200, "attempt": 1}`)

## Example

```python
result = fetch("https://httpbin.org/status/200")
# Logs: {"url": "https://...", "status": 200, "attempt": 1}
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.

## Dependencies

```bash
pip install requests
```
