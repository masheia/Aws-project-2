# How to Access Your AWS Resources

## ✅ Your AWS Account is Already Connected!

**Your AWS Account ID**: `846863292978`  
**Your AWS User**: `MasheiaIAM`  
**Region**: `us-east-1`

**Everything has been deployed to YOUR AWS account!** All resources are live and running in your account right now.

---

## 🔗 Quick Access Links

Click these links to go directly to your resources in AWS Console (make sure you're logged in):

### 🌐 **Live Website** (Access Now!)
**http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com**

This is your working application - try it out!

---

### 📦 **S3 Buckets**
- **S3 Console**: https://console.aws.amazon.com/s3/home?region=us-east-1
- **Your Buckets**:
  - `attendance-images-1765405751` (stores photos)
  - `attendance-frontend-1765405751` (hosts your website)

**To View:**
1. Click the S3 Console link above
2. Look for buckets starting with `attendance-`
3. Click on `attendance-frontend-1765405751` to see your website files

---

### ⚡ **Lambda Functions**
- **Lambda Console**: https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions
- **Your Functions**:
  - `ProcessAttendance`
  - `RegisterFace`
  - `GetAttendance`

**To View:**
1. Click the Lambda Console link above
2. You should see all 3 functions listed
3. Click on any function to see its code and configuration

---

### 🔌 **API Gateway**
- **API Gateway Console**: https://console.aws.amazon.com/apigateway/home?region=us-east-1#/apis
- **Your API**: `face-recognition-attendance-api`
- **API ID**: `pjjf6u13f8`
- **Base URL**: `https://pjjf6u13f8.execute-api.us-east-1.amazonaws.com/prod`

**To View:**
1. Click the API Gateway Console link above
2. Click on `face-recognition-attendance-api`
3. You'll see all endpoints: `/upload`, `/register-face`, `/attendance`

---

### 🗄️ **DynamoDB Tables**
- **DynamoDB Console**: https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#tables
- **Your Tables**:
  - `Students`
  - `AttendanceRecords`

**To View:**
1. Click the DynamoDB Console link above
2. You'll see both tables listed
3. Click on a table to view items and data

---

### 👤 **Amazon Rekognition**
- **Rekognition Console**: https://console.aws.amazon.com/rekognition/home?region=us-east-1#/face-collections
- **Your Collection**: `attendance-students`

**To View:**
1. Click the Rekognition Console link above
2. Go to "Face collections"
3. You'll see `attendance-students` collection

---

### 📧 **Amazon SNS**
- **SNS Console**: https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/topics
- **Your Topic**: `attendance-notifications`

**To View:**
1. Click the SNS Console link above
2. You'll see the `attendance-notifications` topic
3. Click to subscribe your email for notifications

---

## 🔐 How to Log Into AWS Console

If you're not already logged in:

1. **Go to**: https://aws.amazon.com/console/
2. **Click**: "Sign In to the Console"
3. **Enter**: Your AWS account email and password
   - OR use your IAM user credentials
4. **Select**: Your account (Account ID: `846863292978`)

---

## ✅ Verify Everything is Working

### Step 1: Check Your Live Website
1. Open: http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com
2. You should see your Face Recognition Attendance System interface
3. Try registering a student (you'll need a photo)

### Step 2: Check Lambda Functions
1. Go to Lambda Console (link above)
2. Verify you see 3 functions: `ProcessAttendance`, `RegisterFace`, `GetAttendance`
3. Click on one to see the code

### Step 3: Check API Gateway
1. Go to API Gateway Console (link above)
2. Verify API `face-recognition-attendance-api` exists
3. Click on it to see the endpoints

### Step 4: Check DynamoDB
1. Go to DynamoDB Console (link above)
2. Verify tables `Students` and `AttendanceRecords` exist
3. They might be empty until you start using the system

---

## 🧪 Test Your System

### Quick Test:
1. **Open your website**: http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com
2. **Register a Student**:
   - Click "Register Student" tab
   - Enter Student ID: `TEST001`
   - Enter Name: `Test Student`
   - Upload a clear face photo
   - Click "Register Student"
3. **Mark Attendance**:
   - Click "Mark Attendance" tab
   - Select today's date
   - Upload the same photo (or photo with the student)
   - Click "Process Attendance"
4. **View Attendance**:
   - Click "View Attendance" tab
   - You should see the attendance record

---

## 📊 View CloudWatch Logs

If something doesn't work, check the logs:

1. **Go to**: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups
2. **Look for**: `/aws/lambda/ProcessAttendance`, `/aws/lambda/RegisterFace`, `/aws/lambda/GetAttendance`
3. **Click** on a log group to see recent logs

---

## 🔍 Verify Using AWS CLI

If you have AWS CLI installed (which you do), you can verify everything from command line:

```bash
# List S3 buckets
aws s3 ls | findstr attendance

# List Lambda functions
aws lambda list-functions --query "Functions[].FunctionName" --output table

# List DynamoDB tables
aws dynamodb list-tables

# List API Gateways
aws apigateway get-rest-apis --query "items[].{Name:name,Id:id}" --output table
```

---

## ❓ Troubleshooting

### "I can't see my resources"
- Make sure you're logged into the correct AWS account (846863292978)
- Make sure you're in the correct region (us-east-1)
- Check that you have permissions to view these resources

### "The website doesn't work"
- Check API Gateway is deployed to `prod` stage
- Check browser console for errors (F12 → Console)
- Verify frontend is pointing to correct API endpoint

### "Lambda functions don't execute"
- Check CloudWatch Logs for errors
- Verify IAM role has proper permissions
- Check function configuration (timeout, memory)

---

## 📝 Summary

**Your AWS Account**: `846863292978`  
**Everything is deployed and connected!**

**Access Your Live App**: http://attendance-frontend-1765405751.s3-website-us-east-1.amazonaws.com

All resources are in **us-east-1** region.

---

## 🎯 Next Steps

1. **Access your website** and test it
2. **Explore AWS Console** to see all your resources
3. **Register some test students** and mark attendance
4. **Prepare your presentation** using the working system

Everything is ready to go! 🚀




