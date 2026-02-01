# 16. Product of Array Except Self

**Category:** Array  
**Difficulty:** Medium

## Problem

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`. You must write an algorithm that runs in O(n) time and **without using the division operation**.

## Examples

- Input: `nums = [1,2,3,4]` → Output: `[24,12,8,6]`
- Input: `nums = [-1,1,0,-3,3]` → Output: `[0,0,9,0,0]`

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- Product of any prefix or suffix fits in a 32-bit integer.

## Complexity

- **Time:** O(n)
- **Space:** O(1) if output array doesn't count; otherwise O(n) for output

## Interview tip

Prefix/suffix: `answer[i] = prefix[i-1] * suffix[i+1]`. Build prefix in one pass (left to right), then suffix in a second pass (right to left), or combine in one pass by computing prefix in output then multiplying by suffix on the fly.
