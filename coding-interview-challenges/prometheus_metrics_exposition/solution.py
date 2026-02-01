"""
Prometheus metrics exposition: register Counter/Gauge/Histogram, generate /metrics, parse text format.
"""

import re
from typing import Any

from prometheus_client import (
    REGISTRY,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    start_http_server,
)


def register_app_metrics() -> dict[str, Any]:
    """Register Counter, Gauge, Histogram; return dict with refs. Label service='demo'."""
    counter = Counter(
        "app_requests_total", "Total requests", ["service"]
    )
    counter.labels(service="demo").inc(0)

    gauge = Gauge("app_active_tasks", "Active tasks", ["service"])
    gauge.labels(service="demo").set(0)

    histogram = Histogram(
        "app_request_duration_seconds", "Request duration in seconds", ["service"]
    )
    histogram.labels(service="demo").observe(0.1)

    return {"counter": counter, "gauge": gauge, "histogram": histogram}


def serve_metrics(port: int) -> None:
    """Start HTTP server for default registry on port so /metrics is served."""
    start_http_server(port)


def parse_metrics_text(
    metrics_str: str,
) -> list[tuple[str, dict[str, str], float]]:
    """
    Parse Prometheus exposition format into list of (metric_name, labels_dict, value).
    Ignore # TYPE and # HELP. Handle name{label="val"} value and name value.
    """
    result: list[tuple[str, dict[str, str], float]] = []
    # Match: name or name{label="val",...} then whitespace and number (value)
    pattern = re.compile(
        r'^([a-zA-Z_:][a-zA-Z0-9_:]*)'
        r'(?:\{([^}]*)\})?\s+'
        r'([0-9.eE+-]+)'
    )
    for line in metrics_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = pattern.match(line)
        if not match:
            continue
        name = match.group(1)
        labels_str = match.group(2)
        value_str = match.group(3)
        labels: dict[str, str] = {}
        if labels_str:
            # Parse label="value", label2="value2"
            for part in labels_str.split(","):
                part = part.strip()
                if "=" in part:
                    key, _, val = part.partition("=")
                    key = key.strip()
                    val = val.strip().strip('"')
                    labels[key] = val
        try:
            value = float(value_str)
        except ValueError:
            continue
        result.append((name, labels, value))
    return result


def main() -> None:
    register_app_metrics()
    raw = generate_latest(REGISTRY)
    decoded = raw.decode("utf-8")
    samples = parse_metrics_text(decoded)
    # Filter to app_* only for a short summary
    app_samples = [s for s in samples if s[0].startswith("app_")]
    print(f"Parsed {len(samples)} metric samples total")
    print(f"App metrics: {len(app_samples)} samples")
    for name, labels, value in app_samples[:10]:
        print(f"  {name} {labels} = {value}")


if __name__ == "__main__":
    main()
