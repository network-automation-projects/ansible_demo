# useful tidbits
- ISO-like timestamp for filenames: 20250208_143022
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

* unpacks an iterable (list, tuple) into positional arguments.
** unpacks a dict into keyword arguments.

# mistakes i've made

In Python, result[device] = value is the standard way to add or update a key-value pair in a dictionary. The square brackets work differently for dicts vs lists:
List: lst[i] → value at index i
Dict: d[key] → value for key key




NOT: if iface != "disabled" +    iface != "down":
YES: if iface != "disabled" and  iface != "down":


re.findall returns a list of all matches in the string.
    if iface != "disabled" + iface != "down":

def device_in_scope(hostname: str, allowed: List[str]) -> bool:
    """
    Return True if hostname is in the allowed list, else False.
    Use: hostname in allowed

    Example:
        >>> device_in_scope('r1', ['r1', 'r2', 'r3'])
        True
        >>> device_in_scope('r9', ['r1', 'r2', 'r3'])
        False
    """
    # TODO: 
    return hostname in allowed     # ****** 


use mydict["key1"]              (not mydict.get("key1")) 

dictionaries don't have append.

when iterating over a dictionary, you need the items() method to get the key and value pairs.

so:
    reversedDict = {}
    for ip, hostname in device_to_ip.items():    #i left off items and it didn't work.
        reversedDict[ip] = hostname
    return reversedDict  # replace


if not interfaces.find(name):
        interfaces.append(name)
No. That code will raise an error.
Problem: Lists don’t have a .find() method. .find() is for strings (it returns the index or -1). On a list you get:
AttributeError: 'list' object has no attribute 'find'
What to use instead: The docstring is correct: use the in operator to test membership in a list:

if name not in interfaces:    
   interfaces.append(name)

So the logic “only add if not already there” is right, but the implementation should use name not in interfaces, not interfaces.find(name).

Sets use .add(item) to add one element.
Lists use:
.append(item) — add one item at the end (this is the usual “add to list” operation).
.insert(i, item) — insert at index i.
.extend(iterable) — add several items (e.g. another list).
Dictionaries use mydict[key] = value or mydict.update(other) to add multiple key-value pairs from another dict or .setdefault(key, value) to add a key-value pair if the key is not already in the dictionary.

# functions
can be passed as arguments to other functions
can be returned from other functions
can be assigned to variables
can be stored in data structures
can be nested in other functions

def outer_function(x):
   print(f"outer_function: {x}")
    def inner_function(y):
        print(f"inner_function: {y}")
        return x + y
    return inner_function

    inner_function = outer_function(2)

    inner_function(3)

#what is happening here?
outer_function is called with the argument 2.
inner_function is defined inside outer_function and is called with the argument 3.
inner_function returns the value of x + y, which is 5.
so the output of inner_function(3) is 5.

# classes and dataclasses

Why use a regular class instead of a dataclass?
1. Custom __init__ logic
If you need validation, side effects, or derived values in the constructor:
class Device:    def __init__(self, hostname: str, ip: str):        if not hostname:            raise ValueError("hostname required")        self.hostname = hostname        self.ip = ip        self._normalized_ip = self.ip.replace(" ", "")  # computed in __init__
Dataclasses generate __init__ from the fields; you can't add arbitrary logic there without overriding the generated __init__, which quickly gets messy.
2. Mutable default values
Dataclasses use field(default_factory=...) for mutable defaults (lists, dicts). Regular classes can handle this in __init__:
class Config:    def __init__(self, tags=None):        self.tags = tags if tags is not None else []
3. Non-field attributes or complex state
When you have attributes that aren’t constructor parameters or are computed:
class Device:    def __init__(self, hostname: str, ip: str):        self.hostname = hostname        self.ip = ip        self._connection = None  # set later, not a constructor arg
4. Inheritance with tricky behavior
Dataclass inheritance and __init__ generation can be awkward, especially with multiple inheritance. Regular classes give clearer control.
5. No real “data”
For objects that mainly provide behavior, not data (e.g. service, controller, strategy), a regular class is usually simpler.
Summary: Dataclasses are ideal when you mainly need typed, named fields and a generated __init__. Use a regular class when you need custom init logic, complex state, or more flexible design.


