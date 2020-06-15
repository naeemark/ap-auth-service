"""
    A misc utility file
"""
from src.constant.exception import ValidationException as ve


def add_parser_header_argument(parser=None, arg_name=None, arg_type=str, is_required=True, location="headers"):
    """Adds argument for header validations"""
    parser.add_argument(arg_name, type=arg_type, required=is_required, help=ve.FIELD_BLANK, location=location)


def add_parser_argument(parser=None, arg_name=None, arg_type=str):
    """Adds argument for param validations"""
    parser.add_argument(arg_name, type=arg_type)
