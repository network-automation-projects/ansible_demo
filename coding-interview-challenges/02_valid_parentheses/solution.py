"""
Valid Parentheses: check if brackets are balanced and correctly nested.
Time: O(n), Space: O(n)
"""


def valid_parentheses(s: str) -> bool:
    """Stack: push openers, pop and match on closers."""
    stack: list[str] = []
    pairs = {"(": ")", "{": "}", "[": "]"}
    for c in s:
        if c in pairs: # means for each char in string, test if it is one of the key values (an opener)
            stack.append(c)
        else:
            #print(pairs[stack[-1]])
            if not stack or pairs[stack[-1]] != c: # means if there is nothing in stack yet or the last element in stack is not the same as the current element, return False
                return False #“No matching opener (empty stack) or wrong closer → invalid, return False.”
            #the character was not a closer, so pop it off the stack
            stack.pop()
    return len(stack) == 0 # means if the stack is empty, return True


if __name__ == "__main__":
    assert valid_parentheses("()") is True
    assert valid_parentheses("()[]{}") is True
    assert valid_parentheses("(]") is False
    assert valid_parentheses("([)]") is False
    assert valid_parentheses("{[]}") is True
    print("All examples passed.")
