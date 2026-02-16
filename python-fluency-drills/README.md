# 21 Python Fluency Drills (Beginner → Advanced)

Portfolio-ready exercises for daily practice. Build live-coding fluency and architecture clarity. Every day: code from scratch, refactor for clarity, add type hints and docstrings, add tests if time allows.

**Python 3.9+.** Style: Black, type hints, logging (see [AGENTS.md](../AGENTS.md)).

## Index

| # | Drill | Focus | Path |
|---|-------|-------|------|
| 0 | Write a Function | Docstring, type hints | [00_write_a_function/](00_write_a_function/) |
| 0b | Simple Decorator | Non-nested decorator, @wraps | [00b_simple_decorator/](00b_simple_decorator/) |
| 1 | Retry Decorator | Decorators, retry on exception | [01_retry_decorator/](01_retry_decorator/) |
| 2 | Rate Limiter Decorator | Limit calls per time window | [02_rate_limiter/](02_rate_limiter/) |
| 3 | Simple CLI Tool | argparse, JSON replace, backup | [03_cli_json_replace/](03_cli_json_replace/) |
| 4 | Parse Nested JSON | Extract all "id" keys, flat list | [04_nested_json_ids/](04_nested_json_ids/) |
| 5 | Job Queue | add_job, run_next, success/failure/retry | [05_job_queue/](05_job_queue/) |
| 6 | Context Manager Timer | with timer(): print execution time | [06_timer_context_manager/](06_timer_context_manager/) |
| 7 | Async FastAPI Endpoint | POST /process, Pydantic, asyncio | [07_fastapi_process/](07_fastapi_process/) |
| 8 | LRU Cache | get/put with OrderedDict | [08_lru_cache/](08_lru_cache/) |
| 9 | Log Parser | Error count, most common user, status dist | [09_log_parser/](09_log_parser/) |
| 10 | REST Client | Retry on 500, timeout, JSON logs | [10_rest_client/](10_rest_client/) |
| 11 | Exponential Backoff | base_delay * 2^attempt, jitter | [11_backoff_function/](11_backoff_function/) |
| 12 | Custom Exception Hierarchy | AutomationError, ValidationError, ExecutionError | [12_exception_hierarchy/](12_exception_hierarchy/) |
| 13 | ThreadPool Executor | 10 tasks, partial failures, summary | [13_threadpool_executor/](13_threadpool_executor/) |
| 14 | Token Bucket Rate Limiter | N tokens/sec, reject when empty | [14_token_bucket/](14_token_bucket/) |
| 15 | In-Memory Database | insert, update, delete, query, filtering | [15_in_memory_db/](15_in_memory_db/) |
| 16 | Pydantic Nested Validation | Job model, validators, custom rules | [16_pydantic_job_model/](16_pydantic_job_model/) |
| 17 | Background Worker | Task submission, status polling | [17_background_worker/](17_background_worker/) |
| 18 | Mini AI Wrapper | summarize(), mock LLM, timeout, retry | [18_ai_summarize_wrapper/](18_ai_summarize_wrapper/) |
| 19 | Unit Tests | pytest, mock failures, assert behavior | [19_unit_tests/](19_unit_tests/) |
| 20 | Mini Automation Service | CLI + Pydantic + retry + worker + async | [20_mini_automation_service/](20_mini_automation_service/) |

## How to Use

1. Read the drill's `README.md` for the problem statement and requirements.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run: `python exercise.py` (from the drill directory).
4. Compare with `solution.py` when done.

## Dependencies

Drills 1–6, 8–9, 11–15, 17–18 use stdlib only. For the rest:

```bash
pip install -r requirements.txt
```

## After 21 Days

You will feel very different in Python. Live coding anxiety drops. Architecture clarity increases.
