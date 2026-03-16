
from functools import wraps
from typing import Any,Callable

def retry(*, times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs)->Any:
            for _ in range(0, times-1):
                func(*args, **kwargs)
            return(func)
        return wrapper
    return decorator


            

















# def retry(*, times=3)-> Any:
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs)->Any:
#             for i in range(0,times):
#                 func(*args, **kwargs)
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator




@retry(times=2)
def call_api():
    
    print ("me")