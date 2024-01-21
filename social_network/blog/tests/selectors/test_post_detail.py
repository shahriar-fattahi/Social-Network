from django.test import TestCase

from social_network.blog.models import Subscription
from social_network.blog.selectors.posts import post_detail
from social_network.blog.tests.factories import Post, PostFactory
from social_network.users.tests.factories import BaseUserFactory


class TestPostDetail(TestCase):
    def setUp(self) -> None:
        self.user1 = BaseUserFactory.create(email="user1@test.com")
        self.user2 = BaseUserFactory.create(email="user2@test.com")
        self.post1 = PostFactory.create(title="test-post1", auther=self.user1)
        self.post2 = PostFactory.create(title="test-post2", auther=self.user2)

    def test_post_detail(self):
        post = post_detail(slug="test-post1", user=self.user1)
        self.assertEqual(self.post1, post)
        with self.assertRaises(Post.DoesNotExist):
            post_detail(slug="test-post2", user=self.user1)
        Subscription(subscriber=self.user1, target=self.user2)
        post = post_detail(slug="test-post2", user=self.user2)
        self.assertEqual(self.post2, post)
