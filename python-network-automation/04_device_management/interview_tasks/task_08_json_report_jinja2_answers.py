"""
Task 08: JSON report and Jinja2 config generation — full solution.
No device connection; no input files required.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Template

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def output_report_json(results: List[Dict[str, Any]], path: Path) -> None:
    """Write results to JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    logger.info("Report written: %s", path)


def render_config_jinja2(template_str: str, variables: Dict[str, Any]) -> str:
    """Render Jinja2 template with variables."""
    return Template(template_str).render(**variables)


def main() -> None:
    report_path = Path("report.json")
    sample = [{"hostname": "switch1", "down_count": 2}]
    output_report_json(sample, report_path)
    template_str = "interface {{ name }}\n description {{ description }}\n"
    rendered = render_config_jinja2(template_str, {"name": "Gi0/4", "description": "from-jinja"})
    logger.info("Rendered: %s", rendered.strip())
    print("Done.")


if __name__ == "__main__":
    main()
