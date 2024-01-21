from django.test import TestCase

from social_network.blog.models import Subscription
from social_network.blog.selectors.posts import posts_list
from social_network.blog.tests.factories import PostFactory
from social_network.users.tests.factories import BaseUserFactory


class TestPostLists(TestCase):
    def setUp(self) -> None:
        self.user1 = BaseUserFactory.create(email="user1@test.com")
        self.user2 = BaseUserFactory.create(email="user2@test.com")
        self.post1 = PostFactory.create_batch(4, auther=self.user1)
        self.post2 = PostFactory.create_batch(4, auther=self.user2)

    def test_posts_list(self):
        posts = posts_list(user=self.user1)
        self.assertEqual(list(self.post1), list(posts))
        Subscription.objects.create(subscriber=self.user1, target=self.user2)
        posts = posts_list(user=self.user1)
        self.assertEqual(list(self.post1) + list(self.post2), list(posts))
