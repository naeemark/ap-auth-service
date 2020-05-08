from unittest import TestCase
from models.user import UserModel


class ModelTest(TestCase):

    def test_create_user(self):
        user = UserModel("xyz", "hvhj!@#")

        self.assertEqual(user.username, 'xyz', "incorrect username")
        self.assertEqual(user.password, 'hvhj!@#', "incorrect password")

    def test_item_json(self):
        user = UserModel("xyz", "hvhj!@#")
        expected = {
            'username': 'xyz',
            'password': 'hvhj!@#'
        }

        self.assertEqual(user.json(), expected, f"expected {expected}")
