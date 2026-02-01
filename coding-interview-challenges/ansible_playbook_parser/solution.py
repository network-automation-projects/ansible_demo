"""
Ansible playbook and inventory parser: load YAML, list plays, tasks, hosts.
"""

from pathlib import Path

import yaml


def load_playbook(path: str | Path) -> list[dict]:
    """Load YAML from path; return list of plays. Single play -> [play]. Missing file -> []."""
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        if data is None:
            return []
        if isinstance(data, dict):
            return [data]
        return list(data)
    except FileNotFoundError:
        return []


def list_tasks_from_play(play: dict) -> list[str]:
    """Given one play dict, return list of task names. Flatten blocks one level; use 'unnamed' when no name."""
    tasks = play.get("tasks", [])
    names: list[str] = []
    for item in tasks:
        if not isinstance(item, dict):
            continue
        if "block" in item:
            for sub in item["block"]:
                if isinstance(sub, dict):
                    names.append(sub.get("name") or "unnamed")
        else:
            names.append(item.get("name") or "unnamed")
    return names


def load_inventory(path: str | Path) -> dict:
    """Load inventory YAML from path; return raw structure (dict). Missing file -> {}."""
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}


def list_hosts_in_group(inventory: dict, group_name: str) -> list[str]:
    """Return list of host names in the given group. Handle all.children.<group>.hosts and all.hosts."""
    all_data = inventory.get("all", {})
    if group_name == "all":
        hosts: set[str] = set()
        for child in all_data.get("children", {}).values():
            if isinstance(child, dict) and "hosts" in child:
                hosts.update(child["hosts"].keys())
        if "hosts" in all_data:
            hosts.update(all_data["hosts"].keys())
        return sorted(hosts)
    children = all_data.get("children", {})
    group = children.get(group_name)
    if isinstance(group, dict) and "hosts" in group:
        return list(group["hosts"].keys())
    if group_name and "hosts" in all_data and group_name not in children:
        return []
    return []


def main() -> None:
    base = Path(__file__).parent
    playbook_path = base / "sample_playbook.yml"
    inventory_path = base / "sample_inventory.yml"

    plays = load_playbook(playbook_path)
    for i, play in enumerate(plays):
        name = play.get("name") or f"Play {i + 1}"
        hosts = play.get("hosts", "?")
        print(f"Play: {name} (hosts: {hosts})")
        task_names = list_tasks_from_play(play)
        for tn in task_names:
            print(f"  Task: {tn}")
        print()

    inv = load_inventory(inventory_path)
    for group in ["web", "db", "all"]:
        hosts = list_hosts_in_group(inv, group)
        print(f"Group {group}: {hosts}")


if __name__ == "__main__":
    main()
