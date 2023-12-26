from django.urls import path, include

urlpatterns = [
    # path('blog/', include(('social_network.blog.urls', 'blog')))
    path(
        "auth/",
        include("social_network.authentication.urls", namespace="authentication"),
    ),
    path("users/", include("social_network.users.urls", namespace="users")),
]
