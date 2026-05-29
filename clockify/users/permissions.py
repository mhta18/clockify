from rest_framework.permissions import BasePermission
from authentication.permissons import IsUserAuthenticated

class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and IsUserAuthenticated.has_permission()
