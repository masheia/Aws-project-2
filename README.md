# Face Recognition Attendance System - AWS Project

## Project Overview
A serverless attendance tracking system using Amazon Rekognition to automatically identify students from uploaded photos.

## AWS Services Used
- **Amazon S3 (Simple Storage Service)** - Store uploaded images
- **Amazon Rekognition** - Face detection and recognition
- **AWS Lambda** - Serverless compute for processing
- **Amazon DynamoDB** - NoSQL database for attendance records
- **Amazon SNS** - Notifications
- **API Gateway** - REST API endpoints
- **Amazon CloudFront** (Optional) - CDN for frontend

## Architecture
See `architecture-diagram.md` for detailed architecture.

## Setup Instructions
Follow `IMPLEMENTATION_GUIDE.md` for step-by-step setup.

## Deployment
1. Create S3 buckets
2. Set up DynamoDB tables
3. Deploy Lambda functions
4. Configure API Gateway
5. Set up Rekognition face collection
6. Deploy frontend to S3

## Usage
1. Register students' faces in the system
2. Upload attendance photos
3. System automatically identifies and records attendance
4. View attendance dashboard

## Free Tier Considerations
- Rekognition: First 5,000 images/month free
- Lambda: 1M requests/month free
- S3: 5GB storage free
- DynamoDB: 25GB storage free
- API Gateway: 1M requests/month free

## Project Structure
```
aws-project-face-recognition/
├── README.md
├── architecture-diagram.md
├── IMPLEMENTATION_GUIDE.md
├── PRESENTATION_OUTLINE.md
├── lambda-functions/
│   ├── process-attendance/
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   ├── manage-faces/
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   └── get-attendance/
│       ├── lambda_function.py
│       └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── dynamodb-tables/
    └── table-definitions.json
```

## Authors
[Your Names]

## License
Educational Project




