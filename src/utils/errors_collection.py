""" Error Collection for the application"""

uncaught = {
    "errorCode": "UNCAUGHT",
    "errorTitle": "We seem to have a problem!",
    "errorDescription": "Our internal system is having problem, please contact our administrator!",
}

invalid_credentials_401 = {
    "errorCode": "UNAUTHORIZED",
    "errorTitle": "Invalid credentials provided",
    "errorDescription": "Seems the provided input is not validated by the system",
}

bad_request_400 = {
    "errorCode": "VALIDATION_ERROR",
    "errorTitle": "Invalid Parameters provided",
    "errorDescription": "Seems the provided input is not validated by the system",
}

not_found_404 = {
    "errorCode": "RESOURCE_NOT_FOUND",
    "errorTitle": "Resource not found",
    "errorDescription": "Seems the object which you are trying to find is not available",
}

user_conflict_409 = {
    "errorCode": "CONFLICT",
    "errorTitle": "User already Exists",
    "errorDescription": "A user with that identity already exists",
}

service_unavailable_503 = {
    "errorCode": "SERVICE_UNAVAILABLE",
    "errorTitle": "Service unavailable",
    "errorDescription": "One or more services are not available at the moment.",
}

unprocessable_entity_422 = {
    "errorCode": "UNPROCESSABLE_ENTITY",
    "errorTitle": "Token Invalid",
    "errorDescription": (
        "Request was well-formed but was unable to be followed due to semantic errors specify correct token"
    ),
}

not_acceptable_406 = {
    "errorCode": "NOT_ACCEPTABLE",
    "errorTitle": "Invalid Email",
    "errorDescription": "email is not correct",
}


errors_collection = {
    500: uncaught,
    400: bad_request_400,
    401: invalid_credentials_401,
    404: not_found_404,
    409: user_conflict_409,
    503: service_unavailable_503,
    422: unprocessable_entity_422,
    406: not_acceptable_406,
}
