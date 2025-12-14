#!/usr/bin/env python3
"""
Face Recognition Attendance System - Python Deployment Script
Automates deployment of AWS resources
Prerequisites: boto3 installed (pip install boto3) and AWS credentials configured
"""

import boto3
import json
import sys
import time
from datetime import datetime
import os

# Configuration
REGION = 'us-east-1'
BUCKET_PREFIX = 'attendance-images'
FRONTEND_BUCKET_PREFIX = 'attendance-frontend'

def get_account_id():
    """Get AWS Account ID"""
    sts = boto3.client('sts')
    return sts.get_caller_identity()['Account']

def create_s3_buckets(s3_client, account_id):
    """Create S3 buckets for images and frontend"""
    timestamp = int(time.time())
    image_bucket = f"{BUCKET_PREFIX}-{timestamp}"
    frontend_bucket = f"{FRONTEND_BUCKET_PREFIX}-{timestamp}"
    
    print(f"[*] Creating S3 buckets...")
    
    # Create image bucket
    if REGION == 'us-east-1':
        s3_client.create_bucket(Bucket=image_bucket)
    else:
        s3_client.create_bucket(
            Bucket=image_bucket,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
    print(f"[OK] Created bucket: {image_bucket}")
    
    # Create frontend bucket
    if REGION == 'us-east-1':
        s3_client.create_bucket(Bucket=frontend_bucket)
    else:
        s3_client.create_bucket(
            Bucket=frontend_bucket,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
    print(f"[OK] Created bucket: {frontend_bucket}")
    
    # Enable static website hosting for frontend
    s3_client.put_bucket_website(
        Bucket=frontend_bucket,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'index.html'}
        }
    )
    
    # Try to make frontend bucket public (for demo only)
    # Note: This may fail if Block Public Access is enabled
    try:
        # First, disable Block Public Access settings
        s3_client.put_public_access_block(
            Bucket=frontend_bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        
        # Then apply bucket policy
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{frontend_bucket}/*"
            }]
        }
        s3_client.put_bucket_policy(
            Bucket=frontend_bucket,
            Policy=json.dumps(bucket_policy)
        )
        print(f"[OK] Made frontend bucket public")
    except Exception as e:
        print(f"[WARNING] Could not make bucket public: {str(e)}")
        print(f"         You may need to configure this manually in S3 Console")
    
    return image_bucket, frontend_bucket

def create_dynamodb_tables(dynamodb_client):
    """Create DynamoDB tables"""
    print(f"[*] Creating DynamoDB tables...")
    
    # Create Students table
    try:
        dynamodb_client.create_table(
            TableName='Students',
            AttributeDefinitions=[
                {'AttributeName': 'FaceId', 'AttributeType': 'S'},
                {'AttributeName': 'StudentId', 'AttributeType': 'S'}
            ],
            KeySchema=[
                {'AttributeName': 'FaceId', 'KeyType': 'HASH'}
            ],
            BillingMode='PAY_PER_REQUEST',
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'StudentId-index',
                    'KeySchema': [
                        {'AttributeName': 'StudentId', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ]
        )
        print("[OK] Created table: Students")
        wait_for_table(dynamodb_client, 'Students')
    except dynamodb_client.exceptions.ResourceInUseException:
        print("[INFO] Table 'Students' already exists")
    
    # Create AttendanceRecords table
    try:
        dynamodb_client.create_table(
            TableName='AttendanceRecords',
            AttributeDefinitions=[
                {'AttributeName': 'AttendanceId', 'AttributeType': 'S'},
                {'AttributeName': 'Date', 'AttributeType': 'S'},
                {'AttributeName': 'StudentId', 'AttributeType': 'S'}
            ],
            KeySchema=[
                {'AttributeName': 'AttendanceId', 'KeyType': 'HASH'}
            ],
            BillingMode='PAY_PER_REQUEST',
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'Date-index',
                    'KeySchema': [
                        {'AttributeName': 'Date', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                },
                {
                    'IndexName': 'StudentId-Date-index',
                    'KeySchema': [
                        {'AttributeName': 'StudentId', 'KeyType': 'HASH'},
                        {'AttributeName': 'Date', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ]
        )
        print("[OK] Created table: AttendanceRecords")
        wait_for_table(dynamodb_client, 'AttendanceRecords')
    except dynamodb_client.exceptions.ResourceInUseException:
        print("[INFO] Table 'AttendanceRecords' already exists")

def wait_for_table(dynamodb_client, table_name):
    """Wait for DynamoDB table to become active"""
    waiter = dynamodb_client.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    print(f"   Table '{table_name}' is now active")

def create_rekognition_collection(rekognition_client):
    """Create Rekognition face collection"""
    print(f"[*] Creating Rekognition collection...")
    try:
        rekognition_client.create_collection(CollectionId='attendance-students')
        print("[OK] Created collection: attendance-students")
    except rekognition_client.exceptions.ResourceAlreadyExistsException:
        print("[INFO] Collection 'attendance-students' already exists")

def create_sns_topic(sns_client):
    """Create SNS topic"""
    print(f"[*] Creating SNS topic...")
    response = sns_client.create_topic(Name='attendance-notifications')
    topic_arn = response['TopicArn']
    print(f"[OK] Created SNS topic: {topic_arn}")
    return topic_arn

def deploy_frontend(s3_client, frontend_bucket):
    """Deploy frontend files to S3"""
    print(f"[*] Deploying frontend...")
    
    frontend_dir = 'frontend'
    if not os.path.exists(frontend_dir):
        print(f"[ERROR] Error: {frontend_dir} directory not found")
        return
    
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key = os.path.relpath(local_path, frontend_dir).replace('\\', '/')
            
            # Determine content type
            content_type = 'text/html'
            if file.endswith('.css'):
                content_type = 'text/css'
            elif file.endswith('.js'):
                content_type = 'application/javascript'
            
            s3_client.upload_file(
                local_path,
                frontend_bucket,
                s3_key,
                ExtraArgs={'ContentType': content_type}
            )
            print(f"   Uploaded: {s3_key}")
    
    frontend_url = f"http://{frontend_bucket}.s3-website-{REGION}.amazonaws.com"
    print(f"[OK] Frontend deployed to: {frontend_url}")
    return frontend_url

def main():
    """Main deployment function"""
    print("=" * 60)
    print("Starting deployment of Face Recognition Attendance System...")
    print("=" * 60)
    print()
    
    try:
        # Initialize AWS clients
        s3_client = boto3.client('s3', region_name=REGION)
        dynamodb_client = boto3.client('dynamodb', region_name=REGION)
        rekognition_client = boto3.client('rekognition', region_name=REGION)
        sns_client = boto3.client('sns', region_name=REGION)
        
        # Get account ID
        account_id = get_account_id()
        print(f"Using Region: {REGION}")
        print(f"Using Account ID: {account_id}")
        print()
        
        # Deploy resources
        image_bucket, frontend_bucket = create_s3_buckets(s3_client, account_id)
        print()
        
        create_dynamodb_tables(dynamodb_client)
        print()
        
        create_rekognition_collection(rekognition_client)
        print()
        
        sns_topic_arn = create_sns_topic(sns_client)
        print()
        
        frontend_url = deploy_frontend(s3_client, frontend_bucket)
        print()
        
        # Print summary
        print("=" * 60)
        print("DEPLOYMENT SUMMARY")
        print("=" * 60)
        print(f"Region: {REGION}")
        print(f"Account ID: {account_id}")
        print(f"S3 Bucket (Images): {image_bucket}")
        print(f"S3 Bucket (Frontend): {frontend_bucket}")
        print(f"Frontend URL: {frontend_url}")
        print(f"SNS Topic ARN: {sns_topic_arn}")
        print()
        print("\nNEXT STEPS:")
        print("1. Create IAM role 'LambdaAttendanceRole' with proper permissions")
        print("2. Update Lambda function constants:")
        print(f"   - S3_BUCKET: {image_bucket}")
        print(f"   - SNS_TOPIC_ARN: {sns_topic_arn}")
        print(f"   - REGION: {REGION}")
        print(f"   - ACCOUNT_ID: {account_id}")
        print("3. Deploy Lambda functions via AWS Console or SAM")
        print("4. Create API Gateway and connect to Lambda functions")
        print("5. Update frontend/script.js with API Gateway endpoint")
        print("6. Test the system!")
        print()
        print("[OK] Infrastructure deployment complete!")
        
    except Exception as e:
        print(f"[ERROR] Error during deployment: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()

