# Drill 6: Write a Context Manager

Create a timer context manager that prints execution time.

## Requirements

**Base:**
- `with timer(): do_something()` — prints execution time on exit
- Use `contextlib.contextmanager` or a class

**Stretch:**
- Rewrite using a class (implementing `__enter__` and `__exit__`) instead of `@contextmanager`

## Example

```python
with timer():
    time.sleep(0.1)
# Prints: "Elapsed: 0.10s"
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution (include both implementations).
