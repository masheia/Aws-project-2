# 🔗 AWS Console Links - Quick Access

## 📋 All AWS Services Used in This Project

Direct links to access each service in the AWS Console.

---

## 🪣 Amazon S3 (Storage)

### Images Bucket
**Bucket Name:** `attendance-images-1765405751`

**Direct Console Link:**
https://console.aws.amazon.com/s3/buckets/attendance-images-1765405751?region=us-east-1

**What's stored:**
- Student registration photos
- Attendance photos
- Organized in folders: `students/` and `attendance/`

---

### Frontend Bucket (Website)
**Bucket Name:** `attendance-frontend-1765405751`

**Direct Console Link:**
https://console.aws.amazon.com/s3/buckets/attendance-frontend-1765405751?region=us-east-1

**What's stored:**
- Frontend website files (HTML, CSS, JavaScript)
- Live website: http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com

---

### S3 Console (All Buckets)
https://console.aws.amazon.com/s3/home?region=us-east-1

---

## 🤖 AWS Lambda (Serverless Functions)

### RegisterFace Function
**Function Name:** `RegisterFace`

**Direct Console Link:**
https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/RegisterFace

**Purpose:** Registers new student faces in Rekognition

---

### ProcessAttendance Function
**Function Name:** `ProcessAttendance`

**Direct Console Link:**
https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessAttendance

**Purpose:** Processes attendance photos and identifies students

---

### GetAttendance Function
**Function Name:** `GetAttendance`

**Direct Console Link:**
https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/GetAttendance

**Purpose:** Retrieves attendance records from DynamoDB

---

### Lambda Console (All Functions)
https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions

---

## 🌐 Amazon API Gateway (REST API)

### Your API
**API ID:** `pjjf6u13f8`
**API Name:** Face Recognition Attendance API

**Direct Console Link:**
https://console.aws.amazon.com/apigateway/main/apis/pjjf6u13f8?region=us-east-1

**Base URL:**
```
https://pjjf6u13f8.execute-api.us-east-1.amazonaws.com/prod
```

**Endpoints:**
- `POST /register-face` → RegisterFace Lambda
- `POST /upload` → ProcessAttendance Lambda
- `GET /attendance` → GetAttendance Lambda

---

### API Gateway Console (All APIs)
https://console.aws.amazon.com/apigateway/main/apis?region=us-east-1

---

## 🗄️ Amazon DynamoDB (Database)

### Students Table
**Table Name:** `Students`

**Direct Console Link:**
https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=Students

**What's stored:**
- Student ID
- Student Name
- Email
- Face ID (from Rekognition)
- Registration date
- Face details

---

### AttendanceRecords Table
**Table Name:** `AttendanceRecords`

**Direct Console Link:**
https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=AttendanceRecords

**What's stored:**
- Attendance records
- Student ID
- Date and timestamp
- Confidence scores
- Class ID

---

### DynamoDB Console (All Tables)
https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables

---

## 👁️ Amazon Rekognition (Face Recognition)

### Face Collection
**Collection ID:** `attendance-students`

**Note:** Face collections are not directly accessible via console UI, but you can:

**View via AWS CLI:**
```bash
aws rekognition describe-collection \
    --collection-id attendance-students \
    --region us-east-1

aws rekognition list-faces \
    --collection-id attendance-students \
    --region us-east-1
```

**Rekognition Console:**
https://console.aws.amazon.com/rekognition/home?region=us-east-1

**Demos Available:**
- Facial analysis
- Face comparison
- Face liveness
- Label detection

---

## 📧 Amazon SNS (Notifications)

### Notification Topic
**Topic Name:** `attendance-notifications`
**Topic ARN:** `arn:aws:sns:us-east-1:846863292978:attendance-notifications`

**Direct Console Link:**
https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/topic/arn:aws:sns:us-east-1:846863292978:attendance-notifications

**What it does:**
- Sends email notifications when attendance is recorded
- Sends welcome emails to new students
- Manages email subscriptions

---

### SNS Console (All Topics)
https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/topics

---

## ☁️ Amazon CloudFront (CDN)

### Distribution
**Distribution ID:** `E3EMVVYFDKKCB8`
**Domain:** `d3d3y3hf5su68f.cloudfront.net`

**Direct Console Link:**
https://console.aws.amazon.com/cloudfront/v3/home#/distributions/E3EMVVYFDKKCB8

