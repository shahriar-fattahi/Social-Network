from django.test import TestCase

from social_network.users.services import create_user


class TestCreateUser(TestCase):
    def test_create_user(self):
        user = create_user(email="test@test.com", password="password")
        self.assertEqual(str(user), "test@test.com")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("password"))
