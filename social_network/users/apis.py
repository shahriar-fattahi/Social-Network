from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from social_network.api.mixins import ApiAuthMixin
from social_network.users.models import BaseUser, Profile
from social_network.users.selectors import get_profile
from social_network.users.services import register

from .validators import letter_validator, number_validator, special_char_validator


class ProfileApi(ApiAuthMixin, APIView):
    class OutPutProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = (
                "bio",
                "posts_count",
                "followers_count",
                "followings_count",
            )

    @extend_schema(responses=OutPutProfileSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(
            self.OutPutProfileSerializer(query, context={"request": request}).data
        )


class RegisterApi(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(
            validators=[
                number_validator,
                letter_validator,
                special_char_validator,
                MinLengthValidator(limit_value=10),
            ]
        )
        confirm_password = serializers.CharField(max_length=255)
        bio = serializers.CharField(max_length=1000, required=False)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already taken")
            return email

        def validate(self, attrs):
            if not attrs.get("password") or not attrs.get("confirm_password"):
                raise serializers.ValidationError(
                    "Please fill password and confirm password"
                )

            if attrs.get("password") != attrs.get("confirm_password"):
                raise serializers.ValidationError(
                    "confirm password is not equal to password"
                )
            return attrs

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser
            fields = ("email", "token", "created_at", "updated_at")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                bio=serializer.validated_data.get("bio"),
            )
        except Exception as ex:
            return Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        return Response(
            self.OutPutRegisterSerializer(user, context={"request": request}).data
        )
