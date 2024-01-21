from django.test import TestCase

from social_network.users.services import register


class TestRegister(TestCase):
    def test_register(self):
        user = register(bio="test", email="test@test.com", password="password")
        self.assertEqual(str(user), "test@test.com")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("password"))
        self.assertEqual(str(user.profile), "test@test.com >> test")
        self.assertEqual(user.profile.posts_count, 0)
        self.assertEqual(user.profile.followers_count, 0)
        self.assertEqual(user.profile.followings_count, 0)
