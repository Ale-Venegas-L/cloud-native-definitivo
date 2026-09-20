variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "Amazon Linux 2023 AMI ID"
  type        = string
  default     = "ami-09179a962fadf762b"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "classic-library"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "ssh_public_key" {
  description = "SSH public key for EC2 access"
  type        = string
}

variable "callback_urls" {
  description = "OAuth callback URLs for Cognito"
  type        = list(string)
  default     = ["http://localhost:5173/callback"]
}

variable "logout_urls" {
  description = "OAuth logout URLs for Cognito"
  type        = list(string)
  default     = ["http://localhost:5173/"]
}

variable "admin_email" {
  description = "Admin user email for Cognito"
  type        = string
  default     = "admin@example.com"
}

variable "admin_temp_password" {
  description = "Admin user temporary password"
  type        = string
  default     = "Admin123!"
  sensitive   = true
}
