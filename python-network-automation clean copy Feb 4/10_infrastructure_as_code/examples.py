"""
Python Network Automation - Infrastructure as Code Examples
"""

import subprocess
import sys
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TerraformRunner:
    """Execute Terraform commands."""
    
    def run(self, command: str, working_dir: str = '.') -> Dict[str, Any]:
        """Run Terraform command."""
        try:
            result = subprocess.run(
                ['terraform', command],
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return {'success': True, 'output': result.stdout}
        except subprocess.CalledProcessError as e:
            logger.error(f"Terraform command failed: {e.stderr}")
            return {'success': False, 'error': e.stderr}


class AnsibleRunner:
    """Execute Ansible playbooks."""
    
    def run_playbook(self, playbook: str, inventory: str) -> bool:
        """Run Ansible playbook."""
        try:
            result = subprocess.run(
                ['ansible-playbook', playbook, '-i', inventory],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("Playbook executed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Playbook failed: {e.stderr}")
            return False


if __name__ == "__main__":
    print("Infrastructure as Code Examples")
    terraform = TerraformRunner()
    result = terraform.run('init')
    print(f"Terraform init: {result['success']}")
