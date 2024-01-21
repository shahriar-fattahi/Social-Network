from django.test import TestCase

from social_network.users.tests.factories import BaseUserFactory


class TestBaseUserModel(TestCase):
    def setUp(self) -> None:
        self.user = BaseUserFactory(email="test@test.com")

    def test_str_return(self):
        self.assertEqual(str(self.user), "test@test.com")
