# 8. Maximum Subarray (Kadane's Algorithm)

**Category:** Array / DP  
**Difficulty:** Medium

## Problem

Given an integer array `nums`, find the subarray with the largest sum and return that sum.

## Examples

- Input: `nums = [-2,1,-3,4,-1,2,1,-5,4]` → Output: `6` (subarray `[4,-1,2,1]`)
- Input: `nums = [1]` → Output: `1`
- Input: `nums = [5,4,-1,7,8]` → Output: `23` (entire array)

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

## Complexity

- **Time:** O(n)
- **Space:** O(1)

## Interview tip

Kadane: at each position, either extend the current subarray or start fresh. `cur = max(nums[i], cur + nums[i])`, then `best = max(best, cur)`.
