from django.test import TestCase

from social_network.blog.tests.factories import PostFactory
from social_network.users.tests.factories import BaseUserFactory


class TestPostModel(TestCase):
    def setUp(self) -> None:
        self.post = PostFactory.create(title=" Test Post ")

    def test_str_return(self):
        self.assertEqual(str(self.post), "test-post")

    def test_increase_posts_count(self):
        user = BaseUserFactory.create()
        self.assertEqual(user.profile.posts_count, 0)
        PostFactory.create(auther=user)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.posts_count, 1)

    def test_decrease_posts_count(self):
        user = BaseUserFactory.create()
        post = PostFactory.create(auther=user)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.posts_count, 1)
        post.delete()
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.posts_count, 0)
