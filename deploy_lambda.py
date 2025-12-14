#!/usr/bin/env python3
"""
Deploy Lambda Functions and Create API Gateway
"""

import boto3
import json
import zipfile
import os
import shutil
import time

REGION = 'us-east-1'
# IAM_ROLE_NAME will be detected automatically or set it here
IAM_ROLE_NAME = None

# Get IAM role ARN
iam = boto3.client('iam', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)
apigateway = boto3.client('apigateway', region_name=REGION)

def get_role_arn():
    """Get IAM role ARN for Lambda"""
    global IAM_ROLE_NAME
    
    if IAM_ROLE_NAME:
        try:
            response = iam.get_role(RoleName=IAM_ROLE_NAME)
            return response['Role']['Arn']
        except Exception as e:
            print(f"[ERROR] Could not find IAM role '{IAM_ROLE_NAME}': {e}")
    
    # Try to find a suitable role
    print("[*] Searching for Lambda execution role...")
    try:
        roles_response = iam.list_roles()
        # Look for roles with 'lambda' or 'attendance' in name, or roles with Lambda execution policy
        for role in roles_response['Roles']:
            role_name = role['RoleName'].lower()
            if 'lambda' in role_name or 'attendance' in role_name:
                IAM_ROLE_NAME = role['RoleName']
                print(f"[OK] Found role: {IAM_ROLE_NAME}")
                return role['Arn']
        
        # If not found, try to find any role with AWSLambdaBasicExecutionRole attached
        for role in roles_response['Roles']:
            try:
                policies = iam.list_attached_role_policies(RoleName=role['RoleName'])
                for policy in policies['AttachedPolicies']:
                    if 'Lambda' in policy['PolicyName']:
                        IAM_ROLE_NAME = role['RoleName']
                        print(f"[OK] Found role with Lambda policy: {IAM_ROLE_NAME}")
                        return role['Arn']
            except:
                continue
        
        print("[ERROR] Could not find suitable IAM role")
        print("Please specify IAM_ROLE_NAME in deploy_lambda.py or create a role")
        return None
    except Exception as e:
        print(f"[ERROR] Error searching for roles: {e}")
        return None

def create_zip_package(function_dir, zip_name):
    """Create ZIP package for Lambda function"""
    print(f"[*] Creating package for {function_dir}...")
    
    # Create temporary directory for packaging
    temp_dir = f"temp_{function_dir.replace('/', '_')}"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Copy function code
    shutil.copy(f"lambda-functions/{function_dir}/lambda_function.py", temp_dir)
    
    # Install dependencies if requirements.txt exists
    req_file = f"lambda-functions/{function_dir}/requirements.txt"
    if os.path.exists(req_file):
        print(f"   Installing dependencies...")
        os.system(f"python -m pip install -r {req_file} -t {temp_dir} --quiet")
    
    # Create ZIP file
    zip_path = zip_name
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # Cleanup
    shutil.rmtree(temp_dir)
    print(f"[OK] Created {zip_path}")
    return zip_path

def deploy_lambda_function(function_name, zip_path, role_arn, handler='lambda_function.lambda_handler'):
    """Deploy or update Lambda function"""
    print(f"[*] Deploying {function_name}...")
    
    try:
        # Try to get existing function
        lambda_client.get_function(FunctionName=function_name)
        # Function exists, update it
        print(f"   Function exists, updating...")
        with open(zip_path, 'rb') as zip_file:
            response = lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_file.read()
            )
        
        # Wait for code update to complete before updating configuration
        import time
        waiter = lambda_client.get_waiter('function_updated')
        waiter.wait(FunctionName=function_name)
        
        # Update configuration
        try:
            lambda_client.update_function_configuration(
                FunctionName=function_name,
                Timeout=30,
                MemorySize=512,
                Handler=handler,
                Runtime='python3.11'
            )
            print(f"[OK] Updated {function_name}")
        except Exception as e:
            print(f"[WARNING] Could not update configuration: {e}")
            print(f"         Configuration may already be correct")
        
    except lambda_client.exceptions.ResourceNotFoundException:
        # Function doesn't exist, create it
        print(f"   Creating new function...")
        with open(zip_path, 'rb') as zip_file:
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.11',
                Role=role_arn,
                Handler=handler,
                Code={'ZipFile': zip_file.read()},
                Timeout=30,
                MemorySize=512,
                Description=f'{function_name} Lambda function'
            )
        print(f"[OK] Created {function_name}")
    
    return response['FunctionArn']

