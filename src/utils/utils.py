"""
    A misc utility file
"""
import json
from datetime import datetime

from src.utils.logger import info


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


def log_request_info(request=None):
    """ logs request attributes """
    if request:
        info("Request Path: {}".format(request.path))
        info("Request Headers:\n{}".format(str(request.headers).rstrip()))
        info("Request Body: {}".format(json.loads(request.get_data().decode())))
