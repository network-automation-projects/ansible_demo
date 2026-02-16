"""
Drill 19: Unit Tests — Reference solution.
Run: pytest solution.py -v  (solution.py contains tests as well)
Or: pytest test_exercise.py -v  (after implementing)
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "01_retry_decorator"))
from solution import retry


def test_retry_succeeds_immediately() -> None:
    @retry(max_attempts=3, delay=0.01)
    def ok() -> str:
        return "ok"

    assert ok() == "ok"


def test_retry_succeeds_after_failures() -> None:
    call_count = 0

    def flaky() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("fail")
        return "ok"

    decorated = retry(max_attempts=5, delay=0.01)(flaky)
    assert decorated() == "ok"
    assert call_count == 3


def test_retry_reraises_after_max_attempts() -> None:
    def flaky() -> str:
        raise ConnectionError("always fail")

    with pytest.raises(ConnectionError, match="always fail"):
        retry(max_attempts=3, delay=0.01)(flaky)()
