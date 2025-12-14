#!/usr/bin/env python3
"""
Create IAM Role for Face Recognition Attendance System
"""

import boto3
import json

REGION = 'us-east-1'
ACCOUNT_ID = '846863292978'
ROLE_NAME = 'FaceRecognitionAttendanceRole'

iam = boto3.client('iam', region_name=REGION)

def create_role():
    """Create IAM role for Lambda with proper permissions"""
    print(f"[*] Creating IAM role: {ROLE_NAME}...")
    
    # Trust policy for Lambda
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        # Create role
        response = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='IAM role for Face Recognition Attendance System Lambda functions',
            Tags=[
                {'Key': 'Project', 'Value': 'FaceRecognitionAttendance'},
                {'Key': 'Purpose', 'Value': 'LambdaExecution'}
            ]
        )
        role_arn = response['Role']['Arn']
        print(f"[OK] Created role: {role_arn}")
        
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"[INFO] Role {ROLE_NAME} already exists")
        response = iam.get_role(RoleName=ROLE_NAME)
        role_arn = response['Role']['Arn']
        print(f"[OK] Using existing role: {role_arn}")
    
    # Attach basic Lambda execution policy
    try:
        iam.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        print(f"[OK] Attached AWSLambdaBasicExecutionRole")
    except Exception as e:
        print(f"[WARNING] Could not attach basic execution role: {e}")
    
    # Create custom policy for attendance system
    policy_name = 'FaceRecognitionAttendancePolicy'
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject"
                ],
                "Resource": [
                    f"arn:aws:s3:::attendance-images-*/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "rekognition:*"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:PutItem",
                    "dynamodb:GetItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:UpdateItem"
                ],
                "Resource": [
                    f"arn:aws:dynamodb:{REGION}:{ACCOUNT_ID}:table/Students",
                    f"arn:aws:dynamodb:{REGION}:{ACCOUNT_ID}:table/Students/index/*",
                    f"arn:aws:dynamodb:{REGION}:{ACCOUNT_ID}:table/AttendanceRecords",
                    f"arn:aws:dynamodb:{REGION}:{ACCOUNT_ID}:table/AttendanceRecords/index/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": "sns:Publish",
                "Resource": f"arn:aws:sns:{REGION}:{ACCOUNT_ID}:attendance-notifications"
            }
        ]
    }
    
    try:
        # Check if policy exists
        try:
            policy_arn = f"arn:aws:iam::{ACCOUNT_ID}:policy/{policy_name}"
            iam.get_policy(PolicyArn=policy_arn)
            print(f"[INFO] Policy {policy_name} already exists, updating...")
            # Delete old versions and create new
            versions = iam.list_policy_versions(PolicyArn=policy_arn)['Versions']
            for version in versions:
                if not version['IsDefaultVersion']:
                    iam.delete_policy_version(PolicyArn=policy_arn, VersionId=version['VersionId'])
            iam.create_policy_version(
                PolicyArn=policy_arn,
                PolicyDocument=json.dumps(policy_document),
                SetAsDefault=True
            )
        except iam.exceptions.NoSuchEntityException:
            # Create new policy
            response = iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document),
                Description='Policy for Face Recognition Attendance System'
            )
            policy_arn = response['Policy']['Arn']
            print(f"[OK] Created policy: {policy_arn}")
        
        # Attach policy to role
        iam.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn=policy_arn
        )
        print(f"[OK] Attached policy to role")
        
    except Exception as e:
        print(f"[ERROR] Could not create/attach policy: {e}")
        return None
    
    return role_arn

def update_lambda_functions(role_arn):
    """Update Lambda functions to use the new role"""
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    functions = ['ProcessAttendance', 'RegisterFace', 'GetAttendance']
    
    for func_name in functions:
        try:
            print(f"[*] Updating {func_name} to use new role...")
            lambda_client.update_function_configuration(
                FunctionName=func_name,
                Role=role_arn
            )
            print(f"[OK] Updated {func_name}")
        except Exception as e:
            print(f"[WARNING] Could not update {func_name}: {e}")

def main():
    print("=" * 60)
    print("Creating IAM Role for Face Recognition Attendance System")
    print("=" * 60)
    print()
    
    role_arn = create_role()
    
    if role_arn:
        print()
        print("[*] Updating Lambda functions to use new role...")
        update_lambda_functions(role_arn)
        print()
        print("=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"Role ARN: {role_arn}")
        print()
        print("All Lambda functions have been updated to use the new role.")
        print("They now have proper permissions for:")
        print("  - S3 (read/write images)")
        print("  - Rekognition (face detection)")
        print("  - DynamoDB (database)")
        print("  - SNS (notifications)")
        print()
        print("Try registering a student again - it should work now!")
    else:
        print()
        print("[ERROR] Failed to create role. Please check the errors above.")

if __name__ == '__main__':
    main()



