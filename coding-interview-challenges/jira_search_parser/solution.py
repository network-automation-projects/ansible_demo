"""
Parse Jira search response JSON: group by status/assignee, sum story points.
"""

import json
import sys
from pathlib import Path


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


def issues_by_status(response: dict) -> dict[str, list[str]]:
    """Return dict mapping status name to list of issue keys."""
    result: dict[str, list[str]] = {}
    for issue in response.get("issues", []):
        key = issue.get("key", "")
        fields = issue.get("fields", {})
        status_obj = fields.get("status") or {}
        status = status_obj.get("name", "Unknown")
        if status not in result:
            result[status] = []
        result[status].append(key)
    return result


def issues_by_assignee(response: dict) -> dict[str, list[str]]:
    """Return dict mapping assignee display name (or 'Unassigned') to list of issue keys."""
    result: dict[str, list[str]] = {}
    for issue in response.get("issues", []):
        key = issue.get("key", "")
        fields = issue.get("fields", {})
        assignee = fields.get("assignee")
        display = assignee.get("displayName") if assignee else "Unassigned"
        if display not in result:
            result[display] = []
        result[display].append(key)
    return result


def total_story_points(
    response: dict, points_field: str = "customfield_10016"
) -> int:
    """Sum story points across issues. Missing or null field treated as 0."""
    total = 0
    for issue in response.get("issues", []):
        fields = issue.get("fields", {})
        pts = fields.get(points_field)
        total += pts if pts is not None else 0
    return total


def main() -> None:
    base = Path(__file__).parent
    fixture = base / "search_fixture.json"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else fixture

    response = load_jira_search_response(path)
    print("By status:", issues_by_status(response))
    print("By assignee:", issues_by_assignee(response))
    print("Total story points:", total_story_points(response))


if __name__ == "__main__":
    main()
