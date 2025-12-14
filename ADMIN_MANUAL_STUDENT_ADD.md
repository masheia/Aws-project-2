# Admin Guide: Manually Adding Students

When admins manually add students through AWS Console (DynamoDB), they can use this script to ensure proper registration and email notifications.

## Method 1: Using the Admin Script (Recommended)

This script automatically:
- Indexes the face in Rekognition
- Stores the student record in DynamoDB
- Sends a welcome email notification

### Prerequisites

```bash
pip install boto3
```

### Usage

```bash
python admin-add-student.py \
    --student-id "STU001" \
    --name "John Doe" \
    --email "john@example.com" \
    --image-path "student_photo.jpg" \
    --notifications
```

### Parameters

- `--student-id`: Unique student identifier (required)
- `--name`: Student's full name (required)
- `--email`: Student's email address (required)
- `--image-path`: Path to student's face photo (required)
- `--notifications`: Enable email notifications (optional, defaults to True)

### Example

```bash
python admin-add-student.py \
    --student-id "STU123" \
    --name "Jane Smith" \
    --email "jane.smith@university.edu" \
    --image-path "/path/to/jane_photo.jpg"
```

## Method 2: Manual DynamoDB Entry (Advanced)

If you add a student directly through DynamoDB Console, you must:

1. **Add Face to Rekognition First**
   - Use AWS Console → Rekognition → Face collections → `attendance-students`
   - Or use AWS CLI:
     ```bash
     aws rekognition index-faces \
         --collection-id attendance-students \
         --image Bytes=fileb://student_photo.jpg \
         --external-image-id "STU001"
     ```

2. **Add Record to DynamoDB**
   - Go to DynamoDB Console → Tables → `Students`
   - Click "Explore table items" → "Create item"
   - Add these fields:
     - `FaceId`: (from Rekognition response)
     - `StudentId`: Student ID (string)
     - `Name`: Student name (string)
     - `Email`: Student email (string)
     - `EnableNotifications`: true/false (boolean)
     - `ImageS3Key`: S3 path to photo (string)
     - `RegisteredDate`: ISO timestamp (string)
     - `FaceDetails`: Face metadata (map)

3. **Upload Photo to S3**
   - Go to S3 Console → `attendance-images-1765405751`
   - Upload to: `students/{StudentId}/{timestamp}.jpg`

4. **Subscribe Email to SNS (for notifications)**
   ```bash
   aws sns subscribe \
       --topic-arn arn:aws:sns:us-east-1:846863292978:attendance-notifications \
       --protocol email \
       --notification-endpoint "student@example.com"
   ```

5. **Send Welcome Email (Optional)**
   - Use SNS Console to publish a message
   - Or use the script above

## Method 3: Using Lambda Function Directly

You can also invoke the `RegisterFace` Lambda function directly:

```bash
aws lambda invoke \
    --function-name RegisterFace \
    --payload '{
        "body": "{\"studentId\":\"STU001\",\"name\":\"John Doe\",\"email\":\"john@example.com\",\"enableNotifications\":true,\"image\":\"<base64-encoded-image>\"}"
    }' \
    response.json
```

## Email Notification Setup

When a student is added (via script or manually):

1. **Email is automatically subscribed to SNS topic** (`attendance-notifications`)
2. **Student receives a confirmation email** (they must confirm subscription)
3. **Welcome email is sent** after successful registration
4. **Future attendance notifications** will be sent automatically

## Verification

After adding a student, verify:

1. **DynamoDB**: Check `Students` table for the new record
2. **Rekognition**: Check face collection for indexed face
3. **S3**: Verify photo is uploaded
4. **SNS**: Check subscription (student should receive confirmation email)

## Troubleshooting

### Face not detected
- Ensure photo is clear and shows face front-on
- Check photo quality (at least 640x480 recommended)
- Try a different photo

### Email not received
- Check spam folder
- Verify email address is correct
- Check SNS subscription status in AWS Console
- Verify student clicked confirmation link in subscription email

### DynamoDB errors
- Ensure all required fields are present
- Check data types match schema
- Verify IAM permissions for DynamoDB access

