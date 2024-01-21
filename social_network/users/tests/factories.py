import factory
from django.db.models.signals import post_save
from faker import Faker

from social_network.users.models import BaseUser, Profile


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    posts_count = 0
    followers_count = 0
    followings_count = 0
    bio = Faker().unique.sentence(nb_words=10, variable_nb_words=False)
    user = factory.SubFactory(
        "social_network.users.tests.factories.UserFactory", profile=None
    )


@factory.django.mute_signals(post_save)
class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseUser

    class Params:
        uid = Faker().random_number(digits=3)

    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
    is_admin = False
    is_active = True

    profile = factory.RelatedFactory(ProfileFactory, factory_related_name="user")

    @factory.lazy_attribute
    def email(self):
        email = str(self.uid) + Faker().unique.free_email()
        return email
