import yaml
from copy import deepcopy

# Simulate incoming YAML data (e.g., from an API response or file)
incoming_yaml = """
network_devices:
  - hostname: r1.border
    role: border
    mgmt_ip: 10.0.0.1
    platform: cisco_ios
    interfaces:
      - name: GigabitEthernet0/0
        description: To ISP1
        ip: 203.0.113.1/30
      - name: GigabitEthernet0/1
        description: To ISP2
        ip: 198.51.100.1/30

  - hostname: r2.core
    role: core
    mgmt_ip: 10.0.0.2
    platform: cisco_nxos
    interfaces:
      - name: Ethernet1/1
        description: To r1
      - name: Ethernet1/2
        description: To r3

  - hostname: sw1.access
    role: access
    mgmt_ip: 10.0.0.10
    platform: cisco_ios
    interfaces: []   # No configured interfaces yet
"""

# Step 1: Safely load the YAML into a Python dict
data = yaml.safe_load(incoming_yaml)

# Make a working copy so we don't modify the original
devices = deepcopy(data["network_devices"])

#print(type(devices))


print("Original device count:", len(devices))
print()

# Task 1: Find all devices with role 'border'
border_devices = [d for d in devices if d.get("role") == "border"]
print("Border devices:")
for d in border_devices:
    print(f" - {d['hostname']} ({d['mgmt_ip']})")
print()

# Task 2: Add a default 'site' key to all devices
for device in devices:
    if "site" not in device:
        device["site"] = "DC1"

# Task 3: Add a loopback interface to every device that doesn't have one
for device in devices:
    # Check if any interface looks like a loopback
    has_loopback = any(
        interface["name"].lower().startswith(("loopback", "lo"))
        for interface in device.get("interfaces", [])
        if "name" in interface
    )
    if not has_loopback:
        device.setdefault("interfaces", []).append({
            "name": "Loopback0",
            "description": "Management loopback",
            "ip": f"192.168.{device['mgmt_ip'].split('.')[-1]}.1/32"
        })

# Task 4: Collect all management IPs into a list
mgmt_ips = [d["mgmt_ip"] for d in devices]
print("All management IPs:", mgmt_ips)

# Task 5: Output cleaned/modified YAML
print("\nModified YAML output:")
print(yaml.safe_dump({"network_devices": devices}, default_flow_style=False, indent=2))