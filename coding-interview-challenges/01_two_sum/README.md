# 1. Two Sum

**Category:** Array / Hash  
**Difficulty:** Easy

## Problem

Given an array of integers `nums` and an integer `target`, return *indices* of the two numbers such that they add up to `target`. You may assume exactly one solution exists, and you may not use the same element twice.

## Examples

- Input: `nums = [2, 7, 11, 15]`, `target = 9` → Output: `[0, 1]` (2 + 7 = 9)
- Input: `nums = [3, 2, 4]`, `target = 6` → Output: `[1, 2]`
- Input: `nums = [3, 3]`, `target = 6` → Output: `[0, 1]`

## Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- Exactly one valid answer exists.

## Complexity

- **Time:** O(n) — single pass with hash map
- **Space:** O(n) — hash map of value → index

## Follow-ups

- Two Sum II (sorted array, two pointers)
- 3Sum, 4Sum
