# Data source to get the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

locals {
  # Use provided AMI ID or fall back to latest Amazon Linux 2
  ami_id = var.ami_id != "" ? var.ami_id : data.aws_ami.amazon_linux.id

  common_tags = {
    Module = "compute"
  }

  # User data script to install and start Apache web server
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    echo "<h1>Hello from Terraform AWS Demo</h1>" > /var/www/html/index.html
    echo "<p>Instance ID: $(curl -s http://169.254.169.254/latest/meta-data/instance-id)</p>" >> /var/www/html/index.html
    echo "<p>Availability Zone: $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)</p>" >> /var/www/html/index.html
  EOF
}

# EC2 Instance - Web server in private subnet
resource "aws_instance" "web" {
  ami                    = local.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.security_group_ids

  user_data = local.user_data

  # Ensure instance is replaced if user_data changes
  user_data_replace_on_change = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-web-server"
    }
  )
}
