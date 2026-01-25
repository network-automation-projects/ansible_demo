# Compute Module

This module provisions EC2 compute resources for the AWS VPC demo project.

## Purpose

The compute module creates and configures EC2 instances with:
- Automatic web server installation (Apache HTTP Server)
- User data scripts for initialization
- Integration with networking and security modules

## Dependencies

This module depends on:
- **Networking module**: For subnet ID where the instance will be launched
- **Security module**: For security group IDs to attach to the instance

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| subnet_id | ID of the subnet where the EC2 instance will be launched | `string` | n/a | yes |
| security_group_ids | List of security group IDs to attach to the EC2 instance | `list(string)` | n/a | yes |
| instance_type | EC2 instance type | `string` | `"t2.micro"` | no |
| aws_region | AWS region for AMI lookup | `string` | n/a | yes |
| project_name | Project name for resource naming | `string` | n/a | yes |
| environment | Environment name | `string` | n/a | yes |
| ami_id | AMI ID to use (leave empty to use latest Amazon Linux 2) | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| instance_id | ID of the EC2 instance |
| instance_arn | ARN of the EC2 instance |
| private_ip | Private IP address of the EC2 instance |
| private_dns | Private DNS name of the EC2 instance |
| ami_id | AMI ID used for the EC2 instance |
| instance_type | Instance type of the EC2 instance |

## User Data Script

The module includes a user data script that automatically:
1. Updates the system packages
2. Installs Apache HTTP Server (httpd)
3. Starts and enables the httpd service
4. Creates a simple HTML page with instance metadata

## Usage

```hcl
module "compute" {
  source = "./modules/compute"

  subnet_id          = module.networking.private_subnet_id
  security_group_ids = [module.security.web_security_group_id]
  instance_type      = "t2.micro"
  aws_region         = "us-east-1"
  project_name       = "my-project"
  environment        = "dev"
}
```

## AWS Free Tier

- **t2.micro** instances are eligible for AWS Free Tier (750 hours/month for 12 months)
- Ensure you're using a Free Tier eligible instance type to avoid charges
- Free Tier applies to new AWS accounts only

## AMI Selection

- By default, the module uses the latest Amazon Linux 2 AMI
- You can override this by providing a specific `ami_id`
- The module uses a data source to automatically find the latest AMI

## Notes

- Instance is launched in the subnet specified by `subnet_id`
- User data script runs on first boot only
- `user_data_replace_on_change = true` ensures instance is replaced if user_data changes
- Instance metadata is available at http://169.254.169.254/latest/meta-data/

## Accessing the Instance

Since the instance is in a private subnet:
- **With NAT Gateway**: Instance can access the internet for updates, but cannot be directly accessed from the internet
- **Without NAT Gateway**: Instance has no internet access
- To access the instance, you'll need:
  - A bastion host in the public subnet, OR
  - AWS Systems Manager Session Manager, OR
  - VPN/Direct Connect connection

## Cost Considerations

- **t2.micro**: Free Tier eligible (first 750 hours/month for 12 months)
- **t3.micro**: ~$0.0104/hour (~$7.50/month) if Free Tier expired
- Always use `terraform destroy` when done to avoid ongoing charges
