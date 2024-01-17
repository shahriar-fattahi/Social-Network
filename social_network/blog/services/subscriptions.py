from rest_framework.exceptions import APIException

from social_network.blog.models import Subscription
from social_network.users.models import BaseUser


def subscribe(*, user: BaseUser, email: str) -> Subscription:
    try:
        target = BaseUser.objects.get(email=email)
    except BaseUser.DoesNotExist:
        raise APIException("User does not exists")

    return Subscription.objects.create(
        subscriber=user,
        target=target,
    )


def unsubscribe(*, user: BaseUser, email: str):
    try:
        target = BaseUser.objects.get(email=email)
    except BaseUser.DoesNotExist:
        raise APIException("User does not exists")

    try:
        subscription = Subscription.objects.get(subscriber=user, target=target)
    except Subscription.DoesNotExist:
        raise APIException("Subscription does not exists")

    subscription.delete()
