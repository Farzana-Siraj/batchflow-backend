from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminRole(BasePermission):
    """
    Allows access only to users with ADMIN role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsAdminOrReviewer(BasePermission):
    """
    Allows access to ADMIN and REVIEWER roles.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "ADMIN",
            "REVIEWER",
        ]


class AdminOrReadOnly(BasePermission):
    """
    Read-only for REVIEWER.
    Full access for ADMIN.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return request.user.role in ["ADMIN", "REVIEWER"]

        return request.user.role == "ADMIN"
