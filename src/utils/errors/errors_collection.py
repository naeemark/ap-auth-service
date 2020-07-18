""" Error Collection for the application"""

uncaught = {
    "code": "UNCAUGHT",
    "title": "We seem to have a problem!",
    "description": "Our internal system is having problem, please contact our administrator!",
}

invalid_credentials_401 = {
    "code": "UNAUTHORIZED",
    "title": "Invalid auth credentials provided",
    "description": "Seems the provided input is not validated by the system",
}

expired_jwt_401 = {
    "code": "UNAUTHORIZED",
    "title": "Invalid credentials provided",
    "description": "Seems the JWT Token has been revoked or expired",
}

invalid_jwt_401 = {
    "code": "UNAUTHORIZED",
    "title": "Invalid credentials provided",
    "description": "Seems the `Authorization` does not contain required info",
}

inactive_user_401 = {
    "code": "UNAUTHORIZED",
    "title": "Invalid Parameters provided",
    "description": "Seems caller is deactivated and can not perform this operation",
}

pending_approval_401 = {
    "code": "UNAUTHORIZED",
    "title": "Invalid Parameters provided",
    "description": "Registration is not approved by the Admin yet",
}

not_admin_401 = {
    "code": "UNAUTHORIZED",
    "title": "Admin Operation Called by Non-Admin User",
    "description": "Seems you don't have sufficient permissions to perform the operation",
}

restricted_self_operation_401 = {
    "code": "UNAUTHORIZED",
    "title": "Admin Operation called for self user",
    "description": "Seems you don't have sufficient permissions to perform the operation",
}

bad_request_400 = {
    "code": "VALIDATION_ERROR",
    "title": "Invalid Parameters provided",
    "description": "Seems the provided input is not validated by the system",
}

not_found_404 = {
    "code": "RESOURCE_NOT_FOUND",
    "title": "Resource not found",
    "description": "Seems the object which you are trying to find is not available",
}

user_conflict_409 = {
    "code": "CONFLICT",
    "title": "User already Exists",
    "description": "A user with that identity already exists",
}

entity_conflict_409 = {
    "code": "CONFLICT",
    "title": "Entity already Exists",
    "description": "An entity with the same identity already exists",
}

already_approved_409 = {
    "code": "CONFLICT",
    "title": "User already Approved",
    "description": "A user with that identity already approved",
}

email_already_verified_409 = {
    "code": "CONFLICT",
    "title": "Email already Verified",
    "description": "A user with that identity already verified",
}

service_unavailable_503 = {
    "code": "SERVICE_UNAVAILABLE",
    "title": "Service unavailable",
    "description": "One or more services are not available at the moment.",
}

unprocessable_entity_422 = {
    "code": "UNPROCESSABLE_ENTITY",
    "title": "Token Invalid",
    "description": "Request was well-formed but was unable to be followed due to semantic errors specify correct token",
}

precondition_failed_412 = {
    "code": "PRECONDITION_FAILED",
    "title": "Password precondition failed",
    "description": "'Password' policy not followed",
}

email_not_valid_412 = {
    "code": "EmailNotValidError",
    "title": "Email not valid",
    "description": "Provided value is not a valid email address.",
}

errors_collection = {
    400: bad_request_400,
    401: expired_jwt_401,
    404: not_found_404,
    409: entity_conflict_409,
    412: precondition_failed_412,
    422: unprocessable_entity_422,
    500: uncaught,
    503: service_unavailable_503,
}
