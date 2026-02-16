# Answer: Why the Retry Never Succeeds

## Root Cause

The `return None` statement is **incorrectly indented**. It sits at the same level as the `if attempt < max_attempts:` block instead of inside an `else` clause. As a result, after every failed attempt the function returns `None` immediately — even when retries remain. The loop never reaches a second or third iteration.

## Why It Manifests

1. Attempt 1 fails → we enter `except`, log the failure.
2. `attempt < max_attempts` is true (1 < 3) → we sleep.
3. `return None` runs unconditionally (it is not inside the `if`).
4. The function exits. Attempts 2 and 3 never run.

The task would succeed on attempt 3, but we never give it that chance.

## Code Fix

Move `return None` so it runs only when all attempts are exhausted:

```python
        if attempt < max_attempts:
            delay = base_delay * (backoff_multiplier ** (attempt - 1))
            logger.info(f"Waiting {delay:.2f}s before retry...")
            time.sleep(delay)
        else:
            return None

    return None
```

Alternatively, keep a single `return None` at the end of the loop and remove the inner one:

```python
        if attempt < max_attempts:
            delay = base_delay * (backoff_multiplier ** (attempt - 1))
            logger.info(f"Waiting {delay:.2f}s before retry...")
            time.sleep(delay)
        # Don't return here; let the loop continue

    return None  # Only reached after all attempts failed
```

## How to Spot Similar Bugs

- **Indentation and control flow:** A `return` at the wrong indent level can short-circuit loops. Trace each path: "What happens after the first iteration?"
- **Retry loops:** Confirm that "retry" means the loop continues to the next iteration. Any `return` or `break` in the failure path can prevent that.
- **Test the boundary:** Run with `max_attempts=1` (should fail) and `max_attempts=3` (should eventually succeed). If both behave the same, the retry path is broken.

## Best Practices

1. **Explicit structure:** Use `else` when returning on final failure so it’s clear the return is only for the last attempt.
2. **Single exit for failure:** Prefer one `return None` after the loop instead of multiple returns in the loop body.
3. **Tests:** Add a unit test where the task fails N times then succeeds; assert that the runner succeeds when `max_attempts > N`.
