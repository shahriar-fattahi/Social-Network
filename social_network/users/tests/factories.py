import factory
from faker import Faker

from social_network.users.models import BaseUser


class BaseUserFactory(factory.django.DjangoModelFactory):
    email = Faker().unique.free_email()
    password = factory.django.Password("password")
    is_admin = False
    is_active = True

    class Meta:
        model = BaseUser
