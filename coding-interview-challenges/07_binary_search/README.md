# 7. Binary Search

**Category:** Binary Search  
**Difficulty:** Easy

## Problem

Given a **sorted** array of integers `nums` and an integer `target`, return the index of `target` if it is in `nums`, otherwise return `-1`.

## Examples

- Input: `nums = [-1,0,3,5,9,12]`, `target = 9` → Output: `4`
- Input: `nums = [-1,0,3,5,9,12]`, `target = 2` → Output: `-1`
- Input: `nums = [5]`, `target = 5` → Output: `0`

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i], target <= 10^4`
- `nums` is sorted in ascending order.

## Complexity

- **Time:** O(log n)
- **Space:** O(1)

## Interview tip

Classic template: `lo`, `hi`; while `lo <= hi`, `mid = (lo + hi) // 2`; compare with target and narrow range. Avoid off-by-one by being consistent (e.g. `hi = mid - 1` when `nums[mid] > target`).
