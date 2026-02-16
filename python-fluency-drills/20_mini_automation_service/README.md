# Drill 20: Combine It All — Mini Automation Service

Create a portfolio-ready mini service combining CLI, Pydantic, retry, logging, background worker, and async endpoint.

## Requirements

**Base:**
- CLI entrypoint (argparse): e.g. `python service.py run` or `python service.py --config config.json`
- Pydantic validation for config
- Retry logic for external calls
- Logging (structured or standard)
- Background worker for tasks
- Async FastAPI endpoint (e.g. POST /submit, GET /status)

It can be simple but structured. Portfolio-ready.

## Example

```bash
python service.py run
# Starts server. POST /submit with {"task": "..."}, GET /status/{id}
```

## Files

- **exercise.py** — Skeleton with TODOs.
- **solution.py** — Reference solution.

## Dependencies

```bash
pip install fastapi uvicorn pydantic
```
