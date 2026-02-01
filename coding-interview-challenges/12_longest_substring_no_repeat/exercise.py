"""
Longest Substring Without Repeating Characters: sliding window.
Time: O(n), Space: O(min(n, alphabet))
"""


def length_of_longest_substring(s: str) -> int:
    """Sliding window: expand right, shrink left on duplicate."""
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    print("All examples passed.")
