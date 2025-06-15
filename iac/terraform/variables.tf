# Input variables for AWS infrastructure

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "postgres_db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "zodiac_content"
}

variable "postgres_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "zodiac_user"
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
}

variable "instagram_app_id" {
  description = "Instagram App ID"
  type        = string
  sensitive   = true
}

variable "twitter_api_key" {
  description = "Twitter API key"
  type        = string
  sensitive   = true
}

variable "tiktok_client_key" {
  description = "TikTok Client Key"
  type        = string
  sensitive   = true
}

variable "lambda_memory_size" {
  description = "Memory size for Lambda function"
  type        = number
  default     = 512
}

variable "lambda_timeout" {
  description = "Timeout for Lambda function"
  type        = number
  default     = 30
}

variable "ecs_cpu" {
  description = "CPU units for ECS task"
  type        = number
  default     = 256
}

variable "ecs_memory" {
  description = "Memory for ECS task"
  type        = number
  default     = 512
}