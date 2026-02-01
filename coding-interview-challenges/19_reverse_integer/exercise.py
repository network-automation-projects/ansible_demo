"""
Reverse Integer: reverse digits; return 0 if overflow.
Time: O(log |x|), Space: O(1)
"""


def reverse_int(x: int) -> int:
    """Extract digits; build result; check 32-bit overflow."""
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    assert reverse_int(123) == 321
    assert reverse_int(-123) == -321
    assert reverse_int(120) == 21
    assert reverse_int(1534236469) == 0
    print("All examples passed.")
