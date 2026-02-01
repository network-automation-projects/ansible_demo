# 19. Reverse Integer

**Category:** Math  
**Difficulty:** Medium

## Problem

Given a signed 32-bit integer `x`, return `x` with its digits reversed. If reversing causes the value to go outside the signed 32-bit integer range `[-2^31, 2^31 - 1]`, then return 0. Assume the environment does not allow you to store 64-bit integers.

## Examples

- Input: `x = 123` → Output: `321`
- Input: `x = -123` → Output: `-321`
- Input: `x = 120` → Output: `21`
- Input: `x = 1534236469` → Output: `0` (overflow)

## Constraints

- `-2^31 <= x <= 2^31 - 1`

## Complexity

- **Time:** O(log |x|) — number of digits
- **Space:** O(1)

## Interview tip

Extract digits with % 10 and // 10; build result. Before adding next digit, check overflow: if result > MAX//10 or (result == MAX//10 and digit > 7), return 0. Handle sign separately.
