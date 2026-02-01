# Jira Sprint Report Generator

Practice exercise for **Jira + Python** sprint reporting. Focus: produce a sprint summary from Jira search JSON—velocity (completed story points), breakdown by status, and total committed points. No live Jira required; uses fixture JSON only.

## What You'll Use

- **json:** `json.load()` to read search response from file
- **pathlib:** `Path` for file paths
- **Dict navigation:** `response["issues"]`, `issue["fields"]["status"]["name"]`, `customfield_10016` (Story Points)
- **Status categories:** Treat statuses like "Done", "Closed", "Complete" as "done" for velocity calculation

## Problem

1. **load_jira_search_response(path)**  
   Read the JSON file at `path`. Return the parsed dict. Handle `FileNotFoundError` and `json.JSONDecodeError` (same pattern as the Jira search parser exercise).

2. **sprint_summary(response, done_statuses=None)**  
   Return a dict with:
   - **total_issues:** count of issues
   - **by_status:** dict mapping status name to count (e.g. `{"Done": 2, "In Progress": 1, "To Do": 1}`)
   - **velocity:** sum of story points for issues whose status is in `done_statuses` (default `["Done", "Closed", "Complete"]`)
   - **total_points:** sum of all story points (committed scope). Treat missing or null as 0.
   Use `customfield_10016` for story points (Jira Software default).

3. **main()**  
   Load `sprint_fixture.json` (or path from CLI). Call `sprint_summary` and print the result in a readable format.

## Files

- **sprint_fixture.json** – Sprint search response with Story/Bug mix, varying statuses and story points.
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect `sprint_fixture.json`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python solution.py`; check the printed sprint summary.
4. Compare with `solution.py`.

## Prerequisites

- No external dependencies. Stdlib only: `json`, `pathlib`, optionally `sys`.

## Example Output

Given the fixture (6 issues, mix of Done/Closed/Complete/In Progress/To Do):
- `total_issues`: 6
- `by_status`: counts per status
- `velocity`: 13 (points from Done, Closed, Complete)
- `total_points`: 24 (sum of all story points)
