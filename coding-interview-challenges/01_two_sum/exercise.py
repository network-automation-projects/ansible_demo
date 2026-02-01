"""
Two Sum: return indices of two numbers that add up to target.
Time: O(n), Space: O(n) #this is the time and space complexity of the algorithm
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """One-pass hash map: for each num, check if (target - num) is already seen."""
    pairs = {} #this will contain the answer pairs
    try:
        for i in enumerate(nums):
            if 


    return pairs
    
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
    print("All examples passed.")
