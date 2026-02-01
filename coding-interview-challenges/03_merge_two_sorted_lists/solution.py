"""
Merge Two Sorted Lists: merge two sorted linked lists in place.
Time: O(n + m), Space: O(1)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def merge_two_lists(
    list1: Optional[ListNode],
    list2: Optional[ListNode],
) -> Optional[ListNode]:
    """Iterative merge with dummy head."""
    dummy = ListNode(0)
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next


def list_to_nodes(nums: list[int]) -> Optional[ListNode]:
    """Build a linked list from a list of ints."""
    if not nums:
        return None
    head = ListNode(nums[0])
    cur = head
    for x in nums[1:]:
        cur.next = ListNode(x)
        cur = cur.next
    return head


def nodes_to_list(head: Optional[ListNode]) -> list[int]:
    """Convert linked list to list for comparison."""
    out: list[int] = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    l1 = list_to_nodes([1, 2, 4])
    l2 = list_to_nodes([1, 3, 4])
    merged = merge_two_lists(l1, l2)
    assert nodes_to_list(merged) == [1, 1, 2, 3, 4, 4]

    assert nodes_to_list(merge_two_lists(None, None)) == []
    assert nodes_to_list(merge_two_lists(None, list_to_nodes([0]))) == [0]
    print("All examples passed.")
