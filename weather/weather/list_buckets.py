"""Print list of user's s3 buckets to stdout"""
import boto3

# Retrieve the list of existing buckets
s3_client = boto3.client('s3')
response = s3_client.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
