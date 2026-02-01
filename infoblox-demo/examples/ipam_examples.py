#!/usr/bin/env python3
"""IPAM operation examples using Infoblox."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infoblox_client import InfobloxClient
from src.ipam_manager import IPAMManager


def main():
    """Demonstrate IPAM operations."""
    print("=== IPAM Management Examples ===\n")

    # Initialize client
    client = InfobloxClient.from_config_file()
    ipam = IPAMManager(client)

    # Example 1: Create IPAM network
    print("1. Creating IPAM network: 192.168.1.0/24")
    network = ipam.create_network("192.168.1.0/24", comment="Production network")
    print(f"   Created: {network.network} (ref: {network._ref})\n")

    # Example 2: Get next available IP
    print("2. Getting next available IP in 192.168.1.0/24")
    next_ip = ipam.get_next_available_ip("192.168.1.0/24")
    if next_ip:
        print(f"   Next available IP: {next_ip}\n")
    else:
        print("   No available IPs found\n")

    # Example 3: Allocate IP address
    print("3. Allocating IP 192.168.1.10 for 'web-server'")
    allocated = ipam.allocate_ip("192.168.1.0/24", "192.168.1.10", name="web-server")
    print(
        f"   Allocated: {allocated.ipv4addr} "
        f"(status: {allocated.status}, names: {allocated.names})\n"
    )

    # Example 4: Check IP status
    print("4. Checking status of 192.168.1.10")
    ip_status = ipam.get_ip_status("192.168.1.10")
    if ip_status:
        print(f"   IP: {ip_status.ipv4addr}")
        print(f"   Status: {ip_status.status}")
        print(f"   Network: {ip_status.network}")
        print(f"   Names: {ip_status.names}")
    else:
        print("   IP not found in IPAM")

    # Example 5: List all networks
    print("\n5. Listing all IPAM networks")
    networks = ipam.list_all_networks()
    print(f"   Found {len(networks)} network(s):")
    for net in networks:
        print(f"     - {net.network} ({net.comment or 'No comment'})")

    # Example 6: Get next available IP after allocation
    print("\n6. Getting next available IP after allocation")
    next_ip2 = ipam.get_next_available_ip("192.168.1.0/24")
    if next_ip2:
        print(f"   Next available IP: {next_ip2}")
    else:
        print("   No available IPs found")


if __name__ == "__main__":
    main()
