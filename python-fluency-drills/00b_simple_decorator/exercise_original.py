"""
Drill 0b: Simple Decorator (No Nesting)
Fill in the TODO. See README.md for the problem description.
"""

from functools import wraps
from typing import Any, Callable


def log_call(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that prints the function name before and after it runs.
    No parameters — use @log_call (no parentheses).
    """
    # TODO: Use @wraps(func)
    # TODO: Define wrapper(*args, **kwargs) that:
    #   - Prints "Before: {func.__name__}"
    #   - Calls func(*args, **kwargs) and stores result
    #   - Prints "After: {func.__name__}"
    #   - Returns the result
    # TODO: Return wrapper
    raise NotImplementedError("Implement me")


def main() -> None:
    @log_call
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    result = greet("World")
    print(result)


if __name__ == "__main__":
    main()
