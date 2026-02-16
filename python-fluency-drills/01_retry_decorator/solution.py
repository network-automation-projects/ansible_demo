"""
Drill 1: Retry Decorator — Reference solution.
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
            last_exc: BaseException | None = None
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        if use_exponential_backoff:
                            current_delay *= 2
            if last_exc is not None:
                raise last_exc
            raise RuntimeError("Max retries exceeded")

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
