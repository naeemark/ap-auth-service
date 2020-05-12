import json

from models.user import UserModel
from constant.exception import Exception
from constant.success_message import USER_CREATION
from tests.base_test import setUp_tearDown, setUpClass


def test_register_user(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app")() as c:
        with setUp_tearDown.get("app_context")():
            r = c.post('/register', data={'email': 'john12@gmail.com', 'password': '123!!@@AB'})

            assert r.status_code == 201
            assert bool(UserModel.find_by_email('john12@gmail.com'))
            assert USER_CREATION == json.loads(r.data)['message']


def test_register_and_login(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app")() as c:
        with setUp_tearDown.get("app_context")():
            c.post('/register', data={'email': 'john12@gmail.com', 'password': '123!!@@AB'})
            auth_request = c.post('/login', data=json.dumps({
                'email': 'john12@gmail.com',
                'password': '123!!@@AB'
            }), headers={'Content-Type': 'application/json'})

        assert 'access_token' in json.loads(auth_request.data).keys()


def test_register_duplicate_user(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app")() as c:
        with setUp_tearDown.get("app_context")():
            c.post('/register', data={'email': 'john12@gmail.com', 'password': '123!!@@AB'})
            r = c.post('/register', data={'email': 'john12@gmail.com', 'password': '123!!@@AB'})

            assert r.status_code == 400
            assert Exception.USER_ALREDY_EXSIST == json.loads(r.data)['message']


def test_password(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app")() as c:
        with setUp_tearDown.get("app_context")():
            c.post('/register', data={'email': 'john12@gmail.com', 'password': '123!!@@AB123'})

            # to get access token
            auth_request = c.post('/login', data=json.dumps({
                'email': 'john12@gmail.com',
                'password': '123!!@@AB123'
            }), headers={'Content-Type': 'application/json'})
            access_token = json.loads(auth_request.data)['access_token']

            # to get password changed
            password_update_request = c.put('/change-password', data=json.dumps({
                'new_password': '123!!@@AB12'
            }), headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'})

        assert password_update_request.status_code == 200
        assert "password_strength" in json.loads(password_update_request.data).keys()


def test_authentication_password_update(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app")() as c:
        with setUp_tearDown.get("app_context")():
            c.post('/register', data={'email': 'john12@gmail.com', 'password': '123!!@@AB123'})

            # to request for changing password
            password_update_request = c.put('/change-password', data=json.dumps({
                'new_password': '123!!@@AB12'
            }), headers={'Content-Type': 'application/json'})

        assert password_update_request.status_code == 401
