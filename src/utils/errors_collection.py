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
    "errorDescription": ("Request was well-formed but was unable to be followed due to semantic errors specify correct token"),
}

precondition_failed_412 = {
    "errorCode": "PRECONDITION_FAILED",
    "errorTitle": "Password precondition failed",
    "errorDescription": "'Password' policy not followed",
}

email_not_valid_412 = {
    "errorCode": "EmailNotValidError",
    "errorTitle": "Email not valid",
    "errorDescription": "Provided value is not a valid email address.",
}

errors_collection = {
    400: bad_request_400,
    401: invalid_credentials_401,
    404: not_found_404,
    409: user_conflict_409,
    412: precondition_failed_412,
    422: unprocessable_entity_422,
    500: uncaught,
    503: service_unavailable_503,
}
