"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

import subprocess
import sys
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_terraform_command(command: str, working_dir: str = '.') -> str:
    """Run Terraform command using subprocess."""
    result = subprocess.run(
        ['terraform', command],
        cwd=working_dir,
        capture_output=True,
        text=True,
    )
    result.check_returncode()
    return result.stdout


def parse_cli_arguments() -> List[str]:
    """Parse command-line arguments using sys.argv."""
    if len(sys.argv) < 2:
        sys.exit("Usage: script.py <command>")
    return sys.argv[1:]


def execute_ansible_playbook(playbook: str, inventory: str) -> bool:
    """Execute Ansible playbook."""
    result = subprocess.run(
        ['ansible-playbook', playbook, '-i', inventory],
    )
    return result.returncode == 0


if __name__ == "__main__":
    print("10_infrastructure_as_code – answer key (run exercises.py to practice)")
