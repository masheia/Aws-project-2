# Setup Configuration Template

## Important: Update These Values

Before deploying, update the following constants in your Lambda functions and frontend:

### Lambda Functions Configuration

#### 1. `lambda-functions/process-attendance/lambda_function.py`
Update these constants at the top of the file:
```python
FACE_COLLECTION_ID = 'attendance-students'  # Your Rekognition collection ID
ATTENDANCE_TABLE = 'AttendanceRecords'      # Your DynamoDB table name
STUDENTS_TABLE = 'Students'                 # Your DynamoDB table name
SNS_TOPIC_ARN = 'arn:aws:sns:YOUR_REGION:YOUR_ACCOUNT_ID:attendance-notifications'
S3_BUCKET = 'YOUR_BUCKET_NAME'              # Your S3 bucket name
```

#### 2. `lambda-functions/manage-faces/lambda_function.py`
Update these constants:
```python
FACE_COLLECTION_ID = 'attendance-students'
STUDENTS_TABLE = 'Students'
S3_BUCKET = 'YOUR_BUCKET_NAME'
```

#### 3. `lambda-functions/get-attendance/lambda_function.py`
Update these constants:
```python
ATTENDANCE_TABLE = 'AttendanceRecords'
```

### Frontend Configuration

#### `frontend/script.js`
Update the API endpoint:
```javascript
const API_BASE_URL = 'https://YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com/prod';
```

Replace:
- `YOUR_API_ID` - Your API Gateway API ID
- `YOUR_REGION` - Your AWS region (e.g., us-east-1, eu-west-1)

### IAM Role Policy

Update the IAM role policy with your actual resource ARNs:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
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
                "dynamodb:Scan"
            ],
            "Resource": [
                "arn:aws:dynamodb:YOUR_REGION:YOUR_ACCOUNT_ID:table/Students",
                "arn:aws:dynamodb:YOUR_REGION:YOUR_ACCOUNT_ID:table/Students/index/*",
                "arn:aws:dynamodb:YOUR_REGION:YOUR_ACCOUNT_ID:table/AttendanceRecords",
                "arn:aws:dynamodb:YOUR_REGION:YOUR_ACCOUNT_ID:table/AttendanceRecords/index/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:YOUR_REGION:YOUR_ACCOUNT_ID:attendance-notifications"
        }
    ]
}
```

## Quick Checklist

- [ ] Create S3 bucket and note the name
- [ ] Create DynamoDB tables (Students, AttendanceRecords)
- [ ] Create Rekognition collection (attendance-students)
- [ ] Create SNS topic and note the ARN
- [ ] Create IAM role with proper permissions
- [ ] Update all Lambda function constants
- [ ] Deploy Lambda functions
- [ ] Create API Gateway and get endpoint URL
- [ ] Update frontend script.js with API endpoint
- [ ] Test the system end-to-end

## Finding Your AWS Account ID

You can find your AWS Account ID:
1. In the AWS Console, click on your account name (top right)
2. The account ID is displayed in the dropdown

## Finding Your AWS Region

Common regions:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-1 (Singapore)

Check your current region in the AWS Console (top right corner).




