# 👥 Easy Way to View All Registered Students

## 🎯 Best Method: Use DynamoDB Console

Since Rekognition console doesn't show face collections easily, use DynamoDB instead - it's actually easier!

---

## Step-by-Step: View Students in DynamoDB

### Step 1: Go to DynamoDB Console
**Direct Link:** https://console.aws.amazon.com/dynamodb/home?region=us-east-1

### Step 2: Open Students Table
1. Click **"Tables"** in the left sidebar
2. Find and click on **"Students"** table
3. Click **"Explore table items"** button (or tab)

### Step 3: View All Students
- You'll see a list of all registered students
- Each row shows:
  - **FaceId** - Rekognition face ID
  - **StudentId** - Student ID
  - **Name** - Student full name
  - **Email** - Student email (if provided)
  - **EnableNotifications** - Notification preference
  - **RegisteredDate** - When they registered
  - **ImageS3Key** - Location of their photo in S3

### Step 4: Filter or Search (Optional)
- Use the search/filter box to find specific students
- Filter by Student ID or Name

---

## 📊 What You'll See

Example student record:
```
FaceId: 077f3484-c5f6-4769-a9b8-7bd69323a5d5
StudentId: 2025970817
Name: John Doe
Email: john@example.com
EnableNotifications: true
RegisteredDate: 2025-12-10T10:30:00
ImageS3Key: students/2025970817/20251210103000.jpg
```

---

## 🔍 Alternative: Use AWS CLI

If you prefer command line:

```bash
# View all students
aws dynamodb scan \
    --table-name Students \
    --region us-east-1

# View specific student by ID
aws dynamodb query \
    --table-name Students \
    --index-name StudentId-index \
    --key-condition-expression "StudentId = :sid" \
    --expression-attribute-values '{":sid":{"S":"STU001"}}' \
    --region us-east-1
```

---

## ✅ Why DynamoDB is Better

- ✅ **Easier to access** - Clear UI in console
- ✅ **More information** - Shows all student details
- ✅ **Searchable** - Can filter and search
- ✅ **Complete data** - Everything in one place
- ✅ **No API needed** - Direct console access

---

## 🎯 Quick Access Links

- **DynamoDB Console:** https://console.aws.amazon.com/dynamodb/home?region=us-east-1
- **Students Table:** https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=Students
- **Attendance Records:** https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=AttendanceRecords

---

## 💡 Summary

**To view all registered students:**
1. Go to DynamoDB Console
2. Click "Students" table
3. Click "Explore table items"
4. Done! ✅

This is much easier than trying to find face collections in Rekognition console!

