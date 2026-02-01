"""
Exercise: run ansible-playbook from Python, parse play recap.
Fill in the TODOs. See README.md for the problem description.
"""

import re
import subprocess
from pathlib import Path


def run_ansible_playbook(
    playbook_path: Path,
    inventory_path: Path,
    *extra_args: str,
) -> subprocess.CompletedProcess:
    """Run ansible-playbook with -i inventory_path and optional args; cwd=playbook dir. Return CompletedProcess."""
    # TODO: cwd = playbook_path.parent
    # TODO: subprocess.run(["ansible-playbook", str(playbook_path), "-i", str(inventory_path), *extra_args], cwd=cwd, capture_output=True, text=True)
    raise NotImplementedError("TODO: implement run_ansible_playbook")


def parse_play_recap(stdout: str) -> dict[str, dict[str, int]] | None:
    """Extract PLAY RECAP lines; return dict mapping hostname to {ok, changed, unreachable, failed, skipped, rescued, ignored} or None."""
    # TODO: find lines after "PLAY RECAP ***" matching "hostname : ok=N changed=N ..."
    # TODO: regex for "(\S+)\s*:\s*ok=(\d+)\s+changed=(\d+)\s+unreachable=(\d+)\s+failed=(\d+)\s+skipped=(\d+)\s+rescued=(\d+)\s+ignored=(\d+)"
    # TODO: return {"host": {"ok": int, "changed": int, ...}} or {} / None if no recap
    return None


def main() -> None:
    base = Path(__file__).parent
    minimal_dir = base / "minimal"
    playbook = minimal_dir / "playbook.yml"
    inventory = minimal_dir / "inventory.yml"

    # TODO: run ansible-playbook with playbook and inventory (e.g. no extra args, or -v)
    # TODO: print success/failure (returncode == 0)
    # TODO: if success, parse_play_recap(stdout) and print recap
    pass


if __name__ == "__main__":
    main()
