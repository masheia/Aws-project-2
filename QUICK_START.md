# Quick Start Guide

## Project Overview
This is a Face Recognition Attendance System built on AWS. The system automatically identifies students from uploaded photos and records attendance.

## Project Structure
```
aws-project-face-recognition/
├── README.md                          # Project overview
├── architecture-diagram.md            # System architecture
├── IMPLEMENTATION_GUIDE.md            # Detailed setup steps
├── PRESENTATION_OUTLINE.md            # Presentation structure
├── SETUP_CONFIG.md                    # Configuration template
├── QUICK_START.md                     # This file
├── lambda-functions/
│   ├── process-attendance/           # Process attendance Lambda
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   ├── manage-faces/                  # Register faces Lambda
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   └── get-attendance/                # Get attendance Lambda
│       ├── lambda_function.py
│       └── requirements.txt
├── frontend/
│   ├── index.html                     # Main HTML file
│   ├── styles.css                     # Styling
│   └── script.js                      # JavaScript logic
└── dynamodb-tables/
    └── table-definitions.json         # DynamoDB schema
```

## Prerequisites
- AWS Account (Free Tier)
- Basic AWS Console knowledge
- Python 3.11 (for local testing)

## Quick Setup (30 minutes)

### Step 1: AWS Console Setup (15 min)

1. **Create S3 Bucket**
   - Name: `attendance-images-bucket-[your-name]` (must be unique)
   - Region: Choose your preferred region

2. **Create DynamoDB Tables**
   - Table 1: `Students` (Partition key: `FaceId` - String)
   - Table 2: `AttendanceRecords` (Partition key: `AttendanceId` - String)
   - See `IMPLEMENTATION_GUIDE.md` for GSI details

3. **Create Rekognition Collection**
   - Collection ID: `attendance-students`
   - Must be lowercase

4. **Create SNS Topic**
   - Topic name: `attendance-notifications`
   - Subscribe with your email for testing

5. **Create IAM Role**
   - Role name: `LambdaAttendanceRole`
   - Attach policies (see `IMPLEMENTATION_GUIDE.md`)

### Step 2: Deploy Lambda Functions (10 min)

For each Lambda function:

1. Go to Lambda Console → Create Function
2. Choose "Author from scratch"
3. Runtime: Python 3.11
4. Execution role: `LambdaAttendanceRole`
5. Copy code from corresponding `lambda_function.py`
6. **IMPORTANT**: Update constants (S3_BUCKET, SNS_TOPIC_ARN, etc.)
7. Set timeout to 30 seconds, memory to 512 MB

Functions to create:
- `ProcessAttendance` (from `lambda-functions/process-attendance/`)
- `RegisterFace` (from `lambda-functions/manage-faces/`)
- `GetAttendance` (from `lambda-functions/get-attendance/`)

### Step 3: Create API Gateway (5 min)

1. Create REST API
2. Create resources:
   - POST `/upload` → `ProcessAttendance`
   - POST `/register-face` → `RegisterFace`
   - GET `/attendance` → `GetAttendance`
3. Enable CORS on all methods
4. Deploy to `prod` stage
5. **Note the API endpoint URL**

### Step 4: Deploy Frontend (5 min)

**Option A: S3 Static Website**
1. Create bucket: `attendance-frontend-[your-name]`
2. Enable static website hosting
3. Upload `frontend/` files
4. Update `API_BASE_URL` in `script.js`

**Option B: Local Testing**
1. Open `frontend/index.html` in a local web server
2. Update `API_BASE_URL` in `script.js`
3. Use: `python -m http.server 8000`

## Testing the System

### Test 1: Register a Student
1. Open the web interface
2. Go to "Register Student" tab
3. Enter Student ID: `STU001`
4. Enter Name: `John Doe`
5. Upload a clear face photo
6. Click "Register Student"
7. Should see success message

### Test 2: Mark Attendance
1. Go to "Mark Attendance" tab
2. Enter Class ID: `CS101`
3. Select today's date
4. Upload photo with the registered student
5. Click "Process Attendance"
6. Should identify the student and show results

### Test 3: View Attendance
1. Go to "View Attendance" tab
2. Should see the attendance record
3. Filter by date or student ID if needed

## Common Issues & Solutions

### Issue: "Collection not found"
**Solution**: Ensure Rekognition collection `attendance-students` exists and name matches exactly

### Issue: "Access Denied"
**Solution**: Check IAM role permissions, verify bucket/table names match

### Issue: "CORS error"
**Solution**: Enable CORS in API Gateway for all methods

### Issue: "No face detected"
**Solution**: Use clear, front-facing photos with good lighting

## Next Steps

1. Read `IMPLEMENTATION_GUIDE.md` for detailed steps
2. Update all configuration values (see `SETUP_CONFIG.md`)
3. Test thoroughly before presentation
4. Review `PRESENTATION_OUTLINE.md` for your presentation
5. Monitor costs in AWS Cost Explorer

## Free Tier Limits

- **Rekognition**: 5,000 images/month
- **Lambda**: 1M requests/month
- **S3**: 5GB storage
- **DynamoDB**: 25GB storage
- **API Gateway**: 1M requests/month

Stay within these limits to avoid charges!

## Support

For detailed instructions, see:
- `IMPLEMENTATION_GUIDE.md` - Step-by-step setup
- `SETUP_CONFIG.md` - Configuration values to update
- `architecture-diagram.md` - Understand the system

Good luck with your project! 🚀




