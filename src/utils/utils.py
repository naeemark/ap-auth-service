"""
    A misc utility file
"""


def add_parser_headers_argument(parser=None, arg_name=None, arg_type=str, location="headers"):
    """Adds argument for header validations"""
    parser.add_argument(arg_name, type=arg_type, location=location)


def add_parser_argument(parser=None, arg_name=None, arg_type=str):
    """Adds argument for param validations"""
    parser.add_argument(arg_name, type=arg_type)
