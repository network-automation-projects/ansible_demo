#!/usr/bin/env python3
"""Complete automation workflow example: Provision and decommission a server."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infoblox_client import InfobloxClient
from src.dns_manager import DNSManager
from src.dhcp_manager import DHCPManager
from src.ipam_manager import IPAMManager


def provision_server(hostname: str, mac: str, network: str):
    """Provision a new server with DNS, DHCP, and IPAM records.

    Args:
        hostname: Server hostname (e.g., "web-server.example.com")
        mac: MAC address
        network: Network CIDR (e.g., "192.168.1.0/24")
    """
    print(f"=== Provisioning Server: {hostname} ===\n")

    # Initialize managers
    client = InfobloxClient.from_config_file()
    ipam = IPAMManager(client)
    dns = DNSManager(client)
    dhcp = DHCPManager(client)

    # Step 1: Get next available IP from IPAM
    print("Step 1: Getting next available IP from IPAM...")
    ip = ipam.get_next_available_ip(network)
    if not ip:
        print(f"ERROR: No available IPs in {network}")
        return None
    print(f"   Allocated IP: {ip}\n")

    # Step 2: Allocate IP in IPAM
    print("Step 2: Allocating IP in IPAM...")
    ipam.allocate_ip(network, ip, name=hostname, comment=f"Server: {hostname}")
    print(f"   IP {ip} allocated for {hostname}\n")

    # Step 3: Create A record in DNS
    print("Step 3: Creating A record in DNS...")
    a_record = dns.create_a_record(hostname, ip, comment=f"Server: {hostname}")
    print(f"   Created: {a_record.name} -> {a_record.ipv4addr}\n")

    # Step 4: Create PTR record (reverse DNS)
    print("Step 4: Creating PTR record (reverse DNS)...")
    ptr = dns.create_ptr_record(ip, hostname, comment=f"Reverse DNS for {hostname}")
    print(f"   Created: {ptr.ipv4addr} -> {ptr.ptrdname}\n")

    # Step 5: Create DHCP reservation
    print("Step 5: Creating DHCP reservation...")
    reservation = dhcp.create_reservation(
        ip, mac, name=hostname, comment=f"Server: {hostname}"
    )
    print(f"   Created: {reservation.ipv4addr} -> {reservation.mac}\n")

    print("=== Server Provisioning Complete ===\n")
    return {
        "ip": ip,
        "a_record_ref": a_record._ref,
        "ptr_record_ref": ptr._ref,
        "reservation_ref": reservation._ref,
    }


def decommission_server(hostname: str, ip: str):
    """Decommission a server by removing all DNS, DHCP, and IPAM records.

    Args:
        hostname: Server hostname
        ip: IP address
    """
    print(f"=== Decommissioning Server: {hostname} ===\n")

    # Initialize managers
    client = InfobloxClient.from_config_file()
    ipam = IPAMManager(client)
    dns = DNSManager(client)
    dhcp = DHCPManager(client)

    # Step 1: Find and delete DNS records
    print("Step 1: Finding DNS records...")
    dns_records = dns.search_records(hostname)
    print(f"   Found {len(dns_records)} DNS record(s)")
    for record in dns_records:
        if record._ref:
            dns.delete_record(record._ref)
            print(f"   Deleted: {record.name} ({record.record_type})")

    # Also delete PTR record
    ptr_records = dns.get_ptr_records(ipv4addr=ip)
    for ptr in ptr_records:
        if ptr._ref:
            dns.delete_record(ptr._ref)
            print(f"   Deleted PTR: {ptr.ipv4addr} -> {ptr.ptrdname}")

    # Step 2: Find and delete DHCP reservation
    print("\nStep 2: Finding DHCP reservation...")
    reservations = dhcp.get_reservations(ipv4addr=ip)
    for res in reservations:
        if res._ref:
            dhcp.delete_reservation(res._ref)
            print(f"   Deleted reservation: {res.ipv4addr} -> {res.mac}")

    # Step 3: Release IP in IPAM
    print("\nStep 3: Releasing IP in IPAM...")
    if ipam.release_ip(ip):
        print(f"   Released IP: {ip}")
    else:
        print(f"   Could not release IP: {ip}")

    print("\n=== Server Decommissioning Complete ===\n")


def main():
    """Run complete automation workflow."""
    print("=== Infoblox Automation Workflow ===\n")

    # Provision a server
    server_info = provision_server(
        "web-server.example.com", "00:11:22:33:44:55", "192.168.1.0/24"
    )

    if server_info:
        # Wait a moment (in real scenario)
        print("\n--- Waiting before decommissioning ---\n")

        # Decommission the server
        decommission_server("web-server.example.com", server_info["ip"])


if __name__ == "__main__":
    main()
