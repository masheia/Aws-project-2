#!/usr/bin/env python3
"""
Setup CloudFront Distribution for Face Recognition Attendance System
This enables HTTPS support for the S3 static website
"""

import boto3
import time
import json

# Configuration
REGION = 'us-east-1'
FRONTEND_BUCKET = 'attendance-frontend-1765405751'
S3_WEBSITE_ENDPOINT = f'{FRONTEND_BUCKET}.s3-website-{REGION}.amazonaws.com'

def create_cloudfront_distribution(cloudfront_client, s3_client):
    """Create CloudFront distribution for S3 static website"""
    
    print(f"[*] Creating CloudFront distribution for {FRONTEND_BUCKET}...")
    
    # CloudFront distribution configuration
    distribution_config = {
        'CallerReference': f'{FRONTEND_BUCKET}-{int(time.time())}',
        'Comment': f'CloudFront distribution for {FRONTEND_BUCKET}',
        'DefaultRootObject': 'index.html',
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': f'S3-{FRONTEND_BUCKET}',
                    'DomainName': S3_WEBSITE_ENDPOINT,
                    'CustomOriginConfig': {
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'http-only',
                        'OriginSslProtocols': {
                            'Quantity': 1,
                            'Items': ['TLSv1.2']
                        }
                    }
                }
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': f'S3-{FRONTEND_BUCKET}',
            'ViewerProtocolPolicy': 'redirect-to-https',  # Force HTTPS
            'AllowedMethods': {
                'Quantity': 7,
                'Items': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE'],
                'CachedMethods': {
                    'Quantity': 2,
                    'Items': ['GET', 'HEAD']
                }
            },
            'ForwardedValues': {
                'QueryString': True,
                'Cookies': {
                    'Forward': 'all'
                },
                'Headers': {
                    'Quantity': 1,
                    'Items': ['*']
                }
            },
            'MinTTL': 0,
            'DefaultTTL': 86400,
            'MaxTTL': 31536000,
            'Compress': True
        },
        'Enabled': True,
        'PriceClass': 'PriceClass_100',  # Use only North America and Europe (cheaper)
        'CustomErrorResponses': {
            'Quantity': 1,
            'Items': [
                {
                    'ErrorCode': 404,
                    'ResponsePagePath': '/index.html',
                    'ResponseCode': '200',
                    'ErrorCachingMinTTL': 300
                }
            ]
        }
    }
    
    try:
        # Create distribution
        response = cloudfront_client.create_distribution(
            DistributionConfig=distribution_config
        )
        
        distribution = response['Distribution']
        distribution_id = distribution['Id']
        domain_name = distribution['DomainName']
        
        print(f"[OK] CloudFront distribution created!")
        print(f"[*] Distribution ID: {distribution_id}")
        print(f"[*] Domain Name: {domain_name}")
        print(f"[*] Status: {distribution['Status']}")
        print(f"\n[INFO] CloudFront distribution is being deployed...")
        print(f"[INFO] This may take 10-15 minutes to become active")
        print(f"[INFO] You can check status in AWS Console:")
        print(f"      https://console.aws.amazon.com/cloudfront/v3/home?region=us-east-1#/distributions")
        print(f"\n[OK] Once active, use this HTTPS URL:")
        print(f"     https://{domain_name}")
        print(f"\n[INFO] Save this information:")
        print(f"      Distribution ID: {distribution_id}")
        print(f"      HTTPS URL: https://{domain_name}")
        
        return distribution_id, domain_name
        
    except Exception as e:
        print(f"[ERROR] Failed to create CloudFront distribution: {str(e)}")
        if 'already exists' in str(e).lower():
            print(f"[INFO] Distribution may already exist. Checking existing distributions...")
            try:
                distributions = cloudfront_client.list_distributions()
                for dist in distributions.get('DistributionList', {}).get('Items', []):
                    origins = dist.get('Origins', {}).get('Items', [])
                    for origin in origins:
                        if FRONTEND_BUCKET in origin.get('DomainName', ''):
                            print(f"[OK] Found existing distribution:")
                            print(f"     Distribution ID: {dist['Id']}")
                            print(f"     Domain Name: {dist['DomainName']}")
                            print(f"     Status: {dist['Status']}")
                            print(f"     HTTPS URL: https://{dist['DomainName']}")
                            return dist['Id'], dist['DomainName']
            except Exception as check_error:
                print(f"[ERROR] Could not check existing distributions: {str(check_error)}")
        raise

def main():
    """Main function"""
    print("=" * 60)
    print("CloudFront Distribution Setup")
    print("=" * 60)
    print()
    
    try:
        # Initialize clients
        cloudfront_client = boto3.client('cloudfront', region_name=REGION)
        s3_client = boto3.client('s3', region_name=REGION)
        
        # Verify bucket exists
        try:
            s3_client.head_bucket(Bucket=FRONTEND_BUCKET)
            print(f"[OK] S3 bucket verified: {FRONTEND_BUCKET}")
        except Exception as e:
            print(f"[ERROR] S3 bucket not found: {FRONTEND_BUCKET}")
            print(f"       Error: {str(e)}")
            return
        
        # Create CloudFront distribution
        distribution_id, domain_name = create_cloudfront_distribution(cloudfront_client, s3_client)
        
        print()
        print("=" * 60)
        print("Setup Complete!")
        print("=" * 60)
        print()
        print("Your HTTPS URL (will be active in 10-15 minutes):")
        print(f"https://{domain_name}")
        print()
        print("Check status here:")
        print(f"https://console.aws.amazon.com/cloudfront/v3/home?region=us-east-1#/distributions/{distribution_id}")
        
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())



