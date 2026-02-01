"""
Reverse Linked List: reverse a singly linked list in place.
Time: O(n), Space: O(1)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Iterative: prev, curr, next; point curr to prev and advance."""
    prev: Optional[ListNode] = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def list_to_nodes(nums: list[int]) -> Optional[ListNode]:
    if not nums:
        return None
    head = ListNode(nums[0])
    cur = head
    for x in nums[1:]:
        cur.next = ListNode(x)
        cur = cur.next
    return head


def nodes_to_list(head: Optional[ListNode]) -> list[int]:
    out: list[int] = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    h = list_to_nodes([1, 2, 3, 4, 5])
    assert nodes_to_list(reverse_list(h)) == [5, 4, 3, 2, 1]
    h2 = list_to_nodes([1, 2])
    assert nodes_to_list(reverse_list(h2)) == [2, 1]
    assert nodes_to_list(reverse_list(None)) == []
    print("All examples passed.")
