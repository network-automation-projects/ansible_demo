"""
Exercise: parse Jira search response JSON, group by status/assignee, sum story points.
Fill in the TODOs. See README.md for the problem description.
"""

import json
import sys
from pathlib import Path


def load_jira_search_response(path: Path) -> dict:
    """Read Jira search JSON from path. Return parsed dict. Handle FileNotFoundError and JSONDecodeError."""
    # TODO: open path, json.load(), return dict
    # TODO: on FileNotFoundError: re-raise
    # TODO: on json.JSONDecodeError: print message, re-raise
    return {}


def issues_by_status(response: dict) -> dict[str, list[str]]:
    """Return dict mapping status name to list of issue keys."""
    # TODO: for each issue in response.get("issues", []): key = issue.get("key"), status = issue.get("fields", {}).get("status", {}).get("name")
    # TODO: append key to list for that status; return dict
    return {}


def issues_by_assignee(response: dict) -> dict[str, list[str]]:
    """Return dict mapping assignee display name (or 'Unassigned') to list of issue keys."""
    # TODO: for each issue: assignee = fields.get("assignee"); display = assignee.get("displayName") if assignee else "Unassigned"
    # TODO: append key to list for that assignee; return dict
    return {}


def total_story_points(
    response: dict, points_field: str = "customfield_10016"
) -> int:
    """Sum story points across issues. Missing or null field treated as 0."""
    # TODO: for each issue: pts = issue.get("fields", {}).get(points_field); add pts if pts is not None else 0
    return 0


def main() -> None:
    base = Path(__file__).parent
    fixture = base / "search_fixture.json"
    # TODO: use sys.argv[1] if provided, else fixture
    # TODO: response = load_jira_search_response(path)
    # TODO: print issues_by_status, issues_by_assignee, total_story_points
    pass


if __name__ == "__main__":
    main()
