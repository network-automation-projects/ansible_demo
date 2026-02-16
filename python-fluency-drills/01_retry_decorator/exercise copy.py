"""
Drill 1: Retry Decorator
Fill in the TODOs. See README.md for the problem description.
"""

import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def retry(max_attempts: int = 3, delay: float = 1.0, use_exponential_backoff: bool = False):
    """
    Decorator that retries a function on exception.
    Stops after max_attempts and re-raises the final exception.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # TODO: Implement retry loop
            # - Call func(*args, **kwargs)
            # - On exception: sleep(delay), retry
            # - Use exponential backoff if use_exponential_backoff: delay *= 2 each retry
            # - After max_attempts, re-raise last exception
            raise NotImplementedError("Implement me")

        return wrapper

    return decorator


def main() -> None:
    call_count = 0

    @retry(max_attempts=3, delay=0.05)
    def flaky() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Simulated failure")
        return "ok"

    result = flaky()
    print("Result:", result)
    print("Calls:", call_count)


if __name__ == "__main__":
    main()
