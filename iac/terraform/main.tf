# Main Terraform configuration for AWS infrastructure
provider "aws" {
  region = "us-east-1"
}

# VPC Configuration
resource "aws_vpc" "zodiac_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "zodiac-vpc"
  }
}

# Subnets
resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.zodiac_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "zodiac-public-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.zodiac_vpc.id

  tags = {
    Name = "zodiac-igw"
  }
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.zodiac_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "zodiac-public-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "public_rta" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Security Group for Lambda
resource "aws_security_group" "lambda_sg" {
  name        = "zodiac-lambda-sg"
  description = "Security group for Zodiac Lambda functions"
  vpc_id      = aws_vpc.zodiac_vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "zodiac-lambda-sg"
  }
}

# ECS Cluster for PostgreSQL
resource "aws_ecs_cluster" "zodiac_ecs" {
  name = "zodiac-ecs-cluster"
}

# ECS Task Definition for PostgreSQL
resource "aws_ecs_task_definition" "postgres" {
  family                   = "zodiac-postgres"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "postgres"
      image     = "postgres:15-alpine"
      essential = true

      portMappings = [
        {
          containerPort = 5432
          hostPort      = 5432
        }
      ]

      environment = [
        {
          name  = "POSTGRES_DB"
          value = "zodiac_content"
        },
        {
          name  = "POSTGRES_USER"
          value = "zodiac_user"
        },
        {
          name  = "POSTGRES_PASSWORD"
          value = var.postgres_password
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.postgres_logs.name
          awslogs-region        = "us-east-1"
          awslogs-stream-prefix = "postgres"
        }
      }
    }
  ])
}

# ECS Service for PostgreSQL
resource "aws_ecs_service" "postgres" {
  name            = "zodiac-postgres-service"
  cluster         = aws_ecs_cluster.zodiac_ecs.id
  task_definition = aws_ecs_task_definition.postgres.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = [aws_subnet.public_subnet.id]
    security_groups = [aws_security_group.lambda_sg.id]
    assign_public_ip = true
  }
}

# Lambda Function for API
resource "aws_lambda_function" "zodiac_api" {
  function_name = "zodiac-api"
  handler       = "src.main.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = "zodiac-api.zip"

  environment {
    variables = {
      DATABASE_URL = "postgresql://${var.postgres_user}:${var.postgres_password}@${aws_ecs_service.postgres.name}:5432/zodiac_content"
    }
  }

  vpc_config {
    subnet_ids         = [aws_subnet.public_subnet.id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  tags = {
    Name = "zodiac-api"
  }
}

# API Gateway
resource "aws_api_gateway_rest_api" "zodiac_api" {
  name        = "zodiac-api"
  description = "API Gateway for Zodiac AI Content System"
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "zodiac_api" {
  rest_api_id = aws_api_gateway_rest_api.zodiac_api.id
  stage_name  = "prod"
}

# IAM Roles and Policies
resource "aws_iam_role" "lambda_exec" {
  name = "zodiac-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "zodiac-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# S3 Bucket for Lambda Code
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "zodiac-lambda-code"
  acl    = "private"
}

# CloudWatch Logs
resource "aws_cloudwatch_log_group" "postgres_logs" {
  name = "/ecs/zodiac-postgres"
}

# Secrets Manager for API Keys
resource "aws_secretsmanager_secret" "zodiac_secrets" {
  name = "zodiac-secrets"
}

resource "aws_secretsmanager_secret_version" "zodiac_secrets" {
  secret_id = aws_secretsmanager_secret.zodiac_secrets.id
  secret_string = jsonencode({
    openai_api_key      = var.openai_api_key
    instagram_app_id    = var.instagram_app_id
    twitter_api_key     = var.twitter_api_key
    tiktok_client_key   = var.tiktok_client_key
    postgres_password   = var.postgres_password
  })
}

# Variables
variable "openai_api_key" {
  type = string
}

variable "instagram_app_id" {
  type = string
}

variable "twitter_api_key" {
  type = string
}

variable "tiktok_client_key" {
  type = string
}

variable "postgres_user" {
  type    = string
  default = "zodiac_user"
}

variable "postgres_password" {
  type = string
}

# Outputs
output "api_gateway_url" {
  value = aws_api_gateway_deployment.zodiac_api.invoke_url
}

output "postgres_endpoint" {
  value = aws_ecs_service.postgres.name
}

output "lambda_function_name" {
  value = aws_lambda_function.zodiac_api.function_name
}