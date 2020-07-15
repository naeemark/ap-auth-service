"""
  User Common Resource
"""
import os
import uuid
from datetime import datetime
from datetime import timedelta

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from src.models.black_list import BlacklistModel as Blacklist
from src.utils.logger import info
from src.utils.utils import get_epoch_timestamp


def get_user_claim():
    """creates and return jwt user claim dict"""

    expires_access_at = datetime.now() + timedelta(minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"]))
    expires_refresh_at = datetime.now() + timedelta(days=int(os.environ["JWT_REFRESH_TOKEN_EXPIRES_DAYS"]))
    return {
        "access_token_id": str(uuid.uuid4()),
        "refresh_token_id": str(uuid.uuid4()),
        "expires_access_at": int(expires_access_at.timestamp()),
        "expires_refresh_at": int(expires_refresh_at.timestamp()),
    }


def get_jwt_tokens(payload=None):
    """creates and return jwt token in a dictionary"""

    user_claims = get_user_claim()
    info(user_claims)
    access_token = create_access_token(identity=payload, fresh=True, user_claims=user_claims)
    refresh_token = create_refresh_token(identity=payload, user_claims=user_claims)
    tokens_dict = {"accessToken": access_token, "refreshToken": refresh_token}
    info(tokens_dict)
    return tokens_dict


def get_web_auth_jwt_token(payload=None):
    """Create JWT token for email link"""
    expires_delta = timedelta(minutes=int(os.environ["JWT_WEB_AUTH_TOKEN_EXPIRES_MINUTES"]))
    expires_at = datetime.now() + expires_delta

    user_claims = {"access_token_id": str(uuid.uuid4()), "expires_access_at": int(expires_at.timestamp())}

    jwt_token = create_access_token(identity=payload, expires_delta=expires_delta, user_claims=user_claims)
    info(jwt_token)
    return jwt_token


def create_response_data(device_id=None, user=None):
    """Common Method to create response data"""

    payload = {"user": user, "deviceId": device_id}
    response_data = get_jwt_tokens(payload=payload)

    response_data["user"] = user
    return response_data


def blacklist_token(token_id=None, token_type=None, time_to_live=get_epoch_timestamp()):
    """Sends auth Tokens to blacklist"""
    Blacklist(token_id=token_id, type=token_type, time_to_live=time_to_live).save()


def blacklist_auth(jwt_claims):
    """Sends auth Tokens to blacklist"""

    id_access_token = jwt_claims["access_token_id"]
    ttl_access_token = jwt_claims["expires_access_at"]
    blacklist_token(token_id=id_access_token, token_type="access", time_to_live=ttl_access_token)

    id_refresh_token = jwt_claims["refresh_token_id"]
    ttl_refresh_token = jwt_claims["expires_refresh_at"]
    blacklist_token(token_id=id_refresh_token, token_type="refresh", time_to_live=ttl_refresh_token)
