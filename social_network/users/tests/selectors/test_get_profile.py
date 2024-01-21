from django.test import TestCase

from social_network.users.selectors import get_profile
from social_network.users.services import register


class TestGetProfile(TestCase):
    def setUp(self) -> None:
        self.user = register(bio="test", email="test@test.com", password="password")

    def test_get_profile(self):
        profile = get_profile(user=self.user)
        self.assertEqual(profile, self.user.profile)
