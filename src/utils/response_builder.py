"""Response Builder for the application"""
from src.utils.errors_collection import errors_collection


def get_success_response(status_code=200, message="Success", data=None):
    """Returns Success Response stub"""
    return {"responseCode": status_code, "responseMessage": message, "response": data}


def get_error_response(status_code=500, message="Something bad happened!"):
    """ Returns error stub"""
    error = {
        "responseCode": status_code,
        "responseMessage": message,
        "response": {"error": errors_collection.get(status_code)},
    }
    return error, status_code
