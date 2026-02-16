"""
Drill 2: Rate Limiter Decorator
Fill in the TODOs. See README.md for the problem description.
"""

import time
from collections.abc import Callable
from collections import deque
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def rate_limit(calls: int = 5, period: float = 10.0, thread_safe: bool = False):
    """
    Limit function to at most `calls` invocations per `period` seconds.
    Blocks until a slot is available when limit exceeded.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        # TODO: Use a deque or list to track call timestamps
        # TODO: On each call: remove timestamps older than (now - period)
        # TODO: If len(timestamps) >= calls: sleep until oldest expires
        # TODO: Append now, call func
        # TODO: If thread_safe: wrap with threading.Lock
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            raise NotImplementedError("Implement me")

        return wrapper

    return decorator


def main() -> None:
    @rate_limit(calls=3, period=1.0)
    def limited() -> str:
        return "ok"

    for i in range(5):
        t0 = time.perf_counter()
        result = limited()
        elapsed = time.perf_counter() - t0
        print(f"Call {i + 1}: {result} (elapsed {elapsed:.2f}s)")


if __name__ == "__main__":
    main()
