"""
Exercise: load Terraform plan JSON, summarize resource changes (add/change/destroy).
Fill in the TODOs. See README.md for the problem description.
"""

import copy
import json
from pathlib import Path
from webbrowser import get


def load_plan_json(path: Path) -> dict:
    """Read plan JSON from path. Return parsed dict. Handle FileNotFoundError and JSONDecodeError."""
    # TODO: open path, json.load(), return dict
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}")
        raise
    # TODO: on FileNotFoundError: re-raise or print and return {}
    # TODO: on json.JSONDecodeError: print message, re-raise or return {}


def summarize_resource_changes(plan: dict) -> tuple[list[str], list[str], list[str]]:
    """
    From plan['resource_changes'], return (to_add, to_change, to_destroy).
    - to_add: actions == ['create']
    - to_change: 'update' in actions (and not delete)
    - to_destroy: 'delete' in actions (including replace)
    Use each change's 'address' field.
    """
    to_add: list[str] = []
    to_change: list[str] = []
    to_destroy: list[str] = []
    # TODO: for each rc in plan.get("resource_changes", []): actions = rc.get("change", {}).get("actions", [])
        
    # TODO: address = rc.get("address", ""); if "create" in actions and "delete" not in actions: to_add.append(address)
    # TODO: elif "update" in actions: to_change.append(address); elif "delete" in actions: to_destroy.append(address)

    for rc in plan.get("resource_changes", []): 
        actions = rc.get("actions", {})
        change = change.get("change", {})
        address = rc.get("address", "")
        if "create" in actions and "delete" not in actions:
            to_add.append(address)
        elif "update" in actions:
            to_change.append(address)
        elif "delete" in actions:
            to_destroy.append(address)


    return (to_add, to_change, to_destroy)


def main() -> None:
    base = Path(__file__).parent
    fixture = base / "plan_fixture.json"
    # TODO: optional: use sys.argv[1] if provided, else fixture
    # TODO: plan = load_plan_json(path); to_add, to_change, to_destroy = summarize_resource_changes(plan)
    # TODO: print("To add:", to_add); print("To change:", to_change); print("To destroy:", to_destroy)
    pass


if __name__ == "__main__":
    main()



#CLEAN copy
# 
# """
# Exercise: load Terraform plan JSON, summarize resource changes (add/change/destroy).
# Fill in the TODOs. See README.md for the problem description.
# """

# import json
# from pathlib import Path


# def load_plan_json(path: Path) -> dict:
#     """Read plan JSON from path. Return parsed dict. Handle FileNotFoundError and JSONDecodeError."""
#     # TODO: open path, json.load(), return dict
#     # TODO: on FileNotFoundError: re-raise or print and return {}
#     # TODO: on json.JSONDecodeError: print message, re-raise or return {}
#     return {}


# def summarize_resource_changes(plan: dict) -> tuple[list[str], list[str], list[str]]:
#     """
#     From plan['resource_changes'], return (to_add, to_change, to_destroy).
#     - to_add: actions == ['create']
#     - to_change: 'update' in actions (and not delete)
#     - to_destroy: 'delete' in actions (including replace)
#     Use each change's 'address' field.
#     """
#     to_add: list[str] = []
#     to_change: list[str] = []
#     to_destroy: list[str] = []
#     # TODO: for each rc in plan.get("resource_changes", []): actions = rc.get("change", {}).get("actions", [])
#     # TODO: address = rc.get("address", ""); if "create" in actions and "delete" not in actions: to_add.append(address)
#     # TODO: elif "update" in actions: to_change.append(address); elif "delete" in actions: to_destroy.append(address)
#     return (to_add, to_change, to_destroy)


# def main() -> None:
#     base = Path(__file__).parent
#     fixture = base / "plan_fixture.json"
#     # TODO: optional: use sys.argv[1] if provided, else fixture
#     # TODO: plan = load_plan_json(path); to_add, to_change, to_destroy = summarize_resource_changes(plan)
#     # TODO: print("To add:", to_add); print("To change:", to_change); print("To destroy:", to_destroy)
#     pass


# if __name__ == "__main__":
#     main()
