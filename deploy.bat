@echo off
REM Face Recognition Attendance System - Windows Deployment Script
REM Prerequisites: AWS CLI configured with credentials

echo 🚀 Starting deployment of Face Recognition Attendance System...
echo.

REM Configuration - UPDATE THESE VALUES
set REGION=us-east-1
set TIMESTAMP=%RANDOM%
set BUCKET_NAME=attendance-images-%TIMESTAMP%
set FRONTEND_BUCKET=attendance-frontend-%TIMESTAMP%

REM Check if AWS CLI is installed
where aws >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: AWS CLI not found. Please install AWS CLI first.
    pause
    exit /b 1
)

REM Check if AWS CLI is configured
aws sts get-caller-identity >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: AWS CLI not configured or credentials invalid
    echo Run: aws configure
    pause
    exit /b 1
)

echo Using Region: %REGION%
echo.

REM Get AWS Account ID
echo Detecting AWS Account ID...
for /f "tokens=*" %%i in ('aws sts get-caller-identity --query Account --output text') do set AWS_ACCOUNT_ID=%%i
echo Found Account ID: %AWS_ACCOUNT_ID%
echo.

REM Step 1: Create S3 buckets
echo 📦 Step 1: Creating S3 buckets...
aws s3 mb s3://%BUCKET_NAME% --region %REGION%
aws s3 mb s3://%FRONTEND_BUCKET% --region %REGION%
echo ✅ Created buckets: %BUCKET_NAME% and %FRONTEND_BUCKET%
echo.

REM Step 2: Create DynamoDB tables (simplified - tables need JSON file)
echo 🗄️  Step 2: Creating DynamoDB tables...
echo ⚠️  Note: DynamoDB tables should be created using AWS Console
echo    or by importing dynamodb-tables/table-definitions.json
echo    See IMPLEMENTATION_GUIDE.md for detailed instructions
echo.

REM Step 3: Create Rekognition collection
echo 👤 Step 3: Creating Rekognition collection...
aws rekognition create-collection --collection-id attendance-students --region %REGION% 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Created Rekognition collection: attendance-students
) else (
    echo ℹ️  Collection may already exist or failed to create
)
echo.

REM Step 4: Create SNS topic
echo 📧 Step 4: Creating SNS topic...
for /f "tokens=*" %%i in ('aws sns create-topic --name attendance-notifications --region %REGION% --query TopicArn --output text') do set SNS_TOPIC_ARN=%%i
echo ✅ Created SNS topic: %SNS_TOPIC_ARN%
echo.

REM Step 5: Deploy frontend
echo 🌐 Step 7: Deploying frontend...
aws s3 sync frontend\ s3://%FRONTEND_BUCKET% --region %REGION%
aws s3 website s3://%FRONTEND_BUCKET% --index-document index.html --error-document index.html

set FRONTEND_URL=http://%FRONTEND_BUCKET%.s3-website-%REGION%.amazonaws.com
echo ✅ Frontend deployed to: %FRONTEND_URL%
echo.

REM Summary
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📋 DEPLOYMENT SUMMARY
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Region: %REGION%
echo Account ID: %AWS_ACCOUNT_ID%
echo S3 Bucket (Images): %BUCKET_NAME%
echo S3 Bucket (Frontend): %FRONTEND_BUCKET%
echo Frontend URL: %FRONTEND_URL%
echo SNS Topic ARN: %SNS_TOPIC_ARN%
echo.
echo 📝 NEXT STEPS:
echo 1. Create IAM role 'LambdaAttendanceRole' with proper permissions
echo 2. Create DynamoDB tables (Students, AttendanceRecords)
echo 3. Update Lambda function constants
echo 4. Deploy Lambda functions via AWS Console
echo 5. Create API Gateway
echo 6. Update frontend/script.js with API Gateway endpoint
echo 7. Test the system!
echo.
echo ✅ Partial deployment complete!
pause




