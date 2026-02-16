# Search for a value; if not found, run the else block
items = [2, 4, 6, 8, 10]
target = 7



for item in items:
    if item == target:
        print ("found")
        break
else: 
    print("not in list")
    

#Another example: check if a list has any negative number.
numbers = [1, 3, 5, 9]

for n in numbers:
    if n < 0:
        print("found a neg")
        break
else:
    print ("no neg")


score = 78
# find the highest letter grade using a loop

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(grade)


# --- range() ---
# Loop 5 times (0 to 4) and print each number.
# Then loop from 2 to 9 (inclusive start, exclusive stop).
# Then loop even numbers 0, 2, 4, 6, 8 using range step.

for i in range(5):
    print (str(i))
for i in range(2,10):
    print(str(i))
for i in range(0,10,2):
    print(str(i))

# --- while ---
# Use while to count from 0 to 4 and print each number.
# Optional: while True with break when count reaches 5.

count = 0
while count <= 4:
    print(count)
    count += 1
    

# --- enumerate() ---
hosts = ["r1", "r2", "r3"]
# Print "Device 1: r1", "Device 2: r2", "Device 3: r3" (1-based index).

for i,v in enumerate(hosts,1):
    print(f"Device {i}: {v}")


# --- iterating dicts ---
device_ips = {"r1": "10.0.0.1", "r2": "10.0.0.2", "r3": "10.0.0.3"}
# Loop and print each hostname and IP (use .items()).

for key,value in device_ips.items():
    print(f"{key}: {value}")

# --- continue ---
interfaces = ["Eth0", "disabled", "Eth1", "Eth2", "down", "Eth3"]
# Print only the interface names that are not "disabled" or "down"; use continue to skip.

for iface in interfaces:
    if iface != "disabled" and iface != "down":
        print(iface)
   

# --- nested loops ---
devices = ["r1", "r2"]
commands = ["show version", "show ip int brief"]
# For each device, print the device name and each command (nested loop).

for d in devices:
    for command in commands:
        print(f"{d} - {command}")


# --- accumulation ---
# Sum the list [10, 20, 30, 40] in a loop and print the total.
# Build a new list of only the even numbers from [1, 2, 3, 4, 5, 6] using a loop.
mylist = [10, 20, 30, 40]
# result 100
numbers = [1, 2, 3, 4, 5, 6]
# result [2, 4, 6]



mylist = [10, 20, 30, 40]
total = 0
for x in mylist:
    total += x
print (total)

numbers = [1, 2, 3, 4, 5, 6]
even_only = []
for num in numbers:
    if num % 2 == 0:
        even_only.append(num)
    