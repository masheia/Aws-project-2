import json
import boto3
import urllib.parse
import math
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

# Geofencing Configuration - UPDATE THESE WITH YOUR SCHOOL COORDINATES
SCHOOL_LATITUDE = 40.7128   # TODO: Update with your school's latitude
SCHOOL_LONGITUDE = -74.0060  # TODO: Update with your school's longitude
ALLOWED_RADIUS_METERS = 500  # Allowed radius in meters (500m = ~0.3 miles)
REQUIRE_LOCATION = True      # Set to False to allow uploads without location (less secure)

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in meters
    """
    # Earth's radius in meters
    R = 6371000
    
    # Convert to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def validate_location(latitude, longitude):
    """
    Validate if coordinates are within school area
    Returns (is_valid, distance_meters, message)
    """
    if latitude is None or longitude is None:
        if REQUIRE_LOCATION:
            return False, None, "Location is required for security. Please enable location services."
        else:
            return True, None, "Location not provided, allowing upload (flexible mode)"
    
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        # Validate coordinate ranges
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return False, None, "Invalid coordinates provided"
        
        # Calculate distance from school
        distance = calculate_distance(SCHOOL_LATITUDE, SCHOOL_LONGITUDE, lat, lon)
        
        if distance <= ALLOWED_RADIUS_METERS:
            return True, distance, f"Location verified (within {int(distance)}m of school)"
        else:
            return False, distance, f"Upload rejected: You are {int(distance)}m away from school (allowed: {ALLOWED_RADIUS_METERS}m). Please be within the school area to upload images."
            
    except (ValueError, TypeError) as e:
        return False, None, f"Invalid location data: {str(e)}"

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
        
        # Get location data for geofencing
        latitude = body.get('latitude')
        longitude = body.get('longitude')
        
        # Validate location (geofencing) before processing
        is_valid_location, distance, location_message = validate_location(latitude, longitude)
        if not is_valid_location:
            return {
                'statusCode': 403,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'error': location_message,
                    'locationRejected': True,
                    'distance': distance
                })
            }
        
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

