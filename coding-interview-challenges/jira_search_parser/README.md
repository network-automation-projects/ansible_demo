# Jira Search Response Parser

Practice exercise for **Jira + Python** integration. Focus: parse Jira REST API search response JSON (from `/rest/api/3/search` or a fixture), navigate nested `issues` and `fields`, group by status and assignee, and sum story points.

## What You'll Use

- **json:** `json.load()` to read search response from file
- **pathlib:** `Path` for file paths
- **Dict navigation:** `response["issues"]`, `issue["fields"]["status"]["name"]`, `issue["fields"]["assignee"]`, optional `customfield_10016` (Story Points)
- **collections.defaultdict** or plain dicts for grouping

## Problem

1. **load_jira_search_response(path)**  
   Read the JSON file at `path`. Return the parsed dict. Handle `FileNotFoundError` (re-raise) and invalid JSON (`json.JSONDecodeError`; print message, re-raise).

2. **issues_by_status(response)**  
   From the response's `issues` list, group issue keys by status name. Return a dict mapping status to list of keys, e.g. `{"To Do": ["DEV-1", "DEV-3"], "In Progress": ["DEV-2"], "Done": ["DEV-4"]}`.

3. **issues_by_assignee(response)**  
   Group issue keys by assignee display name. If `assignee` is `null`, use `"Unassigned"`. Return e.g. `{"Alice": ["DEV-1", "DEV-4"], "Bob": ["DEV-2", "DEV-5"], "Unassigned": ["DEV-3"]}`.

4. **total_story_points(response, points_field="customfield_10016")**  
   Sum story points across all issues. Use `points_field` as the key (default `customfield_10016` for Jira Software). If the field is missing or `null`, treat as 0.

5. **main()**  
   Load `search_fixture.json` (or a path from CLI if provided). Print the results of `issues_by_status`, `issues_by_assignee`, and `total_story_points`.

## Files

- **search_fixture.json** – Minimal Jira search response (5 issues, mix of statuses, assignees, story points). Structure matches the [Jira search API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/).
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect `search_fixture.json`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py`; check the printed output.
4. Compare with `solution.py`.

## Prerequisites

- No external dependencies. Stdlib only: `json`, `pathlib`, optionally `collections`, `sys`.

## Example Output

Given the fixture:
- `issues_by_status`: `{"To Do": ["DEV-1", "DEV-3"], "In Progress": ["DEV-2", "DEV-5"], "Done": ["DEV-4"]}`
- `issues_by_assignee`: `{"Alice": ["DEV-1", "DEV-4"], "Bob": ["DEV-2", "DEV-5"], "Unassigned": ["DEV-3"]}`
- `total_story_points`: `18` (3+5+2+8+0)
