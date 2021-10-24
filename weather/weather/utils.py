# utils.py
# Andrew Jarcho
# 5/2021

"""Utility functions for weather.py program"""
import argparse


BASE_BUCKET_NAME = 'aaj-raining-buckets'


# see https://stackoverflow.com/questions/55259371
def make_argparser(descrip, args=None):
    """Make a command line argument parser"""
    parser = argparse.ArgumentParser(description=descrip)
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Show the contents of a bucket')
    return parser.parse_args(args)


def get_bucket_name(args):
    """Return bucket name"""
    bucket_name = BASE_BUCKET_NAME
    if args.debug:
        bucket_name += '-test'
    return bucket_name


def get_bucket_contents(client, bucket_name):
    """List the contents of a bucket"""
    return client.list_objects_v2(Bucket=bucket_name)
