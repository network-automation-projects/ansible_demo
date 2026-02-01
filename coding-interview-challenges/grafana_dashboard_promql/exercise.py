"""
Exercise: extract panel titles and PromQL expressions from Grafana dashboard JSON.
Fill in the TODOs. See README.md for the problem description.
"""

import json
from pathlib import Path


def extract_panel_promql(dashboard_path: Path) -> list[dict[str, str]]:
    """
    Read dashboard JSON from path. Return list of {"title": panel title, "expr": PromQL from first target}
    for each panel that has a Prometheus target and non-empty expr. Skip others.
    """
    # TODO: with open(dashboard_path) as f: data = json.load(f)
    # TODO: panels = data.get("panels", [])
    # TODO: for each panel: check datasource type is "prometheus"; targets = panel.get("targets", []); if not targets: continue
    # TODO: first target = targets[0]; expr = first_target.get("expr", "").strip(); if not expr: continue
    # TODO: append {"title": panel.get("title", ""), "expr": expr}
    return []


def main() -> None:
    base = Path(__file__).parent
    fixture_path = base / "fixtures" / "minimal_dashboard.json"
    # TODO: result = extract_panel_promql(fixture_path); print one per line (title: expr)
    pass


if __name__ == "__main__":
    main()
