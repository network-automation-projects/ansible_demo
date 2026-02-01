"""
Grafana dashboard PromQL parser: extract panel titles and PromQL expressions.
"""

import json
from pathlib import Path


def _is_prometheus_panel(panel: dict) -> bool:
    """True if panel uses Prometheus datasource."""
    ds = panel.get("datasource") or {}
    if isinstance(ds, str):
        return False
    return ds.get("type") == "prometheus"


def extract_panel_promql(dashboard_path: Path) -> list[dict[str, str]]:
    """
    Read dashboard JSON from path. Return list of {"title": panel title, "expr": PromQL from first target}
    for each panel that has a Prometheus target and non-empty expr.
    """
    with open(dashboard_path) as f:
        data = json.load(f)
    panels = data.get("panels", [])
    result: list[dict[str, str]] = []
    for panel in panels:
        if not _is_prometheus_panel(panel):
            continue
        targets = panel.get("targets", [])
        if not targets:
            continue
        first_target = targets[0]
        expr = (first_target.get("expr") or "").strip()
        if not expr:
            continue
        result.append({
            "title": panel.get("title", ""),
            "expr": expr,
        })
    return result


def main() -> None:
    base = Path(__file__).parent
    fixture_path = base / "fixtures" / "minimal_dashboard.json"
    result = extract_panel_promql(fixture_path)
    for item in result:
        print(f"{item['title']}: {item['expr']}")


if __name__ == "__main__":
    main()