def create_api_gateway(lambda_arns):
    """Create API Gateway REST API"""
    print(f"[*] Creating API Gateway...")
    
    # Create REST API
    api_response = apigateway.create_rest_api(
        name='face-recognition-attendance-api',
        description='API for Face Recognition Attendance System',
        endpointConfiguration={'types': ['REGIONAL']}
    )
    api_id = api_response['id']
    print(f"[OK] Created API Gateway: {api_id}")
    
    # Get root resource
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = [r['id'] for r in resources['items'] if r['path'] == '/'][0]
    
    # Create resources and methods
    endpoints = [
        ('upload', 'POST', 'ProcessAttendance', lambda_arns[0]),
        ('register-face', 'POST', 'RegisterFace', lambda_arns[1]),
        ('attendance', 'GET', 'GetAttendance', lambda_arns[2])
    ]
    
    for path, method, func_name, func_arn in endpoints:
        print(f"[*] Creating {method} /{path}...")
        
        # Create resource
        resource_response = apigateway.create_resource(
            restApiId=api_id,
            parentId=root_id,
            pathPart=path
        )
        resource_id = resource_response['id']
        
        # Create method
        apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            authorizationType='NONE'
        )
        
        # Create integration with Lambda
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/{func_arn}/invocations'
        )
        
        # Enable CORS
        if method == 'GET':
            apigateway.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=method,
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )
            apigateway.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=method,
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
        else:
            # For POST methods
            apigateway.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=method,
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )
            apigateway.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=method,
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
        
        # Add OPTIONS method for CORS
        apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            authorizationType='NONE'
        )
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={'application/json': '{"statusCode": 200}'}
        )
        apigateway.put_method_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Origin': True,
                'method.response.header.Access-Control-Allow-Methods': True,
                'method.response.header.Access-Control-Allow-Headers': True
            }
        )
        apigateway.put_integration_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Origin': "'*'",
                'method.response.header.Access-Control-Allow-Methods': "'GET,POST,OPTIONS'",
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type'"
            },
            responseTemplates={'application/json': ''}
        )
        
        print(f"[OK] Created {method} /{path}")
        
        # Grant API Gateway permission to invoke Lambda
        try:
            # Get account ID
            sts = boto3.client('sts')
            account_id = sts.get_caller_identity()['Account']
            
            lambda_client.add_permission(
                FunctionName=func_name,
                StatementId=f'apigateway-invoke-{int(time.time())}',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f'arn:aws:execute-api:{REGION}:{account_id}:{api_id}/*/{method}/{path}'
            )
        except lambda_client.exceptions.ResourceConflictException:
            pass  # Permission already exists
        except Exception as e:
            print(f"   [WARNING] Could not add permission: {e}")
    
    # Deploy API
    print(f"[*] Deploying API to 'prod' stage...")
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod',
        description='Production deployment'
    )
    print(f"[OK] API deployed")
    
    api_url = f"https://{api_id}.execute-api.{REGION}.amazonaws.com/prod"
    return api_id, api_url

def main():
    print("=" * 60)
    print("Deploying Lambda Functions and API Gateway")
    print("=" * 60)
    print()
    
    # Get IAM role ARN
    role_arn = get_role_arn()
    if not role_arn:
        return
    print(f"Using IAM Role: {role_arn}")
    print()
    
    # Deploy Lambda functions
    functions = [
        ('process-attendance', 'ProcessAttendance', 'process-attendance.zip'),
        ('manage-faces', 'RegisterFace', 'register-face.zip'),
        ('get-attendance', 'GetAttendance', 'get-attendance.zip')
    ]
    
    lambda_arns = []
    for func_dir, func_name, zip_name in functions:
        zip_path = create_zip_package(func_dir, zip_name)
        func_arn = deploy_lambda_function(func_name, zip_path, role_arn)
        lambda_arns.append(func_arn)
        print()
    
    # Create API Gateway
    api_id, api_url = create_api_gateway(lambda_arns)
    print()
    
    # Summary
    print("=" * 60)
    print("DEPLOYMENT COMPLETE")
    print("=" * 60)
    print(f"API Gateway URL: {api_url}")
    print(f"API ID: {api_id}")
    print()
    print("NEXT STEP: Update frontend/script.js with:")
    print(f'const API_BASE_URL = "{api_url}";')
    print()
    
    # Cleanup ZIP files
    for _, _, zip_name in functions:
        if os.path.exists(zip_name):
            os.remove(zip_name)
            print(f"Cleaned up {zip_name}")

if __name__ == '__main__':
    main()

