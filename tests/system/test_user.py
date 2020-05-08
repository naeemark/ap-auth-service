import json

from models.user import UserModel
from tests.base_test import setUp_tearDown, setUpClass


def test_register_user(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app")() as c:
        with setUp_tearDown.get("app_context")():
            r = c.post('/register', data={'username': 'test', 'password': '1234'})

            assert r.status_code == 201
            assert bool(UserModel.find_by_username('test'))
            assert 'User created successfully.' == json.loads(r.data)['message']


def test_register_and_login(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app")() as c:
        with setUp_tearDown.get("app_context")():
            c.post('/register', data={'username': 'test', 'password': '1234'})
            auth_request = c.post('/auth', data=json.dumps({
                'username': 'test',
                'password': '1234'
            }), headers={'Content-Type': 'application/json'})

        assert 'access_token' in json.loads(auth_request.data).keys()


def test_register_duplicate_user(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app")() as c:
        with setUp_tearDown.get("app_context")():
            c.post('/register', data={'username': 'test', 'password': '1234'})
            r = c.post('/register', data={'username': 'test', 'password': '1234'})

            assert r.status_code == 400
            assert 'A user with that username already exists' == json.loads(r.data)['message']
