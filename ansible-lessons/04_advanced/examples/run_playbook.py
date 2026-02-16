#!/usr/bin/env python3
"""
Run ansible-playbook from Python and print return code and recap snippet.
Demo for ansible-lessons 04_advanced. Run from 04_advanced directory:
  python examples/run_playbook.py
"""
import re
import subprocess
from pathlib import Path
from typing import Optional

def run_playbook(playbook_path: Path, inventory_path: Path, cwd: Path) -> subprocess.CompletedProcess:
    """Run ansible-playbook with -i inventory; cwd = directory containing playbook."""
    result = subprocess.run(
        ["ansible-playbook", str(playbook_path), "-i", str(inventory_path)],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result

def parse_recap(text: str) -> Optional[str]:
    """Extract PLAY RECAP line or last summary line from playbook output."""
    if not text:
        return None
    # PLAY RECAP line often looks like "localhost : ok=2 changed=0 ..."
    match = re.search(r"(\S+\s*:\s*ok=\d+.*?failed=\d+)", text)
    if match:
        return match.group(1).strip()
    return None

def main() -> None:
    base = Path(__file__).resolve().parent
    playbook = base / "playbook.yml"
    inventory = base / "inventory.yml"
    if not playbook.exists() or not inventory.exists():
        print("Playbook or inventory not found in", base)
        return
    result = run_playbook(playbook, inventory, base)
    print("Return code:", result.returncode)
    output = result.stdout or result.stderr or ""
    recap = parse_recap(output)
    if recap:
        print("Recap:", recap)
    else:
        print("(No recap line found; last 3 lines below)")
        for line in output.strip().split("\n")[-3:]:
            print(line)

if __name__ == "__main__":
    main()
