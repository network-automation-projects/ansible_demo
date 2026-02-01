# 4. Best Time to Buy and Sell Stock

**Category:** Array / DP  
**Difficulty:** Easy

## Problem

You are given an array `prices` where `prices[i]` is the price of a stock on day `i`. You want to maximize profit by choosing one day to buy and a different day in the future to sell. Return the maximum profit; if no profit is possible, return 0.

## Examples

- Input: `prices = [7,1,5,3,6,4]` → Output: `5` (buy at 1, sell at 6)
- Input: `prices = [7,6,4,3,1]` → Output: `0`
- Input: `prices = [1,2]` → Output: `1`

## Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

## Complexity

- **Time:** O(n) — one pass, track min price and max profit
- **Space:** O(1)

## Interview tip

Track the minimum price seen so far; at each day, profit = price - min_so_far. Update max profit.
