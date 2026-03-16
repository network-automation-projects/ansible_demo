from functools import wraps

def debug_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"CALL {func.__name__} args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"RETURN {func.__name__} -> {result!r}")
        return result
    return wrapper


# Decorate this function:

@debug_calls
def add(a, b):
    return a + b

#Run:
print(add(2, 3))


'''You should see:
a “CALL add …”
a “RETURN add …”
then the printed result'''