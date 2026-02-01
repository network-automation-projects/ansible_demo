# Practical: CSV Transform

Practice exercise for **automation-style** interviews. Focus: read a CSV file, filter rows by condition, add a computed column, and write a new CSV.

## What You'll Use

- **File I/O:** `open()`, or the `csv` module for reading/writing
- **Parsing:** `csv.reader` / `csv.DictReader` or manual `split(",")`
- **Lists/dicts:** filter rows, add new key/column
- **Writing:** `csv.writer` / `csv.DictWriter` or manual join

## Problem

1. **Read** a CSV file with a header row (e.g. `name,region,cost`). Assume commas don't appear inside quoted fields for simplicity, or use the `csv` module for robustness.
2. **Filter** rows by a condition (e.g. `region == "us-east"` or `cost > 100`).
3. **Add a computed column** (e.g. `cost_with_tax = cost * 1.1`, or `status = "high" if cost > 100 else "low"`).
4. **Write** the result to a new CSV file (same columns plus the new column).

## Files

- **input.csv** – Sample input (name, region, cost).
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect `input.csv`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run and check the output CSV.
4. Compare with `solution.py`.

## Example

Input: `name,region,cost` with rows like `server1,us-east,50`. Filter to `region == "us-east"`, add `cost_with_tax = cost * 1.1`. Output CSV should have columns `name,region,cost,cost_with_tax` and only us-east rows.
