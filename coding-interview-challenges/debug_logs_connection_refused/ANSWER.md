# Answer: Why the Report Shows Success When Logs Show Failure

## Root Cause

The exception handler logs the error correctly but appends a `TaskResult` with `status="success"` instead of `status="failed"`. The bug is in the `except` block: we record success even though the connection failed.

## Why It Manifests

1. `connect_and_run("core-sw2")` raises `ConnectionRefusedError`.
2. The `except Exception` block catches it.
3. We call `logger.error(...)` — so the logs correctly show the failure.
4. We append `TaskResult(hostname=hostname, status="success", error=str(e))` — **incorrect**. We should append `status="failed"`.
5. The report iterates over results and prints each status. Since we stored `"success"`, the report shows success.

The logs and the report are built from different code paths: logging uses the error message; the results list uses the wrong status.

## Code Fix

Change `status="success"` to `status="failed"` in the exception handler:

```python
        except Exception as e:
            logger.error(f"Connection refused for device {hostname}: {e}")
            results.append(
                TaskResult(
                    hostname=hostname,
                    status="failed",   # was "success"
                    error=str(e),
                )
            )
```

## How to Spot Similar Bugs

- **Log vs result mismatch:** If logs say "error" or "failed" but the report says "success", the exception handler is likely recording the wrong status. Trace from the log line to the handler and check what gets appended to the results.
- **Broad exception handling:** `except Exception` catches everything. Ensure the handler does the right thing for each failure type — e.g. connection refused should yield a failed result, not success.
- **Copy-paste errors:** The handler may have been copied from the success path. Verify that failure paths set failure status.

## Best Practices

1. **Match logs and report:** If you log an error, the corresponding result should reflect failure. Consider a helper: `results.append(make_failed_result(hostname, e))`.
2. **Catch specific exceptions:** Use `except ConnectionRefusedError` (or `OSError`) instead of `except Exception` when you know the failure type. That makes the handler’s intent clear and avoids accidentally swallowing unrelated errors.
3. **Explicit status on failure:** Prefer `status="failed"` (or an enum) over reusing success and adding an `error` field. A single source of truth (status) avoids contradictions.
