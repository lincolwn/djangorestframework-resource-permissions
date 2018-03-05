from tests.app.models import Office, Issue
from django.contrib.auth.models import User
from resource_permissions.permissions import ResourcePermisison, \
    PermissionComponent
from resource_permissions.components import IsAdminUser, IsAuthenticated, \
    IsSuperUser, DenyAll

class IsManager(PermissionComponent):
    
    message = 'User is not office manager'

    def check_permissions(self, request, view):
        return Office.objects.filter(manager=request.user).exists()

    def check_action_permissions(self, request, action):
        return Office.objects.filter(manager=request.user).exists()

    def check_object_permissions(self, request, action, obj):
        return obj.manager == request.user


class IsOwner(PermissionComponent):
    
    message = 'User is not issue owner.'

    def check_permissions(self, request, view):
        return Issue.objects.filter(owner=request.user).exists()

    def check_action_permissions(self, request, action):
        return Issue.objects.filter(owner=request.user).exists()

    def check_object_permissions(self, request, action, obj):
        return obj.owner == request.user


class IsManagerOfficeOwner(PermissionComponent):
    
    message = 'User is not manager of issue office.'

    def check_permissions(self, request, view):
        return Office.objects.filter(manager=request.user).exists()

    def check_action_permissions(self, request, action):
        return Office.objects.filter(manager=request.user).exists()

    def check_object_permissions(self, request, action, obj):
        return obj.office.manager == request.user


class IsSimpleUser(PermissionComponent):
    
    message = 'User is simple user'

    def check_permissions(self, request, view):
        return not Office.objects.filter(manager=request.user).exists() and \
            not request.user.is_staff and not request.user.is_superuser

    def check_action_permissions(self, request, action):
        return not Office.objects.filter(manager=request.user).exists() and \
            not request.user.is_staff and not request.user.is_superuser

    def check_object_permissions(self, request, action, obj):
        return not Office.objects.filter(manager=request.user).exists() and \
            not request.user.is_staff and not request.user.is_superuser
    


class OfficePermissions(ResourcePermisison):
    global_perms = IsSuperUser() | IsAdminUser()
    minimal_perms = IsAuthenticated()
    create_perms = ~IsSimpleUser()
    update_perms = partial_update_perms = IsManager()
    destroy_perms = IsManager()



class IssuePermissions(ResourcePermisison):
    minimal_perms = IsAuthenticated()
    update_perms = partial_update_perms = (IsOwner() | IsManagerOfficeOwner() | 
        IsSuperUser() | IsAdminUser())
    start_perms = (IsOwner() | IsManagerOfficeOwner() | 
        IsSuperUser() | IsAdminUser())
    finish_perms = (IsOwner() | IsManagerOfficeOwner() | 
        IsSuperUser() | IsAdminUser())
    cancel_perms = IsManagerOfficeOwner() | IsSuperUser() | IsAdminUser() 
    destroy_perms = DenyAll()