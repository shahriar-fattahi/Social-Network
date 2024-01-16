from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from social_network.api.mixins import ApiAuthMixin
from social_network.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response_context,
)
from social_network.blog.models import Post
from social_network.blog.selectors.posts import post_detail, posts_list
from social_network.blog.services.posts import create_post


class PostApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        auther__in = serializers.CharField(required=False, max_length=100)
        created_at__range = serializers.CharField(required=False, max_length=100)
        title = serializers.CharField(required=False, max_length=100)

    class InputPostSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        content = serializers.CharField(max_length=1000)

    class OutputPostSerializer(serializers.ModelSerializer):
        url = serializers.SerializerMethodField(("get_url"))

        class Meta:
            model = Post
            fields = ["title", "url"]

        def get_url(self, obj):
            request = self.context.get("request")
            path = reverse("api:blog:post_detail", args=(obj.slug,))
            return request.build_absolute_uri(path)

    @extend_schema(
        request=InputPostSerializer,
        responses=OutputPostSerializer,
    )
    def post(self, request):
        serializer = self.InputPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_post(
                user=request.user,
                title=serializer.validated_data.get("title"),
                content=serializer.validated_data.get("content"),
            )
        except Exception as ex:
            return Response(
                data={"detail": "Database Error -> " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=self.OutputPostSerializer(
                query,
                context={"request": request},
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        parameters=[FilterSerializer],
        responses=OutputPostSerializer,
    )
    def get(self, request):
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        try:
            posts = posts_list(
                user=request.user,
                filters=filter_serializer.validated_data,
            )
        except Exception as ex:
            return Response(
                data={"detail": f"Filter error -> {ex}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutputPostSerializer,
            queryset=posts,
            request=request,
            view=self,
        )


class PostDetailApi(ApiAuthMixin, APIView):
    class OutputPostDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ["auther", "title", "slug", "content", "created_at", "updated_at"]

    @extend_schema(
        responses=OutputPostDetailSerializer,
    )
    def get(self, request, slug):
        try:
            post = post_detail(
                slug=slug,
                user=request.user,
            )
        except Exception as ex:
            return Response(
                data={"Filter error ->" + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.OutputPostDetailSerializer(instance=post)
        return Response(serializer.data)
