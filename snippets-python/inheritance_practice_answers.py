"""
Answers for inheritance_practice.py — try the exercises first, then compare.
Run: python inheritance_practice_answers.py
"""

# -----------------------------------------------------------------------------
# Exercise 1: Basic inheritance and override
# -----------------------------------------------------------------------------
class Vehicle:
    def drive(self):
        return "Vehicle driving"


class Car(Vehicle):
    def drive(self):
        return "Car driving"


print("Exercise 1:")
print(Vehicle().drive())
print(Car().drive())


# -----------------------------------------------------------------------------
# Exercise 2: __init__ and super().__init__()
# -----------------------------------------------------------------------------
class Vehicle2:
    def __init__(self, name):
        self.name = name


class Car2(Vehicle2):
    def __init__(self, name, wheels):
        super().__init__(name)
        self.wheels = wheels


print("\nExercise 2:")
c = Car2("Tesla", 4)
print(c.name, c.wheels)


# -----------------------------------------------------------------------------
# Exercise 3: Override but call parent with super()
# -----------------------------------------------------------------------------
class Vehicle3:
    def speak(self):
        return "I am a vehicle"


class Car3(Vehicle3):
    def speak(self):
        return super().speak() + " Specifically a car."


print("\nExercise 3:")
print(Car3().speak())


# -----------------------------------------------------------------------------
# Exercise 4: MRO
# -----------------------------------------------------------------------------
class A:
    pass


class B:
    pass


class C(A, B):
    pass


print("\nExercise 4:")
print(C.__mro__)


# -----------------------------------------------------------------------------
# Exercise 5: Multiple inheritance
# -----------------------------------------------------------------------------
class A5:
    def greet(self):
        return "A"


class B5:
    def greet(self):
        return "B"


class C5(A5, B5):
    def greet(self):
        return super().greet() + " from C"


print("\nExercise 5:")
print(C5().greet())  # A from C (A is first in MRO)


# -----------------------------------------------------------------------------
# Exercise 6: Abstract base class
# -----------------------------------------------------------------------------
from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        return "Woof"


print("\nExercise 6:")
print(Dog().speak())
# Animal() would raise: TypeError: Can't instantiate abstract class Animal


# -----------------------------------------------------------------------------
# Exercise 7: _internal vs __private
# -----------------------------------------------------------------------------
class Person:
    def __init__(self):
        self._internal = "internal"
        self.__private = "mangled"


print("\nExercise 7:")
p = Person()
print(p._internal)
print(p._Person__private)
