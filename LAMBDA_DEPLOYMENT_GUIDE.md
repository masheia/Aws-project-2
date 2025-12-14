# Lambda Functions Deployment Guide

This guide explains how to deploy the Lambda functions to AWS.

## Option 1: Deploy via AWS Console (Recommended for Beginners)

### Step 1: Prepare Lambda Function Packages

For each Lambda function, you need to create a deployment package:

#### Function 1: Process Attendance

1. Create a temporary directory:
```bash
mkdir lambda-process-attendance
cd lambda-process-attendance
```

2. Copy the Lambda function code:
```bash
cp ../lambda-functions/process-attendance/lambda_function.py .
cp ../lambda-functions/process-attendance/requirements.txt .
```

3. Install dependencies (if any):
```bash
pip install -r requirements.txt -t .
```

4. Create ZIP file:
```bash
# On Windows (PowerShell)
Compress-Archive -Path * -DestinationPath process-attendance.zip

# On Linux/Mac
zip -r process-attendance.zip .
```

5. Go to AWS Lambda Console → Create Function
6. Choose "Author from scratch"
7. Function name: `ProcessAttendance`
8. Runtime: Python 3.11
9. Architecture: x86_64
10. Execution role: `LambdaAttendanceRole` (create if doesn't exist)
11. Click "Create function"
12. In "Code" tab, click "Upload from" → ".zip file"
13. Upload your `process-attendance.zip`
14. **Update constants** in the code editor:
    - `FACE_COLLECTION_ID`
    - `ATTENDANCE_TABLE`
    - `STUDENTS_TABLE`
    - `SNS_TOPIC_ARN`
    - `S3_BUCKET`
15. Click "Deploy"
16. Configure:
    - Timeout: 30 seconds
    - Memory: 512 MB

Repeat for other functions:
- `RegisterFace` (from `lambda-functions/manage-faces/`)
- `GetAttendance` (from `lambda-functions/get-attendance/`)

## Option 2: Deploy via AWS CLI

### Install dependencies and create deployment packages:

```bash
# For each Lambda function directory
cd lambda-functions/process-attendance
pip install -r requirements.txt -t .
zip -r ../../process-attendance.zip .
cd ../..
```

### Deploy using AWS CLI:

```bash
# Update function code
aws lambda update-function-code \
    --function-name ProcessAttendance \
    --zip-file fileb://process-attendance.zip \
    --region us-east-1

# Update function configuration
aws lambda update-function-configuration \
    --function-name ProcessAttendance \
    --timeout 30 \
    --memory-size 512 \
    --region us-east-1
```

## Option 3: Deploy via AWS SAM (Infrastructure as Code)

### Install AWS SAM CLI:
```bash
# Follow instructions at: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
```

### Create `template.yaml`:
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Face Recognition Attendance System

Parameters:
  S3Bucket:
    Type: String
    Default: attendance-images-bucket
  SNSTopicArn:
    Type: String
    Default: arn:aws:sns:us-east-1:123456789012:attendance-notifications
  Region:
    Type: String
    Default: us-east-1

Resources:
  ProcessAttendanceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: ProcessAttendance
      CodeUri: lambda-functions/process-attendance/
      Handler: lambda_function.lambda_handler
      Runtime: python3.11
      Timeout: 30
      MemorySize: 512
      Environment:
        Variables:
          FACE_COLLECTION_ID: attendance-students
          ATTENDANCE_TABLE: AttendanceRecords
          STUDENTS_TABLE: Students
          SNS_TOPIC_ARN: !Ref SNSTopicArn
          S3_BUCKET: !Ref S3Bucket
      Policies:
        - S3ReadWritePolicy:
            BucketName: !Ref S3Bucket
        - DynamoDBCrudPolicy:
            TableName: !Ref StudentsTable
        - DynamoDBCrudPolicy:
            TableName: !Ref AttendanceRecordsTable
        - SNSPublishMessagePolicy:
            TopicName: attendance-notifications
        - RekognitionDetectOnlyPolicy: {}

  RegisterFaceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: RegisterFace
      CodeUri: lambda-functions/manage-faces/
      Handler: lambda_function.lambda_handler
      Runtime: python3.11
      Timeout: 30
      MemorySize: 512
      Environment:
        Variables:
          FACE_COLLECTION_ID: attendance-students
          STUDENTS_TABLE: Students
          S3_BUCKET: !Ref S3Bucket
      Policies:
        - S3ReadWritePolicy:
            BucketName: !Ref S3Bucket
        - DynamoDBCrudPolicy:
            TableName: !Ref StudentsTable
        - RekognitionDetectOnlyPolicy: {}

  GetAttendanceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: GetAttendance
      CodeUri: lambda-functions/get-attendance/
      Handler: lambda_function.lambda_handler
      Runtime: python3.11
      Timeout: 30
      MemorySize: 512
      Environment:
        Variables:
          ATTENDANCE_TABLE: AttendanceRecords
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref AttendanceRecordsTable

Outputs:
  ProcessAttendanceFunctionArn:
    Description: ARN of Process Attendance Lambda Function
    Value: !GetAtt ProcessAttendanceFunction.Arn
```

### Deploy with SAM:
```bash
sam build
sam deploy --guided
```

## Important Notes

1. **Update Constants**: Always update the constants in each Lambda function with your actual AWS resource names/ARNs before deploying.

2. **IAM Permissions**: Ensure the Lambda execution role has permissions for:
   - S3 (read/write)
   - DynamoDB (read/write)
   - Rekognition (all actions)
   - SNS (publish)

3. **Test After Deployment**: Always test each function after deployment using the Lambda console test feature.

4. **Environment Variables**: Consider using environment variables instead of hardcoded values for better security.

## Testing Lambda Functions

### Test Process Attendance:
```json
{
  "body": "{\"image\":\"data:image/jpeg;base64,...\",\"classId\":\"CS101\",\"date\":\"2024-01-15\"}"
}
```

### Test Register Face:
```json
{
  "body": "{\"studentId\":\"STU001\",\"name\":\"John Doe\",\"image\":\"data:image/jpeg;base64,...\"}"
}
```

### Test Get Attendance:
```json
{
  "queryStringParameters": {
    "date": "2024-01-15"
  }
}
```

## Troubleshooting

- **Import errors**: Ensure all dependencies are included in the deployment package
- **Timeout errors**: Increase timeout in function configuration
- **Permission errors**: Check IAM role permissions
- **Resource not found**: Verify resource names match exactly




