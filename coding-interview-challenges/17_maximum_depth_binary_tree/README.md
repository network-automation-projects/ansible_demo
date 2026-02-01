# 17. Maximum Depth of Binary Tree

**Category:** Tree  
**Difficulty:** Easy

## Problem

Given the root of a binary tree, return its maximum depth (number of nodes along the longest path from root to a leaf).

## Examples

- Input: `root = [3,9,20,null,null,15,7]` → Output: `3`
- Input: `root = [1,null,2]` → Output: `2`
- Input: `root = []` → Output: `0`

## Constraints

- Number of nodes in `[0, 10^4]`
- `-100 <= Node.val <= 100`

## Complexity

- **Time:** O(n)
- **Space:** O(h) for recursion stack, h = height

## Interview tip

Recursion: if root is None return 0; else return 1 + max(left_depth, right_depth). Or BFS level-order and count levels.
