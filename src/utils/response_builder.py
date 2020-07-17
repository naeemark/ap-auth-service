"""Response Builder for the application"""
from src.utils.errors.errors_collection import errors_collection
from src.utils.logger import error as log_error
from src.utils.logger import info


def get_success_response(status_code=200, message="Success", data=None):
    """
        Returns Success Response stub
        :param status_code: status code to be set as `Status` and `responseCode`
        :param message:     A message string to be set as `responseMessage`
        :param error:       A `dict` object to be passed as response

        :return: an error dict, status code
    """
    info({"message": message, "data": data})
    return {"responseCode": status_code, "responseMessage": message, "response": data}, status_code


def get_error_response(status_code=500, message="Something bad happened!", error=None):
    """
    Returns error stub
        :param status_code: status code to be set as `Status` and `responseCode`
        :param message:     A message string to be set as `responseMessage`
        :param error:   A `dict` object to be passed as response, if `None`,
                        will get from errors_collection based upon the status_code

        :return: an error dict, status code
    """
    error = {
        "responseCode": status_code,
        "responseMessage": message,
        "response": {"error": error if error else errors_collection.get(status_code)},
    }
    log_error(error)
    return error, status_code


def get_app_error_response(application_error=None):
    """
    Returns error stub
        :param error:   An ApplicationError object

        :return: an error dict, status code
    """
    return get_error_response(status_code=application_error.status_code, message=application_error.message, error=application_error.error)
