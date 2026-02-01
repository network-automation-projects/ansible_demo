"""
Exercise: query Prometheus HTTP API from Python, parse JSON response.
Fill in the TODOs. See README.md for the problem description.
"""

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def query_prometheus(base_url: str, query: str) -> dict:
    """GET base_url/api/v1/query?query=... Return full JSON response as dict. Handle errors."""
    # TODO: url = base_url.rstrip('/') + '/api/v1/query?' + urlencode({'query': query})
    # TODO: with urlopen(Request(url)) as resp: return json.loads(resp.read().decode())
    # TODO: on URLError/HTTPError: return {} or re-raise
    return {}


def parse_query_result(response_json: dict) -> list[dict]:
    """
    From Prometheus API response dict, extract data.result into list of
    {"name": ..., "labels": {...}, "value": float, "timestamp": ...}.
    Handle missing data/result safely.
    """
    # TODO: result = response_json.get("data", {}).get("result", [])
    # TODO: for each item: name = item["metric"].get("__name__", ""); labels = {k: v for k, v in item["metric"].items() if k != "__name__"}
    # TODO: value list = item.get("value", [ts, val]); value = float(value_list[1]); timestamp = value_list[0]
    # TODO: append {"name": name, "labels": labels, "value": value, "timestamp": timestamp}
    return []


def main() -> None:
    base = Path(__file__).parent
    fixture_path = base / "fixtures" / "query_response.json"
    # TODO: load fixture JSON from fixture_path
    # TODO: parsed = parse_query_result(loaded); print short table (name, labels, value)
    # TODO: optional: if sys.argv[1:2] then base_url, query = argv[1], argv[2]; response = query_prometheus(base_url, query); parsed = parse_query_result(response); print
    pass


if __name__ == "__main__":
    main()
