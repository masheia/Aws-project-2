#!/bin/bash

# Face Recognition Attendance System - Deployment Script
# This script helps deploy the infrastructure to AWS
# Prerequisites: AWS CLI configured with credentials

set -e  # Exit on error

# Configuration - UPDATE THESE VALUES
REGION="us-east-1"
AWS_ACCOUNT_ID=""  # Leave empty to auto-detect
BUCKET_NAME="attendance-images-$(date +%s)"  # Unique bucket name
FRONTEND_BUCKET="attendance-frontend-$(date +%s)"
STACK_NAME="face-recognition-attendance"

echo "🚀 Starting deployment of Face Recognition Attendance System..."
echo ""

# Get AWS Account ID if not provided
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "Detecting AWS Account ID..."
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    echo "Found Account ID: $AWS_ACCOUNT_ID"
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Error: AWS CLI not configured or credentials invalid"
    echo "Run: aws configure"
    exit 1
fi

echo "Using Region: $REGION"
echo "Using Account ID: $AWS_ACCOUNT_ID"
echo ""

# Step 1: Create S3 buckets
echo "📦 Step 1: Creating S3 buckets..."
aws s3 mb s3://$BUCKET_NAME --region $REGION
aws s3 mb s3://$FRONTEND_BUCKET --region $REGION
echo "✅ Created buckets: $BUCKET_NAME and $FRONTEND_BUCKET"
echo ""

# Step 2: Create DynamoDB tables
echo "🗄️  Step 2: Creating DynamoDB tables..."

# Create Students table
aws dynamodb create-table \
    --table-name Students \
    --attribute-definitions \
        AttributeName=FaceId,AttributeType=S \
        AttributeName=StudentId,AttributeType=S \
    --key-schema \
        AttributeName=FaceId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --global-secondary-indexes \
        "[{\"IndexName\":\"StudentId-index\",\"KeySchema\":[{\"AttributeName\":\"StudentId\",\"KeyType\":\"HASH\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}]" \
    --region $REGION

# Wait for table to be active
echo "Waiting for Students table..."
aws dynamodb wait table-exists --table-name Students --region $REGION

# Create AttendanceRecords table
aws dynamodb create-table \
    --table-name AttendanceRecords \
    --attribute-definitions \
        AttributeName=AttendanceId,AttributeType=S \
        AttributeName=Date,AttributeType=S \
        AttributeName=StudentId,AttributeType=S \
    --key-schema \
        AttributeName=AttendanceId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --global-secondary-indexes \
        "[{\"IndexName\":\"Date-index\",\"KeySchema\":[{\"AttributeName\":\"Date\",\"KeyType\":\"HASH\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}},{\"IndexName\":\"StudentId-Date-index\",\"KeySchema\":[{\"AttributeName\":\"StudentId\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"Date\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}]" \
    --region $REGION

echo "Waiting for AttendanceRecords table..."
aws dynamodb wait table-exists --table-name AttendanceRecords --region $REGION
echo "✅ Created DynamoDB tables"
echo ""

# Step 3: Create Rekognition collection
echo "👤 Step 3: Creating Rekognition collection..."
aws rekognition create-collection \
    --collection-id attendance-students \
    --region $REGION 2>/dev/null || echo "Collection may already exist"
echo "✅ Created Rekognition collection: attendance-students"
echo ""

# Step 4: Create SNS topic
echo "📧 Step 4: Creating SNS topic..."
SNS_TOPIC_ARN=$(aws sns create-topic \
    --name attendance-notifications \
    --region $REGION \
    --query 'TopicArn' --output text)
echo "✅ Created SNS topic: $SNS_TOPIC_ARN"
echo ""

# Step 5: Create IAM role (simplified - you may need to customize)
echo "🔐 Step 5: Creating IAM role..."
echo "⚠️  Note: IAM role creation requires manual configuration in AWS Console"
echo "   See IMPLEMENTATION_GUIDE.md for IAM role setup"
echo ""

# Step 6: Package and deploy Lambda functions
echo "⚡ Step 6: Preparing Lambda functions..."
echo "⚠️  Lambda functions need to be deployed manually via AWS Console"
echo "   or using AWS SAM/CloudFormation"
echo "   See lambda-deployment-guide.md for instructions"
echo ""

# Step 7: Deploy frontend
echo "🌐 Step 7: Deploying frontend..."
aws s3 sync frontend/ s3://$FRONTEND_BUCKET --region $REGION
aws s3 website s3://$FRONTEND_BUCKET \
    --index-document index.html \
    --error-document index.html

# Make frontend bucket public (for demo only)
aws s3api put-bucket-policy --bucket $FRONTEND_BUCKET --policy "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [{
        \"Sid\": \"PublicReadGetObject\",
        \"Effect\": \"Allow\",
        \"Principal\": \"*\",
        \"Action\": \"s3:GetObject\",
        \"Resource\": \"arn:aws:s3:::$FRONTEND_BUCKET/*\"
    }]
}"

FRONTEND_URL="http://$FRONTEND_BUCKET.s3-website-$REGION.amazonaws.com"
echo "✅ Frontend deployed to: $FRONTEND_URL"
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 DEPLOYMENT SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Region: $REGION"
echo "Account ID: $AWS_ACCOUNT_ID"
echo "S3 Bucket (Images): $BUCKET_NAME"
echo "S3 Bucket (Frontend): $FRONTEND_BUCKET"
echo "Frontend URL: $FRONTEND_URL"
echo "SNS Topic ARN: $SNS_TOPIC_ARN"
echo ""
echo "📝 NEXT STEPS:"
echo "1. Create IAM role 'LambdaAttendanceRole' with proper permissions"
echo "2. Update Lambda function constants with:"
echo "   - S3_BUCKET: $BUCKET_NAME"
echo "   - SNS_TOPIC_ARN: $SNS_TOPIC_ARN"
echo "   - REGION: $REGION"
echo "   - ACCOUNT_ID: $AWS_ACCOUNT_ID"
echo "3. Deploy Lambda functions (see lambda-deployment-guide.md)"
echo "4. Create API Gateway and connect to Lambda functions"
echo "5. Update frontend/script.js with API Gateway endpoint"
echo "6. Test the system!"
echo ""
echo "✅ Infrastructure deployment complete!"




