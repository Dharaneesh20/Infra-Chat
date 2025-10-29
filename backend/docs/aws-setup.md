# AWS Setup Guide

## Overview
This guide will help you set up and configure AWS resources for your application infrastructure.

## Prerequisites
- AWS Account with appropriate permissions
- AWS CLI installed
- IAM credentials configured

## EC2 Instance Setup

### Step 1: Launch an Instance
1. Navigate to EC2 Dashboard
2. Click "Launch Instance"
3. Choose Amazon Linux 2 AMI
4. Select instance type (t2.micro for testing, t3.medium for production)
5. Configure instance details:
   - Network: Select your VPC
   - Subnet: Choose availability zone
   - Auto-assign Public IP: Enable

### Step 2: Configure Security Groups
Create a security group with the following rules:
- SSH (22): Your IP only
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0
- Custom TCP (8080): 0.0.0.0/0 (for application)

### Step 3: Add Tags
Always tag your resources:
- Name: `my-app-server`
- Environment: `production` or `development`
- Owner: Your team name
- Project: Project identifier

## S3 Bucket Setup

### Creating a Bucket
```bash
aws s3 mb s3://my-app-bucket --region us-east-1
```

### Bucket Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-app-bucket/*"
    }
  ]
}
```

## RDS Database Setup

### Step 1: Create Database
1. Choose RDS service
2. Select PostgreSQL or MySQL
3. Choose production or dev/test template
4. Set DB instance identifier
5. Configure master username and password

### Step 2: Security Configuration
- VPC: Same as your EC2 instances
- Security group: Allow port 5432 (PostgreSQL) or 3306 (MySQL) from EC2 security group
- Public accessibility: No (for production)

## Best Practices

### Security
- Never use root account for daily operations
- Enable MFA for all users
- Use IAM roles for EC2 instances
- Rotate credentials regularly
- Use AWS Secrets Manager for sensitive data

### Cost Optimization
- Use Reserved Instances for predictable workloads
- Enable Auto Scaling
- Set up CloudWatch billing alarms
- Delete unused resources
- Use S3 lifecycle policies

### Monitoring
- Enable CloudWatch monitoring
- Set up SNS notifications
- Configure CloudTrail for audit logs
- Use AWS Config for compliance

## Common Issues

### SSH Connection Refused
- Check security group allows your IP
- Verify key pair is correct
- Ensure instance is running

### S3 Access Denied
- Check bucket policy
- Verify IAM permissions
- Confirm bucket exists in correct region

### RDS Connection Timeout
- Check security group rules
- Verify VPC and subnet configuration
- Ensure RDS instance is available

## Additional Resources
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)
