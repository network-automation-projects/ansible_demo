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


def :
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
