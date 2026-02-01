"""
Invert Binary Tree: swap left and right child at every node.
Time: O(n), Space: O(h)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Recursion: swap left/right, then invert both subtrees."""
    if root is None:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root


def build_tree(values: list[Optional[int]], i: int = 0) -> Optional[TreeNode]:
    """Build tree from list (level-order)."""
    if i >= len(values) or values[i] is None:
        return None
    node = TreeNode(values[i])
    node.left = build_tree(values, 2 * i + 1)
    node.right = build_tree(values, 2 * i + 2)
    return node


def tree_to_list(root: Optional[TreeNode]) -> list[Optional[int]]:
    """Level-order list for comparison."""
    if root is None:
        return []
    out: list[Optional[int]] = []
    q: list[Optional[TreeNode]] = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        q.append(node.left)
        q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    root = build_tree([4, 2, 7, 1, 3, 6, 9])
    invert_tree(root)
    assert tree_to_list(root) == [4, 7, 2, 9, 6, 3, 1]

    root2 = build_tree([2, 1, 3])
    invert_tree(root2)
    assert tree_to_list(root2) == [2, 3, 1]

    assert invert_tree(None) is None
    print("All examples passed.")
