# 12. Longest Substring Without Repeating Characters

**Category:** String / Sliding window  
**Difficulty:** Medium

## Problem

Given a string `s`, find the length of the longest substring without repeating characters.

## Examples

- Input: `s = "abcabcbb"` → Output: `3` ("abc")
- Input: `s = "bbbbb"` → Output: `1` ("b")
- Input: `s = "pwwkew"` → Output: `3` ("wke" or "kew")
- Input: `s = ""` → Output: `0`

## Constraints

- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols, spaces.

## Complexity

- **Time:** O(n)
- **Space:** O(min(n, alphabet size)) for the char set

## Interview tip

Sliding window + set: expand right, add char; when duplicate, shrink left until no duplicate. Track max length.
