#!/usr/bin/env python3
"""Subnet Calculator - Calculate subnets from CSV input (Terraform-like declarative approach).

This script reads subnet requirements from a CSV file and calculates subnet allocations
in a declarative manner similar to Terraform's cidrsubnets function.
"""

import csv
import ipaddress
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class SubnetRequirement:
    """Represents a subnet requirement from CSV input."""
    name: str
    size: int  # CIDR prefix length (e.g., 24 for /24)
    availability_zone: Optional[str] = None
    subnet_type: Optional[str] = None  # public, private, database, etc.
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class CalculatedSubnet:
    """Represents a calculated subnet allocation."""
    name: str
    cidr: str
    availability_zone: Optional[str]
    subnet_type: Optional[str]
    tags: Dict[str, str]
    network_address: str
    broadcast_address: str
    usable_hosts: int


class SubnetCalculator:
    """Calculates subnet allocations from a parent network and requirements."""
    
    def __init__(self, parent_cidr: str):
        """Initialize with parent network CIDR block.
        
        Args:
            parent_cidr: Parent network in CIDR notation (e.g., '10.0.0.0/16')
            
        Raises:
            ValueError: If parent_cidr is invalid
        """
        try:
            self.parent_network = ipaddress.ip_network(parent_cidr, strict=False)
        except ValueError as e:
            raise ValueError(f"Invalid parent CIDR block '{parent_cidr}': {e}")
        
        self.allocated_subnets: List[ipaddress.ip_network] = []
    
    def calculate_subnets(
        self, 
        requirements: List[SubnetRequirement]
    ) -> List[CalculatedSubnet]:
        """Calculate subnet allocations from requirements.
        
        This mimics Terraform's declarative approach by allocating subnets
        sequentially within the parent network without overlaps.
        
        Args:
            requirements: List of subnet requirements
            
        Returns:
            List of calculated subnet allocations
            
        Raises:
            ValueError: If subnets cannot fit in parent network
        """
        calculated: List[CalculatedSubnet] = []
        current_address = int(self.parent_network.network_address)
        parent_end = int(self.parent_network.broadcast_address)
        
        for req in requirements:
            # Calculate the network address for this subnet
            # Find the next available subnet of the requested size starting from current_address
            subnet_size_bits = 32 - req.size
            subnet_size = 2 ** subnet_size_bits
            
            # Align to subnet boundary
            offset = (current_address - int(self.parent_network.network_address)) % subnet_size
            if offset != 0:
                current_address = current_address - offset + subnet_size
            
            # Calculate the subnet network address
            try:
                subnet_address = ipaddress.IPv4Address(current_address)
                subnet_network = ipaddress.ip_network(
                    f"{subnet_address}/{req.size}",
                    strict=False
                )
            except (ValueError, ipaddress.AddressValueError) as e:
                raise ValueError(
                    f"Cannot allocate subnet '{req.name}' (/{req.size}): "
                    f"Invalid network address. Error: {e}"
                )
            
            # Validate subnet fits in parent network
            if not subnet_network.subnet_of(self.parent_network):
                raise ValueError(
                    f"Cannot allocate subnet '{req.name}' ({subnet_network}): "
                    f"Exceeds parent network {self.parent_network}"
                )
            
            # Check subnet end doesn't exceed parent
            subnet_end = int(subnet_network.broadcast_address)
            if subnet_end > parent_end:
                raise ValueError(
                    f"Cannot allocate subnet '{req.name}' ({subnet_network}): "
                    f"Subnet extends beyond parent network {self.parent_network}"
                )
            
            # Check for overlaps with previously allocated subnets
            for allocated in self.allocated_subnets:
                if subnet_network.overlaps(allocated):
                    raise ValueError(
                        f"Subnet {subnet_network} overlaps with previously allocated {allocated}"
                    )
            
            self.allocated_subnets.append(subnet_network)
            
            # Move current address to next available position
            current_address = subnet_end + 1
            
            # Calculate usable hosts (subtract network and broadcast)
            usable_hosts = subnet_network.num_addresses - 2
            
            calculated.append(CalculatedSubnet(
                name=req.name,
                cidr=str(subnet_network),
                availability_zone=req.availability_zone,
                subnet_type=req.subnet_type,
                tags=req.tags,
                network_address=str(subnet_network.network_address),
                broadcast_address=str(subnet_network.broadcast_address),
                usable_hosts=usable_hosts
            ))
        
        return calculated
    
    def get_summary(self) -> Dict:
        """Get summary statistics about subnet allocation.
        
        Returns:
            Dictionary with allocation statistics
        """
        total_allocated = sum(s.num_addresses for s in self.allocated_subnets)
        parent_size = self.parent_network.num_addresses
        
        return {
            "parent_network": str(self.parent_network),
            "parent_cidr": str(self.parent_network),
            "total_addresses": parent_size,
            "allocated_addresses": total_allocated,
            "available_addresses": parent_size - total_allocated,
            "utilization_percent": (total_allocated / parent_size) * 100,
            "subnet_count": len(self.allocated_subnets)
        }


