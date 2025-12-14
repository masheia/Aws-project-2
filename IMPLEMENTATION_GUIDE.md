# Step-by-Step Implementation Guide

## Prerequisites
- AWS Account (Free Tier eligible)
- AWS CLI configured (optional but recommended)
- Basic knowledge of AWS Console

## Step 1: Create S3 Buckets

1. Go to S3 Console
2. Create bucket: `attendance-images-bucket` (replace with unique name)
3. Enable versioning (optional)
4. Block public access: Keep enabled for security
5. Create folder structure:
   - `attendance/` - For attendance photos
   - `students/` - For registered student faces

## Step 2: Create DynamoDB Tables

### Table 1: Students
- Table name: `Students`
- Partition key: `FaceId` (String)
- Add Global Secondary Index:
  - Index name: `StudentId-index`
  - Partition key: `StudentId` (String)

### Table 2: AttendanceRecords
- Table name: `AttendanceRecords`
- Partition key: `AttendanceId` (String)
- Add Global Secondary Indexes:
  - `Date-index`: Partition key `Date` (String)
  - `StudentId-Date-index`: Partition key `StudentId` (String), Sort key `Date` (String)

## Step 3: Create Rekognition Face Collection

1. Go to Amazon Rekognition Console
2. Navigate to "Face collections"
3. Create collection:
   - Collection ID: `attendance-students`
   - Note: Collection name must be lowercase

## Step 4: Create SNS Topic

1. Go to SNS Console
2. Create topic: `attendance-notifications`
3. Note the Topic ARN
4. Subscribe to topic (email or SMS for testing)

## Step 5: Create IAM Role for Lambda

1. Go to IAM Console
2. Create role: `LambdaAttendanceRole`
3. Attach policies:
   - `AWSLambdaBasicExecutionRole`
   - Custom policy with permissions for:
     - S3 (read/write to bucket)
     - Rekognition (all actions)
     - DynamoDB (read/write to tables)
     - SNS (publish)

### Custom Policy JSON:
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
            "Resource": "arn:aws:s3:::attendance-images-bucket/*"
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
                "arn:aws:dynamodb:*:*:table/Students",
                "arn:aws:dynamodb:*:*:table/Students/index/*",
                "arn:aws:dynamodb:*:*:table/AttendanceRecords",
                "arn:aws:dynamodb:*:*:table/AttendanceRecords/index/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:*:*:attendance-notifications"
        }
    ]
}
```

## Step 6: Create Lambda Functions

### Function 1: Process Attendance

1. Go to Lambda Console
2. Create function: `ProcessAttendance`
3. Runtime: Python 3.11
4. Architecture: x86_64
5. Execution role: Use `LambdaAttendanceRole`
6. Copy code from `lambda-functions/process-attendance/lambda_function.py`
7. Update constants:
   - `FACE_COLLECTION_ID`
   - `ATTENDANCE_TABLE`
   - `STUDENTS_TABLE`
   - `SNS_TOPIC_ARN`
   - `S3_BUCKET`
8. Timeout: 30 seconds
9. Memory: 512 MB

### Function 2: Register Face

1. Create function: `RegisterFace`
2. Same settings as above
3. Copy code from `lambda-functions/manage-faces/lambda_function.py`
4. Update constants

### Function 3: Get Attendance

1. Create function: `GetAttendance`
2. Same settings as above
3. Copy code from `lambda-functions/get-attendance/lambda_function.py`
4. Update constants

## Step 7: Create API Gateway

1. Go to API Gateway Console
2. Create REST API
3. Create resources:
   - `/upload` - POST
   - `/register-face` - POST
   - `/attendance` - GET

### Enable CORS:
For each method, enable CORS with:
- Access-Control-Allow-Origin: *
- Access-Control-Allow-Methods: GET, POST, OPTIONS
- Access-Control-Allow-Headers: Content-Type

### Connect to Lambda:
- `/upload` → `ProcessAttendance` function
- `/register-face` → `RegisterFace` function
- `/attendance` → `GetAttendance` function

4. Deploy API:
   - Stage: `prod`
   - Note the API endpoint URL

## Step 8: Deploy Frontend

### Option 1: S3 Static Website Hosting
1. Create S3 bucket: `attendance-frontend-bucket`
2. Enable static website hosting
3. Upload HTML, CSS, JS files
4. Update `API_BASE_URL` in `script.js` with your API Gateway endpoint
5. Set bucket policy for public read access (for demo only)

### Option 2: Local Testing
1. Use a local web server (Python: `python -m http.server`)
2. Update CORS settings in API Gateway if needed
3. Update `API_BASE_URL` in `script.js`

## Step 9: Testing

1. Register a student:
   - Go to "Register Student" tab
   - Enter Student ID and Name
   - Upload clear face photo
   - Click "Register Student"

2. Mark attendance:
   - Go to "Mark Attendance" tab
   - Select class and date
   - Upload photo with registered student(s)
   - Click "Process Attendance"

3. View attendance:
   - Go to "View Attendance" tab
   - Filter by date or student ID
   - View attendance records

## Step 10: Monitor and Optimize

1. Check CloudWatch Logs for Lambda functions
2. Monitor DynamoDB usage
3. Monitor Rekognition usage (stay within free tier)
4. Review S3 storage usage
5. Check SNS notifications

## Troubleshooting

### Common Issues:

1. **Collection not found error**
   - Ensure collection ID matches exactly
   - Check Rekognition console

2. **Access denied errors**
   - Verify IAM role permissions
   - Check S3 bucket policies

3. **No faces detected**
   - Ensure image has clear face
   - Check image quality and format

4. **CORS errors**
   - Verify CORS settings in API Gateway
   - Check headers in Lambda responses

## Cost Optimization Tips

1. Use S3 lifecycle policies to archive old images
2. Set DynamoDB auto-scaling
3. Monitor Rekognition usage (free tier: 5,000 images/month)
4. Use CloudWatch alarms for cost tracking




