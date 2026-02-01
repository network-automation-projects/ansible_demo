# 3. Merge Two Sorted Lists

**Category:** Linked List  
**Difficulty:** Easy

## Problem

Merge two sorted linked lists and return the head of the merged list. The list should be made by splicing together the nodes of the first two lists.

## Examples

- Input: `list1 = [1,2,4]`, `list2 = [1,3,4]` → Output: `[1,1,2,3,4,4]`
- Input: `list1 = []`, `list2 = []` → Output: `[]`
- Input: `list1 = []`, `list2 = [0]` → Output: `[0]`

## Constraints

- Number of nodes in both lists is in `[0, 50]`.
- Node values in range `[-100, 100]`.
- Both lists are sorted in non-decreasing order.

## Complexity

- **Time:** O(n + m)
- **Space:** O(1) for iterative (just a dummy head and pointer)

## Interview tip

Use a dummy head and a tail pointer; advance the list that has the smaller current value.
