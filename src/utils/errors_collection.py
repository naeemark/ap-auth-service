""" Error Collection for the application"""

error_default = {
    "errorCode": "UNCAUGHT",
    "errorTitle": "We seem to have a problem!",
    "errorDescription": "Our internal system is having problem, please contact our administrator!",
}

error_not_found_404 = {
    "errorCode": "RESOURCE_NOT_FOUND",
    "errorTitle": "Resource not found",
    "errorDescription": "Seems the object which you are trying to find is not available",
}

error_bad_request_400 = {
    "errorCode": "VALIDATION_ERROR",
    "errorTitle": "Invalid Parameters provided",
    "errorDescription": "Seems the provided input is not validated by the system",
}

errors_collection = {400: error_bad_request_400, 404: error_not_found_404, 500: error_default}
