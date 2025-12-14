# Architecture Diagram - Face Recognition Attendance System

## System Architecture

```
┌─────────────────┐
│   Web Browser   │
│   (Frontend)    │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────────────────────────────────────┐
│           Amazon CloudFront (CDN)               │
│         (Optional - for static assets)          │
└────────┬────────────────────────────────────────┘
         │
         │
┌────────▼────────────────────────────────────────┐
│           Amazon API Gateway                    │
│   - POST /upload                                │
│   - POST /register-face                         │
│   - GET /attendance                             │
└────────┬────────────────────────────────────────┘
         │
         │ Triggers
         │
┌────────▼────────────────────────────────────────┐
│           AWS Lambda Functions                  │
│                                                 │
│  ┌──────────────────────────────────────┐     │
│  │  Process Attendance Lambda           │     │
│  │  - Receives image upload             │     │
│  │  - Stores in S3                      │     │
│  │  - Calls Rekognition                 │     │
│  │  - Saves to DynamoDB                 │     │
│  └──────────┬───────────────────────────┘     │
│             │                                   │
│  ┌──────────▼───────────────────────────┐     │
│  │  Manage Faces Lambda                 │     │
│  │  - Add faces to collection           │     │
│  │  - Delete faces                      │     │
│  └──────────┬───────────────────────────┘     │
│             │                                   │
│  ┌──────────▼───────────────────────────┐     │
│  │  Get Attendance Lambda               │     │
│  │  - Query DynamoDB                    │     │
│  │  - Return attendance records         │     │
│  └──────────────────────────────────────┘     │
└────────┬────────────────────────────────────────┘
         │
         │
    ┌────┴────────────────────────────────────────┐
    │                                              │
┌───▼──────────────────┐    ┌─────────────────────▼───┐
│   Amazon S3          │    │   Amazon Rekognition     │
│                      │    │                          │
│  - attendance-images │    │  - Face Collection       │
│  - student-faces     │    │  - Face Detection        │
│  - frontend-assets   │    │  - Face Comparison       │
└───┬──────────────────┘    └──────────────────────────┘
    │
    │
┌───▼──────────────────┐    ┌─────────────────────▼───┐
│   Amazon DynamoDB    │    │   Amazon SNS             │
│                      │    │                          │
│  - Attendance Table  │    │  - Email Notifications   │
│  - Students Table    │    │  - SMS Alerts            │
│  - Face Metadata     │    │                          │
└──────────────────────┘    └──────────────────────────┘
```

## Data Flow

### 1. Face Registration Flow
```
User → API Gateway → Register Face Lambda → S3 (Store Image) 
                                                ↓
                                        Rekognition (Index Face)
                                                ↓
                                        DynamoDB (Save Metadata)
```

### 2. Attendance Recording Flow
```
User Upload Image → API Gateway → Process Attendance Lambda → S3 (Store)
                                                                   ↓
                                                            Rekognition (Search Faces)
                                                                   ↓
                                                            DynamoDB (Save Attendance)
                                                                   ↓
                                                            SNS (Send Notification)
```

### 3. Attendance Retrieval Flow
```
Dashboard Request → API Gateway → Get Attendance Lambda → DynamoDB (Query)
                                                                   ↓
                                                            Return JSON Data
                                                                   ↓
                                                            Frontend Display
```

## AWS Services Interaction

1. **API Gateway** receives HTTP requests
2. **Lambda** processes requests and coordinates services
3. **S3** stores images (uploaded photos and registered faces)
4. **Rekognition** performs face detection and matching
5. **DynamoDB** stores attendance records and student information
6. **SNS** sends notifications (email/SMS) for attendance confirmations
7. **CloudFront** (optional) serves frontend assets globally

## Security Considerations

- IAM roles for Lambda with least privilege access
- S3 bucket policies for secure image access
- API Gateway authentication (optional API keys)
- Encrypted DynamoDB tables
- HTTPS only communication



