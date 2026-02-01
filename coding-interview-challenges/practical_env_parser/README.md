# Practical: Env / .env Parser

Practice exercise for **automation-style** interviews. Focus: read a `.env`-style file, parse KEY=value pairs into a dict, skip comments and blank lines, and handle bad lines gracefully.

## What You'll Use

- **File I/O:** `open()`, iterating over lines
- **String parsing:** `strip()`, `startswith("#")`, split on first `=`
- **Dict:** build key → value mapping
- **Error handling:** optional validation (e.g. key format); skip or flag bad lines

## Problem

1. **Read** a file where each line is either:
   - Blank (skip)
   - A comment starting with `#` (skip)
   - A line of the form `KEY=value` (leading/trailing spaces allowed; value may contain `=`)
2. **Parse** into a dict: keys and values stripped of surrounding whitespace. Use only the **first** `=` to split (so `KEY=value=extra` → key `KEY`, value `value=extra`).
3. **Handle bad lines:** If a line has no `=`, skip it or add a sentinel value; your choice. Empty key after strip can be skipped.

## Files

- **.env.example** – Sample input (comments, blanks, KEY=value lines).
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect `.env.example`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run and check the returned dict.
4. Compare with `solution.py`.

## Example

For a file containing:
```
# config
APP_NAME=myapp
DEBUG=true
SECRET_KEY=abc=def
```
`load_env(path)` should return `{"APP_NAME": "myapp", "DEBUG": "true", "SECRET_KEY": "abc=def"}` (comment and blanks omitted).
