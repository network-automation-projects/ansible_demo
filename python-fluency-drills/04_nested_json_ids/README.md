# Drill 4: Parse and Transform Nested JSON

Extract all keys named `"id"` from deeply nested JSON and return a flat list of IDs.

## Requirements

**Base:**
- Given deeply nested JSON (dicts, lists, arbitrary depth)
- Extract every value for keys named `"id"` (case-sensitive)
- Return a flat list of IDs (preserve order of first occurrence)
- No external libraries (stdlib only)

## Example

```python
data = {"id": "a", "nested": {"id": "b", "items": [{"id": "c"}]}}
extract_ids(data)  # ["a", "b", "c"]
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
