import json
import boto3
import urllib.parse
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize AWS clients
s3_client = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

# Constants
FACE_COLLECTION_ID = 'attendance-students'
ATTENDANCE_TABLE = 'AttendanceRecords'
STUDENTS_TABLE = 'Students'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:846863292978:attendance-notifications'
S3_BUCKET = 'attendance-images-1765405751'

def lambda_handler(event, context):
    """
    Process attendance image upload and identify students
    """
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # Get image data (base64 encoded)
        image_data = body.get('image')
        class_id = body.get('classId', 'default-class')
        date = body.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # Decode base64 image
        import base64
        image_bytes = base64.b64decode(image_data.split(',')[1])
        
        # Upload image to S3
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        s3_key = f'attendance/{date}/{timestamp}.jpg'
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=image_bytes,
            ContentType='image/jpeg'
        )
        
        # Search for faces in Rekognition collection
        response = rekognition.search_faces_by_image(
            CollectionId=FACE_COLLECTION_ID,
            Image={'Bytes': image_bytes},
            MaxFaces=10,
            FaceMatchThreshold=85
        )
        
        # Get attendance table
        attendance_table = dynamodb.Table(ATTENDANCE_TABLE)
        students_table = dynamodb.Table(STUDENTS_TABLE)
        
        identified_students = []
        attendance_records = []
        
        # Process each face match
        for match in response.get('FaceMatches', []):
            face_id = match['Face']['FaceId']
            confidence = match['Similarity']
            
            # Get student information from DynamoDB
            student_response = students_table.get_item(
                Key={'FaceId': face_id}
            )
            
            if 'Item' in student_response:
                student = student_response['Item']
                student_id = student['StudentId']
                student_name = student['Name']
                student_email = student.get('Email')
                enable_notifications = student.get('EnableNotifications', False)
                
                # Create attendance record
                attendance_id = f"{student_id}_{date}_{timestamp}"
                attendance_record = {
                    'AttendanceId': attendance_id,
                    'StudentId': student_id,
                    'StudentName': student_name,
                    'ClassId': class_id,
                    'Date': date,
                    'Timestamp': datetime.now().isoformat(),
                    'Confidence': Decimal(str(confidence)),
                    'ImageS3Key': s3_key,
                    'Status': 'Present'
                }
                
                # Save to DynamoDB
                attendance_table.put_item(Item=attendance_record)
                
                identified_students.append({
                    'studentId': student_id,
                    'name': student_name,
                    'confidence': confidence,
                    'email': student_email if enable_notifications else None
                })
                attendance_records.append(attendance_record)
                
                # Send individual email notification to student if enabled
                if student_email and enable_notifications:
                    try:
                        individual_message = f"""Hello {student_name},

Your attendance has been recorded successfully!

Details:
- Date: {date}
- Time: {datetime.now().strftime('%H:%M:%S')}
- Confidence: {confidence:.2f}%
- Class: {class_id}
- Status: Present

Thank you for using the Face Recognition Attendance System.

Best regards,
Face Recognition Attendance System
"""
                        sns_client.publish(
                            TopicArn=SNS_TOPIC_ARN,
                            Subject=f'Your Attendance Recorded - {date}',
                            Message=individual_message
                        )
                    except ClientError as e:
                        print(f"Error sending individual notification to {student_email}: {e}")
        
        # Send summary notification to admin/topic subscribers if multiple students identified
        if len(identified_students) > 1:
            try:
                summary_message = f"Attendance recorded for {len(identified_students)} student(s) on {date}\n\n"
                for student in identified_students:
                    summary_message += f"- {student['name']} (ID: {student['studentId']}, Confidence: {student['confidence']:.2f}%)\n"
                
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject=f'Attendance Summary - {date}',
                    Message=summary_message
                )
            except ClientError as e:
                print(f"Error sending summary notification: {e}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'message': f'Attendance processed. {len(identified_students)} student(s) identified.',
                'identifiedStudents': identified_students,
                'totalFacesDetected': len(response.get('FaceMatches', []))
            })
        }
        
    except Exception as e:
        print(f"Error processing attendance: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }

