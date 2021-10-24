# import boto3
# import logging
# 
# logging.basicConfig(filename='dl_contents.log', level=logging.INFO)
# logger = logging.getLogger(__name__)
# 
# s3 = boto3.client('s3')
# 
# 
# with open('file_holder', 'wb') as fileholder:
#     s3.download_fileobj(bucket_name, object_name, fileholder)
# 
# logger.info("HTTPStatusCode: %s", response['ResponseMetadata']['HTTPStatusCode'])
# logger.info("RequestId: %s", response['ResponseMetadata']['RequestId'])
# logger.info("HostId: %s", response['ResponseMetadata']['HostId'])
# logger.info("Date: %s", response['ResponseMetadata']['HTTPHeaders']['date'])

from pprint import pprint
import logging
import boto3


bucket_name = "aaj-raining-buckets"
object_name = "2021-10-22T20:17:00-04:00.json"


logging.basicConfig(filename='test_log.log', level=logging.INFO)
logger = logging.getLogger(__name__)

s3_resource = boto3.resource('s3')
# s3 = boto3.client('s3')

response = s3_resource.Bucket('aaj-raining-buckets').Object('2021-10-23T19:17:00-04:00.json').get()

pprint(response)

s3_client = boto3.client('s3')

with open('file_holder', 'wb') as fileholder:
    s3_client.download_fileobj(bucket_name, object_name, fileholder)

logger.info("HTTPStatusCode: %s", response['ResponseMetadata']['HTTPStatusCode'])
logger.info("RequestId: %s", response['ResponseMetadata']['RequestId'])
logger.info("HostId: %s", response['ResponseMetadata']['HostId'])
logger.info("Date: %s", response['ResponseMetadata']['HTTPHeaders']['date'])
