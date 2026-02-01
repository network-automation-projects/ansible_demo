# 11. Missing Number

**Category:** Array / Math  
**Difficulty:** Easy

## Problem

Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in that range that is missing from the array.

## Examples

- Input: `nums = [3,0,1]` → Output: `2` (n=3, range 0..3, 2 is missing)
- Input: `nums = [0,1]` → Output: `2`
- Input: `nums = [9,6,4,2,3,5,7,0,1]` → Output: `8`

## Constraints

- `n == nums.length`
- `1 <= n <= 10^4`
- `0 <= nums[i] <= n`
- All numbers are unique.

## Complexity

- **Time:** O(n)
- **Space:** O(1) with XOR or sum trick

## Interview tip

Sum of 0..n is `n*(n+1)//2`; subtract sum(nums) to get missing. Or XOR: xor all indices and values; result is the missing number.
