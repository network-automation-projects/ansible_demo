"""
Maximum Depth of Binary Tree: longest path from root to leaf.
Time: O(n), Space: O(h)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def max_depth(root: Optional[TreeNode]) -> int:
    """Recursion: 0 if None, else 1 + max(left, right)."""
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def build_tree(values: list[Optional[int]], i: int = 0) -> Optional[TreeNode]:
    """Build tree from list (level-order); None = missing node."""
    if i >= len(values) or values[i] is None:
        return None
    node = TreeNode(values[i])
    node.left = build_tree(values, 2 * i + 1)
    node.right = build_tree(values, 2 * i + 2)
    return node


if __name__ == "__main__":
    # [3,9,20,null,null,15,7] -> depth 3
    root = build_tree([3, 9, 20, None, None, 15, 7])
    assert max_depth(root) == 3

    root2 = build_tree([1, None, 2])
    assert max_depth(root2) == 2

    assert max_depth(None) == 0
    print("All examples passed.")
