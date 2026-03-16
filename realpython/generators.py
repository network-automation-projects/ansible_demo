# generator examples

# def example():
#     yield 1
#     yield 2

# g = example()

# print(next(g))
# print(next(g))
# # print(next(g))


# -----------

# def count_up_to(n):
#     for i in range(n):
#         print(f"About to yield {i}")
#         yield i
#         print(f"Resumed after yielding {i}")

# g = count_up_to(3)

# print("First call:")
# print(next(g))

# print("\nSecond call:")
# print(next(g))

# print("\nThird call:")
# print(next(g))

# print("\nFourth call:")
# print(next(g))


# ------------
# to process raw string a little at a time in case it's really long 
# so you don't have to load it all into memory
# only process the OSPF routes with a lazy filter

raw_output = """
O 10.0.0.0/24 via 192.168.1.1
O 10.0.1.0/24 via 192.168.1.1
C 192.168.1.0/24 is directly connected
O 10.0.2.0/24 via 192.168.1.2
"""

def stream_routes(output):
    for line in output.strip().split("\n"):
        if line.startswith("O"):  # Only OSPF routes
            yield line


for route in stream_routes(raw_output):
    print("Processing route:", route)



# ------------
# log streaming
# prompt: send alerts for all the logs at file_path that have the word ERROR in them using a generator
# don't read the whole file at once, process it line by line


def tail_log(file_path):
    with open(file_path) as f:
        for line in f:
            if "ERROR" in line:
                yield line

for error in tail_log("network.log"):
    send_alert(error)