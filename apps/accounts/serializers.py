from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            request=self.context.get("request"),
            email=data.get("email"),
            password=data.get("password"),
        )

        if not user:
            raise AuthenticationFailed({"detail": "Invalid email or password"})

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled")

        return user


class RefreshSerializer(serializers.Serializer):
    """
    Serializer for refreshing JWT tokens."""

    refreshToken = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get("refreshToken")

        try:
            refresh = RefreshToken(refresh_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired refresh token")

        return {
            "accessToken": str(refresh.access_token),
            "expiresIn": int(
                settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
            ),
        }


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout."""

    refreshToken = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get("refreshToken")

        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except Exception:
            raise AuthenticationFailed("Invalid or expired refresh token")

        return {"detail": "Logout successful"}
