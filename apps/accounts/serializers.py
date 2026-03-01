from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


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
