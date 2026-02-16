# Decorators (Basic)

Basic decorator patterns and a critical lesson: **`__file__` and decorators**.

---

## How the `__file__` dunder works

### What it is

`__file__` is a **module-level attribute**. When Python loads a module (a `.py` file), it sets `__file__` on that module to the path of the **file where the code is defined**.

- **Where it’s set:** On the **module** object (the namespace of the `.py` file).
- **What it contains:** The path of that module’s source file (absolute or relative depending on how the module was loaded).
- **When it’s set:** At **import time**, when the module is first loaded.

### Important points

1. **It’s “where the code lives,” not “where the code is called.”**  
   If `module_a.py` imports and calls a function from `module_b.py`, then inside `module_b.py`, `__file__` is still the path to `module_b.py`, not `module_a.py`.

2. **It’s per module.**  
   Every module has its own `__file__`. There is no built-in “caller’s file” attribute; you have to get the caller’s module (e.g. via the stack or by inspecting a function object).

3. **Typical uses:**  
   Finding a config or resource “next to this module,” building module-relative paths for logging, or registering something “by file/module.”

### Quick example

```python
# In my_module.py
import os

print(__file__)                    # path to my_module.py
print(os.path.dirname(__file__))   # directory containing my_module.py
config_path = os.path.join(os.path.dirname(__file__), "config.json")
```

---

## `__file__` and decorators: the pitfall

### What goes wrong

A **decorator** is defined in one module (e.g. `my_decorator.py`) and runs in **that module’s scope** when Python builds the decorated function (at import/definition time).

So any use of `__file__` **inside the decorator** (or in the wrapper when that wrapper is created in the decorator’s file) refers to the **decorator’s file**, not the file where `@decorator` was applied (e.g. `user_module.py`).

- “Load a config next to the **caller’s** file” → if you use `__file__` inside the decorator, you load next to the **decorator’s** file → wrong path, `FileNotFoundError`, or wrong resource.
- “Log with module-relative path” or “register by file/module” → you’re using the decorator’s module, not the user’s.

So: **the decorator runs in its own module’s context; `__file__` there is the decorator’s file.**

### Wrong way: using `__file__` in the decorator

```python
# my_decorator.py
import os

def load_config_next_to_caller():
    """WRONG: __file__ here is the DECORATOR's file."""
    config_dir = os.path.dirname(__file__)
    config_path = os.path.join(config_dir, "config.json")
    with open(config_path) as f:
        return f.read()

def with_config(wrapped_func):
    def wrapper(*args, **kwargs):
        config = load_config_next_to_caller()  # Looks next to my_decorator.py!
        return wrapped_func(*args, **kwargs, config=config)
    return wrapper
```

```python
# user_module.py
from my_decorator import with_config

@with_config
def my_handler(config=None):
    return config
# Config is loaded from next to my_decorator.py, not user_module.py.
```

Using `__file__` inside the wrapper doesn’t fix it if the wrapper is still **defined** in the decorator’s module:

```python
def with_config(wrapped_func):
    def wrapper(*args, **kwargs):
        config_dir = os.path.dirname(__file__)  # Still the decorator's file!
        ...
    return wrapper
```

### Right way: use the decorated function’s module file

You want “the file where the **decorated function** is defined.” That’s the function’s **module**, not the decorator’s. Use `inspect.getfile(func)` on the function passed into the decorator.

```python
# my_decorator.py
import os
import inspect

def load_config_next_to_module(module_file_path):
    """Load config from the same directory as the given module file."""
    config_dir = os.path.dirname(module_file_path)
    config_path = os.path.join(config_dir, "config.json")
    with open(config_path) as f:
        return f.read()

def with_config(wrapped_func):
    # Resolve caller's file once when the decorator is applied (at import time).
    caller_file = inspect.getfile(wrapped_func)

    def wrapper(*args, **kwargs):
        config = load_config_next_to_module(caller_file)  # Correct path.
        return wrapped_func(*args, **kwargs, config=config)
    return wrapper
```

Now `caller_file` is the path of the module where the decorated function (e.g. `my_handler`) is defined, so config is loaded from next to **that** file.

### Summary

| Goal                            | Wrong (in decorator)              | Right                                      |
|---------------------------------|-----------------------------------|--------------------------------------------|
| Config next to “caller’s” file  | `os.path.dirname(__file__)`       | `inspect.getfile(wrapped_func)` then dir   |
| Log with module-relative path   | `__file__` in decorator           | `inspect.getfile(wrapped_func)` or `__module__` |
| Register by file/module        | Same: `__file__` → decorator’s    | Use `inspect.getfile(wrapped_func)` or `wrapped_func.__module__` |

---

## Runnable examples

- **Wrong:** Run `python example_file_in_decorator_wrong_caller.py` — the decorator uses `__file__`, so the config path is next to the decorator’s file (`example_file_in_decorator_wrong_decorator.py`), not the caller’s.
- **Right:** Run `python example_file_in_decorator_right_caller.py` — the decorator uses `inspect.getfile(wrapped_func)`, so the config path is next to the caller’s file (`example_file_in_decorator_right_caller.py`), as intended.

Run both from this directory. When the decorator and caller live in the **same** directory (as here), the resolved path can look the same; the bug shows up when the decorator is in a different package (e.g. a shared library) and the caller is in app code — then the wrong version loads from the library’s directory and the right version from the app’s.
