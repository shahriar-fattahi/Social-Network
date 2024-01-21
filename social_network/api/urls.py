from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include("social_network.authentication.urls", namespace="authentication"),
    ),
    path("users/", include("social_network.users.urls", namespace="users")),
    path("blog/", include(("social_network.blog.urls", "blog"))),
]
