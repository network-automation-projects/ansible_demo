# 10. Contains Duplicate

**Category:** Array / Hash  
**Difficulty:** Easy

## Problem

Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

## Examples

- Input: `nums = [1,2,3,1]` → Output: `True`
- Input: `nums = [1,2,3,4]` → Output: `False`
- Input: `nums = [1,1,1,3,3,4,3,2,4,2]` → Output: `True`

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

## Complexity

- **Time:** O(n) with set; O(n log n) with sort
- **Space:** O(n) with set; O(1) with sort (if in-place)

## Interview tip

Set: if we've seen the value before, return True. Alternatively: `len(nums) != len(set(nums))`.
