import argparse
from argparse import Namespace

from weather.utils import make_argparser, get_bucket_name, BASE_BUCKET_NAME


def test_make_argparser(capsys):
    description = 'my parser'
    parser = make_argparser(description, [])
    assert type(parser) == argparse.Namespace


def test_get_bucket_name_no_debug():
    namespace = Namespace(debug=False)
    name = get_bucket_name(namespace)
    assert name == BASE_BUCKET_NAME


def test_get_bucket_name_debug():
    namespace = Namespace(debug=True)
    name = get_bucket_name(namespace)
    assert name == BASE_BUCKET_NAME + '-test'
