"""
3Sum: find all unique triplets that sum to 0.
Time: O(n^2), Space: O(1) excluding output
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    """Sort, then for each first element run two-pointer for the pair."""
    nums = sorted(nums)
    out: list[list[int]] = []
    for i in range(len(nums)):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        target = -nums[i]
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[left] + nums[right]
            if s == target:
                out.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1
    return out


if __name__ == "__main__":
    result = three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted(result) == sorted([[-1, -1, 2], [-1, 0, 1]])
    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    print("All examples passed.")
