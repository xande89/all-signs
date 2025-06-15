# Zodiac AI Content System - Setup Guide

## 🚀 Getting Started

### Prerequisites

1. **AWS Account**: Create an AWS account if you don't have one
2. **Terraform**: Install Terraform (version >= 1.0.0)
3. **AWS CLI**: Install and configure AWS CLI
4. **Git**: Install Git for version control
5. **Python**: Install Python 3.11

### Step 1: Clone the Repository

```bash
git clone https://github.com/xande89/all-signs.git
cd all-signs
```

### Step 2: Set Up AWS Credentials

1. Create an IAM user with the following permissions:
   - AmazonECS_FullAccess
   - AmazonLambda_FullAccess
   - AmazonAPIGateway_Administrator
   - AmazonS3_FullAccess
   - SecretsManager_ReadWrite
   - AmazonVPC_FullAccess
   - CloudWatchLogs_FullAccess

2. Configure AWS CLI:
   ```bash
   aws configure
   ```

### Step 3: Initialize Terraform

```bash
cd iac/terraform
terraform init
```

### Step 4: Gather Required API Keys

You'll need the following API keys:

1. **OpenAI API Key**: Get from OpenAI platform
2. **Instagram App ID**: Create Facebook Developer account
3. **Twitter API Key**: Create Twitter Developer account
4. **TikTok Client Key**: Create TikTok Developer account
5. **PostgreSQL Password**: Choose a secure password

### Step 5: Deploy Infrastructure

```bash
terraform apply
```

When prompted, provide the required variables:
```bash
var.openai_api_key = "your_openai_key"
var.instagram_app_id = "your_instagram_app_id"
var.twitter_api_key = "your_twitter_api_key"
var.tiktok_client_key = "your_tiktok_client_key"
var.postgres_password = "your_secure_password"
```

### Step 6: Verify Deployment

After deployment completes, you'll receive output values including:
- API Gateway URL
- PostgreSQL Endpoint
- Lambda Function Name
- S3 Bucket Name

### Step 7: Deploy Application Code

1. Package the Lambda function:
   ```bash
   zip -r lambda.zip src/
   ```

2. Upload to S3:
   ```bash
   aws s3 cp lambda.zip s3://your-bucket-name/
   ```

3. Update Lambda function:
   ```bash
   aws lambda update-function-code \
     --function-name zodiac-api \
     --s3-bucket your-bucket-name \
     --s3-key lambda.zip
   ```

### Step 8: Test the System

1. Access the API Gateway URL
2. Use the API documentation at `/docs` endpoint
3. Test content generation endpoints

## 🔒 Security Best Practices

1. **IAM Roles**: Use least privilege principle
2. **Secrets Manager**: Store all sensitive credentials
3. **VPC**: Use private subnets for database
4. **Monitoring**: Set up CloudWatch alarms
5. **Backups**: Enable RDS snapshots

## 📈 Scaling the System

### Horizontal Scaling
- Increase Lambda concurrency
- Add ECS tasks for PostgreSQL
- Use API Gateway caching

### Vertical Scaling
- Increase Lambda memory
- Use larger ECS instance types
- Enable RDS read replicas

## 🛠️ Maintenance

### Regular Tasks
- Monitor CloudWatch metrics
- Review security groups
- Rotate API keys periodically
- Update Lambda function code

### Updating Infrastructure
1. Modify Terraform files
2. Run `terraform plan`
3. Apply changes with `terraform apply`

## 🚨 Troubleshooting

### Common Issues
- **Authentication Errors**: Verify IAM permissions
- **Resource Limits**: Check AWS service quotas
- **Connectivity Issues**: Verify VPC settings
- **Deployment Failures**: Check CloudWatch logs

### Useful Commands
```bash
# View Lambda logs
aws logs tail /aws/lambda/zodiac-api

# Check ECS task status
aws ecs describe-tasks --cluster zodiac-ecs-cluster

# Test API endpoints
curl -X POST https://your-api-url/api/content/generate
```

## 📚 Additional Resources

- [AWS Documentation](https://aws.amazon.com/documentation/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Instagram API Documentation](https://developers.facebook.com/docs/instagram-api)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [TikTok API Documentation](https://developers.tiktok.com/doc/)

## 📞 Support

For assistance, contact:
- Email: support@zodiac-ai-content.com
- GitHub Issues: https://github.com/xande89/all-signs/issues
- Documentation: https://github.com/xande89/all-signs/docs