# decorators
decorators are functions that take in a function as an argument and return a function.?

https://www.udemy.com/course/100-days-of-code/learn/quiz/6474209#overview

example:
def decorator(func):
    def wrapper(*args, **kwargs):
        #do something before the function is called
        print(f"Decorator: {func.__name__}")
        #do something after the function is called
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_function():
    print("My function")

OR

my_decorated_function = decorator(my_function)
my_decorated_function()

https://www.udemy.com/course/100-days-of-code/learn/quiz/6474205#overview

The single * and double ** match how Python separates positional and keyword arguments.
One asterisk * — positional arguments
Collects extra positional arguments into a tuple.
Positional args are passed by position (order), not by name, so they’re a sequence.
def foo(*args):    print(args)  # tuple: (1, 2, 3)foo(1, 2, 3)
Two asterisks ** — keyword arguments
Collects extra keyword arguments into a dict.
Keyword args are passed as name=value pairs, so they’re stored as a mapping.
def bar(**kwargs):    print(kwargs)  # dict: {'a': 1, 'b': 2}bar(a=1, b=2)
How it matches unpacking
The same symbols are used when unpacking:
*iterable unpacks an iterable into positional arguments
**mapping unpacks a mapping into keyword arguments
nums = (1, 2, 3)d = {'x': 10, 'y': 20}foo(*nums)   # same as foo(1, 2, 3)bar(**d)     # same as bar(x=10, y=20)
So:
* = positional / iterable
** = keyword / name-value mapping
The number of asterisks reflects that positional args are “flat” (a sequence) while keyword args are “paired” (name and value).


# quirks regarding .get()
Here are the main things to keep in mind with .get():
1. Default is only used when the key is missing
d.get(key, default) returns default only if key is not in the dict. If the key exists and its value is None, you get None, not the default.
d = {"a": None}d.get("a", "default")   # → None (key exists; default is ignored)d.get("b", "default")   # → "default" (key missing)
2. Default is optional
If you omit the second argument and the key is missing, you get None (no KeyError):
d.get("missing")   # → None
3. Default is evaluated even when not used
The default value is a normal argument, so it’s evaluated before the call. That can matter if it’s expensive or has side effects:
# Bad: [] is created even when key exists; you might expect "reuse one list"d.get("key", [])   # Safe for "missing" but a new [] each time# If you need a mutable default shared across calls, you still need the usual pattern:# d.setdefault("key", []) or check "key" in d and create list once
4. Only one “default”
.get(key, default) has a single default. There’s no built-in “default for missing, different default for None”. For that you need something like:
d.get(key) or default   # careful: also replaces 0, "", []# ord[key] if key in d and d[key] is not None else default
5. Type hints
Type checkers treat .get() as returning V | None (when one argument) or V (when default is given). So d.get("x", 0) is inferred as int, while d.get("x") is int | None.
Summary: The main “quirk” is that the default is only used for a missing key; it does not replace an existing value (even if that value is None).
so get is not a 'read only pull'? it sounds like find, like something that wouldn't modify values

Yes. .get() is read-only. It never changes the dict.
It only returns a value: either d[key] if the key exists, or the default you passed if it doesn’t.
It does not add the key, update a value, or modify the dict in any way.
So it’s like a safe “look up and return” (similar in spirit to “find”): you’re only reading. The earlier point was just that the default is only used when the key is missing — so you might get None back when the key exists with value None, instead of your default. That’s about what value you get back, not about the dict being modified.

