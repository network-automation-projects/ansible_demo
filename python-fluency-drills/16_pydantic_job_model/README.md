# Drill 16: Write a Pydantic Model with Nested Validation

Create a `Job` model with field validators and custom validation rules.

## Requirements

**Base:**
- `Job` model: `id: str`, `retries: int`, `metadata: dict`
- Field validators: `retries` in 0–5, `metadata` keys must be strings
- Custom validation: e.g. `id` must be non-empty

## Example

```python
Job(id="j1", retries=2, metadata={"env": "prod"})  # ok
Job(id="", retries=2, metadata={})  # ValidationError
Job(id="j1", retries=10, metadata={})  # ValidationError (retries > 5)
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.

## Dependencies

```bash
pip install pydantic
```
