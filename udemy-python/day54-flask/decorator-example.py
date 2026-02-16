import time
current_time = time.time()
print(current_time) # seconds since Jan 1st, 1970 

# Write your code below 👇
def time_decorator(function_name):
    def wrapper(*args):
        # grab start time 
        start_time = time.time() 
        result = function_name(*args)
        finish_time = time.time() 
        elapsed = finish_time - start_time
        print(str(elapsed))
        return result
    return wrapper

def speed_calc_decorator():
  pass

def fast_function():
  for i in range(1000000):
    i * i
        

def slow_function():
  for i in range(10000000):
    i * i
    
decorated_function = time_decorator(slow_function)
decorated_function()
