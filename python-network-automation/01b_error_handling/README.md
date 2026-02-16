# Module 01b: Error Handling

Exception handling in Python for network automation: try/except, specific exceptions, re-raising, logging, and per-device handling so one failure does not kill the whole run.

## Learning Objectives

By completing this module, you will learn:

- How and when to use try, except, else, and finally
- Why to catch specific exceptions and avoid bare except
- When to re-raise and how to add context or log before re-raising
- How to log in exception handlers so errors are never swallowed silently
- How to fail fast with clear messages for invalid input
- How to handle errors per device in a batch so one failing device does not stop the rest

## Prerequisites

- Module 01: Core Fundamentals
- Basic familiarity with functions and control flow

## Concepts Covered

### try / except / else / finally

- **try:** Run code that might raise.
- **except:** Run only when a matching exception is raised; catch one or more exception types (e.g. `except FileNotFoundError:` or `except (OSError, ValueError):`).
- **else:** Run only when the try block completed without raising (optional; use for "success path" code that should not be in the try body).
- **finally:** Always run after try/except/else, whether or not an exception occurred; use for cleanup (e.g. close a handle, release a lock).

Order of execution: try → (if exception) except → (if no exception) else → finally.

### Catching Specific Exceptions

- Prefer **specific exception types** so you handle only what you intend: `FileNotFoundError`, `json.JSONDecodeError`, `OSError`, `ConnectionRefusedError`, `TimeoutError`, etc.
- Use **`except Exception as e:`** only as a deliberate fallback when you want to log and record "any other error" (e.g. per-device failure). Always log; do not swallow silently.
- **Avoid bare `except:`** — it catches everything, including `KeyboardInterrupt` and `SystemExit`, and can hide bugs. Use `except Exception` if you need a broad catch.

### Re-raising

- **`raise`** (no argument) re-raises the current exception and preserves the original traceback.
- **`raise e`** re-raises the caught exception; use when you want to re-raise after logging or cleanup.
- You can wrap in a custom exception (e.g. `raise DeviceConnectionError("r1") from e`) to add context while chaining the cause.

### Logging in Handlers

- **Never swallow exceptions silently.** When you catch an exception, log it (e.g. `logger.warning(...)` or `logger.error(...)`) so operators can see what went wrong.
- Use the `logging` module; avoid `print` for non-CLI code (per project style).

### Fail Fast with Clear Messages

- For invalid input or preconditions, raise early with a clear message: e.g. `raise ValueError("hostname required")` or `raise TypeError("devices must be a list")`.
- This makes debugging easier and keeps invalid state from propagating.

### Per-Device Handling

- When processing multiple devices (or files, API calls), wrap the per-item work in try/except **inside the loop**. On exception, log, record that item as failed (e.g. append to a `failed` list or a result dict with status), and continue. Do not let one failure terminate the entire batch.
- See the coding-interview challenge [debug_netmiko_timeout_crash](../../coding-interview-challenges/debug_netmiko_timeout_crash/) for a concrete example: catch `NetmikoTimeoutException` (and optionally `NetmikoAuthenticationException`) per device and append a failed result instead of letting the exception propagate.

### Optional: Custom Exceptions

- For domain-specific errors (e.g. device connection or config validation), define a subclass of `Exception` (or a more specific base like `RuntimeError`) and raise it when your logic detects the error. Callers can then catch that type specifically.

## Use Cases in Network Automation

### File and JSON Loading

- Catch `FileNotFoundError` when opening a config or inventory file; return a default or exit with a clear message.
- Catch `json.JSONDecodeError` when parsing JSON; log the line or file and re-raise or return empty dict/list per your convention.

### Device Connection and Commands

- Catch connection/timeout exceptions (e.g. `NetmikoTimeoutException`, `NetmikoAuthenticationException`) per device; log and record as failed, then continue with the next device.
- Use a broader `except Exception` only as fallback and always log.

### API and Network Calls

- Catch `requests` or `urllib` errors (e.g. `ConnectionError`, `TimeoutError`) and either retry or record failure and continue, depending on your design.

### Input Validation

- Validate types and required fields (e.g. "devices must be a list", "hostname required"); raise `ValueError` or `TypeError` with a clear message so callers get actionable feedback.

## Related Modules and Challenges

- **Module 01:** Core Fundamentals (e.g. `isinstance()` for type checks before operations)
- **Module 03:** File I/O (FileNotFoundError, JSONDecodeError when reading configs)
- **Module 04:** Device Management (per-device exception handling for Netmiko/NAPALM)
- **Module 05:** API Integration (handling API errors and retries)
- **Coding challenges:** [debug_netmiko_timeout_crash](../../coding-interview-challenges/debug_netmiko_timeout_crash/) (per-device try/except, catch specific exceptions, log, avoid bare except); [debug_logs_connection_refused](../../coding-interview-challenges/debug_logs_connection_refused/) (record failed status in handler); [nre_core_patterns](../../coding-interview-challenges/nre_core_patterns/) (try/except with intent, collect ok/failed)

## Exercises

Work through `exercises.py` to practice catching specific exceptions, per-device handling, and logging/re-raising with fill-in-the-blank exercises.

## Examples

Review `examples.py` for runnable examples: file/JSON loading with specific exceptions, per-device loop with ok/failed collection, and optional else/finally and re-raise patterns.
