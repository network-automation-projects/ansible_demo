"""
Contains Duplicate: return True if any value appears at least twice.
Time: O(n), Space: O(n)
"""


def contains_duplicate(nums: list[int]) -> bool:
    """Track seen in a set; return True on first repeat."""
    seen: set[int] = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False


if __name__ == "__main__":
    assert contains_duplicate([1, 2, 3, 1]) is True
    assert contains_duplicate([1, 2, 3, 4]) is False
    assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    print("All examples passed.")
