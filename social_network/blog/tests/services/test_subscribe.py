from django.test import TestCase
from rest_framework.exceptions import APIException

from social_network.blog.services.subscriptions import subscribe
from social_network.users.tests.factories import BaseUserFactory


class TestSubscribe(TestCase):
    def setUp(self) -> None:
        self.user1 = BaseUserFactory.create(email="user1@test.com")
        self.user2 = BaseUserFactory.create(email="user2@test.com")

    def test_limit(self):
        self.user1.profile.followings_count = 100
        with self.assertRaises(APIException):
            subscribe(user=self.user1, email="user2@test.com")

    def test_user_not_exist(self):
        with self.assertRaises(APIException):
            subscribe(user=self.user2, email="not@exist.com")

    def test_return(self):
        subscription = subscribe(user=self.user1, email="user2@test.com")
        self.assertEqual(subscription.subscriber, self.user1)
        self.assertEqual(subscription.target, self.user2)
