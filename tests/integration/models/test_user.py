from models.user import UserModel
from tests.base_test import setUp_tearDown, setUpClass


def test_crud(setUp_tearDown, setUpClass):
    with setUp_tearDown.get("app_context")():
        user = UserModel("xyz", "fwaefawe")

        user.save_to_db()
        assert bool(UserModel.find_by_username("xyz"))
        assert bool(UserModel.find_by_id(1))

        user.delete_from_db()
        assert not bool(UserModel.find_by_username("xyz")), "User should be deleted"
