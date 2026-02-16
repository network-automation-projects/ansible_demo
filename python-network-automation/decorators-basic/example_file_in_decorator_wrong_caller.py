"""
Caller module: uses the WRONG decorator (one that uses __file__).
Run this file and see: config_path points to the DECORATOR's directory,
not this file's directory.
"""
from example_file_in_decorator_wrong_decorator import with_config


@with_config
def my_handler(config_path=None):
    return config_path


if __name__ == "__main__":
    path = my_handler()
    print("MYDEBUG → Config path (wrong):", path)
    print("  → This is next to the decorator file, not this (caller) file.")
