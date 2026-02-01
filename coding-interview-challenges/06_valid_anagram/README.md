# 6. Valid Anagram

**Category:** String / Hash  
**Difficulty:** Easy

## Problem

Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`. An anagram is formed by rearranging the letters of another, using all letters exactly once.

## Examples

- Input: `s = "anagram"`, `t = "nagaram"` → Output: `True`
- Input: `s = "rat"`, `t = "car"` → Output: `False`
- Input: `s = "a"`, `t = "ab"` → Output: `False`

## Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

## Complexity

- **Time:** O(n) with a single counter (or O(n log n) with sort)
- **Space:** O(1) if we consider alphabet size fixed (counter of 26 chars)

## Interview tip

Option 1: Count chars in `s`, decrement for `t`; all counts must be 0. Option 2: `sorted(s) == sorted(t)`.
