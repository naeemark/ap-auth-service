"""
 A file to contain all auth tests of
    UserResource
"""
import json

from src.constant.success_message import ACCESS_REVOKED


def test_refresh_with_access_token(test_client, api_prefix, session, test_database):
    """request refresh with access token"""
    response_refresh_token = test_client.post(
        f"{api_prefix}/auth/refreshToken", headers={"Authorization": f" {session[0]}"},
    )
    assert response_refresh_token.status_code == 422
    assert len(test_database.metadata.sorted_tables[0].columns) == 3


def test_refresh_token(test_client, api_prefix, session, test_database):
    """request refresh with refresh token"""
    response_refresh_token = test_client.post(
        f"{api_prefix}/auth/refreshToken", headers={"Authorization": f" {session[1]}"},
    )
    assert response_refresh_token.status_code == 200
    assert "access_token" in json.loads(response_refresh_token.data).keys()
    assert len(test_database.metadata.sorted_tables[0].columns) == 3


def test_revoke_access(api_prefix, test_client, session):
    """revoke access"""

    response_revoke = test_client.post(
        f"{api_prefix}/auth/revokeAccess",
        headers={"Authorization": f"{session[0]}", "Content-Type": "application/json"},
    )
    assert response_revoke.status_code == 200
    assert json.loads(response_revoke.data)["message"] == ACCESS_REVOKED


def test_revoke_access_without_token(api_prefix, test_client):
    """revoke access without token"""

    response_revoke = test_client.post(f"{api_prefix}/auth/revokeAccess")
    assert response_revoke.status_code == 401
