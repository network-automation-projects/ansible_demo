"""
Drill 0b: Simple Decorator (No Nesting)
Fill in the TODO. See README.md for the problem description.

- Write a decorator `log_call` that prints the function name before and after it runs
- Use `@wraps(func)` to preserve the wrapped function's metadata
- No parameters: use `@log_call` (no parentheses)  # so, python does -- greet = log_call(greet) -- with parentheses would -- Python does: greet = log_call()(greet)
First log_call() is called with no arguments.
Whatever it returns is then used as the decorator and called with greet.


"""

from typing import Callable, Any
from functools import wraps



def log_call(func: Callable) -> Callable:
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
    
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print (f"Before: {func.__name__}")
        result = func(*args, **kwargs)
        print (f"After: {func.__name__}")
        return result

    # TODO: Return wrapper
    return wrapper


def main() -> None:
    @log_call
    def greet(name)->str:
        result = f"Hello {name}!"
        return result

    result = greet("world")
    print(result)


if __name__ == "__main__":
    main()
