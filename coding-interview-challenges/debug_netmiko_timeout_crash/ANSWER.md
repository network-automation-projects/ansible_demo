# Answer: Why the Script Crashes on Timeout

## Root Cause

The script has **no exception handling** around the device connection and command execution. When `connect_and_run("core-sw2")` raises `NetmikoTimeoutException`, the exception propagates out of `run_batch()` and then out of `main()`, so the process crashes before the report is ever printed.

## Why It Manifests

1. `run_batch()` iterates over devices and calls `connect_and_run(hostname)` for each.
2. For `core-sw2`, the mock raises `NetmikoTimeoutException`.
3. There is no `try/except` in `run_batch()`, so the exception is not caught.
4. The exception bubbles up; `main()` never gets the `results` list and never reaches the "Report" print.
5. The script exits with a traceback.

## Code Fix

Catch connection/timeout exceptions per device and append a failed result instead of letting the exception propagate:

```python
def run_batch(devices: list[str]) -> list[DeviceResult]:
    """Process each device and collect results."""
    results: list[DeviceResult] = []

    for hostname in devices:
        try:
            result = connect_and_run(hostname)
            results.append(result)
        except NetmikoTimeoutException as e:
            logger.warning(f"Timeout for {hostname}: {e}")
            results.append(
                DeviceResult(hostname=hostname, status="failed", error=str(e))
            )
        except Exception as e:
            logger.error(f"Unexpected error for {hostname}: {e}")
            results.append(
                DeviceResult(hostname=hostname, status="failed", error=str(e))
            )

    return results
```

Optional: also catch `NetmikoAuthenticationException` if using real Netmiko, so auth failures are recorded per device instead of crashing.

## How to Spot Similar Bugs

- **No try/except around device I/O:** Any network or SSH call can raise. If there is no handler, one bad device kills the whole run.
- **Traceback points at "connect" or "send_command":** Look for the loop that calls that code; add exception handling in the loop so one failure does not stop the batch.
- **Report never prints:** If the crash happens before the report, the code path that builds/prints the report is never reached. Handle exceptions before that point.

## Best Practices

1. **Catch specific exceptions:** Use `except NetmikoTimeoutException` (and `NetmikoAuthenticationException`) so you can log and handle timeouts vs auth separately; use a broader `Exception` only as a fallback and log clearly.
2. **Record failure per device:** Append a "failed" result with hostname and error message so the report is complete and you don't lose track of which device failed.
3. **Don't swallow silently:** Always log (e.g. `logger.warning` or `logger.error`) when you catch an exception so operators can see what went wrong.
4. **Avoid bare except:** Use `except Exception` only when you intend to handle "anything else"; avoid `except:` so you don't hide bugs like `KeyboardInterrupt` or `SystemExit`.
