# 13. 3Sum

**Category:** Array / Two pointers  
**Difficulty:** Medium

## Problem

Given an integer array `nums`, return all unique triplets `[nums[i], nums[j], nums[k]]` such that `i != j != k` and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

## Examples

- Input: `nums = [-1,0,1,2,-1,-4]` → Output: `[[-1,-1,2],[-1,0,1]]`
- Input: `nums = [0,1,1]` → Output: `[]`
- Input: `nums = [0,0,0]` → Output: `[[0,0,0]]`

## Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

## Complexity

- **Time:** O(n^2) — sort O(n log n), then for each first element, two-pointer scan
- **Space:** O(1) excluding output; O(log n) for sort

## Interview tip

Sort the array. For each index `i`, use two pointers (left = i+1, right = end) to find pairs that sum to `-nums[i]`. Skip duplicates for `i`, left, and right.
