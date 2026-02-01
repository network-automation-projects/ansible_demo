"""
Exercise: produce sprint summary from Jira search JSON (velocity, by_status, total_points).
Fill in the TODOs. See README.md for the problem description.
"""

import json
import sys
from pathlib import Path


DEFAULT_DONE_STATUSES = ["Done", "Closed", "Complete"]


def load_jira_search_response(path: Path) -> dict:
    """Read Jira search JSON from path. Return parsed dict. Handle FileNotFoundError and JSONDecodeError."""
    # TODO: open path, json.load(), return dict; handle FileNotFoundError and json.JSONDecodeError
    return {}


def sprint_summary(
    response: dict,
    done_statuses: list[str] | None = None,
    points_field: str = "customfield_10016",
) -> dict:
    """
    Return dict with total_issues, by_status, velocity, total_points.
    velocity = sum of story points for issues in done_statuses.
    """
    if done_statuses is None:
        done_statuses = DEFAULT_DONE_STATUSES
    # TODO: total_issues = len(response.get("issues", []))
    # TODO: by_status = {}: for each issue, status = fields.status.name; increment count
    # TODO: velocity = 0, total_points = 0: for each issue, pts = fields.get(points_field) or 0; total_points += pts
    # TODO: if status in done_statuses: velocity += pts
    # TODO: return {"total_issues": ..., "by_status": ..., "velocity": ..., "total_points": ...}
    return {
        "total_issues": 0,
        "by_status": {},
        "velocity": 0,
        "total_points": 0,
    }


def main() -> None:
    base = Path(__file__).parent
    fixture = base / "sprint_fixture.json"
    # TODO: use sys.argv[1] if provided, else fixture
    # TODO: response = load_jira_search_response(path)
    # TODO: summary = sprint_summary(response)
    # TODO: print summary in readable format
    pass


if __name__ == "__main__":
    main()
