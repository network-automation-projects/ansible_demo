# Networking Module

This module provisions the core networking infrastructure for the AWS VPC demo project.

## Purpose

The networking module encapsulates all VPC-related resources including:
- VPC creation and configuration
- Public and private subnets
- Internet Gateway for public internet access
- NAT Gateway for private subnet outbound access
- Route tables and associations

## Dependencies

This module has no dependencies on other modules. It is the foundation that other modules (security, compute) depend on.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| vpc_cidr | CIDR block for the VPC | `string` | n/a | yes |
| public_subnet_cidr | CIDR block for the public subnet | `string` | n/a | yes |
| private_subnet_cidr | CIDR block for the private subnet | `string` | n/a | yes |
| availability_zone | Availability zone for subnets (empty to auto-generate) | `string` | `""` | no |
| aws_region | AWS region | `string` | n/a | yes |
| enable_nat_gateway | Enable NAT Gateway for private subnet | `bool` | `true` | no |
| project_name | Project name for resource naming | `string` | n/a | yes |
| environment | Environment name | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | ID of the created VPC |
| public_subnet_id | ID of the public subnet |
| private_subnet_id | ID of the private subnet |
| internet_gateway_id | ID of the Internet Gateway |
| nat_gateway_id | ID of the NAT Gateway (null if disabled) |
| public_route_table_id | ID of the public route table |
| private_route_table_id | ID of the private route table |
| availability_zone | Availability zone used for subnets |

## Architecture

```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   ├── Internet Gateway (attached)
│   └── Public Route Table (0.0.0.0/0 → IGW)
└── Private Subnet (10.0.2.0/24)
    ├── NAT Gateway (if enabled)
    └── Private Route Table (0.0.0.0/0 → NAT)
```

## Usage

```hcl
module "networking" {
  source = "./modules/networking"

  vpc_cidr           = "10.0.0.0/16"
  public_subnet_cidr = "10.0.1.0/24"
  private_subnet_cidr = "10.0.2.0/24"
  aws_region         = "us-east-1"
  enable_nat_gateway = true
  project_name       = "my-project"
  environment        = "dev"
}
```

## Cost Considerations

- **NAT Gateway**: Costs approximately $0.045/hour (~$32/month) when enabled
- To reduce costs in development, set `enable_nat_gateway = false`
- Note: Without NAT Gateway, private subnet resources cannot access the internet

## Notes

- DNS hostnames and DNS support are enabled on the VPC by default
- Public subnet has `map_public_ip_on_launch = true` for automatic public IP assignment
- NAT Gateway is placed in the public subnet (required by AWS)
- Route tables are automatically associated with their respective subnets
