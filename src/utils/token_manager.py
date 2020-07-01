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


def blacklist_tokens(raw_jwt):
    """common method to black list token"""
    blacklist_manager = BlacklistManager()
    props = get_payload_properties(raw_jwt)
    expire_sec_access_token = get_expire_time_seconds(props["jwt_exp"])
    blacklist_manager.revoke_token(props["identity"], props["jti"], expire_sec_access_token)
    refresh_expiry_sec = get_expire_time_seconds(props["refreshTokenExpire"])
    blacklist_manager.revoke_token(props["identity"], props["refreshTokenId"], refresh_expiry_sec)
