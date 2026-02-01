# Practical: Parse a Log File

Practice exercise for **automation-style** interviews. Focus: read a text file, parse lines into structured records, filter by level, and produce simple counts.

## What You'll Use

- **File I/O:** `open()`, iterating over lines
- **String parsing:** `split()` or `re` to extract timestamp, level, message
- **Dicts/lists:** list of parsed records; counting by level
- **Error handling:** `try/except` for missing file; skip or flag malformed lines

## Problem

1. **Read** a log file where each line has the format: `YYYY-MM-DD HH:MM:SS LEVEL Message text`
   - Example: `2025-01-29 10:00:00 INFO Server started`
2. **Parse** each line into a dict with keys: `timestamp`, `level`, `message`. Skip blank lines. If a line doesn't match the format, either skip it or set `level` to `"UNKNOWN"`.
3. **Filter** by log level: given a level (e.g. `"ERROR"`), return only entries with that level.
4. **Count by level:** Return a dict mapping each level to the number of entries (e.g. `{"INFO": 5, "ERROR": 2}`).

## Files

- **sample.log** – Sample input (mixed INFO, WARN, ERROR lines).
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect `sample.log`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run against `sample.log`; check parsed output and counts.
4. Compare with `solution.py`.

## Example

For a file with 3 INFO lines and 2 ERROR lines, `count_by_level(records)` might return `{"INFO": 3, "ERROR": 2}`.
