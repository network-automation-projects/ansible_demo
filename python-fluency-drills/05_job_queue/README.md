# Drill 5: Build a Simple Job Queue

Write a `JobQueue` class that manages jobs with success, failure, and retry tracking.

## Requirements

**Base:**
- `JobQueue` class with:
  - `add_job(self, job)` — add a job (job can be a callable or dict with `"task"` key)
  - `run_next(self)` — run the next job; return result or raise
- Jobs can fail (raise exception)
- Track: success count, failure count, retry count per job (optional: retry failed jobs)

## Example

```python
queue = JobQueue()
queue.add_job(lambda: 1 + 1)
queue.add_job(lambda: 1 / 0)  # fails
queue.run_next()  # 2
queue.run_next()  # raises ZeroDivisionError
# queue.stats() -> {"success": 1, "failure": 1}
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
