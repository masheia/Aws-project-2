#!/usr/bin/env python3
"""
Setup AWS Cognito for User Authentication
Creates User Pool with Student and Admin groups
"""

import boto3
import json

REGION = 'us-east-1'
USER_POOL_NAME = 'FaceRecognitionAttendanceUsers'
CLIENT_NAME = 'AttendanceWebClient'

cognito = boto3.client('cognito-idp', region_name=REGION)

def create_user_pool():
    """Create Cognito User Pool"""
    print(f"[*] Creating Cognito User Pool: {USER_POOL_NAME}...")
    
    try:
        response = cognito.create_user_pool(
            PoolName=USER_POOL_NAME,
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': False
                }
            },
            AutoVerifiedAttributes=['email'],
            Schema=[
                {
                    'Name': 'email',
                    'AttributeDataType': 'String',
                    'Required': True,
                    'Mutable': True
                },
                {
                    'Name': 'custom:role',
                    'AttributeDataType': 'String',
                    'Required': False,
                    'Mutable': True
                }
            ],
            MfaConfiguration='OFF'
        )
        user_pool_id = response['UserPool']['Id']
        print(f"[OK] Created User Pool: {user_pool_id}")
        return user_pool_id
        
    except cognito.exceptions.InvalidParameterException as e:
        if 'already exists' in str(e).lower():
            # Find existing pool
            pools = cognito.list_user_pools(MaxResults=60)
            for pool in pools['UserPools']:
                if pool['Name'] == USER_POOL_NAME:
                    user_pool_id = pool['Id']
                    print(f"[INFO] User Pool already exists: {user_pool_id}")
                    return user_pool_id
        raise

def create_user_pool_client(user_pool_id):
    """Create User Pool Client for web app"""
    print(f"[*] Creating User Pool Client...")
    
    try:
        response = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=CLIENT_NAME,
            GenerateSecret=False,  # For web apps
            ExplicitAuthFlows=[
                'ALLOW_USER_PASSWORD_AUTH',
                'ALLOW_REFRESH_TOKEN_AUTH',
                'ALLOW_USER_SRP_AUTH'
            ],
            SupportedIdentityProviders=['COGNITO'],
            CallbackURLs=['http://localhost:8000'],
            LogoutURLs=['http://localhost:8000'],
            AllowedOAuthFlows=['code'],
            AllowedOAuthScopes=['email', 'openid', 'profile'],
            AllowedOAuthFlowsUserPoolClient=True
        )
        client_id = response['UserPoolClient']['ClientId']
        print(f"[OK] Created Client: {client_id}")
        return client_id
        
    except cognito.exceptions.InvalidParameterException as e:
        if 'already exists' in str(e).lower():
            clients = cognito.list_user_pool_clients(UserPoolId=user_pool_id)
            for client in clients['UserPoolClients']:
                if client['ClientName'] == CLIENT_NAME:
                    client_id = client['ClientId']
                    print(f"[INFO] Client already exists: {client_id}")
                    return client_id
        raise

def create_user_groups(user_pool_id):
    """Create Student and Admin groups"""
    groups = [
        {'Name': 'Students', 'Description': 'Student users - can view own attendance'},
        {'Name': 'Admins', 'Description': 'Admin users - full access'}
    ]
    
    for group in groups:
        try:
            cognito.create_group(
                UserPoolId=user_pool_id,
                GroupName=group['Name'],
                Description=group['Description']
            )
            print(f"[OK] Created group: {group['Name']}")
        except cognito.exceptions.GroupExistsException:
            print(f"[INFO] Group already exists: {group['Name']}")

def main():
    print("=" * 60)
    print("Setting Up AWS Cognito for User Authentication")
    print("=" * 60)
    print()
    
    try:
        user_pool_id = create_user_pool()
        print()
        
        client_id = create_user_pool_client(user_pool_id)
        print()
        
        create_user_groups(user_pool_id)
        print()
        
        print("=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"User Pool ID: {user_pool_id}")
        print(f"Client ID: {client_id}")
        print()
        print("Next Steps:")
        print("1. Update frontend/script.js with these IDs")
        print("2. Add login/registration UI")
        print("3. Update Lambda functions to check user roles")
        print()
        print("Save these values:")
        print(f"USER_POOL_ID={user_pool_id}")
        print(f"CLIENT_ID={client_id}")
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")

if __name__ == '__main__':
    main()

