"""
Exercise: load playbook and inventory YAML, list plays, tasks, hosts.
Fill in the TODOs. See README.md for the problem description.
"""

from pathlib import Path

import yaml  # pip install pyyaml


def load_playbook(path: str | Path) -> list[dict]:
    """Load YAML from path; return list of plays. Single play -> [play]. Missing file -> [] or raise."""
    # TODO: open path, yaml.safe_load; if result is dict then return [result], else return result (list)
    # TODO: handle FileNotFoundError: return [] or raise
    return []


def list_tasks_from_play(play: dict) -> list[str]:
    """Given one play dict, return list of task names. Flatten blocks one level; use 'unnamed' when no name."""
    # TODO: tasks = play.get("tasks", [])
    # TODO: names = []; for each item: if dict with "block", extend with names from block items; else append task.get("name", "unnamed")
    return []


def load_inventory(path: str | Path) -> dict:
    """Load inventory YAML from path; return raw structure (dict). Missing file -> {} or raise."""
    # TODO: open path, yaml.safe_load; return dict or {}
    # TODO: handle FileNotFoundError
    return {}


def list_hosts_in_group(inventory: dict, group_name: str) -> list[str]:
    """Return list of host names in the given group. Handle all.children.<group>.hosts and all.hosts."""
    # TODO: all_data = inventory.get("all", {})
    # TODO: if group_name == "all": collect hosts from all_data.get("children", {}).values() and all_data.get("hosts", {}); return sorted unique
    # TODO: else: group = all_data.get("children", {}).get(group_name) or all_data.get("hosts") if group_name else None; return list(hosts.keys()) if group and "hosts" in group else list(group.keys()) if isinstance(group, dict) else []
    # Simpler: children = all_data.get("children", {}); group = children.get(group_name); if group and "hosts" in group: return list(group["hosts"].keys()); also check all_data.get("hosts") for top-level hosts
    return []


def main() -> None:
    base = Path(__file__).parent
    playbook_path = base / "sample_playbook.yml"
    inventory_path = base / "sample_inventory.yml"

    # TODO: plays = load_playbook(playbook_path); for each play print name/hosts, then list_tasks_from_play(play)
    # TODO: inv = load_inventory(inventory_path); for group in ["web", "db", "all"] print list_hosts_in_group(inv, group)
    pass


if __name__ == "__main__":
    main()
