"""
Drill 6: Write a Context Manager
Fill in the TODOs. See README.md for the problem description.
"""

import time
from contextlib import contextmanager


@contextmanager
def timer():
    """
    Context manager that prints execution time on exit.
    with timer():
        do_something()
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Elapsed: {elapsed:.2f}s")


def main() -> None:
    with timer():
        time.sleep(0.1)
    print("Done")


if __name__ == "__main__":
    main()
