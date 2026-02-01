"""
Missing Number: find the single number in [0, n] missing from nums.
Time: O(n), Space: O(1)
"""


def missing_number(nums: list[int]) -> int:
    """Sum of 0..n minus sum(nums) = missing."""
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    assert missing_number([3, 0, 1]) == 2
    assert missing_number([0, 1]) == 2
    assert missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    print("All examples passed.")
