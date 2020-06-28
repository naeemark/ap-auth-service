"""
  Response Messages Constants
"""
import os

USER_CREATION = "User Register Successful"
UPDATED_PASSWORD = "Password updated successfully"
LOGGED_IN = "User Login Successful"
REFRESH_TOKEN_REVOKED = "Refresh token revoked successfully"
LOGOUT = "Successfully logged out"
REFRESH_SESSION = "Refresh Session"
VALIDATE_SESSION = "Validate Session"

HEADERS_INCORRECT = "Invalid Headers"
REDIS_CONNECTION = "Redis Connectivity Error: {}".format(os.environ["REDIS_HOST"])
HEADERS_REQUIRED = "'{properties}' is required"
INVALID_CREDENTIAL = "Invalid email or password"
DATABASE_CONNECTION = "Database Connectivity Error: {}".format(os.environ["DB_URL"])
DUPLICATE_USER = "Email already registered"
REDIS_CONNECTION = "Redis Connectivity Error: {}".format(os.environ["REDIS_HOST"])
TOKEN_EXPIRED = "Token has expired"
TOKEN_REVOKED = "Token has been revoked"
FRESH_TOKEN = "Login required"
PROPERTY_REQUIRED = "Params `{required_properties}` required"
PASSWORD_CONDITION = "'Password' policy not followed"
CREDENTIAL_REQUIRED = "Credentials Required"
EMAIL_CONDITION = "'email' is not valid"
PASSWORD_POLICY = "Password must have {policy}"
REUSE_PASSWORD_ERROR = "Can not reset the same password"
