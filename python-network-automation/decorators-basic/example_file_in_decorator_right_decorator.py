"""
RIGHT: Decorator uses inspect.getfile(wrapped_func) — so the path is
the CALLER's file (where the decorated function is defined), not this file.
"""
import os
import inspect


def load_config_next_to_module(module_file_path):
    """Load config from the same directory as the given module file."""
    config_dir = os.path.dirname(module_file_path)
    config_path = os.path.join(config_dir, "config.json")
    return config_path


def with_config(wrapped_func):
    caller_file = inspect.getfile(wrapped_func)

    def wrapper(*args, **kwargs):
        config_path = load_config_next_to_module(caller_file)
        return wrapped_func(*args, **kwargs, config_path=config_path)
    return wrapper