# list comprehesions, dict comprehesions, set comprehesions, and generator expressions
list comprehesions: [expression for item in iterable]
dict comprehesions: {key: value for item in iterable}
set comprehesions: {expression for item in iterable}
generator expressions: (expression for item in iterable)

useful examples:
1. Any device in a list is in the allowed set
def any_device_allowed(devices: List[str], allowed: set) -> bool:    return any(d in allowed for d in devices)
Generator yields one bool per device; any() is True if at least one is True.
2. All interfaces are in “up” state
def all_interfaces_up(interfaces: List[Dict[str, str]]) -> bool:    return all(iface.get("state") == "up" for iface in interfaces)
Yields True for each interface whose "state" is "up"; all() is True only if every one is True.
3. Count how many required keys are missing
def missing_required_count(config: dict, required: List[str]) -> int:    return sum(1 for key in required if key not in config)
Generator yields 1 for each missing key; sum() gives the total count.
4. Check that no hostname is empty
def all_hostnames_nonempty(devices: List[Dict[str, str]]) -> bool:    return all(bool(d.get("hostname", "").strip()) for d in devices)
Yields True/False per device; all() ensures every hostname is non-empty after strip.
5. Get only the keys that are present in config
def present_keys(config: dict, keys: List[str]) -> List[str]:    return [k for k in keys if k in config]
This one is a list comprehension (same idea as a generator, but builds a list). The generator version would be (k for k in keys if k in config); you’d use it when iterating once or passing to list(), sum(), etc.
Pattern: (expression for item in iterable) or (expression for item in iterable if condition), then pass it to all(), any(), sum(), list(), or a for loop.

# dictionary basics

In Python, result[device] = value is the standard way to add or update a key-value pair in a dictionary. The square brackets work differently for dicts vs lists:
List: lst[i] → value at index i
Dict: d[key] → value for key key

other ways to add or update a key-value pair in a dictionary:
d[key] = value
d.update({key: value})
d.setdefault(key, value)

d.setdefault(key, value) is like d[key] = value, but it only sets the value if the key is not already in the dictionary.

.update() is the way to merge two dictionaries together in place.

a.update(b) # a is now merged with b. b is at the end of a.
print(a) 

result = a.update(b)
print(result) # result is None because update is a method that updates the dictionary in place.

also, c = a | b # c is a new dictionary that is the merge of a and b.

# cool ways to use dictionary comprehensions
In a dict comprehension the key and value are just expressions. You can use any expression that gives you a valid key and value.
Examples:
Key/value methods: {k.lower(): v.upper() for k, v in config.items()}
Arithmetic: {k: v * 2 for k, v in counts.items()}
Conditionals: {k: v if v else "n/a" for k, v in config.items()}
Different key: {k.strip(): v for k, v in raw.items()}
New keys from values: {v: k for k, v in config.items()} (swap key/value)
Call a function: {k: normalize(v) for k, v in config.items()}
The only requirements are:
The key must be hashable (e.g. str, int, tuple — not a list or dict).
The expression runs for each item and produces one key and one value.
So your k.lower(): v.upper() (and other simple manipulations) are fine.

# list comprehension - weird fact
[x for a in A for b in B for c in C]
# same as:
# for a in A:
#     for b in B:
#         for c in C:
#             x

you can use this to flatten a list of lists
you can nest many loops to create a new list with the results of each loop, the limit
being readability

# dictionary unpacking / merging dictionaries

** is dictionary unpacking. Inside a dict literal it “unpacks” another dict’s key–value pairs into that literal.
How {**base, **override} works:
**base — All key–value pairs from base are spread into the new dict.
**override — All key–value pairs from override are spread in after. If a key was already there (from base), it gets overwritten.
You get one new dict: base’s entries first, then override’s, with override winning on conflicts.
Example:
base    = {'a': 1, 'b': 2}override = {'b': 20, 'c': 3}{**base, **override}# Step 1: **base     →  a: 1, b: 2# Step 2: **override →  b: 20, c: 3  (b overwrites the previous b)# Result: {'a': 1, 'b': 20, 'c': 3}
Same idea elsewhere:
In a dict literal: {**d} is a shallow copy of d; {**d1, **d2} merges two dicts.
In a function call: func(**d) passes the keys as keyword argument names and values as their values.
So “merge base, then override, with override winning” is exactly what {**base, **override} does; it builds a new dict and doesn’t change base or override.

