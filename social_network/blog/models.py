from django.db import models
from django.core.exceptions import ValidationError
from social_network.common.models import BaseModel
from django.contrib.auth import get_user_model
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_DELETE
from django.db.models import F


class Post(BaseModel, LifecycleModel):
    slug = models.SlugField(
        primary_key=True,
        max_length=100,
    )
    title = models.CharField(
        unique=True,
        max_length=100,
    )
    contnet = models.CharField(
        max_length=1000,
    )
    auther = models.ForeignKey(
        get_user_model(),
        related_name="posts",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.slug

    @hook(AFTER_CREATE)
    def increase_posts_count(self):
        if self.auther.profile:
            self.auther.profile.posts_count = F("posts_count") + 1
            self.auther.profile.save()

    @hook(AFTER_DELETE)
    def decrease_posts_count(self):
        if self.auther.profile:
            self.auther.profile.posts_count = F("posts_count") - 1
            self.auther.profile.save()


class Subscription(BaseModel):
    subscriber = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="followings",
    )
    target = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        unique_together = ("subscriber", "target")

    def clean(self) -> None:
        if self.subscriber == self.target:
            raise ValidationError("subscriber can not equal to target")

    def __str__(self) -> str:
        return f"{self.subscriber} -> {self.target}"
