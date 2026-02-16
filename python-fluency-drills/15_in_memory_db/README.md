# Drill 15: Build a Minimal In-Memory Database

Class with `insert()`, `update()`, `delete()`, `query()` backed by a dict. Add simple filtering.

## Requirements

**Base:**
- `insert(record: dict)` — add record, assign id
- `update(id, **kwargs)` — update record by id
- `delete(id)` — remove record
- `query(**filters)` — return records matching filters (e.g. `query(status="active")`)

## Example

```python
db = InMemoryDB()
db.insert({"name": "a", "status": "active"})
db.insert({"name": "b", "status": "inactive"})
db.query(status="active")  # [{"id": 1, "name": "a", "status": "active"}]
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
