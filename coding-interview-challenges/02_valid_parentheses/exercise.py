"""
Valid Parentheses: check if brackets are balanced and correctly nested.
Time: O(n), Space: O(n)
"""


def valid_parentheses(s: str) -> bool:
    """Stack: push openers, pop and match on closers."""

    # a variable to hold the list of characters
    stack = []
    pairs = {"(": ")", "{": "}", "[": "]"} #to check against
    #for each character in the string
    for c in s:
        #test if it is one of the key values (an opener)
        if c in pairs():
            # it is a match for an opener
            # add it to the stack
            stack.append()
        else:
            # it wasn't a match for an opener, see if it's a closer
            if not stack:  # if there is something in stack to test
                if c != pairs[stack-1]: 
                    #no matching opener or incorrect closer, return False
                    return False
                else:
                    #it was a closer, pop it off the stack
                    stack.pop()
            return False
    return len(stack) == 0 # means if the stack is empty, return True

    




if __name__ == "__main__":
    assert valid_parentheses("()") is True
    assert valid_parentheses("()[]{}") is True
    assert valid_parentheses("(]") is False
    assert valid_parentheses("([)]") is False
    assert valid_parentheses("{[]}") is True
    print("All examples passed.")




    #     # a variable to hold the list of 
    # stack = []
    # # a dictionary to hold the pairs of parentheses
    # pairs = {"(": ")", "{": "}", "[": "]"}
    # for c in s: # for each character in the string being tested
    #     if c in pairs: #if that character is in the pairs dictionary
    #         # add it to stack to check
    #         stack.append(c)

    #     else: #if that character is not in the pairs dictionary then it doesn't matter?
    #         if not stack or pairs[stack[-1]] != c:
    #             return False
    #         stack.pop()
        
    # return len(stack) == 0 # return true if stack is empty of errors




    # try:
    #     #variable to hold the pieces as we test them?
    #     #so we can pop them off as we test them?
    #     stack = [] 
    #     # a dictionary to hold the pairs of parentheses
    #     pairs = {"(": ")", "{": "}", "[": "]"} 
    #     for c in s: # for each character in the string
    #         if c in pairs: # if the character is in the pairs dictionary
    #             stack.append(c) # add the character to the stack
    #         else: # if the character is not in the pairs dictionary
    #             if not stack or pairs[stack[-1]] != c: #is there a clearer way to write this section: not stack or pairs[stack[-1]] != c:
    #                 # so above is saying if the stack is empty or the last element in the stack is not the same as the current element, return False
    #                 return False # return False
    #             stack.pop() # pop the last element from the stack
    #     return len(stack) == 0 # return True if the stack is empty, False otherwise
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return False

    #would this handle complex nested parentheses?

    # raise NotImplementedError("Implement me")