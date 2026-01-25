"""
Practice Exercises: Python Unpacking
=====================================
Fill in the blanks or complete the code to test your understanding of unpacking.
Run this file to check your answers!
"""

# ============================================================================
# Exercise 1: Basic Unpacking
# ============================================================================
# TODO: Unpack the list [10, 20, 30] into three variables: x, y, z
# Your code here:
# x, y, z = 

# ============================================================================
# Exercise 2: Extended Iterable Unpacking with *
# ============================================================================
# TODO: Unpack the list [1, 2, 3, 4, 5, 6, 7] so that:
#       first = 1
#       middle = [2, 3, 4, 5, 6] (all middle values)
#       last = 7
# Your code here:
# first, , last = [1, 2, 3, 4, 5, 6, 7]
# 
# ==========================================================================
# Exercise 3: Ignoring Values
# ============================================================================
# TODO: From the tuple ("skip", "ignore", "keep"), 
#       only unpack the third value into a variable called 'important'
# Your code here:
# important = 

# ============================================================================
# Exercise 4: Unpacking Nested Structures
# ============================================================================
# TODO: Unpack this nested structure correctly:
#       data = ("John", (30, "Developer"))
#       Get name, age, and profession as separate variables
# Your code here:
# data = ("John", (30, "Developer"))
# name, (age, profession) = 
# print(f"Name: {name}, Age: {age}, Profession: {profession}")

# ============================================================================
# Exercise 5: Unpacking in Function Arguments
# ============================================================================
# TODO: Create a function called 'sum_numbers' that accepts any number of 
#       arguments using *args and returns their sum
# Your code here:
# def sum_numbers( ):
#     # Your code here
#     pass

# Test it: sum_numbers(1, 2, 3, 4, 5) should return 15

# ============================================================================
# Exercise 6: Combining Lists with Unpacking
# ============================================================================
# TODO: Combine list_a = [1, 2, 3] and list_b = [7, 8, 9] into a new list
#       using unpacking, so the result is [1, 2, 3, 7, 8, 9]
list_a = [1, 2, 3]
list_b = [7, 8, 9]
# Your code here:
# combined = 

# ============================================================================
# Exercise 7: Unpacking Dictionaries with **
# ============================================================================
# TODO: Combine dict_a = {"x": 1, "y": 2} and dict_b = {"z": 3} into one dict
#       using unpacking
dict_a = {"x": 1, "y": 2}
dict_b = {"z": 3}
# Your code here:
# merged = 

# ============================================================================
# Exercise 8: Swapping Variables
# ============================================================================
# TODO: Swap the values of variables p and q using unpacking
p = 100
q = 200
# Your code here:


# ============================================================================
# Exercise 9: Challenge - Multiple Unpacking
# ============================================================================
# TODO: Given three lists, unpack them all into one combined list:
list1 = [1, 2]
list2 = [3, 4, 5]
list3 = [6]
# Your code here:
# all_combined = 

# ============================================================================
# Exercise 10: Challenge - Function with Keyword Arguments
# ============================================================================
# TODO: Create a function that accepts any keyword arguments using **kwargs
#       and prints them out as "key: value" pairs
# Your code here:
# def print_info( ):
#     # Your code here
#     pass

# Test it: print_info(name="Alice", age=25, city="NYC")

# ============================================================================
# TEST YOUR ANSWERS
# ============================================================================
# Uncomment the sections below to test your code:

# Exercise 1 Test
# print(f"Exercise 1 - x={x}, y={y}, z={z}")
# Expected: x=10, y=20, z=30

# Exercise 2 Test
# print(f"Exercise 2 - first={first}, middle={middle}, last={last}")
# Expected: first=1, middle=[2, 3, 4, 5, 6], last=7

# Exercise 3 Test
# print(f"Exercise 3 - important={important}")
# Expected: important=keep

# Exercise 4 Test
# print(f"Exercise 4 - Name: {name}, Age: {age}, Profession: {profession}")
# Expected: Name: John, Age: 30, Profession: Developer

# Exercise 5 Test
# print(f"Exercise 5 - sum={sum_numbers(1, 2, 3, 4, 5)}")
# Expected: sum=15

# Exercise 6 Test
# print(f"Exercise 6 - combined={combined}")
# Expected: combined=[1, 2, 3, 7, 8, 9]

# Exercise 7 Test
# print(f"Exercise 7 - merged={merged}")
# Expected: merged={'x': 1, 'y': 2, 'z': 3}

# Exercise 8 Test
# print(f"Exercise 8 - After swap: p={p}, q={q}")
# Expected: After swap: p=200, q=100

# Exercise 9 Test
# print(f"Exercise 9 - all_combined={all_combined}")
# Expected: all_combined=[1, 2, 3, 4, 5, 6]

# Exercise 10 Test
# print("Exercise 10:")
# print_info(name="Alice", age=25, city="NYC")
# Expected: name: Alice
#          age: 25
#          city: NYC



"""
Practice Exercises: Python Unpacking
=====================================
Fill in the blanks or complete the code to test your understanding of unpacking.
Run this file to check your answers!
"""

# ============================================================================
# Exercise 1: Basic Unpacking
# ============================================================================
# TODO: Unpack the list [10, 20, 30] into three variables: x, y, z
# Your code here:
x, y, z = [10, 20, 30]

# ============================================================================
# Exercise 2: Extended Iterable Unpacking with *
# ============================================================================
# TODO: Unpack the list [1, 2, 3, 4, 5, 6, 7] so that:
#       first = 1
#       middle = [2, 3, 4, 5, 6] (all middle values)
#       last = 7
# Your code here:
first, *_, last = [1, 2, 3, 4, 5, 6, 7]

