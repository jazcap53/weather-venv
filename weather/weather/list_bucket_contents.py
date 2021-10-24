# filename: list_bucket_contents.py
# Andrew Jarcho
# 5/2021

"""Get contents (filenames) of s3 bucket; pprint them to stdout"""
from pprint import pprint

import boto3

from utils import (make_argparser, get_bucket_name,
                  get_bucket_contents)


def output_filenames(all_objects):
    """pprint filenames retrieved from s3 bucket"""
    all_filenames = []
    try:
        for i in range(len(all_objects['Contents'])):
            all_filenames.append(all_objects['Contents'][i]['Key'])
    # all_objects['Contents'] raises KeyError if no files
    except KeyError as err:
        if 'Contents' in str(err):
            pass
    pprint(all_filenames)


def main():
    """Driver for this script"""
    args = make_argparser('List contents of a bucket')
    s3_client = boto3.client('s3')  # aws client for s3 service
    bucket_name = get_bucket_name(args)  # use test bucket if args.name == True
    all_objects = get_bucket_contents(s3_client, bucket_name)
    output_filenames(all_objects)


if __name__ == '__main__':
    main()
