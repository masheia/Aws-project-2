#!/usr/bin/env python3
"""
Admin script to manually add a student to the system
This script allows admins to add students via AWS Console/CLI
and automatically sends a welcome email notification.

Usage:
    python admin-add-student.py --student-id STU001 --name "John Doe" --email "john@example.com" --image-path "photo.jpg"
"""

import boto3
import base64
import json
import argparse
from datetime import datetime
from decimal import Decimal

# Initialize AWS clients
s3_client = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

# Constants
FACE_COLLECTION_ID = 'attendance-students'
STUDENTS_TABLE = 'Students'
S3_BUCKET = 'attendance-images-1765405751'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:846863292978:attendance-notifications'

def add_student(student_id, name, email, image_path, enable_notifications=True):
    """
    Add a student manually (for admin use)
    """
    try:
        # Read image file
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Sanitize student_id for Rekognition
        import re
        sanitized_student_id = re.sub(r'[^a-zA-Z0-9_.\-:]', '_', student_id)
        
        # Index face in Rekognition collection
        print(f"Indexing face for {name}...")
        response = rekognition.index_faces(
            CollectionId=FACE_COLLECTION_ID,
            Image={'Bytes': image_bytes},
            ExternalImageId=sanitized_student_id,
            MaxFaces=1,
            QualityFilter='AUTO',
            DetectionAttributes=['ALL']
        )
        
        if not response['FaceRecords']:
            print("Error: No face detected in image")
            return False
        
        face_id = response['FaceRecords'][0]['Face']['FaceId']
        face_details = response['FaceRecords'][0]['Face']
        
        # Upload image to S3
        s3_key = f'students/{student_id}/{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
        print(f"Uploading image to S3: {s3_key}")
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=image_bytes,
            ContentType='image/jpeg'
        )
        
        # Convert float to Decimal for DynamoDB
        def convert_floats(obj):
            if isinstance(obj, float):
                return Decimal(str(obj))
            elif isinstance(obj, dict):
                return {k: convert_floats(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_floats(item) for item in obj]
            return obj
        
        face_details_converted = convert_floats(face_details)
        
        # Save student information to DynamoDB
        students_table = dynamodb.Table(STUDENTS_TABLE)
        student_record = {
            'FaceId': face_id,
            'StudentId': student_id,
            'Name': name,
            'Email': email,
            'EnableNotifications': enable_notifications,
            'ImageS3Key': s3_key,
            'RegisteredDate': datetime.now().isoformat(),
            'FaceDetails': {
                'Confidence': str(face_details_converted['Confidence']),
                'BoundingBox': face_details_converted['BoundingBox']
            }
        }
        
        print(f"Saving student record to DynamoDB...")
        students_table.put_item(Item=student_record)
        
        # Send welcome email notification
        if email and enable_notifications:
            try:
                print(f"Sending welcome email to {email}...")
                
                # Subscribe email to SNS topic
                try:
                    sns_client.subscribe(
                        TopicArn=SNS_TOPIC_ARN,
                        Protocol='email',
                        Endpoint=email
                    )
                    print("Email subscribed to SNS topic (check email for confirmation)")
                except Exception as e:
                    print(f"Subscription note: {e}")
                
                # Send welcome notification
                welcome_message = f"""Hello {name},

Welcome to the Face Recognition Attendance System!

Your account has been successfully created by an administrator:
- Student ID: {student_id}
- Name: {name}
- Email: {email}

Your face has been registered and you can now mark your attendance using the system.

You will receive email notifications when your attendance is recorded.

Best regards,
Face Recognition Attendance System
"""
                
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject='Welcome to Face Recognition Attendance System',
                    Message=welcome_message
                )
                print("Welcome email sent successfully!")
            except Exception as e:
                print(f"Error sending welcome notification: {e}")
        
        print(f"\n✅ Student {name} (ID: {student_id}) added successfully!")
        print(f"   Face ID: {face_id}")
        print(f"   Image stored at: s3://{S3_BUCKET}/{s3_key}")
        
        return True
        
    except Exception as e:
        print(f"Error adding student: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a student manually to the attendance system')
    parser.add_argument('--student-id', required=True, help='Student ID')
    parser.add_argument('--name', required=True, help='Student full name')
    parser.add_argument('--email', required=True, help='Student email address')
    parser.add_argument('--image-path', required=True, help='Path to student photo file')
    parser.add_argument('--notifications', action='store_true', default=True, help='Enable email notifications (default: True)')
    
    args = parser.parse_args()
    
    success = add_student(
        student_id=args.student_id,
        name=args.name,
        email=args.email,
        image_path=args.image_path,
        enable_notifications=args.notifications
    )
    
    exit(0 if success else 1)

