def add_item(item, basket=[]):
    basket.append(item)
    print(basket)

# add_item("apple")  
# add_item("banana")  

# add_item("apple", basket=[])  
# add_item("banana", basket=[])  


# add_item("apple")    → ['apple']
# add_item("banana")   → ['apple', 'banana']

# Fix: use a non-mutable default and create a new list inside the function when no basket is passed:

# def add_item(item, basket=None):
#     if basket is None:
#         basket = []
#     basket.append(item)
#     print(basket)
# Then:

# add_item("apple") → ['apple']
# add_item("banana") → ['banana']
# because each call that doesn’t pass basket gets a new []. This pattern is the standard way to avoid the “mutable default argument” gotcha in Python.




x = "global"

def outer():
    x = "outer"
    def inner():
        x = "inner"
        print(x)
    inner()
    print(x)

outer()
print(x)


# Scope (LEGB rule)

# L – Local
# Names defined inside the current function (including parameters).

# E – Enclosing
# Names in the local scopes of any enclosing functions (e.g. outer function in a closure).

# G – Global
# Names defined at the top level of the current module (module-level variables and functions).

# B – Built-in
# Names in the built-in namespace (print, len, int, list, etc.).


# inner() sees its local x = "inner" → prints "inner"
# outer() sees its local x = "outer" → prints "outer"
# global x = "global" → prints "global"
# So output:

# textinner
# outer
# global

# Truthy / Falsy values
# In Python:


# bool(0) → False
# bool("") → False
# bool([]) → False
# bool("False") → True (non-empty string is truthy, even if it says "False")

# So only d) bool("False") is True.
# You said: A, b, c, d → Incorrect — the first three are all falsy.

# so if it is something that the bool is evaluating that is false, it's false, but if it is any non empty string even the word false, it's true?


def func(*args, **kwargs):
    print(len(args), len(kwargs))

func(1, 2, 3, name="Alice", age=30)


def count_up(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up(3):
    print(num, end=" ")


# late binding closure
funcs = []
for i in range(3):
    def f():
        print(i)
    funcs.append(f)

for func in funcs:
    func()

# prints 2,2,2

# How to fix it (for reference)

# You “freeze” the value at definition time by making i an argument with a default (so the current value is stored when the function is created):

funcs = []
for i in range(3):
    def f(x=i):   # default captures current value of i
        print(x)
    funcs.append(f)
for func in funcs:
    func()
# 0 1 2