"""
Practice: Python Inheritance
=============================
You know C, C++, VB, Swift/SwiftUI — here you practice Python's rules.
Complete the TODOs and run this file to check your answers.
"""

# =============================================================================
# Exercise 1: Basic inheritance and override
# =============================================================================
# TODO: Define a class Vehicle with a method drive() that returns "Vehicle driving".
#       Then define Car(Vehicle) that overrides drive() to return "Car driving".
#       No super() needed yet.

class Vehicle:
    def print_drive(self):
        return " Vehicle Driving "

class Car(Vehicle):
    def print_drive(self):
        return "Car Driving"

# Uncomment to test:
v = Vehicle()
c = Car()
print(v.print_drive())   # expected: Vehicle driving
print(c.print_drive())   # expected: Car driving


# =============================================================================
# Exercise 2: __init__ and super().__init__()
# =============================================================================
# TODO: Give Vehicle an __init__(self, name) that sets self.name = name.
#       Give Car an __init__(self, name, wheels) that:
#         1) calls super().__init__(name)
#         2) sets self.wheels = wheels
#       Then create c = Car("Tesla", 4) and print c.name and c.wheels.

class Vehicle:
    def __init__(self, name):
        self.name = name

class Car(Vehicle):
    def __init__(self, name, wheels):
        super().__init__(name)              # one statement: call the parent initializer
        self.wheels = wheels
        

# Uncomment to test:
c = Car("Tesla", 4)
print(c.name, c.wheels)   # expected: Tesla 4


# =============================================================================
# Exercise 3: Override but call parent with super()
# =============================================================================
# TODO: Vehicle has speak(self) returning "I am a vehicle".
#       Car overrides speak(self) to return: parent message + " Specifically a car."
#       Use super().speak() to get the parent message.

class Vehicle:
    def speak(self):
        return "I am a vehicle"

class Car(Vehicle):
    def speak(self):
        message = super().speak()
        return message + " Specifically a car."

# Uncomment to test:
c = Car()
print(c.speak())   # expected: I am a vehicle Specifically a car.


# =============================================================================
# Exercise 4: Method Resolution Order (MRO)
# =============================================================================
# TODO: Define A, B, C where C(A, B). Print C.__mro__ and say what order
#       Python will look for methods (first to last).

class A:
    def iam(self):
        return "A"
class B:
    def iam(self):
        return "B"
class C(A, B):
    def iam(self):
        return "C"

# Uncomment to test:
print(C.__mro__)   # expected: (C, A, B, object) or similar


# =============================================================================
# Exercise 5: Multiple inheritance — who runs first?
# =============================================================================
# TODO: A and B both define method greet(self) returning "A" and "B".
#       C(A, B). What does C().greet() return? Try it.
#       Then define C.greet(self) to return super().greet() + " from C".
#       What does C().greet() return now? (MRO: C -> A -> B -> object)

class A:
    def greet(self):
        return "A"

class B:
    def greet(self):
        return "B"

class C(A, B):
    # pass
    def greet(self):
        return super().greet() + " from C"

# Uncomment to test:
print(C().greet())  # A from C (A is first in MRO)


# one way to see B
# class A:
#     def greet(self):
#         return "A" + super().greet()  # pass the baton to next in MRO (B)

# class B:
#     def greet(self):
#         return "B"

# class C(A, B):
#     def greet(self):
#         return super().greet() + " from C"

#so...
# C().greet() → C calls super().greet() → A.
# A returns "A" + super().greet() → B.
# B returns "B".
# So you get "A" + "B" + " from C" (e.g. "AB from C").

# Uncomment to test:
print(C().greet())  # A from C (A is first in MRO)



# =============================================================================
# Exercise 6: Abstract base class (optional)
# =============================================================================
# TODO: From abc import ABC, abstractmethod.
#       Define class Animal(ABC) with @abstractmethod def speak(self): pass.
#       Define Dog(Animal) with def speak(self): return "Woof".
#       Try instantiating Animal() — it should raise. Dog() should work.

from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    ...

# Uncomment to test:
a = Animal()   # expected: TypeError (cannot instantiate)
d = Dog()
print(d.speak())   # expected: Woof


# =============================================================================
# Exercise 7: Naming convention — “internal” vs “name mangling”
# =============================================================================
# TODO: In a class Person, set self._internal = "internal" and self.__private = "mangled".
#       From outside, person._internal is readable; person.__private is not (AttributeError).
#       The mangled name is stored as _Person__private (try person._Person__private).

# class Person:
#     def __init__(self):
#         ...
#         ...

# Uncomment to test:
# p = Person()
# print(p._internal)            # expected: internal
# print(p._Person__private)     # expected: mangled
# print(p.__private)            # expected: AttributeError


# =============================================================================
# RUN ME: uncomment the exercises you completed and run:
#   python inheritance_practice.py
# =============================================================================
