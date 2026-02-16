"""
Drill 2: Rate Limiter Decorator — Reference solution.
"""

import threading
import time
from collections import deque
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def rate_limit(calls: int = 5, period: float = 10.0, thread_safe: bool = False):
    """
    Limit function to at most `calls` invocations per `period` seconds.
    Blocks until a slot is available when limit exceeded.
    """
    timestamps: deque[float] = deque()
    lock = threading.Lock() if thread_safe else None

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            def do_call() -> T:
                now = time.monotonic()
                cutoff = now - period
                while timestamps and timestamps[0] < cutoff:
                    timestamps.popleft()
                while len(timestamps) >= calls:
                    sleep_time = timestamps[0] + period - time.monotonic()
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    now = time.monotonic()
                    cutoff = now - period
                    while timestamps and timestamps[0] < cutoff:
                        timestamps.popleft()
                timestamps.append(time.monotonic())
                return func(*args, **kwargs)

            if lock is not None:
                with lock:
                    return do_call()
            return do_call()

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
