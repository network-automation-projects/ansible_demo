"""
Two Sum: return indices of two numbers that add up to target.
Time: O(n), Space: O(n)
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """One-pass hash map: for each num, check if (target - num) is already seen."""
    seen: dict[int, int] = {}
    for i, n in enumerate(nums): #so i is the first value and n is the second?
                                        #yes, i is the index and n is the value at that index
        need = target - n #why target - n?
                            #because we need to find the two numbers that add up to the target
                            #so if we have the target and the current number, we can find the other number by subtracting the current number from the target
                            #so if we have the target and the current number, we can find the other number by subtracting the current number from the target
        if need in seen:
            return [seen[need], i]
        seen[n] = i
    return []  # guaranteed one solution


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
    print("All examples passed.")