# ============================================================================
# Exercise 3: Ignoring Values
# ============================================================================
# TODO: From the tuple ("skip", "ignore", "keep"), 
#       only unpack the third value into a variable called 'important'
# Your code here:
_, _, important =  ("skip", "ignore", "keep")

# ============================================================================
# Exercise 4: Unpacking Nested Structures
# ============================================================================
# TODO: Unpack this nested structure correctly:
#       data = ("John", (30, "Developer"))
#       Get name, age, and profession as separate variables
# Your code here:
data = ("John", (30, "Developer"))
name, (age, profession) = ("John", (30, "Developer")) 

# age = age[0] #is there a better way to do this?
# profession = profession[1] #is there a better way to do this?

#how would people unpack complex nested structures?

print(f"Name: {name}, Age: {age}, Profession: {profession}")

# ============================================================================
# Exercise 5: Unpacking in Function Arguments
# ============================================================================
# TODO: Create a function called 'sum_numbers' that accepts any number of 
#       arguments using *args and returns their sum
# Your code here:
def sum_numbers(*args):
    return sum(args)  

# sum_numbers(1, 2, 3, 4, 5) should return 15
print(f"Exercise 5 - sum={sum_numbers(1, 2, 3, 4, 5)}")

# ============================================================================
# Exercise 6: Combining Lists with Unpacking
# ============================================================================
# TODO: Combine list_a = [1, 2, 3] and list_b = [7, 8, 9] into a new list
#       using unpacking, so the result is [1, 2, 3, 7, 8, 9]
list_a = [1, 2, 3]
list_b = [7, 8, 9]
# Your code here:
combined = [*list_a, *list_b]
print(f"Exercise 6 - combined={combined}")

# ============================================================================
# Exercise 7: Unpacking Dictionaries with **
# ============================================================================
# TODO: Combine dict_a = {"x": 1, "y": 2} and dict_b = {"z": 3} into one dict
#       using unpacking
dict_a = {"x": 1, "y": 2}
dict_b = {"z": 3}
# Your code here:
merged = {**dict_a, **dict_b} #why **?
#because ** is used to unpack the dictionaries into the new dictionary
print(f"Exercise 7 - merged={merged}")

# interesting that with one *, it unpacks the dictionary into a list, 
# but with two **, it unpacks the dictionary into a dictionary
merged = {*dict_a, *dict_b} #why **?
#because ** is used to unpack the dictionaries into the new dictionary
print(f"Exercise 7 - merged but list not dictionary={merged}")

# merged = {dict_a, dict_b} #why not work?
#because dict_a and dict_b are dictionaries, not a list of dictionaries
#so we need to unpack the dictionaries into a list of dictionaries
#so we need to use * to unpack the dictionaries into a list of dictionaries

#because ** is used to unpack the dictionaries into the new dictionary
#print(f"Exercise 7 - merged but ?={merged}")

# ============================================================================
# Exercise 8: Swapping Variables
# ============================================================================
# TODO: Swap the values of variables p and q using unpacking
p = 100
q = 200
# Your code here:
p, q = q, p
print(f"Exercise 8 - After swap: p={p}, q={q}")

# ============================================================================
# Exercise 9: Challenge - Multiple Unpacking
# ============================================================================
# TODO: Given three lists, unpack them all into one combined list:
list1 = [1, 2]
list2 = [3, 4, 5]
list3 = [6]
# Your code here:
all_combined = [*list1, *list2, *list3]
print(f"Exercise 9 - all_combined={all_combined}")

# ============================================================================
# Exercise 10: Challenge - Function with Keyword Arguments
# ============================================================================
# TODO: Create a function that accepts any keyword arguments using **kwargs
#       and prints them out as "key: value" pairs
# Your code here:
def print_info(**kwargs ): #kwargs is a dictionary  so we can unpack the dictionary into key: value pairs
    for key, value in kwargs.items():
        print(f"{key}: {value}")

#     # Your code here
#     pass

print_info(name="Alice", age=25, city="NYC")

# ============================================================================
# TEST YOUR ANSWERS
# ============================================================================
# Uncomment the sections below to test your code:

# Exercise 1 Test
# print(f"Exercise 1 - x={x}, y={y}, z={z}")
# Expected: x=10, y=20, z=30

# Exercise 2 Test
# print(f"Exercise 2 - first={first}, middle={middle}, last={last}")
# Expected: first=1, middle=[2, 3, 4, 5, 6], last=7

# Exercise 3 Test
# print(f"Exercise 3 - important={important}")
# Expected: important=keep

# Exercise 4 Test
# print(f"Exercise 4 - Name: {name}, Age: {age}, Profession: {profession}")
# Expected: Name: John, Age: 30, Profession: Developer

# Exercise 5 Test
# print(f"Exercise 5 - sum={sum_numbers(1, 2, 3, 4, 5)}")
# Expected: sum=15

# Exercise 6 Test
# print(f"Exercise 6 - combined={combined}")
# Expected: combined=[1, 2, 3, 7, 8, 9]

# Exercise 7 Test
# print(f"Exercise 7 - merged={merged}")
# Expected: merged={'x': 1, 'y': 2, 'z': 3}

# Exercise 8 Test
# print(f"Exercise 8 - After swap: p={p}, q={q}")
# Expected: After swap: p=200, q=100

# Exercise 9 Test
# print(f"Exercise 9 - all_combined={all_combined}")
# Expected: all_combined=[1, 2, 3, 4, 5, 6]

# Exercise 10 Test
# print("Exercise 10:")
# print_info(name="Alice", age=25, city="NYC")
# Expected: name: Alice
#          age: 25
#          city: NYC