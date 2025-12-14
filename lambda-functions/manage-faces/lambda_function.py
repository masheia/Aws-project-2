import json
import boto3
import base64
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize AWS clients
s3_client = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

# Constants
FACE_COLLECTION_ID = 'attendance-students'
STUDENTS_TABLE = 'Students'
S3_BUCKET = 'attendance-images-1765405751'

def lambda_handler(event, context):
    """
    Register a new student face in the system
    """
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        student_id = body.get('studentId')
        student_name = body.get('name')
        image_data = body.get('image')
        
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
        
        students_table.put_item(Item=student_record)
        
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

