from functools import wraps # makes debugging easier because it keeps the original functions' __name__ and other metadata intact


# TODO: Create the logging_decorator() function 
def logging_decorator(function):        # pass in the function we are decorating
    def wrapper(*args):                 # grab the arguments that wrapped function is receiving
        print(f"you called {function.__name__} {args}")     # print all the args as a tuple
        result = function(*args)        # run the function that is being wrapped which calculates
        print(f"it returned {result}")  # grab the result from the wrapped function that ran
        return result                   # return the result that the wrapped function created
    return wrapper                      # return the wrapper (so it replaces the original when decorated)


# TODO: Use the decorator 
@logging_decorator
def a_function(*args):
    return sum(args)
    
a_function(1,2,3)