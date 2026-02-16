# Drill 7: Async FastAPI Endpoint

Write a small FastAPI app with POST /process that accepts JSON, validates with Pydantic, and simulates async work.

## Requirements

**Base:**
- POST `/process` endpoint
- Accept JSON body
- Validate with Pydantic model (e.g. `{"data": str, "delay": float}`)
- Simulate async work with `asyncio.sleep(delay)`
- Return result (e.g. `{"status": "ok", "processed": data}`)

## Example

```bash
curl -X POST http://localhost:8000/process -H "Content-Type: application/json" -d '{"data":"hello","delay":0.5}'
# {"status":"ok","processed":"hello"}
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.

## Dependencies

```bash
pip install fastapi uvicorn pydantic
```
