# 14. Merge Intervals

**Category:** Intervals  
**Difficulty:** Medium

## Problem

Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of non-overlapping intervals that cover all intervals in the input.

## Examples

- Input: `intervals = [[1,3],[2,6],[8,10],[15,18]]` → Output: `[[1,6],[8,10],[15,18]]`
- Input: `intervals = [[1,4],[4,5]]` → Output: `[[1,5]]`
- Input: `intervals = [[1,4],[0,4]]` → Output: `[[0,4]]`

## Constraints

- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`

## Complexity

- **Time:** O(n log n) for sort
- **Space:** O(log n) for sort; O(n) for output

## Interview tip

Sort by start. Then iterate: if current overlaps with last merged (current.start <= last.end), merge by extending last.end; else append new interval.
