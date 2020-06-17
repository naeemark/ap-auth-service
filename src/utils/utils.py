"""
    A misc utility file
"""
from src.utils.constant.exception import ValidationException as ve
from src.utils.constant.response_messages import PROPERTY_REQUIRED


def add_parser_headers_argument(parser=None, arg_name=None, arg_type=str, location="headers"):
    """Adds argument for header validations"""
    parser.add_argument(arg_name, type=arg_type, help=ve.FIELD_BLANK, location=location)


def add_parser_argument(parser=None, arg_name=None, arg_type=str):
    """Adds argument for param validations"""
    parser.add_argument(arg_name, type=arg_type)


def check_none(element):
    """filter method"""
    if not element[1]:
        return True
    return False


def check_missing_properties(properties):
    """checks for missing properties"""
    missing_values = tuple(filter(check_none, properties))
    if missing_values:
        required_properties_list = (missing_elements[0] for missing_elements in missing_values)
        required_properties = ",".join(required_properties_list)
        return PROPERTY_REQUIRED.format(required_properties=required_properties)

    return False
