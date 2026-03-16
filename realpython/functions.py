# def say_hello():
#     print("Hello")

# def greet_jane(func):
#     print("Hello jane")

# greet_jane(say_hello)



# vs
def say_hello():
    print("Hello")

def greet_jane(func):
    print("Hello jane")
    func()

greet_jane(say_hello)