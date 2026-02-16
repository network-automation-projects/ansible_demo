"""
WRONG: Decorator uses __file__ — so the path is THIS file (the decorator's),
not the file where @with_config was applied.
"""
import os


def load_config_next_to_caller():
    """Uses __file__ here — this is the DECORATOR's file."""
    config_dir = os.path.dirname(__file__)
    config_path = os.path.join(config_dir, "config.json")
    return config_path  # return path for demo (no real file needed)


def with_config(wrapped_func):
    def wrapper(*args, **kwargs):
        config_path = load_config_next_to_caller()
        return wrapped_func(*args, **kwargs, config_path=config_path)
    return wrapper
