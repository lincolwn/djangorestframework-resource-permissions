from .permissions import PermissionComponent
from django.contrib.auth.models import AnonymousUser

class IsSuperUser(PermissionComponent):
    
    def check_permissions(self, request, view):
        return request.user.is_superuser

    def check_action_permissions(self, request, action):
        return request.user.is_superuser

    def check_object_permissions(self, request, action):
        return request.user.is_superuser


class IsAdminUser(PermissionComponent):

    def check_permissions(self, request, view):
        return request.user.is_staff

    def check_action_permissions(self, request, action):
        return request.user.is_staff

    def check_object_permissions(self, request, action):
        return request.user.is_staff


class IsAuthenticated(PermissionComponent):
    
    def check_permissions(self, request, view):
        return request.user.is_authenticated

    def check_action_permissions(self, request, action):
        return request.user.is_authenticated

    def check_object_permissions(self, request, action):
        return request.user.is_authenticated


class AllowAny(PermissionComponent):
    
    def check_permissions(self, request, view):
        return True

    def check_action_permissions(self, request, action):
        return True

    def check_object_permissions(self, request, action):
        return True