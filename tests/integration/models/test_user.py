from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("xyz", "fwaefawe")

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username("xyz"))
            self.assertIsNotNone(UserModel.find_by_id(1))

            user.delete_from_db()
            self.assertIsNone(UserModel.find_by_username("xyz"), "User should be deleted")
