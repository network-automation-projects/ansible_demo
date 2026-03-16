# Ready-to-use decorators from Real Python and workplace patterns.
# Copy-paste as needed.

from functools import wraps
from typing import Any, Callable
import inspect
import time

# -----------------------------------------------------------------------------
# @timer — single-run wall-clock timing
# Use time.perf_counter() (not datetime or time.time). See python-from-basic-to-tools.md
# -----------------------------------------------------------------------------


def timer(func: Callable) -> Callable:
    """Print elapsed time for decorated function. Use perf_counter for accuracy."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}() took {elapsed:.4f} seconds")
        return result

    return wrapper


# Usage: @timer
# def my_func(): ...

# -----------------------------------------------------------------------------
# @debug — print function signature and return value
# Uses inspect.signature for name=value output (e.g. make_greeting(name='Maria', age=116))
# -----------------------------------------------------------------------------


def debug(func: Callable) -> Callable:
    """Print calling signature and return value. Useful for development."""

    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        args_str = ", ".join(f"{name}={value!r}" for name, value in bound.arguments.items())
        result = func(*args, **kwargs)
        print(f"Calling {func.__name__}({args_str})")
        print(f"{func.__name__}() returned {result!r}")
        return result

    return wrapper


# Usage: @debug
# def greet(name: str, age: int = 0): ...

# -----------------------------------------------------------------------------
# @register — add function to PLUGINS dict by __name__
# Curated list of functions for plugin/task dispatch
# -----------------------------------------------------------------------------

PLUGINS: dict[str, Callable] = {}


def register(func: Callable) -> Callable:
    """Register a function as a plugin. PLUGINS[func.__name__] = func."""

    PLUGINS[func.__name__] = func
    return func


# Usage: @register
# def backup_config(host): ...
# PLUGINS["backup_config"](host)

# -----------------------------------------------------------------------------
# @task(name) — register with custom name (decorator factory)
# Use when you want a different key than func.__name__ (e.g. "backup" vs "backup_config")
# -----------------------------------------------------------------------------

TASKS: dict[str, Callable] = {}


def task(name: str) -> Callable:
    """Register function under custom name. Use for CLI dispatch: TASKS[args.command]()."""

    def decorator(func: Callable) -> Callable:
        TASKS[name] = func
        return func

    return decorator


# Usage: @task("backup")
# def backup_config(host): ...
# TASKS["backup"](host)

# -----------------------------------------------------------------------------
# @slow_down — sleep before each call
# Useful for rate limiting, demos, or recursive functions where each call gets a delay
# -----------------------------------------------------------------------------


def slow_down(func: Callable) -> Callable:
    """Sleep 0.5 seconds before calling decorated function."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        time.sleep(0.5)
        return func(*args, **kwargs)

    return wrapper


# Usage: @slow_down
# def countdown(n): ...
