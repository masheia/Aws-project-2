# 📷 Where to Find Uploaded Images

## 🎯 Your Images Bucket

**Bucket Name:** `attendance-images-1765405751`

This is where all uploaded images are stored!

---

## 🔍 How to Access Your Images

### **Option 1: Direct Link to Your Images Bucket**
Click this link to go directly to your images bucket:

**https://console.aws.amazon.com/s3/buckets/attendance-images-1765405751?region=us-east-1&tab=objects**

---

### **Option 2: Manual Navigation**

1. **Go to AWS S3 Console:**
   - https://console.aws.amazon.com/s3/home?region=us-east-1

2. **Find Your Bucket:**
   - Look for: `attendance-images-1765405751`
   - Click on it

3. **View Images:**
   - Click the **"Objects"** tab
   - You'll see folders and images

---

## 📁 Folder Structure

When you upload images, they're organized in folders:

### **1. Student Face Photos**
**Folder:** `students/`

**Contains:**
- Photos uploaded when students sign up
- One photo per student
- Named with student ID

**Example:**
```
students/
  └── 123d.jpg
  └── 456e.jpg
  └── 789f.jpg
```

### **2. Attendance Photos**
**Folder:** `attendance/`

**Contains:**
- Photos uploaded when marking attendance
- Organized by date
- Multiple photos per day

**Example:**
```
attendance/
  └── 2024-01-15/
      └── 20240115143022.jpg
      └── 20240115144530.jpg
  └── 2024-01-16/
      └── 20240116120000.jpg
```

---

## 🖼️ Viewing Images

### **In S3 Console:**
1. Navigate to the folder (e.g., `students/` or `attendance/2024-01-15/`)
2. Click on an image file
3. Click **"Open"** button to view the image
4. Or click **"Download"** to save it

### **Image Details:**
- **Name:** File name (student ID or timestamp)
- **Type:** image/jpeg
- **Size:** File size in KB/MB
- **Last Modified:** When it was uploaded
- **Storage Class:** Standard

---

## 📊 Current Status

### **If Bucket is Empty:**
✅ **This is NORMAL!** The bucket will be empty until you:
1. Sign up new students (photos go to `students/` folder)
2. Mark attendance (photos go to `attendance/` folder)

### **After Using the System:**
- Student signups → Images appear in `students/` folder
- Attendance marking → Images appear in `attendance/` folder

---

## 🔗 Quick Links

### **View Images Bucket:**
**https://console.aws.amazon.com/s3/buckets/attendance-images-1765405751?region=us-east-1&tab=objects**

### **View All S3 Buckets:**
**https://console.aws.amazon.com/s3/home?region=us-east-1**

---

## 📝 How Images Are Uploaded

### **When Students Sign Up:**
1. Student fills signup form
2. Uploads face photo
3. Photo is saved to: `students/{studentId}.jpg`
4. Photo is also indexed in Rekognition for face recognition

### **When Marking Attendance:**
1. Student uploads attendance photo
2. Photo is saved to: `attendance/{date}/{timestamp}.jpg`
3. System searches for faces in the photo
4. Matches faces with registered students
5. Records attendance in DynamoDB

---

## 🎯 Finding Specific Images

### **Find a Student's Photo:**
1. Go to `students/` folder
2. Look for file named with student ID (e.g., `123d.jpg`)

### **Find Attendance Photos:**
1. Go to `attendance/` folder
2. Navigate to date folder (e.g., `2024-01-15/`)
3. See all photos uploaded that day

---

## 💡 Tips

- **Images are automatically organized** by the system
- **You don't need to manually organize** them
- **All images are stored securely** in your S3 bucket
- **Images are used for face recognition** by Rekognition

---

## ✅ Summary

| What | Where |
|------|-------|
| **Images Bucket** | `attendance-images-1765405751` |
| **Student Photos** | `students/` folder |
| **Attendance Photos** | `attendance/{date}/` folders |
| **Direct Link** | [Click Here](https://console.aws.amazon.com/s3/buckets/attendance-images-1765405751?region=us-east-1&tab=objects) |

**Your images will appear here automatically when you use the system!** 🎉



