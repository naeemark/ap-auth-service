from tests.base_test import setUp_tearDown
from tests.base_test import setUpClass

from models.user import UserModel


def test_crud(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app_context")():
        # create
        user = UserModel("xyz", "abc!23(")
        user.save_to_db()
        assert bool(UserModel.find_by_email("xyz"))
        assert bool(UserModel.find_by_id(1))

        # update
        user.password = "abc!@@jhda"
        user.save_to_db()
        assert user.password != "abc!23("

        # delete
        user.delete_from_db()
        assert not bool(UserModel.find_by_email("xyz")), "User should be deleted"
