"""Prepare data structures needed for weather program"""
import argparse
from collections import namedtuple
import logging
from pathlib import Path
import sys

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


CityState = namedtuple('CityState', 'city state')


def setup_logging():
    """Configure logging for weather program"""
    log_file_name = str(Path(__file__).resolve().parent / 'weather_record.log')
    logging.basicConfig(filename=log_file_name, encoding='utf-8',
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s %(message)s')
    logger = logging.getLogger(__name__)



def do_parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
            description='Store and retrieve weather data.'
    )
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Run in debug mode.')
    args = parser.parse_args()
    return args


def log_python_executable(args):
    python_executable_path = sys.executable
    if python_executable_path:
        if 'pypoetry' in python_executable_path:
            debug_str = 'weather.py invoked manually'
            if args.debug:
                debug_str += ' in debug mode.'
            else:
                debug_str += '.'
        else:
            debug_str = 'weather.py invoked by cron job.'
        logging.info(debug_str)


def get_location_list(args):
    """Set different pair of locations for production and for debug"""
    if args.debug:
        west = CityState('Seattle', 'WA')
        east = CityState('Boston', 'MA')
    else:
        west = CityState('Los Angeles', 'CA')
        east = CityState('New York', 'NY')
    return [west, east]


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: bucket name if bucket created or bucket already exists, else ''
    """
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            response = s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=location
                    )
    except (ClientError, NoCredentialsError) as err:
        logging.error(err)
        raise

    response_bucket = response["Location"][1:]
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info(f'Bucket {response_bucket} OK.')
    else:
        logging.info(f'Bucket {response_bucket} not created.')

    return bucket_name
