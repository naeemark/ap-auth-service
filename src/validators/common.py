"""common validator utilities """
from src.utils.constant.response_messages import PROPERTY_REQUIRED


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
        required_properties = ", ".join(required_properties_list)
        raise LookupError(PROPERTY_REQUIRED.format(required_properties=required_properties))
