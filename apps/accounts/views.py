from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, LogoutSerializer, RefreshSerializer


class LoginView(APIView):
    """View for user login."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle POST request for user login."""
        serializer = LoginSerializer(data=request.data, context={"request": request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        try:
            refresh = RefreshToken.for_user(user)
        except TypeError:
            return Response(
                {"error": "Token generation failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "accessToken": str(refresh.access_token),
                "refreshToken": str(refresh),
                "expiresIn": int(
                    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
                ),
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )


class RefreshView(APIView):
    """View for refreshing JWT tokens."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle POST request to refresh JWT tokens."""
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """View for user logout."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Handle POST request for user logout."""
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
