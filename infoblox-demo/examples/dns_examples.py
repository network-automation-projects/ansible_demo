#!/usr/bin/env python3
"""DNS operation examples using Infoblox."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infoblox_client import InfobloxClient
from src.dns_manager import DNSManager


def main():
    """Demonstrate DNS operations."""
    print("=== DNS Management Examples ===\n")

    # Initialize client (uses mock server by default)
    client = InfobloxClient.from_config_file()
    dns = DNSManager(client)

    # Example 1: Create A record
    print("1. Creating A record: web.example.com -> 192.168.1.10")
    a_record = dns.create_a_record("web.example.com", "192.168.1.10", comment="Web server")
    print(f"   Created: {a_record.name} -> {a_record.ipv4addr} (ref: {a_record._ref})\n")

    # Example 2: Create CNAME
    print("2. Creating CNAME: www.example.com -> web.example.com")
    cname = dns.create_cname("www.example.com", "web.example.com", comment="WWW alias")
    print(f"   Created: {cname.name} -> {cname.canonical} (ref: {cname._ref})\n")

    # Example 3: Create PTR record (reverse DNS)
    print("3. Creating PTR record: 192.168.1.10 -> web.example.com")
    ptr = dns.create_ptr_record("192.168.1.10", "web.example.com", comment="Reverse DNS")
    print(f"   Created: {ptr.ipv4addr} -> {ptr.ptrdname} (ref: {ptr._ref})\n")

    # Example 4: Search for records
    print("4. Searching for records matching 'web.example.com'")
    records = dns.search_records("web.example.com")
    print(f"   Found {len(records)} record(s):")
    for record in records:
        print(f"     - {record.name} ({record.record_type})")

    # Example 5: Get A records
    print("\n5. Getting all A records")
    a_records = dns.get_a_records()
    print(f"   Found {len(a_records)} A record(s):")
    for record in a_records:
        print(f"     - {record.name} -> {record.ipv4addr}")

    # Example 6: Get CNAME records
    print("\n6. Getting all CNAME records")
    cname_records = dns.get_cname_records()
    print(f"   Found {len(cname_records)} CNAME record(s):")
    for record in cname_records:
        print(f"     - {record.name} -> {record.canonical}")


if __name__ == "__main__":
    main()
