"""
  User Common Resource
"""
from src.utils.token_manager import get_jwt_tokens


def create_response_data(device_id=None, user=None):
    """Common Method to create response data"""

    payload = {"user": user, "deviceId": device_id}
    response_data = get_jwt_tokens(payload=payload)

    response_data["user"] = user
    return response_data
