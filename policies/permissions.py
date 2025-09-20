from rest_framework.permissions import BasePermission


class IsJWTAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, "jwt_payload") and request.jwt_payload is not None
