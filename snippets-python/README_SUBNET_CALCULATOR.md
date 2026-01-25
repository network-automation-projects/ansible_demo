# Subnet Calculator - CSV to Terraform-like Subnet Allocation

A declarative subnet calculator that reads requirements from CSV and generates subnet allocations similar to Terraform's approach.

## Features

- **Declarative approach**: Define subnet requirements in CSV, script calculates allocations
- **Terraform-like output**: Generates Terraform configuration format
- **Multiple output formats**: Table, JSON, or Terraform HCL
- **Validates allocations**: Ensures subnets fit and don't overlap
- **Tags support**: Include tags in CSV for Terraform resource tagging

## CSV Format

The CSV file must contain at minimum `name` and `size` columns:

```csv
name,size,availability_zone,subnet_type,tags
public-subnet-1,24,us-east-1a,public,"Environment=prod,Project=webapp"
private-subnet-1,24,us-east-1b,private,"Environment=prod,Project=webapp"
database-subnet-1,26,us-east-1a,database,"Environment=prod,Project=webapp"
```

**Note**: When tags contain commas, the entire tags field must be quoted. CSV parsing requires proper quoting for fields containing delimiters.

### Columns

- **name** (required): Subnet name/identifier
- **size** (required): CIDR prefix length (e.g., 24 for /24 subnet)
- **availability_zone** (optional): AWS AZ or similar (e.g., us-east-1a)
- **subnet_type** (optional): Type of subnet (public, private, database, etc.)
- **tags** (optional): Comma-separated key=value pairs, **must be quoted** if containing commas
  - Example: `"Environment=prod,Project=webapp"`
  - Single tag: `Environment=prod` (quotes optional)

## Usage

### Basic Usage

```bash
python subnet_calculator.py subnets_example.csv
```

### Specify VPC CIDR

```bash
python subnet_calculator.py subnets_example.csv --vpc-cidr 172.16.0.0/16
```

### Generate Terraform Configuration

```bash
python subnet_calculator.py subnets_example.csv --vpc-cidr 10.0.0.0/16 --output-format terraform
```

### Generate JSON Output

```bash
python subnet_calculator.py subnets_example.csv --output-format json
```

### Save Output to File

```bash
python subnet_calculator.py subnets_example.csv --output-format terraform --output-file subnets.tf
```

## Example Output

### Table Format (Default)

```
================================================================================
SUBNET ALLOCATION SUMMARY
================================================================================
Parent Network: 10.0.0.0/16
Total Addresses: 65,536
Allocated Addresses: 12,416
Available Addresses: 53,120
Utilization: 18.95%
Number of Subnets: 6

--------------------------------------------------------------------------------
CALCULATED SUBNETS
--------------------------------------------------------------------------------
Name                           CIDR                AZ             Type       Hosts      
--------------------------------------------------------------------------------
public-subnet-1                10.0.0.0/24         us-east-1a     public     254        
public-subnet-2                10.0.1.0/24         us-east-1b     public     254        
private-subnet-1               10.0.2.0/24         us-east-1a     private    254        
private-subnet-2               10.0.3.0/24         us-east-1b     private    254        
database-subnet-1              10.0.4.0/26         us-east-1a     database   62         
database-subnet-2              10.0.4.64/26        us-east-1b     database   62         
```

### Terraform Format

```hcl
# Terraform-like Subnet Configuration (Generated)
# VPC CIDR: 10.0.0.0/16

locals {
  vpc_cidr = "10.0.0.0/16"
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1"
    Type = "public"
    Environment = "prod"
    Project = "webapp"
  }
}
```

## How It Works (Terraform-like Approach)

The script mimics Terraform's declarative subnet allocation:

1. **Read Requirements**: Parse CSV to get subnet requirements
2. **Sequential Allocation**: Allocate subnets sequentially within parent network
3. **Validation**: Ensure subnets fit and don't overlap
4. **Output**: Generate declarative configuration

This is similar to Terraform's `cidrsubnets()` function which allocates subnets declaratively based on size requirements rather than manually calculating CIDR blocks.

## Requirements

- Python 3.9+
- Standard library only (no external dependencies for core functionality)
- Uses `ipaddress` module (built-in) for subnet calculations

## Examples

See `subnets_example.csv` for a sample input file.
