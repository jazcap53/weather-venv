# file: weather_data.py
# Andrew Jarcho
# 2021-10-24

import json
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
                 obj_name_list=None
                 ):
        self.resource = resource
        self.client = client
        self.bucket_name = bucket_name
        self.obj_name_list = [] if obj_name_list is None else obj_name_list
        self.logger = logger()

    def get_obj_name_list(self):
        self.obj_name_list.extend(['2021-10-22T20:17:00-04:00.json',
                                   '2021-10-22T21:17:00-04:00.json',
                                   '2021-10-22T22:17:00-04:00.json',
                                   '2021-10-22T23:17:00-04:00.json'])

    def get_response(self):
        response_list = []
        for obj_name in self.obj_name_list:
            response = self.resource.Bucket(self.bucket_name).\
                                     Object(obj_name).\
                                     get()
            response_str = response['Body'].read().decode('utf-8')  # new
            response_list.extend(json.loads(response_str))
        pprint(response_list)


if __name__ == '__main__':
    # logger = setup_logging()
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3',
                             aws_secret_access_key=
                             os.environ['AWS_SECRET_ACCESS_KEY'],
                             aws_access_key_id=
                             os.environ['AWS_ACCESS_KEY_ID'])

    wd = WeatherData(s3_resource, s3_client, setup_logging)
    wd.get_obj_name_list()
    wd.get_response()
