from werkzeug.security import safe_str_cmp

from models.user import UserModel
from tests.base_test import setUp_tearDown, setUpClass


def test_create_user(setUp_tearDown, setUpClass):
    user = UserModel("xyz", "hvhj!@#")

    assert safe_str_cmp(user.username, 'xya'), "incorrect username"
    assert safe_str_cmp(user.password, "hvhj!@#"), "incorrect password"


def test_item_json(setUp_tearDown, setUpClass):
    user = UserModel("xyz", "hvhj!@#")
    expected = {
        'username': 'xyz',
        'password': 'hvhj!@#'
    }
    similar_records = expected.items() & user.json().items()
    assert len(similar_records) == len(expected), f"expected {expected}"


def test_update_password(setUp_tearDown, setUpClass):
    user = UserModel("xyz", "hvhj!@#")
    user.password = "abc!@@jhda"
    user.save_to_db()
    assert user.password != 'abc!23('
