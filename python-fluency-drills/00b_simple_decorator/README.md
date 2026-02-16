# Drill 0b: Simple Decorator (No Nesting)

A decorator with **no parameters** — just one function that wraps another. No nested `decorator` inside `retry(...)`.

## Requirements

- Write a decorator `log_call` that prints the function name before and after it runs
- Use `@wraps(func)` to preserve the wrapped function's metadata
- No parameters: use `@log_call` (no parentheses)  # so, python does -- greet = log_call(greet) -- with parentheses would -- Python does: greet = log_call()(greet)
First log_call() is called with no arguments.
Whatever it returns is then used as the decorator and called with greet.

## Example

```python
@log_call
def greet(name: str) -> str:
    return f"Hello, {name}!"

greet("World")
# Before: greet
# After: greet
# (main prints the return value: Hello, World!)
```

## Files

- **exercise.py** — Skeleton with TODO; implement the decorator.
- **solution.py** — Reference solution.
