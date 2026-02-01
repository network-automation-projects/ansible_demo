"""
Maximum Subarray (Kadane): largest sum of any contiguous subarray.
Time: O(n), Space: O(1)
"""


def max_subarray_sum(nums: list[int]) -> int:
    """Kadane: cur = max(x, cur + x), best = max(best, cur)."""
    if not nums:
        return 0
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


if __name__ == "__main__":
    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray_sum([1]) == 1
    assert max_subarray_sum([5, 4, -1, 7, 8]) == 23
    print("All examples passed.")
