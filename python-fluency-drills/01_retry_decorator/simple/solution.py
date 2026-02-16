"""
Drill 1: Retry Decorator (Simple) — Reference solution.
Uses Callable[..., Any] instead of ParamSpec/TypeVar.
"""

import time
from functools import wraps
from typing import Any, Callable


def retry(max_attempts: int = 3, delay: float = 1.0, use_exponential_backoff: bool = False):
    """
    Decorator that retries a function on exception.
    Stops after max_attempts and re-raises the final exception.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: BaseException | None = None       #set tracking variable for exception
            current_delay = delay                       # and delay length
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)        #if it succeeds, it jumps out here
                except Exception as e:
                    last_exc = e                        #if it fails, it stores the error in this var
                    if attempt < max_attempts - 1:      #if its less than max tries
                        time.sleep(current_delay)       #delay
                        if use_exponential_backoff:
                            current_delay *= 2
            if last_exc is not None:                    # flow will continue here in case of error persisting after max retries
                raise last_exc                          # raise the error
            raise RuntimeError("Max retries exceeded")  # if it gets here, it's because max_attempts was 0

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
