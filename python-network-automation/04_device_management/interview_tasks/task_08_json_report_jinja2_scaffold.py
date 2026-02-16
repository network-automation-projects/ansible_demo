"""
INTERVIEW PROMPT (about 25 min)
-------------------------------
Write a function to output a list of result dicts to a JSON file (e.g. for
reports). Also implement a function that renders a Jinja2 template with given
variables (e.g. for generating interface config snippets). No device connection.
Assume you have the data to write and the template string; no supporting files
unless provided.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Template

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# --- Step 1: I'm going to write the results list to a JSON file. ---
def output_report_json(results: List[Dict[str, Any]], path: Path) -> None:
    """Write results to JSON file."""
    # TODO: path.parent.mkdir(parents=True, exist_ok=True)
    # TODO: path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    raise NotImplementedError("Step 1: json.dumps and write to path")


# --- Step 2: Next I'm going to render a Jinja2 template with the given variables. ---
def render_config_jinja2(template_str: str, variables: Dict[str, Any]) -> str:
    """Render Jinja2 template with variables."""
    # TODO: return Template(template_str).render(**variables)
    raise NotImplementedError("Step 2: Jinja2 Template(...).render(**variables)")


# --- Step 3: main() — write sample report to JSON, render a template (no input files). ---
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
