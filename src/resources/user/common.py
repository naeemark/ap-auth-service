"""
  User Common Resource
"""
from src.utils.token_manager import get_jwt_tokens


def create_response_data(device_id=None, user=None):
    """Common Method to create response data"""

    user_data = {"email": user.email, "name": user.name}

    payload = {"user": user_data, "deviceId": device_id}
    response_data = get_jwt_tokens(payload=payload)

    response_data["user"] = user_data
    return response_data
