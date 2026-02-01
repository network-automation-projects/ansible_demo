"""
Parse Terraform plan JSON: load plan, summarize resource changes (add/change/destroy).
"""

import json
import sys
from pathlib import Path


def load_plan_json(path: Path) -> dict:
    """Read plan JSON from path. Return parsed dict. Handle FileNotFoundError and JSONDecodeError."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}")
        raise


def summarize_resource_changes(plan: dict) -> tuple[list[str], list[str], list[str]]:
    """
    From plan['resource_changes'], return (to_add, to_change, to_destroy).
    - to_add: actions == ['create'] only
    - to_change: 'update' in actions (and not delete)
    - to_destroy: 'delete' in actions (including replace)
    Use each change's 'address' field.
    """
    to_add: list[str] = []
    to_change: list[str] = []
    to_destroy: list[str] = []

    for rc in plan.get("resource_changes", []):
        change = rc.get("change", {})
        actions = change.get("actions", [])
        address = rc.get("address", "")

        if "delete" in actions:
            to_destroy.append(address)
        if "create" in actions and "delete" not in actions:
            to_add.append(address)
        elif "update" in actions:
            to_change.append(address)

    return (to_add, to_change, to_destroy)


def main() -> None:
    base = Path(__file__).parent
    fixture = base / "plan_fixture.json"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else fixture

    plan = load_plan_json(path)
    to_add, to_change, to_destroy = summarize_resource_changes(plan)
    print("To add:", to_add)
    print("To change:", to_change)
    print("To destroy:", to_destroy)


if __name__ == "__main__":
    main()
