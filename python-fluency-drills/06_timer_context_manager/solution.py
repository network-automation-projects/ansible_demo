"""
Drill 6: Write a Context Manager — Reference solution.
"""

import time
from contextlib import contextmanager


@contextmanager
def timer():
    """
    Context manager that prints execution time on exit.
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Elapsed: {elapsed:.2f}s")


class Timer:
    """
    Class-based timer context manager (stretch).
    """

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args: object) -> None:
        elapsed = time.perf_counter() - self._start
        print(f"Elapsed: {elapsed:.2f}s")


def main() -> None:
    print("Using @contextmanager:")
    with timer():
        time.sleep(0.1)

    print("Using class:")
    with Timer():
        time.sleep(0.05)
    print("Done")


if __name__ == "__main__":
    main()
