# 9. Reverse Linked List

**Category:** Linked List  
**Difficulty:** Easy

## Problem

Given the head of a singly linked list, reverse the list and return the new head.

## Examples

- Input: `head = [1,2,3,4,5]` → Output: `[5,4,3,2,1]`
- Input: `head = [1,2]` → Output: `[2,1]`
- Input: `head = []` → Output: `[]`

## Constraints

- Number of nodes in the list is in `[0, 5000]`.
- `-5000 <= Node.val <= 5000`

## Complexity

- **Time:** O(n)
- **Space:** O(1) iterative; O(n) recursive (stack)

## Interview tip

Iterative: three pointers — `prev`, `curr`, `next`. At each step: save next, point curr to prev, advance prev and curr.
