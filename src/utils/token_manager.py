"""Token creation"""
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from src.utils.blacklist_manager import BlacklistManager
from src.utils.utils import get_expire_time_seconds
from src.utils.utils import get_payload_properties


def get_jwt_tokens(payload=None, fresh=True):
    """creates and return jwt token in a dictionary"""
    access_token = create_access_token(identity=payload, fresh=fresh)
    refresh_token = create_refresh_token(identity=payload)

    return {"accessToken": access_token, "refreshToken": refresh_token}


def blacklist_token(payload):
    """common method to black list token"""
    identity, jwt_exp, jti = get_payload_properties(payload)
    expire_time_sec = get_expire_time_seconds(jwt_exp)
    BlacklistManager().revoke_token(identity, jti, expire_time_sec)
