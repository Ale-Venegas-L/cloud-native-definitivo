output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.app.public_ip
}

output "public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = aws_instance.app.public_dns
}

output "ssh_command" {
  description = "SSH command to connect"
  value       = "ssh -i ~/.ssh/${var.project_name}-key ec2-user@${aws_instance.app.public_ip}"
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = var.enable_cognito ? aws_cognito_user_pool.main[0].id : "not-created"
}

output "cognito_app_client_id" {
  description = "Cognito App Client ID"
  value       = var.enable_cognito ? aws_cognito_user_pool_client.main[0].id : "not-created"
}

output "cognito_domain" {
  description = "Cognito hosted UI domain"
  value       = var.enable_cognito ? "${aws_cognito_user_pool_domain.main[0].domain}.auth.${var.aws_region}.amazoncognito.com" : "not-created"
}

output "api_gateway_url" {
  description = "API Gateway invoke URL (prod)"
  value       = aws_api_gateway_stage.prod.invoke_url
}

output "api_gateway_url_dev" {
  description = "API Gateway invoke URL (dev)"
  value       = aws_api_gateway_stage.dev.invoke_url
}
