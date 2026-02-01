# 18. Climbing Stairs

**Category:** DP  
**Difficulty:** Easy

## Problem

You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

## Examples

- Input: `n = 2` → Output: `2` (1+1 or 2)
- Input: `n = 3` → Output: `3` (1+1+1, 1+2, 2+1)
- Input: `n = 4` → Output: `5`

## Constraints

- `1 <= n <= 45`

## Complexity

- **Time:** O(n)
- **Space:** O(1) with two variables (Fibonacci-style)

## Interview tip

dp[i] = ways to reach step i = dp[i-1] + dp[i-2]. Base: dp[0]=1, dp[1]=1. Can do with two vars: a, b = 1, 1; for _ in range(n-1): a, b = b, a+b; return b.
