output "vpc_id" {
  description = "ID del VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs de las subnets publicas"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs de las subnets privadas"
  value       = aws_subnet.private[*].id
}

output "mongodb_instance_id" {
  description = "ID de la instancia EC2 de MongoDB"
  value       = aws_instance.mongodb.id
}

output "mongodb_private_ip" {
  description = "IP privada de MongoDB"
  value       = aws_instance.mongodb.private_ip
}

output "alb_dns_name" {
  description = "DNS del Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "ecs_cluster_name" {
  description = "Nombre del ECS Cluster"
  value       = aws_ecs_cluster.main.name
}
