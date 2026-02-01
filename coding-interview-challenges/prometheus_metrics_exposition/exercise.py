"""
Exercise: expose Prometheus metrics from Python, optionally serve /metrics, parse exposition format.
Fill in the TODOs. See README.md for the problem description.
"""

import re
from typing import Any

# TODO: from prometheus_client import Counter, Gauge, Histogram, REGISTRY, start_http_server, generate_latest


def register_app_metrics() -> dict[str, Any]:
    """Register Counter, Gauge, Histogram; return dict with refs or use module-level. Optional label service='demo'."""
    # TODO: counter = Counter('app_requests_total', 'Total requests', ['service']); counter.labels(service='demo').inc(0)
    # TODO: gauge = Gauge('app_active_tasks', 'Active tasks', ['service']); gauge.labels(service='demo').set(0)
    # TODO: histogram = Histogram('app_request_duration_seconds', 'Request duration', ['service']); histogram.labels(service='demo').observe(0.1)
    # TODO: return {"counter": counter, "gauge": gauge, "histogram": histogram} or similar
    raise NotImplementedError("TODO: implement register_app_metrics")


def serve_metrics(port: int) -> None:
    """Start HTTP server for default registry on port so /metrics is served."""
    # TODO: start_http_server(port)
    raise NotImplementedError("TODO: implement serve_metrics")


def parse_metrics_text(metrics_str: str) -> list[tuple[str, dict[str, str], float]]:
    """
    Parse Prometheus exposition format into list of (metric_name, labels_dict, value).
    Ignore # TYPE and # HELP. Handle name{label="val"} value and name value.
    """
    # TODO: for each line: skip comment lines; match name{...} value or name value; extract labels; append (name, labels, float(value))
    # TODO: regex for name optionally followed by {label="val",...} then whitespace and value
    return []


def main() -> None:
    # TODO: register_app_metrics(); optionally increment counter, set gauge, observe histogram once
    # TODO: raw = generate_latest(REGISTRY); decoded = raw.decode('utf-8'); samples = parse_metrics_text(decoded)
    # TODO: print short summary (e.g. count of samples, or first few metric names)
    pass


if __name__ == "__main__":
    main()
