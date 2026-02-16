"""
Python Network Automation - Configuration Management Exercises
"""

import argparse
import re
import logging
from typing import Any, Dict, List

import yaml
from jinja2 import Template

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def render_config_template(template_str: str, variables: Dict[str, Any]) -> str:
    """Render Jinja2 template with variables."""
    return Template(template_str).render(**variables)


def parse_yaml_config(yaml_file: str) -> Dict[str, Any]:
    """Parse YAML configuration file."""
    with open(yaml_file, "r") as f:
        return yaml.safe_load(f) or {}


def extract_ips_from_output(output: str) -> List[str]:
    """Extract IP addresses from device output using regex."""
    return re.findall(r"\d+\.\d+\.\d+\.\d+", output)


def parse_cli_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", required=True, help="Device hostname or IP")
    parser.add_argument("--config", required=True, help="Config file path")
    return parser.parse_args()


if __name__ == "__main__":
    print("Configuration Management Exercises")
