import json
import boto3
import base64
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
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:846863292978:attendance-notifications'

# Constants
FACE_COLLECTION_ID = 'attendance-students'
STUDENTS_TABLE = 'Students'
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
    Register a new student face in the system
    """
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        student_id = body.get('studentId')
        student_name = body.get('name')
        email = body.get('email')  # Optional for backwards compatibility
        enable_notifications = body.get('enableNotifications', True)  # Default to True
        image_data = body.get('image')
        
        # Get location data for geofencing
        latitude = body.get('latitude')
        longitude = body.get('longitude')
        
        if not all([student_id, student_name, image_data]):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'Missing required fields: studentId, name, image'
                })
            }
        
        # Validate location (geofencing)
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
        image_bytes = base64.b64decode(image_data.split(',')[1])
        
        # Sanitize student_id for Rekognition externalImageId
        # Rekognition only allows: [a-zA-Z0-9_.\-:]+
        # Replace spaces and other invalid characters with underscores
        import re
        sanitized_student_id = re.sub(r'[^a-zA-Z0-9_.\-:]', '_', student_id)
        
        # Index face in Rekognition collection
        response = rekognition.index_faces(
            CollectionId=FACE_COLLECTION_ID,
            Image={'Bytes': image_bytes},
            ExternalImageId=sanitized_student_id,
            MaxFaces=1,
            QualityFilter='AUTO',
            DetectionAttributes=['ALL']
        )
        
        if not response['FaceRecords']:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'No face detected in image'
                })
            }
        
        face_id = response['FaceRecords'][0]['Face']['FaceId']
        face_details = response['FaceRecords'][0]['Face']
        
        # Upload image to S3
        s3_key = f'students/{student_id}/{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=image_bytes,
            ContentType='image/jpeg'
        )
        
        # Save student information to DynamoDB
        students_table = dynamodb.Table(STUDENTS_TABLE)
        # Convert float to Decimal for DynamoDB
        def convert_floats(obj):
            if isinstance(obj, float):
                return Decimal(str(obj))
            elif isinstance(obj, dict):
                return {k: convert_floats(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_floats(item) for item in obj]
            return obj
        
        # Convert all floats in face_details to Decimal or string
        face_details_converted = convert_floats(face_details)
        
        student_record = {
            'FaceId': face_id,
            'StudentId': student_id,
            'Name': student_name,
            'ImageS3Key': s3_key,
            'RegisteredDate': datetime.now().isoformat(),
            'FaceDetails': {
                'Confidence': str(face_details_converted['Confidence']),
                'BoundingBox': face_details_converted['BoundingBox']  # Already converted
            }
        }
        
        # Add email and notification preferences if provided
        if email:
            student_record['Email'] = email
            student_record['EnableNotifications'] = enable_notifications
        
        students_table.put_item(Item=student_record)
        
        # Send welcome email notification if email provided and notifications enabled
        if email and enable_notifications:
            try:
                # Subscribe email to SNS topic (if not already subscribed)
                # IMPORTANT: SNS requires email confirmation before messages can be sent
                subscription_arn = None
                try:
                    subscribe_response = sns_client.subscribe(
                        TopicArn=SNS_TOPIC_ARN,
                        Protocol='email',
                        Endpoint=email
                    )
                    subscription_arn = subscribe_response.get('SubscriptionArn')
                    print(f"Email subscription initiated: {subscription_arn}")
                    # AWS will automatically send a confirmation email to the user
                except ClientError as e:
                    error_code = e.response.get('Error', {}).get('Code', '')
                    if error_code == 'SubscriptionLimitExceeded':
                        print(f"Email may already be subscribed: {e}")
                    else:
                        print(f"Subscription note: {e}")
                
                # Send welcome notification
                # Note: This will only work if subscription is already confirmed
                # If not confirmed, AWS will send confirmation email first
                welcome_message = f"""Hello {student_name},

Welcome to the Face Recognition Attendance System!

Your account has been successfully created:
- Student ID: {student_id}
- Name: {student_name}
- Email: {email}

Your face has been registered and you can now mark your attendance using the system.

IMPORTANT: To receive email notifications when your attendance is recorded, please check your email and confirm your subscription. You should receive a confirmation email from AWS SNS shortly. After confirming, you will receive email notifications whenever your attendance is recorded.

Best regards,
Face Recognition Attendance System
"""
                
                # Try to publish - will work if subscription is already confirmed
                # If not confirmed, the message may be queued or the confirmation email will be sent
                try:
                    sns_client.publish(
                        TopicArn=SNS_TOPIC_ARN,
                        Subject='Welcome to Face Recognition Attendance System',
                        Message=welcome_message
                    )
                    print(f"Welcome email sent successfully to {email}")
                except ClientError as publish_error:
                    error_code = publish_error.response.get('Error', {}).get('Code', '')
                    if 'InvalidParameter' in str(publish_error) or 'PendingConfirmation' in str(publish_error):
                        # Subscription not confirmed yet - this is expected for new emails
                        print(f"Subscription pending confirmation. User will receive confirmation email first.")
                    else:
                        print(f"Error publishing welcome message: {publish_error}")
                        
            except Exception as e:
                print(f"Error in email notification process: {e}")
                # Don't fail the registration if notification fails
                import traceback
                traceback.print_exc()
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'message': f'Face registered successfully for {student_name}',
                'faceId': face_id,
                'studentId': student_id
            })
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            # Collection doesn't exist, create it
            try:
                rekognition.create_collection(CollectionId=FACE_COLLECTION_ID)
                # Retry the index_faces call
                return lambda_handler(event, context)
            except Exception as create_error:
                return {
                    'statusCode': 500,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'success': False,
                        'error': f'Failed to create collection: {str(create_error)}'
                    })
                }
        else:
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
    except Exception as e:
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

