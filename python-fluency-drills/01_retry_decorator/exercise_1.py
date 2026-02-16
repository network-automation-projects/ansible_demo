"""
Drill 1: Retry Decorator
Fill in the TODOs. See README.md for the problem description.

- `@retry(max_attempts=3, delay=1)` — decorator with configurable max attempts and delay
- Retry the function when it raises an exception
- Stop after `max_attempts` attempts
- Re-raise the final exception if all attempts fail

"""

import time
from collections.abc import Callable
from functools import wraps



def @retry_decorator(max_attempts=3, delay=1, use_exponential_backoff=False):
    """
    Decorator that retries a function on exception.
    Stops after max_attempts and re-raises the final exception.
    """

    def decorator(

    return decorator


def main() -> None:







    print("Result:", result)
    print("Calls:", call_count)


if __name__ == "__main__":
    main()
