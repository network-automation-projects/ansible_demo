"""
Climbing Stairs: distinct ways to climb n steps (1 or 2 per step).
Time: O(n), Space: O(1)
"""


def climb_stairs(n: int) -> int:
    """Fibonacci: a, b = 1, 1; then a, b = b, a+b for n-1 steps."""
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(4) == 5
    print("All examples passed.")
