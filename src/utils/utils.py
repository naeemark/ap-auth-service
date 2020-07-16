"""
    A misc utility file
"""
from datetime import datetime


def add_parser_headers_argument(parser=None, arg_name=None, arg_type=str, location="headers"):
    """Adds argument for header validations"""
    parser.add_argument(arg_name, type=arg_type, location=location)


def add_parser_query_argument(parser=None, arg_name=None, arg_type=str, location="args"):
    """Adds argument for header validations"""
    parser.add_argument(arg_name, type=arg_type, location=location)


def add_parser_argument(parser=None, arg_name=None, arg_type=str):
    """Adds argument for param validations"""
    parser.add_argument(arg_name, type=arg_type)


def get_epoch_utc_timestamp():
    """Returns a UTC epoch timestamp"""
    return int(datetime.utcnow().timestamp())


def get_epoch_timestamp():
    """Returns a local epoch timestamp"""
    return int(datetime.now().timestamp())
