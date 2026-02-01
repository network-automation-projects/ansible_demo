"""
Valid Palindrome: alphanumeric-only, case-insensitive palindrome check.
Time: O(n), Space: O(1) with two pointers
"""


def is_palindrome(s: str) -> bool:
    """Two pointers; skip non-alphanumeric, compare lowercased."""
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            i += 1
            continue
        if not s[j].isalnum():
            j -= 1
            continue
        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True


if __name__ == "__main__":
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False
    assert is_palindrome(" ") is True
    print("All examples passed.")
