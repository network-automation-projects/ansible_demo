# Drill 17: Write a Simple Background Worker

Using `asyncio.create_task` or threading: task submission and status polling.

## Requirements

**Base:**
- Submit tasks (e.g. callable or coroutine)
- Run in background (asyncio task or thread)
- `get_status(task_id)` — return "pending", "running", "done", "failed"
- Simulate: submit 3 tasks, poll status until all done

## Example

```python
worker = BackgroundWorker()
worker.submit(slow_task)
worker.submit(another_task)
while not worker.all_done():
    print(worker.get_status(...))
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
