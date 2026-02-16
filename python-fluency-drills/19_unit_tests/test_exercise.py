"""
Drill 19: Unit Tests for Retry Decorator
Fill in the TODOs. Run: pytest test_exercise.py -v
"""

import sys
from pathlib import Path

import pytest

# Import retry from 01_retry_decorator
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "01_retry_decorator"))
from solution import retry


def test_retry_succeeds_immediately() -> None:
    """When function succeeds on first call, no retries."""
    # TODO: Decorate a function that returns "ok", assert result
    raise NotImplementedError("Implement me")


def test_retry_succeeds_after_failures() -> None:
    """When function fails N times then succeeds, returns result."""
    # TODO: call_count = 0; flaky raises 2x then returns "ok"
    # TODO: assert retry(max_attempts=5)(flaky)() == "ok"
    # TODO: assert call_count == 3
    raise NotImplementedError("Implement me")


def test_retry_reraises_after_max_attempts() -> None:
    """When all attempts fail, re-raise the last exception."""
    # TODO: flaky always raises ConnectionError
    # TODO: with pytest.raises(ConnectionError): retry(max_attempts=3)(flaky)()
    raise NotImplementedError("Implement me")