Main gotchas with {**base, **override}:
1. Shallow merge only
Only the top level is merged. Values are not copied; the new dict gets references to the same objects. If a value is mutable (list, dict, etc.), changing it affects every dict that “has” that key:
base = {"a": [1, 2]}override = {"b": 3}merged = {**base, **override}merged["a"].append(3)# base["a"] is now [1, 2, 3] too — same list
So merging doesn’t “clone” nested structures; it just copies the top-level key/value references.
2. No deep/recursive merge
If both dicts have the same key and the value is a dict, the whole value is replaced; the inner dict is not merged:
{**{"a": {"x": 1}}, **{"a": {"y": 2}}}# → {"a": {"y": 2}}   # first "a" is gone, not merged with second
To merge nested dicts you need custom logic (e.g. a recursive merge function or a library that does it).
3. Order
In Python 3.7+ dicts keep insertion order. The merged dict is: all keys from the first dict (in order), then from the second (in order), with later unpackings overwriting earlier ones for duplicate keys. So order is well-defined and “last wins.”
4. Keys in ** in a dict literal
Inside {**d} the keys of d can be any hashable type. The “keys must be strings” rule only applies when you use ** in a function call (e.g. func(**d)).
Summary: The main pitfalls are shared mutable values (shallow merge) and no automatic deep merge. For simple top-level config-style dicts, {**base, **override} is usually fine.
this Only the top level is merged. Values are not copied; the new dict gets references to the same objects. If a value is mutable (list, dict, etc.), changing it affects every dict that “has” that key: seems to mean that the appending or deleting of items in the values for the base are affected by the changes to the merged list

It works both ways: they’re sharing the same object.
merged gets a reference to the same list/dict that base (or override) had for that key — not a copy.
So there’s only one list/dict in memory; base["a"] and merged["a"] are two names for it.
So:
If you change via merged (e.g. merged["a"].append(3)), then base["a"] also changes, because it’s the same list.
If you change via base (e.g. base["a"].append(3)), then merged["a"] also changes, because it’s still the same list.
So it’s not “only base is affected by merged”; whoever mutates that value, everyone else that has that key sees the change, because they all point to the same object. Your phrasing “the appending or deleting of items in the values for the base are affected by the changes to the merged [dict]” is right in that base is affected when you change through merged; just keep in mind it’s symmetric: base’s mutations also affect merged.

One small precision: this applies to mutating the value in place (e.g. merged["a"].append(1) or base["a"].append(1)). If you reassign a key in the merged dict (e.g. merged["a"] = [99]), you’re just making that key in merged point to a new object; base and override are unchanged. So “changes to the values” = mutating the object (append, delete, etc.), not reassigning the key.


# defaultdict

What defaultdict does
defaultdict is like a normal dict, but when you access a key that doesn’t exist, it creates that key and sets its value using a factory function you pass in (e.g. list, int, set). So you avoid “if key not in dict” checks and manual initialization.
Common uses
Grouping / bucketing (e.g. by status)
You’re already doing this: one key per status, value = list of items.
   grouped = defaultdict(list)   for item in items:       grouped[item["category"]].append(item["name"])  # no "if key not in grouped"
Without defaultdict you’d do:
   grouped = {}   for item in items:       if item["category"] not in grouped:           grouped[item["category"]] = []       grouped[item["category"]].append(item["name"])
Counting
Use defaultdict(int) so missing keys start at 0:
   counts = defaultdict(int)   for word in words:       counts[word] += 1  # first time: 0 + 1
