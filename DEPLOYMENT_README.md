# Deployment Instructions

This project includes multiple deployment options. Choose the one that works best for you.

## Prerequisites

1. **AWS Account** with Free Tier access
2. **AWS CLI** installed and configured
   - Install: https://aws.amazon.com/cli/
   - Configure: `aws configure`
3. **Python 3.8+** (for Python deployment script)
4. **boto3** installed (for Python script): `pip install boto3`

## Deployment Options

### Option 1: Python Script (Recommended - Easiest)

**Best for**: Automated deployment, cross-platform support

```bash
# Install boto3 if not installed
pip install boto3

# Run deployment script
python deploy.py
```

The script will:
- ✅ Create S3 buckets
- ✅ Create DynamoDB tables
- ✅ Create Rekognition collection
- ✅ Create SNS topic
- ✅ Deploy frontend to S3
- ❌ Lambda functions need manual deployment (see below)
- ❌ IAM role needs manual creation (see IMPLEMENTATION_GUIDE.md)

**Note**: You may need to update the `REGION` variable in `deploy.py` to match your preferred AWS region.

### Option 2: Bash Script (Linux/Mac)

**Best for**: Linux and Mac users familiar with bash

```bash
# Make script executable
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

**Note**: Update configuration variables at the top of `deploy.sh` before running.

### Option 3: Windows Batch Script

**Best for**: Windows users

```cmd
# Double-click deploy.bat or run from command prompt
deploy.bat
```

**Note**: Some steps (like DynamoDB table creation) may need to be done manually via AWS Console.

### Option 4: Manual Deployment via AWS Console

**Best for**: Learning AWS, step-by-step control

Follow the detailed instructions in `IMPLEMENTATION_GUIDE.md`

## What Gets Deployed Automatically

✅ **S3 Buckets**
- Images bucket (for storing photos)
- Frontend bucket (for hosting web interface)

✅ **DynamoDB Tables**
- Students table
- AttendanceRecords table

✅ **Rekognition Collection**
- Collection ID: `attendance-students`

✅ **SNS Topic**
- Topic name: `attendance-notifications`

✅ **Frontend**
- HTML, CSS, JavaScript files deployed to S3

## What Needs Manual Setup

❌ **IAM Role** - Must be created manually with proper permissions
   - See `IMPLEMENTATION_GUIDE.md` Step 5

❌ **Lambda Functions** - Must be deployed manually
   - See `LAMBDA_DEPLOYMENT_GUIDE.md`

❌ **API Gateway** - Must be created manually
   - See `IMPLEMENTATION_GUIDE.md` Step 7

## After Deployment

1. **Create IAM Role** for Lambda functions
2. **Update Lambda Constants** with your resource names:
   - S3 bucket name
   - DynamoDB table names
   - SNS topic ARN
   - AWS region
   - Account ID

3. **Deploy Lambda Functions** (see `LAMBDA_DEPLOYMENT_GUIDE.md`)

4. **Create API Gateway**:
   - Create REST API
   - Connect to Lambda functions
   - Enable CORS
   - Deploy to `prod` stage
   - Note the endpoint URL

5. **Update Frontend**:
   - Edit `frontend/script.js`
   - Update `API_BASE_URL` with your API Gateway endpoint

6. **Test the System**:
   - Register a student
   - Mark attendance
   - View attendance dashboard

## Troubleshooting

### AWS CLI Not Found
- Install AWS CLI: https://aws.amazon.com/cli/
- Verify: `aws --version`

### Credentials Not Configured
- Run: `aws configure`
- Enter your Access Key ID and Secret Access Key

### Permission Denied Errors
- Check IAM user permissions
- Ensure your user has permission to create resources

### Region Issues
- Update `REGION` variable in deployment scripts
- Ensure all resources are in the same region

### Lambda Deployment Issues
- See `LAMBDA_DEPLOYMENT_GUIDE.md`
- Check function code for syntax errors
- Verify IAM role has proper permissions

## Cost Considerations

All resources created are within AWS Free Tier:
- S3: 5GB storage free
- DynamoDB: 25GB storage free
- Lambda: 1M requests/month free
- Rekognition: 5,000 images/month free
- API Gateway: 1M requests/month free
- SNS: 1M requests/month free

**Monitor your usage** to stay within free tier limits!

## Need Help?

1. Check `IMPLEMENTATION_GUIDE.md` for detailed steps
2. Review `SETUP_CONFIG.md` for configuration values
3. See `LAMBDA_DEPLOYMENT_GUIDE.md` for Lambda deployment
4. Check AWS CloudWatch logs for errors

Good luck with your deployment! 🚀




