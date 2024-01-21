from django.test import TestCase
from rest_framework.exceptions import APIException

from social_network.blog.models import Subscription
from social_network.blog.services.subscriptions import subscribe, unsubscribe
from social_network.users.tests.factories import BaseUser, BaseUserFactory


class TestUnsubscribe(TestCase):
    def setUp(self) -> None:
        self.user1 = BaseUserFactory.create(email="user1@test.com")
        self.user2 = BaseUserFactory.create(email="user2@test.com")
        self.subscription = subscribe(user=self.user1, email="user2@test.com")

    def test_user_not_exist(self):
        with self.assertRaises(APIException):
            unsubscribe(user=self.user2, email="not@exist.com")

    def test_subscription_not_exist(self):
        BaseUserFactory.create(email="user3@test.com")
        self.assertTrue(BaseUser.objects.filter(email="user3@test.com").exists())
        with self.assertRaises(APIException):
            unsubscribe(user=self.user1, email="user3@test.com")

    def test_delete(self):
        self.assertTrue(
            Subscription.objects.filter(subscriber=self.user1, target=self.user2)
        )
        unsubscribe(user=self.user1, email="user2@test.com")
        self.assertFalse(
            Subscription.objects.filter(subscriber=self.user1, target=self.user2)
        )
