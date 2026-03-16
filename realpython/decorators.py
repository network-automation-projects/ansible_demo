# decorators from realpython
# https://realpython.com/primer-on-python-decorators/#first-class-objects

from typing import Any, Callable
from functools import wraps
from datetime import datetime
import time
#from flask import Flask, g, request, redirect, url_for
from dataclasses import dataclass


### Fancy Decorators

### --------------------------------------------------
#testing to see if user notices this line of comment XD

# to take an argument in the decorator

def repeat_times(num_times: int)-> Any:
    '''When this decorator is called, it runs the wrapped function num_times times'''
    def decorator(func: Callable)-> Any:
        @wraps(func)
        def wrapper(*args, **kwargs)->Any:
            if num_times:
                for n in range(num_times):
                    func(*args, **kwargs)
        return wrapper
    return decorator


@repeat_times(num_times = 2)
def countdown_repeated(from_number) -> None:
    if from_number < 1:
        print ("Liftoff!")
    else:
        print (from_number)
        countdown(from_number - 1)


### --------------------------------------------------

@dataclass
class PlayingCard:
    rank: str
    suit: str


### --------------------------------------------------


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        """Get value of radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Set radius, raise error if negative"""
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("radius must be non-negative")

    @property
    def area(self):
        """Calculate area inside circle"""
        return self.pi() * self.radius**2

    def cylinder_volume(self, height):
        """Calculate volume of cylinder with circle as base"""
        return self.area * height

    @classmethod
    def unit_circle(cls):
        """Factory method creating a circle with radius 1"""
        return cls(1)

    @staticmethod
    def pi():
        """Value of π, could use math.pi instead though"""
        return 3.1415926535



### --------------------------------------------------



# use Flask to set up a /secret web page that should only be visible to users that are logged in or otherwise authenticated:
# In production, you can use the Flask-Login extension instead, which adds more security and functionality.

# app = Flask(__name__)

# def login_required(func) -> Any:
#     @wraps(func)
#     def wrapper(*args, **kwargs) -> None:
#         if g.user is None:
#             return redirect(url_for("login", next=request.url))
#         return func(*args, **kwargs)
#     return wrapper


# @app.route("/secret")
# @login_required
# def secret():
#     pass


### --------------------------------------------------


# @register  (for PLUGINS)
# stores a reference to the decorated function in the global PLUGINS dictionary.

PLUGINS = dict()

def register(func):
    """Register a function as a plug-in"""
    PLUGINS[func.__name__] = func
    return func



### --------------------------------------------------

# @slow_down
# sleep one second before it calls the decorated function:

def slow_down(func: Callable) -> Any:
    @wraps(func)
    def wrapper(*args, ** kwargs)->Any:
        time.sleep(0.5)
        result = func(*args, **kwargs)
        return result
    return wrapper

@slow_down
def countdown(from_number) -> None:
    if from_number < 1:
        print ("Liftoff!")
    else:
        print (from_number)
        countdown(from_number - 1)


### --------------------------------------------------


# @debug
#     """Print the function signature and return value"""
# build 'signature' with a nice comma between args and kwargs

def debug(func: Callable) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs)->Any:
        args_repr = [repr(arg) for arg in args]
        kwargs_repr = [f"{k}={repr(v)}" for k,v in kwargs.items()]
        
        # print(f"the parameters being sent in are: {*args, *{*kwargs}}")

        result = func(*args, **kwargs)
        
        # print (f"{func.__name__}() returns {result}")
        print (f"{func.__name__} ({args_repr}, {kwargs_repr}) returned {result} (of type: {type(result).__name__})")
        return result
    return wrapper

@debug
def test_debug(text: str, age=None) -> str:
    if age == None:
        return text
    else:
        return (f"{text} {age} years old")



### --------------------------------------------------


# @timer
# time how long a function takes to complete and print it out 

def timer(func: Callable) -> Any:
    @wraps(func)
    def wrapper(*args, ** kwargs)->Any:
        start_time = datetime.now()
        start = time.perf_counter()
        result = func(*args, **kwargs)
        stop_time = datetime.now()
        stop = time.perf_counter()
        print (f"{func.__name__}() took: {stop_time-start_time} seconds")
        print(f"using perf_counter... {func.__name__}() took: {stop-start} seconds")
        return result
    return wrapper


@timer
def call_timer()-> None:
    time.sleep(.5)



### --------------------------------------------------
### --------------------------------------------------
### TESTING
### --------------------------------------------------
### --------------------------------------------------


def main()->None:
    # call_timer()
    # test_debug("blah blah", age=5)

    # countdown(3)

    result = countdown_repeated(2)

if __name__ == "__main__":
    main()