"""Token creation"""
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token


def get_token(identity, fresh=False):
    """creates token"""
    access_token = create_access_token(identity=identity, fresh=fresh)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token
