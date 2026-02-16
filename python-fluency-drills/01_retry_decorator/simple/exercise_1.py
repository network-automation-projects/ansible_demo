"""
Drill 1: Retry Decorator (Simple — no ParamSpec/TypeVar)
Fill in the TODOs. See README.md for the problem description.

- `@retry(max_attempts=3, delay=1)` — decorator with configurable max attempts and delay
- Retry the function when it raises an exception
- Stop after `max_attempts` attempts
- Re-raise the final exception if all attempts fail

"""

import time
from typing import Callable, Any
from functools import wraps


def retry(max_attempts=3, delay=1, with_backoff=False):
    """
    Decorator that retries a function on exception.
    Stops after max_attempts and re-raises the final exception.
    """
    def decorator(func: Callable) -> Callable:
        
            # TODO: Implement retry loop
            # - Call func(*args, **kwargs)
            # - On exception: sleep(delay), retry
            # - Use exponential backoff if use_exponential_backoff: delay *= 2 each retry
            # - After max_attempts, re-raise last exception
            

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exc: BaseException | None = None
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < (max_attempts - 1):
                        time.sleep(current_delay)
                        if with_backoff:
                            current_delay *= 2
            if last_exc is not None:
                raise last_exc
                

            
        return wrapper

    return decorator


def main() -> None:


    
    result = flaky()
    print("Result:", result)
    print("Calls:", call_count)


if __name__ == "__main__":
    main()
