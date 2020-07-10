"""
  User Common Resource
"""
from datetime import datetime

from src.models.black_list import BlacklistModel as Blacklist
from src.utils.token_manager import get_jwt_tokens


def create_response_data(device_id=None, user=None):
    """Common Method to create response data"""

    payload = {"user": user, "deviceId": device_id}
    response_data = get_jwt_tokens(payload=payload)

    response_data["user"] = user
    return response_data


def blacklist_auth(raw_jwt):
    """Sends auth Tokens to blacklist"""
    id_access_token = raw_jwt["jti"]
    ttl_access_token = datetime.fromtimestamp(raw_jwt["exp"]).timestamp()

    id_refresh_token = raw_jwt["identity"]["refreshTokenId"]
    ttl_refresh_token = datetime.fromtimestamp(raw_jwt["identity"]["refreshTokenExpire"]).timestamp()

    Blacklist(token_id=id_access_token, type="access", time_to_live=ttl_access_token).save()
    Blacklist(token_id=id_refresh_token, type="refresh", time_to_live=ttl_refresh_token).save()
