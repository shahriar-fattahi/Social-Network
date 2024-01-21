from django.test import TestCase

from social_network.blog.models import Subscription
from social_network.users.tests.factories import BaseUserFactory


class TestSubscriptionModel(TestCase):
    def setUp(self) -> None:
        self.subscriber = BaseUserFactory.create(email="subscriber@test.com")
        self.target = BaseUserFactory.create(email="target@test.com")
        self.subscription = Subscription.objects.create(
            subscriber=self.subscriber, target=self.target
        )
        self.target.profile.refresh_from_db()
        self.subscriber.profile.refresh_from_db()

    def test_return(self):
        self.assertEqual(
            str(self.subscription), "subscriber@test.com -> target@test.com"
        )

    def test_change_subscriptions_count(self):
        self.assertEqual(self.target.profile.followers_count, 1)
        self.assertEqual(self.target.profile.followings_count, 0)
        self.assertEqual(self.subscriber.profile.followers_count, 0)
        self.assertEqual(self.subscriber.profile.followings_count, 1)
        self.subscription.delete()
        self.target.profile.refresh_from_db()
        self.subscriber.profile.refresh_from_db()
        self.assertEqual(self.target.profile.followers_count, 0)
        self.assertEqual(self.target.profile.followings_count, 0)
        self.assertEqual(self.subscriber.profile.followers_count, 0)
        self.assertEqual(self.subscriber.profile.followings_count, 0)
