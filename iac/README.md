# Infrastructure as Code (IaC) Documentation

This directory contains Terraform configurations for deploying the Zodiac AI Content System on AWS.

## 🏗️ Architecture Overview

The system is deployed using the following AWS services:

- **AWS Lambda**: Hosts the backend API
- **Amazon ECS**: Runs PostgreSQL in a container
- **API Gateway**: Provides REST API endpoints
- **Secrets Manager**: Stores sensitive credentials
- **VPC**: Network isolation and security
- **S3**: Stores Lambda deployment packages
- **CloudWatch**: Logging and monitoring

## 📂 Directory Structure

```
iac/
├── terraform/
│   ├── main.tf         # Main Terraform configuration
│   ├── variables.tf    # Input variables
│   ├── outputs.tf      # Output values
│   └── versions.tf     # Terraform and provider versions
└── README.md           # This documentation
```

## 🚀 Deployment Steps

1. **Install Terraform**
   ```bash
   brew install terraform
   ```

2. **Initialize Terraform**
   ```bash
   cd iac/terraform
   terraform init
   ```

3. **Set up AWS credentials**
   ```bash
   export AWS_ACCESS_KEY_ID="your-access-key"
   export AWS_SECRET_ACCESS_KEY="your-secret-key"
   ```

4. **Apply the configuration**
   ```bash
   terraform apply
   ```

5. **Provide required variables**
   ```bash
   var.openai_api_key
   var.instagram_app_id
   var.twitter_api_key
   var.tiktok_client_key
   var.postgres_password
   ```

## 🔒 Secrets Management

All sensitive credentials are stored in AWS Secrets Manager. The following secrets are required:

- OpenAI API Key
- Instagram App ID
- Twitter API Key
- TikTok Client Key
- PostgreSQL Password

## 💻 Local Development

For local development, you can use the following commands:

```bash
# Format Terraform code
terraform fmt

# Validate configuration
terraform validate

# Plan changes
terraform plan

# Apply changes
terraform apply

# Destroy resources
terraform destroy
```

## 📊 Outputs

After deployment, the following outputs will be available:

- API Gateway URL
- PostgreSQL Endpoint
- Lambda Function Name
- S3 Bucket Name
- Secrets Manager ARN
- VPC ID
- Public Subnet ID
- ECS Cluster Name

## 🛠️ Maintenance

### Updating Infrastructure
1. Make changes to Terraform files
2. Run `terraform plan` to preview changes
3. Apply changes with `terraform apply`

### Monitoring
- Use CloudWatch for logs and metrics
- Set up alarms for critical resources
- Monitor API Gateway usage and errors

### Scaling
- Adjust Lambda memory and timeout as needed
- Scale ECS tasks based on database load
- Use API Gateway caching for improved performance

## 🚨 Troubleshooting

### Common Issues
- **Authentication Errors**: Verify AWS credentials
- **Resource Limits**: Check AWS service quotas
- **Deployment Failures**: Review CloudWatch logs
- **Connectivity Issues**: Verify VPC and security group settings

### Useful Commands
```bash
# Show current state
terraform show

# Import existing resources
terraform import

# Refresh state
terraform refresh

# List resources
terraform state list
```

## 📚 Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Best Practices](https://aws.amazon.com/architecture/well-architected/)