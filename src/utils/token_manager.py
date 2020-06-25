"""Token creation"""
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import decode_token
from src.utils.blacklist_manager import BlacklistManager
from src.utils.utils import get_expire_time_seconds
from src.utils.utils import get_payload_properties


def get_jwt_tokens(payload=None, fresh=True):
    """creates and return jwt token in a dictionary"""
    refresh_token = create_refresh_token(identity=payload)
    refresh_token_id = decode_token(refresh_token)["jti"]
    refresh_token_exp = decode_token(refresh_token)["exp"]
    payload.update({"refreshTokenId": refresh_token_id, "refreshTokenExpire": refresh_token_exp})
    access_token = create_access_token(identity=payload, fresh=fresh)
    return {"accessToken": access_token, "refreshToken": refresh_token}


def blacklist_token(payload, logout=False):
    """common method to black list token"""
    blacklist_manager = BlacklistManager()
    payload_properties = get_payload_properties(payload, logout)
    expire_sec_access_token = get_expire_time_seconds(payload_properties["jwt_exp"])
    blacklist_manager.revoke_token(payload_properties["identity"], payload_properties["jti"], expire_sec_access_token)
    if logout:
        expire_sec_refresh_token = get_expire_time_seconds(payload_properties["refreshTokenExpire"])
        blacklist_manager.revoke_token(
            payload_properties["identity"], payload_properties["refreshTokenId"], expire_sec_refresh_token
        )
