"""
Drill 0b: Simple Decorator (No Nesting)
Fill in the TODO. See README.md for the problem description.

- Write a decorator `log_call` that prints the function name before and after it runs
- Use `@wraps(func)` to preserve the wrapped function's metadata
- No parameters: use `@log_call` (no parentheses)  # so, python does -- greet = log_call(greet) -- with parentheses would -- Python does: greet = log_call()(greet)
First log_call() is called with no arguments.
Whatever it returns is then used as the decorator and called with greet.


"""



def :
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


def 

    #define a greeting function that takes a name and returns str hello world


    print(result)


if 