(For simple counting, Counter is often nicer, but the idea is the same.)
Accumulating / summing by key
Same pattern: missing key → 0, then add.
   totals = defaultdict(int)   for record in records:       totals[record["device"]] += record["bytes"]
Collecting unique things per key
Use defaultdict(set) so each key maps to a set (no duplicates):
   unique_hosts = defaultdict(set)   for event in events:       unique_hosts[event["site"]].add(event["host"])
Nested structures
e.g. “for each device, a list of interfaces”:
   by_device = defaultdict(list)   for iface in interfaces:       by_device[iface["device"]].append(iface["name"])
Why use it
Less boilerplate: no “if key not in dict” or “get key or create”.
One clear pattern: “key → default value, then update.”
Fewer bugs from forgetting to initialize a key.
Gotcha
Accessing a missing key creates it (and the default value). So if you only want to check existence, use a normal dict or key in d; use defaultdict when you intend to create and use a value for that key.




# map vs transformer
Not usually. For “do something to each item and collect the results,” people mostly say map or mapping (e.g. “map over the list,” “a list comprehension that maps each dict to its 'status'”). The comprehension form [i["status"] for i in interfaces] is a mapping (or “map”) style list comprehension.
“Transformer” is used in a few other ways:
In Python/CS it often means a callable or step that transforms data in a pipeline (e.g. “a transformer that normalizes hostnames”), not the comprehension syntax itself.
In ML/NLP, “Transformer” usually means the Transformer model (attention-based architecture).
So: the pattern is usually called a map (or mapping); “transformer” isn’t the standard name for that list comprehension.    


#deque
???
A deque (pronounced “deck”) is a double-ended queue: a sequence that supports adding and removing elements from both ends in O(1) time.
What it is
Name: “deque” = double-ended queue.
Behavior: Like a list you can efficiently push/pop on the left and right.
In Python: Implemented in collections as collections.deque.
Why use it instead of a list?
Left-side operations: Appending or popping on the left of a list is O(n) (elements shift). On a deque it’s O(1).
Right-side operations: Appending/popping on the right is O(1) for both list and deque.
So when you need a queue (FIFO) or a stack (LIFO) or anything that frequently touches both ends, a deque is a better fit than a list.
Basic usage
from collections import dequed = deque([1, 2, 3])d.append(4)       # right: [1, 2, 3, 4]d.appendleft(0)  # left:  [0, 1, 2, 3, 4]d.pop()           # 4d.popleft()       # 0# d is now deque([1, 2, 3])
Optional: maxlen
You can create a bounded deque that drops the oldest element when full:
d = deque(maxlen=3)d.extend([1, 2, 3])  # deque([1, 2, 3])d.append(4)          # 1 is dropped → deque([2, 3, 4])
So in short: a deque is a double-ended sequence optimized for fast add/remove at both ends; in Python you get it from collections.deque.
what does O(1) mean? also, are there other tools thta people use on the job or is this the best for this situation?

What O(1) means
O(1) is Big O notation: it describes how the time (or space) of an operation grows as the size of the data grows.
O(1) = constant time: the operation takes the same time whether you have 10 items or 10 million. The “1” means “doesn’t scale with input size.”
O(n) = linear: time grows in proportion to size (e.g. scanning a list of length n).
O(log n) = logarithmic: grows slowly as n grows (e.g. binary search on a sorted list).
So when we say “append/pop on the left of a deque is O(1),” we mean: adding or removing from the left takes the same time no matter how many elements are in the deque. For a list, doing that is O(n) because other elements have to shift.
Other tools people use (and when deque is “best”)
Deque is the standard, built-in choice when you need:
A FIFO queue (e.g. task queue, BFS): deque with append + popleft is the usual Python approach.
A LIFO stack: list is fine (append/pop are O(1) on the right); deque works too.
Add/remove on both ends: deque is the right tool; list is bad for left-end operations.
Other things people use on the job:
Need	What people use
Thread-safe queue (multiple workers)	queue.Queue — FIFO, thread-safe; uses a deque under the hood.
Priority queue (always process “highest priority” first)	queue.PriorityQueue or heapq — not a deque; different use case.
Async / asyncio	asyncio.Queue — for coroutines, not threads.
Bounded buffer / sliding window	deque(maxlen=n) — very common.
Simple stack (only one end)	Plain list with append/pop — totally fine and very common.
So: O(1) means “constant time; doesn’t depend on size.” For double-ended queues and FIFO queues in normal Python code, deque is the usual and best choice; other tools (Queue, PriorityQueue, heapq, asyncio.Queue) are for thread-safety, priorities, or async, not as replacements for deque in its core use case.


