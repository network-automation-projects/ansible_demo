#for- else

# Search for a value; if not found, run the else block
items = [2, 4, 6, 8, 10]
target = 7

for x in items:
    if x == target:
        print(f"Found {target}")
        break
else:
    # Runs only if the loop never hit 'break'
    print(f"{target} not in list")
# Output: 7 not in list

#Another example: check if a list has any negative number.
numbers = [1, 3, 5, 9]
for n in numbers:
    if n < 0:
        print("Has negative")
        break
else:
    print("All non-negative")  # This runs

# if elif else

score = 78

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"   # 78 matches here
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(grade)  # C


x = 0
if x > 0:
    print("positive")
elif x < 0:
    print("negative")
else:
    print("zero")  # zero


# --- range() ---
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

for i in range(2, 10):
    print(i)  # 2 through 9

for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8


# --- while ---
count = 0
while count <= 4:
    print(count)
    count += 1

# while True + break
count = 0
while True:
    print(count)
    count += 1
    if count >= 5:
        break


# --- enumerate() ---
hosts = ["r1", "r2", "r3"]
for idx, host in enumerate(hosts, start=1):
    print(f"Device {idx}: {host}")
# Device 1: r1, Device 2: r2, Device 3: r3


# --- iterating dicts ---
device_ips = {"r1": "10.0.0.1", "r2": "10.0.0.2", "r3": "10.0.0.3"}
for hostname, ip in device_ips.items():
    print(f"{hostname}: {ip}")


# --- continue ---
interfaces = ["Eth0", "disabled", "Eth1", "Eth2", "down", "Eth3"]
for iface in interfaces:
    if iface in ("disabled", "down"):
        continue
    print(iface)  # Eth0, Eth1, Eth2, Eth3


# --- nested loops ---
devices = ["r1", "r2"]
commands = ["show version", "show ip int brief"]
for device in devices:
    for cmd in commands:
        print(f"{device}: {cmd}")


# --- accumulation ---
values = [10, 20, 30, 40]
total = 0
for v in values:
    total += v
print(total)  # 100

numbers = [1, 2, 3, 4, 5, 6]
evens = []
for n in numbers:
    if n % 2 == 0:
        evens.append(n)
print(evens)  # [2, 4, 6]