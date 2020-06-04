"""fixtures defined for unit test"""
import datetime
import os

import fakeredis
import pytest
from src import create_app


@pytest.fixture(scope="module")
def test_context():
    """unit test instance for app and redis"""
    redis_instance = fakeredis.FakeStrictRedis()
    flask_app = create_app("flask_test.cfg")
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
        minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"])
    )
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(
        days=int(os.environ["JWT_REFRESH_TOKEN_EXPIRES_DAYS"])
    )
    yield flask_app, redis_instance
    del flask_app
    del redis_instance
