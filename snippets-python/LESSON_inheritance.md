# Python Inheritance — Lesson

A short reference for Python inheritance rules, especially if you're used to C++, VB, Swift, or SwiftUI.

---

## 1. Basic syntax

**Python:**
```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):   # Dog inherits from Animal
    def speak(self):
        return "Woof"
```

- **No** `public` / `private` / `protected` keywords. Use naming conventions:
  - `_single` = “internal use” (by convention).
  - `__double` = name mangling (not true private; avoids accidental overrides).
- **No** `virtual` — all methods are overridable by default.
- **No** semicolons or access specifiers; inheritance is declared in the class header: `class Child(Parent):`.

**Compared to:**  
C++ `class Dog : public Animal`, Swift `class Dog : Animal`, VB `Inherits Animal`.

---

## 2. Calling the parent: `super()`

**Python 3 (recommended):**
```python
class Dog(Animal):
    def __init__(self, name):
        super().__init__()   # no arguments: current class and instance are implicit
        self.name = name
```

- `super()` with **no arguments** (inside a method) means “parent of this class, for this instance.” Use this in normal single-inheritance and cooperative multiple-inheritance.
- You do **not** pass `self` or the class name to `super()` in Python 3.

**Compared to:**  
C++ `Animal::__init__()` or `Base::method()`, Swift `super.init()`, VB `MyBase.New()`.

---

## 3. Constructors and `__init__`

- The constructor is `__init__(self, ...)`, not a method named after the class.
- **You must** call the parent’s initializer if the parent defines `__init__` and you need its setup:

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # initialize parent state first
        self.breed = breed
```

- If you don’t call `super().__init__()`, the parent’s `__init__` is not run (unlike some languages that auto-chain).

---

## 4. Overriding methods

- Override by defining a method with the **same name** in the child.
- Call the parent’s implementation explicitly when you want “super” behavior:

```python
class Dog(Animal):
    def speak(self):
        parent_msg = super().speak()
        return f"{parent_msg} But I say: Woof!"
```

---

## 5. Multiple inheritance and MRO

- Python allows multiple base classes: `class C(A, B):`.
- Order matters. Method resolution follows the **MRO** (Method Resolution Order), which you can inspect:

```python
class A: pass
class B: pass
class C(A, B): pass

print(C.__mro__)   # (C, A, B, object)
```

- `super()` in a method of `C` will try `A` first, then `B`, then `object`, so **all** base classes can get a chance (cooperative multiple inheritance). Design base classes so they also use `super()` in the same methods.

**Compared to:**  
C++ has a fixed order and no single “next” in the chain like Python’s `super()`; Swift has single inheritance; VB has `Inherits` for one base.

---

## 6. “Abstract” base classes (optional)

- Python has **no** `abstract`/`virtual = 0` keyword. Use the `abc` module:

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof"
```

- You **cannot** instantiate `Animal()`; you can instantiate `Dog()`.

**Compared to:**  
C++ pure virtual, Swift `protocol` + optional default, VB `MustInherit` / `MustOverride`.

---

## 7. Quick comparison table

| Concept              | Python                    | C++ / Swift / VB (rough)     |
|----------------------|---------------------------|------------------------------|
| Inherit from         | `class Child(Parent):`    | `: public Base` / `: Base`   |
| Call parent          | `super().method()`        | `Base::method()` / `super`   |
| Constructor          | `__init__(self, ...)`     | same name as class / `init`  |
| Override             | same method name          | same signature               |
| Virtual by default   | yes                       | C++: no; Swift: yes          |
| Multiple inheritance | yes, with MRO             | C++: yes; Swift: no          |
| “Private”            | `_` or `__` by convention | `private` / `protected`      |
| Abstract             | `abc.ABC` + `@abstractmethod` | pure virtual / protocol  |

---

## 8. What to practice

1. Define a base class and a subclass that override one method and call `super()`.
2. Use `__init__` in base and child and call `super().__init__(...)` correctly.
3. Inspect `YourClass.__mro__` for a class with two base classes.
4. (Optional) Use `ABC` and `@abstractmethod` and instantiate only the concrete class.

Use `inheritance_practice.py` for the exercises.
