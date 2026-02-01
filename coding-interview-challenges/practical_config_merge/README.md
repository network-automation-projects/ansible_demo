# Practical: Config Merge or Diff

Practice exercise for **automation-style** interviews. Focus: read two simple key=value config files, merge them (second file wins for overlapping keys), or report which keys differ.

## What You'll Use

- **File I/O:** `open()`, iterating over lines
- **Dicts:** load each file into key → value; merge with second overwriting first
- **Set operations:** optional diff (keys only in A, only in B, in both with same/different value)
- **Error handling:** missing file, empty file

## Problem

1. **Load config:** Read a file where each non-blank, non-comment line is `KEY=value`. Return a dict (same rules as env parser: first `=` splits key and value, strip both).
2. **Merge:** Given two file paths, load both configs and merge into one dict. If a key exists in both, the **second** file's value wins.
3. **Diff (optional):** Given two config dicts, return:
   - Keys only in first
   - Keys only in second
   - Keys in both with different values

## Files

- **config_a.txt** – First config (key=value lines).
- **config_b.txt** – Second config (overrides for merge).
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect the sample config files.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run and check merged result and/or diff output.
4. Compare with `solution.py`.

## Example

config_a: `HOST=localhost` and `PORT=8080`. config_b: `PORT=9090` and `DEBUG=true`.  
Merge: `{"HOST": "localhost", "PORT": "9090", "DEBUG": "true"}`.  
Diff: only_in_a = `{"HOST"}`, only_in_b = `{"DEBUG"}`, different = `{"PORT"}`.
