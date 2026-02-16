# Drill 9: Write a Log Parser

Parse a log file and return error count, most common user, and status distribution.

## Requirements

**Base:**
- Log format: `LEVEL user=N code=N` (e.g. `ERROR user=12 code=500`)
- Return:
  - Error count (lines with LEVEL=ERROR)
  - Most common user (user= value that appears most)
  - Status distribution (count of each code value)

## Example

```
ERROR user=12 code=500
INFO user=9 code=200
ERROR user=12 code=500
```

Result: `{"error_count": 2, "most_common_user": "12", "status_distribution": {"500": 2, "200": 1}}`

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
