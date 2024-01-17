from django.db.models import QuerySet
from django.utils.text import slugify

from social_network.blog.models import Post
from social_network.users.models import BaseUser


def create_post(*, user: BaseUser, title: str, content: str) -> QuerySet[Post]:
    post = Post.objects.create(
        slug=slugify(title),
        title=title,
        content=content,
        auther=user,
    )
    return post
