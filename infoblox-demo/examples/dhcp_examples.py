#!/usr/bin/env python3
"""DHCP operation examples using Infoblox."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infoblox_client import InfobloxClient
from src.dhcp_manager import DHCPManager


def main():
    """Demonstrate DHCP operations."""
    print("=== DHCP Management Examples ===\n")

    # Initialize client
    client = InfobloxClient.from_config_file()
    dhcp = DHCPManager(client)

    # Example 1: Create DHCP network
    print("1. Creating DHCP network: 192.168.1.0/24")
    network = dhcp.create_network("192.168.1.0/24", comment="Production network")
    print(f"   Created: {network.network} (ref: {network._ref})\n")

    # Example 2: Create DHCP range
    print("2. Creating DHCP range: 192.168.1.100-192.168.1.200")
    dhcp_range = dhcp.create_range(
        "192.168.1.100",
        "192.168.1.200",
        "192.168.1.0/24",
        comment="DHCP pool",
    )
    print(
        f"   Created: {dhcp_range.start_ip}-{dhcp_range.end_ip} "
        f"(ref: {dhcp_range._ref})\n"
    )

    # Example 3: Create DHCP reservation
    print("3. Creating DHCP reservation: 192.168.1.50 for MAC 00:11:22:33:44:55")
    reservation = dhcp.create_reservation(
        "192.168.1.50",
        "00:11:22:33:44:55",
        name="server-01",
        comment="Production server",
    )
    print(
        f"   Created: {reservation.ipv4addr} -> {reservation.mac} "
        f"(ref: {reservation._ref})\n"
    )

    # Example 4: List all networks
    print("4. Listing all DHCP networks")
    networks = dhcp.get_networks()
    print(f"   Found {len(networks)} network(s):")
    for net in networks:
        print(f"     - {net.network} ({net.comment or 'No comment'})")

    # Example 5: List ranges for a network
    print("\n5. Listing DHCP ranges for 192.168.1.0/24")
    ranges = dhcp.get_ranges(network="192.168.1.0/24")
    print(f"   Found {len(ranges)} range(s):")
    for r in ranges:
        print(f"     - {r.start_ip}-{r.end_ip} ({r.comment or 'No comment'})")

    # Example 6: List reservations
    print("\n6. Listing all DHCP reservations")
    reservations = dhcp.get_reservations()
    print(f"   Found {len(reservations)} reservation(s):")
    for res in reservations:
        print(
            f"     - {res.ipv4addr} -> {res.mac} "
            f"({res.name or 'No name'})"
        )


if __name__ == "__main__":
    main()
