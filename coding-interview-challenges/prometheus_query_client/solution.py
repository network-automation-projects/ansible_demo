"""
Prometheus query API client: query /api/v1/query and parse JSON response.
"""

import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def query_prometheus(base_url: str, query: str) -> dict:
    """GET base_url/api/v1/query?query=... Return full JSON response as dict. On error return {}."""
    url = base_url.rstrip("/") + "/api/v1/query?" + urlencode({"query": query})
    try:
        with urlopen(Request(url), timeout=10) as resp:
            return json.loads(resp.read().decode())
    except (URLError, HTTPError, json.JSONDecodeError):
        return {}


def parse_query_result(response_json: dict) -> list[dict]:
    """
    From Prometheus API response dict, extract data.result into list of
    {"name": ..., "labels": {...}, "value": float, "timestamp": ...}.
    """
    result = response_json.get("data", {}).get("result", [])
    parsed: list[dict] = []
    for item in result:
        metric = item.get("metric", {})
        name = metric.get("__name__", "")
        labels = {k: v for k, v in metric.items() if k != "__name__"}
        value_list = item.get("value", [0, "0"])
        try:
            value = float(value_list[1])
        except (IndexError, TypeError, ValueError):
            value = 0.0
        timestamp = value_list[0] if len(value_list) > 0 else None
        parsed.append({
            "name": name,
            "labels": labels,
            "value": value,
            "timestamp": timestamp,
        })
    return parsed


def main() -> None:
    base = Path(__file__).parent
    fixture_path = base / "fixtures" / "query_response.json"

    if len(sys.argv) >= 3:
        base_url, query = sys.argv[1], sys.argv[2]
        response = query_prometheus(base_url, query)
        parsed = parse_query_result(response)
    else:
        with open(fixture_path) as f:
            response = json.load(f)
        parsed = parse_query_result(response)

    print(f"{'name':<30} {'labels':<40} value")
    print("-" * 80)
    for row in parsed:
        labels_str = ",".join(f"{k}={v}" for k, v in sorted(row["labels"].items()))
        print(f"{row['name']:<30} {labels_str:<40} {row['value']}")


if __name__ == "__main__":
    main()
