import json
import boto3
from datetime import datetime, timedelta
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')

# Custom JSON encoder to handle Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Constants
ATTENDANCE_TABLE = 'AttendanceRecords'

def lambda_handler(event, context):
    """
    Retrieve attendance records from DynamoDB
    """
    try:
        # Get query parameters
        query_params = event.get('queryStringParameters') or {}
        
        date = query_params.get('date')
        student_id = query_params.get('studentId')
        class_id = query_params.get('classId')
        
        attendance_table = dynamodb.Table(ATTENDANCE_TABLE)
        
        # Build query based on parameters
        if date and student_id:
            # Get specific student attendance for a date
            response = attendance_table.query(
                IndexName='StudentId-Date-index',  # GSI
                KeyConditionExpression='StudentId = :sid AND #dt = :dt',
                ExpressionAttributeNames={'#dt': 'Date'},
                ExpressionAttributeValues={
                    ':sid': student_id,
                    ':dt': date
                }
            )
        elif date:
            # Get all attendance for a date
            response = attendance_table.query(
                IndexName='Date-index',  # GSI
                KeyConditionExpression='#dt = :dt',
                ExpressionAttributeNames={'#dt': 'Date'},
                ExpressionAttributeValues={':dt': date}
            )
        elif student_id:
            # Get all attendance for a student
            response = attendance_table.query(
                IndexName='StudentId-Date-index',
                KeyConditionExpression='StudentId = :sid',
                ExpressionAttributeValues={':sid': student_id}
            )
        else:
            # Get recent attendance (last 7 days)
            seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            today = datetime.now().strftime('%Y-%m-%d')
            
            response = attendance_table.scan(
                FilterExpression='#dt BETWEEN :start AND :end',
                ExpressionAttributeNames={'#dt': 'Date'},
                ExpressionAttributeValues={
                    ':start': seven_days_ago,
                    ':end': today
                }
            )
        
        items = response.get('Items', [])
        
        # Format response - convert Decimal to float/string for JSON
        def convert_decimals(obj):
            """Recursively convert Decimal to float"""
            if isinstance(obj, Decimal):
                return float(obj)
            elif isinstance(obj, dict):
                return {k: convert_decimals(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_decimals(item) for item in obj]
            return obj
        
        attendance_records = []
        for item in items:
            # Convert all values, handling Decimal types
            record = {
                'attendanceId': item['AttendanceId'],
                'studentId': item['StudentId'],
                'studentName': item['StudentName'],
                'classId': item['ClassId'],
                'date': item['Date'],
                'timestamp': item['Timestamp'],
                'confidence': convert_decimals(item.get('Confidence', 'N/A')),
                'status': item['Status']
            }
            attendance_records.append(convert_decimals(record))
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'records': attendance_records,
                'count': len(attendance_records)
            }, cls=DecimalEncoder)
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


