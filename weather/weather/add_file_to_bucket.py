# file: add_file_to_bucker.py
# Andrew Jarcho
# 2021-10-24

import logging
import boto3

logging.basicConfig(filename='test_log.log', level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.resource('s3')

response = s3.Bucket('aaj-raining-buckets').\
              Object('2021-10-23T20:18:00-04:00.json').put()

logger.info("HTTPStatusCode: %s", response['ResponseMetadata']['HTTPStatusCode'])
logger.info("RequestId: %s", response['ResponseMetadata']['RequestId'])
logger.info("HostId: %s", response['ResponseMetadata']['HostId'])
logger.info("Date: %s", response['ResponseMetadata']['HTTPHeaders']['date'])
