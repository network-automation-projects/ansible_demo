"""
Produce sprint summary from Jira search JSON: velocity, by_status, total_points.
"""

import json
import sys
from pathlib import Path


DEFAULT_DONE_STATUSES = ["Done", "Closed", "Complete"]


def load_jira_search_response(path: Path) -> dict:
    """Read Jira search JSON from path. Return parsed dict. Handle FileNotFoundError and JSONDecodeError."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}")
        raise


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

    issues = response.get("issues", [])
    total_issues = len(issues)
    by_status: dict[str, int] = {}
    velocity = 0
    total_points = 0

    for issue in issues:
        fields = issue.get("fields", {})
        status_obj = fields.get("status") or {}
        status = status_obj.get("name", "Unknown")
        pts = fields.get(points_field)
        pts_val = pts if pts is not None else 0

        by_status[status] = by_status.get(status, 0) + 1
        total_points += pts_val
        if status in done_statuses:
            velocity += pts_val

    return {
        "total_issues": total_issues,
        "by_status": by_status,
        "velocity": velocity,
        "total_points": total_points,
    }


def main() -> None:
    base = Path(__file__).parent
    fixture = base / "sprint_fixture.json"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else fixture

    response = load_jira_search_response(path)
    summary = sprint_summary(response)
    print("Sprint Summary")
    print("-" * 40)
    print("Total issues:", summary["total_issues"])
    print("By status:", summary["by_status"])
    print("Velocity (completed points):", summary["velocity"])
    print("Total points (committed):", summary["total_points"])


if __name__ == "__main__":
    main()
