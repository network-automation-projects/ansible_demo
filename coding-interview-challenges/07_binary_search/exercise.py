"""
Binary Search: find index of target in sorted array, or -1.
Time: O(log n), Space: O(1)
"""


def binary_search(nums: list[int], target: int) -> int:
    """Classic binary search with lo/hi."""
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert binary_search([5], 5) == 0
    print("All examples passed.")
