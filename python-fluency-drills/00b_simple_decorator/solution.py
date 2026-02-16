"""
Drill 0b: Simple Decorator (No Nesting) — Reference solution.
"""

from functools import wraps
from typing import Any, Callable


def log_call(func: Callable[..., Any]) -> Callable[..., Any]:           #define the decorator
    """
    Decorator that prints the function name before and after it runs.
    No parameters — use @log_call (no parentheses).
    """

    @wraps(func)                                                        #make the wrapper
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Before calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After calling: {func.__name__}")
        return result

    return wrapper


def main() -> None:
    @log_call
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    result = greet("World")
    print(result)


if __name__ == "__main__":
    main()
