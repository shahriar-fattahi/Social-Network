from django.test import TestCase

from social_network.blog.services.posts import create_post
from social_network.users.tests.factories import BaseUserFactory


class TestCratePost(TestCase):
    def setUp(self) -> None:
        self.user = BaseUserFactory.create()

    def test_str_return(self):
        self.assertEqual(self.user.profile.posts_count, 0)
        post = create_post(user=self.user, title="Title post", content="Content post")
        self.assertEqual(str(post), "title-post")
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.posts_count, 1)
