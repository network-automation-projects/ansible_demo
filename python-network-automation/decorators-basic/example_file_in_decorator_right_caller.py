"""
Caller module: uses the RIGHT decorator (inspect.getfile(wrapped_func)).
Run this file and see: config_path points to THIS file's directory
(caller), not the decorator's.
"""
from example_file_in_decorator_right_decorator import with_config


@with_config
def my_handler(config_path=None):
    return config_path


if __name__ == "__main__":
    path = my_handler()
    print("MYDEBUG → Config path (right):", path)
    print("  → This is next to this (caller) file, as intended.")
