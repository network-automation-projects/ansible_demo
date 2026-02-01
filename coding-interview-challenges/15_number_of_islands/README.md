# 15. Number of Islands

**Category:** Graph / DFS-BFS  
**Difficulty:** Medium

## Problem

Given an `m x n` 2D binary grid where `'1'` is land and `'0'` is water, return the number of islands. An island is formed by connecting adjacent lands horizontally or vertically.

## Examples

- Input: `grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]` → Output: `1`
- Input: `grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]` → Output: `3`

## Constraints

- `m == grid.length`, `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`.

## Complexity

- **Time:** O(m * n)
- **Space:** O(m * n) for recursion/queue in worst case; O(1) if we mutate grid to mark visited

## Interview tip

For each unvisited `'1'`, run DFS or BFS to mark the whole island (e.g. set to `'0'` or use a visited set). Count how many times we start a new island.
