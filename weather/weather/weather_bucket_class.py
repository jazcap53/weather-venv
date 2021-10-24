# file: weather_bucket.py
# andrew jarcho
# 6/2021

import argparse
import boto3
from pprint import pprint


class WeatherBucket:
    BASE_BUCKET_NAME = 'aaj-raining-buckets'

    def __init__(self, client):
        self.client = client
        self.args = None
        self.bucket_name = ''
        self.bucket_contents = []

    # see https://stackoverflow.com/questions/55259371
    @staticmethod
    def make_argparser(descrip, args=None):
        """Make a command line argument parser"""
        parser = argparse.ArgumentParser(description=descrip)
        parser.add_argument('-d', '--debug', action='store_true',
                            help='Operate on a separate debug bucket')
        return parser.parse_args(args)

    def get_bucket_name(self):
        """Return bucket name"""
        bucket_name = self.BASE_BUCKET_NAME
        if self.args.debug:
            bucket_name += '-test'
        return bucket_name

    def get_bucket_contents(self):
        """List the contents of a bucket"""
        return self.client.list_objects_v2(Bucket=self.bucket_name)

    def output_filenames(self):
        """pprint filenames retrieved from s3 bucket"""
        try:
            all_filenames = [self.bucket_contents['Contents'][i]['Key']
                             for i in
                             range(len(self.bucket_contents['Contents']))]
        # self.bucket_contents['Contents'] raises KeyError if no files
        except KeyError as err:
            if 'Contents' in str(err):
                all_filenames = []
            else:
                raise
        pprint(all_filenames)

    def main(self):
        self.args = self.make_argparser('Store weather data in an AWS S3 bucket')
        self.bucket_name = self.get_bucket_name()
        print(f'bucket name is {self.bucket_name}')
        self.bucket_contents = self.get_bucket_contents()
        self.output_filenames()


if __name__ == '__main__':
    w_b = WeatherBucket(boto3.client('s3'))
    w_b.main()

