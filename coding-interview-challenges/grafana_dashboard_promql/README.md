# Grafana Dashboard PromQL Parser (Python)

Practice exercise for **Grafana + Prometheus**. Focus: read Grafana dashboard JSON and extract panel titles and their PromQL expressions. Proves understanding of how Grafana panels reference Prometheus (datasource, targets, `expr`).

## What You'll Use

- **JSON:** Load Grafana dashboard JSON from path (e.g. [go-monitor-with-grafana/grafana/dashboards/ping-monitor-dashboard.json](../../go-monitor-with-grafana/grafana/dashboards/ping-monitor-dashboard.json))
- **Dict navigation:** `dashboard["panels"]`, each `panel["targets"]`, `target["expr"]`, `panel["title"]`, datasource `type`/`uid`

## Problem

**extract_panel_promql(dashboard_path)**  
Read dashboard JSON from path. Return a list of `{"title": panel title, "expr": PromQL from first target}` for each panel that has a Prometheus target and a non-empty `expr`. Skip panels with no targets, empty targets, or non-Prometheus datasource. Use pathlib for the path.

## Files

- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).
- **fixtures/minimal_dashboard.json** – Minimal Grafana dashboard JSON with two panels (Prometheus + PromQL).

## How to Practice

1. Read this README and inspect `fixtures/minimal_dashboard.json`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py`; check the list of title/expr.
4. Compare with `solution.py`.

## Prerequisites

- Python 3.9+. Stdlib only.

## Run with real stack (optional)

Import the generated dashboard JSON (or the parsed spec) into Grafana with Prometheus as datasource. You can also run the parser against `../../go-monitor-with-grafana/grafana/dashboards/ping-monitor-dashboard.json` to see all panels and their PromQL.
