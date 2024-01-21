from django.db.models import QuerySet

from social_network.users.models import BaseUser

from ..filters import PostFilter
from ..models import Post, Subscription


def posts_list(*, user: BaseUser, filters=None) -> QuerySet[Post]:
    filters = filters or {}
    followings = list(
        Subscription.objects.filter(subscriber=user).values_list("target", flat=True)
    )
    followings.append(user.id)
    query = Post.objects.filter(auther__in=followings)
    if not followings:
        return Post.objects.none()
    return PostFilter(filters, query).qs


def post_detail(*, slug, user: BaseUser) -> Post:
    followings = list(
        Subscription.objects.filter(subscriber=user).values_list("target", flat=True)
    )
    followings.append(user.id)
    return Post.objects.get(slug=slug, auther__in=followings)
