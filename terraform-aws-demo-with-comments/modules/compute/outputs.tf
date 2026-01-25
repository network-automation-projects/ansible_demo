output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "instance_arn" {
  description = "ARN of the EC2 instance"
  value       = aws_instance.web.arn
}

output "private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.web.private_ip
}

output "private_dns" {
  description = "Private DNS name of the EC2 instance"
  value       = aws_instance.web.private_dns
}

output "ami_id" {
  description = "AMI ID used for the EC2 instance"
  value       = aws_instance.web.ami
}

output "instance_type" {
  description = "Instance type of the EC2 instance"
  value       = aws_instance.web.instance_type
}
