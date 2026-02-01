"""
Product of Array Except Self: answer[i] = product of all elements except nums[i].
Time: O(n), Space: O(1) excluding output
"""


def product_except_self(nums: list[int]) -> list[int]:
    """Prefix pass then suffix pass (reuse output for prefix)."""
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    print("All examples passed.")
