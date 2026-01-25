# Security Module

This module manages security groups and access policies for the AWS VPC demo project.

## Purpose

The security module provides network-level access control through AWS Security Groups. It defines ingress and egress rules that control traffic flow to and from resources.

## Dependencies

This module depends on the **networking module** for the VPC ID where security groups will be created.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| vpc_id | ID of the VPC where security groups will be created | `string` | n/a | yes |
| allowed_ssh_cidr | CIDR block allowed for SSH access (use /32 for single IP) | `string` | n/a | yes |
| allowed_http_cidr | CIDR block allowed for HTTP access | `string` | n/a | yes |
| project_name | Project name for resource naming | `string` | n/a | yes |
| environment | Environment name | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| web_security_group_id | ID of the web security group |
| web_security_group_arn | ARN of the web security group |

## Security Group Rules

### Web Security Group

**Ingress Rules:**
- **SSH (port 22)**: Allowed from `allowed_ssh_cidr` (restrict to your IP in production!)
- **HTTP (port 80)**: Allowed from `allowed_http_cidr`

**Egress Rules:**
- **All traffic**: Allowed to `0.0.0.0/0` (required for outbound internet access)

## Usage

```hcl
module "security" {
  source = "./modules/security"

  vpc_id            = module.networking.vpc_id
  allowed_ssh_cidr  = "1.2.3.4/32"  # Your public IP
  allowed_http_cidr = "0.0.0.0/0"
  project_name      = "my-project"
  environment       = "dev"
}
```

## Security Best Practices

1. **Restrict SSH Access**: Always use `/32` CIDR notation for single IP addresses
   - Example: `allowed_ssh_cidr = "203.0.113.42/32"` (your public IP)
   - Find your IP at: https://whatismyip.com

2. **Principle of Least Privilege**: Only open ports that are necessary
   - This module opens SSH (22) and HTTP (80) as examples
   - Add additional ingress rules only as needed

3. **Production Considerations**:
   - Never use `0.0.0.0/0` for SSH in production
   - Consider using AWS Systems Manager Session Manager instead of SSH
   - Use HTTPS (port 443) instead of HTTP for production web traffic

## Notes

- Security groups are stateful: if you allow inbound traffic, the response is automatically allowed
- Security groups act as a virtual firewall at the instance level
- Multiple security groups can be attached to a single instance
- Rules are evaluated per rule, not per security group
