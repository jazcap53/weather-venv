# file: weather_data.py
# Andrew Jarcho
# 2021-10-24

import logging
import os
from pprint import pprint

import boto3


def setup_logging():
    logging.basicConfig(filename='test_log.log', level=logging.INFO)
    return logging.getLogger(__name__)


class WeatherData:
    BASE_BUCKET_NAME = 'aaj-raining-buckets'

    def __init__(self, resource, client, logger,
                 bucket_name=BASE_BUCKET_NAME,
                 object_name='2021-10-22T20:17:00-04:00.json'):
        self.resource = resource
        self.client = client
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.logger = logger()

    def get_response(self):
        response = self.resource.Bucket(self.bucket_name).\
                                 Object(self.object_name).\
                                 get()
        pprint(response)
        self.logger.info("HTTPStatusCode: %s", response['ResponseMetadata']['HTTPStatusCode'])
        self.logger.info("RequestId: %s", response['ResponseMetadata']['RequestId'])
        self.logger.info("HostId: %s", response['ResponseMetadata']['HostId'])
        self.logger.info("Date: %s", response['ResponseMetadata']['HTTPHeaders']['date'])

    def retrieve_json(self):
        with open('file_holder', 'wb') as fileholder:
            self.client.download_fileobj(self.bucket_name,
                                         self.object_name,
                                         fileholder)
            # self.logger.info("HTTPStatusCode: %s", response['ResponseMetadata']['HTTPStatusCode'])
            # self.logger.info("RequestId: %s", response['ResponseMetadata']['RequestId'])
            # self.logger.info("HostId: %s", response['ResponseMetadata']['HostId'])
            # self.logger.info("Date: %s", response['ResponseMetadata']['HTTPHeaders']['date'])


if __name__ == '__main__':
    # logger = setup_logging()
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3',
                             aws_secret_access_key=
                             os.environ['AWS_SECRET_ACCESS_KEY'],
                             aws_access_key_id=
                             os.environ['AWS_ACCESS_KEY_ID'])

    wd = WeatherData(s3_resource, s3_client, setup_logging)
    wd.get_response()
    wd.retrieve_json()
