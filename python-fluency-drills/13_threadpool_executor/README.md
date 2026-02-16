# Drill 13: Write a ThreadPool Executor Tool

Use `concurrent.futures.ThreadPoolExecutor` to run 10 simulated tasks, collect results, handle partial failures, and print a summary.

## Requirements

**Base:**
- Run 10 simulated tasks (e.g. each sleeps briefly, some "fail" by raising)
- Collect results (success values and exceptions)
- Handle partial failures (don't let one failure kill the batch)
- Print summary: success count, failure count, sample results

## Example

```python
# 10 tasks: 7 succeed, 3 raise
# Summary: success=7, failure=3, results=[...]
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
