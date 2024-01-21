from django.test import TestCase

from social_network.users.services import create_profile, create_user


class TestCreateProfile(TestCase):
    def setUp(self) -> None:
        self.user = create_user(email="test@test.com", password="password")

    def test_create_profile(self):
        profile = create_profile(user=self.user, bio="test")
        self.assertEqual(str(profile), "test@test.com >> test")
        self.assertEqual(profile.posts_count, 0)
        self.assertEqual(profile.followers_count, 0)
        self.assertEqual(profile.followings_count, 0)
