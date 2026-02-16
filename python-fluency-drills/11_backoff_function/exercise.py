"""
Drill 11: Implement Exponential Backoff Function
Fill in the TODOs. See README.md for the problem description.
"""

import random


def backoff(base_delay: float, attempt: int, jitter: bool = False) -> float:
    """
    Return delay for given attempt: base_delay * 2 ** attempt.
    If jitter: add random variation (e.g. ±25%).
    """
    # TODO: delay = base_delay * (2 ** attempt)
    # TODO: if jitter: delay *= (0.75 + 0.5 * random.random())
    raise NotImplementedError("Implement me")


def main() -> None:
    for i in range(4):
        print(f"attempt {i}: {backoff(1.0, i):.2f}s")
    print("With jitter:")
    for i in range(4):
        print(f"attempt {i}: {backoff(1.0, i, jitter=True):.2f}s")


if __name__ == "__main__":
    main()
