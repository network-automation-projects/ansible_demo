# Drill 3: Simple CLI Tool

Build a CLI tool using argparse that loads JSON, replaces keys, and saves with backup.

## Requirements

**Base:**
- Command: `python tool.py --file config.json --replace foo=bar --replace baz=qux`
- Load JSON from `--file`
- Replace matching keys with values from `--replace key=value` (can appear multiple times)
- Save file safely: write to temp, then atomic rename (or create backup before overwrite)

## Example

```bash
python tool.py --file config.json --replace host=localhost --replace port=8080
```

Input `config.json`: `{"host": "old", "port": 3000}`  
Output: `{"host": "localhost", "port": 8080}` with `config.json.bak` backup.

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.
