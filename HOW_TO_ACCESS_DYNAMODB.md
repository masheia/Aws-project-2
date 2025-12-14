# How to Access Your DynamoDB Tables and Data

## 🔗 Quick Access Links

### **DynamoDB Console** (Main Dashboard)
**https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#tables**

### **Your Tables Direct Links:**
- **Students Table**: https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=Students&tab=items
- **AttendanceRecords Table**: https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=AttendanceRecords&tab=items

---

## 📋 Step-by-Step Guide

### Method 1: Using AWS Console (Easiest)

#### Step 1: Log Into AWS Console
1. Go to: https://console.aws.amazon.com/
2. Sign in with your AWS credentials
3. Make sure you're in region: **us-east-1** (check top-right corner)

#### Step 2: Open DynamoDB
1. In the search bar at the top, type: **"DynamoDB"**
2. Click on **"DynamoDB"** service
3. Or use direct link: https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1

#### Step 3: View Your Tables
1. In the left sidebar, click **"Tables"**
2. You'll see your two tables:
   - ✅ **Students** - Stores registered student information
   - ✅ **AttendanceRecords** - Stores attendance records

#### Step 4: View Data in a Table
1. **Click on a table name** (e.g., "Students")
2. Click the **"Explore table items"** tab (or "Items" tab)
3. You'll see all the data stored in that table!

---

## 📊 Your Tables

### **1. Students Table**
**Purpose**: Stores registered student information

**Structure:**
- **Partition Key**: `FaceId` (String)
- **Attributes**:
  - `FaceId` - Unique face ID from Rekognition
  - `StudentId` - Student ID you entered
  - `Name` - Student name
  - `ImageS3Key` - S3 location of student photo
  - `RegisteredDate` - When student was registered
  - `FaceDetails` - Face detection details (confidence, bounding box)

**How to View:**
1. Go to: https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=Students&tab=items
2. Click on **"Items"** tab
3. You'll see all registered students!

---

### **2. AttendanceRecords Table**
**Purpose**: Stores attendance records

**Structure:**
- **Partition Key**: `AttendanceId` (String)
- **Attributes**:
  - `AttendanceId` - Unique attendance record ID
  - `StudentId` - Student ID
  - `StudentName` - Student name
  - `ClassId` - Class identifier
  - `Date` - Attendance date
  - `Timestamp` - When attendance was recorded
  - `Confidence` - Face recognition confidence score
  - `ImageS3Key` - S3 location of attendance photo
  - `Status` - Usually "Present"

**How to View:**
1. Go to: https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=AttendanceRecords&tab=items
2. Click on **"Items"** tab
3. You'll see all attendance records!

---

## 🔍 Viewing Data in Console

### View All Items:
1. Click on a table
2. Click **"Explore table items"** or **"Items"** tab
3. All items will be displayed in a table format

### Search/Filter Items:
1. In the Items view, use the **search bar** at the top
2. You can filter by any attribute
3. Click **"Filter items"** for advanced filtering

### View Item Details:
1. Click on any item in the list
2. You'll see all attributes and their values
3. You can edit or delete items from here

---

## 💻 Method 2: Using AWS CLI (Command Line)

### List All Tables:
```bash
aws dynamodb list-tables --region us-east-1
```

### View All Items in Students Table:
```bash
aws dynamodb scan --table-name Students --region us-east-1
```

### View All Items in AttendanceRecords Table:
```bash
aws dynamodb scan --table-name AttendanceRecords --region us-east-1
```

### Query by Student ID:
```bash
aws dynamodb query \
  --table-name Students \
  --index-name StudentId-index \
  --key-condition-expression "StudentId = :sid" \
  --expression-attribute-values '{":sid":{"S":"123d"}}' \
  --region us-east-1
```

### Query Attendance by Date:
```bash
aws dynamodb query \
  --table-name AttendanceRecords \
  --index-name Date-index \
  --key-condition-expression "#dt = :dt" \
  --expression-attribute-names '{"#dt":"Date"}' \
  --expression-attribute-values '{":dt":{"S":"2025-12-11"}}' \
  --region us-east-1
```

---

## 📊 Understanding the Data

### Students Table Example:
```json
{
  "FaceId": "abc123-face-id",
  "StudentId": "123d",
  "Name": "masheia",
  "ImageS3Key": "students/123d/20251210123456.jpg",
  "RegisteredDate": "2025-12-10T12:34:56.789Z",
  "FaceDetails": {
    "Confidence": "99.5",
    "BoundingBox": {
      "Width": "0.2",
      "Height": "0.3",
      "Left": "0.4",
      "Top": "0.1"
    }
  }
}
```

### AttendanceRecords Table Example:
```json
{
  "AttendanceId": "123d_2025-12-11_20251211120000",
  "StudentId": "123d",
  "StudentName": "masheia",
  "ClassId": "CS101",
  "Date": "2025-12-11",
  "Timestamp": "2025-12-11T12:00:00.000Z",
  "Confidence": 95.5,
  "ImageS3Key": "attendance/2025-12-11/20251211120000.jpg",
  "Status": "Present"
}
```

---

## 🎯 Quick Actions in Console

### Add Item Manually:
1. Click on table → **"Items"** tab
2. Click **"Create item"** button
3. Add attributes and values
4. Click **"Create item"**

### Edit Item:
1. Click on an item in the list
2. Click **"Edit item"**
3. Modify values
4. Click **"Save changes"**

### Delete Item:
1. Click on an item
2. Click **"Delete"** button
3. Confirm deletion

### Export Data:
1. Click on table
2. Go to **"Actions"** → **"Export to CSV"**
3. Download the CSV file

---

## 📈 View Table Statistics

### Table Metrics:
1. Click on a table
2. Click **"Metrics"** tab
3. See:
   - Read/Write capacity
   - Item count
   - Table size
   - Request metrics

### Table Details:
1. Click on a table
2. Click **"Additional info"** tab
3. See:
   - Table ARN
   - Creation date
   - Status
   - Indexes

---

## 🔍 Useful Queries

### Find Student by ID:
1. Go to Students table
2. Click **"Items"** tab
3. Use filter: `StudentId = "123d"`

### Find Attendance for Today:
1. Go to AttendanceRecords table
2. Click **"Items"** tab
3. Use filter: `Date = "2025-12-11"` (today's date)

### Find All Attendance for a Student:
1. Go to AttendanceRecords table
2. Click **"Items"** tab
3. Use filter: `StudentId = "123d"`

---

## 💡 Tips

1. **Refresh Data**: Click the refresh button to see latest data
2. **Sort Columns**: Click column headers to sort
3. **Pagination**: Use page controls if you have many items
4. **Search**: Use the search bar to quickly find items
5. **Export**: Export data to CSV for analysis

---

## 🚀 Quick Start

**Right now, do this:**

1. **Click this link**: https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#tables
2. **Click on "Students"** table
3. **Click "Items"** tab
4. **You'll see all registered students!**

Then:
1. **Click on "AttendanceRecords"** table
2. **Click "Items"** tab
3. **You'll see all attendance records!**

---

## 📝 Summary

- **Console Access**: Use the links above or search "DynamoDB" in AWS Console
- **Your Tables**: Students and AttendanceRecords
- **View Data**: Click table → "Items" tab
- **Region**: Make sure you're in **us-east-1**

**Everything is stored in your AWS account and accessible through the console!** 🎉



