"""
Ansible playbook driver: run ansible-playbook from Python, parse play recap.
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
    cwd = playbook_path.parent
    return subprocess.run(
        [
            "ansible-playbook",
            str(playbook_path),
            "-i",
            str(inventory_path),
            *extra_args,
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def parse_play_recap(stdout: str) -> dict[str, dict[str, int]] | None:
    """Extract PLAY RECAP lines; return dict mapping hostname to counts or None."""
    # Match "hostname : ok=N changed=N unreachable=N failed=N skipped=N rescued=N ignored=N"
    pattern = re.compile(
        r"(\S+)\s*:\s*ok=(\d+)\s+changed=(\d+)\s+unreachable=(\d+)\s+failed=(\d+)\s+skipped=(\d+)\s+rescued=(\d+)\s+ignored=(\d+)"
    )
    recap = {}
    in_recap = False
    for line in stdout.splitlines():
        if "PLAY RECAP" in line:
            in_recap = True
            continue
        if in_recap:
            match = pattern.search(line)
            if match:
                host = match.group(1)
                recap[host] = {
                    "ok": int(match.group(2)),
                    "changed": int(match.group(3)),
                    "unreachable": int(match.group(4)),
                    "failed": int(match.group(5)),
                    "skipped": int(match.group(6)),
                    "rescued": int(match.group(7)),
                    "ignored": int(match.group(8)),
                }
    return recap if recap else None


def main() -> None:
    base = Path(__file__).parent
    minimal_dir = base / "minimal"
    playbook = minimal_dir / "playbook.yml"
    inventory = minimal_dir / "inventory.yml"

    result = run_ansible_playbook(playbook, inventory)
    if result.returncode == 0:
        print("ansible-playbook: OK")
        recap = parse_play_recap(result.stdout)
        if recap is not None:
            print("Play recap:", recap)
        else:
            print("Play recap: (could not parse)")
    else:
        print("ansible-playbook: FAILED")
        print(result.stderr or result.stdout)


if __name__ == "__main__":
    main()
