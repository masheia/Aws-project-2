# 🎓 Face Recognition Attendance System - AWS Serverless Project

<div align="center">

![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Serverless](https://img.shields.io/badge/Serverless-FD5750?style=for-the-badge&logo=serverless&logoColor=white)

**An automated attendance tracking system using Amazon Rekognition AI to identify students from photos**

[Live Demo](http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com) • [Documentation](#-documentation) • [Architecture](#-system-architecture)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [AWS Services Used](#-aws-services-used)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Cost Analysis](#-cost-analysis)
- [Security & Privacy](#-security--privacy)
- [Challenges & Solutions](#-challenges--solutions)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **Face Recognition Attendance System** is a fully serverless, cloud-based solution that automates student attendance tracking using Amazon Rekognition's facial recognition technology. Students can mark their own attendance by uploading a photo through the web interface, and the system automatically identifies them and records their attendance in real-time. Administrators manage the system through AWS Console (DynamoDB, CloudWatch, IAM) for secure, direct data control and system monitoring.

### Problem Statement

Traditional attendance systems face several challenges:
- ⏱️ **Time-consuming**: Manual attendance takes 5-10 minutes per class
- ❌ **Error-prone**: Human errors in recording attendance
- 📝 **Inefficient**: Teachers waste valuable class time on administrative tasks
- 📊 **Difficult to track**: Maintaining accurate historical records is challenging

### Our Solution

- ⚡ **Fast**: Attendance recorded in 30 seconds
- 🎯 **Accurate**: AI-powered face recognition with 85%+ accuracy
- 🤖 **Automated**: Zero manual data entry required
- ☁️ **Scalable**: Serverless architecture handles any class size
- 💰 **Cost-effective**: Built entirely on AWS Free Tier

---

## ✨ Features

### 🔐 User Authentication
- **Student Profile**: Sign up with student ID, name, and face photo
- **Student Login**: Secure login to mark attendance and view records
- **Admin Access**: Admins manage the system through AWS Console (DynamoDB, CloudWatch, IAM)
- **Session Management**: Secure login/logout for students

### 👤 Face Registration
- Upload student photos with their information
- Automatic face detection and indexing using Amazon Rekognition
- Face data stored securely in Rekognition Face Collection
- Support for multiple faces per student (optional)

### 📸 Attendance Marking (Student Web Interface)
- **Student Self-Attendance**: Students upload their own photo to mark attendance
- Automatic face recognition and verification
- Real-time processing with confidence scores
- Automatic timestamp and date recording
- Secure verification ensures only registered students can mark attendance

### 🔧 Administrative Management (AWS Console)
- **Direct Database Access**: Admins manage all data through DynamoDB Console
- **System Monitoring**: CloudWatch logs for troubleshooting and monitoring
- **Face Management**: Re-register faces, manage Rekognition collections
- **Data Management**: Add/remove students, fix attendance records, bulk operations
- **IAM Security**: Role-based access control for admin operations

### 📊 Attendance Dashboard (Students)
- View your own attendance records
- Filter by date
- View confidence scores for each recognition
- See attendance history and timestamps

### 🔧 Admin Management (AWS Console)
- **DynamoDB Console**: Direct access to all attendance records and student data
- **CloudWatch Logs**: Monitor system activity and troubleshoot issues
- **IAM Access**: Secure role-based access control
- **Lambda Functions**: Direct management and monitoring
- **S3 Bucket**: Manage uploaded images and face photos
- **Direct Data Management**: Add/remove students, fix incorrect attendance, re-register faces

### 🔔 Notifications
- Email/SMS notifications when attendance is recorded
- Configurable notification settings
- Daily attendance summaries

### 📱 Mobile-Friendly
- Responsive web design works on all devices
- Touch-friendly interface
- Optimized for mobile browsers

---

## 🛠️ Tech Stack

### Frontend
- **HTML5/CSS3**: Modern, responsive user interface
- **JavaScript (ES6+)**: Interactive frontend logic
- **Bootstrap/Modern CSS**: Beautiful gradient styling
- **File Upload API**: Native file handling for photos

### Backend (Serverless)
- **AWS Lambda**: Serverless compute (Python 3.11)
- **Amazon API Gateway**: RESTful API endpoints
- **AWS IAM**: Secure access control and permissions

### AI/ML
- **Amazon Rekognition**: Face detection and recognition
- **Face Collection**: Stores registered student faces
- **Confidence Scoring**: Measures recognition accuracy (85%+ threshold)

### Database
- **Amazon DynamoDB**: NoSQL database
  - `Students` table: Student information and face metadata
  - `AttendanceRecords` table: All attendance data with timestamps

### Storage
- **Amazon S3**: Object storage for
  - Student registration photos
  - Attendance photos
  - Frontend website files (static hosting)

### Notifications
- **Amazon SNS**: Email/SMS notifications

### Infrastructure
- **Amazon CloudFront**: Content Delivery Network (CDN) for global access
- **AWS CloudWatch**: Logging and monitoring

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Login     │  │  Sign Up    │  │  Dashboard  │        │
│  │   Page      │  │   Page      │  │   Page      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTPS
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Amazon CloudFront                        │
│              (CDN for global content delivery)              │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                  Amazon S3 (Static Hosting)                 │
│              Frontend: HTML, CSS, JavaScript                │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API Calls
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                   Amazon API Gateway                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ POST /upload │  │ POST /register│ │ GET /attendance│    │
│  │              │  │   -face      │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────────┬─────────────────────────────────┘
                            │ Triggers
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    AWS Lambda Functions                     │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ ProcessAttendance│  │  RegisterFace    │               │
│  │                  │  │                  │               │
│  │ - Process photos │  │ - Index faces    │               │
│  │ - Search faces   │  │ - Store metadata │               │
│  │ - Record attend. │  │                  │               │
│  └──────────────────┘  └──────────────────┘               │
│  ┌──────────────────┐                                      │
│  │  GetAttendance   │                                      │
│  │                  │                                      │
│  │ - Query records  │                                      │
│  │ - Filter data    │                                      │
│  └──────────────────┘                                      │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌───────▼────────┐  ┌──────▼───────────┐
│  Amazon S3     │  │  Amazon        │  │  Amazon          │
│  (Images)      │  │  Rekognition   │  │  DynamoDB        │
│                │  │                │  │                  │
│ - Student      │  │ - Face         │  │ - Students Table │
│   photos       │  │   Collection   │  │ - Attendance     │
│ - Attendance   │  │ - Face         │  │   Records Table  │
│   photos       │  │   Detection    │  │                  │
│                │  │ - Face         │  │                  │
│                │  │   Matching     │  │                  │
└────────────────┘  └────────────────┘  └────────┬─────────┘
                                                  │
                                         ┌────────▼─────────┐
                                         │   Amazon SNS     │
                                         │                  │
                                         │ - Notifications  │
                                         │ - Email/SMS      │
                                         └──────────────────┘
```

### Data Flow

#### Student Registration Flow:
1. User uploads student photo via web interface
2. Image sent to API Gateway → Lambda (`RegisterFace`)
3. Image stored in S3 bucket
4. Face detected and indexed in Rekognition Face Collection
5. Student metadata (ID, name, face details) saved to DynamoDB `Students` table

#### Attendance Marking Flow:
1. User uploads attendance photo via web interface
2. Image sent to API Gateway → Lambda (`ProcessAttendance`)
3. Image stored in S3 bucket
4. Rekognition searches Face Collection for matches
5. For each match found:
   - Student identified with confidence score
   - Attendance record created in DynamoDB `AttendanceRecords` table
   - Notification sent via SNS (optional)

#### Attendance Retrieval Flow:
1. User requests attendance records via web interface
2. Request sent to API Gateway → Lambda (`GetAttendance`)
3. Lambda queries DynamoDB based on filters (date, student ID, class)
4. Results returned to frontend
5. Frontend displays attendance dashboard

---

## ☁️ AWS Services Used

This project utilizes **7+ AWS services** to create a fully serverless, scalable solution:

| Service | Purpose | Free Tier Limit |
|---------|---------|-----------------|
| **Amazon S3** | Image storage and static website hosting | 5 GB storage, 20,000 GET requests |
| **Amazon Rekognition** | Face detection and recognition AI | 5,000 images/month |
| **AWS Lambda** | Serverless compute for processing | 1M requests/month, 400,000 GB-seconds |
| **Amazon DynamoDB** | NoSQL database for attendance records | 25 GB storage, 25 read/write units |
| **Amazon API Gateway** | REST API endpoints | 1M requests/month |
| **Amazon SNS** | Email/SMS notifications | 1M requests/month |
| **Amazon CloudFront** | CDN for global content delivery | 50 GB data transfer |
| **AWS IAM** | Access control and security | Free |

### Service Details

#### Amazon S3
- **Purpose**: Store student photos, attendance photos, and host static website
- **Buckets**:
  - `attendance-images-1765405751`: Student and attendance photos
  - `attendance-frontend-1765405751`: Frontend website files

#### Amazon Rekognition
- **Purpose**: Face detection and recognition
- **Face Collection**: `attendance-students`
- **Features Used**:
  - `IndexFaces`: Index student faces during registration
  - `SearchFacesByImage`: Search for faces in attendance photos
  - Confidence threshold: 85%

#### AWS Lambda
- **Runtime**: Python 3.11
- **Functions**:
  - `ProcessAttendance`: Processes attendance photos
  - `RegisterFace`: Registers new student faces
  - `GetAttendance`: Retrieves attendance records
- **Memory**: 512 MB
- **Timeout**: 30 seconds

#### Amazon DynamoDB
- **Tables**:
  - `Students`: Stores student information
    - Primary Key: `FaceId` (from Rekognition)
    - GSI: `StudentId-index`
  - `AttendanceRecords`: Stores attendance data
    - Primary Key: `AttendanceId` (UUID)
    - GSI: `Date-index`, `StudentId-Date-index`

#### Amazon API Gateway
- **Base URL**: `https://pjjf6u13f8.execute-api.us-east-1.amazonaws.com/prod`
- **Endpoints**:
  - `POST /upload` → ProcessAttendance Lambda
  - `POST /register-face` → RegisterFace Lambda
  - `GET /attendance` → GetAttendance Lambda
- **CORS**: Enabled for frontend access

---

## 🚀 Installation & Setup

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured with credentials
- Python 3.11+ installed
- Git installed

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Aws-project-2.git
   cd Aws-project-2
   ```

2. **Configure AWS credentials**
   ```bash
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, region (e.g., `us-east-1`), and output format (e.g., `json`).

3. **Deploy AWS Infrastructure**
   ```bash
   python deploy.py
   ```
   This will create:
   - S3 buckets for images and frontend
   - DynamoDB tables
   - Rekognition face collection
   - SNS topic

4. **Deploy Lambda Functions**
   ```bash
   python deploy_lambda.py
   ```
   This will:
   - Package Lambda functions
   - Deploy to AWS Lambda
   - Set up API Gateway
   - Configure IAM roles and permissions

5. **Update Frontend API Endpoint**
   - After Lambda deployment, copy the API Gateway URL
   - Update `frontend/script.js` with the new API endpoint:
   ```javascript
   const API_ENDPOINT = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod';
   ```

6. **Deploy Frontend**
   ```bash
   aws s3 sync frontend/ s3://attendance-frontend-1765405751 --region us-east-1
   ```

7. **Access the Application**
   - Open: `http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com`
   - Or use CloudFront URL: `https://d3d3y3hf5su68f.cloudfront.net`

### Detailed Setup Instructions

For detailed step-by-step instructions, see:
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) - Complete manual setup guide
- [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md) - Infrastructure deployment details
- [LAMBDA_DEPLOYMENT_GUIDE.md](./LAMBDA_DEPLOYMENT_GUIDE.md) - Lambda function deployment

---

## 📖 Usage

### For Students (Web Interface)

1. **Sign Up**
   - Go to the Sign Up page
   - Enter your Student ID and Name
   - Upload a clear photo of your face
   - Create a password
   - Click "Create Account"

2. **Mark Attendance**
   - Log in with your Student ID and password
   - Go to "Mark My Attendance" tab
   - Select the date
   - Upload your photo (file upload)
   - Click "Process Attendance"
   - System verifies your face and records your attendance automatically

3. **View Attendance History**
   - Go to "Attendance History" tab
   - View all your attendance records
   - Filter by date if needed
   - See confidence scores and timestamps

### For Administrators (AWS Console)

Admins manage the system through AWS Console for better security and direct data control.

#### Accessing AWS Console

1. **Log in to AWS Console**
   - Go to: https://console.aws.amazon.com/
   - Use admin IAM credentials

2. **Manage Students (DynamoDB)**
   - Navigate to: **DynamoDB Console** → Tables → `Students`
   - **View all students**: Browse all registered student records
   - **Add student**: Insert new student record with FaceId, StudentId, StudentName
   - **Remove student**: Delete student records
   - **Update student**: Modify student information

3. **Manage Attendance Records (DynamoDB)**
   - Navigate to: **DynamoDB Console** → Tables → `AttendanceRecords`
   - **View all attendance**: See all attendance records across all students
   - **Filter records**: Use DynamoDB query/scan with filters
   - **Fix incorrect attendance**: Delete or modify incorrect records
   - **Export data**: Use DynamoDB export feature or query via AWS CLI

4. **Monitor System (CloudWatch)**
   - Navigate to: **CloudWatch** → Logs → Log groups
   - **View Lambda logs**: Monitor `ProcessAttendance`, `RegisterFace`, `GetAttendance` logs
   - **Troubleshoot issues**: Check error logs and debug problems
   - **Monitor performance**: Track execution times and success rates

5. **Manage Face Recognition (Rekognition)**
   - Navigate to: **Amazon Rekognition Console** → Face collections
   - **View face collection**: Check `attendance-students` collection
   - **Re-register faces**: Remove and re-index faces if needed
   - **Verify face indexing**: Ensure faces are properly indexed

6. **Manage Images (S3)**
   - Navigate to: **S3 Console** → `attendance-images-1765405751`
   - **View uploaded photos**: Browse student photos and attendance photos
   - **Delete images**: Remove old or incorrect images
   - **Organize folders**: Manage folder structure

7. **Manage Lambda Functions**
   - Navigate to: **Lambda Console**
   - **Update functions**: Modify code or configuration
   - **View metrics**: Monitor invocation counts, errors, duration
   - **Test functions**: Manually trigger functions for testing

#### Common Admin Tasks

- **Add Student Manually**: Insert record in DynamoDB `Students` table
- **Fix Attendance Error**: Delete incorrect record from `AttendanceRecords` table
- **Re-register Face**: Delete face from Rekognition collection, re-upload via web interface
- **Review Logs**: Check CloudWatch logs for system issues
- **Monitor Usage**: Track AWS service usage in Cost Explorer

#### Benefits of Console-Based Admin Access

- ✅ **Better Security**: IAM role-based access control
- ✅ **Direct Data Control**: Full access to all data without UI limitations
- ✅ **Audit Trail**: All changes logged in CloudWatch
- ✅ **Bulk Operations**: Query and modify multiple records at once
- ✅ **System Monitoring**: Real-time monitoring of all AWS services
- ✅ **Troubleshooting**: Direct access to logs and error details

---

## 🔌 API Endpoints

### Base URL
```
https://pjjf6u13f8.execute-api.us-east-1.amazonaws.com/prod
```

### Endpoints

#### 1. Register Face
**POST** `/register-face`

Register a new student's face in the system.

**Request Body:**
```json
{
  "studentId": "STU001",
  "studentName": "John Doe",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response:**
```json
{
  "statusCode": 200,
  "body": {
    "message": "Student registered successfully",
    "faceId": "abc123...",
    "studentId": "STU001"
  }
}
```

#### 2. Process Attendance
**POST** `/upload`

Process an attendance photo and identify students.

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "classId": "CS101",
  "date": "2025-12-10"
}
```

**Response:**
```json
{
  "statusCode": 200,
  "body": {
    "message": "Attendance processed successfully",
    "identifiedStudents": [
      {
        "studentId": "STU001",
        "studentName": "John Doe",
        "confidence": 95.5
      }
    ],
    "totalIdentified": 1
  }
}
```

#### 3. Get Attendance
**GET** `/attendance?date=2025-12-10&studentId=STU001&classId=CS101`

Retrieve attendance records with optional filters.

**Query Parameters:**
- `date` (optional): Filter by date (YYYY-MM-DD)
- `studentId` (optional): Filter by student ID
- `classId` (optional): Filter by class ID

**Response:**
```json
{
  "statusCode": 200,
  "body": {
    "records": [
      {
        "attendanceId": "uuid-here",
        "studentId": "STU001",
        "studentName": "John Doe",
        "classId": "CS101",
        "date": "2025-12-10",
        "timestamp": "2025-12-10T10:30:00Z",
        "confidence": 95.5
      }
    ],
    "total": 1
  }
}
```

---

## 📁 Project Structure

```
Aws-project-2/
│
├── README.md                          # This file
├── architecture-diagram.md            # Detailed architecture documentation
├── IMPLEMENTATION_GUIDE.md            # Step-by-step setup guide
├── PRESENTATION_OUTLINE.md            # Presentation structure
├── PROJECT_OVERVIEW.md                # Project overview and details
├── FINAL_DEPLOYMENT_STATUS.md         # Deployment status and URLs
│
├── lambda-functions/                  # AWS Lambda functions
│   ├── process-attendance/
│   │   ├── lambda_function.py        # Process attendance photos
│   │   └── requirements.txt          # Python dependencies
│   ├── manage-faces/
│   │   ├── lambda_function.py        # Register student faces
│   │   └── requirements.txt          # Python dependencies
│   └── get-attendance/
│       ├── lambda_function.py        # Retrieve attendance records
│       └── requirements.txt          # Python dependencies
│
├── frontend/                          # Web application frontend
│   ├── index.html                    # Main dashboard page
│   ├── login.html                    # Login page
│   ├── signup.html                   # Sign up page
│   ├── styles.css                    # Styling
│   └── script.js                     # Frontend logic and API calls
│
├── dynamodb-tables/                   # Database schema
│   └── table-definitions.json        # DynamoDB table definitions
│
├── deploy.py                          # Infrastructure deployment script
├── deploy_lambda.py                   # Lambda deployment script
├── setup_cloudfront.py                # CloudFront setup script
├── setup_cognito.py                   # Cognito setup script (optional)
│
└── Documentation/                     # Additional documentation
    ├── DEPLOYMENT_SUMMARY.md
    ├── LAMBDA_DEPLOYMENT_GUIDE.md
    ├── WEBSITE_URLS.md
    └── ...
```

---

## 💰 Cost Analysis

### AWS Free Tier (First 12 Months)

| Service | Free Tier | Estimated Usage | Cost |
|---------|-----------|-----------------|------|
| Amazon S3 | 5 GB storage, 20K GET requests | ~1 GB storage, 5K requests | **$0** |
| Amazon Rekognition | 5,000 images/month | ~500 images/month | **$0** |
| AWS Lambda | 1M requests, 400K GB-seconds | ~10K requests/month | **$0** |
| Amazon DynamoDB | 25 GB storage, 25 units | ~1 GB, 10 units | **$0** |
| API Gateway | 1M requests/month | ~10K requests/month | **$0** |
| Amazon SNS | 1M requests/month | ~500 requests/month | **$0** |
| CloudFront | 50 GB data transfer | ~5 GB/month | **$0** |

**Total Monthly Cost: $0** (within free tier limits)

### Production Cost Estimate

For a production deployment with moderate usage (1,000 students, 100 classes/month):

| Service | Usage | Estimated Cost |
|---------|-------|----------------|
| S3 Storage | 10 GB | ~$0.23/month |
| S3 Requests | 50K requests | ~$0.01/month |
| Rekognition | 10K images | ~$1.00/month |
| Lambda | 50K requests | ~$0.01/month |
| DynamoDB | 10 GB, 100 units | ~$2.50/month |
| API Gateway | 50K requests | ~$1.50/month |
| CloudFront | 50 GB transfer | ~$4.50/month |
| **Total** | | **~$9.75/month** |

---

## 🔒 Security & Privacy

### Security Measures

- **Encryption at Rest**: All data stored in S3 and DynamoDB is encrypted
- **Encryption in Transit**: All API calls use HTTPS/TLS
- **IAM Roles**: Least privilege access for Lambda functions
- **Private S3 Buckets**: Images stored in private buckets (not publicly accessible)
- **Secure API Gateway**: API keys and authentication (can be enhanced)
- **CloudFront Security**: DDoS protection and AWS Shield Standard

### Privacy Considerations

- **Face Data**: Stored securely in Rekognition Face Collection (not publicly accessible)
- **Student Information**: Encrypted in DynamoDB
- **Access Control**: Role-based access (Students see only their data, Admins see all)
- **No Third-Party Sharing**: All data stays within your AWS account

### Best Practices Implemented

- ✅ Secure credential management (no hardcoded secrets)
- ✅ CORS configured for API Gateway
- ✅ Input validation in Lambda functions
- ✅ Error handling and logging
- ✅ Regular security updates

---

## 🐛 Challenges & Solutions

### Challenge 1: DynamoDB Decimal Type Serialization
**Problem**: DynamoDB returns `Decimal` types that cannot be serialized to JSON directly.

**Solution**: Created custom `DecimalEncoder` class to convert `Decimal` to `float` during JSON serialization.

```python
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
```

### Challenge 2: Rekognition ExternalImageId Format
**Problem**: Rekognition `ExternalImageId` doesn't accept spaces or special characters.

**Solution**: Implemented `sanitize_student_id()` function to clean student IDs before indexing.

```python
def sanitize_student_id(student_id):
    """Replace invalid characters with underscores"""
    return re.sub(r'[^a-zA-Z0-9_.\-:]', '_', student_id)
```

### Challenge 3: S3 Public Access Configuration
**Problem**: S3 Block Public Access settings prevented public website hosting.

**Solution**: Programmatically disabled Block Public Access and applied public read policy for frontend bucket only.

### Challenge 4: CloudFront 404 Errors
**Problem**: CloudFront distribution returning 404 for S3 website endpoint.

**Solution**: Updated CloudFront configuration to use S3 website endpoint with correct `OriginProtocolPolicy`.

### Challenge 5: IAM Role Propagation
**Problem**: Lambda functions failing due to IAM role not being fully propagated.

**Solution**: Added `time.sleep(10)` after role creation and used waiter for Lambda function updates.

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **Multi-factor Authentication**: Add 2FA for enhanced security
- [ ] **Real-time Notifications**: WebSocket support for live updates
- [ ] **Attendance Reports**: Generate PDF/Excel reports
- [ ] **Class Management**: Create and manage multiple classes
- [ ] **Student Dashboard**: Detailed attendance analytics for students
- [ ] **Admin Analytics**: Comprehensive attendance statistics and trends
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Batch Processing**: Process multiple photos at once
- [ ] **Face Verification**: Two-factor verification for critical attendance
- [ ] **Integration**: Integration with learning management systems (LMS)

### Technical Improvements

- [ ] **AWS Cognito**: Full authentication service integration
- [ ] **API Caching**: Implement API Gateway caching for better performance
- [ ] **Lambda Layers**: Extract common dependencies to Lambda layers
- [ ] **Auto-scaling**: Configure DynamoDB auto-scaling
- [ ] **Monitoring**: Enhanced CloudWatch dashboards and alarms
- [ ] **Testing**: Unit tests and integration tests
- [ ] **CI/CD**: Automated deployment pipeline with GitHub Actions
- [ ] **Infrastructure as Code**: Convert to AWS CDK or Terraform

---

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow the existing code style
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly
- Ensure all tests pass

---

## 📝 License

This project is created for educational purposes. Feel free to use and modify as needed.

**Educational Project** - Not for commercial use without proper licensing.

---

## 👨‍💻 Authors

- **Your Name** - *Initial work* - [GitHub Profile](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Amazon Web Services for providing excellent cloud services
- Amazon Rekognition team for powerful facial recognition capabilities
- AWS Free Tier for making this project affordable
- Open source community for inspiration and tools

---

## 📚 Additional Documentation

- [Architecture Diagram](./architecture-diagram.md) - Detailed system architecture
- [Implementation Guide](./IMPLEMENTATION_GUIDE.md) - Step-by-step setup instructions
- [Presentation Outline](./PRESENTATION_OUTLINE.md) - Project presentation structure
- [Deployment Status](./FINAL_DEPLOYMENT_STATUS.md) - Current deployment details
- [API Documentation](./LAMBDA_DEPLOYMENT_GUIDE.md) - API endpoint details

---

## 🔗 Quick Links

- **Live Website**: http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com
- **CloudFront URL**: https://d3d3y3hf5su68f.cloudfront.net
- **AWS Console**: https://console.aws.amazon.com/
- **API Gateway**: https://pjjf6u13f8.execute-api.us-east-1.amazonaws.com/prod

---

<div align="center">

**Built with ❤️ using AWS Serverless Technologies**

⭐ **Star this repo if you find it helpful!** ⭐

[Report Bug](https://github.com/YOUR_USERNAME/Aws-project-2/issues) · [Request Feature](https://github.com/YOUR_USERNAME/Aws-project-2/issues) · [Documentation](./IMPLEMENTATION_GUIDE.md)

</div>
