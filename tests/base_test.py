import pytest

from app import app
from db import db


@pytest.fixture(scope='module')
def setUpClass():
    SQLALCHEMY_DATABASE_URI = "sqlite:////sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['DEBUG'] = False
    with app.app_context():
        db.init_app(app)


@pytest.yield_fixture()
def setUp_tearDown():
    with app.app_context():
        db.create_all()
        application = app.test_client
        app_context = app.app_context
        yield {"app": application, "app_context": app_context}

        db.session.remove()
        db.drop_all()
