"""
3Sum: find all unique triplets that sum to 0.
Time: O(n^2), Space: O(1) excluding output
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    """Sort, then for each first element run two-pointer for the pair."""
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    result = three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted(result) == sorted([[-1, -1, 2], [-1, 0, 1]])
    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    print("All examples passed.")
