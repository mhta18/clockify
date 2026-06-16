from rest_framework.permissions import BasePermission
from authentication.permissions import IsUserAuthenticated


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return (
            IsUserAuthenticated.has_permission(self, request, view)
            and request.user.is_admin
        )
