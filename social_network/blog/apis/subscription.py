from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from social_network.api.mixins import ApiAuthMixin
from social_network.api.pagination import LimitOffsetPagination, get_paginated_response
from social_network.blog.models import Subscription
from social_network.blog.selectors.subscriptions import get_subscribers
from social_network.blog.services.subscriptions import subscribe, unsubscribe


class SubscribeApi(ApiAuthMixin, APIView):
    class pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSubscribeSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=100)

    class OutputSubscribeSerializer(serializers.ModelSerializer):
        email = serializers.SerializerMethodField("get_email")
        bio = serializers.SerializerMethodField("get_bio")

        class Meta:
            model = Subscription
            fields = ["email", "bio"]

        def get_email(self, obj):
            return obj.target.email

        def get_bio(self, obj):
            return obj.target.profile.bio

    @extend_schema(
        request=InputSubscribeSerializer,
        responses=OutputSubscribeSerializer,
    )
    def post(self, request):
        serializer = self.InputSubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            subscription = subscribe(
                user=request.user, email=serializer.validated_data.get("email")
            )
        except Exception as ex:
            return Response(
                data={"Detail": "Database error -> " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        output_serializer = self.OutputSubscribeSerializer(instance=subscription)
        return Response(
            data=output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses=OutputSubscribeSerializer,
    )
    def get(self, request):
        try:
            subscribers = get_subscribers(user=request.user)
        except Exception as ex:
            return Response(
                data={"detail": "Filter error -> " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return get_paginated_response(
            pagination_class=self.pagination,
            serializer_class=self.OutputSubscribeSerializer,
            queryset=subscribers,
            request=request,
            view=self,
        )


class UnsubscribeApi(ApiAuthMixin, APIView):
    class InputUnsubscribeSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=100)

    def delete(self, request):
        serializer = self.InputUnsubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            unsubscribe(user=request.user, email=serializer.validated_data.get("email"))
        except Exception as ex:
            return Response(
                data={"detail": "Database error -> " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(f"{serializer.validated_data.get('email')} was unsubscribed.")
