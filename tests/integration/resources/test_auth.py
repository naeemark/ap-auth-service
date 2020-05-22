"""
 A file to contain all auth tests of
    UserResource
"""


def test_refresh_with_access_token(test_client, prefix, session, test_database):
    """request refresh with access token"""
    response_refresh_token = test_client.post(
        f"{prefix}/auth/refreshToken", headers={"Authorization": f"Bearer {session}"},
    )
    assert response_refresh_token.status_code == 422
    assert len(test_database.metadata.sorted_tables[0].columns) == 3
