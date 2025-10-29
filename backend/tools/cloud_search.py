"""
Cloud Search Tool
Provides read-only access to AWS infrastructure using Boto3
"""

import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import json

# Initialize AWS clients (with error handling)
try:
    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    
    AWS_CONFIGURED = True
except (NoCredentialsError, Exception) as e:
    print(f"⚠️  AWS not configured: {e}")
    AWS_CONFIGURED = False


def search_aws_resources(query: str) -> str:
    """
    Query AWS resources based on user input
    
    Args:
        query: Natural language query about AWS resources
        
    Returns:
        Formatted information about AWS resources
    """
    if not AWS_CONFIGURED:
        return """
        AWS integration is not configured. To enable:
        1. Add AWS credentials to your .env file
        2. Use read-only IAM credentials for security
        
        Note: This is optional - the bot works without AWS integration!
        """
    
    query_lower = query.lower()
    
    try:
        # EC2 Instances
        if 'ec2' in query_lower or 'instance' in query_lower or 'server' in query_lower:
            return get_ec2_instances(query_lower)
        
        # S3 Buckets
        elif 's3' in query_lower or 'bucket' in query_lower:
            return get_s3_buckets()
        
        # Default response
        else:
            return """
            I can help you query the following AWS resources:
            - EC2 instances (e.g., "list EC2 instances" or "show prod servers")
            - S3 buckets (e.g., "list S3 buckets")
            
            What would you like to know?
            """
    
    except Exception as e:
        return f"Error querying AWS: {str(e)}"


def get_ec2_instances(query: str) -> str:
    """Get EC2 instance information"""
    try:
        response = ec2_client.describe_instances()
        
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                # Extract relevant info
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                state = instance['State']['Name']
                
                # Get tags
                tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                name = tags.get('Name', 'N/A')
                env = tags.get('Environment', 'N/A')
                
                # Filter by query if needed
                if 'prod' in query and env.lower() != 'prod':
                    continue
                
                instances.append({
                    'id': instance_id,
                    'name': name,
                    'type': instance_type,
                    'state': state,
                    'environment': env
                })
        
        if not instances:
            return "No EC2 instances found matching your criteria."
        
        # Format output
        result = f"Found {len(instances)} EC2 instance(s):\n\n"
        for inst in instances:
            result += f"• {inst['name']} ({inst['id']})\n"
            result += f"  Type: {inst['type']}\n"
            result += f"  State: {inst['state']}\n"
            result += f"  Environment: {inst['environment']}\n\n"
        
        print(f"☁️  CloudSearch found {len(instances)} EC2 instances")
        return result
    
    except ClientError as e:
        return f"AWS API Error: {e.response['Error']['Message']}"


def get_s3_buckets() -> str:
    """Get S3 bucket information"""
    try:
        response = s3_client.list_buckets()
        buckets = response['Buckets']
        
        if not buckets:
            return "No S3 buckets found in your account."
        
        result = f"Found {len(buckets)} S3 bucket(s):\n\n"
        for bucket in buckets:
            result += f"• {bucket['Name']}\n"
            result += f"  Created: {bucket['CreationDate'].strftime('%Y-%m-%d')}\n\n"
        
        print(f"☁️  CloudSearch found {len(buckets)} S3 buckets")
        return result
    
    except ClientError as e:
        return f"AWS API Error: {e.response['Error']['Message']}"


# Test function
if __name__ == "__main__":
    print("Testing AWS integration...\n")
    result = search_aws_resources("list ec2 instances")
    print(result)
