# Drill 19: Write Unit Tests

Pick one prior drill (e.g. retry decorator) and write pytest tests with mocks and assertions.

## Requirements

**Base:**
- Write pytest tests for the retry decorator (drill 01)
- Mock failures (e.g. function that raises N times then succeeds)
- Assert: success after retries, final exception re-raised when max exceeded

## Example

```python
def test_retry_succeeds_on_third_attempt():
    call_count = 0
    def flaky():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError()
        return "ok"
    result = retry(max_attempts=5)(flaky)()
    assert result == "ok"
    assert call_count == 3
```

## Files

- **exercise.py** — Skeleton with TODOs (or import from 01_retry_decorator).
- **test_exercise.py** — Your tests.
- **solution.py** — Reference tests.

## Dependencies

```bash
pip install pytest
```
