from django.test import TestCase

from social_network.users.tests.factories import BaseUserFactory


class TestProfileModel(TestCase):
    def setUp(self) -> None:
        self.user = BaseUserFactory(email="test@test.com", profile__bio="test")

    def test_str_return(self):
        self.assertEqual(str(self.user.profile), "test@test.com >> test")
