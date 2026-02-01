"""
Retry with backoff: wrap a flaky function in retry logic with exponential backoff.
"""

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exceptions: tuple[type[Exception], ...] = (ConnectionError, TimeoutError),
) -> T:
    """Call func(); on exception, wait with exponential backoff and retry up to max_attempts."""
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            last_exc = e
            if attempt < max_attempts - 1:
                delay = min(base_delay * (2**attempt), max_delay)
                time.sleep(delay)
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("Max retries exceeded")


def main() -> None:
    call_count = 0

    def flaky() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Simulated failure")
        return "ok"

    result = retry_with_backoff(flaky, max_attempts=5, base_delay=0.05, max_delay=1.0)
    print("Result:", result)
    print("Calls:", call_count)


if __name__ == "__main__":
    main()
