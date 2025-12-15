# 🔍 How to Access Amazon Rekognition Face Collections

## Quick Access Link

**Direct Link to Face Collections:**
https://console.aws.amazon.com/rekognition/home?region=us-east-1#/collections

Or follow these steps:

---

## Step-by-Step Guide

### Method 1: Direct Navigation

1. **Go to AWS Console**
   - Visit: https://console.aws.amazon.com/
   - Make sure you're in the correct region: **us-east-1** (N. Virginia)

2. **Open Amazon Rekognition**
   - In the search bar at the top, type: **"Rekognition"**
   - Click on **"Amazon Rekognition"** service

3. **Navigate to Face Collections**
   - In the left sidebar, look for **"Face collections"** or **"Collections"**
   - Click on it

4. **View Your Collection**
   - You should see: **`attendance-students`** collection
   - Click on it to view details

---

### Method 2: From Rekognition Dashboard

1. **Go to Rekognition Console**
   - Visit: https://console.aws.amazon.com/rekognition/home?region=us-east-1

2. **Look in the Left Sidebar**
   - Scroll down past "Demos" section
   - Find **"Face collections"** or **"Face indexing"**
   - Click on it

3. **View Collections**
   - You'll see all face collections
   - Find **`attendance-students`**

---

## Your Face Collection Details

**Collection ID:** `attendance-students`

**Location:**
- **Region:** us-east-1 (N. Virginia)
- **Service:** Amazon Rekognition
- **Feature:** Face Collections

---

## What You Can Do in Face Collections

### View Collection
- See collection ID and creation date
- View number of faces indexed

### View Indexed Faces
- Click on the collection name
- See list of all indexed faces
- View face IDs and external image IDs (student IDs)

### Search Faces
- Use the search feature to find specific faces
- Search by external image ID (student ID)

### Delete Collection (if needed)
- Delete individual faces
- Delete entire collection

---

## If You Can't Find Face Collections

The interface might be different. Try:

1. **Search in Rekognition Console**
   - Use the search bar in the Rekognition console
   - Search for: "collections" or "face collections"

2. **Check All Menu Items**
   - Look through all items in the left sidebar
   - Check for: "Collections", "Face indexing", "Face search", "Face collections"

3. **Use AWS CLI**
   ```bash
   aws rekognition list-collections --region us-east-1
   ```
   
   This will list all collections including `attendance-students`

4. **Check Collection via CLI**
   ```bash
   aws rekognition describe-collection \
       --collection-id attendance-students \
       --region us-east-1
   ```

5. **List Faces in Collection**
   ```bash
   aws rekognition list-faces \
       --collection-id attendance-students \
       --region us-east-1
   ```

---

## Quick Verification

To verify your collection exists and has faces:

```bash
# List all collections
aws rekognition list-collections --region us-east-1

# Describe your collection
aws rekognition describe-collection \
    --collection-id attendance-students \
    --region us-east-1

# List faces in collection (shows all registered students)
aws rekognition list-faces \
    --collection-id attendance-students \
    --region us-east-1 \
    --max-results 10
```

---

## Alternative: Access via AWS CLI

If you prefer command line:

```bash
# List collections
aws rekognition list-collections --region us-east-1

# Describe collection details
aws rekognition describe-collection \
    --collection-id attendance-students \
    --region us-east-1

# List all faces (students) in collection
aws rekognition list-faces \
    --collection-id attendance-students \
    --region us-east-1

# Search for specific student face
aws rekognition search-faces \
    --collection-id attendance-students \
    --face-id <FACE_ID> \
    --region us-east-1
```

---

## Collection Information

**Your Collection:**
- **ID:** `attendance-students`
- **Created:** When you deployed the system
- **Faces:** Number of registered students
- **Status:** Active

---

## Need Help?

If you still can't find it:

1. **Check Region**
   - Make sure you're in **us-east-1** region
   - Collection is region-specific

2. **Check Permissions**
   - Ensure your IAM user/role has Rekognition permissions
   - Need: `rekognition:DescribeCollection`, `rekognition:ListFaces`

3. **Check via API**
   - Use the AWS CLI commands above
   - Or use the Rekognition API directly

---

## Direct Console Links

- **Rekognition Dashboard:** https://console.aws.amazon.com/rekognition/home?region=us-east-1
- **Face Collections (if available):** https://console.aws.amazon.com/rekognition/home?region=us-east-1#/collections
- **All Rekognition Services:** https://console.aws.amazon.com/rekognition/

