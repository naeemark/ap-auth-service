"""Token creation"""
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token


def get_jwt_tokens(payload=None, fresh=True):
    """creates and return jwt token in a dictionary"""
    access_token = create_access_token(identity=payload, fresh=fresh)
    refresh_token = create_refresh_token(identity=payload)

    return {"accessToken": access_token, "refreshToken": refresh_token}
