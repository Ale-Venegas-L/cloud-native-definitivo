variable "aws_region" {
  description = "Region de AWS"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "classic-library"
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t2.micro"
}

variable "mongodb_port" {
  description = "Puerto de MongoDB"
  type        = number
  default     = 27017
}

variable "backend_port" {
  description = "Puerto del backend"
  type        = number
  default     = 8000
}

variable "frontend_port" {
  description = "Puerto del frontend"
  type        = number
  default     = 80
}
