from django.urls import include, path

from .apis import posts, subscription

app_name = "blog"

urlpatterns = [
    path("post/", view=posts.PostApi.as_view(), name="post"),
    path("post/<slug:slug>", view=posts.PostDetailApi.as_view(), name="post_detail"),
]
