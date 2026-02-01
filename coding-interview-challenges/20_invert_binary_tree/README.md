# 20. Invert Binary Tree

**Category:** Tree  
**Difficulty:** Easy

## Problem

Given the root of a binary tree, invert the tree and return its root. Inverting means: swap the left and right subtree of every node.

## Examples

- Input: `root = [4,2,7,1,3,6,9]` → Output: `[4,7,2,9,6,3,1]` (structure with swapped children)
- Input: `root = [2,1,3]` → Output: `[2,3,1]`
- Input: `root = []` → Output: `[]`

## Constraints

- Number of nodes in `[0, 100]`
- `-100 <= Node.val <= 100`

## Complexity

- **Time:** O(n)
- **Space:** O(h) for recursion

## Interview tip

Recursion: if root is None return None. Swap root.left and root.right, then recursively invert left and right. Return root.
