from __future__ import unicode_literals
import inspect
from functools import reduce
from rest_framework.settings import api_settings

class ResourcePermisison:
    '''
    Base class for manage all resource permission.

    global_perms: represents total access permision to resource
    minimal_perms: represents minimal permission to be applied 
                   on resource level (resource is represented by
                   viewset objects)
    '''

    global_perms = None
    minimal_perms = None
    list_perms = None
    retrieve_perms = None
    create_perms = None
    update_perms = None
    destroy_perms = None

    def __init__(self):
        if self.global_perms and self.minimal_perms:
            self.global_perms & self.minimal_perms

    def check_permissions(self, request, view):
        '''
        Check class based view permission (like ModelViewset)
        '''
        permset = self.initialize_permset()
        if permset:
            return permset.check_permissions(request, view)
        return True

    def check_action_permissions(self, request, action):
        '''
        Check permission for specific endpoint represented by method.
        :param endpoint: method name that represents endpoint
        '''
        permset = self.initialize_permset(action)
        if permset:
            return permset.check_action_permissions(request, action)
        return True

    def check_object_permissions(self, request, action, obj):
        '''
        Check permisison to specific resource (object instance).
        '''
        permset = self.initialize_permset(action)
        if permset:
            return permset.check_object_permissions(request, action, obj)
        return True

    def initialize_permset(self, action=None):
        if action:
            permset = getattr(self, f'{action}_perms', None)
        else:
            permset = self.minimal_perms

        if isinstance(permset, (list, tuple)):
            permset = reduce(lambda x, y: x & y, permset)
        elif inspect.isclass(permset):
            if not issubclass(permset, PermissionComponent):
                raise AttributeError("perms objects must be 'PermissionComponent' type.")
            else:
                permset = permset()
        
        if self.minimal_perms:
            permset = (permset & self.minimal_perms) if permset else self.minimal_perms
        if self.global_perms:
            permset = (permset | self.global_perms) if permset else self.global_perms
        return permset
            


class PermissionComponent:

    def check_permissions(self, request, view):
        raise NotImplementedError('children classes must implement this method')

    def check_action_permissions(self, request, action):
        raise NotImplementedError('children classes must implement this method')

    def check_object_permissions(self, request, action, obj):
        raise NotImplementedError('children classes must implement this method')

    def __invert__(self):
        return Not(self)

    def __and__(self, component):
        return And(self, component)

    def __or__(self, component):
        return Or(self, component)


class PermissionOperator(PermissionComponent):
    
    def __init__(self, *components):
        self.components = tuple(components)


class And(PermissionOperator):

    def check_permissions(self, request, view):
        value = True
        for perm_component in self.components:
            value = value & perm_component.check_permissions(request, view)
            if not value:
                break
        return value

    def check_action_permissions(self, request, action):
        value = True
        for perm_component in self.components:
            value = value & perm_component.check_action_permissions(request, action)
            if not value:
                break
        return value

    def check_object_permissions(self, request, action, obj):
        value = True
        for perm_component in self.components:
            value = value & perm_component.check_object_permissions(request, action, obj)
            if not value:
                break
        return value


class Or(PermissionOperator):

    def check_permissions(self, request, view):
        value = False
        for perm_component in self.components:
            value = value | perm_component.check_permissions(request, view)
            if value:
                break
        return value

    def check_action_permissions(self, request, action):
        value = False
        for perm_component in self.components:
            value = value | perm_component.check_action_permissions(request, action)
            if value:
                break
        return value

    def check_object_permissions(self, request, action, obj):
        value = False
        for perm_component in self.components:
            value = value | perm_component.check_object_permissions(request, action, obj)
            if value:
                break
        return value


class Not(PermissionComponent):

    def check_permissions(self, request, view):
        return not self.check_permissions[0](request, view)

    def check_action_permissions(self, request, action):
        return not self.check_action_permissions[0](request, action)

    def check_object_permissions(self, request, action, obj):
        return not self.check_object_permissions[0](request, action, obj)