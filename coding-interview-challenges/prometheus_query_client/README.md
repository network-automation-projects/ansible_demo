# Prometheus Query API Client (Python)

Practice exercise for **Prometheus HTTP API + Python**. Focus: query the Prometheus API from Python and parse the JSON response (metric names, labels, values). Uses a **fixture JSON** so it runs without a live Prometheus.

## What You'll Use

- **HTTP:** `urllib.request` or `requests` to GET `{base_url}/api/v1/query?query=...`
- **JSON:** Parse response: `status`, `data.result[]`; each result has `.metric` (labels, `__name__`) and `.value` (tuple `[timestamp, value_str]`)
- **pathlib:** Path to fixture file

## Problem

1. **query_prometheus(base_url, query)**  
   GET `base_url + "/api/v1/query"` with param `query` (PromQL). Return the full JSON response as a dict. Handle `urllib.error` or `requests` errors; return empty dict or re-raise as appropriate.

2. **parse_query_result(response_json)**  
   Given the dict returned by the Prometheus API (e.g. from a fixture or from `query_prometheus`), extract the result list. Return a list of dicts: e.g. `[{"name": "...", "labels": {...}, "value": float, "timestamp": "..."}]` for each `data.result[]` item. Handle missing `data` or `result` safely.

3. **main()**  
   Load fixture `fixtures/query_response.json` (sample Prometheus API response), call `parse_query_result`, and print a short table (metric name, labels, value). Optionally accept CLI args for live URL + query and call `query_prometheus` then `parse_query_result`.

## Files

- **fixtures/query_response.json** – Sample Prometheus API response (`status`, `data.resultType`, `data.result` with metric and value).
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py` (from this directory).

## How to Practice

1. Read this README and inspect `fixtures/query_response.json`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py`; check the printed table.
4. Compare with `solution.py`.

## Prerequisites

- Python 3.9+. Stdlib only (or `requests` if you prefer).

## Example API response shape

```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": { "__name__": "up", "job": "demo" },
        "value": [1706630400, "1"]
      }
    ]
  }
}
```

## Run with real stack (optional)

To query a real Prometheus: use the same stack as go-monitor-with-grafana; set base_url to `http://localhost:9090` and run with a query like `up` (e.g. `python solution.py http://localhost:9090 up`).
