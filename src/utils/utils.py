"""
    A misc utility file
"""
import datetime


def add_parser_headers_argument(parser=None, arg_name=None, arg_type=str, location="headers"):
    """Adds argument for header validations"""
    parser.add_argument(arg_name, type=arg_type, location=location)


def add_parser_argument(parser=None, arg_name=None, arg_type=str):
    """Adds argument for param validations"""
    parser.add_argument(arg_name, type=arg_type)


def get_expire_time_seconds(jwt_exp):
    """tells the remaining expire time of token"""
    token_expire_time = datetime.datetime.fromtimestamp(jwt_exp)
    current_time = datetime.datetime.now()
    time_difference = token_expire_time - current_time
    return time_difference.seconds


def get_payload_properties(payload):
    """common function that returns common payload properties used to revoke or logout token"""
    identity = payload["identity"]
    identity_device_id = identity["deviceId"]

    payload_properties = {"identity": identity_device_id, "jwt_exp": payload["exp"], "jti": payload["jti"]}

    refresh_token_id = identity["refreshTokenId"]
    refresh_token_exp = identity["refreshTokenExpire"]
    payload_properties.update({"refreshTokenExpire": refresh_token_exp, "refreshTokenId": refresh_token_id})

    return payload_properties