def read_subnet_requirements(csv_path: Path) -> List[SubnetRequirement]:
    """Read subnet requirements from CSV file.
    
    Expected CSV format:
        name,size,availability_zone,subnet_type,tags
        public-subnet-1,24,us-east-1a,public,Environment=prod
        private-subnet-1,24,us-east-1b,private,Environment=prod
        
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of SubnetRequirement objects
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV format is invalid
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    requirements: List[SubnetRequirement] = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Validate required columns
        required_cols = {'name', 'size'}
        if not required_cols.issubset(reader.fieldnames or []):
            raise ValueError(
                f"CSV must contain columns: {required_cols}. "
                f"Found: {reader.fieldnames}"
            )
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
            try:
                name = row['name'].strip()
                if not name:
                    raise ValueError(f"Row {row_num}: 'name' cannot be empty")
                
                size = int(row['size'])
                if not (0 <= size <= 32):
                    raise ValueError(f"Row {row_num}: 'size' must be 0-32, got {size}")
                
                az = row.get('availability_zone', '').strip() or None
                subnet_type = row.get('subnet_type', '').strip() or None
                
                # Parse tags (format: "key1=value1,key2=value2")
                tags: Dict[str, str] = {}
                if 'tags' in row and row['tags']:
                    for tag_pair in row['tags'].split(','):
                        tag_pair = tag_pair.strip()
                        if '=' in tag_pair:
                            key, value = tag_pair.split('=', 1)
                            tags[key.strip()] = value.strip()
                
                requirements.append(SubnetRequirement(
                    name=name,
                    size=size,
                    availability_zone=az,
                    subnet_type=subnet_type,
                    tags=tags
                ))
            except (KeyError, ValueError) as e:
                raise ValueError(f"Error parsing CSV row {row_num}: {e}")
    
    return requirements


def generate_terraform_output(subnets: List[CalculatedSubnet], vpc_cidr: str) -> str:
    """Generate Terraform-like declarative configuration output.
    
    Args:
        subnets: List of calculated subnets
        vpc_cidr: VPC CIDR block
        
    Returns:
        Terraform configuration as string
    """
    output_lines = [
        "# Terraform-like Subnet Configuration (Generated)",
        f"# VPC CIDR: {vpc_cidr}",
        "",
        "locals {",
        "  vpc_cidr = \"" + vpc_cidr + "\"",
        "}",
        "",
    ]
    
    for subnet in subnets:
        subnet_resource_name = subnet.name.replace('-', '_').replace(' ', '_')
        
        output_lines.extend([
            f"resource \"aws_subnet\" \"{subnet_resource_name}\" {{",
            f"  vpc_id            = aws_vpc.main.id",
            f"  cidr_block        = \"{subnet.cidr}\"",
        ])
        
        if subnet.availability_zone:
            output_lines.append(f"  availability_zone = \"{subnet.availability_zone}\"")
        
        if subnet.subnet_type == 'public':
            output_lines.append(f"  map_public_ip_on_launch = true")
        
        # Tags
        output_lines.append("")
        output_lines.append("  tags = {")
        output_lines.append(f"    Name = \"{subnet.name}\"")
        if subnet.subnet_type:
            output_lines.append(f"    Type = \"{subnet.subnet_type}\"")
        for key, value in subnet.tags.items():
            output_lines.append(f"    {key} = \"{value}\"")
        output_lines.append("  }")
        output_lines.append("}")
        output_lines.append("")
    
    return "\n".join(output_lines)


def generate_json_output(subnets: List[CalculatedSubnet], summary: Dict) -> str:
    """Generate JSON output for programmatic consumption.
    
    Args:
        subnets: List of calculated subnets
        summary: Summary statistics
        
    Returns:
        JSON string
    """
    import json
    
    output = {
        "summary": summary,
        "subnets": [
            {
                "name": s.name,
                "cidr": s.cidr,
                "availability_zone": s.availability_zone,
                "subnet_type": s.subnet_type,
                "network_address": s.network_address,
                "broadcast_address": s.broadcast_address,
                "usable_hosts": s.usable_hosts,
                "tags": s.tags
            }
            for s in subnets
        ]
    }
    
    return json.dumps(output, indent=2)


def main():
    """Main entry point for subnet calculator script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Calculate subnets from CSV input (Terraform-like declarative approach)"
    )
    parser.add_argument(
        'csv_file',
        type=Path,
        help='Path to CSV file with subnet requirements'
    )
    parser.add_argument(
        '--vpc-cidr',
        type=str,
        default='10.0.0.0/16',
        help='Parent VPC CIDR block (default: 10.0.0.0/16)'
    )
    parser.add_argument(
        '--output-format',
        choices=['terraform', 'json', 'table'],
        default='table',
        help='Output format (default: table)'
    )
    parser.add_argument(
        '--output-file',
        type=Path,
        help='Write output to file instead of stdout'
    )
    
    args = parser.parse_args()
    
    try:
        # Read requirements from CSV
        requirements = read_subnet_requirements(args.csv_file)
        
        if not requirements:
            print("Warning: No subnet requirements found in CSV file", file=sys.stderr)
            return 1
        
        # Calculate subnets
        calculator = SubnetCalculator(args.vpc_cidr)
        calculated_subnets = calculator.calculate_subnets(requirements)
        summary = calculator.get_summary()
        
        # Generate output
        if args.output_format == 'terraform':
            output = generate_terraform_output(calculated_subnets, args.vpc_cidr)
        elif args.output_format == 'json':
            output = generate_json_output(calculated_subnets, summary)
        else:  # table format
            output_lines = [
                "=" * 80,
                "SUBNET ALLOCATION SUMMARY",
                "=" * 80,
                f"Parent Network: {summary['parent_network']}",
                f"Total Addresses: {summary['total_addresses']:,}",
                f"Allocated Addresses: {summary['allocated_addresses']:,}",
                f"Available Addresses: {summary['available_addresses']:,}",
                f"Utilization: {summary['utilization_percent']:.2f}%",
                f"Number of Subnets: {summary['subnet_count']}",
                "",
                "-" * 80,
                "CALCULATED SUBNETS",
                "-" * 80,
                f"{'Name':<30} {'CIDR':<20} {'AZ':<15} {'Type':<10} {'Hosts':<10}",
                "-" * 80,
            ]
            
            for subnet in calculated_subnets:
                az = subnet.availability_zone or "N/A"
                subnet_type = subnet.subnet_type or "N/A"
                output_lines.append(
                    f"{subnet.name:<30} {subnet.cidr:<20} {az:<15} {subnet_type:<10} {subnet.usable_hosts:<10}"
                )
            
            output = "\n".join(output_lines)
        
        # Write output
        if args.output_file:
            args.output_file.write_text(output)
            print(f"Output written to: {args.output_file}", file=sys.stderr)
        else:
            print(output)
        
        return 0
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