#OrderedDict

1. Do you still need OrderedDict?
In Python 3.7+, the built-in dict preserves insertion order as part of the language. For “I need order preserved,” a normal dict is usually enough and is what most production code uses:
# Modern Python (3.7+): plain dict is ordereddef create_config_order() -> dict[str, str]:    config = {}    config["step1"] = "configure interface"    config["step2"] = "configure routing"    return config  # order preserved
So in many cases the “better” approach in production is: use dict and type it as dict[K, V]. Reserve OrderedDict for when you need its extra behavior (see below).
2. When OrderedDict is still useful
You need move_to_end(key) or popitem(last=...) for LRU/cache-style logic.
You need to support Python 3.6 or earlier and must guarantee order.
You want to be explicit that order is part of the contract (API clarity).
3. Fixing the type hint (and dropping # type: ignore)
The # type: ignore[return-value] is likely because the return type is unparameterized OrderedDict. Type checkers expect parameterized types. A production-friendly version is:
from typing import OrderedDict  # or from collections.abc (Python 3.9+)def create_config_order() -> OrderedDict[str, str]:  # or OrderedDict[str, Any]    return OrderedDict()
With a proper OrderedDict[K, V] return type, you typically don’t need # type: ignore; the checker accepts return OrderedDict() as that type.
4. Implementation in your repo that uses it
Your codebase already has a concrete use in examples.py:
create_configuration_plan(config_steps) (lines 192–212) builds an OrderedDict from a list of steps and returns it so step order is preserved.
apply_configuration_plan(plan, device) (lines 215–233) iterates over that OrderedDict with .items() and applies the steps in the same order.
So: in production, prefer dict + dict[K, V] when order is the only requirement; use OrderedDict + OrderedDict[K, V] when you need its extra APIs or explicit ordering guarantees, and type it properly so you can remove the # type: ignore.


# copy.copy and copy.deepcopy

In Python, copy and deepcopy are about how much gets copied, not about “pointers” in the C sense. Python doesn’t have C-style pointers; it has references. Names refer to objects; assignment just rebinds a name to an object.
copy.copy() (shallow copy)
Creates a new top-level object (e.g. a new list or dict), but the contents are still the same objects (same references). So you get a new container, but nested structures are shared.
copy.deepcopy() (deep copy)
Creates a new top-level object and recursively creates new copies of everything inside it, so no nested object is shared with the original.
So:
They are about copying (creating new object(s)), not about introducing or managing “pointers.”
The difference is how much is copied:
Shallow: one level of structure; nested objects are not copied (references are copied).
Deep: full structure; nested objects are copied too so nothing is shared.
Example:
import copya = [[1, 2], [3, 4]]b = copy.copy(a)      # new list, same inner listsc = copy.deepcopy(a)  # new list and new inner listsa[0].append(99)# b[0] is [1, 2, 99]  (shared)# c[0] is [1, 2]      (independent)
So: no pointers—just “shallow” vs “deep” copying.

Two different things are in play:
1. What copy is in this file
At the top you have:
from copy import copy, deepcopy
So copy is the function from the copy module (the same as copy.copy from that module). The line return copy(config) is calling that function and passing config as the argument. That’s the usual way to use it after from copy import copy.
2. Why config.copy.copy() is wrong
config is a dict. Dicts have a method named .copy(), so config.copy is that method (a bound method), not the copy module.
So config.copy.copy() would mean: take the dict’s .copy method, then look for an attribute named .copy on that method. Method objects don’t have a .copy attribute, and even if they did, it wouldn’t be the shallow-copy function. So config.copy.copy() is invalid for that reason.
What you could use instead
Shallow copy:
copy(config) ← what you have (function from copy module).
config.copy() ← dict’s own method; same effect for a dict.
If you used the module name:
import copy then copy.copy(config) ← that’s “module name, then function name,” not anything on config.
So: copy here is the module’s function, not something on config. The correct call is copy(config) (or config.copy() for a dict); config.copy.copy() mixes up the dict method with the module’s function and doesn’t work.

# modules, packages, and namespaces

A module is a file that contains Python code.
A package is a directory that contains modules.
A namespace is a collection of modules.

So you can write:
from models import deviceinv = device.DeviceInventory(hostname="r1", ip="10.0.0.1", device_type="cisco_ios")
Or:
from models.device import DeviceInventoryinv = DeviceInventory(hostname="r1", ip="10.0.0.1", device_type="cisco_ios")

The first one is a relative import, the second one is an absolute import.
The first one is more flexible, the second one is more explicit.


Yes. Any .py file can be used as a module as long as Python can find it (i.e. its directory is on sys.path). You don’t have to do anything special in the file for it to be importable.
Caveats:
Location — The file (or its package) must be in a directory on sys.path. Usually that’s the current directory when you run Python, or the project root.
Naming — The filename (without .py) becomes the module name. So my_script.py is imported as my_script. Names that aren’t valid identifiers (e.g. my-script.py) or that clash with stdlib names can be awkward.
Side effects — When the module is imported, Python runs all top-level code in the file. So if the script does real work at import time (e.g. connects to a DB), that runs on import. The usual pattern is to guard that with if __name__ == "__main__": so it only runs when the file is executed, not when it’s imported.
Packages — A folder is only treated as a package (so you can do from folder import module) if it’s on sys.path and typically has an __init__.py (in Python 3.3+ namespace packages are the exception).
So in practice: any .py file in a findable path can be used as a module; naming and “run on import” behavior are what you need to think about.



# principles

SOLID principles
Single Responsibility Principle
Open/Closed Principle
Liskov Substitution Principle
Interface Segregation Principle
Dependency Inversion Principle

DRY principle
Don't Repeat Yourself

KISS principle
Keep It Simple, Silly

YAGNI principle
You Aren't Gonna Need It
(meaning - don't add features that are not needed yet.)

OTHER PRINCIPLES

1. Principle of Least Privilege - give the least privileges needed to do the job.
2. Principle of Least Astonishment - make the code easy to understand.
3. Principle of Least Knowledge - only know what is needed to do the job.
4. Principle of Least Surprise - make the code easy to understand.

#exception handling

nested exception handling

So if you want the outer process to continue even if there was an error, don't re-raise the exception.

Here are the main quirks with nested try/except:
1. Inner handler runs first
An exception is handled by the innermost except that matches. If the inner handler catches it and doesn’t re-raise, the outer handler never sees it.
2. Swallowing exceptions
If the inner except catches and doesn’t re-raise, the exception is effectively swallowed. The outer except won’t run for that exception. In your worker, the inner except catches job-processing errors and doesn’t re-raise, so the outer loop keeps running.
3. Re-raising
Use raise (no argument) in the inner except to re-raise the same exception so the outer handler can catch it. raise e or raise SomeOtherError(...) creates a new exception and can change the traceback.
4. finally runs regardless
finally runs whether or not an exception was caught. If finally raises, that new exception replaces the original one, which can hide the real cause.
5. Order of handlers
With multiple except clauses, the first matching one wins. Put more specific exceptions before broader ones (e.g. except ValueError before except Exception).
6. Double logging
If both inner and outer handlers log and the inner one re-raises, you can log the same error twice. Decide which level should log.
7. return in except
If the inner except does return, the function exits immediately. The outer except never runs for that exception.

logger.exception is a shortcut for logger.error(exc_info=True) which will log the exception and the traceback.


# File io

from pathlib import Path    # preferred over os.path
## `os` and `pathlib` — common in network & AI automation

### `os` module

| What | Function | Use |
|------|----------|-----|
| Change directory | `os.chdir(path)` | Switch cwd before running scripts or loading configs |
| Current directory | `os.getcwd()` | Get cwd; build paths relative to it |
| Environment vars | `os.environ`, `os.getenv(name, default)` | API keys, config paths, feature flags |
| Join paths | `os.path.join(a, b, ...)` | Cross-platform path building |
| Dir / base name | `os.path.dirname(path)`, `os.path.basename(path)` | Split directory vs filename |
| Exists / type | `os.path.exists(path)`, `os.path.isfile(path)`, `os.path.isdir(path)` | Guard before read/write or list |
| Absolute path | `os.path.abspath(path)` | Resolve relative to cwd |
| List directory | `os.listdir(path)` | List files/dirs (e.g. configs, logs) |
| Make dirs | `os.makedirs(path, exist_ok=True)` | Create output dirs (logs, artifacts) |
| Remove | `os.remove(path)`, `os.rmdir(path)` | Delete file or empty dir |
| Run command | `os.system(cmd)` | Run shell (prefer `subprocess` when possible) |
| Separator | `os.path.sep`, `os.sep` | `'/'` vs `'\\'` when needed |

### `pathlib` (`Path`) — preferred for paths

| What | Usage | Use |
|------|--------|-----|
| Current dir | `Path.cwd()` | Like `os.getcwd()` but returns a `Path` |
| Home dir | `Path.home()` | User config / default project dir |
| Join | `Path("a") / "b" / "file.txt"` or `path / "subdir"` | Clean path building |
| Parent / name | `path.parent`, `path.name`, `path.stem`, `path.suffix` | Dir, filename, stem, extension |
| Absolute | `path.resolve()` | Full path (resolves symlinks) |
| Exists / type | `path.exists()`, `path.is_file()`, `path.is_dir()` | Same checks as `os.path` |
| Read/write text | `path.read_text()`, `path.write_text(s)` | One-liner file I/O |
| Read/write bytes | `path.read_bytes()`, `path.write_bytes(b)` | Binaries, pickles |
| List dir | `path.iterdir()` | Iterator over entries (often `sorted()`) |
| Glob | `path.glob("*.json")`, `path.rglob("**/*.yaml")` | Find configs, logs, datasets |
| Make dirs | `path.mkdir(parents=True, exist_ok=True)` | Like `os.makedirs(..., exist_ok=True)` |
| Remove | `path.unlink()`, `path.rmdir()` | Delete file or empty dir |
| Rename | `path.rename(new_path)` | Move/rename (e.g. log rotation) |

### Using `Path`: class vs instance

from pathlib import Path

# p = Path  →  p is the class; p.cwd(), p("scripts"), p.home() all work
# p = Path.cwd()  →  p is the current-directory Path; use p / "config.yaml", p.exists(), etc.

# One-off
Path.cwd()
Path.home()
Path("data") / "logs"

# Short alias for the class
P = Path
P.cwd()
P("output") / "results.json"

# Store current directory
here = Path.cwd()
config = here / "config.yaml"

Paths and files: Prefer pathlib: Path.cwd(), / joining, .read_text() / .write_text(), .glob(), .mkdir(parents=True, exist_ok=True).
Environment / process: Use os: os.environ, os.getenv(); for running commands use subprocess rather than os.system().
