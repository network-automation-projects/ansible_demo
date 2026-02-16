# Drill 12: Write a Custom Exception Hierarchy

Create `AutomationError`, `ValidationError`, `ExecutionError` and use them meaningfully.

## Requirements

**Base:**
- `AutomationError` — base for automation failures
- `ValidationError(AutomationError)` — invalid input/config
- `ExecutionError(AutomationError)` — runtime failure (e.g. device unreachable)
- Use them in a small example (e.g. validate config, run task)

## Example

```python
def validate(config):
    if "host" not in config:
        raise ValidationError("Missing host")
def run(config):
    # simulate failure
    raise ExecutionError("Device unreachable")
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
