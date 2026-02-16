# Drill 14: Implement Basic Token Bucket Rate Limiter

Simulate N tokens per second. Reject calls when the bucket is empty.

## Requirements

**Base:**
- `TokenBucket(rate: float)` — rate = tokens per second
- `acquire() -> bool` — consume 1 token; return True if available, False if bucket empty
- Tokens refill at `rate` per second (simple: track last refill time, add tokens based on elapsed)

## Example

```python
bucket = TokenBucket(rate=2.0)  # 2 tokens/sec
bucket.acquire()  # True
bucket.acquire()  # True
bucket.acquire()  # False (empty)
# After 0.5s: bucket.acquire()  # True
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
