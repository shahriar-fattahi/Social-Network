from django.db.models import QuerySet

from social_network.blog.models import Subscription
from social_network.users.models import BaseUser


def get_subscribers(*, user: BaseUser) -> QuerySet[Subscription]:
    return Subscription.objects.filter(subscriber=user)
