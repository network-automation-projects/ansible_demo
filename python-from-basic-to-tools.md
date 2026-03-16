# Python: From Basic to Tools

A reference chart mapping **learning patterns** (common in tutorials and courses) to **better tools and practices** used in professional Python codebases.

---

## Timing & Benchmarking

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| `time.time()` for elapsed time | `time.perf_counter()` | `time.time()` is wall-clock; affected by NTP, daylight saving, manual clock changes. `perf_counter()` is monotonic and higher resolution for timing. |
| `datetime.now()` for elapsed time | `time.perf_counter()` | `datetime` is for dates/timestamps, not measuring duration. Use `perf_counter()` for timing. |
| Manual `start = time.X(); ...; elapsed = time.X() - start` for **benchmarking** | `timeit` module | `timeit` runs code many times, disables GC during runs, reports mean/std, and handles setup/teardown. Ideal for comparing performance of snippets. |
| Manual timing in a decorator (single run) | `time.perf_counter()` | For one-off wall-clock timing (e.g. a timer decorator), `perf_counter()` is correct. Use `timeit` when you need **repeated runs** for benchmarking. |

**Summary:**

- Single-run timing (decorator, context manager): `time.perf_counter()`
- Benchmarking (compare algorithms, micro-optimize): `timeit.timeit()` or `timeit.repeat()`
- Durations that must survive clock skew: `time.monotonic()`

---

## Debugging & Output

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| `print()` for debugging | `logging` module | Logging has levels (DEBUG, INFO, WARNING, ERROR), configurable handlers, timestamps, and can be turned off in production. |
| `print()` for user-facing output | `print()` is fine | For CLI tools, `print()` is appropriate. Use logging for internal diagnostics. |

---

## Dates & Times

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| `datetime.now()` for "now" | `datetime.now(timezone.utc)` | Explicit timezone avoids "naive" datetime bugs. Store and compare in UTC. |
| `datetime.utcnow()` | `datetime.now(timezone.utc)` | `utcnow()` is deprecated in Python 3.12+; `now(timezone.utc)` is the replacement. |
| `datetime.strftime()` for filenames | Same, or `datetime.now().strftime('%Y%m%d_%H%M%S')` | Fine for timestamps. Ensure timezone if needed. |

---

## Strings

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| `"Hello " + name + "!"` | `f"Hello {name}!"` | F-strings are readable, fast, and less error-prone. |
| `"%s %s" % (a, b)` | `f"{a} {b}"` | F-strings are preferred in modern Python. |
| `.format()` | `f"..."` | F-strings are usually clearer and faster. |

---

## Paths & Files

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| `open("/hardcoded/path/file.txt")` | `pathlib.Path` | `Path` is cross-platform, composable (`p / "sub" / "file.txt"`), and has `.read_text()`, `.write_text()`, `.exists()`, etc. |
| String concatenation for paths | `path / "subdir" / "file.txt"` | Avoids `os.path.join` and slash issues. |
| `os.path.exists()`, `os.path.join()` | `Path.exists()`, `path / other` | `pathlib` is the preferred API. |

---

## Configuration & Secrets

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| Hardcoded API keys, passwords | Environment variables or `.env` | Never commit secrets. Use `os.environ` or `python-dotenv` for local dev. |
| Config in code | `pydantic-settings`, `python-dotenv`, or YAML/JSON | Centralized, validated config; different values per environment. |
| `os.environ.get("KEY")` | `pydantic-settings.BaseSettings` | Type coercion, validation, `.env` loading, and clear config schema. |

---

## Retries & Resilience

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| Manual `for i in range(n): try ... except` | `tenacity` or `backoff` | Decorators for retries with exponential backoff, jitter, and configurable conditions. |
| `time.sleep()` in retry loops | Same, or `tenacity.wait_exponential()` | For simple cases, `time.sleep()` is fine. Libraries handle backoff/jitter for you. |

---

## Data Validation

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| Manual `if not isinstance(x, str): raise` | `pydantic` | Declarative models with validation, JSON serialization, and clear error messages. |
| Parsing JSON into dicts | `pydantic` models | Validates structure and types at parse time; catches bad data early. |

---

## HTTP Requests

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| `requests` for sync | `requests` is fine | Still widely used. |
| `requests` for async | `httpx` | Same API, supports `async`/`await`. Use when you need async HTTP. |

---

## Testing

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| `unittest` | `pytest` | Less boilerplate, better assertions, fixtures, parametrize, plugins. |
| `assert x == y` in scripts | `pytest` test functions | Assertions in scripts run only when `__debug__`; pytest captures and reports them properly. |

---

## Type Hints

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| No type hints | Type hints on public functions | Improves readability and enables static checking. |
| `List[str]`, `Dict[str, int]` | `list[str]`, `dict[str, int]` (Python 3.9+) | Built-in generics; no `typing` import needed. |
| Manual type checking | `mypy` or `pyright` | Catches type errors before runtime. |

---

## Error Handling

| Learn This (Basic) | Replace With (Workplace) | Why |
|-------------------|--------------------------|-----|
| `except Exception:` | `except SpecificError:` | Catch specific exceptions; let unexpected ones propagate. |
| `except: pass` | Never | Silences all errors; makes debugging impossible. |
| Broad `try/except` | Narrow scope, specific exceptions | Fail fast with clear messages. |

---

## Quick Reference: Your Timer Decorator

For a **single-run** timer decorator (like in `realpython/decorators.py`):

- Use `time.perf_counter()` — correct for wall-clock elapsed time.
- Avoid `datetime.now()` for elapsed time — it's for timestamps, not duration.
- Use `timeit` when you want to **benchmark** (many runs, statistics) rather than time one call.

```python
# Single-run timing (decorator) — use perf_counter
start = time.perf_counter()
result = func(*args, **kwargs)
elapsed = time.perf_counter() - start

# Benchmarking (compare implementations) — use timeit
import timeit
timeit.timeit("func()", setup="from mymodule import func", number=10000)
```

---

## See Also

- **AGENTS.md** — Build, run, test, and style guidelines for this repo
- **python-notes-decorators.md** — Decorator patterns and examples
- **python-notes.md** — General Python tidbits and gotchas
