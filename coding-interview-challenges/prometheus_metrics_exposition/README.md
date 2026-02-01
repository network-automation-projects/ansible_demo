# Prometheus Metrics Exposition (Python)

Practice exercise for **Prometheus + Python**. Focus: expose Counter, Gauge, and Histogram metrics using `prometheus_client`, optionally serve `/metrics`, and parse Prometheus text exposition format.

## What You'll Use

- **prometheus_client:** `Counter`, `Gauge`, `Histogram` with names and optional labels
- **prometheus_client:** `start_http_server(port)` and/or `generate_latest(REGISTRY)` to produce `/metrics` text
- **String parsing (optional):** Parse Prometheus text format (metric name, labels, value) from a given string

## Problem

1. **register_app_metrics()**  
   Register and return (or use module-level) metrics: one Counter (e.g. `app_requests_total`), one Gauge (e.g. `app_active_tasks`), one Histogram (e.g. `app_request_duration_seconds`). Use `prometheus_client`; add a label like `service="demo"` if desired.

2. **serve_metrics(port)**  
   Start the HTTP server for the default registry on `port` (e.g. 8000) so `/metrics` is served. Use `start_http_server(port)`. Optionally run in a thread so `main()` can also demonstrate `generate_latest` without blocking.

3. **parse_metrics_text(metrics_str)**  
   Given a string of Prometheus exposition format (as returned by `/metrics` or `generate_latest()`), parse it into a list of tuples or dicts: `(metric_name, labels_dict, value)`. Handle `# TYPE` and `# HELP` by ignoring or storing; focus on lines that are `name{label="val"} value` or `name value`. Return a simple list of parsed samples (name, labels, float value).

4. **main()**  
   Register metrics, optionally increment counter/gauge/set histogram once, then call `generate_latest()` and pass the result to `parse_metrics_text` and print a short summary. Prefer this path so the exercise runs and validates without keeping a server running.

## Files

- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).
- **requirements.txt** – `prometheus_client>=0.19.0`.

## How to Practice

1. Read this README and install dependencies: `pip install -r requirements.txt`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py` from this directory; check parsed metrics summary.
4. Compare with `solution.py`.

## Prerequisites

- Python 3.9+. `pip install prometheus_client`.

## Run with real stack (optional)

To see metrics in Prometheus: run the app with `serve_metrics(8000)` (e.g. in a thread), add a scrape config for `localhost:8000` in Prometheus, then open Prometheus UI and query the metric names.
