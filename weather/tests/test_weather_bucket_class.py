import boto3
import pytest

from weather.weather_bucket_class import WeatherBucket


@pytest.fixture
def s3client():
    return boto3.client('s3')


@pytest.fixture
def bucket(s3client):
    return WeatherBucket(s3client)


def test_make_argparser(bucket):
    description = 'make argparser'
    arg_parser = bucket.make_argparser(description, [])
    assert arg_parser.debug is False


def test_make_argparser_debug(bucket):
    description = 'make argparser with debug switch'
    arg_parser = bucket.make_argparser(description, ['-d'])
    assert arg_parser.debug is True


def test_get_bucket_name(bucket):
    bucket.args = bucket.make_argparser('Some description')
    assert bucket.get_bucket_name() == bucket.BASE_BUCKET_NAME


def test_get_bucket_name_debug(bucket):
    bucket.args = bucket.make_argparser('Some description', ['-d'])
    assert bucket.get_bucket_name() == bucket.BASE_BUCKET_NAME + '-test'
