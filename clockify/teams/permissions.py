from rest_framework import permissions
from authentication.permissons import IsUserAuthenticated
class IsObjectWorkerOrSupervisor(permissions.BasePermission):

    def has_permission(self, request, view):
        return IsUserAuthenticated.has_permission()
    def has_object_permission(self, request, view, obj):
        
        is_worker= obj.assigned_to= request.user
         
        is_supervisor = obj.team and obj.team.supervisor == request.user 
        return is_worker or is_supervisor
    