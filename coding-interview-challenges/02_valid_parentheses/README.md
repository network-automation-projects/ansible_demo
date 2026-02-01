# 2. Valid Parentheses

**Category:** Stack  
**Difficulty:** Easy

## Problem

Given a string `s` containing only `(`, `)`, `{`, `}`, `[`, `]`, determine if the input string is valid. Valid means: open brackets are closed by the same type, and in the correct order.

## Examples

- Input: `s = "()"` → Output: `True`
- Input: `s = "()[]{}"` → Output: `True`
- Input: `s = "(]"` → Output: `False`
- Input: `s = "([)]"` → Output: `False`
- Input: `s = "{[]}"` → Output: `True`

## Constraints

- `1 <= s.length <= 10^4`
- `s` contains only the characters above.

## Complexity

- **Time:** O(n)
- **Space:** O(n) for the stack

## Interview tip

Use a stack: push opening brackets, pop and match on closing. If stack is empty when we see a closer, or leftover at end, invalid.
