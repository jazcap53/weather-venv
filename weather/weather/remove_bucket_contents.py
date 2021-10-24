# file: remove_bucket_contents.py
# Andrew Jarcho
# 5/2021

"""Delete contents of an AWS S3 bucket"""
import boto3

from utils import (make_argparser, get_bucket_name, get_bucket_contents)


def delete_items(client, bucket_name, all_objects):
    """Delete all items from bucket"""
    deleted_count = 0
    try:
        for i in range(len(all_objects['Contents'])):
            client.delete_object(Bucket=bucket_name,
                                 Key=all_objects['Contents'][i]['Key'])
            deleted_count += 1
    # all_objects['Contents'] raises KeyError if no items
    except KeyError as err:
        if 'Contents' in str(err):
            pass
    print(f'{deleted_count} items deleted')


def main():
    """Driver for this script"""
    args = make_argparser('Remove items from bucket')
    s3_client = boto3.client('s3')
    bucket_name = get_bucket_name(args)  # use test bucket if args.name
    all_objects = get_bucket_contents(s3_client, bucket_name)
    delete_items(s3_client, bucket_name, all_objects)


if __name__ == '__main__':
    main()
