"""
Drill 0: Write a Function — Reference solution.
"""


def add(a: int | float, b: int | float) -> int | float:
    """Return the sum of a and b."""
    return a + b


def main() -> None:
    print("add(2, 3) =", add(2, 3))
    print("add(-1, 1) =", add(-1, 1))


if __name__ == "__main__":
    main()
