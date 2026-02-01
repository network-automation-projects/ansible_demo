# 5. Valid Palindrome

**Category:** String / Two pointers  
**Difficulty:** Easy

## Problem

Given a string `s`, return `True` if it is a palindrome after converting to lowercase and removing non-alphanumeric characters. Empty string is considered a palindrome.

## Examples

- Input: `s = "A man, a plan, a canal: Panama"` → Output: `True`
- Input: `s = "race a car"` → Output: `False`
- Input: `s = " "` → Output: `True`

## Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

## Complexity

- **Time:** O(n)
- **Space:** O(1) if we use two pointers; O(n) if we build a filtered string first.

## Interview tip

Two pointers: left at start, right at end; skip non-alphanumeric; compare (lowercased) chars; move inward until they meet.
