"""
Valid Anagram: check if t is an anagram of s (same chars, same counts).
Time: O(n), Space: O(1) for fixed alphabet
"""


def is_anagram(s: str, t: str) -> bool:
    """Single counter: increment for s, decrement for t; all zeros."""
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False
    assert is_anagram("a", "ab") is False
    print("All examples passed.")