**What it does:**
- Provides HTTPS access to frontend
- CDN for faster global access
- Secure URL: https://d3d3y3hf5su68f.cloudfront.net

---

### CloudFront Console (All Distributions)
https://console.aws.amazon.com/cloudfront/v3/home#/distributions

---

## 🔐 AWS IAM (Identity & Access Management)

### Lambda Execution Role
**Role Name:** `FaceRecognitionAttendanceRole`

**Direct Console Link:**
https://console.aws.amazon.com/iam/home#/roles/FaceRecognitionAttendanceRole

**What it does:**
- Provides permissions for Lambda functions
- Allows access to S3, Rekognition, DynamoDB, SNS

---

### IAM Console (All Roles)
https://console.aws.amazon.com/iam/home#/roles

---

## 📊 Amazon CloudWatch (Logs & Monitoring)

### Lambda Function Logs

**RegisterFace Logs:**
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/%2Faws%2Flambda%2FRegisterFace

**ProcessAttendance Logs:**
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/%2Faws%2Flambda%2FProcessAttendance

**GetAttendance Logs:**
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/%2Faws%2Flambda%2FGetAttendance

---

### CloudWatch Logs Console
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups

---

## 🏠 AWS Console Home

**Main Console:**
https://console.aws.amazon.com/

**Region:** us-east-1 (N. Virginia)

---

## 📱 Live Website Links

### Frontend Website
**S3 Website Endpoint (HTTP):**
http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com

**CloudFront (HTTPS):**
https://d3d3y3hf5su68f.cloudfront.net

**Login Page:**
http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com/login.html

**Sign Up Page:**
http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com/signup.html

---

## 🔑 Quick Access Summary

| Service | Resource | Direct Link |
|---------|----------|-------------|
| **S3** | Images Bucket | [View Bucket](https://console.aws.amazon.com/s3/buckets/attendance-images-1765405751?region=us-east-1) |
| **S3** | Frontend Bucket | [View Bucket](https://console.aws.amazon.com/s3/buckets/attendance-frontend-1765405751?region=us-east-1) |
| **Lambda** | RegisterFace | [View Function](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/RegisterFace) |
| **Lambda** | ProcessAttendance | [View Function](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProcessAttendance) |
| **Lambda** | GetAttendance | [View Function](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/GetAttendance) |
| **API Gateway** | Main API | [View API](https://console.aws.amazon.com/apigateway/main/apis/pjjf6u13f8?region=us-east-1) |
| **DynamoDB** | Students Table | [View Table](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=Students) |
| **DynamoDB** | AttendanceRecords | [View Table](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=AttendanceRecords) |
| **Rekognition** | Console | [View Console](https://console.aws.amazon.com/rekognition/home?region=us-east-1) |
| **SNS** | Notification Topic | [View Topic](https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/topic/arn:aws:sns:us-east-1:846863292978:attendance-notifications) |
| **CloudFront** | Distribution | [View Distribution](https://console.aws.amazon.com/cloudfront/v3/home#/distributions/E3EMVVYFDKKCB8) |
| **IAM** | Lambda Role | [View Role](https://console.aws.amazon.com/iam/home#/roles/FaceRecognitionAttendanceRole) |
| **CloudWatch** | Logs | [View Logs](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups) |

---

## 🎯 Most Used Links

### For Daily Management:
1. **DynamoDB Students Table** - View all registered students
2. **DynamoDB AttendanceRecords** - View all attendance records
3. **S3 Images Bucket** - View uploaded photos
4. **CloudWatch Logs** - Debug issues

### For Monitoring:
1. **Lambda Functions** - Check function status
2. **API Gateway** - Monitor API calls
3. **CloudWatch Logs** - View error logs

### For Configuration:
1. **IAM Roles** - Check permissions
2. **SNS Topic** - Manage email subscriptions
3. **CloudFront** - Check distribution status

---

## 📝 Notes

- **Region:** All resources are in `us-east-1` (N. Virginia)
- **Account ID:** `846863292978`
- **All links require AWS login** - Make sure you're logged in
- **Bookmark these links** for quick access!

---

## 🔍 Finding Resources Manually

If links don't work, you can find resources by:

1. **Service Name** - Go to the service console
2. **Resource Name** - Search for the resource name
3. **Region** - Make sure you're in `us-east-1`

---

**All links are ready to use! Just click and access your AWS resources.** 🚀

