"""
Reverse Integer: reverse digits; return 0 if overflow.
Time: O(log |x|), Space: O(1)
"""


def reverse_int(x: int) -> int:
    """Extract digits; build result; check 32-bit overflow."""
    INT_MAX = 2**31 - 1
    INT_MIN = -(2**31)
    sign = 1 if x >= 0 else -1
    x = abs(x)
    rev = 0
    while x:
        digit = x % 10
        x //= 10
        if rev > INT_MAX // 10 or (rev == INT_MAX // 10 and digit > 7):
            return 0
        rev = rev * 10 + digit
    return sign * rev


if __name__ == "__main__":
    assert reverse_int(123) == 321
    assert reverse_int(-123) == -321
    assert reverse_int(120) == 21
    assert reverse_int(1534236469) == 0
    print("All examples passed.")
