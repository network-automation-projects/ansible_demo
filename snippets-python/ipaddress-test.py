import ipaddress

# # For your example: Third octet 240 (11110000) in mask
# network = ipaddress.ip_network('172.16.0.0/20')  # /20 implies 255.255.240.0
# print(f"Network: {network}")
# print(f"Netmask: {network.netmask}")  # Outputs 255.255.240.0
# print(f"Binary Netmask: {network.netmask.packed.hex()}")  # Hex view; for binary:
# binary_mask = ' '.join(f'{octet:08b}' for octet in network.netmask.packed)
# print(f"Binary: {binary_mask}")  # 11111111 11111111 11110000 00000000

# # Manipulate: Get subnets
# for subnet in network.subnets(new_prefix=24):  # Split into /24s
#     print(subnet)
#     # here we are divide the /20 into smaller /24 subnets 
#     # (borrowing 4 more bits from the host portion).

# net = ipaddress.ip_network('172.16.0.0/20')
# print(f"Usable hosts in /20: {net.num_addresses - 2}")  # 4094


# network = ipaddress.ip_network('10.0.0.0/16')
# subnets = list(network.subnets(new_prefix=20))  # Carve into /20s
# for s in subnets[:3]: print(s)

# # this takes the /16 chunk and divides it into /20 chunks.
# # i see 3 /20 chunks.  what other subnet sizes could we use?
# # /19, /18, /17, /16, /15, /14, /13, /12, /11, /10, /9, /8, /7, /6, /5, /4, /3, /2, /1, /0

# #problem 4
# network = ipaddress.ip_network('10.0.0.0/16')
# subnets = list(network.subnets(new_prefix=18))  # Carve into /20s
# for s in subnets[:4]: 
#     print(s)

# for s in subnets[:4]: 
#     net = ipaddress.ip_network(s)
#     print(f"Usable hosts in /18: {net.num_addresses - 2}")



# #another example
# # For your example: Third octet 240 (11110000) in mask
# network = ipaddress.ip_network('172.16.0.0/24')  # /24 implies 255.255.255.0
# print(f"Network: {network}")
# print(f"Netmask: {network.netmask}")  # Outputs 255.255.240.0
# print(f"Binary Netmask: {network.netmask.packed.hex()}")  # Hex view; for binary:
# binary_mask = ' '.join(f'{octet:08b}' for octet in network.netmask.packed)
# print(f"Binary: {binary_mask}")  # 11111111 11111111 11110000 00000000

# # Manipulate: Get subnets
# for subnet in network.subnets(new_prefix=28):  # Split into /28s
#     print(subnet)
#     # here we are divide the /24 into smaller /28 subnets 
#     # (borrowing 4 more bits from the host portion).

# #this demonstrates the bitwise operator:
# print(45 & 240)  # Outputs: 32

# #this demonstrates the network address of the ip address
# print(ipaddress.ip_interface('172.16.45.200/20').network)  # 172.16.32.0/20
# #the 200 could be any number between 0 and 255 
# # because the network address is the first 20 bits of the ip address.
# #the others are host bits.

# # Full example
# print(bin(45))          # 0b101101
# print(bin(240))         # 0b11110000
# print(45 & 240)         # 32
# print(bin(45 & 240))    # 0b100000 → 00100000 = 32


# test - we have 10.10.0.0/20 to allocate.
# Sequential allocation:
# - one /24 for servers (largest)
# - one /26 for printers (next available after /24)
# - one /28 for management (right after /26)

parent_network = ipaddress.ip_network('10.10.0.0/20')
print(f"\n=== Parent Network ===")
print(f"{parent_network} ({parent_network.num_addresses} addresses)")

# Allocate Servers: /24 starting at 10.10.0.0
servers = ipaddress.ip_network('10.10.0.0/24')
print(f"\n=== Servers (/24 - largest) ===")
print(f"{servers}")
print(f"First block: {servers.num_addresses} addresses, {servers.num_addresses - 2} usable")

# Allocate Printers: /26 starting at 10.10.1.0 (next available after /24)
#printers = ipaddress.ip_network('10.10.1.0/26') # we hardcoded this.  could we generate it?
# yes, we can generate it.  we can use the subnets function to generate the next available subnet.
# Find first /26 subnet that doesn't overlap with servers (starts after 10.10.0.255)

all_26_subnets = list(parent_network.subnets(new_prefix=26)) # this generates all the /26 subnets in the parent network.
servers_end = servers.broadcast_address  # 10.10.0.255   #this is the first /26 subnet that doesn't overlap with the servers subnet.
for subnet in all_26_subnets: #testing each subnet to see if it overlaps with the servers subnet.
    if subnet.network_address > servers_end:
        printer_start_subnet = subnet # if the subnet doesn't overlap with the servers subnet, 
        # then we assign it to the printers subnet.
        #so this grabs the first /26 subnet that doesn't overlap with the servers subnet.
        #which will be the start of the printers subnet.
        break

print(f"\n=== Printers (/26) ===")
print(f"{printer_start_subnet}")
print(f"Next available after /24: starts at .1.0, takes {printer_start_subnet.num_addresses} addresses")


# Allocate Management: /28 starting at 10.10.1.64 (right after the /26)
management = ipaddress.ip_network('10.10.1.64/28')
print(f"\n=== Management (/28) ===")
print(f"{management}")
print(f"Right after the /26: starts at .1.64, takes {management.num_addresses} addresses")

# Calculate remaining space
print(f"\n=== Remaining Space ===")
# Next available starts at 10.10.1.80 (after the /28 which ends at 10.10.1.79)
next_available = ipaddress.ip_address('10.10.1.80')
print(f"Next available: {next_available}")
print(f"Remaining: {next_available}/{26} onward (plus the rest of 10.10.2.0/23, 10.10.4.0/22, etc. - plenty left for future growth)")

# Verify all allocations are within parent network
allocated = [servers, printer_start_subnet, management]  #servers and managemenet etc are lists of ip addresses.
print(f"\n=== Validation ===")
for subnet in allocated: #this is checking if the allocated subnets are within the parent network.
    is_subnet = subnet.subnet_of(parent_network)
    print(f"{subnet} is within {parent_network}: {is_subnet}")
