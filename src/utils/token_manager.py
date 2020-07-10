"""Token creation"""
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import decode_token


def get_jwt_tokens(payload=None, fresh=True):
    """creates and return jwt token in a dictionary"""
    refresh_token = create_refresh_token(identity=payload)
    refresh_token_id = decode_token(refresh_token)["jti"]
    refresh_token_exp = decode_token(refresh_token)["exp"]
    payload.update({"refreshTokenId": refresh_token_id, "refreshTokenExpire": refresh_token_exp})
    access_token = create_access_token(identity=payload, fresh=fresh)
    return {"accessToken": access_token, "refreshToken": refresh_token}
