# Output values for AWS infrastructure

output "api_gateway_url" {
  description = "URL for API Gateway endpoint"
  value       = aws_api_gateway_deployment.zodiac_api.invoke_url
}

output "postgres_endpoint" {
  description = "Endpoint for PostgreSQL database"
  value       = aws_ecs_service.postgres.name
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.zodiac_api.function_name
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket for Lambda code"
  value       = aws_s3_bucket.lambda_bucket.bucket
}

output "secrets_manager_arn" {
  description = "ARN for Secrets Manager"
  value       = aws_secretsmanager_secret.zodiac_secrets.arn
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.zodiac_vpc.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public_subnet.id
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.zodiac_ecs.name
}